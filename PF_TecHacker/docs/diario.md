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

**Estado:** organização inicial concluída e versionada.
**Commit confirmado:** `8fc6bff` — `docs: registra requisitos e rotina do projeto`.
Na conferência seguinte, a árvore estava limpa e `main` coincidia com a referência
local `origin/main`; não foi realizada uma nova consulta ao servidor GitHub.
**Próxima ação:** preparar a instalação do Juice Shop a partir da configuração
atual do kit, com proposta técnica submetida à revisão antes de instalar.

A configuração atual do laboratório pode ser levantada antes da instalação do
Juice Shop: o sistema operacional orienta a instalação, e a conectividade define
o acesso a partir do Kali e o escopo local. Esse levantamento não é pré-requisito
para o commit documental. CPU, RAM e GPU permanecem adiados. Não copiar os IPs
antigos como fatos atuais.

### Registro para apresentação futura

Tema deste marco: organizar um laboratório e um fluxo de revisão que tornem a
assistência de IA rastreável. Ainda não há resultados experimentais para divulgar.
Fontes: F01–F08. Evidência atual: arquivos documentais e histórico da conversa.

## 27/10/2026 — levantamento inicial do Dell

**Origem da evidência:** saídas de comandos enviadas pelo usuário nesta conversa,
executados presencialmente no Dell. Não houve acesso remoto pelo assistente.
**Tempo efetivamente dedicado:** não medido.

| Verificação | Resultado observado |
|---|---|
| `cat /etc/os-release` | Ubuntu 22.04.5 LTS, Jammy, versão base 22.04 |
| `ip -br address` | Interface `enp0s31f6` em estado UP, IPv4 `10.0.80.3/24` |
| `ip route` | Rede conectada `10.0.80.0/24`; rota padrão via `10.0.80.1` |
| `docker --version` | Comando não encontrado; instalação funcional não demonstrada |

O usuário confirmou acesso presencial ao kit e Kali em VM no VirtualBox.
O modo de rede da VM ainda não foi informado. Os endereços do Dell coincidem com
o registro histórico, mas essas saídas não identificam o sistema do gateway nem
comprovam acesso ao Dell pelo computador pessoal ou pelo Kali.

### Verificação do SSH e da rede do computador pessoal

O usuário enviou os seguintes resultados adicionais:

- No Dell, `systemctl status ssh --no-pager` retornou
  `Unit ssh.service could not be found.`
- No Dell, `ss -ltn 'sport = :22'` não listou sockets em escuta.
- No PC Ubuntu, `wlo1` está UP com `10.100.26.63/20`; `enp2s0` está DOWN.
- No PC, a rede conectada é `10.100.16.0/20` e a rota padrão usa `10.100.16.1`.

Essas evidências não demonstram um servidor SSH disponível no Dell. O PC e o Dell
estão em sub-redes diferentes; a existência de rota padrão no PC não comprova
nem descarta um caminho funcional até o Dell. Ainda faltam a ligação física atual
e as interfaces/endereço do appliance para definir esse acesso.

Por inspeção presencial, o usuário identificou que o cabo azul provavelmente liga
a interface Ethernet do Dell à porta `ETH1` do appliance. Essa observação indica
o cabeamento físico, mas não comprova o sistema, a função lógica da porta ou o
endereço atual do appliance. O sistema pfSense ainda não foi confirmado.

O Dell respondeu ao gateway `10.0.80.1` em três tentativas, sem perda, com tempo
médio informado de 0,263 ms. A tabela de vizinhos associou esse endereço ao MAC
`60:be:b4:1e:52:1d` pela interface `enp0s31f6`, em estado `REACHABLE`. Isso confirma
comunicação local entre o Dell e o equipamento no endereço do gateway. Uma consulta
HTTPS à porta 443 expirou após cinco segundos; portanto, não demonstrou uma
interface web nessa porta e não identificou o sistema.

O relatório anterior registra que o painel do appliance havia sido configurado em
HTTP na porta 8080 (`http://10.0.80.1:8080`). Trata-se de configuração histórica,
ainda sujeita a verificação no equipamento atual.

A consulta HTTP à porta 8080 retornou `200 OK`, com servidor `nginx`, conteúdo
HTML/PHP e cookie de sessão. A resposta comprova uma aplicação web ativa no
gateway e é coerente com o painel histórico, mas os cabeçalhos não bastam para
identificá-la como pfSense. A identidade visual ainda precisa ser conferida no
navegador ou console, sem registrar credenciais.

O Dell alcançou `1.1.1.1` em três tentativas, sem perda, e `getent hosts
ubuntu.com` retornou endereços IPv6. Assim, há evidência de saída IPv4 e resolução
de nome. Não foi testada nesta coleta uma conexão HTTP/HTTPS externa nem a saída
IPv6; o resultado de DNS isolado não comprova conectividade IPv6.

No PC Ubuntu, `ip route get 10.0.80.3` indicou encaminhamento pelo gateway do
Wi-Fi `10.100.16.1`, usando a origem `10.100.26.63`. Três solicitações ICMP ao
Dell resultaram em 100% de perda. Logo, não há acesso direto demonstrado do PC ao
Dell por esse caminho. O resultado não permite distinguir ausência de rota de
retorno, filtragem no trajeto ou filtragem no destino. Instalar o servidor SSH,
isoladamente, não resolveria essa falta de conectividade.

Para o acesso administrativo e o futuro acesso do Kali, é necessário identificar
a WAN do appliance e então revisar uma opção: encaminhamento restrito no firewall,
VPN existente ou conexão do PC à LAN por um meio apropriado. Não assumir que uma
porta livre do appliance pertence à LAN sem conferir sua atribuição.

### Consulta ao histórico de credenciais do pfSense

Foi feita uma busca nos arquivos textuais e nomes de arquivos dos projetos atual
e anterior, excluindo imagens e PDFs. Não foi localizado arquivo de credenciais
nem uma senha personalizada do painel. O relatório anterior afirma que senhas
reais não foram incluídas no repositório e documenta somente a credencial de
fábrica após um reset. Ele também deixava como pendência confirmar o reset e
trocar a senha administrativa. Portanto, o histórico não comprova qual credencial
está ativa hoje; uma tentativa local com a credencial de fábrica pode verificar
se a pendência permaneceu, sem registrar a senha no projeto.

**Próximo passo:** confirmar o cabeamento do Dell e a configuração atual do
appliance; propor acesso administrativo e habilitação do SSH para revisão.
Não instalar Docker nem alterar firewall/rede nesta coleta.
CPU, RAM e GPU continuam adiados. Hipóteses de segurança ainda não foram propostas.

**Aprendizado:** sistema operacional e configuração de rede orientam a instalação
e o acesso; possuir uma rota padrão não demonstra, sozinho, conectividade funcional.
Fontes F03 e F11. Alterações documentais aguardam revisão e commit.

## 29/10/2026 — confirmação do pfSense e retomada

**Meta da sessão:** concluir o inventário de rede e definir o caminho de acesso
administrativo antes da instalação do laboratório. **Tempo dedicado:** em andamento;
o grupo preencherá o total ao encerrar.

O usuário confirmou visualmente o pfSense em `http://10.0.80.1:8080` e conseguiu
autenticar localmente. Duas fotografias do painel, inspecionadas fora do repositório,
mostram:

| Item | Evidência observada |
|---|---|
| WAN | UP, `1000baseT full-duplex`, endereço `192.168.20.30` |
| LAN | UP, `1000baseT full-duplex`, endereço `10.0.80.1` |
| Sistema | pfSense `2.7.2-RELEASE` (amd64), FreeBSD `14.0-CURRENT` |
| Acesso observado | Sessão administrativa originada do Dell `10.0.80.3` |

Os nomes lógicos e endereços são suficientes para desenhar a topologia atual.
Os nomes internos dos dispositivos físicos podem ser coletados depois, caso seja
necessário diagnosticar ou reatribuir portas; nenhuma reatribuição é planejada agora.

As fotos originais não foram copiadas para o repositório: uma delas exibe o Netgate
Device ID e outros detalhes administrativos que não são necessários para a entrega
pública. Uma imagem sanitizada poderá ser preparada posteriormente, após revisão.

**Interpretação:** a WAN do pfSense está na rede cabeada `192.168.20.0/24`; a LAN
protegida contém o Dell em `10.0.80.3/24`. O PC do usuário permanece no Wi-Fi
`10.100.16.0/20`, portanto os dados explicam por que ele não possui acesso direto
demonstrado ao Dell. Ainda falta registrar o modo de rede da VM Kali e escolher o
caminho controlado do PC/Kali até os serviços internos.

O usuário confirmou que o Adaptador 1 da VM Kali é uma Intel PRO/1000 MT Desktop
configurada em modo NAT no VirtualBox. Nesse modo, a VM utiliza a conectividade do
host para sair; a configuração não cria, por si só, um caminho físico ou roteado
até a LAN do Dell. Assim, a ausência de acesso demonstrado do host ao laboratório
também bloqueia o acesso esperado do Kali enquanto essa topologia for mantida.

Com sistema, endereçamento, interfaces lógicas, ligação Dell–appliance e modo de
rede da VM identificados, o inventário necessário para decidir o acesso está
concluído. O próximo passo é escolher e validar um caminho de rede, não coletar
mais características gerais do equipamento.

### Ajuste do método de estudo

O usuário observou que a discussão avançou rápido demais pelos conceitos e pediu
que cada passo passe a ser apresentado com explicação, analogia e exemplo concreto.
As instruções de colaboração foram atualizadas: antes de comandos ou mudanças,
devem ser explicitados o papel do componente, sua relação com os demais, o motivo
da decisão, o efeito esperado, a validação e a reversão. Também será indicado o
que é requisito do enunciado e o que é escolha de arquitetura do grupo.

Após comparar instalação direta e contêiner, o usuário escolheu executar o Juice
Shop diretamente com Node.js no Ubuntu do Dell. Docker não é requisito do enunciado
e foi descartado para esta implementação. A proposta passa a usar Node.js 24.x,
recomendado pelo guia do Juice Shop v20.3.0, e avaliar primeiro a distribuição
pré-empacotada oficial. A instalação ainda não foi executada.

### Pré-verificação para Node.js e Juice Shop

O usuário executou a verificação no Dell e informou:

| Item | Resultado |
|---|---|
| Arquitetura | `amd64` |
| Node.js | comando não encontrado; sugestão automática do `apt` não executada |
| Partição raiz | 221 GB totais, 188 GB disponíveis, 11% de uso |
| TCP 3000 | nenhuma entrada em escuta; porta disponível |
| Ferramentas | `curl`, `tar` e `sha256sum` presentes em `/usr/bin` |

Os requisitos locais para a instalação pré-empacotada estão atendidos. A release
oficial v20.3.0 oferece o arquivo `juice-shop-20.3.0_node24_linux_x64.tgz`, cujo
SHA-256 publicado é `47420604f215eb412cc02890973ee208a63fc0c62fe7da1d64ac5743b12c1186`.
O Node.js será instalado inicialmente no diretório do usuário, sem substituir
binários do sistema. A execução ainda depende da vistoria dos comandos.

O Node.js v24.22.2 foi posteriormente extraído em
`/home/kit10/lab-tech-hacker/runtime/node-v24.22.2`. Na sessão de terminal, o
usuário adicionou temporariamente seu diretório `bin` ao `PATH` e validou:

- `command -v node`: `/home/kit10/lab-tech-hacker/runtime/node-v24.22.2/bin/node`;
- `node --version`: `v24.22.2`;
- `npm --version`: `11.19.1`.

O primeiro teste de checksum falhou porque `SHASUMS256.txt` não estava no diretório
de trabalho; a mensagem de formato do `sha256sum` foi consequência da entrada vazia
produzida pelo `grep`, não evidência de corrupção do pacote. A execução do Node
comprova que o pacote foi extraído. O usuário confirmou posteriormente que a
verificação corrigida retornou `node-v24.22.2-linux-x64.tar.xz: OK`. O `PATH` ainda
não foi persistido no perfil ou no sistema.

O pacote `juice-shop-20.3.0_node24_linux_x64.tgz` também retornou `OK` contra o
SHA-256 publicado na release oficial. A listagem, feita sem extração, mostrou uma
única raiz `juice-shop_20.3.0/`, contendo `package.json`, código compilado em
`build/`, configurações e demais arquivos da distribuição. A etapa seguinte é
extrair essa raiz versionada e inspecionar o script `start` antes de executá-lo.

O código oficial inicia o servidor informando a porta, sem fixar um endereço de
escuta no `server.listen`. Por isso, a restrição a `127.0.0.1` não será presumida
na instalação direta: o endereço real será conferido com `ss`, e firewall/NAT
serão revisados antes de qualquer acesso externo.

Após a extração, o usuário confirmou `package.json` e `node_modules` presentes,
484 MB de espaço ocupado e os seguintes metadados: aplicação `juice-shop` v20.3.0,
engine Node `24` e script `start` igual a `node build/app`. O UFW do Dell está
inativo, portanto não há regra de firewall de host demonstrada para bloquear a
porta 3000.

Uma captura da lista de regras WAN do pfSense mostrou bloqueios explícitos para
TCP/22, ICMP echo e TCP/443; permissão UDP/1194 para OpenVPN; e regras antigas
associadas a NAT para WordPress/HTTP 80 e Nextcloud/8000. Não há porta 3000 visível
nessa lista. A tela de regras WAN mostra o filtro após a tradução e não substitui
a conferência de `Firewall > NAT > Port Forward`, onde origem externa e destino
interno do encaminhamento podem ser vistos diretamente. Nenhuma regra foi alterada.

A captura posterior de `Firewall > NAT > Port Forward` confirmou duas regras
herdadas e habilitadas: WAN TCP/80 para o alias `SRV_WEB` na porta 80 (WordPress)
e WAN TCP/8000 para `SRV_WEB` na porta 8000 (Nextcloud). Não existe encaminhamento
para TCP/3000. A regra do Nextcloud exibe ainda porta de origem 80, restrição
incomum para conexões de clientes e que será analisada fora desta instalação.
O valor atual do alias `SRV_WEB` não foi conferido nesta captura. Nenhuma regra
foi criada, removida ou editada.

### Primeira execução local do Juice Shop

O usuário iniciou a aplicação com `npm start`. Durante a execução, `ss -ltnp
'sport = :3000'` mostrou um socket `LISTEN` na porta 3000 sem endereço local
restrito, associado ao processo `MainThread` (PID observado 428257). A ausência
de um endereço específico e os testes seguintes demonstram escuta nas interfaces
disponíveis do Dell.

Requisições HTTP HEAD a `http://127.0.0.1:3000` e
`http://10.0.80.3:3000` retornaram `HTTP/1.1 200 OK`, `Content-Type:
text/html; charset=UTF-8` e o mesmo tamanho de conteúdo (9984 bytes). Isso confirma
resposta pelo loopback e pelo endereço da LAN. O navegador do próprio Dell também
renderizou a interface do Juice Shop. Não existe ainda NAT TCP/3000 na WAN.

Não atualizar o pfSense durante esta etapa apenas porque o painel informa uma
versão disponível. Uma atualização alteraria a base do laboratório e exige proposta,
backup da configuração, janela de indisponibilidade e validação próprios.

## 30/10/2026 — parada e restauração do Juice Shop

**Meta da sessão:** comprovar que a aplicação para de forma controlada, reinicia
com as mesmas versões e retorna a um estado conhecido. **Tempo dedicado:** em
andamento; o grupo preencherá o total ao encerrar.

**Ponto de partida:** Node.js v24.22.2 e Juice Shop v20.3.0 estão instalados no
diretório do usuário e tiveram checksums validados. A primeira execução respondeu
por loopback e LAN, sem NAT WAN/3000. Ainda faltam evidências da porta fechada após
o encerramento e do comportamento de restauração.

**Sequência aprovada para estudo:** verificar se a porta está fechada; iniciar pelo
caminho absoluto; produzir uma alteração funcional controlada; encerrar e reiniciar;
verificar se a alteração foi removida pelo self-healing. Não alterar pfSense,
VirtualBox ou regras de rede nesta etapa.

O usuário confirmou que `ss -ltnp 'sport = :3000'` não apresentou socket em
estado `LISTEN` no início da sessão. Isso evidencia que a instância anterior foi
encerrada e que a porta 3000 estava livre antes do teste de restauração.

O usuário iniciou novamente a aplicação pelo Node.js fixado, criou uma conta
descartável pela interface normal e comprovou que ela existia. Após encerrar e
reiniciar a aplicação, a conta deixou de existir. O teste demonstra que o
self-healing da versão v20.3.0 recriou o banco usado pela instância neste cenário.
Nenhuma credencial do teste foi registrada.

**Conclusão do teste:** o reinício é um procedimento de restauração validado para
o estado mutável coberto pelo self-healing. A evidência não afirma que o reinício
repara Node.js, arquivos da distribuição ou configuração do sistema; para esses
casos, o pacote original verificado continua preservado em `downloads/` e permite
reextração controlada.

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
