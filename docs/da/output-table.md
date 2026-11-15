---
title: Tabellen
nav_order: 4
lang: da
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabellen: `<demo>.parquet` {#the-table-parquet}

Én række pr. prøve eller hændelse. En prøve tages, når serveren har replikeret
aktørens bevægelse, op til 8 gange i sekundet (demoens optagelseshastighed),
mens den bevæger sig.

![De første rækker i en syntetisk demos tabel](../assets/img/table.svg)

## Kolonner {#columns}

| Kolonne | Hvad det er |
|---|---|
| `time` | sekunder siden optagelsen startede |
| `x`, `y`, `z` | position i Unreal-enheder (centimeter), Z op |
| `dirX`, `dirY`, `dirZ` | hvor en soldat kigger: kroppens yaw og visningens pitch, som en enhedsvektor (for et køretøj: vandret) |
| `yaw`, `pitch` | det samme i grader; `pitch` op fra horisonten, kun for soldater |
| `health` | soldatens, bottens eller køretøjets helbred på det tidspunkt, hvor serveren sendte det (en soldats falder under 0, mens den er såret) |
| `speed` | den replikerede hastighed, cm/s |
| `player` | spillerens navn; `bot <id>` for en bot; for et køretøj eller deployable, som ingen ejer, dets klasse; for et skud fra et køretøjs våben, den spiller, der sidder i køretøjet |
| `team`, `faction` | Squads holdnummer (1, 2) og dets fraktionsopsætning, **på det tidspunkt**: spillere kan skifte side |
| `squad` | squadnummeret, -1 når man ikke er i en squad |
| `event` | hvad rækken er (nedenfor) |
| `pawn` | soldat-blueprintet (`SQSquidBot` for en bot), køretøjet, eller for `fire` våbnet |
| `seat` | for et tårn- eller passagersæde, sædets egen pawn |
| `detail` | for `fire` våbnets kald, der placerede skuddet, for `hit` skadetypen, for `removed` hvorfor kanalen lukkede (`Destroyed`, `Dormancy`...) |
| `entity` | aktøren, rækken handler om (dens net-GUID): `entity` i sidefilernes rækker |
| `match` | demoens navn |

## Hændelser {#events}

| `event` | På rækken for | Hvad |
|---|---|---|
| `position` | en soldat eller bot til fods | en bevægelsesprøve |
| `vehicle` | en soldat i et landkøretøj eller helikopter | en prøve ved køretøjets position |
| `wounded`, `revived`, `death` | soldater og bots | hvor det skete |
| `spawn`, `damaged`, `destroyed`, `removed` | køretøjer, deployables, emplacements, kasser, helikoptere | hvor de var |
| `seat` | en spiller | satte sig i et sæde |
| `fire` | skytten | et skud: hvor det forlod, dets retning som `yaw`/`pitch`/`dirX..Z` |
| `hit` | køretøjet | et træf på køretøjet: hvor |

Hvordan hændelserne læses, står i [Sådan læses en demo](how-it-works.md#how-the-events-are-read).

## I fremviseren {#in-the-viewer}

Parquet-footeren bærer læsevejledninger under nøglen `heat3d`: Z op, ingen
akse spejlet, enhedsskala 1, så fremviseren ikke behøver nogen kolonnekortlægning. Indlæs
tabellen i Heatmap-fanen; se fremviserens
[Hent data ind](https://holdi601.github.io/3DHeat/getting-data-in.html)
og [Kolonnekortlægning](https://holdi601.github.io/3DHeat/column-mapping.html).
