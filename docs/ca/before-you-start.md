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

Si ets nou amb la línia d'ordres, aquesta pàgina et porta des de no tenir res fins a una primera
execució. Triga uns deu minuts, una sola vegada.

## 1. Instal·lar Python {#install-python}

Aquesta eina necessita **Python 3.10 o posterior**.

- **Windows:** descarrega Python de [python.org/downloads](https://www.python.org/downloads/)
  i executa l'instal·lador. A la primera pantalla, marca **Add python.exe to PATH**,
  i després fes clic a **Install Now**.
- **macOS i Linux:** sovint Python 3 ja hi és. On aquestes pàgines diuen
  `python`, escriu `python3`.

## 2. Obtenir aquesta eina {#get-this-tool}

Obre [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), fes clic al
botó verd **Code** i després a **Download ZIP**, i descomprimeix-la en una carpeta
que triïs. Si uses git: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Obrir una terminal en aquesta carpeta {#open-a-terminal-in-that-folder}

Una terminal és una finestra on escrius ordres.

- **Windows:** obre la carpeta a l'Explorador, fes clic a la barra d'adreces, escriu
  `powershell` i prem Intro. S'obre una finestra blava o negra, ja situada en
  aquesta carpeta.
- **macOS:** obre **Terminal**, escriu `cd ` (amb un espai), arrossega la carpeta
  a la finestra i prem Intro.

`cd` vol dir «canvia de carpeta»: `cd C:\Eines\3DHeat-Ext-Squad` va a aquesta carpeta.

## 4. Instal·lar l'eina {#install-the-tool}

Escriu això i prem Intro:

```bash
python -m pip install -e .
```

Al final hauries de veure: `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Executar-la {#run-it}

```bash
heat3d-squad-demo --version
```

Hauries de veure alguna cosa com:

```text
heat3d-squad-demo 0.1.0
```

Següent: [Gravar una demo](recording.md), i després [Convertir demos](converting.md).

## Com llegir les ordres d'aquestes pàgines {#how-to-read-the-commands-on-these-pages}

| Veu | Vol dir |
|---|---|
| `<carpeta>` | un marcador de posició: escriu el teu propi valor en lloc seu, sense els `< >` |
| `[--force]` | opcional: deixa-ho estar, o escriu-ho tal com apareix |
| `a\|b` | una elecció: escriu `a` o `b` |
| `# una nota` | un comentari per a tu: no l'escriguis |
| `"C:\Els meus fitxers\x"` | posa entre cometes una ruta que tingui espais |
| `D:\Demos` | una carpeta d'exemple de Windows: fes servir la teva |

## Quan alguna cosa va malament {#when-something-goes-wrong}

| El missatge | Què cal fer |
|---|---|
| `'python' is not recognized` | Python no està instal·lat, o no es va marcar la casella PATH: instal·la'l de nou i marca-la (o escriu `py` en lloc de `python`). |
| `'heat3d-squad-demo' is not recognized` | Torna a fer el pas 4 a la carpeta de l'eina, o escriu `python -m heat3d_ext_squad` en lloc de `heat3d-squad-demo`: fa el mateix. |
| `No module named heat3d_ext_squad` | No ets a la carpeta de l'eina, o el pas 4 ha fallat: fes `cd` fins allà i executa el pas 4. |
| `No module named pip` | Executa `python -m ensurepip`, i després el pas 4. |
| qualsevol altra cosa | Llegeix l'última línia del missatge i obre una incidència a GitHub amb ella. |

Cada ordre acaba també amb un **estat de sortida**: 0 vol dir que ha funcionat. Per veure'l,
escriu `echo $LASTEXITCODE` a PowerShell o `echo $?` a macOS i Linux.
