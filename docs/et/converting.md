---
title: "Demode teisendamine"
nav_order: 3
lang: et
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demode teisendamine {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          sama, ilma paigaldamata
```

## Samm-sammult {#step-by-step}

Pole sul käsurealt kogemust? Loe enne [Enne alustamist](before-you-start.md).

1. Paigalda üks kord: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   ava terminal selles kaustas, käivita `python -m pip install -e .`
   (Python 3.10 või uuem; see toob kaasa pyarrow ja numpy).
2. Pane `.replay` failid kausta või nimeta need ükshaaval.
3. Käivita `heat3d-squad-demo <folder> -o out`.
4. Näed ühte rida demo kohta: selle kiht, mängijad ja read ning kuhu tabel kirjutati.
   Iga demo muutub nelja lahtiseks failiks kausta `out/<map>/` (mitte
   `.3dheat` konteineriks); laadi `.parquet` 3DHeat vaatajasse.

![Käivitus sünteetilisel demol](../assets/img/run.svg)

Pilt näitab käivitust demol, mille testid koostavad (`tests/test_stream.py`),
mitte päris mängu.

## Valikud {#options}

| Valik | Vaikimisi | Teeb |
|---|---|---|
| `demos` (üks või mitu) | - | `.replay` failid või kaustad, mis neid hoiavad |
| `-o`, `--out` | nõutud | kaust, kuhu kirjutada; iga demo läheb kausta `<out>/<map>/` |
| `--flat` | väljas | kirjuta otse kausta, ilma `<map>/` kaustata |
| `--json` | väljas | prindi standardväljundisse üks JSON-rida demo kohta (programmidele, mis seda käsku kutsuvad): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; ebaõnnestunud demo prindib selle asemel `demo`, `ok: false` ja `error` |
| `--version` | - | prindi versioon ja lõpeta |

Iga valik, nii nagu programm selle prindib: [Käsu viide](../cli-reference.md).

Kaardi kaust on kaardi nimi, mis võetakse demo nimetatud taseme teelt
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` annab `<Map>`).

Väljumisolek: 0, kui iga demo teisendati; 1, kui mõni ebaõnnestus (teised
kirjutatakse ikka) või kui ühtegi `.replay` faili ei leitud.

## Mis välja tuleb {#what-comes-out}

| Fail | Mis selles on |
|---|---|
| `<demo>.parquet` | tabel: asukohad ja sündmused, üks rida kumbki ([Tabel](output-table.md)) |
| `<demo>.match.json` | mängu dokument ([Mängu dokument](output-match.md)) |
| `<demo>.entities.parquet` | lisafail: iga omaduse uuendus ja iga kaugkäsk, tervena |
| `<demo>.packets.parquet` | lisafail: faili tükid ja kõik, mis ei loetud, tervena |

Tabel ja mängu dokument on sama paar, mida kirjutab 3DHeat CS2 tööriist.
Vaataja avab tabeli otse ja jätab lisafailid välja, kui laaditakse terve kaust.

## Näited {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # iga demo kaustas
heat3d-squad-demo one.replay two.replay -o out --flat  # otse kausta out/
heat3d-squad-demo D:\SquadDemos -o out --json          # üks JSON-rida demo kohta
```

`D:\SquadDemos` on näidiskaust kettal D: kasuta oma.
