---
title: Limites, atualizações e termos
nav_order: 7
lang: pt
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Limites, atualizações e termos {#limits-updates-and-terms}

## Não lido {#not-read}

- **Quem matou quem, e o dano a soldados por acerto.** Estes viajam nos resultados de acerto das chamadas remotas das armas e dos estados de jogador (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), cuja estrutura não é lida; são guardados inteiros no auxiliar de entidades. Só a vida das vítimas é decodificada.
- **A equipe do bot.** O estado de um bot traz um número que pode ser a sua equipe; não confirmado, não usado.
- **Para onde um soldado olha de lado**, além do yaw do corpo.

## Atualizações do jogo {#game-updates}

O leitor depende do formato de repetição do motor e de um punhado de nomes de classes e propriedades do Squad. Ele não depende de layouts de propriedades que não consegue ver: a própria repetição os nomeia.

**O que pode quebrar com uma atualização do Squad:**

- **Uma atualização do motor.** O Squad passou para o UE 5.7 com a v10.4, e isso não foi testado nela. A atualização pode mudar o cabeçalho do bunch, os dados de surgimento ou o `FRepMovement`. Eles são controlados por versão no código onde a mudança é conhecida. Passos desconhecidos (`ENG_PARTIAL_CUSTOM_EXPORTS`, o bit final de movimento) estão fixados no que a v10.3.1 faz.
- **Replicação Iris.** Se o Squad mudar para o Iris, o fluxo dentro dos blocos seria novo e este leitor não o leria. A v10.3.1 do Squad usa o sistema clássico (ele roda com o ReplicationGraph).
- **Classes ou propriedades renomeadas.** Se o Squad renomear suas classes de jogador, equipe ou pelotão, ou as suas propriedades, nomes ou equipes desapareceriam, mas as posições não.
- **O que acontece em caso de falha.** Quando o formato muda, o leitor falha de forma clara, com erros de fluxo ou de movimento nos diagnósticos. Ele não produz posições erradas em silêncio: o `FRepMovement` só é aceito quando os seus bits fecham exatamente.

## Dados pessoais {#personal-data}

Uma demo guarda os nomes e os IDs online de todos no servidor. A tabela e o documento da partida trazem nomes, não IDs. Os auxiliares guardam os bits de cada propriedade, então guardam os IDs como a demo os tem (sem decodificar). Trate todos eles como a própria demo.

## Licença e fontes {#licence-and-sources}

MIT; veja [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Tudo aqui foi escrito para este pacote. Nenhum código de terceiros está incluído ou vinculado: as únicas dependências são pyarrow (Apache-2.0) e numpy (BSD-3-Clause).

Os fatos sobre o formato vieram destas fontes:

- **Unreal.Core** no [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Descreve o layout genérico de repetições do Unreal: o bloco de informações, os blocos, os quadros, os bunches e as tabelas de exportação de campos de rede.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). O seu analisador foi lido para o layout como o Squad v10.3.1 o grava, para as verificações de versão, e para saber quais classes do Squad carregam os dados do elenco. As suas demos de teste publicadas e as contagens de referência foram usadas como verificação cruzada independente. Nenhum do seu código foi copiado ou traduzido: este leitor é estruturado de outra forma (um arquivo de bits em Python sobre pacotes inteiros, bunches parciais unidos bit a bit, propriedades despachadas pelo nome), e duas coisas que ele não faz foram encontradas aqui nas próprias demos: o terceiro sinalizador de bunch parcial e o bit final de movimento.

Squad é uma marca registrada da Offworld Industries. Este pacote lê arquivos que um servidor do Squad grava; ele não toca no jogo, no seu código nem nos seus arquivos. A política de licenciamento e administração de servidores da Offworld não diz nada sobre gravar ou analisar demos. O EULA do Squad proíbe a engenharia reversa do próprio jogo, o que este pacote não faz.
