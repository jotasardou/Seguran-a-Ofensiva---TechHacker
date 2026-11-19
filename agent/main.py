#!/usr/bin/env python3
"""Agente mínimo e supervisionado para o Juice Shop local."""

from __future__ import annotations

import json
import os
import re
import shlex
import subprocess
import time
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


TARGET = "10.0.80.3"
BASE_URL = f"http://{TARGET}:3000"
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")
LOG = Path(__file__).with_name("logs") / "session.jsonl"
BEARER_SECRET = re.compile(r"(Authorization: Bearer )[A-Za-z0-9._~-]+")


def redact_bearer(value: object) -> object:
    if isinstance(value, str):
        return BEARER_SECRET.sub(r"\1[REDACTED]", value)
    if isinstance(value, list):
        return [redact_bearer(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_bearer(item) for key, item in value.items()}
    return value


def record(event: str, **data: object) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    item = redact_bearer({"time": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "event": event, **data})
    with LOG.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(item, ensure_ascii=False) + "\n")


INTERPRETATION_SCHEMA = {
    "type": "object",
    "properties": {field: {"type": "string"} for field in ("interpretacao", "limite", "proximo_passo")},
    "required": ["interpretacao", "limite", "proximo_passo"],
    "additionalProperties": False,
}


def ask_ollama(messages: list[dict[str, str]], *, format: str | dict = "json") -> str:
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False, "format": format}).encode()
    request = Request(OLLAMA_URL, data=body, headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=120) as response:
        payload = json.loads(response.read())
    return payload["message"]["content"]


def extract_proposal(text: str) -> dict[str, object]:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("O modelo não retornou um objeto JSON.")
    proposal = json.loads(text[start : end + 1])
    if proposal.get("tool") not in {"curl", "nmap"}:
        raise ValueError("Ferramenta fora da lista autorizada.")
    args = proposal.get("args")
    if isinstance(args, str):
        proposal["args"] = shlex.split(args)
    elif not isinstance(args, list) or not all(isinstance(x, str) for x in args):
        raise ValueError("args deve ser uma lista ou texto de argumentos.")
    return proposal


def validate(proposal: dict[str, object]) -> list[str]:
    tool = proposal["tool"]
    args = proposal["args"]
    assert isinstance(tool, str) and isinstance(args, list)
    if tool == "nmap":
        return [] if args == ["-p", "3000", TARGET] else ["Use exatamente: -p 3000 10.0.80.3."]
    if not args:
        return ["curl precisa de uma URL autorizada."]
    url = args[-1]
    try:
        parsed = urlsplit(url)
        allowed_url = (parsed.scheme == "http" and parsed.hostname == TARGET
                       and parsed.port == 3000 and not parsed.username
                       and not parsed.password and not parsed.fragment)
    except ValueError:
        allowed_url = False
    if not allowed_url:
        return ["A URL deve apontar somente para http://10.0.80.3:3000."]
    options = args[:-1]
    if url == BASE_URL + "/rest/user/login" and len(options) == 7 and options[:6] == [
        "-sS", "-X", "POST", "-H", "Content-Type: application/json", "--data-raw"
    ]:
        try:
            body = json.loads(options[6])
        except json.JSONDecodeError:
            return ["O corpo do login precisa ser JSON válido."]
        if (isinstance(body, dict) and set(body) == {"email", "password"}
                and all(isinstance(value, str) and len(value) <= 256 for value in body.values())):
            return []
        return ["O login aceita apenas email e password como textos de até 256 caracteres."]
    feedback_path = parsed.path
    is_feedback_collection = feedback_path == "/api/Feedbacks"
    is_feedback_item = re.fullmatch(r"/api/Feedbacks/[1-9][0-9]*", feedback_path) is not None
    if is_feedback_collection or is_feedback_item:
        if parsed.query:
            return ["Rotas de feedback não aceitam parâmetros de consulta."]
        if len(options) not in (3, 5) or options[:2] != ["-sS", "-H"]:
            return ["Use somente -sS e o cabeçalho Authorization autorizado para feedbacks."]
        header = options[2]
        token = header.removeprefix("Authorization: Bearer ")
        if not re.fullmatch(r"[A-Za-z0-9._~-]+", token):
            return ["Feedbacks exigem Authorization: Bearer com token válido e sem espaços."]
        if is_feedback_collection and len(options) == 3:
            return []
        if is_feedback_item and options[3:] == ["-X", "DELETE"]:
            return []
        return ["Feedbacks permitem apenas GET /api/Feedbacks ou DELETE /api/Feedbacks/<id>."]
    if feedback_path.startswith("/api/Feedbacks"):
        return ["Rota de feedback não autorizada."]
    if options not in ([], ["-I"], ["-I", "--connect-timeout", "5"], ["--connect-timeout", "5"]):
        return ["Opções curl não autorizadas; POST só é permitido em /rest/user/login."]
    return []


def public_proposal(proposal: dict[str, object]) -> dict[str, object]:
    """Remove credenciais da proposta antes de exibir ou registrar."""
    safe = dict(proposal)
    args = list(proposal["args"])
    if "--data-raw" in args:
        index = args.index("--data-raw") + 1
        if index < len(args):
            try:
                body = json.loads(args[index])
                if isinstance(body, dict) and "password" in body:
                    body["password"] = "[REDACTED]"
                    args[index] = json.dumps(body, ensure_ascii=False)
            except json.JSONDecodeError:
                args[index] = "[REDACTED]"
    for index, arg in enumerate(args):
        if arg.startswith("Authorization: Bearer "):
            args[index] = "Authorization: Bearer [REDACTED]"
    safe["args"] = args
    return redact_bearer(safe)


def public_result(output: str) -> str:
    """Resume respostas de login sem expor tokens de autenticação."""
    try:
        response, status = output.rsplit("\nHTTP_STATUS:", 1)
        data = json.loads(response)
        if isinstance(data, dict) and isinstance(data.get("authentication"), dict):
            auth = data["authentication"]
            return f'HTTP_STATUS:{status.strip()}\nauthentication: umail={auth.get("umail")}, token=[REDACTED]'
        if isinstance(data, dict) and data.get("status") == "totp_token_required":
            return f"HTTP_STATUS:{status.strip()}\nstatus: totp_token_required; tmpToken=[REDACTED]"
    except (ValueError, json.JSONDecodeError):
        pass
    return output


def parse_interpretation(raw: str) -> dict[str, str]:
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("Interpretação não é JSON válido.") from error
    expected = set(INTERPRETATION_SCHEMA["required"])
    if (not isinstance(result, dict) or set(result) != expected
            or not all(isinstance(result[key], str) and result[key].strip() for key in expected)):
        raise ValueError("Interpretação deve conter somente interpretacao, limite e proximo_passo como textos não vazios.")
    return result


def read_block(label: str) -> str:
    print(f"Cole {label} em uma linha ou em várias linhas; termine com FIM sozinho em uma linha.")
    lines: list[str] = []
    while True:
        line = input(f"{label}> ")
        if line.strip() == "FIM":
            return "\n".join(lines)
        lines.append(line)


def execute(proposal: dict[str, object]) -> tuple[int, str]:
    tool = proposal["tool"]
    args = proposal["args"]
    assert isinstance(tool, str) and isinstance(args, list)
    command = [tool, "-q", *args] if tool == "curl" else [tool, *args]
    if tool == "curl" and ("--data-raw" in args or "Authorization: Bearer " in "\n".join(args)):
        command += ["-w", "\nHTTP_STATUS:%{http_code}"]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    output = (completed.stdout + completed.stderr)[-12000:]
    for arg in args:
        if arg.startswith("Authorization: Bearer "):
            output = output.replace(arg.removeprefix("Authorization: Bearer "), "[REDACTED]")
    if tool == "curl" and "--data-raw" in args:
        output = public_result(output)
    return completed.returncode, output


def main() -> int:
    try:
        hypothesis = read_block("Hipótese").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada encerrada sem executar ferramenta.")
        return 0
    if not hypothesis:
        print("A hipótese é obrigatória.")
        return 2
    system = (
        "Você é um analista de segurança supervisionado. O único alvo autorizado é "
        f"{BASE_URL}. Ferramentas disponíveis: curl e nmap. "
        "Responda SOMENTE JSON com os campos tool, args e rationale. "
        "args deve conter apenas argumentos, sem o nome da ferramenta. "
        "Para curl use URL completa no alvo autorizado; para nmap use exatamente "
        "args [\"-p\", \"3000\", \"10.0.80.3\"]. Para testar login, curl aceita "
        "-sS -X POST -H 'Content-Type: application/json' --data-raw com JSON "
        "email/password e URL /rest/user/login. Uma tentativa por proposta. "
        "Para feedbacks, use token de conta comum somente no cabeçalho "
        "Authorization: Bearer; é permitido GET /api/Feedbacks para consultar ou "
        "DELETE /api/Feedbacks/<id> para excluir um único ID numérico. "
        "Não use outros cabeçalhos, rotas ou métodos. Não proponha outras ações "
        "destrutivas além desse DELETE estritamente limitado."
    )
    messages = [{"role": "system", "content": system}, {"role": "user", "content": hypothesis}]
    record("session_started", model=MODEL, target=BASE_URL, hypothesis=hypothesis)

    try:
            raw = ask_ollama(messages)
            proposal = extract_proposal(raw)
            errors = validate(proposal)
            record("proposal", proposal=public_proposal(proposal), validation_errors=errors)
            print(json.dumps(public_proposal(proposal), ensure_ascii=False, indent=2))
            if errors:
                print("BLOQUEADA:", "; ".join(errors))
                decision = input("[m]odificar ou [r]ejeitar: ").strip().lower()
            else:
                decision = input("[a]provar, [m]odificar, [r]ejeitar: ").strip().lower()
            if decision == "r":
                record("human_decision", decision="rejected")
                print("Proposta rejeitada. Encerrando esta sessão.")
                return 0
            if decision == "m":
                modified = read_block("JSON")
                proposal = extract_proposal(modified)
                errors = validate(proposal)
                record("human_decision", decision="modified", proposal=public_proposal(proposal), validation_errors=errors)
                if errors:
                    print("Modificação bloqueada:", "; ".join(errors))
                    return 2
            elif decision != "a":
                print("Decisão inválida.")
                return 2
            else:
                record("human_decision", decision="approved")
            code, output = execute(proposal)
            record("tool_result", tool=proposal["tool"], args=public_proposal(proposal)["args"], returncode=code, output=output)
            print(f"\nResultado (código {code}):\n{output}")
            interpretation_raw = ask_ollama([
                {"role": "system", "content": "Analise o resultado já obtido. Responda somente JSON com interpretacao, limite e proximo_passo. Não proponha ferramentas ou comandos nem afirme vulnerabilidade sem evidência."},
                {"role": "user", "content": f"Hipótese: {hypothesis}\nResultado da ferramenta {proposal['tool']} (código {code}):\n{output}"},
            ], format=INTERPRETATION_SCHEMA)
            try:
                interpretation = parse_interpretation(interpretation_raw)
            except ValueError as error:
                record("interpretation_invalid", reason=str(error), text=interpretation_raw)
                print(f"Interpretação inválida: {error}")
                return 2
            record("interpretation", text=interpretation)
            print(f"\nInterpretação do modelo:\n{json.dumps(interpretation, ensure_ascii=False)}")
            print("Sessão encerrada após uma execução supervisionada.")
            return 0
    except (OSError, ValueError, json.JSONDecodeError, KeyError, subprocess.TimeoutExpired) as error:
        record("error", error=repr(error))
        print(f"Erro controlado: {redact_bearer(str(error))}")
        return 1
    except (EOFError, KeyboardInterrupt):
        record("session_interrupted")
        print("\nSessão interrompida sem executar nova ferramenta.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
