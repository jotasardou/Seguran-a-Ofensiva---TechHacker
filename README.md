# Tecnologias Hacker — agente de IA supervisionado

Projeto acadêmico para investigar como um modelo de linguagem local pode apoiar
testes de segurança em uma instância local do OWASP Juice Shop, com decisões e
execuções supervisionadas pelo grupo.

**Estado atual:** Juice Shop acessível pelo Kali através de VPN e restauração
local validados. Modelo, agente e investigações ainda estão pendentes.

O objetivo de estudo é compreender as decisões técnicas, registrar evidências e
avaliar onde a IA ajuda, erra ou exige intervenção humana. A quantidade de
vulnerabilidades encontradas não é a medida de sucesso.

O plano inicial de testes será elaborado pelo grupo sem auxílio de LLM, conforme
o enunciado. As investigações ficam restritas à instância autorizada do Juice Shop.

## Navegação

| Documento | Finalidade |
|---|---|
| [Requisitos](docs/requisitos.md) | Obrigações do enunciado e critérios de conclusão |
| [Cronograma](docs/cronograma.md) | Entregas, sessões e commits previstos |
| [Laboratório](docs/laboratorio.md) | Instalação, execução, validação e restauração já comprovadas |
| [Fontes](docs/fontes.md) | Referências consultadas e decisões que sustentam |

## Laboratório

O alvo roda diretamente em Node.js no Ubuntu; o Kali acessa a rede do alvo por
OpenVPN no pfSense. [Instalação e verificação](docs/laboratorio.md) descreve o
estado validado. Os endereços da topologia são exemplos da instalação original e
devem ser adaptados à rede de quem reproduzir o laboratório.

## Entrega acadêmica

Laboratório reproduzível, código do agente, registros de três investigações,
relatório de 4–6 páginas e vídeo de até 10 minutos. Todos os testes ficam restritos
ao Juice Shop local autorizado. A matriz de requisitos detalha o aceite.

O perfil VPN, credenciais, capturas e anotações de sessões ficam fora do repositório.
