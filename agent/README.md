# Agente supervisionado

Este agente conecta o modelo local do Ollama a duas ferramentas autorizadas,
`curl` e `nmap`, para investigar somente o Juice Shop em `10.0.80.3:3000`.
Cada proposta exige aprovação humana antes da execução. As interações são
registradas em `agent/logs/session.jsonl`.

## Pré-requisitos no Kali

- VPN ativa e `http://10.0.80.3:3000` respondendo;
- Ollama ativo em `http://127.0.0.1:11434`;
- modelo local disponível, por exemplo `qwen2.5:0.5b`;
- `curl`, `nmap` e Python 3.

## Execução

Na raiz do projeto:

```bash
python3 agent/main.py
```

O agente começa com uma hipótese fornecida pelo operador, pede uma proposta ao
modelo, mostra a ação e oferece `a` (aprovar), `m` (modificar) ou `r` (rejeitar).
Após uma execução aprovada, o resultado é enviado ao modelo para orientar a
próxima proposta.
