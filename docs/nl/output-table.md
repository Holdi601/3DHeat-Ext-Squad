---
title: De tabel
nav_order: 4
lang: "nl"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# De tabel: `<demo>.parquet` {#the-table-parquet}

Eén rij per monster of gebeurtenis. Er wordt een monster genomen wanneer de server de
bewegingen van de actor heeft gerepliceerd, tot 8 keer per seconde (de opnamesnelheid van de demo)
terwijl hij beweegt.

![De eerste rijen van de tabel van een synthetische demo](../assets/img/table.svg)

## Kolommen {#columns}

| Kolom | Wat het is |
|---|---|
| `time` | seconden sinds het begin van de opname |
| `x`, `y`, `z` | positie in Unreal-eenheden (centimeters), Z omhoog |
| `dirX`, `dirY`, `dirZ` | waar een soldaat naar kijkt: de gier van het lichaam en de helling van het zicht, als eenheidsvector (bij een voertuig: vlak) |
| `yaw`, `pitch` | hetzelfde in graden; `pitch` omhoog vanaf de horizon, alleen soldaten |
| `health` | de gezondheid van de soldaat, bot of het voertuig op dat moment, waar de server die stuurde (die van een soldaat zakt onder 0 terwijl hij gewond is) |
| `speed` | de gerepliceerde snelheid, cm/s |
| `player` | de naam van de speler; `bot <id>` voor een bot; voor een voertuig of opstelling die niemand bezit, de klasse ervan; voor een schot uit het wapen van een voertuig, de speler die in dat voertuig zit |
| `team`, `faction` | Squads teamnummer (1, 2) en zijn factie-indeling, **op dat moment**: spelers kunnen van kant wisselen |
| `squad` | het squadnummer, -1 wanneer hij in geen squad zit |
| `event` | wat de rij is (hieronder) |
| `pawn` | de soldaatblueprint (`SQSquidBot` voor een bot), het voertuig, of bij `fire` het wapen |
| `seat` | bij een torenstoel of passagiersstoel, de eigen pawn van die stoel |
| `detail` | bij `fire` de wapenaanroep die het schot plaatste, bij `hit` het schadetype, bij `removed` waarom het kanaal sloot (`Destroyed`, `Dormancy`...) |
| `entity` | de actor waar de rij over gaat (zijn net-GUID): de `entity` van de rijen in de bijbestanden |
| `match` | de naam van de demo |

## Gebeurtenissen {#events}

| `event` | Op de rij van | Wat |
|---|---|---|
| `position` | een soldaat of bot te voet | een bewegingsmonster |
| `vehicle` | een soldaat in een grondvoertuig of helikopter | een monster op de positie van het voertuig |
| `wounded`, `revived`, `death` | soldaten en bots | waar het gebeurde |
| `spawn`, `damaged`, `destroyed`, `removed` | voertuigen, opstellingen, stellingen, kratten, helikopters | waar ze waren |
| `seat` | een speler | nam een stoel in |
| `fire` | de schutter | een schot: waar het vertrok, zijn richting als `yaw`/`pitch`/`dirX..Z` |
| `hit` | het voertuig | een treffer op een voertuig: waar |

Hoe de gebeurtenissen worden gelezen, staat in [Hoe een demo wordt gelezen](how-it-works.md#how-the-events-are-read).

## In de viewer {#in-the-viewer}

De footer van het Parquet-bestand bevat leesinstructies onder de sleutel `heat3d`: Z omhoog,
geen as gespiegeld, eenheidsschaal 1, zodat de viewer geen kolommen hoeft te koppelen. Laad
de tabel in het tabblad Heatmap; zie [Gegevens binnenhalen](https://holdi601.github.io/3DHeat/getting-data-in.html)
en [Kolomkoppeling](https://holdi601.github.io/3DHeat/column-mapping.html) in de viewer-documentatie.
