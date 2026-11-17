#!/usr/bin/env python3
"""Agente mínimo e supervisionado para o Juice Shop local."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import time
from pathlib import Path
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
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False}).encode()
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
    joined = " ".join(args)
    if any(value in joined for value in ["10.0.80.3:3000", "10.0.80.3"]):
        return []
    if tool == "curl" and any(value.startswith("http://") or value.startswith("https://") for value in args):
        return ["curl deve apontar para o Juice Shop autorizado."]
    if tool == "nmap" and TARGET not in args:
        return ["nmap deve apontar somente para 10.0.80.3."]
    return ["A proposta não identifica o alvo autorizado."]


def execute(proposal: dict[str, object]) -> tuple[int, str]:
    tool = proposal["tool"]
    args = proposal["args"]
    assert isinstance(tool, str) and isinstance(args, list)
    command = [tool, *args]
    completed = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    output = (completed.stdout + completed.stderr)[-12000:]
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
        "Para curl use URL completa no alvo autorizado; para nmap use 10.0.80.3 "
        "e, preferencialmente, uma porta explícita. Não proponha ações destrutivas."
    )
    messages = [{"role": "system", "content": system}, {"role": "user", "content": hypothesis}]
    record("session_started", model=MODEL, target=BASE_URL, hypothesis=hypothesis)

    while True:
        try:
            raw = ask_ollama(messages)
            proposal = extract_proposal(raw)
            errors = validate(proposal)
            record("proposal", raw=raw, proposal=proposal, validation_errors=errors)
            print(json.dumps(proposal, ensure_ascii=False, indent=2))
            if errors:
                print("BLOQUEADA:", "; ".join(errors))
                decision = "r"
            else:
                decision = input("[a]provar, [m]odificar, [r]ejeitar: ").strip().lower()
            if decision == "r":
                record("human_decision", decision="rejected")
                print("Proposta rejeitada. Encerrando esta sessão.")
                return 0
            if decision == "m":
                modified = input("Informe a proposta JSON modificada: ").strip()
                proposal = extract_proposal(modified)
                errors = validate(proposal)
                record("human_decision", decision="modified", proposal=proposal, validation_errors=errors)
                if errors:
                    print("Modificação bloqueada:", "; ".join(errors))
                    return 2
            elif decision != "a":
                print("Decisão inválida.")
                continue
            else:
                record("human_decision", decision="approved")
            code, output = execute(proposal)
            record("tool_result", tool=proposal["tool"], args=proposal["args"], returncode=code, output=output)
            print(f"\nResultado (código {code}):\n{output}")
            messages.extend([
                {"role": "assistant", "content": json.dumps(proposal, ensure_ascii=False)},
                {"role": "user", "content": f"Resultado da ferramenta (código {code}):\n{output}"},
            ])
        except (OSError, ValueError, json.JSONDecodeError, KeyError) as error:
            record("error", error=repr(error))
            print(f"Erro controlado: {error}")
            return 1


if __name__ == "__main__":
    raise SystemExit(main())
