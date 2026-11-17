# Revisão do plano pelo modelo local — 17/11/2026

## Origem e limite da evidência

O grupo executou `ollama run qwen2.5:1.5b` no Kali e forneceu ao modelo as
linhas T10, T16 e T26 de `plano_humano.md`, juntamente com a instrução para
avaliar hipóteses, ferramentas, evidências, melhorias e limitações. A transcrição
integral foi enviada pelo usuário nesta conversa; o texto abaixo resume a saída
observada. A versão exata do binário Ollama e o identificador do modelo não foram
registrados na transcrição. Nenhum teste no Juice Shop foi executado por essa
revisão textual. As decisões abaixo foram tomadas pelo assistente Codex por
delegação explícita do usuário, e não são decisões atribuídas retroativamente
ao grupo nem conclusões do modelo local.

## Sugestões e decisões

| Investigação | Sugestão ou afirmação do modelo local | Decisão delegada | Justificativa técnica |
| --- | --- | --- | --- |
| Five Star Feedback (T10) | Proxy HTTP e contas de teste são adequados. | Aceitar. | Comparar sessão sem privilégios, requisição de exclusão e estado da avaliação antes/depois permite avaliar autorização. |
| Five Star Feedback (T10) | Uma exclusão **sem sucesso** confirmaria a falha. | Rejeitar. | Rejeição é o comportamento esperado do controle. Confirmação exigiria exclusão indevida efetiva por conta sem permissão. |
| Five Star Feedback (T10) | Criar script para automatizar cadastro, avaliação e exclusão. | Modificar. | Preparar contas e avaliação manualmente e automatizar apenas requisições pontuais supervisionadas, caso necessário; evitar criar efeitos múltiplos sem rastreio. |
| Login Admin (T16) | Proxy HTTP e cliente de API são adequados. | Aceitar. | Permitem comparar login inválido comum com entrada modificada e verificar identidade da sessão emitida. |
| Login Admin (T16) | Falha de autenticação em todas as tentativas confirmaria a injeção. | Rejeitar. | Falhas não confirmam bypass. Confirmar somente se uma entrada modificada produzir sessão administrativa sem senha válida. |
| Login Admin (T16) | Script para gerar parâmetros errados e executar tentativas. | Modificar. | Limitar tentativas manuais ou supervisionadas, preservar entradas e respostas e evitar inferir vulnerabilidade a partir de erro isolado. |
| Confidential Document (T26) | Navegador e proxy HTTP são adequados. | Aceitar. | Uma requisição HTTP sem autenticação, status e trecho mínimo do documento permitem avaliar exposição. |
| Confidential Document (T26) | Script para pesquisar URL e analisar conteúdo. | Modificar. | Usar primeiro a URL conhecida apenas como ponto de partida declarado; executar uma requisição supervisionada e registrar o contexto da descoberta anterior. |
| Ordem | Começar por Login Admin, apoiado em um script supostamente já criado. | Rejeitar. | Não há evidência de tal script. Confidential Document requer menos preparação e pode ser verificado com `curl` GET sem alterar estado. |

## Ordem escolhida

1. **Confidential Document (T26):** primeira investigação do agente, com leitura
   HTTP sem autenticação e interpretação limitada à evidência obtida.
2. **Login Admin (T16):** preparar comparação entre login inválido comum e
   tentativa modificada. A ferramenta atual do agente aceita apenas `curl` GET/HEAD;
   suporte seguro a POST e registro do resultado deve ser implementado e validado
   antes da execução.
3. **Five Star Feedback (T10):** preparar contas, avaliação e verificação
   antes/depois. O agente atual não permite DELETE; ampliar a ferramenta com
   autorização e limites específicos antes dessa investigação.

Um resultado positivo observado manualmente antes do agente não substitui a
execução supervisionada. Cada investigação deve registrar proposta do modelo,
decisão humana, parâmetros executados, resposta bruta, interpretação posterior e
conclusão sustentada. O erro do modelo sobre evidência de falha, e a premissa do
script inexistente, são limitações concretas para a análise crítica (R14).
