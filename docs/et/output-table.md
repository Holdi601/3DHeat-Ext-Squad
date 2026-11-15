---
title: "Tabel"
nav_order: 4
lang: et
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabel: `<demo>.parquet` {#the-table-parquet}

Üks rida proovi või sündmuse kohta. Proov võetakse alati, kui server replitseeris
actori liikumise, kuni 8 korda sekundis (demo salvestuskiirus), kui see liigub.

![Sünteetilise demo tabeli esimesed read](../assets/img/table.svg)

## Veerud {#columns}

| Veerg | Mis see on |
|---|---|
| `time` | sekundeid, mis on möödunud salvestuse algusest |
| `x`, `y`, `z` | asukoht Unreali ühikutes (sentimeetrites), Z üles |
| `dirX`, `dirY`, `dirZ` | kuhu sõdur vaatab: keha pöörde ja vaate kallet ühikvektorina (sõiduki oma: tasane) |
| `yaw`, `pitch` | sama kraadides; `pitch` horisondist ülespoole, ainult sõdurid |
| `health` | sõduri, boti või sõiduki tervis sel hetkel, kui server selle saatis (sõduri oma langeb alla 0, kui ta on haavatud) |
| `speed` | replitseeritud kiirus, cm/s |
| `player` | mängija nimi; `bot <id>` botile; sõidukile või paigaldatavale, mida keegi ei oma, tema klass; lasule sõiduki relvast, selle sõiduki istmel olev mängija |
| `team`, `faction` | Squadi meeskonna number (1, 2) ja tema vormi seadistus, **sel hetkel**: mängijad võivad pooli vahetada |
| `squad` | squadi number, -1, kui ei ole squadis |
| `event` | mis see rida on (allpool) |
| `pawn` | sõduri plaan (`SQSquidBot` botile), sõiduk, või `fire` puhul relv |
| `seat` | pöörlevale või reisijaistmele see istme enda pawn |
| `detail` | `fire` puhul relva käsk, mis lasu paigutas; `hit` puhul kahjutüüp; `removed` puhul põhjus, miks kanal suleti (`Destroyed`, `Dormancy`...) |
| `entity` | actor, millest rida räägib (tema net GUID): lisafailide ridade `entity` |
| `match` | demo nimi |

## Sündmused {#events}

| `event` | Millise rea sündmus | Mis |
|---|---|---|
| `position` | sõdur või bot jalgsi | liikumisproov |
| `vehicle` | sõdur maismaasõidukis või helikopteris | proov sõiduki asukohas |
| `wounded`, `revived`, `death` | sõdurid ja botid | kus see juhtus |
| `spawn`, `damaged`, `destroyed`, `removed` | sõidukid, paigaldatavad, emplacementid, kastid, helikopterid | kus nad olid |
| `seat` | mängija | võttis istme |
| `fire` | lasija | lask: kust see lahkus, selle suund kui `yaw`/`pitch`/`dirX..Z` |
| `hit` | sõiduk | sõiduki tabamus: kus |

Kuidas sündmused loetakse, on kirjas [Kuidas demo loetakse](how-it-works.md#how-the-events-are-read).

## Vaatajas {#in-the-viewer}

Parquet'i jalus kannab lugemisjuhiseid võtme `heat3d` all: Z üles, ühtegi telge ei peegeldata,
ühikumõõt 1, nii et vaataja ei vaja veergude vastendamist. Laadi tabel Soojuskaardi
vahelehel; vt vaataja
[Andmete sisestamine](https://holdi601.github.io/3DHeat/getting-data-in.html)
ja [Veergude vastendamine](https://holdi601.github.io/3DHeat/column-mapping.html).
