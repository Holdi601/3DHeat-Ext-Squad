---
title: "Tabela"
nav_order: 4
lang: bs
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tabela: `<demo>.parquet` {#the-table-parquet}

Jedan red po uzorku ili događaju. Uzorak se uzima kad god je server replicirao
kretanje aktera, do 8 puta u sekundi (frekvencija snimanja demoa)
dok se kreće.

![Prvi redovi tabele sintetičkog demoa](../assets/img/table.svg)

## Kolone {#columns}

| Kolona | Šta je to |
|---|---|
| `time` | sekunde od početka snimanja |
| `x`, `y`, `z` | pozicija u Unreal jedinicama (centimetri), Z je gore |
| `dirX`, `dirY`, `dirZ` | kamo vojnik gleda: skretanje tijela (yaw) i nagib pogleda (pitch), kao jedinični vektor (kod vozila: vodoravno) |
| `yaw`, `pitch` | isto u stepenima; `pitch` gore od horizonta, samo za vojnike |
| `health` | zdravlje vojnika, bota ili vozila u tom trenutku, gdje ga je server poslao (kod vojnika pada ispod 0 dok je ranjen) |
| `speed` | replicirana brzina, cm/s |
| `player` | ime igrača; `bot <id>` za bota; za vozilo ili postavljivi objekat koji nikome ne pripada, njegova klasa; za hitac iz oružja vozila, igrač koji sjedi u tom vozilu |
| `team`, `faction` | Squadov broj tima (1, 2) i postavka njegove frakcije, **u tom trenutku**: igrači mogu promijeniti stranu |
| `squad` | broj odreda, -1 kad nije ni u jednom |
| `event` | šta je red (dolje) |
| `pawn` | nacrt vojnika (`SQSquidBot` za bota), vozilo, ili za `fire` oružje |
| `seat` | za kupolu ili putničko sjedalo, pawn samog sjedala |
| `detail` | za `fire` poziv oružja koji je postavio hitac, za `hit` vrsta štete, za `removed` zašto se kanal zatvorio (`Destroyed`, `Dormancy`...) |
| `entity` | akter na koji se red odnosi (njegov net GUID): `entity` redova pomoćnih datoteka |
| `match` | ime demoa |

## Događaji {#events}

| `event` | U redu za | Šta |
|---|---|---|
| `position` | vojnika ili bota pješice | uzorak kretanja |
| `vehicle` | vojnika u kopnenom vozilu ili helikopteru | uzorak na poziciji vozila |
| `wounded`, `revived`, `death` | vojnike i botove | gdje se dogodilo |
| `spawn`, `damaged`, `destroyed`, `removed` | vozila, postavljive objekte, utvrđene položaje, sanduke, helikoptere | gdje su bili |
| `seat` | igrača | zauzeo sjedalo |
| `fire` | strijelca | hitac: odakle je izašao, njegov smjer kao `yaw`/`pitch`/`dirX..Z` |
| `hit` | vozilo | pogodak u vozilo: gdje |

Kako se događaji čitaju, piše u [Kako se demo čita](how-it-works.md#how-the-events-are-read).

## U pregledniku {#in-the-viewer}

Podnožje Parqueta nosi upute za čitanje pod ključem `heat3d`: Z je gore,
nijedna os nije zrcaljena, jedinična skala 1, pa preglednik ne treba mapiranje
kolona. Učitaj tabelu u kartici Toplotna mapa; vidi
[Unos podataka](https://holdi601.github.io/3DHeat/getting-data-in.html)
i [Mapiranje kolona](https://holdi601.github.io/3DHeat/column-mapping.html) u pregledniku.
