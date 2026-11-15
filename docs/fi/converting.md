---
title: "Demojen muuntaminen"
nav_order: 3
lang: fi
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demojen muuntaminen {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          sama ilman asennusta
```

## Vaihe vaiheelta {#step-by-step}

Uusi komentorivin kanssa? Lue ensin [Ennen aloittamista](before-you-start.md).

1. Asenna kerran: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   avaa pääte kyseisessä kansiossa ja suorita `python -m pip install -e .`
   (Python 3.10 tai uudempi; se tuo mukanaan pyarrow- ja numpy-kirjastot).
2. Laita `.replay`-tiedostot kansioon tai nimeä ne yksi kerrallaan.
3. Suorita `heat3d-squad-demo <folder> -o out`.
4. Näet yhden rivin demoa kohden: sen tason, pelaajat ja rivit sekä sen, minne taulukko
   kirjoitettiin. Jokainen demo muuttuu neljäksi irralliseksi tiedostoksi kansioon
   `out/<map>/` (ei `.3dheat`-säiliöksi); lataa `.parquet` 3DHeat-katselimeen.

![Ajo synteettisellä demolla](../assets/img/run.svg)

Kuvassa on ajo demolla, jonka testit rakentavat (`tests/test_stream.py`),
ei oikealla ottelulla.

## Asetukset {#options}

| Asetus | Oletus | Tekee |
|---|---|---|
| `demos` (yksi tai useampi) | - | `.replay`-tiedostot tai kansiot, joissa niitä on |
| `-o`, `--out` | pakollinen | kansio, johon kirjoitetaan; jokainen demo menee kansioon `<out>/<map>/` |
| `--flat` | pois | kirjoittaa suoraan kansioon ilman `<map>/`-kansiota |
| `--json` | pois | tulostaa yhden JSON-rivin demoa kohden vakiotulosteeseen (ohjelmille, jotka kutsuvat komentoa): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; epäonnistunut demo tulostaa `demo`, `ok: false` ja `error` sen sijaan |
| `--version` | - | tulostaa version ja pysähtyy |

Jokainen asetus sellaisena kuin ohjelma ne tulostaa: [Komentoviite](../cli-reference.md).

Kansion nimi on kartan nimi, joka otetaan demon nimeämästä tason polusta
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` antaa `<Map>`).

Poistumistila: 0, kun jokainen demo muunnettiin; 1, kun jokin epäonnistui (muut
kirjoitetaan silti) tai kun yhtään `.replay`-tiedostoa ei löytynyt.

## Mitä syntyy {#what-comes-out}

| Tiedosto | Mitä se sisältää |
|---|---|
| `<demo>.parquet` | taulukko: sijainnit ja tapahtumat, yksi rivi kumpikin ([Taulukko](output-table.md)) |
| `<demo>.match.json` | ottelun asiakirja ([Ottelun asiakirja](output-match.md)) |
| `<demo>.entities.parquet` | liitetiedosto: jokainen ominaisuuspäivitys ja etäkutsu kokonaisena |
| `<demo>.packets.parquet` | liitetiedosto: tiedoston osat ja kaikki, mitä ei luettu, kokonaisena |

Taulukko ja ottelun asiakirja ovat sama pari, jonka 3DHeat CS2 -työkalu kirjoittaa.
Katselin avaa taulukon suoraan ja jättää liitetiedostot pois, kun koko kansio ladataan.

## Esimerkit {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # jokainen demo kansiossa
heat3d-squad-demo one.replay two.replay -o out --flat  # suoraan kansioon out/
heat3d-squad-demo D:\SquadDemos -o out --json          # yksi JSON-rivi demoa kohden
```

`D:\SquadDemos` on esimerkkikansio asemalla D: käytä omaasi.
