---
title: "Ennen aloittamista"
nav_order: 1.5
lang: "fi"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Ennen aloittamista {#before-you-start}

Uusi komentorivin kanssa? Tämä sivu vie sinut nollasta ensimmäiseen ajoon.
Se vie noin kymmenen minuuttia, kerran.

## 1. Asenna Python {#install-python}

Tämä työkalu tarvitsee **Python 3.10:n tai uudemman**.

- **Windows:** lataa Python osoitteesta [python.org/downloads](https://www.python.org/downloads/)
  ja suorita asennusohjelma. Ensimmäisellä näytöllä rastita **Add python.exe to PATH**,
  ja napsauta sitten **Install Now**.
- **macOS ja Linux:** Python 3 on usein jo koneella. Missä nämä sivut sanovat
  `python`, kirjoita `python3`.

## 2. Hae tämä työkalu {#get-this-tool}

Avaa [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), napsauta
vihreää **Code**-painiketta ja sitten **Download ZIP**, ja pura zip haluamaasi kansioon.
Jos käytät gitiä: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Avaa pääte tuon kansion kohdalla {#open-a-terminal-in-that-folder}

Pääte on ikkuna, johon kirjoitat komentoja.

- **Windows:** avaa kansio Resurssienhallinnassa, napsauta osoitepalkkiin, kirjoita
  `powershell` ja paina Enter. Avautuu sininen tai musta ikkuna, joka on jo kyseisessä kansiossa.
- **macOS:** avaa **Terminal**, kirjoita `cd ` (välilyönnin kanssa), vedä kansio
  ikkunaan ja paina Enter.

`cd` tarkoittaa "vaihda kansiota": `cd C:\Tools\3DHeat-Ext-Squad` menee kyseiseen kansioon.

## 4. Asenna työkalu {#install-the-tool}

Kirjoita tämä ja paina Enter:

```bash
python -m pip install -e .
```

Lopussa pitäisi näkyä: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Suorita se {#run-it}

```bash
heat3d-squad-demo --version
```

Pitäisi näkyä jotain tämän kaltaista:

```text
heat3d-squad-demo 0.1.0
```

Seuraavaksi: [Demon tallentaminen](recording.md), sitten [Demojen muuntaminen](converting.md).

## Miten näitä komentoja luetaan {#how-to-read-the-commands-on-these-pages}

| Näet | Se tarkoittaa |
|---|---|
| `<folder>` | paikanpitäjä: kirjoita oma arvosi sen tilalle ilman `< >`-merkkejä |
| `[--force]` | valinnainen: jätä pois tai kirjoita juuri näin |
| `a\|b` | valinta: kirjoita `a` tai `b` |
| `# a note` | kommentti sinulle: älä kirjoita sitä |
| `"C:\My Files\x"` | laita välilyönnillisen polun ympärille lainausmerkit |
| `D:\Demos` | esimerkki Windows-kansiosta: käytä omaasi |

## Kun jokin menee pieleen {#when-something-goes-wrong}

| Viesti | Mitä tehdä |
|---|---|
| `'python' is not recognized` | Python ei ole asennettu, tai PATH-ruutua ei rastitettu: asenna se uudelleen ja rastita ruutu (tai kirjoita `py` komennon `python` sijaan). |
| `'heat3d-squad-demo' is not recognized` | Suorita vaihe 4 uudelleen työkalun kansiossa, tai kirjoita `python -m heat3d_ext_squad` komennon `heat3d-squad-demo` sijaan: se tekee saman. |
| `No module named heat3d_ext_squad` | Olet väärässä kansiossa tai vaihe 4 epäonnistui: `cd` työkalun kansioon ja suorita vaihe 4. |
| `No module named pip` | Suorita `python -m ensurepip`, sitten vaihe 4. |
| muu | Lue viestin viimeinen rivi ja avaa siitä issue GitHubissa. |

Jokainen komento päättyy myös **poistumistilaan**: 0 tarkoittaa, että se onnistui.
Näet sen kirjoittamalla PowerShellissä `echo $LASTEXITCODE` tai macOS:ssa ja Linuxissa `echo $?`.
