---
title: Abans de començar
nav_order: 1.5
lang: ca
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Abans de començar {#before-you-start}

Si és nou amb la línia d'ordres, aquesta pàgina el porta de no tenir res a una primera
execució. Triga uns deu minuts, una sola vegada.

## 1. Instal·lar Python {#install-python}

Aquesta eina necessita **Python 3.10 o posterior**.

- **Windows:** descarregui Python de [python.org/downloads](https://www.python.org/downloads/)
  i executi l'instal·lador. A la primera pantalla, marqui **Add python.exe to PATH**,
  i després faci clic a **Install Now**.
- **macOS i Linux:** sovint Python 3 ja hi és. On aquestes pàgines diuen
  `python`, escrigui `python3`.

## 2. Obtenir aquesta eina {#get-this-tool}

Obri [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), faci clic al
botó verd **Code** i després a **Download ZIP**, i descomprimeixi-la en una carpeta
que triï. Si utilitza git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Obrir una terminal en aquesta carpeta {#open-a-terminal-in-that-folder}

Una terminal és una finestra on escriu ordres.

- **Windows:** obri la carpeta a l'Explorador, faci clic a la barra d'adreces, escrigui
  `powershell` i premi Intro. S'obre una finestra blava o negra, ja situada en
  aquesta carpeta.
- **macOS:** obri **Terminal**, escrigui `cd ` (amb un espai), arrossegui la carpeta
  a la finestra i premi Intro.

`cd` vol dir «canvia de carpeta»: `cd C:\Eines\3DHeat-Ext-Squad` va a aquesta carpeta.

## 4. Instal·lar l'eina {#install-the-tool}

Escrigui això i premi Intro:

```bash
python -m pip install -e .
```

Al final hauria de veure: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Executar-la {#run-it}

```bash
heat3d-squad-demo --version
```

Hauria de veure alguna cosa com:

```text
heat3d-squad-demo 0.1.0
```

Següent: [Gravar una demo](recording.md), i després [Convertir demos](converting.md).

## Com llegir les ordres d'aquestes pàgines {#how-to-read-the-commands-on-these-pages}

| Veu | Vol dir |
|---|---|
| `<carpeta>` | un marcador de posició: escrigui el seu propi valor en lloc seu, sense els `< >` |
| `[--force]` | opcional: deixi-ho estar, o escrigui-ho tal com apareix |
| `a\|b` | una elecció: escrigui `a` o `b` |
| `# una nota` | un comentari per a vostè: no l'escrigui |
| `"C:\Els meus fitxers\x"` | posi entre cometes una ruta que tingui espais |
| `D:\Demos` | una carpeta d'exemple de Windows: utilitzi la seva |

## Quan alguna cosa va malament {#when-something-goes-wrong}

| El missatge | Què cal fer |
|---|---|
| `'python' is not recognized` | Python no està instal·lat, o no es va marcar la casella PATH: instal·li'l de nou i marqui-la (o escrigui `py` en lloc de `python`). |
| `'heat3d-squad-demo' is not recognized` | Torni a fer el pas 4 a la carpeta de l'eina, o escrigui `python -m heat3d_ext_squad` en lloc de `heat3d-squad-demo`: fa el mateix. |
| `No module named heat3d_ext_squad` | No és a la carpeta de l'eina, o el pas 4 ha fallat: feu `cd` fins allà i executi el pas 4. |
| `No module named pip` | Executi `python -m ensurepip`, i després el pas 4. |
| qualsevol altra cosa | Llegeixi l'última línia del missatge i obri una incidència a GitHub amb ella. |

Cada ordre acaba també amb un **estat de sortida**: 0 vol dir que ha funcionat. Per veure'l,
escrigui `echo $LASTEXITCODE` a PowerShell o `echo $?` a macOS i Linux.
