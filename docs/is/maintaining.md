---
title: "Viðhald þessara skjala"
nav_order: 91
lang: is
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Viðhald þessara skjala {#maintaining-these-docs}

Gátlisti fyrir hverja útgáfu, svo síðurnar dragist aldrei aftur úr kóðanum.

1. **Endurgerðu tilvísunina.** `python tools/gen_docs_reference.py` endurskrifar
   [Skipanayfirlit](../cli-reference.md) út frá `--help` forritsins og
   úttaksdálkum þess. `python tools/gen_docs_reference.py --check` skilar 1 þegar
   innritaða tilvísunarsíðan er úrelt.
2. **Taktu saman hvað breyttist.** `git log v<VERSION>..HEAD --oneline`, þar sem
   `<VERSION>` er síðasta útgefna útgáfa (`VERSION` skráin við útgáfu).
   Gefðu hverjum nýjum eiginleika, valkosti og úttaksdálki stað á síðu, og
   röð í **Docs** hlutanum í [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Óháð yfirlestur.** Einhver sem skrifaði ekki síðurnar les
   README og hverja breytta síðu, myndirnar líka, þrisvar: sem byrjandi sem hefur aldrei notað skipanalínu,
   sem 8 ára barn, og sem sérfræðingur
   sem ber hvern valkost saman við `--help`. Dæmi nota aðeins tilbúin nöfn og
   tölur.
4. **Lagaðu** allt sem yfirlesturinn finnur.
5. **Þýðingar.** Sérhver þýdd síða geymir tætigildi ensku síðunnar
   sem hún var gerð úr. Þýddu aftur þær síður þar sem enska frumtextanum var breytt,
   og yfirfarðu síðan hvert tungumál: skýran texta, réttar skýringar á myndritum, sömu
   orð og í þýddu viðmóti skoðarans sjálfs.
6. **Keyrðu prófanirnar** (`pytest`).
7. **Ýttu** (push) aðeins eftir samþykki eigandans.

## Þýðingar: skipanirnar {#translations-the-commands}

Vefurinn er þýddur á 40 tungumál 3DHeat-skoðarans: enska í `docs/`, hvert annað
tungumál í `docs/<lang>/` með sömu skráarnöfnum. `tools/docs_i18n.py` sér um bókhaldið:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Þýddu aðeins það sem `todo` telur upp: haltu Markdown, tenglum, kóða, skráar- og dálkanöfnum óbreyttum,
þýddu titla og myndlýsingar, og notaðu orð 3DHeat-skoðarans sjálfs fyrir hnappa hans
og spjöld (`src/i18n/locales/<lang>/`). Búnar tilvísunarsíður og skipanalínumyndir haldast
á ensku. Á vefnum segir úrelt þýðing frá því og tengir í ensku síðuna; sé þýðing ekki til
er notuð enska. Tungumálavalmynd haussins og tungumálatilvísun heimasíðunnar eftir vafra
koma úr `docs/_includes/`.
