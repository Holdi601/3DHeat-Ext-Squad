---
title: A tabela
nav_order: 4
lang: pt
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# A tabela: `<demo>.parquet` {#the-table-parquet}

Uma linha por amostra ou evento. Uma amostra é tomada sempre que o servidor replicou
o movimento do ator, até 8 vezes por segundo (a taxa de gravação da demo)
enquanto ele se move.

![As primeiras linhas da tabela de uma demo sintética](../assets/img/table.svg)

## Colunas {#columns}

| Coluna | O que é |
|---|---|
| `time` | segundos desde o início da gravação |
| `x`, `y`, `z` | posição em unidades do Unreal (centímetros), Z para cima |
| `dirX`, `dirY`, `dirZ` | para onde um soldado olha: o yaw do corpo e a inclinação da visão, como vetor unitário (o de um veículo: nivelado) |
| `yaw`, `pitch` | o mesmo em graus; `pitch` para cima a partir do horizonte, só para soldados |
| `health` | a vida do soldado, do bot ou do veículo naquele momento, quando o servidor a enviou (a de um soldado cai abaixo de 0 enquanto ferido) |
| `speed` | a velocidade replicada, cm/s |
| `player` | o nome do jogador; `bot <id>` para um bot; para um veículo ou implantável que ninguém possui, a sua classe; para um tiro de arma de veículo, o jogador sentado nesse veículo |
| `team`, `faction` | o número da equipe do Squad (1, 2) e a sua configuração de facção, **naquele momento**: jogadores podem trocar de lado |
| `squad` | o número do pelotão, -1 quando não está em um |
| `event` | o que a linha representa (abaixo) |
| `pawn` | o blueprint do soldado (`SQSquidBot` para um bot), o veículo, ou, para `fire`, a arma |
| `seat` | para um assento de torre ou de passageiro, o próprio pawn do assento |
| `detail` | para `fire`, a chamada da arma que posicionou o tiro; para `hit`, o tipo de dano; para `removed`, o motivo do fechamento do canal (`Destroyed`, `Dormancy`...) |
| `entity` | o ator a que a linha se refere (o seu GUID de rede): o `entity` das linhas dos auxiliares |
| `match` | o nome da demo |

## Eventos {#events}

| `event` | Na linha de | O que é |
|---|---|---|
| `position` | um soldado ou bot a pé | uma amostra de movimento |
| `vehicle` | um soldado em um veículo terrestre ou helicóptero | uma amostra na posição do veículo |
| `wounded`, `revived`, `death` | soldados e bots | onde aconteceu |
| `spawn`, `damaged`, `destroyed`, `removed` | veículos, implantáveis, postos de tiro, caixas, helicópteros | onde estavam |
| `seat` | um jogador | ocupou um assento |
| `fire` | o atirador | um tiro: de onde saiu, sua direção como `yaw`/`pitch`/`dirX..Z` |
| `hit` | o veículo | um acerto no veículo: onde |

Como os eventos são lidos está em [Como uma demo é lida](how-it-works.md#how-the-events-are-read).

## No visualizador {#in-the-viewer}

O rodapé do Parquet traz instruções de leitura sob a chave `heat3d`: Z para cima,
nenhum eixo espelhado, escala unitária 1, então o visualizador não precisa de mapeamento de colunas. Carregue
a tabela na aba Mapa de calor; veja [Obter dados](https://holdi601.github.io/3DHeat/getting-data-in.html)
e [Mapeamento de colunas](https://holdi601.github.io/3DHeat/column-mapping.html) no visualizador.
