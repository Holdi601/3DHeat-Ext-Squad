---
title: "Lentelė"
nav_order: 4
lang: lt
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Lentelė: `<demo>.parquet` {#the-table-parquet}

Viena eilutė vienam matavimui ar įvykiui. Matavimas imamas kiekvieną kartą, kai serveris replikavo veikėjo judėjimą,
iki 8 kartų per sekundę (demo įrašymo dažnis), kol jis juda.

![Pirmosios sintetinio demo lentelės eilutės](../assets/img/table.svg)

## Stulpeliai {#columns}

| Stulpelis | Ką jis reiškia |
|---|---|
| `time` | sekundės nuo įrašo pradžios |
| `x`, `y`, `z` | pozicija Unreal vienetais (centimetrais), Z aukštyn |
| `dirX`, `dirY`, `dirZ` | kur žiūri kareivis: kūno posūkis ir žvilgsnio kampas kaip vienetinis vektorius (transporto priemonės: lygiai) |
| `yaw`, `pitch` | tas pats laipsniais; `pitch` – aukštyn nuo horizonto, tik kareiviams |
| `health` | kareivio, boto ar transporto priemonės sveikata tuo metu, kai serveris ją išsiuntė (kareivio sveikata nukrenta žemiau 0, kai jis sužeistas) |
| `speed` | replikuotas greitis, cm/s |
| `player` | žaidėjo vardas; `bot <id>` botui; transporto priemonei ar įrenginiui, kurio niekas neturi – jo klasė; šūviui iš transporto priemonės ginklo – žaidėjas, sėdintis toje transporto priemonėje |
| `team`, `faction` | Squad komandos numeris (1, 2) ir jos frakcijos sąranka, **tuo metu**: žaidėjai gali pakeisti puses |
| `squad` | būrio numeris, -1, kai nėra būryje |
| `event` | kas yra eilutė (žemiau) |
| `pawn` | kareivio blueprint (`SQSquidBot` botui), transporto priemonė, o `fire` atveju – ginklas |
| `seat` | bokštelio ar keleivio sėdynei – pačios sėdynės pawn |
| `detail` | `fire` atveju – ginklo kvietimas, kuris užfiksavo šūvį; `hit` atveju – žalos tipas; `removed` atveju – kodėl kanalas uždarytas (`Destroyed`, `Dormancy`...) |
| `entity` | veikėjas, apie kurį eilutė (jo tinklo GUID): papildomų failų eilučių `entity` |
| `match` | demo pavadinimas |

## Įvykiai {#events}

| `event` | Eilutės, kurioje yra | Kas tai |
|---|---|---|
| `position` | kareivis ar botas pėsčiomis | judėjimo matavimas |
| `vehicle` | kareivis sausumos transporto priemonėje ar sraigtasparnyje | matavimas transporto priemonės pozicijoje |
| `wounded`, `revived`, `death` | kareiviai ir botai | kur tai įvyko |
| `spawn`, `damaged`, `destroyed`, `removed` | transporto priemonės, įrenginiai, įtvirtinimai, dėžės, sraigtasparniai | kur jie buvo |
| `seat` | žaidėjas | užėmė sėdynę |
| `fire` | šaulys | šūvis: iš kur išskrido, kryptis kaip `yaw`/`pitch`/`dirX..Z` |
| `hit` | transporto priemonė | transporto priemonės pataikymas: kur |

Kaip skaitomi įvykiai aprašyta [Kaip skaitomas demo](how-it-works.md#how-the-events-are-read).

## Žiūryklėje {#in-the-viewer}

Parquet poraštė turi skaitymo nurodymus raktu `heat3d`: Z aukštyn, jokia ašis neveidrodinama, vieneto mastelis 1,
todėl žiūryklei nereikia stulpelių susiejimo. Įkelkite lentelę Šilumos žemėlapio skirtuke; žr. žiūryklės
[Duomenų įkėlimas](https://holdi601.github.io/3DHeat/getting-data-in.html)
ir [Stulpelių susiejimas](https://holdi601.github.io/3DHeat/column-mapping.html).
