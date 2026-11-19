# Agente supervisionado

Este agente conecta o modelo local do Ollama a duas ferramentas autorizadas,
`curl` e `nmap`, para investigar somente o Juice Shop em `10.0.80.3:3000`.
Cada proposta exige aprovação humana antes da execução. As interações são
registradas em `agent/logs/session.jsonl`.

## Pré-requisitos no Kali

- VPN ativa e `http://10.0.80.3:3000` respondendo;
- Ollama ativo em `http://127.0.0.1:11434`;
- modelo local disponível, por exemplo `qwen2.5:1.5b`;
- `curl`, `nmap` e Python 3.

## Execução

Na raiz do projeto:

```bash
OLLAMA_MODEL=qwen2.5:1.5b python3 agent/main.py
```

O agente solicita a hipótese. Cole uma ou várias linhas e digite `FIM` sozinho
em uma linha para encerrá-la. Ele mostra a proposta e oferece `a` (aprovar),
`m` (modificar) ou `r` (rejeitar). Ao modificar, cole o JSON e encerre com
`FIM`. Após uma execução aprovada, o resultado é enviado ao modelo para
interpretação; a sessão termina após essa única ação. Para outra hipótese,
inicie uma nova sessão.

Para Login Admin, o `curl` aceita POST somente em `/rest/user/login`, com
`email` e `password` em JSON e uma tentativa por proposta. A resposta de
autenticação é resumida sem exibir o token, e senhas são omitidas do log.
Os arquivos em `agent/logs/` permanecem fora do Git. O operador deve revisar
propostas e resultados antes de compartilhar qualquer transcrição.
