# Investigação 01 — Confidential Document

Data: 17/11/2026. Alvo autorizado: Juice Shop local em
`http://10.0.80.3:3000`. Evidência recebida: transcrição do terminal do Kali
enviada pelo usuário nesta conversa. O log JSONL original permanece no Kali e
ainda não foi inspecionado neste repositório.

## Hipótese e estratégia

Hipótese T26 do plano humano: um documento confidencial pode ser acessado sem
autenticação. O agente usa o modelo local `qwen2.5:1.5b` para propor uma ação;
o operador aprova, modifica ou rejeita antes de `curl` executar a requisição.
O caminho `/ftp/acquisitions.md` já havia sido descoberto manualmente antes
desta investigação; a sessão do agente testa o acesso a essa URL conhecida.

## Sequência observada

1. O operador forneceu a hipótese e pediu uma requisição GET ao alvo autorizado.
2. O modelo propôs `curl` com apenas `/ftp/acquisitions.md`, sem origem HTTP.
3. O agente bloqueou a proposta porque ela não identificava o alvo permitido.
4. O operador escolheu `m` e forneceu
   `{"tool":"curl","args":["http://10.0.80.3:3000/ftp/acquisitions.md"]}`.
5. Após essa intervenção, a ferramenta retornou código de saída `0` e
   apresentou 909 bytes de conteúdo, incluindo o título `Planned Acquisitions`
   e a declaração `This document is confidential! Do not distribute!`.
6. Recebido o resultado, o modelo propôs novamente a mesma URL e afirmou que
   o conteúdo indicava acesso ao documento confidencial. Essa interpretação
   aparece na proposta seguinte, no campo `rational`; a transcrição não mostra
   um campo de conclusão independente. A decisão sobre repetir essa ação ainda
   não consta na saída recebida.

## Conclusão e limites

A evidência sustenta que o documento foi entregue a uma requisição `curl` sem
credenciais explícitas ou cookie de sessão. O trecho exibido declara a natureza
confidencial e descreve planos de aquisição. Isso é consistente com exposição
de documento sensível na instalação testada. A saída do agente não inclui os
cabeçalhos HTTP nem o código de status; o código de saída `0` de `curl` não deve
ser apresentado como se fosse `HTTP 200`. O usuário havia mostrado um `HTTP 200`
em uma exploração manual anterior, que é evidência distinta desta sessão.

O modelo falhou ao fornecer uma URL completa na primeira proposta; o bloqueio
e a correção humana impediram execução fora do formato autorizado. A sugestão
posterior repetiu uma requisição já bem-sucedida, caso útil para examinar
repetição e necessidade de intervenção no agente. A transcrição integral e o
registro de decisão final devem ser preservados para reconstruir o ciclo.

Próximas melhorias: registrar status HTTP junto ao corpo, distinguir uma
interpretação de resultado de uma nova proposta de ferramenta e testar
explicitamente o encerramento da investigação quando a evidência for suficiente.
