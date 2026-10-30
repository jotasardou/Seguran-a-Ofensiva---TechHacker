# Fontes e decisões

## Referências consultadas em 27/10/2026

| ID | Referência | Utilização atual | Limite |
|---|---|---|---|
| F01 | Enunciado local: `AF - Tecnologias Hackers 26-2.pdf`, 11 páginas | Requisitos, entregáveis e avaliação | Não determina uma arquitetura única |
| F02 | [Relatório do projeto firewall](../../../projeto_firewall/relatorio/relatorio.md), inventário e topologia | Contexto histórico do kit | Caminho do workspace, indisponível em um clone isolado; não comprova configuração atual |
| F03 | Relato do usuário e duas fotos originais em `img/` | Tipos de equipamento, disponibilidade do Kali e preferências de trabalho | Não identifica recursos internos ou toda a topologia; fotos fora do Git |
| F04 | [OWASP Juice Shop](https://owasp.org/projects/juice-shop) | Referência oficial do alvo exigido | Instruções específicas de instalação ainda serão consultadas |
| F05 | [API do Ollama](https://docs.ollama.com/api/introduction) | Referência para possível integração local | Ollama ainda não foi escolhido nem instalado neste projeto |
| F06 | [Saídas estruturadas do Ollama](https://docs.ollama.com/capabilities/structured-outputs) | Possibilidade de estruturar propostas por esquema JSON | Formato estruturado não comprova correção técnica ou autorização |
| F07 | [Manual do curl](https://curl.se/docs/manpage.html) | Ferramenta candidata para interação HTTP | Seleção e opções ainda dependem do plano |
| F08 | [Referência do Nmap](https://nmap.org/book/man.html) | Ferramenta candidata | Seleção e opções ainda dependem do plano |
| F09 | [Executar o Juice Shop — guia oficial](https://pwning.owasp-juice.shop/companion-guide/latest/part1/running.html), seção Docker image | Preparação da etapa 2: avaliar a instalação por imagem oficial | Instalação ainda não aprovada nem executada; versão será fixada na proposta |
| F10 | [Publicação de portas — Docker](https://docs.docker.com/engine/network/port-publishing/), seção Publishing ports | Entender como o endereço de publicação determina o acesso ao contêiner | O acesso pelo Kali depende da topologia; não copiar um mapeamento genérico antes de defini-la |
| F11 | [Servidor OpenSSH — Ubuntu](https://ubuntu.com/server/docs/how-to/security/openssh-server/) | Referência para acesso administrativo remoto ao Dell | SSH ainda não verificado ou configurado no kit; consulta não equivale a instalação |
| F12 | [Instalar Docker Engine no Ubuntu](https://docs.docker.com/engine/install/ubuntu/), requisitos e instalação pelo repositório `apt` | Preparar instalação reproduzível no Ubuntu 22.04 do Dell | Docker alerta que portas publicadas podem contornar regras do UFW; nenhuma porta será publicada externamente nesta primeira validação |
| F13 | [Downloads oficiais do Node.js](https://nodejs.org/en/download) | Selecionar uma versão LTS compatível e um binário oficial para o Dell | A versão concreta e seu checksum serão fixados antes da instalação |
| F14 | [Release v20.3.0 do Juice Shop](https://github.com/juice-shop/juice-shop/releases/tag/v20.3.0) | Fixar a versão da aplicação em vez de depender do estado futuro da branch principal | O nome do pacote Linux/Node e sua integridade ainda serão confirmados antes do download |

As referências web foram consultadas durante o planejamento inicial. Não há ainda
implementação derivada delas. O vínculo com arquivos e validações será acrescentado
quando cada incremento for aprovado e realizado.

## Registro por implementação

Antes de implementar, registrar: requisito/etapa, URL e seção consultadas, data de
consulta, decisão sustentada, alternativas relevantes e limitações. Após validar,
acrescentar arquivos alterados, evidência da verificação e commit correspondente.

Uma decisão própria será identificada como decisão de projeto. Não atribuir à
documentação conclusões que ela não sustenta nem usar conhecimento de treinamento
como se fosse uma fonte consultada. Confirmar instruções e versões no momento do uso.

## Decisões iniciais

- **D01 — incrementos revisados:** preferência explícita do usuário. Fontes F01 e F03.
- **D02 — preservar plano humano:** exigência do enunciado, §3. Fonte F01.
- **D03 — adiar inventário detalhado:** preferência explícita do usuário; coletar
  recursos quando uma decisão de execução depender deles. Fonte F03.
- **D04 — Kali existente como ponto de partida:** evita planejar reinstalação antes
  de conferir a conectividade; topologia ainda sujeita a revisão. Fonte F03.
- **D05 — preparar apresentação pública:** pedido do usuário; originais locais e
  material público revisado separadamente. Fonte F03.
- **D06 — execução direta com Node.js:** decisão do usuário em 29/10/2026. O
  Juice Shop será executado diretamente no Ubuntu do Dell, sem Docker. A primeira
  opção a avaliar é a distribuição pré-empacotada oficial, com versões e checksum
  fixados. Fontes F13 e F14.
