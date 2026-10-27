# Matriz de requisitos

Fonte: **AF - Tecnologias Hackers 26-2.pdf**, 11 páginas, lido integralmente.
O original fica na raiz local do projeto e não integra o versionamento inicial.
Esta matriz resume o enunciado; não substitui sua consulta.

Todos os requisitos abaixo estão **pendentes de implementação ou validação**.
Uma referência a uma etapa é planejamento, não evidência de conclusão.

| ID | Requisito | Critério de conclusão | Etapas | Fonte |
|---|---|---|---|---|
| R01 | Juice Shop local acessível pelo Kali | Acesso verificado e configuração documentada | 2 | §1, p. 2 |
| R02 | LLM local integrado ao programa | Execução local e comunicação demonstradas; modelo e configuração registrados | 4, 9 | §1, p. 2 |
| R03 | Pelo menos duas ferramentas, uma interagindo diretamente com o alvo | Ambas executadas pelo agente em condições autorizadas | 7–10 | §2, p. 4 |
| R04 | Supervisão humana | Autorizar, modificar e rejeitar demonstrados; execução apenas após autorização | 6, 10 | §§1–2, p. 3–4 |
| R05 | Decisão adaptativa | Evidências mostram resultados anteriores influenciando a próxima ação; não apenas sequência fixa | 9–14 | §2, p. 4–5 |
| R06 | Escopo restrito | Ferramentas e limites definidos; ações fora do Juice Shop local bloqueadas | 2, 5, 10 | §§1–2, p. 3–4 |
| R07 | Restauração | Procedimento retorna o Juice Shop a estado conhecido, com verificação | 2, 10, 14 | §1, p. 3 |
| R08 | Plano inicial sem LLM | Registro original do grupo com aspectos, hipóteses, ferramentas e evidências necessárias | 3 | §3, p. 5 |
| R09 | Revisão posterior pelo modelo | Sugestões e decisões de aceitar/modificar/rejeitar registradas com justificativas técnicas | Após 3 e antes de 11 | §3, p. 5 |
| R10 | Três investigações distintas | Cada uma registra hipótese, estratégia, contribuição do agente, execução, intervenção humana e conclusão | 11–13 | §4, p. 6–7 |
| R11 | Registros completos e consultáveis | Proposta, ferramenta, parâmetros, decisão humana, resultado, interpretação do modelo e decisão posterior reconstruíveis | 5–14 | §5, p. 7 |
| R12 | Conclusões sustentadas | Cada conclusão aponta para evidências; limitações e hipóteses rejeitadas são explícitas | 11–15 | §§4–5, p. 6–7 |
| R13 | Análise crítica da IA | Compara estratégia humana e contribuições do agente; examina adequação, adaptação, erros, repetição e intervenção | 14–15 | §6, p. 8 |
| R14 | Exemplo concreto de limitação, erro ou dificuldade | Caso realmente observado, como foi identificado e como foi tratado | 11–15 | §6, p. 8 |
| R15 | Laboratório reproduzível e código entregue | Instruções e configurações permitem executar alvo, modelo, agente e integrações | 14, 16 | §7, p. 9 |
| R16 | Relatório de 4–6 páginas | Arquitetura, estratégia, resultados e análise crítica, com prioridade às evidências | 15 | §7, p. 9 |
| R17 | Vídeo de até 10 minutos | Demonstra agente e uma investigação completa, da hipótese à conclusão, com decisões e intervenções | 16 | §7, p. 9–10 |

## Pesos de avaliação

| Critério | Peso |
|---|---|
| Funcionamento e reprodução do laboratório | 15% |
| Desenvolvimento e integração do agente supervisionado | 20% |
| Planejamento e qualidade técnica dos testes | 20% |
| Qualidade das evidências e interpretação dos resultados | 20% |
| Análise crítica da contribuição da IA | 20% |
| Documentação e apresentação | 5% |

Fonte: §8, p. 10. Quantidade de vulnerabilidades e autonomia do agente não são
critérios de pontuação. Investigações que rejeitem uma hipótese são resultados válidos.

## Acordos adicionais do projeto

Rotina de 2 horas, vistoria antes de implementar, aceite antes do commit, fontes por
implementação e preparação de material para LinkedIn são acordos com o usuário.
Não são exigências adicionais atribuídas ao enunciado.
