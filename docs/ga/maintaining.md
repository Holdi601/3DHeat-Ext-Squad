---
title: Na doiciméid seo a chothabháil
nav_order: 91
lang: ga
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Na doiciméid seo a chothabháil {#maintaining-these-docs}

Seicliosta do gach eisiúint, ionas nach dtiteann na leathanaigh taobh thiar den chód choíche.

1. **Athghin an tagairt.** Athscríobhann `python tools/gen_docs_reference.py`
   [Tagairt orduithe](../cli-reference.md) ó `--help` an chláir féin agus
   ó cholúin aschuir. Scoireann `python tools/gen_docs_reference.py --check` le 1 nuair a
   bhíonn an leathanach tiomanta as dáta.
2. **Liostaigh an rud a d'athraigh.** `git log v<VERSION>..HEAD --oneline`, áit a bhfuil
   `<VERSION>` an leagan eisithe deireanach (an comhad `VERSION` ag an eisiúint).
   Tabhair áit ar leathanach do gach gné nua, rogha nua agus colún aschuir nua, agus sraith
   sa chuid **Docs** de [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Athbhreithniú neamhspleách.** Léann duine nár scríobh na leathanaigh an
   README agus gach leathanach athraithe, na pictiúir san áireamh, trí huaire: mar
   thosaitheoir nár úsáid teirminéal riamh, mar leanbh 8 mbliana d'aois, agus mar shaineolaí
   a sheiceálann gach rogha i gcoinne `--help`. Ní úsáideann samplaí ach ainmneacha agus
   uimhreacha cumtha.
4. **Deisigh** gach rud a aimsíonn an t-athbhreithniú.
5. **Aistriúcháin.** Taifeadann gach leathanach aistrithe haisiú an leathanaigh
   Bhéarla óna ndearnadh é. Aistrigh arís na leathanaigh ar athraigh a bhfoinse Bhéarla,
   ansin athbhreithnigh gach teanga: téacs soiléir, lipéid chearta léaráide, na
   focail chéanna le comhéadan aistrithe an lucht féachana.
6. **Rith na tástálacha** (`pytest`).
7. **Brúigh** tar éis cead an úinéara amháin.

## Aistriúcháin: na horduithe {#translations-the-commands}

Tá an suíomh aistrithe go 40 teanga lucht féachana 3DHeat: Béarla i `docs/`, gach ceann eile
teanga i `docs/<lang>/` leis na hainmneacha comhaid céanna. Déanann `tools/docs_i18n.py` an leabhar-choinneáil:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Ná haistrigh ach an méid a liostaíonn `todo`: fág Markdown, naisc, cód, ainmneacha comhad agus colún mar atá siad,
aistrigh teidil agus tuairiscí pictiúr, agus úsáid focail féin an lucht féachana 3DHeat do chnaipí
agus painéil (a `src/i18n/locales/<lang>/`). Fanann leathanaigh tagartha ghinte agus pictiúir teirminéil
i mBéarla. Ar an suíomh, deir aistriúchán as dáta é sin agus nascann sé an leathanach Béarla; titeann ceann ar iarraidh
siar ar an mBéarla. Tagann roghchlár teangacha an cheanntásc agus athsheoladh teanga brabhsálaí an leathanaigh baile
ó `docs/_includes/`.
