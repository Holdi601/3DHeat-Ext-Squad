---
title: "Mielőtt elkezdi"
nav_order: 1.5
lang: hu
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Mielőtt elkezdi {#before-you-start}

Még nem használt parancssort? Ez az oldal a semmitől az első futtatásig vezeti el.
Egyszer tart, nagyjából tíz percig.

## 1. Telepítse a Pythont {#install-python}

Ehhez az eszközhöz **Python 3.10 vagy újabb** kell.

- **Windows:** töltse le a Pythont a [python.org/downloads](https://www.python.org/downloads/)
  oldalról, és futtassa a telepítőt. Az első képernyőn pipálja be a **Add python.exe to PATH**
  lehetőséget, majd kattintson az **Install Now** gombra.
- **macOS és Linux:** a Python 3 gyakran már fent van. Ahol ezek az oldalak `python`-t írnak,
  ott gépelje be a `python3`-at.

## 2. Szerezze meg ezt az eszközt {#get-this-tool}

Nyissa meg a [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad)
oldalt, kattintson a zöld **Code** gombra, majd a **Download ZIP** lehetőségre, és csomagolja
ki egy tetszőleges mappába. Ha git-et használ: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Nyisson terminált abban a mappában {#open-a-terminal-in-that-folder}

A terminál olyan ablak, ahová parancsokat gépel.

- **Windows:** nyissa meg a mappát a Fájlkezelőben, kattintson a címsorba, gépelje be
  a `powershell`-t, és nyomjon Entert. Egy kék vagy fekete ablak nyílik meg, már abban a
  mappában.
- **macOS:** nyissa meg a **Terminal** alkalmazást, gépelje be a `cd `-t (szóközzel), húzza
  a mappát az ablakba, és nyomjon Entert.

A `cd` azt jelenti: „mappát vált”. A `cd C:\Tools\3DHeat-Ext-Squad` ebbe a mappába visz.

## 4. Telepítse az eszközt {#install-the-tool}

Gépelje be ezt, és nyomjon Entert:

```bash
python -m pip install -e .
```

A végén ezt kell látnia: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Futtassa {#run-it}

```bash
heat3d-squad-demo --version
```

Valami ilyesmit kell látnia:

```text
heat3d-squad-demo 0.1.0
```

Következő: [Demó felvétele](recording.md), majd [Demók átalakítása](converting.md).

## Hogyan olvassa a parancsokat ezeken az oldalakon {#how-to-read-the-commands-on-these-pages}

| Amit lát | Jelentése |
|---|---|
| `<folder>` | helyőrző: írja be a saját értékét, a `< >` jelek nélkül |
| `[--force]` | nem kötelező: hagyja ki, vagy írja be úgy, ahogy látja |
| `a\|b` | választás: írja be az `a`-t vagy a `b`-t |
| `# a note` | megjegyzés az Ön számára: ne írja be |
| `"C:\My Files\x"` | a szóközöket tartalmazó útvonalat idézőjelek közé tegye |
| `D:\Demos` | példa Windows-mappa: használja a sajátját |

## Ha valami nem jól működik {#when-something-goes-wrong}

| Az üzenet | Mit tegyen |
|---|---|
| `'python' is not recognized` | A Python nincs telepítve, vagy nem volt bepipálva a PATH mező: telepítse újra, és pipálja be (vagy `python` helyett írja be a `py`-t). |
| `'heat3d-squad-demo' is not recognized` | Futtassa újra a 4. lépést az eszköz mappájában, vagy a `heat3d-squad-demo` helyett írja be a `python -m heat3d_ext_squad`-ot: ugyanazt csinálja. |
| `No module named heat3d_ext_squad` | Nem az eszköz mappájában van, vagy a 4. lépés nem sikerült: lépjen oda a `cd` paranccsal, és futtassa a 4. lépést. |
| `No module named pip` | Futtassa a `python -m ensurepip` parancsot, majd a 4. lépést. |
| minden más | Olvassa el az üzenet utolsó sorát, és nyisson róla egy hibajegyet (issue) a GitHubon. |

Minden parancs egy **kilépési állapottal** (exit status) is végződik: a 0 azt jelenti, hogy
sikerült. Ennek megtekintéséhez gépelje be az `echo $LASTEXITCODE` parancsot PowerShellben,
vagy az `echo $?` parancsot macOS-en és Linuxon.
