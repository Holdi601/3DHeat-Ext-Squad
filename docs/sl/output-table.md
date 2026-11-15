---
title: "Tabela"
nav_order: 4
lang: "sl"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabela: `<posnetek>.parquet` {#the-table-parquet}

Ena vrstica na vzorec ali dogodek. Vzorec se vzame vsakič, ko strežnik posreduje
premik akterja, do 8-krat na sekundo (hitrost snemanja posnetka), medtem ko se
akter premika.

![Prve vrstice tabele sintetičnega posnetka](../assets/img/table.svg)

## Stolpci {#columns}

| Stolpec | Kaj je |
|---|---|
| `time` | sekunde od začetka snemanja |
| `x`, `y`, `z` | položaj v enotah Unreal (centimetri), Z navzgor |
| `dirX`, `dirY`, `dirZ` | kam vojak gleda: zasuk telesa (yaw) in nagib pogleda kot enotski vektor (pri vozilu: vodoravno) |
| `yaw`, `pitch` | isto v stopinjah; `pitch` je navzgor od obzorja, samo za vojake |
| `health` | zdravje vojaka, bota ali vozila v tistem trenutku, kjer ga je strežnik poslal (zdravje vojaka pade pod 0, ko je ranjen) |
| `speed` | posredovana hitrost, cm/s |
| `player` | ime igralca; `bot <id>` za bota; za vozilo ali postavljiv objekt, ki ga nihče ne poseduje, njegov razred; za strel iz orožja vozila igralec, ki sedi na tem vozilu |
| `team`, `faction` | številka ekipe v Squadu (1, 2) in njena postavitev frakcije, **v tistem trenutku**: igralci lahko menjajo strani |
| `squad` | številka skupine, -1, če ni v skupini |
| `event` | kaj vrstica pomeni (spodaj) |
| `pawn` | pawn vojaka (`SQSquidBot` za bota), vozilo, pri `fire` pa orožje |
| `seat` | pri sedežu v stolpu ali sopotniškem sedežu sam pawn sedeža |
| `detail` | pri `fire` klic orožja, ki je določil strel, pri `hit` vrsta poškodbe, pri `removed` razlog zaprtja kanala (`Destroyed`, `Dormancy`...) |
| `entity` | akter, na katerega se vrstica nanaša (njegov mrežni GUID): `entity` vrstic spremljevalnih datotek |
| `match` | ime posnetka |

## Dogodki {#events}

| `event` | Na vrstici | Kaj |
|---|---|---|
| `position` | vojak ali bot peš | vzorec premika |
| `vehicle` | vojak v kopenskem vozilu ali helikopterju | vzorec na položaju vozila |
| `wounded`, `revived`, `death` | vojaki in boti | kje se je zgodilo |
| `spawn`, `damaged`, `destroyed`, `removed` | vozila, postavljivi objekti, strelni položaji, zaboji, helikopterji | kje so bili |
| `seat` | igralec | je sedel na sedež |
| `fire` | strelec | strel: kje je odletel, njegova smer kot `yaw`/`pitch`/`dirX..Z` |
| `hit` | vozilo | zadetek v vozilo: kje |

Kako se dogodki preberejo, je v [Kako se posnetek bere](how-it-works.md#how-the-events-are-read).

## V pregledovalniku {#in-the-viewer}

Noga datoteke Parquet nosi navodila za branje pod ključem `heat3d`: Z navzgor,
nobena os ni zrcaljena, merilo enote 1, zato pregledovalnik ne potrebuje
preslikave stolpcev. Tabelo naloži na zavihku Toplotni zemljevid; glej
[Vnos podatkov](https://holdi601.github.io/3DHeat/getting-data-in.html) in
[Preslikava stolpcev](https://holdi601.github.io/3DHeat/column-mapping.html).
