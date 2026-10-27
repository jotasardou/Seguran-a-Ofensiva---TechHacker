# Diário de trabalho

Registrar fatos, decisões e aprendizados ao encerrar cada sessão. Não estimar tempo
como se fosse uma medição. Referenciar requisitos, fontes, evidências e commits
quando existirem.

## 27/10/2026 — organização inicial

**Meta:** preparar a base documental para a vistoria do usuário (etapa 1).
**Tempo efetivamente dedicado:** não medido; preencher pelo grupo se disponível.

### Contexto e trabalho realizado

- Enunciado de 11 páginas lido integralmente; requisitos organizados na matriz.
- Proposta de entregas e rotina de 2 horas apresentada na conversa.
- Usuário criou os arquivos e diretórios iniciais e adicionou duas fotos do kit.
- Consultados inventário e topologia do projeto firewall; fotos inspecionadas.
- Usuário confirmou appliance, Dell OptiPlex Micro 7020 e Kali no computador pessoal.
- Usuário pediu adiar especificações de hardware e preparar o projeto para LinkedIn.
- Git local iniciado na pasta PF_TecHacker, com branch main, sem remoto.
- Arquivos iniciais preenchidos para revisão. Nenhum componente do laboratório,
  agente ou investigação implementado nesta etapa.

### Decisões e aprendizado

- Detalhes de CPU/RAM/disco/GPU não bloqueiam a documentação inicial (D03).
- O plano de testes independente deve preceder a revisão pelo LLM (D02, R08–R09).
- Fotos registram o aspecto físico, mas não comprovam topologia ou sistemas atuais.
- O inventário distingue appliance/firewall, computador servidor e computador
  pessoal; múltiplas portas Ethernet não bastam para classificar um aparelho como switch.
- Para a futura apresentação, separar planos, resultados comprovados e contribuições
  humanas/IA. PDF e fotos originais ficam locais nesta primeira versão (D05).

### Validação inicial, antes da mudança para o clone

Validação: sete arquivos conferidos quanto a conteúdo não vazio, links locais,
newline final e espaços finais, sem problemas. Git confirmou branch main sem
commits ou remoto e exclusão do PDF e das duas fotos originais pelo .gitignore.

Naquele momento, a documentação estava preparada e aguardava vistoria, sem commits.

### Organização no clone e aceite do usuário

O usuário criou o repositório no GitHub, clonou-o em
`projetos/Seguran-a-Ofensiva---TechHacker/` e moveu o projeto para a subpasta
`PF_TecHacker/`. A movimentação também levou o `.git` local anterior, que ainda
não tinha commits. O Git do clone passa a controlar os arquivos do projeto.

Com autorização explícita do usuário, os metadados internos foram movidos para
`projetos/.git-backups/PF_TecHacker-2026-10-27`, fora do clone, preservando os
18 arquivos. Os hashes SHA-256 antes e depois da movimentação foram comparados
e são idênticos. Nenhum arquivo de trabalho foi removido.

A referência F02 ao projeto firewall foi corrigida para a nova localização. O
README foi atualizado somente para refletir a criação do repositório remoto.
O usuário informou ter revisado e aprovado o README e o cronograma.

Conferência final: o projeto resolve para a raiz Git do clone; a simulação de
adição lista somente os sete arquivos documentais/configuração previstos. Os
links locais são válidos, e o PDF e as duas fotos continuam ignorados. Nenhum
arquivo foi colocado no índice durante essa simulação.

**Estado:** organização ajustada; README e cronograma aprovados; nenhum commit criado.
**Commit proposto:** `docs: registra requisitos e rotina do projeto`.
**Próxima ação:** usuário pode criar o primeiro commit após a conferência dos
arquivos previstos. O envio ao GitHub não foi executado nesta etapa.

A configuração atual do laboratório pode ser levantada antes da instalação do
Juice Shop: o sistema operacional orienta a instalação, e a conectividade define
o acesso a partir do Kali e o escopo local. Esse levantamento não é pré-requisito
para o commit documental. CPU, RAM e GPU permanecem adiados. Não copiar os IPs
antigos como fatos atuais.

### Registro para apresentação futura

Tema deste marco: organizar um laboratório e um fluxo de revisão que tornem a
assistência de IA rastreável. Ainda não há resultados experimentais para divulgar.
Fontes: F01–F08. Evidência atual: arquivos documentais e histórico da conversa.

## Modelo para próximas sessões

- Data e duração efetivamente medida:
- Meta e escopo aprovado:
- Requisitos e decisões envolvidos:
- Fontes consultadas:
- Alterações realizadas:
- Validação e evidências:
- Aprendizado e contribuição humana/IA:
- Estado da vistoria e commit, se aprovado:
- Pendências e próximo passo:
- Material candidato à apresentação pública:
