---
title: "Tabelul"
nav_order: 4
lang: "ro"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabelul: `<demo>.parquet` {#the-table-parquet}

Câte un rând pentru fiecare mostră sau eveniment. O mostră se ia ori de câte ori serverul a replicat
mișcarea actorului, de până la 8 ori pe secundă (ritmul de înregistrare al demo-ului)
cât timp el se mișcă.

![Primele rânduri din tabelul unui demo sintetic](../assets/img/table.svg)

## Coloane {#columns}

| Coloană | Ce este |
|---|---|
| `time` | secunde de la începutul înregistrării |
| `x`, `y`, `z` | poziția în unități Unreal (centimetri), Z în sus |
| `dirX`, `dirY`, `dirZ` | unde se uită un soldat: girația corpului și unghiul vertical al privirii, ca vector unitar (la un vehicul: orizontal) |
| `yaw`, `pitch` | același lucru în grade; `pitch` în sus față de orizont, doar pentru soldați |
| `health` | sănătatea soldatului, a botului sau a vehiculului în acel moment, acolo unde a trimis-o serverul (sănătatea unui soldat scade sub 0 când este rănit) |
| `speed` | viteza replicată, cm/s |
| `player` | numele jucătorului; `bot <id>` pentru un bot; pentru un vehicul sau un dispozitiv desfășurabil fără proprietar, clasa lui; pentru un foc dintr-o armă a unui vehicul, jucătorul așezat pe acel vehicul |
| `team`, `faction` | numărul echipei Squad (1, 2) și configurația sa de fracțiune, **în acel moment**: jucătorii pot schimba taberele |
| `squad` | numărul scuadronului, -1 când nu face parte dintr-unul |
| `event` | ce reprezintă rândul (mai jos) |
| `pawn` | planul de bază al soldatului (`SQSquidBot` pentru un bot), vehiculul, sau, pentru `fire`, arma |
| `seat` | pentru un loc de turelă sau de pasager, pionul locului însuși |
| `detail` | pentru `fire`, apelul armei care a plasat focul; pentru `hit`, tipul de daună; pentru `removed`, motivul închiderii canalului (`Destroyed`, `Dormancy`...) |
| `entity` | actorul la care se referă rândul (net GUID-ul său): `entity` din rândurile fișierelor auxiliare |
| `match` | numele demo-ului |

## Evenimente {#events}

| `event` | Pe rândul | Ce este |
|---|---|---|
| `position` | un soldat sau un bot pe jos | o mostră de mișcare |
| `vehicle` | un soldat dintr-un vehicul terestru sau dintr-un elicopter | o mostră la poziția vehiculului |
| `wounded`, `revived`, `death` | soldați și boți | unde s-a întâmplat |
| `spawn`, `damaged`, `destroyed`, `removed` | vehicule, dispozitive desfășurabile, puncte de tragere, cutii, elicoptere | unde se aflau |
| `seat` | un jucător | a ocupat un loc |
| `fire` | trăgătorul | un foc: de unde a plecat, direcția sa ca `yaw`/`pitch`/`dirX..Z` |
| `hit` | vehiculul | o lovitură asupra vehiculului: unde |

Cum se citesc evenimentele este în [Cum se citește un demo](how-it-works.md#how-the-events-are-read).

## În vizualizator {#in-the-viewer}

Subsolul fișierului Parquet poartă instrucțiuni de citire sub cheia `heat3d`: Z în sus,
nicio axă oglindită, scară unitară 1, așa că vizualizatorul nu are nevoie de nicio mapare a coloanelor. Încărcați
tabelul în fila Hartă termică; vedeți [Introducerea datelor](https://holdi601.github.io/3DHeat/getting-data-in.html)
și [Maparea coloanelor](https://holdi601.github.io/3DHeat/column-mapping.html) din documentația vizualizatorului.
