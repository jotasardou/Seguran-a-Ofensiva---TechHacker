# Laboratório — Juice Shop no Dell

Este documento descreve somente o estado já implementado e validado no Dell.
Acesso pelo Kali, execução automática e integração com o agente ainda não estão
configurados.

## Componentes confirmados

| Componente | Versão ou endereço |
|---|---|
| Dell OptiPlex Micro 7020 | Ubuntu 22.04.5 LTS · `10.0.80.3/24` |
| Gateway da LAN | pfSense `2.7.2-RELEASE` · `10.0.80.1` |
| WAN do pfSense | `192.168.20.30` |
| Node.js | `v24.22.2` · instalação no diretório do usuário |
| npm | `11.19.1` |
| OWASP Juice Shop | `v20.3.0` · pacote para Node 24, Linux x64 |

O pfSense não possui encaminhamento WAN para TCP/3000. O UFW do Dell estava
inativo durante a validação. A aplicação escutou nas interfaces disponíveis do
Dell e respondeu por loopback e LAN.

## Estrutura no Dell

```text
/home/kit10/lab-tech-hacker/
├── downloads/
│   ├── SHASUMS256.txt
│   ├── node-v24.22.2-linux-x64.tar.xz
│   └── juice-shop-20.3.0_node24_linux_x64.tgz
├── runtime/
│   └── node-v24.22.2/
└── apps/
    └── juice-shop_20.3.0/
```

`downloads/` preserva os arquivos originais. `runtime/` contém o interpretador
Node.js. `apps/` contém a distribuição extraída do Juice Shop.

## Preparar e baixar

No Ubuntu 22.04 do Dell, criar os diretórios sem privilégios administrativos:

```bash
mkdir -p /home/kit10/lab-tech-hacker/downloads
mkdir -p /home/kit10/lab-tech-hacker/runtime/node-v24.22.2
mkdir -p /home/kit10/lab-tech-hacker/apps
cd /home/kit10/lab-tech-hacker/downloads
```

Baixar Node.js e sua lista oficial de checksums:

```bash
curl -fLO https://nodejs.org/dist/v24.22.2/node-v24.22.2-linux-x64.tar.xz
curl -fLO https://nodejs.org/dist/v24.22.2/SHASUMS256.txt
```

Baixar a distribuição do Juice Shop compatível com Node 24 e Linux x64:

```bash
curl -fL \
  -o juice-shop-20.3.0_node24_linux_x64.tgz \
  https://github.com/juice-shop/juice-shop/releases/download/v20.3.0/juice-shop-20.3.0_node24_linux_x64.tgz
```

Nenhum arquivo baixado deve ser extraído antes das verificações a seguir.

## Integridade dos downloads

No diretório de downloads, o Node.js foi conferido contra a lista publicada pelo
próprio projeto:

```bash
cd /home/kit10/lab-tech-hacker/downloads
sha256sum -c <(grep ' node-v24.22.2-linux-x64.tar.xz$' SHASUMS256.txt)
```

Resultado observado:

```text
node-v24.22.2-linux-x64.tar.xz: OK
```

O Juice Shop foi conferido contra o SHA-256 publicado na release v20.3.0:

```bash
printf '%s  %s\n' \
  '47420604f215eb412cc02890973ee208a63fc0c62fe7da1d64ac5743b12c1186' \
  'juice-shop-20.3.0_node24_linux_x64.tgz' \
  | sha256sum -c -
```

Resultado observado:

```text
juice-shop-20.3.0_node24_linux_x64.tgz: OK
```

## Extrair

Após os dois resultados `OK`, extrair o Node.js no runtime versionado:

```bash
tar -xJf /home/kit10/lab-tech-hacker/downloads/node-v24.22.2-linux-x64.tar.xz \
  -C /home/kit10/lab-tech-hacker/runtime/node-v24.22.2 \
  --strip-components=1
```

Extrair o Juice Shop. O pacote já contém a raiz `juice-shop_20.3.0/`:

```bash
tar -xzf /home/kit10/lab-tech-hacker/downloads/juice-shop-20.3.0_node24_linux_x64.tgz \
  -C /home/kit10/lab-tech-hacker/apps
```

Validar as versões e a presença das dependências:

```bash
/home/kit10/lab-tech-hacker/runtime/node-v24.22.2/bin/node --version
cd /home/kit10/lab-tech-hacker/apps/juice-shop_20.3.0
test -f package.json && echo "package.json presente"
test -d node_modules && echo "node_modules presente"
```

## Iniciar manualmente

Entrar na raiz da aplicação é necessário porque ela usa caminhos relativos para
configurações e arquivos:

```bash
cd /home/kit10/lab-tech-hacker/apps/juice-shop_20.3.0
```

Executar explicitamente com o Node.js validado:

```bash
/home/kit10/lab-tech-hacker/runtime/node-v24.22.2/bin/node build/app
```

O processo permanece no primeiro plano. Enquanto ele está ativo, a aplicação
responde no Dell em:

```text
http://127.0.0.1:3000
http://10.0.80.3:3000
```

O acesso pela WAN não foi configurado.

## Validar a execução

Em outro terminal:

```bash
ss -ltnp 'sport = :3000'
curl -I --connect-timeout 5 http://127.0.0.1:3000
curl -I --connect-timeout 5 http://10.0.80.3:3000
```

Na validação realizada, o socket apareceu em `LISTEN` sem restrição a um endereço
local específico e as duas requisições retornaram `HTTP/1.1 200 OK`.

## Parar

No terminal que executa o Node.js, pressionar `Ctrl+C`. Depois, verificar:

```bash
ss -ltnp 'sport = :3000'
```

Sem uma linha `LISTEN`, não há processo esperando conexões nessa porta. Esse
resultado foi confirmado antes do teste de restauração.

## Restaurar pelo self-healing

O procedimento validado é:

1. parar a aplicação com `Ctrl+C`;
2. confirmar que a porta 3000 foi fechada;
3. iniciar novamente pelo comando documentado acima;
4. validar a resposta HTTP.

Como evidência, foi criada e validada uma conta descartável. Após parar e iniciar
novamente, a conta deixou de existir. Isso demonstra a recriação do banco da
instância nesse cenário.

O self-healing restaura o estado mutável tratado pela aplicação. Ele não reinstala
Node.js nem recupera arquivos da distribuição que tenham sido alterados fora desse
mecanismo. Os pacotes originais verificados são preservados para uma futura
reextração, caso seja necessário testar esse nível de recuperação.

## Estado e limites atuais

- O Juice Shop é iniciado manualmente e depende de um terminal aberto.
- Não existe unidade `systemd` nem inicialização automática.
- Não existe NAT WAN/3000 no pfSense.
- O Kali em modo NAT ainda não possui caminho demonstrado até o Dell.
- As regras antigas de WordPress e Nextcloud continuam no pfSense e não foram
  alteradas nesta etapa.
- Nenhuma investigação de vulnerabilidade foi iniciada.

## Fontes

- [Executar o OWASP Juice Shop](https://pwning.owasp-juice.shop/companion-guide/latest/part1/running.html)
- [Release v20.3.0](https://github.com/juice-shop/juice-shop/releases/tag/v20.3.0)
- [Downloads oficiais do Node.js](https://nodejs.org/en/download)
