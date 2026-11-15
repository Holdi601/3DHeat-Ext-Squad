---
title: "Než začnete"
nav_order: 1.5
lang: cs
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Než začnete {#before-you-start}

Nikdy jste nepracovali s příkazovým řádkem? Tato stránka vás provede od začátku až k prvnímu spuštění.
Zabere to jednou asi deset minut.

## 1. Nainstalujte Python {#install-python}

Tento nástroj potřebuje **Python 3.10 nebo novější**.

- **Windows:** stáhněte Python z [python.org/downloads](https://www.python.org/downloads/)
  a spusťte instalátor. Na první obrazovce zaškrtněte **Add python.exe to PATH**,
  pak klikněte na **Install Now**.
- **macOS a Linux:** Python 3 tam často už je. Kde tyto stránky píšou
  `python`, napište `python3`.

## 2. Získejte tento nástroj {#get-this-tool}

Otevřete [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), klikněte na
zelené tlačítko **Code** a pak na **Download ZIP**. Soubor rozbalte do složky podle vlastního výběru. Pokud používáte git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Otevřete terminál ve složce nástroje {#open-a-terminal-in-that-folder}

Terminál je okno, do kterého píšete příkazy.

- **Windows:** otevřete složku v Průzkumníkovi, klikněte do adresního řádku, napište
  `powershell` a stiskněte Enter. Otevře se modré nebo černé okno, které už bude v této složce.
- **macOS:** otevřete **Terminal**, napište `cd ` (s mezerou), přetáhněte složku
  do okna a stiskněte Enter.

`cd` znamená „změň složku“: `cd C:\Tools\3DHeat-Ext-Squad` přejde do té složky.

## 4. Nainstalujte nástroj {#install-the-tool}

Napište tento příkaz a stiskněte Enter:

```bash
python -m pip install -e .
```

Na konci byste měli vidět: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Spusťte ho {#run-it}

```bash
heat3d-squad-demo --version
```

Měli byste vidět něco takového:

```text
heat3d-squad-demo 0.1.0
```

Dále: [Nahrávání dema](recording.md), pak [Převod dem](converting.md).

## Jak číst příkazy na těchto stránkách {#how-to-read-the-commands-on-these-pages}

| Vidíte | Znamená to |
|---|---|
| `<folder>` | zástupný text: místo něj napište svou hodnotu, bez `< >` |
| `[--force]` | volitelné: můžete to vynechat, nebo napsat přesně tak, jak je uvedeno |
| `a\|b` | volba: napište `a` nebo `b` |
| `# a note` | poznámka pro vás: nepište ji |
| `"C:\My Files\x"` | cestu, která obsahuje mezery, dejte do uvozovek |
| `D:\Demos` | příklad složky ve Windows: použijte svou |

## Když se něco pokazí {#when-something-goes-wrong}

| Zpráva | Co dělat |
|---|---|
| `'python' is not recognized` | Python není nainstalovaný, nebo nebylo zaškrtnuté políčko PATH: nainstalujte ho znovu a zaškrtněte ho (nebo napište `py` místo `python`). |
| `'heat3d-squad-demo' is not recognized` | Spusťte krok 4 znovu ve složce nástroje, nebo napište `python -m heat3d_ext_squad` místo `heat3d-squad-demo`: udělá to samé. |
| `No module named heat3d_ext_squad` | Nejste ve složce nástroje, nebo krok 4 selhal: `cd` tam přejděte a spusťte krok 4. |
| `No module named pip` | Spusťte `python -m ensurepip`, pak krok 4. |
| cokoli jiného | Přečtěte poslední řádek zprávy a na GitHubu otevřete issue s tímto řádkem. |

Každý příkaz také skončí **stavovým kódem**: 0 znamená, že se povedl. Abyste ho viděli,
napište `echo $LASTEXITCODE` v PowerShellu, nebo `echo $?` na macOS a Linuxu.
