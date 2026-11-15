---
title: O documento da partida e os auxiliares
nav_order: 5
lang: pt
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# O documento da partida e os auxiliares {#the-match-document-and-sidecars}

Ao lado da tabela, cada demo ganha `<demo>.match.json` e dois auxiliares,
`<demo>.entities.parquet` e `<demo>.packets.parquet`. O visualizador lê o
documento da partida na sua aba Partida.

## O documento da partida {#the-match-document}

`<demo>.match.json` (o documento da partida) traz no nível superior `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` e `selfCheck` (a lista completa: [Referência de comandos](../cli-reference.md)). Em palavras: o mapa e a camada, as versões do jogo e do motor, a hora da gravação, a duração, e:

- **as equipes**: número, facção e tudo o que o seu estado replicou (tickets, disponibilidades, comandante), à medida que mudava;
- **os pelotões**: número, equipe, nome, criador, líder, membros;
- **o estado do jogo**: nome do servidor e configurações, modo de jogo, estado e id da partida, rotações de mapas e de camadas, votações, cronômetros, a mensagem do dia;
- **os atores**: cada veículo, implantável, posto de tiro, caixa de munição e helicóptero - classe, onde e quando surgiu, quando foi embora, de quem era, e o seu estado replicado (vida, estado de construção, assentos...);
- **uma linha para cada jogador**: amostras a pé e em veículos, distância percorrida, classes de soldado jogadas, veículos usados, mudanças de equipe, assentos ocupados, e tudo o que o estado do jogador replicou (ping, nível, função, assento atual...); e uma linha para cada bot;
- **os eventos** contados, o **censo de propriedades** (quantas vezes foram enviadas as propriedades de cada classe) e o **censo de chamadas remotas**, os tiros e acertos, o que **não** foi lido, e os diagnósticos do leitor;
- **o arquivo e o cabeçalho**: cada campo do bloco de informações e do cabeçalho da demo, a tabela de blocos, as tabelas de exportação de campos de rede (`net_field_exports`), os motivos de fechamento dos canais, e as classes encontradas para objetos que as exportações não nomeiam (`stream.class_resolution`);
- **a autoverificação** (`selfCheck.completeness`, veja [Completude](#completeness)).

Os IDs online (Steam, EOS) ficam de fora de propósito.

Um rápido olhar em uma demo convertida:

```bash
python -c "import json; d = json.load(open('out/<mapa>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Completude {#completeness}

Este leitor segue a regra que todos os conversores do 3DHeat compartilham: decodificar o que pode ser lido agora, guardar o resto inteiro, e dizer quanto de cada tipo ele conseguiu ([Conversores guardam tudo](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Cada documento da partida tem `selfCheck.completeness`: por tipo de item encontrado na demo, quantos foram `seen` (vistos), `decoded` (decodificados), `partial` (decodificados em parte e guardados inteiros), `raw` (só guardados inteiros) e `lost` (perdidos, que deve ser 0). Os tipos são contados onde o leitor os encontra: `file.info`, `chunk.<tipo>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<classe>`, `rpc:<classe>`, `block:<objeto>`, `subobject.*`.

Nas demos reais lidas, `lost` é 0: seus itens vão de centenas de milhares a milhões; cerca de metade decodifica por completo, o resto é parcial ou bruto.

**Lido** (para a tabela e o documento da partida):

- o bloco de informações, o cabeçalho da demo (cada campo; dois bytes finais desconhecidos são guardados em hexadecimal), a tabela de blocos;
- cada quadro, pacote e bunch (divididos inteiros no que carregam), cada ator aberto (com a posição de surgimento, a rotação, a escala e a velocidade) e fechado (com o motivo: `Destroyed`, `Dormancy`...);
- cada propriedade replicada, até onde os seus bits indicam ([Decodificar propriedades](how-it-works.md#decoding-properties)), posições do `FRepMovement` e do componente de movimento dos helicópteros, as baixas, a vida dos veículos, os assentos;
- cada chamada remota pelo nome, com os seus parâmetros quando a demo exporta o grupo da função: tiros (`fire`) e acertos em veículos (`hit`) para a tabela;
- as tabelas de exportação de campos de rede e os GUIDs de rede (a sua contagem; os caminhos estão no auxiliar de entidades).

**Guardado bruto** (inteiro, com o que foi lido ao lado):

- `<demo>.entities.parquet`, colunas `time`, `type` (`<classe>.<propriedade>`, `<classe>.<chamada>`, ou o nome do objeto), `name` (a classe do ator), `entity` (o GUID de rede do ator, como o `entity` da tabela), `kind`, `object` (o subobjeto), `channel`, `handle`, `group` (o caminho de classe do grupo de exportação), `decoded` (JSON), `bits` e `payload` (os bits, do menos para o mais significativo, completados até bytes inteiros):
  - cada atualização de propriedade (`kind` `property`), o movimento incluído, com o que foi decodificado; bruto apenas onde nada foi (identificadores sem nome, estruturas como `RotationReplicatedMovement` de torres, e propriedades deixadas como bits);
  - cada chamada remota e campo de delta personalizado (`rpc`), os parâmetros decodificados onde o grupo da função foi exportado; bruto onde não foram (`RepInventory`, `PlayerStateData`);
  - cada bloco de conteúdo de um objeto cuja classe não pôde ser encontrada (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), com o seu cabeçalho decodificado;
  - cada canal de ator aberto e fechado (`open`, `close`), cada subobjeto excluído ou destruído;
  - o contexto que um decodificador posterior precisa para ler o arquivo sozinho: cada exportação de campo de rede (`export.field`: caminho do grupo, identificador, nome da propriedade, soma de verificação) e cada GUID de rede exportado (`export.guid`: seu caminho, externo e sinalizadores), no momento em que o fluxo os entregou.
- `<demo>.packets.parquet`, colunas `time`, `type`, `name`, `channel`, `offset` (no arquivo), `decoded`, `bits` e `payload`: o bloco de informações, o bloco de cabeçalho, cada bloco de ponto de verificação (um ponto de verificação é o estado de cada ator naquele instante, que o fluxo desde o início também tem), cada bloco de evento, e cada quadro, pacote ou bunch que não é lido (um bunch por demo: o bunch de abertura do próprio ator espectador do gravador), inteiro.

As linhas de entidades são agrupadas por `kind`, `type` e `entity`, cada grupo em ordem de tempo; ordene por `time` para a ordem do fluxo.

**Não disponível:**

- o que uma demo de servidor não registra: as entradas dos clientes, o que um jogador viu;
- efeitos do lado do cliente: marcadores de acerto, sons, o texto do feed de abates (o servidor envia as chamadas, não a sua exibição);
- IDs online decodificados: guardados apenas como bits (veja [Dados pessoais](limits.md#personal-data)).
