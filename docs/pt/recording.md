---
title: Gravar uma demo
nav_order: 2
lang: pt
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Gravar uma demo {#recording-a-demo}

As demos do Squad são gravadas **no servidor**, não pelo cliente do jogo.

1. No `Admins.cfg` do servidor, dê à sua função de administrador a permissão `demos`.
2. No console do jogo, execute `AdminDemoRec <nome>` quando a partida começar.
   Um administrador precisa digitar isto no próprio jogo; um relato diz que o RCON não aceita.
3. Jogue a partida e depois execute `AdminDemoStop`.
4. A demo é gravada em `<servidor>/SquadGame/Saved/Demos/<nome>.replay`.
   Copie-a do servidor para a máquina que faz a conversão.

O `Server.cfg` também tem uma configuração `RecordDemos`, desligada por padrão. Espere cerca de
70 a 80 MB por hora para uma partida pequena; o tamanho de um servidor completo de 100 jogadores
ainda não foi medido.

Uma demo guarda os nomes e os IDs online de todos no servidor: trate-a como dado pessoal
([Limites, atualizações e termos](limits.md#personal-data)).

Próximo: [Converter demos](converting.md).
