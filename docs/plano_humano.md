# Planejamento dos testes — OWASP Juice Shop

Data de elaboração: 17 de novembro de 2026.

Status: planejamento produzido pelo grupo. Nenhum teste foi executado durante a elaboração desta versão; existem explorações manuais preliminares registradas separadamente.

Playlist: [How to hack OWASP Juice Shop — A Guided Walkthrough showing all Solutions, por Hacksplained](https://www.youtube.com/playlist?list=PL8j1j35M7wtKXpTBE6V1RlN_pBZ4StKZw).

## 1. Contexto e limites

Foram conferidos os 50 títulos da playlist. O planejamento abaixo contempla cada título individualmente, agrupando os desafios por tema.

A análise utilizou os títulos e a documentação oficial. Não houve visualização integral dos 50 vídeos nem execução de testes. O repositório oficial associa essa série às versões 10 e 11 do Juice Shop; o grupo deverá verificar quais desafios existem e como se comportam na versão utilizada no laboratório. A documentação atual pode descrever comportamentos diferentes dos apresentados nos vídeos.

Este documento assume que a aplicação investigada será uma instância de laboratório do OWASP Juice Shop. Todas as falhas descritas são hipóteses a investigar, não resultados confirmados.

Nem todo título representa uma vulnerabilidade: alguns são exercícios de reconhecimento, leitura ou descoberta. A conclusão de um desafio não demonstra, por si só, impacto de segurança.

## 2. Requisitos da atividade

Antes dos experimentos com o agente, o grupo deverá analisar inicialmente o ambiente e elaborar um plano de testes que apresente:

- Quais aspectos da aplicação serão investigados.
- Quais hipóteses iniciais serão consideradas.
- Quais ferramentas poderão contribuir para a investigação.
- Quais evidências serão necessárias para sustentar as conclusões.

O grupo deverá registrar sua estratégia e documentar as decisões tomadas durante a revisão e a execução, com justificativa técnica. O planejamento deverá orientar a investigação e permitir a formulação de novas hipóteses durante os testes. Não é necessário identificar previamente todas as vulnerabilidades.

Este arquivo é uma proposta de apoio. Ele não substitui o registro das contribuições e decisões efetivamente realizadas pelo grupo.

## 3. Planejamento dos testes

### 3.1. Objetivo e preparação

O planejamento busca investigar como a aplicação valida entradas, autentica usuários, controla permissões, protege informações e trata comportamentos inesperados. A investigação começará pelo funcionamento normal de cada recurso e avançará para testes controlados, alterando uma condição por vez.

Antes dos experimentos, registrar:

- Versão da aplicação, configuração do ambiente e funcionalidades disponíveis.
- Contas de teste e respectivos perfis de acesso.
- Hipóteses selecionadas, ordem dos testes e resultados esperados.
- Limites de execução, incluindo quantidade de requisições e condições para interrupção.
- Cópia do estado inicial para permitir repetição e comparação.

Nas tabelas, **proxy HTTP** significa Burp Suite ou OWASP ZAP, usados para inspecionar, modificar e reenviar requisições. **DevTools** são as ferramentas de desenvolvimento do navegador.

### 3.2. Validação de entradas

Comparar as restrições apresentadas pela interface com aquelas efetivamente aplicadas pelo servidor.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T01 | Zero Stars | Limites da nota enviada no formulário de feedback. | O servidor pode aceitar nota zero, embora a interface permita apenas valores de 1 a 5. | DevTools e proxy HTTP. | Requisição com nota zero, resposta e consulta posterior mostrando o valor armazenado. |
| T02 | Missing Encoding | Construção e interpretação de URLs com caracteres especiais. | Uma imagem pode ficar inacessível porque seu endereço foi codificado incorretamente. | DevTools, painel Network e codificador de URL. | Comparação entre os endereços original e corrigido, respostas HTTP e carregamento da imagem. Isso não demonstra, isoladamente, acesso indevido. |
| T03 | Repetitive Registration | Conferência dos campos de senha e confirmação de senha. | A conferência pode ocorrer apenas no navegador, permitindo cadastro com confirmação ausente ou diferente. | Proxy HTTP e cliente de API. | Requisição modificada, criação da conta e autenticação posterior com a senha cadastrada. |
| T04 | Admin Registration | Campos aceitos no cadastro e atribuição de privilégios. | O servidor pode aceitar um atributo de perfil administrativo enviado pelo cliente. | Proxy HTTP e cliente de API. | Corpo enviado no cadastro, perfil persistido e acesso efetivo a uma operação administrativa. |
| T05 | Payback Time | Quantidades, preços e cálculo do total do pedido. | Valores negativos ou inconsistentes podem gerar um pedido com total favorável ao comprador. | Proxy HTTP e planilha para conferir cálculos. | Carrinho antes e depois, requisição modificada, total calculado pelo servidor e pedido registrado. |
| T06 | Upload Size | Limite de tamanho dos arquivos enviados. | O limite apresentado pela interface pode não ser aplicado no servidor. | Proxy HTTP e arquivos de teste com tamanhos conhecidos. | Tamanho real do arquivo, requisição de upload e confirmação de recebimento ou armazenamento. |
| T07 | Upload Type | Validação de extensão, tipo MIME e conteúdo do arquivo. | A aplicação pode confiar apenas em verificações do navegador ou em metadados declarados pelo cliente. | Proxy HTTP, comando `file` e arquivos inofensivos. | Extensão, MIME, assinatura do conteúdo e resultado de aceitação ou rejeição de cada combinação. |
| T08 | Expired Coupon | Validade temporal dos cupons e aplicação de descontos. | Um cupom expirado pode continuar sendo aceito pelo servidor. | Proxy HTTP e comparação de pedidos de teste. | Validade conhecida do cupom, data do ambiente e desconto aplicado ao total do pedido. |

Referência temática: [Improper Input Validation](https://pwning.owasp-juice.shop/companion-guide/latest/part2/improper-input-validation.html).

### 3.3. Controle de acesso

Comparar ações realizadas pelo proprietário do recurso, por outro usuário e por uma sessão sem autenticação.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T09 | Admin Section | Proteção da área administrativa e das APIs utilizadas por ela. | A aplicação pode esconder o menu sem verificar adequadamente as permissões no servidor. | DevTools e proxy HTTP. | Perfil da conta utilizada, recurso acessado e dados ou operações administrativas efetivamente disponíveis. |
| T10 | Five Star Feedback | Permissão para excluir feedbacks. | Um usuário sem privilégios pode conseguir remover avaliações de cinco estrelas. | Proxy HTTP e contas de teste. | Avaliações existentes antes do teste, requisição de exclusão e confirmação posterior da remoção. |
| T11 | View Basket | Autorização para consultar carrinhos. | Alterar a referência do carrinho pode revelar o conteúdo pertencente a outro usuário. | Proxy HTTP e duas contas de teste. | Identificação dos proprietários e resposta contendo itens do segundo usuário durante a sessão do primeiro. |
| T12 | Forged Feedback | Associação entre feedback e autor autenticado. | O servidor pode confiar no identificador de autor enviado pelo cliente. | Proxy HTTP e cliente de API. | Sessão utilizada, autor informado na requisição e autoria atribuída ao feedback persistido. |
| T13 | Forged Review | Autoria e permissão de alteração de avaliações de produtos. | Pode ser possível publicar ou editar uma avaliação em nome de outra conta. | Proxy HTTP e duas contas de teste. | Avaliação original, identidade autenticada, requisição modificada e avaliação resultante. |
| T14 | Manipulate Basket | Autorização para adicionar itens ao carrinho. | Um usuário pode conseguir inserir produtos no carrinho de outra conta. | Proxy HTTP e duas sessões separadas. | Carrinho da conta afetada antes e depois, sessão responsável e requisição que causou a alteração. |
| T15 | Product Tampering | Permissão para alterar informações do catálogo. | Uma conta comum pode modificar uma descrição ou um link de produto. | Proxy HTTP e cliente de API. | Conteúdo original, alteração enviada e conteúdo persistido, visível em uma nova consulta. |

Referência temática: [Broken Access Control](https://pwning.owasp-juice.shop/companion-guide/latest/part2/broken-access-control.html).

### 3.4. Injeção em consultas

Buscar diferenças reproduzíveis entre entradas comuns e entradas que possam alterar a interpretação de uma consulta. Um erro isolado será tratado apenas como indício.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T16 | Login Admin | Processamento das entradas no login. | A construção insegura de consultas pode permitir autenticação como administrador sem a senha correta. | Proxy HTTP e cliente de API. | Comparação com login inválido, entrada utilizada, sessão emitida e confirmação da identidade administrativa. |
| T17 | Database Schema | Isolamento entre consultas funcionais e metadados do banco. | Um parâmetro de consulta pode permitir recuperar informações sobre tabelas e colunas. | Proxy HTTP e cliente de API. | Requisição reproduzível e resposta contendo definições do esquema que não aparecem no funcionamento normal. |
| T18 | Login Bender | Seleção da identidade retornada pelo login. | Uma consulta manipulável pode permitir autenticação direcionada para a conta Bender. | Proxy HTTP. | Sessão emitida e consulta autenticada confirmando que a identidade corresponde à conta pretendida. |
| T19 | Login Jim | Seleção da identidade e validação de credenciais. | O login pode permitir obter uma sessão de Jim sem validar sua senha corretamente. | Proxy HTTP. | Tentativa de controle rejeitada, tentativa modificada e confirmação da identidade na sessão obtida. |
| T20 | Ephemeral Accountant | Relação entre resultado da consulta e criação da sessão. | O login pode confiar em um resultado manipulado e emitir sessão para uma identidade não cadastrada. | Proxy HTTP; consulta de dados de apoio, se permitida. | Evidência da inexistência prévia da conta, resposta do login e identidade assumida, sem cadastro persistente. |
| T21 | NoSql Manipulation | Interpretação de filtros e operadores em atualizações. | Entradas controladas pelo cliente podem ampliar uma atualização para vários registros. | Proxy HTTP e conjunto de avaliações de teste. | Corpo da requisição e comparação dos registros antes e depois, demonstrando quais foram alterados. |

Referência temática: [Injection](https://pwning.owasp-juice.shop/companion-guide/latest/part2/injection.html).

### 3.5. Cross-Site Scripting — XSS

Utilizar um marcador inofensivo de execução. Inserir texto ou HTML na página, por si só, não será considerado prova suficiente de execução de JavaScript.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T22 | DOM XSS | Fluxo entre entradas do usuário e atualização do DOM. | Uma entrada pode alcançar um ponto de renderização que interprete conteúdo executável. | DevTools, inspeção do DOM e depurador JavaScript. | Entrada utilizada, elemento resultante e execução observada, identificando o processamento ocorrido no navegador. |
| T23 | Classic Stored XSS | Armazenamento e exibição de conteúdo em página legada. | Um campo persistido pode ser renderizado sem proteção adequada. | Proxy HTTP e navegador com sessão separada. | Gravação do conteúdo e execução ao consultar novamente a página, inclusive em outra sessão quando aplicável. |
| T24 | API-Only XSS | Validação de conteúdo enviado diretamente à API. | A API pode aceitar conteúdo que posteriormente será executado pela interface. | Cliente de API, proxy HTTP e navegador. | Requisição direta, persistência do conteúdo e execução posterior ao abrir o recurso correspondente. |
| T25 | Client-side XSS Protection | Dependência de filtros executados no navegador. | Uma proteção local pode ser contornada enviando a requisição diretamente ao servidor. | DevTools e proxy HTTP. | Bloqueio na interface, aceitação pela API e execução posterior do conteúdo armazenado. |

Referência temática: [Cross Site Scripting](https://pwning.owasp-juice.shop/companion-guide/latest/part2/xss.html).

### 3.6. Exposição de dados e arquivos

Distinguir arquivos intencionalmente públicos de informações que deveriam ter acesso restrito. A classificação dependerá do conteúdo e do contexto, além da possibilidade de download.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T26 | Confidential Document | Publicação e proteção de documentos internos. | Um documento confidencial pode estar disponível sem autenticação. | Navegador, DevTools e proxy HTTP. | URL, estado da sessão e trecho mínimo do conteúdo que demonstre sua natureza confidencial. |
| T27 | Login MC SafeSearch | Divulgação de informações que possam revelar credenciais. | Informações públicas relacionadas ao personagem podem permitir deduzir sua senha. | Pesquisa nas referências do desafio e navegador. | Fonte da informação, raciocínio utilizado e autenticação com a credencial original da conta do laboratório. |
| T28 | Login Amy | Origem, exposição e previsibilidade de uma senha aparentemente forte. | Uma senha longa pode continuar recuperável por causa de sua origem ou divulgação. | Pesquisa nas referências do desafio e análise textual. | Fonte encontrada, relação com a credencial e login confirmado, sem troca prévia da senha. |
| T29 | Access Log | Acesso a registros operacionais do servidor. | Um arquivo de log pode ter sido publicado em área acessível pela aplicação. | Navegador, proxy HTTP e leitor de texto. | Endereço, sessão utilizada e conteúdo demonstrando que o arquivo registra acessos ao servidor. |
| T30 | Forgotten Developer Backup | Exposição de arquivos de configuração ou desenvolvimento. | Um backup esquecido pode ser recuperado apesar das restrições aparentes de download. | Proxy HTTP e editor de texto. | Requisição, arquivo recuperado e conteúdo que permita identificar sua finalidade e sensibilidade. |
| T31 | Forgotten Sales Backup | Exposição de informações comerciais em backups. | Um arquivo antigo de vendas pode permanecer acessível. | Proxy HTTP e leitor de arquivos. | Arquivo obtido, condição de acesso e presença de informações comerciais que deveriam estar restritas. |
| T32 | GDPR Data Theft | Separação dos dados incluídos na exportação pessoal. | A exportação pode associar registros incorretamente e incluir dados de outra conta. | Duas contas, pedidos fictícios e comparador de JSON. | Dados preparados para cada conta e exportação contendo registros pertencentes à outra, sem uso de injeção. |
| T33 | Misplaced Signature File | Publicação indevida de arquivo de assinatura de monitoramento. | Um arquivo operacional pode ter sido incluído entre os recursos disponibilizados pela aplicação. | Proxy HTTP e editor de texto. | Arquivo recuperado, caminho de acesso e identificação de sua finalidade. O impacto deverá ser avaliado separadamente. |

Referência temática: [Sensitive Data Exposure](https://pwning.owasp-juice.shop/companion-guide/latest/part2/sensitive-data-exposure.html). As classificações de determinados desafios podem variar conforme a versão.

### 3.7. Autenticação e recuperação de contas

Verificar como a aplicação comprova a identidade do usuário no login, na recuperação e na alteração de senha.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T34 | Password Strength | Resistência da senha administrativa a tentativas previsíveis. | A conta pode utilizar uma senha comum, mesmo que o mecanismo de login funcione corretamente. | Lista pequena de candidatos e cliente HTTP; análise offline de hash somente se obtido no escopo. | Origem dos candidatos, quantidade de tentativas e login com a senha original, sem injeção ou redefinição. |
| T35 | Björn’s Favorite Pet | Confiabilidade das perguntas de segurança. | Informações públicas podem fornecer a resposta usada na recuperação da conta. | Pesquisa nas referências do desafio e navegador. | Fonte da resposta, recuperação concluída e acesso à conta do laboratório. |
| T36 | GDPR Data Erasure | Efeito da exclusão da conta sobre a autenticação. | Uma conta marcada como excluída pode continuar sendo aceita pelo login. | Proxy HTTP e registros disponíveis no laboratório. | Evidência do estado de exclusão e emissão de uma sessão utilizável para a mesma conta. |
| T37 | Reset Jim’s Password | Resistência da recuperação a respostas pesquisáveis. | A resposta de segurança pode ser encontrada a partir de informações sobre o personagem. | Pesquisa nas referências do desafio e navegador. | Fonte consultada, resposta aceita e confirmação da recuperação da conta. |
| T38 | Login Bjoern | Integração de identidade externa e autenticação local. | A implementação associada ao login externo pode produzir uma forma previsível de autenticação local. | DevTools, proxy HTTP e análise do código cliente. | Fluxo observado, origem da previsibilidade e sessão obtida na aplicação, sem acessar a conta Google real. |
| T39 | Change Benders Password | Validações exigidas para alterar uma senha. | O servidor pode aceitar a alteração sem verificar corretamente a senha atual ou a identidade da sessão. | Proxy HTTP e cliente de API. | Requisição de alteração, identidade autenticada, senha anterior rejeitada e nova senha aceita na conta de teste. |

Referência temática: [Broken Authentication](https://pwning.owasp-juice.shop/companion-guide/latest/part2/broken-authentication.html).

### 3.8. Configuração e tratamento de erros

Examinar informações e funcionalidades expostas por configurações inadequadas ou componentes mantidos após sua desativação aparente.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T40 | Error Handling | Respostas a campos ausentes, tipos inesperados e rotas inválidas. | Erros podem revelar detalhes internos ou ser tratados de maneira inconsistente. | Proxy HTTP, DevTools e console do navegador. | Entrada que provocou o erro, resposta completa e detalhe interno exposto. Um código 500 sozinho não comprova vazamento. |
| T41 | Deprecated Interface | Permanência de uma interface antiga e de suas rotas. | A interface pode ter sido retirada da navegação, mas continuar funcional no servidor. | DevTools, proxy HTTP e análise das referências do cliente. | Rota identificada, requisição aceita e processamento que demonstre que a interface antiga permanece ativa. |

Referência temática: [Security Misconfiguration](https://pwning.owasp-juice.shop/companion-guide/latest/part2/security-misconfiguration.html).

### 3.9. Redirecionamento

O desafio usa o nome antigo “Outdated Whitelist”; a documentação atual emprega “Outdated Allowlist”. Distinguir um destino antigo ainda permitido de um redirecionamento arbitrário.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T42 | Outdated Whitelist | Atualização da lista de destinos permitidos. | Um destino que deixou de ser promovido pode permanecer autorizado para redirecionamento. | Proxy HTTP e DevTools. | Parâmetro enviado, resposta de redirecionamento e destino final, comparados aos destinos atualmente apresentados pela aplicação. |

Referência temática: [Unvalidated Redirects](https://pwning.owasp-juice.shop/companion-guide/latest/part2/unvalidated-redirects.html).

### 3.10. Proteção contra automação

Usar uma quantidade previamente limitada de requisições e registrar as proteções observadas.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T43 | Captcha Bypass | Validação, reutilização e previsibilidade do CAPTCHA. | O mecanismo pode permitir automatizar o envio de feedbacks sem resolver um novo desafio a cada operação. | Proxy HTTP e script curto de teste. | Sequência de requisições, relação entre desafios e respostas, horários e quantidade de feedbacks efetivamente criados. |
| T44 | Extra Language | Descoberta de arquivos de tradução não apresentados no menu. | Um arquivo adicional pode ser encontrado por análise ou enumeração limitada dos identificadores de idioma. | DevTools, script com lista limitada e leitor de JSON. | Idiomas exibidos no menu, candidatos consultados e arquivo adicional recuperado. Sua existência não comprova, isoladamente, exposição sensível. |

Referência temática: [Broken Anti-Automation](https://pwning.owasp-juice.shop/companion-guide/latest/part2/broken-anti-automation.html).

### 3.11. Criptografia e ofuscação

Identificar qual propriedade está sendo investigada: confidencialidade, integridade, armazenamento de senha ou simples ocultação de conteúdo.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T45 | Weird Crypto | Algoritmos, bibliotecas e contexto de uso da criptografia. | A aplicação pode usar um mecanismo inadequado para a finalidade pretendida. | Análise de código ou artefatos permitidos e documentação técnica. | Identificação do mecanismo, local e finalidade de uso, parâmetros relevantes e justificativa técnica da inadequação. |
| T46 | Nested Easter Egg | Proteção de um conteúdo oculto por transformações sucessivas. | As camadas podem ser reversíveis sem um segredo protegido. | CyberChef local ou scripts de transformação. | Conteúdo inicial, sequência reproduzível das transformações e recurso final recuperado, distinguindo codificação de criptografia. |

Referência temática: [Cryptographic Issues](https://pwning.owasp-juice.shop/companion-guide/latest/part2/cryptographic-issues.html).

### 3.12. Componentes e cadeia de dependências

Investigar a procedência dos pacotes. A análise pode ser documental, sem executar componentes suspeitos.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T47 | Legacy Typosquatting | Nomes, origem e histórico das dependências. | Uma versão histórica pode ter incluído um pacote cujo nome imita uma dependência legítima. | Manifestos, arquivos de lock, histórico do repositório e metadados do registro. | Nome exato, versão, referência histórica da inclusão e comparação com o pacote legítimo. Diferenciar ocorrência histórica de presença na instalação atual. |

Referência: [índice oficial de desafios](https://pwning.owasp-juice.shop/companion-guide/latest/part2/README.html).

### 3.13. Segurança por obscuridade

Examinar conteúdo já entregue ao navegador e verificar o que sua apresentação visual esconde.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T48 | Privacy Policy Inspection | Conteúdo e apresentação da política de privacidade. | Uma informação pode estar visualmente escondida, mas continuar disponível no documento recebido pelo navegador. | DevTools, inspeção de HTML e CSS. | Conteúdo recebido, regra visual responsável pela ocultação e informação recuperada. O impacto dependerá da natureza dessa informação. |

Referência temática: [Security through Obscurity](https://pwning.owasp-juice.shop/companion-guide/latest/part2/security-through-obscurity.html).

### 3.14. Descoberta e boas práticas

“Privacy Policy” e “Security Policy” são atividades de reconhecimento e leitura. Sua conclusão não representa, por si só, a descoberta de uma vulnerabilidade.

| ID | Título da playlist | Aspectos investigados | Hipótese inicial | Ferramentas propostas | Evidências necessárias |
| --- | --- | --- | --- | --- | --- |
| T49 | Privacy Policy | Disponibilidade e conteúdo da política de privacidade. | O documento pode fornecer informações úteis para planejar a investigação dos fluxos de dados pessoais. | Navegador e registro de observações. | Endereço, conteúdo consultado e relação entre suas declarações e as funcionalidades que serão testadas. |
| T50 | Security Policy | Orientações para pesquisa de segurança e comunicação de falhas. | A aplicação pode publicar condições e canais relevantes para a condução dos testes. | Navegador e cliente HTTP. | Documento localizado, condições identificadas e delimitação do escopo adotado pelo grupo. |

Referência temática: [Miscellaneous](https://pwning.owasp-juice.shop/companion-guide/latest/part2/miscellaneous.html).

## 4. Execução e sustentação das conclusões

Para cada hipótese selecionada:

1. **Registrar o comportamento normal:** executar a funcionalidade com dados válidos e com o perfil esperado.
2. **Definir a comparação:** indicar qual entrada, permissão ou condição será alterada.
3. **Executar o teste:** modificar uma condição por vez e preservar as requisições e respostas.
4. **Verificar o efeito real:** consultar novamente o recurso, confirmar a identidade da sessão ou conferir os dados persistidos.
5. **Repetir quando necessário:** verificar se o comportamento é reproduzível a partir de condições conhecidas.
6. **Classificar o resultado:** hipótese confirmada, não confirmada nas condições testadas ou inconclusiva.

Uma resposta HTTP 200, um alerta de scanner ou a marcação do desafio como resolvido serão evidências auxiliares. A conclusão deverá explicar qual controle falhou e demonstrar o efeito correspondente.

A hipótese não confirmada não demonstra ausência de vulnerabilidades. O resultado deve ser limitado à versão, à configuração, às entradas e às condições efetivamente testadas.

### 4.1. Modelo de registro por teste

| Campo | Conteúdo a registrar |
| --- | --- |
| Identificação | Código do teste e título do desafio. |
| Hipótese | Comportamento suspeito e condição que permitiria observá-lo. |
| Pré-condições | Versão, estado inicial, conta, perfil e dados preparados. |
| Procedimento | Ações realizadas e variável alterada. |
| Resultado esperado | Comportamento previsto caso o controle funcione. |
| Resultado observado | Resposta efetivamente obtida, sem antecipar a interpretação. |
| Evidências | Requisições, respostas, capturas, arquivos e comparação antes/depois. |
| Conclusão | Confirmada, não confirmada ou inconclusiva, com justificativa. |
| Continuidade | Limitações encontradas e novas hipóteses propostas. |

### 4.2. Registro dos experimentos com o agente

Registrar também:

- Modelo e versão informados.
- Prompt e instruções fornecidos ao agente.
- Ferramentas disponíveis e respectivos limites.
- Estado inicial da aplicação e dados preparados.
- Ações realizadas e resultados retornados pelas ferramentas.
- Intervenções humanas e motivo de cada intervenção.
- Critérios de encerramento e condições que impediram a continuidade.

Comparações entre execuções deverão partir de estados equivalentes da aplicação.

## 5. Investigações selecionadas

Para o experimento com o agente, o grupo selecionou três investigações distintas:

1. **Controle de acesso — Five Star Feedback (T10):** verificar se uma conta sem privilégios consegue excluir feedbacks que não deveria administrar.
2. **Injeção em consultas — Login Admin (T16):** verificar se entradas manipuladas no login alteram a consulta e permitem autenticação administrativa sem a senha correta.
3. **Exposição de dados e arquivos — Confidential Document (T26):** verificar se um documento confidencial pode ser acessado sem autenticação.

Os testes deverão usar o modelo de registro da seção 4.1, permanecer no Juice Shop local e ser restaurados entre experimentos comparáveis.

## 6. Referências e rastreabilidade

- [Playlist original — Hacksplained](https://www.youtube.com/playlist?list=PL8j1j35M7wtKXpTBE6V1RlN_pBZ4StKZw).
- [Repositório oficial — índice de vídeos e soluções, incluindo a referência às versões 10 e 11 da série](https://github.com/juice-shop/juice-shop/blob/master/SOLUTIONS.md?plain=1).
- [Pwning OWASP Juice Shop — índice oficial de desafios](https://pwning.owasp-juice.shop/companion-guide/latest/part2/README.html).

As referências temáticas foram indicadas junto às respectivas tabelas. As hipóteses, ferramentas e critérios de evidência são propostas de planejamento e deverão ser ajustados ao ambiente real do grupo.

Os IDs T01 a T50 organizam este documento por tema; não correspondem à posição original dos vídeos na playlist nem aos identificadores internos da aplicação.
