---
title: "Tabulka"
nav_order: 4
lang: cs
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabulka: `<demo>.parquet` {#the-table-parquet}

Jeden řádek na jeden vzorek nebo událost. Vzorek vznikne, kdykoli server replikoval
pohyb aktéra, až 8krát za sekundu (rychlost nahrávání dema), dokud se aktér hýbe.

![První řádky tabulky syntetického dema](../assets/img/table.svg)

## Sloupce {#columns}

| Sloupec | Co je to |
|---|---|
| `time` | sekundy od začátku nahrávání |
| `x`, `y`, `z` | poloha v jednotkách Unreal (centimetrech), Z nahoru |
| `dirX`, `dirY`, `dirZ` | kam voják míří: natočení těla a sklon pohledu jako jednotkový vektor (u vozidla: vodorovně) |
| `yaw`, `pitch` | totéž ve stupních; `pitch` nahoru od obzoru, jen u vojáků |
| `health` | zdraví vojáka, bota nebo vozidla v daném okamžiku, tam, kde ho server poslal (zdraví vojáka klesá pod 0, je-li zraněn) |
| `speed` | replikovaná rychlost, cm/s |
| `player` | jméno hráče; `bot <id>` pro bota; u vozidla nebo rozmístitelného prvku, který nikdo nevlastní, jeho třída; u výstřelu ze zbraně vozidla hráč sedící na tom vozidle |
| `team`, `faction` | číslo týmu podle Squadu (1, 2) a jeho nastavení frakce, **v daném okamžiku**: hráči mohou přeběhnout na druhou stranu |
| `squad` | číslo oddílu, -1, když není v oddílu |
| `event` | co řádek znamená (níže) |
| `pawn` | blueprint vojáka (`SQSquidBot` pro bota), vozidlo, nebo u `fire` zbraň |
| `seat` | u věžového nebo spolujezdeckého sedadla vlastní pawn sedadla |
| `detail` | u `fire` volání zbraně, které výstřel vyvolalo, u `hit` typ poškození, u `removed` důvod zavření kanálu (`Destroyed`, `Dormancy`...) |
| `entity` | aktér, o kterém řádek je (jeho síťové GUID): `entity` řádků doplňkových dat |
| `match` | jméno dema |

## Události {#events}

| `event` | Na řádku | Co |
|---|---|---|
| `position` | voják nebo bot pěšky | vzorek pohybu |
| `vehicle` | voják v pozemním vozidle nebo vrtulníku | vzorek na poloze vozidla |
| `wounded`, `revived`, `death` | vojáci a boti | kde se to stalo |
| `spawn`, `damaged`, `destroyed`, `removed` | vozidla, rozmístitelné prvky, stanoviště, bedny, vrtulníky | kde byly |
| `seat` | hráč | zaujal sedadlo |
| `fire` | střelec | výstřel: kde opustil zbraň, jeho směr jako `yaw`/`pitch`/`dirX..Z` |
| `hit` | vozidlo | zásah vozidla: kde |

Jak se události čtou, je popsáno v [Jak se demo čte](how-it-works.md#how-the-events-are-read).

## V prohlížeči {#in-the-viewer}

Patička Parquet nese pokyny pro čtení pod klíčem `heat3d`: Z nahoru, žádná osa
zrcadlená, měřítko jednotky 1, takže prohlížeč nepotřebuje mapování sloupců. Tabulku
načtěte na kartě Teplotní mapa; viz [Získání dat](https://holdi601.github.io/3DHeat/getting-data-in.html)
a [Mapování sloupců](https://holdi601.github.io/3DHeat/column-mapping.html) v dokumentaci prohlížeče.
