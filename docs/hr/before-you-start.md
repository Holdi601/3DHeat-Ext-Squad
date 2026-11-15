---
title: Prije nego što počnete
nav_order: 1.5
lang: hr
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Prije nego što počnete {#before-you-start}

Ne znate ništa o naredbenom retku? Ova stranica vas vodi od nule do prvog pokretanja.
Traje oko deset minuta, samo jednom.

## 1. Instalirajte Python {#install-python}

Ovaj alat treba **Python 3.10 ili noviji**.

- **Windows:** preuzmite Python s [python.org/downloads](https://www.python.org/downloads/)
  i pokrenite instalaciju. Na prvom zaslonu označite **Add python.exe to PATH**,
  zatim kliknite **Install Now**.
- **macOS i Linux:** Python 3 je često već tu. Tamo gdje ove stranice pišu
  `python`, upišite `python3`.

## 2. Nabavite ovaj alat {#get-this-tool}

Otvorite [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), kliknite
zeleni gumb **Code**, zatim **Download ZIP**, i raspakirajte ga u mapu po vašem izboru. Ako koristite git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Otvorite terminal u toj mapi {#open-a-terminal-in-that-folder}

Terminal je prozor u koji upisujete naredbe.

- **Windows:** otvorite mapu u Exploreru, kliknite u adresnu traku, upišite
  `powershell` i pritisnite Enter. Otvori se plavi ili crni prozor, već u toj mapi.
- **macOS:** otvorite **Terminal**, upišite `cd ` (s razmakom), povucite mapu
  u prozor i pritisnite Enter.

`cd` znači "promijeni mapu": `cd C:\Tools\3DHeat-Ext-Squad` vodi u tu mapu.

## 4. Instalirajte alat {#install-the-tool}

Upišite ovo i pritisnite Enter:

```bash
python -m pip install -e .
```

Na kraju biste trebali vidjeti: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Pokrenite ga {#run-it}

```bash
heat3d-squad-demo --version
```

Trebali biste vidjeti nešto poput:

```text
heat3d-squad-demo 0.1.0
```

Dalje: [Snimanje dema](recording.md), zatim [Pretvaranje dema](converting.md).

## Kako čitati naredbe na ovim stranicama {#how-to-read-the-commands-on-these-pages}

| Vidite | Znači |
|---|---|
| `<folder>` | mjesto za upis: upišite svoju vrijednost, bez `< >` |
| `[--force]` | izborno: izostavite ili upišite kao što piše |
| `a\|b` | izbor: upišite `a` ili `b` |
| `# a note` | komentar za vas: ne upisujte ga |
| `"C:\My Files\x"` | put koji ima razmake stavite u navodnike |
| `D:\Demos` | primjer mape na Windowsu: upotrijebite svoju |

## Kad nešto pođe po zlu {#when-something-goes-wrong}

| Poruka | Što učiniti |
|---|---|
| `'python' is not recognized` | Python nije instaliran ili nije bio označen okvir PATH: instalirajte ga ponovno i označite ga (ili upišite `py` umjesto `python`). |
| `'heat3d-squad-demo' is not recognized` | Ponovite korak 4 u mapi alata ili upišite `python -m heat3d_ext_squad` umjesto `heat3d-squad-demo`: radi isto. |
| `No module named heat3d_ext_squad` | Niste u mapi alata ili korak 4 nije uspio: `cd` u tu mapu i pokrenite korak 4. |
| `No module named pip` | Pokrenite `python -m ensurepip`, zatim korak 4. |
| sve drugo | Pročitajte zadnji redak poruke, zatim na GitHubu otvorite issue s tim retkom. |

Svaka naredba također završava **izlaznim statusom**: 0 znači da je uspjela. Da ga vidite,
upišite `echo $LASTEXITCODE` u PowerShellu ili `echo $?` na macOS-u i Linuxu.
