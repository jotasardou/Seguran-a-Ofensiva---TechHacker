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

## Tentativa modificada supervisionada

Em 19/11/2026, após atualizar o Kali para a versão com validação estruturada da
interpretação, o operador iniciou uma nova sessão com uma única tentativa. Os
cinco eventos finais do JSONL original foram preservados no Kali e compartilhados
de forma sanitizada para conferência:

1. A hipótese mencionou explicitamente o controle anterior `HTTP 401` e pediu
   que o resultado fosse comparado com ele.
2. O modelo propôs um POST sem a URL. O agente bloqueou a proposta com o erro
   `A URL deve apontar somente para http://10.0.80.3:3000.`.
3. O operador escolheu `modified` e forneceu uma requisição para o endpoint
   autorizado, com uma entrada modificada no campo `email` e senha fictícia. A
   política local registrou `validation_errors: []` antes da execução.
4. Uma única chamada de `curl` foi executada. Ela retornou código de saída 0,
   `HTTP_STATUS:200` e `authentication: umail=admin@juice-sh.op,
   token=[REDACTED]`. A senha também foi omitida do registro compartilhado.
5. O modelo devolveu os três campos estruturados exigidos e a sessão foi
   encerrada sem executar outra ferramenta.

Os horários do log vão de `2026-11-19T07:12:21-0500` a
`2026-11-19T07:13:02-0500`. O fuso é preservado como registrado pelo Kali; não
foi convertido para o horário desta documentação.

## Comparação e conclusão

No controle, credenciais fictícias comuns produziram `HTTP_STATUS:401` e
`Invalid email or password.`. Na tentativa modificada, uma senha incorreta
acompanhada da entrada alterada no campo `email` produziu `HTTP_STATUS:200`, um
token e a identidade `admin@juice-sh.op`. A diferença observada sustenta, nesta
instância do laboratório, bypass de autenticação por injeção no campo `email` e
emissão de uma sessão identificada como administrativa.

O token não foi usado posteriormente para realizar uma operação administrativa.
Essa ausência limita a demonstração de privilégios efetivos após o login, mas
não elimina a evidência de que o próprio endpoint de autenticação emitiu token e
identidade administrativa sem a senha correta. Não foram feitas novas variações
do payload, pois a repetição não acrescentaria a comparação necessária.

## Avaliação da contribuição do modelo

O modelo chamou o resultado de possível *session hijacking* ou *session
takeover*. Essa classificação não é sustentada: nenhuma sessão preexistente foi
roubada; o servidor emitiu uma nova sessão após a entrada modificada. O modelo
também sugeriu consultar novamente o endpoint de login e repetir o teste com
outras entradas, embora a comparação planejada já estivesse completa.

O caso mostra simultaneamente contribuição e limitação da IA. O modelo gerou uma
proposta inicial incompleta, que a política bloqueou; a intervenção humana
corrigiu alvo e parâmetros; e a interpretação final teve formato válido, mas
conteúdo técnico parcialmente incorreto. A validação por esquema garantiu a
estrutura da resposta, não sua correção. As repetições sugeridas não foram
executadas.
