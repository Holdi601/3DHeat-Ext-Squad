---
title: "Tabuľka"
nav_order: 4
lang: sk
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabuľka: `<demo>.parquet` {#the-table-parquet}

Jeden riadok na každú vzorku alebo udalosť. Vzorka sa odoberie vždy, keď server replikoval
pohyb aktéra, až 8-krát za sekundu (rýchlosť nahrávania dema), kým sa aktér hýbe.

![Prvé riadky tabuľky syntetického dema](../assets/img/table.svg)

## Stĺpce {#columns}

| Stĺpec | Čo to je |
|---|---|
| `time` | sekundy od začiatku nahrávania |
| `x`, `y`, `z` | poloha v jednotkách Unreal (centimetroch), Z smeruje hore |
| `dirX`, `dirY`, `dirZ` | kam sa vojak pozerá: uhol natočenia tela a uhol pohľadu ako jednotkový vektor (vozidlo: vodorovne) |
| `yaw`, `pitch` | to isté v stupňoch; `pitch` nahor od horizontu, len vojaci |
| `health` | zdravie vojaka, bota alebo vozidla v tom momente, keď ho server poslal (zdravie vojaka klesne pod 0, keď je ranený) |
| `speed` | replikovaná rýchlosť, cm/s |
| `player` | meno hráča; `bot <id>` pre bota; pre vozidlo alebo rozmiestnený prvok, ktorý nikomu nepatrí, jeho trieda; pre výstrel z zbrane vozidla hráč sediaci na tomto vozidle |
| `team`, `faction` | číslo tímu Squad (1, 2) a jeho nastavenie frakcie, **v tom momente**: hráči môžu zmeniť strany |
| `squad` | číslo družstva, -1 keď nie je v družstve |
| `event` | čo riadok predstavuje (nižšie) |
| `pawn` | plán vojaka (`SQSquidBot` pre bota), vozidlo, alebo pre `fire` zbraň |
| `seat` | pri veži alebo sedadle pasažiera pešiak samotného sedadla |
| `detail` | pri `fire` volanie zbrane, ktoré výstrel vytvorilo; pri `hit` typ poškodenia; pri `removed` dôvod zatvorenia kanála (`Destroyed`, `Dormancy`...) |
| `entity` | aktér, ktorého sa riadok týka (jeho sieťové GUID): `entity` riadkov sprievodných súborov |
| `match` | názov dema |

## Udalosti {#events}

| `event` | Na riadku | Čo |
|---|---|---|
| `position` | vojak alebo bot pešo | vzorka pohybu |
| `vehicle` | vojak v pozemnom vozidle alebo helikoptére | vzorka na polohe vozidla |
| `wounded`, `revived`, `death` | vojaci a boti | kde sa to stalo |
| `spawn`, `damaged`, `destroyed`, `removed` | vozidlá, rozmiestnené prvky, stanovištia, muničné bedne, helikoptéry | kde boli |
| `seat` | hráč | sadol si na sedadlo |
| `fire` | strelec | výstrel: odkiaľ odletel, jeho smer ako `yaw`/`pitch`/`dirX..Z` |
| `hit` | vozidlo | zásah vozidla: kde |

Ako sa udalosti čítajú, je na stránke [Ako sa demo číta](how-it-works.md#how-the-events-are-read).

## V prehliadači {#in-the-viewer}

Pätička Parquet nesie čitateľské pokyny pod kľúčom `heat3d`: Z hore,
žiadna os zrkadlená, mierka jednotky 1, takže prehliadač nepotrebuje mapovanie stĺpcov. Načítajte
tabuľku na karte Heatmapa; pozri [Načítanie dát](https://holdi601.github.io/3DHeat/getting-data-in.html)
a [Mapovanie stĺpcov](https://holdi601.github.io/3DHeat/column-mapping.html) v dokumentácii prehliadača.
