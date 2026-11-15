---
title: "Pretvaranje demoa"
nav_order: 3
lang: bs
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Pretvaranje demoa {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Korak po korak {#step-by-step}

Komandna linija ti je nova? Prvo pročitaj [Prije nego počneš](before-you-start.md).

1. Instaliraj jednom: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   otvori terminal u tom folderu, pokreni `python -m pip install -e .`
   (Python 3.10 ili noviji; donosi pyarrow i numpy).
2. Stavi `.replay` datoteke u folder ili ih navedi jednu po jednu.
3. Pokreni `heat3d-squad-demo <folder> -o out`.
4. Trebao bi vidjeti jedan red po demou: njegov sloj, igrače i redove, te gdje je
   tabela završila. Svaki demo postaje četiri odvojene datoteke u `out/<map>/` (ne
   `.3dheat` spremnik); učitaj `.parquet` u 3DHeat pregledniku.

![Pokretanje na sintetičkom demou](../assets/img/run.svg)

Slika prikazuje pokretanje na demou koji grade testovi (`tests/test_stream.py`),
a ne pravi meč.

## Opcije {#options}

| Opcija | Zadano | Radi |
|---|---|---|
| `demos` (jedan ili više) | - | `.replay` datoteke ili folderi u kojima se nalaze |
| `-o`, `--out` | obavezno | folder u koji se piše; svaki demo ide u `<out>/<map>/` |
| `--flat` | isključeno | piše direktno u folder, bez foldera `<map>/` |
| `--json` | isključeno | ispisuje jedan red JSON-a po demou na stdout (za programe koji pozivaju naredbu): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; demo koji nije uspio umjesto toga ispisuje `demo`, `ok: false` i `error` |
| `--version` | - | ispisuje verziju i staje |

Sve opcije, onako kako ih program ispisuje: [Referenca naredbi](../cli-reference.md).

Folder mape je naziv mape uzet iz putanje nivoa koju demo navodi
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` daje `<Map>`).

Izlazni status: 0 kad je svaki demo pretvoren; 1 kad je ijedan propao (ostali
se svejedno pišu) ili kad nije pronađena nijedna `.replay` datoteka.

## Šta izlazi {#what-comes-out}

| Datoteka | Šta sadrži |
|---|---|
| `<demo>.parquet` | tabela: pozicije i događaji, po jedan red ([Tabela](output-table.md)) |
| `<demo>.match.json` | dokument meča ([Dokument meča](output-match.md)) |
| `<demo>.entities.parquet` | pomoćna datoteka: svako ažuriranje svojstva i svaki udaljeni poziv, cjelovito |
| `<demo>.packets.parquet` | pomoćna datoteka: dijelovi (chunks) datoteke i sve što se nije dalo pročitati, cjelovito |

Tabela i dokument meča su isti par koji piše 3DHeat CS2 alat.
Preglednik otvara tabelu direktno, a pomoćne datoteke preskače kad se
učitava cijeli folder.

## Primjeri {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` je primjer foldera na disku D: koristi svoj.
