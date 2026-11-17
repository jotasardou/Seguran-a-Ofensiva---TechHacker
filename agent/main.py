#!/usr/bin/env python3
"""Agente mínimo e supervisionado para o Juice Shop local."""

from __future__ import annotations

import json
import os
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


def record(event: str, **data: object) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    item = {"time": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "event": event, **data}
    with LOG.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(item, ensure_ascii=False) + "\n")


def ask_ollama(messages: list[dict[str, str]]) -> str:
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False, "format": "json"}).encode()
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
    if options not in ([], ["-I"], ["-I", "--connect-timeout", "5"], ["--connect-timeout", "5"]):
        return ["Opções curl não autorizadas; POST só é permitido em /rest/user/login."]
    return []


def public_proposal(proposal: dict[str, object]) -> dict[str, object]:
    """Remove a senha da proposta antes de exibir ou registrar."""
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
    safe["args"] = args
    return safe


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


def read_modified_proposal() -> str:
    print("Cole o JSON em uma linha ou em várias linhas; encerre com uma linha contendo apenas FIM.")
    lines: list[str] = []
    while True:
        line = input("JSON> ")
        if line.strip() == "FIM":
            return "\n".join(lines)
        lines.append(line)


def execute(proposal: dict[str, object]) -> tuple[int, str]:
    tool = proposal["tool"]
    args = proposal["args"]
    assert isinstance(tool, str) and isinstance(args, list)
    command = [tool, *args]
    if tool == "curl" and "--data-raw" in args:
        command += ["-w", "\nHTTP_STATUS:%{http_code}"]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    output = (completed.stdout + completed.stderr)[-12000:]
    if tool == "curl" and "--data-raw" in args:
        output = public_result(output)
    return completed.returncode, output


def main() -> int:
    hypothesis = input("Hipótese inicial: ").strip()
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
        "Não proponha ações destrutivas."
    )
    messages = [{"role": "system", "content": system}, {"role": "user", "content": hypothesis}]
    record("session_started", model=MODEL, target=BASE_URL, hypothesis=hypothesis)

    while True:
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
                modified = read_modified_proposal()
                proposal = extract_proposal(modified)
                errors = validate(proposal)
                record("human_decision", decision="modified", proposal=public_proposal(proposal), validation_errors=errors)
                if errors:
                    print("Modificação bloqueada:", "; ".join(errors))
                    return 2
            elif decision != "a":
                print("Decisão inválida.")
                continue
            else:
                record("human_decision", decision="approved")
            code, output = execute(proposal)
            record("tool_result", tool=proposal["tool"], args=public_proposal(proposal)["args"], returncode=code, output=output)
            print(f"\nResultado (código {code}):\n{output}")
            messages.extend([
                {"role": "assistant", "content": json.dumps(public_proposal(proposal), ensure_ascii=False)},
                {"role": "user", "content": f"Resultado da ferramenta (código {code}):\n{output}"},
            ])
        except (OSError, ValueError, json.JSONDecodeError, KeyError) as error:
            record("error", error=repr(error))
            print(f"Erro controlado: {error}")
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
