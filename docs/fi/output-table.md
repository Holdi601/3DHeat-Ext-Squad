---
title: "Taulukko"
nav_order: 4
lang: fi
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Taulukko: `<demo>.parquet` {#the-table-parquet}

Yksi rivi jokaista näytettä tai tapahtumaa kohden. Näyte otetaan aina, kun palvelin replikoi
toimijan liikkeen, enintään 8 kertaa sekunnissa (demon tallennusnopeus) sen liikkuessa.

![Synteettisen demon taulukon ensimmäiset rivit](../assets/img/table.svg)

## Sarakkeet {#columns}

| Sarake | Mitä se on |
|---|---|
| `time` | sekunteja tallennuksen alusta |
| `x`, `y`, `z` | sijainti Unreal-yksiköissä (senttimetreissä), Z ylöspäin |
| `dirX`, `dirY`, `dirZ` | mihin sotilas katsoo: rungon kiertymä ja katseen kallistus yksikkövektorina (ajoneuvon: vaakasuora) |
| `yaw`, `pitch` | sama asteina; `pitch` ylöspäin horisontista, vain sotilaat |
| `health` | sotilaan, botin tai ajoneuvon terveys sillä hetkellä, missä palvelin sen lähetti (sotilaan laskee alle 0:n haavoittuneena) |
| `speed` | replikoitu nopeus, cm/s |
| `player` | pelaajan nimi; `bot <id>` botille; ajoneuvolle tai siirrettävälle tukikohdalle, jota kukaan ei omista, sen luokka; ajoneuvon aseen laukaukselle ajoneuvossa istuva pelaaja |
| `team`, `faction` | Squadin joukkuenumero (1, 2) ja sen puoliasetelma, **sillä hetkellä**: pelaajat voivat vaihtaa puolta |
| `squad` | ryhmän numero, -1 kun ei ryhmässä |
| `event` | mitä rivi on (alla) |
| `pawn` | sotilaan blueprint (`SQSquidBot` botille), ajoneuvo, tai `fire`-rivillä ase |
| `seat` | tykin tai matkustajan istuimelle istuimen oma pawn |
| `detail` | `fire`-rivillä aseen kutsu, joka teki laukauksen; `hit`-rivillä vahingon tyyppi; `removed`-rivillä syy, miksi kanava suljettiin (`Destroyed`, `Dormancy`...) |
| `entity` | toimija, jota rivi koskee (sen net GUID): sivutiedostojen rivien `entity` |
| `match` | demon nimi |

## Tapahtumat {#events}

| `event` | Rivi, jolla | Mitä |
|---|---|---|
| `position` | sotilas tai botti jalan | liikenäyte |
| `vehicle` | sotilas maavoimilla tai helikopterissa | näyte ajoneuvon sijainnista |
| `wounded`, `revived`, `death` | sotilaat ja botit | missä se tapahtui |
| `spawn`, `damaged`, `destroyed`, `removed` | ajoneuvot, siirrettävät tukikohdat, asemat, laatikot, helikopterit | missä ne olivat |
| `seat` | pelaaja | otti istuimen |
| `fire` | ampuja | laukaus: mistä se lähti, sen suunta `yaw`/`pitch`/`dirX..Z` -arvoina |
| `hit` | ajoneuvo | ajoneuvo-osuma: mihin |

Miten tapahtumat luetaan, on kohdassa [Miten demo luetaan](how-it-works.md#how-the-events-are-read).

## Katselimessa {#in-the-viewer}

Parquet-alatunnisteessa on lukuohjeet avaimen `heat3d` alla: Z ylöspäin, mitään akselia ei peilata,
yksikkömittakaava 1, joten katselin ei tarvitse sarakkeiden kartoitusta. Lataa taulukko
Lämpökartta-välilehdelle; katso katselimen
[Tietojen tuominen](https://holdi601.github.io/3DHeat/getting-data-in.html) ja
[Sarakkeiden kartoitus](https://holdi601.github.io/3DHeat/column-mapping.html).
