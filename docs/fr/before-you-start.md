---
title: "Avant de commencer"
nav_order: 1.5
lang: "fr"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# Avant de commencer {#before-you-start}

Vous débutez avec la ligne de commande ? Cette page vous mène de zéro à un premier essai.
Cela prend une dizaine de minutes, une seule fois.

## 1. Installer Python {#install-python}

Cet outil demande **Python 3.10 ou plus récent**.

- **Windows :** téléchargez Python sur [python.org/downloads](https://www.python.org/downloads/)
  et lancez l'installeur. Sur son premier écran, cochez **Add python.exe to PATH**,
  puis cliquez sur **Install Now**.
- **macOS et Linux :** Python 3 est souvent déjà là. Là où ces pages écrivent
  `python`, tapez `python3`.

## 2. Récupérer cet outil {#get-this-tool}

Ouvrez [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad), cliquez sur le
bouton vert **Code**, puis sur **Download ZIP**, et décompressez-le dans un dossier de
votre choix. Si vous utilisez git : `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`.

## 3. Ouvrir un terminal dans ce dossier {#open-a-terminal-in-that-folder}

Un terminal est une fenêtre dans laquelle vous tapez des commandes.

- **Windows :** ouvrez le dossier dans l'Explorateur, cliquez dans la barre d'adresse,
  tapez `powershell` et appuyez sur Entrée. Une fenêtre bleue ou noire s'ouvre,
  déjà dans ce dossier.
- **macOS :** ouvrez **Terminal**, tapez `cd ` (avec un espace), glissez le dossier
  dans la fenêtre et appuyez sur Entrée.

`cd` signifie « changer de dossier » : `cd C:\Outils\3DHeat-Ext-Squad` va dans ce dossier.

## 4. Installer l'outil {#install-the-tool}

Tapez ceci et appuyez sur Entrée :

```bash
python -m pip install -e .
```

Vous devez voir, à la fin : `Successfully installed heat3d-ext-squad-demo-...`.

## 5. Lancer l'outil {#run-it}

```bash
heat3d-squad-demo --version
```

Vous devez voir quelque chose comme :

```text
heat3d-squad-demo 0.1.0
```

Suite : [Enregistrer une démo](recording.md), puis [Convertir les démos](converting.md).

## Comment lire les commandes de ces pages {#how-to-read-the-commands-on-these-pages}

| Vous voyez | Cela signifie |
|---|---|
| `<dossier>` | un espace réservé : tapez votre propre valeur à la place, sans les `< >` |
| `[--force]` | facultatif : omettez-le, ou tapez-le tel quel |
| `a\|b` | un choix : tapez `a` ou `b` |
| `# une remarque` | un commentaire pour vous : ne le tapez pas |
| `"C:\Mes Fichiers\x"` | mettez entre guillemets un chemin qui contient des espaces |
| `D:\Demos` | un exemple de dossier Windows : utilisez le vôtre |

## Quand quelque chose ne va pas {#when-something-goes-wrong}

| Le message | Que faire |
|---|---|
| `'python' is not recognized` | Python n'est pas installé, ou la case PATH n'était pas cochée : installez-le à nouveau et cochez-la (ou tapez `py` au lieu de `python`). |
| `'heat3d-squad-demo' is not recognized` | Relancez l'étape 4 dans le dossier de l'outil, ou tapez `python -m heat3d_ext_squad` à la place de `heat3d-squad-demo` : cela fait la même chose. |
| `No module named heat3d_ext_squad` | Vous n'êtes pas dans le dossier de l'outil, ou l'étape 4 a échoué : faites `cd` jusque-là et relancez l'étape 4. |
| `No module named pip` | Lancez `python -m ensurepip`, puis l'étape 4. |
| autre chose | Lisez la dernière ligne du message, puis ouvrez un ticket sur GitHub avec cette ligne. |

Chaque commande se termine aussi par un **code de sortie** : 0 signifie que cela a réussi. Pour le voir,
tapez `echo $LASTEXITCODE` dans PowerShell, ou `echo $?` sur macOS et Linux.
