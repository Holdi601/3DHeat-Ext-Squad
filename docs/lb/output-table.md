---
title: "D'Tabell"
nav_order: 4
lang: "lb"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# D'Tabell: `<demo>.parquet` {#the-table-parquet}

Eng Zeil pro Echantillon oder Evenement. Een Echantillon gëtt geholl, wann de Server
d'Beweegung vum Akteur replizéiert huet, bis zu 8 Mol d'Sekonn (d'Opnamerate vun der Demo),
während en sech beweegt.

![Déi éischt Zeile vun der Tabell vun enger syntheteschen Demo](../assets/img/table.svg)

## Kolonnen {#columns}

| Kolonn | Wat et ass |
|---|---|
| `time` | Sekonnen, zënter d'Opnam ugefaangen huet |
| `x`, `y`, `z` | Positioun an Unreal-Eenheeten (Zentimeter), Z no uewen |
| `dirX`, `dirY`, `dirZ` | wouhin e Zaldot kuckt: de Yaw vum Kierper an de Pitch vum Bléck, als Eenheetsvektor (bei engem Gefier: horizontal) |
| `yaw`, `pitch` | datselwecht a Grad; `pitch` no uewen vum Horizont, nëmmen bei Zaldoten |
| `health` | d'Gesondheet vum Zaldot, Bot oder Gefier an deem Moment, wou de Server se geschéckt huet (bei engem Zaldot fällt se ënner 0, während en verwonnt ass) |
| `speed` | déi replizéiert Geschwindegkeet, cm/s |
| `player` | den Numm vum Spiller; `bot <id>` fir e Bot; bei engem Gefier oder Deployable, dat kengem gehéiert, seng Klass; bei engem Schoss vun der Waff vun engem Gefier de Spiller, deen op deem Gefier sëtzt |
| `team`, `faction` | Squads Teamnummer (1, 2) a seng Fraktiounsopstellung, **an deem Moment**: Spiller kënnen d'Säit wiesselen |
| `squad` | d'Squad-Nummer, -1 wann net an engem |
| `event` | wat d'Zeil ass (ënnen) |
| `pawn` | de Blueprint vum Zaldot (`SQSquidBot` fir e Bot), d'Gefier, oder bei `fire` d'Waff |
| `seat` | bei engem Tuerm oder Passagéierplaz de Pawn vun der Plaz selwer |
| `detail` | bei `fire` den Opruff vun der Waff, deen de Schoss gesat huet, bei `hit` den Schuedenstyp, bei `removed` firwat de Kanal zougaangen ass (`Destroyed`, `Dormancy`...) |
| `entity` | den Akteur, ëm deen et an der Zeil geet (säin Net GUID): den `entity` vun de Zeilen an de Niewendateien |
| `match` | den Numm vun der Demo |

## Evenementer {#events}

| `event` | An der Zeil vun | Wat |
|---|---|---|
| `position` | engem Zaldot oder Bot zu Fouss | en Beweegungs-Echantillon |
| `vehicle` | engem Zaldot an engem Buedemgefier oder Helikopter | en Echantillon op der Positioun vum Gefier |
| `wounded`, `revived`, `death` | Zaldoten a Boten | wou et geschitt ass |
| `spawn`, `damaged`, `destroyed`, `removed` | Gefierer, Deployables, Emplacementer, Këschten, Helikopteren | wou se waren |
| `seat` | engem Spiller | huet sech higesat |
| `fire` | dem Schéisser | e Schoss: wou e fortgaangen ass, seng Richtung als `yaw`/`pitch`/`dirX..Z` |
| `hit` | dem Gefier | en Treffer um Gefier: wou |

Wéi d'Evenementer gelies ginn, steet an [Wéi eng Demo gelies gëtt](how-it-works.md#how-the-events-are-read).

## Am Viewer {#in-the-viewer}

De Parquet-Footer huet Liesinstruktiounen ënnert dem Schlëssel `heat3d`: Z no uewen,
keng Achs gespigelt, Eenheetsskala 1, sou brauch de Viewer keng Kolonn-Zuordnung. Lued
d'Tabell am Heatmap-Tab; kuckt dem Viewer säin
[Daten eran kréien](https://holdi601.github.io/3DHeat/getting-data-in.html)
an [Kolonn-Zuordnung](https://holdi601.github.io/3DHeat/column-mapping.html).
