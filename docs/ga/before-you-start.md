---
title: Sula dtosaíonn tú
nav_order: 1.5
lang: ga
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Sula dtosaíonn tú {#before-you-start}

An bhfuil tú nua leis an líne ordaithe? Tugann an leathanach seo thú ó rud ar bith go dtí do chéad rith.
Tógann sé thart ar dheich nóiméad, uair amháin.

## 1. Suiteáil Python {#install-python}

Teastaíonn **Python 3.10 nó níos nuaí** ón uirlis seo.

- **Windows:** íoslódáil Python ó [python.org/downloads](https://www.python.org/downloads/)
  agus rith an suiteálaí. Ar a chéad scáileán, cuir tic i **Add python.exe to PATH**,
  ansin cliceáil **Install Now**.
- **macOS agus Linux:** is minic go bhfuil Python 3 ann cheana féin. Nuair a deir na leathanaigh seo
  `python`, clóscríobh `python3`.

## 2. Faigh an uirlis seo {#get-this-tool}

Oscail [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), cliceáil an
cnaipe glas **Code**, ansin **Download ZIP**, agus dízipeáil é i bhfillteán
de do rogha. Má úsáideann tú git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Oscail teirminéal sa fhillteán sin {#open-a-terminal-in-that-folder}

Is fuinneog é teirminéal inar clóscríobhann tú orduithe.

- **Windows:** oscail an fillteán in Explorer, cliceáil isteach sa bharra seoltaí, clóscríobh
  `powershell` agus brúigh Enter. Osclaíonn fuinneog ghorm nó dhubh, cheana féin sa
  fhillteán sin.
- **macOS:** oscail **Terminal**, clóscríobh `cd ` (le spás), tarraing an fillteán isteach sa
  fhuinneog agus brúigh Enter.

Ciallaíonn `cd` "athraigh fillteán": téann `cd C:\Tools\3DHeat-Ext-Squad` go dtí an fillteán sin.

## 4. Suiteáil an uirlis {#install-the-tool}

Clóscríobh é seo agus brúigh Enter:

```bash
python -m pip install -e .
```

Ba chóir duit a fheiceáil, ag an deireadh: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Rith í {#run-it}

```bash
heat3d-squad-demo --version
```

Ba chóir duit rud éigin mar seo a fheiceáil:

```text
heat3d-squad-demo 0.1.0
```

Ar aghaidh: [Taifead demo](recording.md), ansin [Demos a thiontú](converting.md).

## Conas na horduithe ar na leathanaigh seo a léamh {#how-to-read-the-commands-on-these-pages}

| Feiceann tú | Ciallaíonn sé |
|---|---|
| `<folder>` | ionadchoinneálaí: clóscríobh do luach féin ina áit, gan an `< >` |
| `[--force]` | roghnach: fág ar lár é, nó clóscríobh é mar atá le feiceáil |
| `a\|b` | rogha: clóscríobh `a` nó `b` |
| `# a note` | nóta duitse: ná clóscríobh é |
| `"C:\My Files\x"` | cuir cosán a bhfuil spásanna ann idir comharthaí athfhriotail |
| `D:\Demos` | sampla d'fhillteán Windows: úsáid ceann de do chuid féin |

## Nuair a théann rud éigin cearr {#when-something-goes-wrong}

| An teachtaireacht | Cad atá le déanamh |
|---|---|
| `'python' is not recognized` | Níl Python suiteáilte, nó níor cuireadh tic sa bhosca PATH: suiteáil arís é agus cuir tic ann (nó clóscríobh `py` in ionad `python`). |
| `'heat3d-squad-demo' is not recognized` | Rith céim 4 arís i bhfillteán na huirlise, nó clóscríobh `python -m heat3d_ext_squad` in ionad `heat3d-squad-demo`: déanann sé an rud céanna. |
| `No module named heat3d_ext_squad` | Níl tú i bhfillteán na huirlise, nó theip ar chéim 4: úsáid `cd` chun dul ansin agus rith céim 4. |
| `No module named pip` | Rith `python -m ensurepip`, ansin céim 4. |
| aon rud eile | Léigh líne dheireanach na teachtaireachta, ansin oscail ceist (issue) ar GitHub léi. |

Críochnaíonn gach ordú le **stádas scoir** freisin: ciallaíonn 0 gur oibrigh sé. Chun é a fheiceáil,
clóscríobh `echo $LASTEXITCODE` i PowerShell nó `echo $?` ar macOS agus Linux.
