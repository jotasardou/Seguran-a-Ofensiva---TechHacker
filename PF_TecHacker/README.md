# Tecnologias Hacker — agente de IA supervisionado

Projeto acadêmico para investigar como um modelo de linguagem local pode apoiar
testes de segurança em uma instância local do OWASP Juice Shop, com decisões e
execuções supervisionadas pelo grupo.

**Estado atual:** organização inicial. Laboratório, agente e investigações ainda
não foram implementados ou validados neste projeto.

O objetivo de estudo é compreender as decisões técnicas, registrar evidências e
avaliar onde a IA ajuda, erra ou exige intervenção humana. A quantidade de
vulnerabilidades encontradas não é a medida de sucesso.

## Como vamos trabalhar

- Sessões de até 2 horas por dia, sem data de término definida neste planejamento.
- Antes de implementar: apresentar objetivo, escopo, fontes e validação para revisão.
- Depois de implementar: explicar o fluxo, revisar o diff e apresentar evidências.
- Criar commits pequenos após o aceite do usuário; registrar pendências ao encerrar.
- Preservar o plano inicial de testes elaborado pelo grupo sem auxílio de LLM.

## Navegação

| Documento | Finalidade |
|---|---|
| [Requisitos](docs/requisitos.md) | Obrigações do enunciado e critérios de conclusão |
| [Cronograma](docs/cronograma.md) | Entregas, sessões e commits previstos |
| [Laboratório](docs/laboratorio.md) | Instalação, execução, validação e restauração já comprovadas |
| [Fontes](docs/fontes.md) | Referências consultadas e decisões que sustentam |
| [Diário](docs/diario.md) | Contexto, decisões, aprendizados e próxima ação |
| [Instruções de colaboração](AGENTS.md) | Regras para assistência neste repositório |

## Kit disponível

| Equipamento | Informação disponível | Papel neste projeto |
|---|---|---|
| Appliance sem ventoinha, com quatro portas de rede | pfSense 2.7.2-RELEASE (amd64) confirmado no painel; WAN `192.168.20.30`, LAN `10.0.80.1` | Gateway e fronteira de rede do laboratório |
| Dell OptiPlex Micro 7020 | Ubuntu 22.04.5 LTS confirmado pela saída enviada pelo usuário; comando Docker indisponível | Candidato a hospedar componentes do laboratório |
| Computador pessoal | Usuário informa que possui Kali em VM no VirtualBox | Ponto de partida para acesso e ferramentas |

As fotos mostram um Dell OptiPlex e appliances com múltiplas portas; não confirmam
CPU, RAM, armazenamento, GPU, sistemas atuais ou a topologia completa. Há outros
equipamentos nas imagens, que não entram automaticamente no escopo do grupo.

As especificações serão verificadas quando forem necessárias para escolher ou
executar os componentes, especialmente o modelo local. Não bloqueiam esta etapa.
Qwen3 4B quantizado e Ollama são exemplos do enunciado, ainda não escolhas fechadas.

## Entrega acadêmica

Laboratório reproduzível, código do agente, registros de três investigações,
relatório de 4–6 páginas e vídeo de até 10 minutos. Todos os testes ficam restritos
ao Juice Shop local autorizado. A matriz de requisitos detalha o aceite.

## Portfólio e LinkedIn

A apresentação pública será construída a partir de decisões, resultados e
limitações realmente observados. Vamos guardar referências às evidências e aos
commits durante o desenvolvimento, para preparar uma demonstração clara ao final.

O relato deverá distinguir a assistência de IA no desenvolvimento do comportamento
do LLM local avaliado nos experimentos e reconhecer as contribuições do grupo.
Resultados planejados não serão apresentados como resultados obtidos.

O PDF da disciplina e as fotos originais ficam disponíveis localmente, fora do
versionamento inicial. As fotos contêm etiquetas institucionais e outros
equipamentos. Uma seleção de imagens e evidências para publicação passará por
revisão, incluindo credenciais, identificadores e dados de terceiros. O usuário
criou o repositório no GitHub e o clonou, mantendo este projeto na subpasta
`PF_TecHacker/`. O envio dos arquivos e a publicação no LinkedIn continuam como
ações separadas, com conteúdo aprovado pelo usuário.
