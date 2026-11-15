---
title: Tabellen
nav_order: 4
lang: sv
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabellen: `<demo>.parquet` {#the-table-parquet}

En rad per prov eller händelse. Ett prov tas när servern replikerade aktörens rörelse, upp till 8 gånger per sekund (demons inspelningstakt) medan den rör sig.

![De första raderna i en syntetisk demos tabell](../assets/img/table.svg)

## Kolumner {#columns}

| Kolumn | Vad den är |
|---|---|
| `time` | sekunder sedan inspelningen startade |
| `x`, `y`, `z` | position i Unreal-enheter (centimeter), Z uppåt |
| `dirX`, `dirY`, `dirZ` | vart en soldat tittar: kroppens gir och synvinkelns lutning, som en enhetsvektor (för ett fordon: plant) |
| `yaw`, `pitch` | samma i grader; `pitch` uppåt från horisonten, bara soldater |
| `health` | soldatens, botens eller fordonets hälsa vid det ögonblicket, där servern skickade den (en soldats sjunker under 0 medan den är sårad) |
| `speed` | den replikerade hastigheten, cm/s |
| `player` | spelarens namn; `bot <id>` för en bot; för ett fordon eller en utplacerad sak som ingen äger, dess klass; för ett skott från ett fordons vapen, spelaren som satt i det fordonet |
| `team`, `faction` | Squads lagnummer (1, 2) och dess fraktionsuppsättning, **vid det ögonblicket**: spelare kan byta sida |
| `squad` | truppnumret, -1 när man inte är i en trupp |
| `event` | vad raden är (nedan) |
| `pawn` | soldatens blueprint (`SQSquidBot` för en bot), fordonet, eller för `fire` vapnet |
| `seat` | för en kanon- eller passagerarplats, platsens egen pjäs |
| `detail` | för `fire` vapnets anrop som placerade skottet, för `hit` skadetypen, för `removed` varför kanalen stängdes (`Destroyed`, `Dormancy`...) |
| `entity` | aktören raden handlar om (dess nätverks-GUID): sidofilernas `entity` |
| `match` | demons namn |

## Händelser {#events}

| `event` | På raden för | Vad |
|---|---|---|
| `position` | en soldat eller bot till fots | ett rörelseprov |
| `vehicle` | en soldat i ett markfordon eller en helikopter | ett prov vid fordonets position |
| `wounded`, `revived`, `death` | soldater och bots | var det hände |
| `spawn`, `damaged`, `destroyed`, `removed` | fordon, utplacerade saker, bunkrar, lådor, helikoptrar | var de var |
| `seat` | en spelare | tog en plats |
| `fire` | skytten | ett skott: var det lämnade, dess riktning som `yaw`/`pitch`/`dirX..Z` |
| `hit` | fordonet | en träff på fordonet: var |

Hur händelserna läses beskrivs i [Så läses en demo](how-it-works.md#how-the-events-are-read).

## I visaren {#in-the-viewer}

Parquet-sidfoten bär läsanvisningar under nyckeln `heat3d`: Z uppåt,
ingen axel speglad, enhetsskala 1, så visaren behöver ingen kolumnmappning. Läs in
tabellen i Värmekarta-fliken; se visarens
[Hämta data](https://holdi601.github.io/3DHeat/getting-data-in.html)
och [Kolumnmappning](https://holdi601.github.io/3DHeat/column-mapping.html).
