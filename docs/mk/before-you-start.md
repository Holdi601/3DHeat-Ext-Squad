---
title: Пред да започнете
nav_order: 1.5
lang: "mk"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Пред да започнете {#before-you-start}

Нови сте со командната линија? Оваа страница ве води од нула до првото извршување.
Потребни се околу десет минути, еднаш.

## 1. Инсталирајте Python {#install-python}

Оваа алатка бара **Python 3.10 или понов**.

- **Windows:** преземете го Python од [python.org/downloads](https://www.python.org/downloads/)
  и пуштете го инсталерот. На неговиот прв екран штиклирајте **Add python.exe to PATH**,
  а потоа кликнете **Install Now**.
- **macOS и Linux:** Python 3 често веќе е тука. Таму каде што овие страници
  велат `python`, напишете `python3`.

## 2. Преземете ја алатката {#get-this-tool}

Отворете [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), кликнете на
зеленото копче **Code**, потоа **Download ZIP** и распакувајте го во папка по
ваш избор. Ако користите git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Отворете терминал во таа папка {#open-a-terminal-in-that-folder}

Терминалот е прозорец во кој пишувате команди.

- **Windows:** отворете ја папката во Explorer, кликнете во адресната лента, напишете
  `powershell` и притиснете Enter. Се отвора син или црн прозорец, веќе во таа
  папка.
- **macOS:** отворете **Terminal**, напишете `cd ` (со празно место), повлечете ја папката во
  прозорецот и притиснете Enter.

`cd` значи „смени папка“: `cd C:\Tools\3DHeat-Ext-Squad` оди во таа папка.

## 4. Инсталирајте ја алатката {#install-the-tool}

Напишете го ова и притиснете Enter:

```bash
python -m pip install -e .
```

На крајот треба да видите: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Пуштете ја {#run-it}

```bash
heat3d-squad-demo --version
```

Треба да видите нешто такво:

```text
heat3d-squad-demo 0.1.0
```

Следно: [Снимање демо](recording.md), потоа [Претворање демоа](converting.md).

## Како да ги читате командите на овие страници {#how-to-read-the-commands-on-these-pages}

| Што гледате | Што значи |
|---|---|
| `<folder>` | место за пополнување: напишете своја вредност наместо тоа, без `< >` |
| `[--force]` | по избор: изоставете го или напишете го како што е прикажано |
| `a\|b` | избор: напишете `a` или `b` |
| `# a note` | коментар за вас: не го пишувајте |
| `"C:\My Files\x"` | патека со празни места ставете во наводници |
| `D:\Demos` | пример за Windows папка: користете своја |

## Кога нешто ќе тргне наопаку {#when-something-goes-wrong}

| Пораката | Што да направите |
|---|---|
| `'python' is not recognized` | Python не е инсталиран, или не е штиклирано PATH: инсталирајте го повторно и штиклирајте го (или напишете `py` наместо `python`). |
| `'heat3d-squad-demo' is not recognized` | Повторете го чекор 4 во папката на алатката, или напишете `python -m heat3d_ext_squad` наместо `heat3d-squad-demo`: прави исто. |
| `No module named heat3d_ext_squad` | Не сте во папката на алатката, или чекор 4 не успеа: со `cd` одете таму и повторете го чекор 4. |
| `No module named pip` | Пуштете `python -m ensurepip`, потоа чекор 4. |
| сè друго | Прочитајте ја последната линија од пораката, па отворете проблем (issue) на GitHub со неа. |

Секоја команда завршува и со **излезен статус**: 0 значи дека успеала. За да го видите,
напишете `echo $LASTEXITCODE` во PowerShell или `echo $?` на macOS и Linux.
