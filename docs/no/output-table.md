---
title: Tabellen
nav_order: 4
lang: "no"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabellen: `<demo>.parquet` {#the-table-parquet}

Én rad per prøve eller hendelse. En prøve tas hver gang serveren replikerte aktørens
bevegelse, opptil 8 ganger i sekundet (demoens opptaksrate) mens den beveger seg.

![De første radene i en syntetisk demos tabell](../assets/img/table.svg)

## Kolonner {#columns}

| Kolonne | Hva den er |
|---|---|
| `time` | sekunder siden opptaket startet |
| `x`, `y`, `z` | posisjon i Unreal-enheter (centimeter), Z opp |
| `dirX`, `dirY`, `dirZ` | hvor en soldat ser: kroppens gir og synsvinkelens stigning, som en enhetsvektor (for et kjøretøy: vannrett) |
| `yaw`, `pitch` | det samme i grader; `pitch` opp fra horisonten, bare soldater |
| `health` | soldatens, bottens eller kjøretøyets helse i det øyeblikket, der serveren sendte den (en soldats synker under 0 mens den er såret) |
| `speed` | den replikerte farten, cm/s |
| `player` | spillerens navn; `bot <id>` for en bot; for et kjøretøy eller utplasserbart objekt ingen eier, dets klasse; for et skudd fra et kjøretøys våpen, spilleren som satt i kjøretøyet |
| `team`, `faction` | Squads lagnummer (1, 2) og dets fraksjonsoppsett, **på det tidspunktet**: spillere kan bytte side |
| `squad` | troppnummeret, -1 når ikke i en tropp |
| `event` | hva raden er (under) |
| `pawn` | soldatens blåkopi (`SQSquidBot` for en bot), kjøretøyet, eller for `fire` våpenet |
| `seat` | for et tårn- eller passasjersete, setets egen pawn |
| `detail` | for `fire` våpenets kall som plasserte skuddet, for `hit` skadetypen, for `removed` hvorfor kanalen ble lukket (`Destroyed`, `Dormancy`...) |
| `entity` | aktøren raden handler om (dens nett-GUID): sidefilenes `entity` for rader |
| `match` | demoens navn |

## Hendelser {#events}

| `event` | På raden til | Hva |
|---|---|---|
| `position` | en soldat eller bot til fots | en bevegelsesprøve |
| `vehicle` | en soldat i et bakkekjøretøy eller helikopter | en prøve på kjøretøyets posisjon |
| `wounded`, `revived`, `death` | soldater og boter | hvor det skjedde |
| `spawn`, `damaged`, `destroyed`, `removed` | kjøretøy, utplasserbare objekter, stillinger, kasser, helikoptre | hvor de var |
| `seat` | en spiller | tok et sete |
| `fire` | skytteren | et skudd: hvor det forlot, dets retning som `yaw`/`pitch`/`dirX..Z` |
| `hit` | kjøretøyet | et treff på kjøretøyet: hvor |

Hvordan hendelsene leses står i [Slik leses en demo](how-it-works.md#how-the-events-are-read).

## I visningsprogrammet {#in-the-viewer}

Parquet-bunnteksten bærer leseinstruksjoner under nøkkelen `heat3d`: Z opp,
ingen akse speilvendt, enhetsskala 1, så visningsprogrammet trenger ingen kolonneoppsett. Last
tabellen inn i Varmekart-fanen; se visningsprogrammets
[Få data inn](https://holdi601.github.io/3DHeat/getting-data-in.html)
og [Kolonneoppsett](https://holdi601.github.io/3DHeat/column-mapping.html).
