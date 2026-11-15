---
title: Pretvaranje dema
nav_order: 3
lang: hr
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Pretvaranje dema {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          isto, bez instalacije
```

## Korak po korak {#step-by-step}

Ne znate ništa o naredbenom retku? Prvo pročitajte [Prije nego što počnete](before-you-start.md).

1. Instalirajte jednom: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   otvorite terminal u toj mapi, pokrenite `python -m pip install -e .`
   (Python 3.10 ili noviji; donosi pyarrow i numpy).
2. Stavite `.replay` datoteke u mapu ili ih navedite jednu po jednu.
3. Pokrenite `heat3d-squad-demo <folder> -o out`.
4. Trebali biste vidjeti jedan redak po demu: njegov sloj, igrače i retke te
   gdje je završila tablica. Svaki demo postaje četiri zasebne datoteke u `out/<map>/`
   (ne spremnik `.3dheat`); učitajte `.parquet` u preglednik 3DHeat.

![Pokretanje na sintetičkom demou](../assets/img/run.svg)

Slika prikazuje pokretanje na demou koji grade testovi (`tests/test_stream.py`),
a ne na pravom meču.

## Opcije {#options}

| Opcija | Zadano | Što radi |
|---|---|---|
| `demos` (jedna ili više) | - | `.replay` datoteke ili mape koje ih sadrže |
| `-o`, `--out` | obavezno | mapa u koju se piše; svaki demo ide u `<out>/<map>/` |
| `--flat` | isključeno | piše izravno u mapu, bez mape `<map>/` |
| `--json` | isključeno | ispisuje jedan redak JSON-a po demu na stdout (za programe koji pozivaju naredbu): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; demo koji nije uspio ispisuje `demo`, `ok: false` i `error` |
| `--version` | - | ispisuje verziju i staje |

Svaka opcija, onako kako je program ispisuje: [Referenca naredbi](../cli-reference.md).

Mapa karte je ime karte uzeto iz putanje razine koju demo navodi
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` daje `<Map>`).

Izlazni status: 0 kad je svaki demo pretvoren; 1 kad je neki nije uspio (ostali se
ipak zapišu) ili kad nije pronađena nijedna `.replay` datoteka.

## Što izlazi {#what-comes-out}

| Datoteka | Što sadrži |
|---|---|
| `<demo>.parquet` | tablica: položaji i događaji, po jedan redak ([Tablica](output-table.md)) |
| `<demo>.match.json` | dokument meča ([Dokument meča](output-match.md)) |
| `<demo>.entities.parquet` | prateća datoteka: svaka promjena svojstva i udaljeni poziv, cijela |
| `<demo>.packets.parquet` | prateća datoteka: dijelovi datoteke i sve što se nije pročitalo, cijelo |

Tablica i dokument meča isti su par koji piše 3DHeat CS2 alat.
Preglednik otvara tablicu izravno i izostavlja prateće datoteke kad se učita cijela
mapa.

## Primjeri {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # svaki demo u mapi
heat3d-squad-demo one.replay two.replay -o out --flat  # izravno u out/
heat3d-squad-demo D:\SquadDemos -o out --json          # jedan JSON redak po demou
```

`D:\SquadDemos` je primjer mape na pogonu D: upotrijebite svoju.
