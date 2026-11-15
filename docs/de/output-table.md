---
title: "Die Tabelle"
nav_order: 4
lang: de
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Die Tabelle: `<demo>.parquet` {#the-table-parquet}

Eine Zeile pro Probe oder Ereignis. Eine Probe wird genommen, wann immer der Server die Bewegung des Akteurs
repliziert hat, bis zu 8 Mal pro Sekunde (die Aufnahmerate der Demo), solange er sich bewegt.

![Die ersten Zeilen der Tabelle einer synthetischen Demo](../assets/img/table.svg)

## Spalten {#columns}

| Spalte | Was sie ist |
|---|---|
| `time` | Sekunden seit Beginn der Aufnahme |
| `x`, `y`, `z` | Position in Unreal-Einheiten (Zentimeter), Z nach oben |
| `dirX`, `dirY`, `dirZ` | wohin ein Soldat schaut: der Gierwinkel des Körpers und der Neigungswinkel der Sicht, als Einheitsvektor (bei einem Fahrzeug: waagerecht) |
| `yaw`, `pitch` | dasselbe in Grad; `pitch` nach oben vom Horizont, nur Soldaten |
| `health` | die Gesundheit des Soldaten, Bots oder Fahrzeugs in diesem Moment, wo der Server sie gesendet hat (die des Soldaten fällt unter 0, während er verwundet ist) |
| `speed` | die replizierte Geschwindigkeit, cm/s |
| `player` | der Name des Spielers; `bot <id>` für einen Bot; für ein Fahrzeug oder einen Verbrauchsgegenstand, der niemandem gehört, seine Klasse; für einen Schuss aus der Waffe eines Fahrzeugs der Spieler, der in diesem Fahrzeug sitzt |
| `team`, `faction` | Die Teamnummer (1, 2) von Squad und ihre Fraktionszuordnung, **in diesem Moment**: Spieler können die Seite wechseln |
| `squad` | die Squad-Nummer, -1, wenn er in keiner Squad ist |
| `event` | was die Zeile ist (unten) |
| `pawn` | das Soldaten-Blueprint (`SQSquidBot` für einen Bot), das Fahrzeug, oder für `fire` die Waffe |
| `seat` | bei einem Geschütz- oder Passagiersitz die eigene Figur des Sitzes |
| `detail` | bei `fire` der Aufruf der Waffe, der den Schuss auslöste; bei `hit` der Schadenstyp; bei `removed`, warum der Kanal geschlossen wurde (`Destroyed`, `Dormancy`...) |
| `entity` | der Akteur, um den es in der Zeile geht (seine Net-GUID): das `entity` der Zeilen in den Begleitdateien |
| `match` | der Name der Demo |

## Ereignisse {#events}

| `event` | Auf der Zeile von | Was |
|---|---|---|
| `position` | einem Soldaten oder Bot zu Fuß | eine Bewegungsprobe |
| `vehicle` | einem Soldaten in einem Bodenfahrzeug oder Helikopter | eine Probe an der Position des Fahrzeugs |
| `wounded`, `revived`, `death` | Soldaten und Bots | wo es geschah |
| `spawn`, `damaged`, `destroyed`, `removed` | Fahrzeuge, Verbrauchsgegenstände, Geschütze, Kisten, Helikopter | wo sie waren |
| `seat` | einem Spieler | hat einen Sitz eingenommen |
| `fire` | dem Schützen | ein Schuss: wo er abging, seine Richtung als `yaw`/`pitch`/`dirX..Z` |
| `hit` | dem Fahrzeug | ein Fahrzeugtreffer: wo |

Wie die Ereignisse gelesen werden, steht in [Wie eine Demo gelesen wird](how-it-works.md#how-the-events-are-read).

## Im Viewer {#in-the-viewer}

Der Parquet-Footer trägt Leseanweisungen unter dem Schlüssel `heat3d`: Z nach oben, keine Achse gespiegelt, Maßstab 1,
sodass der Viewer keine Spaltenzuordnung braucht. Lade die Tabelle im Heatmap-Reiter; siehe die Seiten des Viewers
[Daten hineinbringen](https://holdi601.github.io/3DHeat/getting-data-in.html)
und [Spaltenzuordnung](https://holdi601.github.io/3DHeat/column-mapping.html).
