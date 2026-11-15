---
title: "Prije nego počneš"
nav_order: 1.5
lang: "bs"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Prije nego počneš {#before-you-start}

Komandna linija ti je nova? Ova stranica te vodi od nule do prvog
pokretanja. Treba otprilike deset minuta, jednom.

## 1. Instaliraj Python {#install-python}

Ovaj alat treba **Python 3.10 ili noviji**.

- **Windows:** preuzmi Python sa [python.org/downloads](https://www.python.org/downloads/)
  i pokreni instalacijski program. Na njegovom prvom ekranu označi **Add python.exe to PATH**,
  pa klikni **Install Now**.
- **macOS i Linux:** Python 3 je često već instaliran. Gdje ove stranice kažu
  `python`, upiši `python3`.

## 2. Nabavi ovaj alat {#get-this-tool}

Otvori [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), klikni zeleno
dugme **Code**, zatim **Download ZIP**, i raspakuj ga u željeni folder. Ako koristiš git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Otvori terminal u tom folderu {#open-a-terminal-in-that-folder}

Terminal je prozor u koji upisuješ naredbe.

- **Windows:** otvori folder u Exploreru, klikni u adresnu traku, upiši
  `powershell` i pritisni Enter. Otvara se plavi ili crni prozor, već u tom
  folderu.
- **macOS:** otvori **Terminal**, upiši `cd ` (s razmakom), prevuci folder u
  prozor i pritisni Enter.

`cd` znači "promijeni folder": `cd C:\Tools\3DHeat-Ext-Squad` vodi u taj folder.

## 4. Instaliraj alat {#install-the-tool}

Upiši ovo i pritisni Enter:

```bash
python -m pip install -e .
```

Na kraju bi trebao vidjeti: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Pokreni ga {#run-it}

```bash
heat3d-squad-demo --version
```

Trebao bi vidjeti nešto ovako:

```text
heat3d-squad-demo 0.1.0
```

Dalje: [Snimanje demoa](recording.md), zatim [Pretvaranje demoa](converting.md).

## Kako čitati naredbe na ovim stranicama {#how-to-read-the-commands-on-these-pages}

| Vidiš | Znači |
|---|---|
| `<folder>` | rezervirano mjesto: upiši vlastitu vrijednost umjesto toga, bez `< >` |
| `[--force]` | neobavezno: izostavi ili upiši kako je prikazano |
| `a\|b` | izbor: upiši `a` ili `b` |
| `# a note` | komentar za tebe: ne upisuj ga |
| `"C:\My Files\x"` | putanju s razmacima stavi u navodnike |
| `D:\Demos` | primjer Windows foldera: koristi svoj |

## Kad nešto pođe po zlu {#when-something-goes-wrong}

| Poruka | Šta učiniti |
|---|---|
| `'python' is not recognized` | Python nije instaliran ili polje PATH nije označeno: instaliraj ga ponovo i označi ga (ili upiši `py` umjesto `python`). |
| `'heat3d-squad-demo' is not recognized` | Ponovo izvedi korak 4 u folderu alata, ili upiši `python -m heat3d_ext_squad` umjesto `heat3d-squad-demo`: radi isto. |
| `No module named heat3d_ext_squad` | Nisi u folderu alata ili je korak 4 propao: uradi `cd` tamo i izvedi korak 4. |
| `No module named pip` | Pokreni `python -m ensurepip`, zatim korak 4. |
| bilo šta drugo | Pročitaj zadnji red poruke, pa otvori issue na GitHubu s njim. |

Svaka naredba također završava **izlaznim statusom**: 0 znači da je uspjela. Da ga vidiš,
upiši `echo $LASTEXITCODE` u PowerShellu ili `echo $?` na macOS-u i Linuxu.
