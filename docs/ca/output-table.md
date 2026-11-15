---
title: La taula
nav_order: 4
lang: ca
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# La taula: `<demo>.parquet` {#the-table-parquet}

Una fila per mostra o esdeveniment. Es pren una mostra cada vegada que el servidor
replica el moviment de l'actor, fins a 8 vegades per segon (la freqüència de gravació
de la demo) mentre es mou.

![Les primeres files de la taula d'una demo sintètica](../assets/img/table.svg)

## Columnes {#columns}

| Columna | Què és |
|---|---|
| `time` | segons des que va començar la gravació |
| `x`, `y`, `z` | posició en unitats d'Unreal (centímetres), Z cap amunt |
| `dirX`, `dirY`, `dirZ` | cap a on mira un soldat: el guinyament del cos i la inclinació de la vista, com a vector unitari (el d'un vehicle: pla) |
| `yaw`, `pitch` | el mateix en graus; `pitch` és l'angle sobre l'horitzó, només per als soldats |
| `health` | la salut del soldat, del bot o del vehicle en aquell moment, quan el servidor l'ha enviat (la d'un soldat baixa de 0 quan està ferit) |
| `speed` | la velocitat replicada, cm/s |
| `player` | el nom del jugador; `bot <id>` per a un bot; per a un vehicle o element desplegable que no té propietari, la seva classe; per a un tret d'una arma d'un vehicle, el jugador assegut en aquell vehicle |
| `team`, `faction` | el número d'equip de Squad (1, 2) i la seva configuració de facció, **en aquell moment**: els jugadors poden canviar de bàndol |
| `squad` | el número d'esquadró, -1 quan no n'hi ha cap |
| `event` | què és la fila (a continuació) |
| `pawn` | el pla del soldat (`SQSquidBot` per a un bot), el vehicle o, per a `fire`, l'arma |
| `seat` | per a una torreta o un seient de passatger, el peó del mateix seient |
| `detail` | per a `fire`, la crida d'arma que va col·locar el tret; per a `hit`, el tipus de dany; per a `removed`, per què es va tancar el canal (`Destroyed`, `Dormancy`...) |
| `entity` | l'actor a què fa referència la fila (el seu GUID de xarxa): el `entity` de les files dels fitxers auxiliars |
| `match` | el nom de la demo |

## Esdeveniments {#events}

| `event` | A la fila de | Què |
|---|---|---|
| `position` | un soldat o bot a peu | una mostra de moviment |
| `vehicle` | un soldat en un vehicle terrestre o un helicòpter | una mostra a la posició del vehicle |
| `wounded`, `revived`, `death` | soldats i bots | on va passar |
| `spawn`, `damaged`, `destroyed`, `removed` | vehicles, elements desplegables, emplaçaments, caixes, helicòpters | on eren |
| `seat` | un jugador | va ocupar un seient |
| `fire` | el tirador | un tret: on va sortir, la seva direcció com a `yaw`/`pitch`/`dirX..Z` |
| `hit` | el vehicle | un impacte en un vehicle: on |

Com es llegeixen els esdeveniments és a [Com es llegeix una demo](how-it-works.md#how-the-events-are-read).

## Al visualitzador {#in-the-viewer}

El peu del fitxer Parquet porta instruccions de lectura sota la clau `heat3d`: Z cap amunt,
cap eix reflectit, escala d'unitat 1, de manera que el visualitzador no necessita
cap assignació de columnes. Carregui la taula a la pestanya Mapa de calor; vegi
[Introduir dades](https://holdi601.github.io/3DHeat/getting-data-in.html)
i [Assignació de columnes](https://holdi601.github.io/3DHeat/column-mapping.html)
del visualitzador.
