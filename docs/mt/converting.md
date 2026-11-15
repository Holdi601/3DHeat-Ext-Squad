---
title: Tikkonverti demos
nav_order: 3
lang: "mt"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Tikkonverti demos {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Pass b'pass {#step-by-step}

Ġdid mal-linja tal-kmandi? Aqra [Qabel ma tibda](before-you-start.md) l-ewwel.

1. Installa darba: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   iftaħ terminal f'dak il-folder, ħaddem `python -m pip install -e .`
   (Python 3.10 jew aktar ġdid; iġib miegħu pyarrow u numpy).
2. Poġġi l-fajls `.replay` f'folder, jew semmihom wieħed wieħed.
3. Ħaddem `heat3d-squad-demo <folder> -o out`.
4. Għandek tara linja waħda għal kull demo: is-saff tagħha, il-plejers u r-ringieli, u fejn
   marret it-tabella. Kull demo ssir erba' fajls separati f'`out/<map>/` (mhux
   container `.3dheat`); tgħabbi l-`.parquet` fil-viewer ta' 3DHeat.

![Użu fuq demo sintetika](../assets/img/run.svg)

L-istampa turi użu fuq demo li jibnu t-testijiet (`tests/test_stream.py`),
mhux partita vera.

## Għażliet {#options}

| Għażla | Default | X'jagħmel |
|---|---|---|
| `demos` (waħda jew aktar) | - | fajls `.replay`, jew folders li fihom |
| `-o`, `--out` | meħtieġa | il-folder fejn tinkiteb; kull demo tmur f'`<out>/<map>/` |
| `--flat` | mitfi | tikteb direttament fil-folder, mingħajr il-folder `<map>/` |
| `--json` | mitfi | tistampa linja waħda ta' JSON għal kull demo fuq stdout (għal programmi li jsejħu l-kmand): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; demo li falliet tistampa `demo`, `ok: false` u `error` minflok |
| `--version` | - | tistampa l-verżjoni u tieqaf |

Kull għażla, kif tistampaha l-programm: [Referenza tal-kmandi](../cli-reference.md).

Il-folder tal-mappa huwa l-isem tal-mappa meħud mit-triq tal-livell li semmiet id-demo
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` jagħti `<Map>`).

Status tal-ħruġ: 0 meta kull demo ġiet ikkonvertita; 1 meta xi waħda falliet (l-oħrajn
xorta jinkitbu) jew meta ma nstab ebda fajl `.replay`.

## X'toħroġ {#what-comes-out}

| Fajl | X'fih |
|---|---|
| `<demo>.parquet` | it-tabella: pożizzjonijiet u avvenimenti, ringiela għal kull wieħed ([It-tabella](output-table.md)) |
| `<demo>.match.json` | id-dokument tal-partita ([Id-dokument tal-partita](output-match.md)) |
| `<demo>.entities.parquet` | sidecar: kull aġġornament ta' proprjetà u kull remote call, sħiħ |
| `<demo>.packets.parquet` | sidecar: il-chunks tal-fajl u dak kollu li ma nqrax, sħiħ |

It-tabella u d-dokument tal-partita huma l-istess par li tikteb l-għodda CS2 ta' 3DHeat.
Il-viewer jiftaħ it-tabella direttament u jħalli barra s-sidecars meta
jitgħabba folder sħiħ.

## Eżempji {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` huwa folder ta' eżempju fuq drive D: uża tiegħek.
