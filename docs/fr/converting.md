---
title: "Convertir les démos"
nav_order: 3
lang: "fr"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Convertir les démos {#converting-demos}

```text
heat3d-squad-demo <démos ou dossiers> -o <dossier> [--flat] [--json]
python -m heat3d_ext_squad ...          la même chose, sans installer
```

## Pas à pas {#step-by-step}

Vous débutez avec la ligne de commande ? Lisez d'abord [Avant de commencer](before-you-start.md).

1. Installez une fois : `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   ouvrez un terminal dans ce dossier, puis lancez `python -m pip install -e .`
   (Python 3.10 ou plus récent ; cela installe pyarrow et numpy).
2. Placez les fichiers `.replay` dans un dossier, ou indiquez-les un par un.
3. Lancez `heat3d-squad-demo <dossier> -o out`.
4. Vous devez voir une ligne par démo : sa couche, ses joueurs et ses lignes, et
   l'endroit où la table a été écrite. Chaque démo devient quatre fichiers séparés dans
   `out/<carte>/` (et non un conteneur `.3dheat`) ; chargez le `.parquet` dans
   le visualiseur 3DHeat.

![Une conversion sur une démo synthétique](../assets/img/run.svg)

L'image montre une conversion sur une démo que créent les tests (`tests/test_stream.py`),
et non sur une vraie partie.

## Options {#options}

| Option | Par défaut | Effet |
|---|---|---|
| `demos` (une ou plusieurs) | - | des fichiers `.replay`, ou des dossiers qui les contiennent |
| `-o`, `--out` | obligatoire | le dossier où écrire ; chaque démo va dans `<out>/<carte>/` |
| `--flat` | désactivé | écrit directement dans le dossier, sans le sous-dossier `<carte>/` |
| `--json` | désactivé | affiche sur la sortie standard une ligne de JSON par démo (pour les programmes qui appellent la commande) : `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix` ; une démo en échec affiche `demo`, `ok: false` et `error` à la place |
| `--version` | - | affiche la version et s'arrête |

Chaque option, telle que le programme l'affiche : [Référence des commandes](../cli-reference.md).

Le dossier de la carte porte le nom de la carte, tiré du chemin de niveau que nomme la démo
(`/Game/Maps/<Carte>/Gameplay_Layers/<Couche>` donne `<Carte>`).

Code de sortie : 0 quand toutes les démos ont été converties ; 1 quand l'une a échoué
(les autres sont tout de même écrites) ou quand aucun fichier `.replay` n'a été trouvé.

## Ce qui sort {#what-comes-out}

| Fichier | Ce qu'il contient |
|---|---|
| `<démo>.parquet` | la table : positions et événements, une ligne chacun ([La table](output-table.md)) |
| `<démo>.match.json` | le document de partie ([Le document de partie](output-match.md)) |
| `<démo>.entities.parquet` | fichier annexe : chaque mise à jour de propriété et chaque appel distant, en entier |
| `<démo>.packets.parquet` | fichier annexe : les blocs du fichier et tout ce qui n'a pas pu être lu, en entier |

La table et le document de partie forment la même paire que celle qu'écrit l'outil 3DHeat CS2.
Le visualiseur ouvre la table directement, et laisse les fichiers annexes de côté
lorsqu'un dossier entier est chargé.

## Exemples {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # toutes les démos d'un dossier
heat3d-squad-demo un.replay deux.replay -o out --flat  # directement dans out/
heat3d-squad-demo D:\SquadDemos -o out --json          # une ligne JSON par démo
```

`D:\SquadDemos` est un exemple de dossier sur le disque D : utilisez le vôtre.
