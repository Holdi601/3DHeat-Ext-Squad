---
title: "Enne alustamist"
nav_order: 1.5
lang: et
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Enne alustamist {#before-you-start}

Pole sul käsurealt kogemust? See leht viib sind nullist esimese käivituseni.
See võtab umbes kümme minutit, ainult üks kord.

## 1. Paigalda Python {#install-python}

See tööriist vajab **Python 3.10 või uuemat**.

- **Windows:** laadi Python alla lehelt [python.org/downloads](https://www.python.org/downloads/)
  ja käivita installer. Selle esimesel ekraanil märgi **Add python.exe to PATH**,
  seejärel klõpsa **Install Now**.
- **macOS ja Linux:** Python 3 on sageli juba olemas. Kus need lehed ütlevad
  `python`, kirjuta `python3`.

## 2. Hangi see tööriist {#get-this-tool}

Ava [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), klõpsa
roheline nupp **Code**, seejärel **Download ZIP**, ja paki see lahti kausta, mille valid. Kui kasutad gitti:
`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Ava terminal selles kaustas {#open-a-terminal-in-that-folder}

Terminal on aken, kuhu kirjutad käske.

- **Windows:** ava kaust Exploreris, klõpsa aadressiribale, kirjuta
  `powershell` ja vajuta Enter. Avaneb sinine või must aken, mis on juba selles
  kaustas.
- **macOS:** ava **Terminal**, kirjuta `cd ` (tühikuga), lohista kaust
  aknasse ja vajuta Enter.

`cd` tähendab "vaheta kausta": `cd C:\Tools\3DHeat-Ext-Squad` viib sellesse kausta.

## 4. Paigalda tööriist {#install-the-tool}

Kirjuta see ja vajuta Enter:

```bash
python -m pip install -e .
```

Lõpus peaks näha: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Käivita see {#run-it}

```bash
heat3d-squad-demo --version
```

Peaksid nägema midagi sellist:

```text
heat3d-squad-demo 0.1.0
```

Edasi: [Demo salvestamine](recording.md), seejärel [Demode teisendamine](converting.md).

## Kuidas neid käske nendel lehtedel lugeda {#how-to-read-the-commands-on-these-pages}

| Näed | See tähendab |
|---|---|
| `<folder>` | kohatäide: kirjuta selle asemel oma väärtus, ilma `< >` märkideta |
| `[--force]` | valikuline: jäta välja või kirjuta täpselt nii, nagu on näidatud |
| `a\|b` | valik: kirjuta `a` või `b` |
| `# a note` | kommentaar sulle: ära kirjuta seda |
| `"C:\My Files\x"` | aseta tühikuid sisaldav tee jutumärkidesse |
| `D:\Demos` | näidis-Windowsi kaust: kasuta oma |

## Kui midagi läheb valesti {#when-something-goes-wrong}

| Teade | Mida teha |
|---|---|
| `'python' is not recognized` | Python pole paigaldatud või PATH-kasti ei märgitud: paigalda uuesti ja märgi see (või kirjuta `python` asemel `py`). |
| `'heat3d-squad-demo' is not recognized` | Käivita samm 4 uuesti tööriista kaustas või kirjuta `heat3d-squad-demo` asemel `python -m heat3d_ext_squad`: see teeb sama. |
| `No module named heat3d_ext_squad` | Sa ei ole tööriista kaustas või samm 4 ebaõnnestus: liigu sinna `cd`-ga ja käivita samm 4. |
| `No module named pip` | Käivita `python -m ensurepip`, seejärel samm 4. |
| muu | Loe teate viimast rida ja ava GitHubis probleem, lisades selle rea. |

Iga käsk lõpeb ka **väljumisolekuga**: 0 tähendab, et see töötas. Selle nägemiseks
kirjuta PowerShellis `echo $LASTEXITCODE` või macOS-is ja Linuxis `echo $?`.
