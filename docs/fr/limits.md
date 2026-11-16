---
title: "Limites, mises à jour et conditions"
nav_order: 7
lang: "fr"
source: limits.md
source_hash: "8a9c7c448411"
nav_exclude: true
search_exclude: true
---
# Limites, mises à jour et conditions {#limits-updates-and-terms}

## Non lu {#not-read}

- **Qui a tué qui, et les dégâts infligés à un soldat par impact.** Ces informations voyagent dans les résultats d'impact des appels distants des armes et des états de joueurs (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), dont la structure n'est pas lue ; elles sont gardées en entier dans le fichier annexe des entités. Seule la santé des victimes est décodée.
- **L'équipe d'un bot.** L'état d'un bot porte un nombre qui pourrait être son équipe ; non confirmé, non utilisé.
- **Le regard latéral d'un soldat**, au-delà du lacet du corps.

## Mises à jour du jeu {#game-updates}

Le lecteur dépend du format de réplication du moteur et d'une poignée de noms de classes et de propriétés de Squad. Il ne dépend pas de dispositions de propriétés qu'il ne voit pas : la réplication les nomme elle-même.

**Ce qui peut casser avec une mise à jour de Squad :**

- **Une mise à niveau du moteur.** Squad est passé à UE 5.7 avec la v10.4, et ce n'est pas testé là-bas. La mise à niveau peut changer l'en-tête de bunch, les données d'apparition ou `FRepMovement`. Ceux-ci sont conditionnés par version dans le code là où l'étape est connue. Les étapes inconnues (`ENG_PARTIAL_CUSTOM_EXPORTS`, le bit de mouvement final) sont calées sur le comportement de la v10.3.1.
- **La réplication Iris.** Si Squad passait à Iris, le flux à l'intérieur des blocs serait nouveau et ce lecteur ne le lirait pas. Squad v10.3.1 utilise le système classique (il exécute un ReplicationGraph).
- **Classes ou propriétés renommées.** Si Squad renommait ses classes de joueur, d'équipe ou d'escouade, ou leurs propriétés, les noms ou équipes manqueraient, mais pas les positions.
- **Ce qui se passe en cas d'échec.** Quand le format change, le lecteur échoue bruyamment, avec des erreurs de flux ou de mouvement dans les diagnostics. Il ne produit pas silencieusement de fausses positions : `FRepMovement` n'est accepté que lorsque ses bits tombent juste.

## Données personnelles {#personal-data}

Une démo contient les noms et identifiants en ligne de tous les joueurs du serveur. La table et le document de partie portent des noms, non des identifiants. Les fichiers annexes gardent les bits de chaque propriété, donc les identifiants tels que la démo les contient (non décodés). Traitez-les tous comme la démo elle-même.

## Licence et sources {#licence-and-sources}

MIT ; voir [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Tout a été écrit pour ce paquet. Aucun code tiers n'est inclus ni lié : les seules dépendances sont pyarrow (Apache-2.0) et numpy (BSD-3-Clause).

Les informations sur le format viennent de ces sources :

- **Unreal.Core** dans [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Il décrit la disposition générique des réplications Unreal : le bloc d'information, les blocs, les trames, les bunches et les exports de champs réseau.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Son analyseur a été lu pour la disposition telle que Squad v10.3.1 l'écrit, pour les contrôles de version, et pour savoir quelles classes de Squad portent les données d'effectif. Ses démos de test publiées et ses comptes de référence ont servi de contrôle croisé indépendant. Aucun de son code n'a été copié ni traduit : ce lecteur est structuré autrement (une archive de bits en Python sur des paquets entiers, des bunches partiels réunis bit à bit, des propriétés aiguillées par nom), et deux points qu'il ne traite pas ont été trouvés ici sur les démos elles-mêmes : le troisième drapeau de bunch partiel et le bit de mouvement final.

Ce paquet lit les fichiers de démo qu'écrit un serveur Squad ; il ne touche ni au jeu, ni à son code, ni à ses archives, et rien du jeu n'est inclus ni redistribué. Ce qu'il écrit reste sur votre machine.

3DHeat n'est ni affilié à Offworld Industries ni approuvé par Offworld Industries. Squad ainsi que les noms et marques associés appartiennent à leurs propriétaires.

Ayants droit : ouvrez un ticket sur <https://github.com/Holdi601/3DHeat-Ext-Squad/issues> - nous répondons rapidement et retirons tout ce qui est demandé.
