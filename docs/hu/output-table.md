---
title: "A táblázat"
nav_order: 4
lang: "hu"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# A táblázat: `<demo>.parquet` {#the-table-parquet}

Soronként egy minta vagy esemény. Mintát akkor vesz a rendszer, amikor a szerver replikálta
az aktor mozgását, másodpercenként legfeljebb 8-szor (a demó rögzítési sebessége), amíg mozog.

![Egy szintetikus demó táblázatának első sorai](../assets/img/table.svg)

## Oszlopok {#columns}

| Oszlop | Mit jelent |
|---|---|
| `time` | másodpercek a felvétel kezdete óta |
| `x`, `y`, `z` | pozíció Unreal-egységekben (centiméterben), a Z felfelé mutat |
| `dirX`, `dirY`, `dirZ` | merre néz a katona: a test yaw-ja és a nézés pitch-e egységvektorként (járműé: vízszintes) |
| `yaw`, `pitch` | ugyanez fokban; a `pitch` a horizonttól felfelé, csak katonáknál |
| `health` | a katona, bot vagy jármű életereje abban a pillanatban, ahol a szerver elküldte (a katonáé 0 alá eshet, miközben sebesült) |
| `speed` | a replikált sebesség, cm/s |
| `player` | a játékos neve; botnál `bot <id>`; olyan járműnél vagy telepíthető eszköznél, amelynek nincs tulajdonosa, az osztálya; a jármű fegyveréből leadott lövésnél az a játékos, aki azon a járművön ül |
| `team`, `faction` | a Squad csapatszáma (1, 2) és frakcióbeállítása, **abban a pillanatban**: a játékosok oldalt válthatnak |
| `squad` | a rajszám, -1, ha nincs rajban |
| `event` | mi a sor (lent) |
| `pawn` | a katonablueprint (botnál `SQSquidBot`), a jármű, vagy `fire` esetén a fegyver |
| `seat` | fegyvertorony- vagy utasülésnél az ülés saját figurája |
| `detail` | `fire`-nél a lövést elhelyező fegyverhívás, `hit`-nél a sérülés típusa, `removed`-nál, miért zárult le a csatorna (`Destroyed`, `Dormancy`...) |
| `entity` | az aktor, amelyről a sor szól (a hálózati GUID-ja): a kísérőfájlok sorainak `entity` oszlopa |
| `match` | a demó neve |

## Események {#events}

| `event` | Melyik során | Mi |
|---|---|---|
| `position` | gyalogos katona vagy bot | egy mozgásminta |
| `vehicle` | szárazföldi járműben vagy helikopterben ülő katona | minta a jármű helyén |
| `wounded`, `revived`, `death` | katonák és botok | hol történt |
| `spawn`, `damaged`, `destroyed`, `removed` | járművek, telepíthető eszközök, fegyverállások, ládák, helikopterek | hol voltak |
| `seat` | játékos | elfoglalt egy ülést |
| `fire` | a lövő | egy lövés: honnan indult, iránya `yaw`/`pitch`/`dirX..Z` formában |
| `hit` | a jármű | egy találat a járművön: hol |

Hogyan olvasódnak be az események: [Hogyan olvasódik be a demó](how-it-works.md#how-the-events-are-read).

## A megjelenítőben {#in-the-viewer}

A Parquet lábléce a `heat3d` kulcs alatt olvasási utasításokat tartalmaz: Z felfelé, egyik tengely
sincs tükrözve, egységskála 1, így a megjelenítőnek nincs szüksége oszlop-hozzárendelésre. Töltsd be a
táblázatot a Hőtérkép fülön; lásd a megjelenítő
[Adatok betöltése](https://holdi601.github.io/3DHeat/getting-data-in.html) és
[Oszlop-hozzárendelés](https://holdi601.github.io/3DHeat/column-mapping.html) oldalait.
