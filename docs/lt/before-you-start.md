---
title: "Prieš pradedant"
nav_order: 1.5
lang: lt
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Prieš pradedant {#before-you-start}

Nesate įpratę prie komandinės eilutės? Šis puslapis padės nuo nieko iki pirmo paleidimo.
Tai trunka apie dešimt minučių, vieną kartą.

## 1. Įdiekite Python {#install-python}

Šiam įrankiui reikia **Python 3.10 ar naujesnės versijos**.

- **Windows:** atsisiųskite Python iš [python.org/downloads](https://www.python.org/downloads/)
  ir paleiskite diegimo programą. Pirmame ekrane pažymėkite **Add python.exe to PATH**,
  tada spustelėkite **Install Now**.
- **macOS ir Linux:** Python 3 dažniausiai jau įdiegtas. Ten, kur šiuose puslapiuose
  parašyta `python`, rašykite `python3`.

## 2. Gaukite šį įrankį {#get-this-tool}

Atidarykite [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), spustelėkite
žalią mygtuką **Code**, tada **Download ZIP**, ir išskleiskite jį pasirinktame aplanke. Jei naudojate git:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Atidarykite terminalą tame aplanke {#open-a-terminal-in-that-folder}

Terminalas – tai langas, kuriame rašote komandas.

- **Windows:** atidarykite aplanką Explorer, spustelėkite adresų juostą, įrašykite
  `powershell` ir paspauskite Enter. Atsidaro mėlynas ar juodas langas, jau tame aplanke.
- **macOS:** atidarykite **Terminal**, įrašykite `cd ` (su tarpu), įtempkite aplanką
  į langą ir paspauskite Enter.

`cd` reiškia „keisti aplanką“: `cd C:\Tools\3DHeat-Ext-Squad` nueina į tą aplanką.

## 4. Įdiekite įrankį {#install-the-tool}

Įrašykite tai ir paspauskite Enter:

```bash
python -m pip install -e .
```

Pabaigoje turėtumėte pamatyti: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Paleiskite {#run-it}

```bash
heat3d-squad-demo --version
```

Turėtumėte pamatyti maždaug tokį tekstą:

```text
heat3d-squad-demo 0.1.0
```

Toliau: [Demo įrašymas](recording.md), tada [Demo konvertavimas](converting.md).

## Kaip skaityti šiuose puslapiuose esančias komandas {#how-to-read-the-commands-on-these-pages}

| Ką matote | Ką tai reiškia |
|---|---|
| `<folder>` | vietos žymeklis: vietoj jo įrašykite savo reikšmę, be `< >` |
| `[--force]` | neprivaloma: galite jos nerašyti arba įrašyti taip, kaip parodyta |
| `a\|b` | pasirinkimas: įrašykite `a` arba `b` |
| `# a note` | komentaras jums: jo nerašykite |
| `"C:\My Files\x"` | kelią su tarpais įrašykite kabutėse |
| `D:\Demos` | pavyzdinis Windows aplankas: naudokite savo |

## Kai kas nors neveikia {#when-something-goes-wrong}

| Pranešimas | Ką daryti |
|---|---|
| `'python' is not recognized` | Python neįdiegtas arba nepažymėtas langelis PATH: įdiekite iš naujo ir pažymėkite (arba vietoj `python` įrašykite `py`). |
| `'heat3d-squad-demo' is not recognized` | Vykdykite 4 veiksmą dar kartą įrankio aplanke arba įrašykite `python -m heat3d_ext_squad` vietoj `heat3d-squad-demo`: tai daro tą patį. |
| `No module named heat3d_ext_squad` | Nesate įrankio aplanke arba 4 veiksmas nepavyko: nueikite ten su `cd` ir vykdykite 4 veiksmą. |
| `No module named pip` | Vykdykite `python -m ensurepip`, tada 4 veiksmą. |
| bet kas kita | Perskaitykite paskutinę pranešimo eilutę, tada GitHub atidarykite problemą (issue) su ja. |

Kiekviena komanda baigiasi **išeities kodu**: 0 reiškia, kad pavyko. Jį pamatysite įrašę
`echo $LASTEXITCODE` PowerShell arba `echo $?` macOS ir Linux.
