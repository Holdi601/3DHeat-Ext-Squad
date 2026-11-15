---
title: "Umbreyting á demo"
nav_order: 3
lang: is
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Umbreyting á demo {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Skref fyrir skref {#step-by-step}

Hefurðu aldrei notað skipanalínu? Lestu fyrst [Áður en þú byrjar](before-you-start.md).

1. Settu upp einu sinni: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   opnaðu skipanalínu í þeirri möppu og keyrðu `python -m pip install -e .`
   (Python 3.10 eða nýrra; það kemur með pyarrow og numpy).
2. Settu `.replay` skrárnar í möppu eða nefndu þær hverja fyrir sig.
3. Keyrðu `heat3d-squad-demo <folder> -o out`.
4. Þú ættir að sjá eina línu fyrir hvert demo: lagið (layer), leikmenn og raðir, og hvert
   taflan fór. Hvert demo verður að fjórum lausum skrám í `out/<map>/` (ekki
   `.3dheat` gámur); hladdu `.parquet` skránni inn í 3DHeat-skoðarann.

![Keyrsla á gervidemo](../assets/img/run.svg)

Myndin sýnir keyrslu á demo sem prófanirnar smíða (`tests/test_stream.py`),
ekki raunverulegan leik.

## Valkostir {#options}

| Valkostur | Sjálfgefið | Gerir |
|---|---|---|
| `demos` (eitt eða fleiri) | - | `.replay` skrár eða möppur sem geyma þær |
| `-o`, `--out` | nauðsynlegt | mappan sem skrifað er í; hvert demo fer í `<out>/<map>/` |
| `--flat` | af | skrifa beint í möppuna, án `<map>/` möppunnar |
| `--json` | af | prenta eina JSON-línu fyrir hvert demo á stdout (fyrir forrit sem kalla á skipunina): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; demo sem mistókst prentar `demo`, `ok: false` og `error` í staðinn |
| `--version` | - | prenta útgáfuna og hætta |

Hver valkostur, eins og forritið prentar hann: [Skipanayfirlit](../cli-reference.md).

Kortamappan er nafn kortsins, tekið úr borðaslóðinni sem demo-ið nefnir
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` gefur `<Map>`).

Útgöngustaða: 0 þegar öll demo voru umbreytt; 1 þegar eitthvert mistókst (hin
eru samt skrifuð) eða þegar engin `.replay` skrá fannst.

## Hvað kemur út {#what-comes-out}

| Skrá | Hvað hún geymir |
|---|---|
| `<demo>.parquet` | taflan: staðsetningar og atburðir, ein röð hvert ([Taflan](output-table.md)) |
| `<demo>.match.json` | leikjaskjalið ([Leikjaskjalið](output-match.md)) |
| `<demo>.entities.parquet` | hliðarskrá: sérhver eigindauppfærsla og fjarkall, í heild |
| `<demo>.packets.parquet` | hliðarskrá: bútar skrárinnar og allt sem ekki las, í heild |

Taflan og leikjaskjalið eru sama parið og 3DHeat CS2 verkfærið skrifar.
Skoðarinn opnar töfluna beint og sleppir hliðarskránum þegar heil
mappa er hlaðin inn.

## Dæmi {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` er dæmi um möppu á drifi D: notaðu þína eigin.
