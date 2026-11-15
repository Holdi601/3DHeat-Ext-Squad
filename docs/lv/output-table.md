---
title: Tabula
nav_order: 4
lang: lv
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabula: `<demo>.parquet` {#the-table-parquet}

Viena rinda katram paraugam vai notikumam. Paraugs tiek ņemts ikreiz, kad serveris replicēja
aktora kustību, līdz 8 reizēm sekundē (demo ierakstīšanas ātrums), kamēr tas kustas.

![Sintētiska demo tabulas pirmās rindas](../assets/img/table.svg)

## Kolonnas {#columns}

| Kolonna | Ko tā ir |
|---|---|
| `time` | sekundes kopš ieraksta sākuma |
| `x`, `y`, `z` | pozīcija Unreal vienībās (centimetros), Z uz augšu |
| `dirX`, `dirY`, `dirZ` | kur karavīrs skatās: ķermeņa virziens un skata augstums kā vienības vektors (transportlīdzekļa: līmenī) |
| `yaw`, `pitch` | tas pats grādos; `pitch` uz augšu no horizonta, tikai karavīriem |
| `health` | karavīra, bota vai transportlīdzekļa veselība tajā brīdī, kur serveris to nosūtīja (karavīra veselība nokrīt zem 0, kamēr ir ievainots) |
| `speed` | replicētais ātrums, cm/s |
| `player` | spēlētāja vārds; `bot <id>` botam; transportlīdzeklim vai deployable, kuram neviens nepieder, tā klase; šāvienam no transportlīdzekļa ieroča - spēlētājs, kas sēž šajā transportlīdzeklī |
| `team`, `faction` | Squad komandas numurs (1, 2) un tās frakcijas uzstādījums **tajā brīdī**: spēlētāji var mainīt pusi |
| `squad` | squad numurs, -1, ja nav squad |
| `event` | kas ir rinda (zemāk) |
| `pawn` | karavīra blueprint (`SQSquidBot` botam), transportlīdzeklis vai `fire` gadījumā ierocis |
| `seat` | torņa vai pasažiera sēdeklim - paša sēdekļa pawn |
| `detail` | `fire` gadījumā ieroča izsaukums, kas ielika šāvienu; `hit` gadījumā bojājuma tips; `removed` gadījumā iemesls, kādēļ kanāls aizvērās (`Destroyed`, `Dormancy`...) |
| `entity` | aktors, par ko ir rinda (tā tīkla GUID): papildfailu rindu `entity` |
| `match` | demo nosaukums |

## Notikumi {#events}

| `event` | Rindas, kurā tas ir | Ko nozīmē |
|---|---|---|
| `position` | karavīrs vai bots kājām | kustības paraugs |
| `vehicle` | karavīrs sauszemes transportlīdzeklī vai helikopterā | paraugs transportlīdzekļa pozīcijā |
| `wounded`, `revived`, `death` | karavīri un boti | kur tas notika |
| `spawn`, `damaged`, `destroyed`, `removed` | transportlīdzekļi, deployables, ierīkojumi, kastes, helikopteri | kur tie bija |
| `seat` | spēlētājs | ieņēma sēdekli |
| `fire` | šāvējs | šāviens: kur tas izlidoja, tā virziens kā `yaw`/`pitch`/`dirX..Z` |
| `hit` | transportlīdzeklis | transportlīdzekļa trāpījums: kur |

Kā notikumi tiek nolasīti, ir aprakstīts [Kā tiek nolasīts demo](how-it-works.md#how-the-events-are-read).

## Skatītājā {#in-the-viewer}

Parquet kājene satur lasīšanas norādes zem atslēgas `heat3d`: Z uz augšu, neviena ass nav
apgriezta, vienību mērogs 1, tāpēc skatītājam nav vajadzīga kolonnu kartēšana. Ielādējiet
tabulu cilnē Siltumkarte; skat. skatītāja
[Datu ievade](https://holdi601.github.io/3DHeat/getting-data-in.html)
un [Kolonnu kartēšana](https://holdi601.github.io/3DHeat/column-mapping.html).
