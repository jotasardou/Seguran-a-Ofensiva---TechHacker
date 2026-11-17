# Proposta de revisão do plano por IA

Data: 17/11/2026. Autoria: assistente de IA nesta conversa, após o registro
[humano](plano_humano.md). Esta proposta não é uma revisão pelo modelo local
do projeto; essa revisão ainda precisa ser realizada e registrada.

Esta proposta foi redigida antes da versão atual do plano humano. O grupo
posteriormente registrou hipóteses, estratégias, ferramentas, evidências e
selecionou Five Star Feedback, Login Admin e Confidential Document. Houve
explorações manuais preliminares antes da formalização do plano. Este arquivo
é histórico e não representa a revisão pelo modelo local exigida em R09.

## Escopo e propostas

Ambiente do agente: Kali Linux conectado ao laboratório pelo OpenVPN. Alvo
autorizado: somente a instância Juice Shop em `http://10.0.80.3:3000`.
Cada ação do agente depende de aprovação humana; resultados devem retornar ao
modelo, com registros de proposta, decisão, execução e interpretação.

### 1. Documento confidencial

- Hipótese: um documento confidencial está acessível sem autenticação.
- Estratégia: examinar o diretório conhecido e solicitar o documento identificado,
  usando `curl` sob supervisão.
- Evidência: resposta HTTP e conteúdo que permitam avaliar acesso e sensibilidade;
  erro ou ausência do conteúdo não comprova a hipótese.
- Contexto preliminar: o usuário relatou acesso manual a `/ftp/acquisitions.md`
  com resposta 200. Falta execução e análise pelo agente.

### 2. Reconhecimento do serviço

- Hipótese: a porta TCP 3000 do alvo responde ao teste a partir da máquina do agente.
- Estratégia: verificar somente essa porta com `nmap`, após aprovação.
- Evidência: saída e estado da porta; porta aberta, por si só, não comprova
  vulnerabilidade. Falha de acesso exige análise de conectividade.
- Limite: esta investigação é distinta, mas representa reconhecimento e não uma
  segunda vulnerabilidade; avaliar se satisfaz a interpretação do professor.

### 3. XSS no campo de pesquisa

- Hipótese: entrada controlada no campo de pesquisa pode executar código no navegador.
- Estratégia: inspecionar a interação HTTP com ferramenta do agente e confirmar
  o comportamento no navegador sob supervisão humana.
- Evidência: requisição e observação visual da execução; resposta HTTP isolada
  não comprova execução no DOM.
- Contexto preliminar: o usuário relatou um alerta `xss` e conclusão do desafio.
  Falta registro reproduzível com participação do agente.

## Decisões e próximos passos

O usuário autorizou a elaboração desta proposta histórica. A revisão posterior
do modelo local e as decisões delegadas estão em [revisao_modelo_local.md](revisao_modelo_local.md).
Não foram executadas ferramentas ou testes nesta proposta histórica.
