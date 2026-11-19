# Investigação 02 — Login Admin

Alvo: `http://10.0.80.3:3000`. Modelo local usado pelo agente:
`qwen2.5:1.5b`. Fonte desta etapa: transcrição da sessão no Kali enviada pelo
usuário nesta conversa. O arquivo `agent/logs/session.jsonl` original permanece
no Kali; seu conteúdo integral não foi recebido nem inspecionado aqui.

## Hipótese e comparação planejada

Hipótese T16 do plano humano: entradas de login podem alterar a consulta e
permitir uma sessão administrativa sem a senha correta. O controle é um POST
com credenciais fictícias inválidas; uma tentativa modificada deve ser comparada
com ele. Uma falha de autenticação, sozinha, não confirma injeção.

## Sessão de controle observada

1. O operador pediu ao agente uma única requisição POST com credenciais
   inválidas, antes da tentativa modificada.
2. O modelo propôs `curl` com `--data-raw "{}"`, sem URL. O agente bloqueou a
   proposta por não identificar o alvo autorizado.
3. O operador escolheu modificar e forneceu POST em `/rest/user/login`, com
   JSON contendo `email=naoexiste@example.invalid` e uma senha fictícia.
4. A ferramenta retornou código de saída 0, corpo
   `Invalid email or password.` e `HTTP_STATUS:401`. O status foi registrado
   explicitamente pelo agente; o código de saída 0 apenas indica que o curl
   executou sem erro de transporte.
5. O modelo propôs outra requisição de login com credenciais inválidas. O
   operador rejeitou a repetição com `R`, encerrando a sessão.

## Interpretação provisória

O controle demonstrou rejeição de credenciais inválidas nessa condição. Não
houve ainda tentativa modificada nem sessão administrativa demonstrada; a
hipótese segue **não avaliada** quanto ao bypass. A proposta incompleta do
modelo, o bloqueio, a modificação humana e a repetição rejeitada são evidências
da supervisão e de limitações do modelo local. A saída compartilhada na conversa
contém artefatos de escape e autolink; este documento registra o comportamento
observado, sem assumir que a formatação da conversa seja idêntica ao JSONL bruto.

## Tentativas posteriores e falha do fluxo

Uma sessão posterior usou literalmente os marcadores
`VALOR_DE_EMAIL_DO_TESTE` e `VALOR_DE_SENHA_DO_TESTE`. Ela também retornou 401,
mas não representa o teste de injeção planejado. Em outra sessão, o operador
colou uma hipótese longa com quebras de linha. A versão anterior do agente leu
apenas a primeira linha; o restante entrou como respostas aos menus, causando
`Decisão inválida` e novas propostas do modelo. O operador interrompeu com
`Ctrl+C` enquanto aguardava Ollama. Essa transcrição não mostra execução de uma
requisição modificada com entrada de injeção, portanto não comprova bypass nem
ausência dele.

O agente foi alterado para ler a hipótese até `FIM`, executar no máximo uma
ação por sessão e pedir interpretação após o resultado. Essa mudança precisa
ser enviada ao Kali e validada no laboratório antes de retomar T16.

## Próxima coleta

Executar uma única tentativa modificada supervisionada e registrar status HTTP,
identidade devolvida e decisão humana. O agente deve omitir tokens e senhas na
saída compartilhada. Somente a comparação entre controle e tentativa modificada
permitirá concluir a investigação.
