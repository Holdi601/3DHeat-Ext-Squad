---
title: "La table"
nav_order: 4
lang: fr
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# La table : `<démo>.parquet` {#the-table-parquet}

Une ligne par échantillon ou événement. Un échantillon est pris chaque fois que le serveur a répliqué
le mouvement de l'acteur, jusqu'à 8 fois par seconde (la cadence d'enregistrement de la démo)
pendant qu'il se déplace.

![Les premières lignes de la table d'une démo synthétique](../assets/img/table.svg)

## Colonnes {#columns}

| Colonne | Ce que c'est |
|---|---|
| `time` | secondes depuis le début de l'enregistrement |
| `x`, `y`, `z` | position en unités Unreal (centimètres), Z vers le haut |
| `dirX`, `dirY`, `dirZ` | où regarde un soldat : le lacet du corps et l'inclinaison du regard, sous forme de vecteur unitaire (pour un véhicule : à plat) |
| `yaw`, `pitch` | la même chose en degrés ; `pitch` au-dessus de l'horizon, soldats seulement |
| `health` | la santé du soldat, du bot ou du véhicule à cet instant, quand le serveur l'a envoyée (celle d'un soldat descend sous 0 quand il est blessé) |
| `speed` | la vitesse répliquée, cm/s |
| `player` | le nom du joueur ; `bot <id>` pour un bot ; pour un véhicule ou déployable que personne ne possède, sa classe ; pour un tir d'arme de véhicule, le joueur assis sur ce véhicule |
| `team`, `faction` | le numéro d'équipe de Squad (1, 2) et sa configuration de faction, **à cet instant** : les joueurs peuvent changer de camp |
| `squad` | le numéro d'escouade, -1 quand il n'y en a pas |
| `event` | ce que représente la ligne (ci-dessous) |
| `pawn` | le blueprint du soldat (`SQSquidBot` pour un bot), le véhicule, ou pour `fire` l'arme |
| `seat` | pour un siège de tourelle ou de passager, le pion propre au siège |
| `detail` | pour `fire`, l'appel de l'arme qui a placé le tir ; pour `hit`, le type de dégâts ; pour `removed`, la raison de la fermeture du canal (`Destroyed`, `Dormancy`...) |
| `entity` | l'acteur concerné par la ligne (son GUID réseau) : le `entity` des lignes des fichiers annexes |
| `match` | le nom de la démo |

## Événements {#events}

| `event` | Sur la ligne de | Ce que c'est |
|---|---|---|
| `position` | un soldat ou un bot à pied | un échantillon de mouvement |
| `vehicle` | un soldat dans un véhicule terrestre ou un hélicoptère | un échantillon à la position du véhicule |
| `wounded`, `revived`, `death` | soldats et bots | où cela s'est passé |
| `spawn`, `damaged`, `destroyed`, `removed` | véhicules, déployables, emplacements, caisses, hélicoptères | où ils se trouvaient |
| `seat` | un joueur | a pris un siège |
| `fire` | le tireur | un tir : d'où il est parti, sa direction en `yaw`/`pitch`/`dirX..Z` |
| `hit` | le véhicule | un impact sur véhicule : où |

La manière dont les événements sont lus est expliquée dans [Comment une démo est lue](how-it-works.md#how-the-events-are-read).

## Dans la visionneuse {#in-the-viewer}

Le pied du fichier Parquet contient des consignes de lecture sous la clé `heat3d` : Z vers le haut,
aucun axe miroir, échelle unitaire 1, donc la visionneuse n'a besoin d'aucune correspondance de colonnes. Chargez
la table dans l'onglet Carte de chaleur ; voir [Charger des données](https://holdi601.github.io/3DHeat/getting-data-in.html)
et [Correspondance des colonnes](https://holdi601.github.io/3DHeat/column-mapping.html) de la visionneuse.
