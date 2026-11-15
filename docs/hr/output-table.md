---
title: Tablica
nav_order: 4
lang: "hr"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tablica: `<demo>.parquet` {#the-table-parquet}

Jedan redak po uzorku ili događaju. Uzorak se uzima kad god server replicira
kretanje aktora, do 8 puta u sekundi (brzina snimanja dema), dok se on kreće.

![Prvi reci tablice sintetičkog dema](../assets/img/table.svg)

## Stupci {#columns}

| Stupac | Što je |
|---|---|
| `time` | sekunde od početka snimanja |
| `x`, `y`, `z` | položaj u Unreal jedinicama (centimetri), Z gore |
| `dirX`, `dirY`, `dirZ` | kamo vojnik gleda: skretanje tijela i nagib pogleda, kao jedinični vektor (kod vozila: vodoravno) |
| `yaw`, `pitch` | isto u stupnjevima; `pitch` je kut prema gore od horizonta, samo za vojnike |
| `health` | zdravlje vojnika, bota ili vozila u tom trenutku, tamo gdje ga server šalje (vojnikovo pada ispod 0 dok je ranjen) |
| `speed` | replicirana brzina, cm/s |
| `player` | ime igrača; `bot <id>` za bota; za vozilo ili postavljeni objekt koji nitko ne posjeduje, njegova klasa; za hitac iz oružja vozila, igrač koji sjedi u tom vozilu |
| `team`, `faction` | Squadov broj tima (1, 2) i njegova postavka frakcije, **u tom trenutku**: igrači mogu promijeniti strane |
| `squad` | broj odreda, -1 kad nije u odredu |
| `event` | što redak predstavlja (dolje) |
| `pawn` | vojnikov nacrt (`SQSquidBot` za bota), vozilo, ili za `fire` oružje |
| `seat` | za sjedalo topa ili putnika, vlastiti pawn sjedala |
| `detail` | za `fire` poziv oružja koji je postavio hitac, za `hit` vrsta štete, za `removed` zašto je kanal zatvoren (`Destroyed`, `Dormancy`...) |
| `entity` | akter o kojem je redak (njegov mrežni GUID): `entity` redaka u pratećim datotekama |
| `match` | ime dema |

## Događaji {#events}

| `event` | Na retku | Što |
|---|---|---|
| `position` | vojnik ili bot pješice | uzorak kretanja |
| `vehicle` | vojnik u kopnenom vozilu ili helikopteru | uzorak na položaju vozila |
| `wounded`, `revived`, `death` | vojnici i botovi | gdje se dogodilo |
| `spawn`, `damaged`, `destroyed`, `removed` | vozila, postavljeni objekti, utvrde, sanduci, helikopteri | gdje su bili |
| `seat` | igrač | zauzeo sjedalo |
| `fire` | strijelac | hitac: odakle je krenuo, smjer kao `yaw`/`pitch`/`dirX..Z` |
| `hit` | vozilo | pogodak u vozilo: gdje |

Kako se događaji čitaju: [Kako se demo čita](how-it-works.md#how-the-events-are-read).

## U pregledniku {#in-the-viewer}

Podnožje Parquet datoteke nosi upute za čitanje pod ključem `heat3d`: Z gore,
nijedna os nije zrcaljena, mjerilo jedan, pa preglednik ne treba preslikavanje stupaca.
Učitajte tablicu na kartici Toplinska karta; vidi
[Unos podataka](https://holdi601.github.io/3DHeat/getting-data-in.html) preglednika
i [Preslikavanje stupaca](https://holdi601.github.io/3DHeat/column-mapping.html).
