---
title: Пре почетка
nav_order: 1.5
lang: sr
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Пре почетка {#before-you-start}

Први пут у командној линији? Ова страница вас води од нуле до првог покретања.
Траје око десет минута, једном.

## 1. Инсталирајте Python {#install-python}

Овај алат захтева **Python 3.10 или новији**.

- **Windows:** преузмите Python са [python.org/downloads](https://www.python.org/downloads/)
  и покрените инсталер. На његовом првом екрану штиклирајте **Add python.exe to PATH**,
  па кликните на **Install Now**.
- **macOS и Linux:** Python 3 је често већ инсталиран. Где ове стране кажу
  `python`, укуцајте `python3`.

## 2. Набави овај алат {#get-this-tool}

Отворите [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), кликните на
зелено дугме **Code**, па на **Download ZIP**, и распакујте га у фасциклу по свом избору. Ако користите git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Отворите терминал у тој фасцикли {#open-a-terminal-in-that-folder}

Терминал је прозор у који куцате команде.

- **Windows:** отворите фасциклу у Explorer-у, кликните у адресну траку, укуцајте
  `powershell` и притисните Enter. Отвара се плаво или црно прозорче, већ у
  тој фасцикли.
- **macOS:** отворите **Terminal**, укуцајте `cd ` (са размаком), превуците фасциклу
  у прозор и притисните Enter.

`cd` значи „промените фасциклу": `cd C:\Tools\3DHeat-Ext-Squad` иде у ту фасциклу.

## 4. Инсталирајте алат {#install-the-tool}

Укуцајте ово и притисните Enter:

```bash
python -m pip install -e .
```

На крају би требало да видите: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Покрените га {#run-it}

```bash
heat3d-squad-demo --version
```

Требало би да видите нешто слично:

```text
heat3d-squad-demo 0.1.0
```

Следеће: [Снимање демоа](recording.md), па [Претварање демоа](converting.md).

## Како читати команде на овим страницама {#how-to-read-the-commands-on-these-pages}

| Видите | Значи |
|---|---|
| `<folder>` | место за попуњавање: уместо тога укуцајте своју вредност, без `< >` |
| `[--force]` | необавезно: изоставите или укуцајте како је приказано |
| `a\|b` | избор: укуцајте `a` или `b` |
| `# a note` | коментар за вас: не куцајте га |
| `"C:\My Files\x"` | путању са размацима ставите под наводнике |
| `D:\Demos` | пример Windows фасцикле: користите своју |

## Кад нешто није у реду {#when-something-goes-wrong}

| Порука | Шта да урадите |
|---|---|
| `'python' is not recognized` | Python није инсталиран, или поље PATH није штиклирано: инсталирајте га поново и штиклирајте га (или укуцајте `py` уместо `python`). |
| `'heat3d-squad-demo' is not recognized` | Поново покрените корак 4 у фасцикли алата, или укуцајте `python -m heat3d_ext_squad` уместо `heat3d-squad-demo`: ради исто. |
| `No module named heat3d_ext_squad` | Нисте у фасцикли алата, или корак 4 није успео: `cd` до ње и покрените корак 4. |
| `No module named pip` | Покрените `python -m ensurepip`, па корак 4. |
| било шта друго | Прочитајте последњи ред поруке, па отворите issue на GitHub-у са њим. |

Свака команда се завршава и **излазним статусом**: 0 значи да је успела. Да га видите,
укуцајте `echo $LASTEXITCODE` у PowerShell-у или `echo $?` на macOS и Linux-у.
