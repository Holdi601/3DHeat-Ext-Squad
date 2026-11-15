---
title: "Le document de match et les fichiers annexes"
nav_order: 5
lang: fr
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Le document de match et les fichiers annexes {#the-match-document-and-sidecars}

À côté de la table, chaque démo produit `<démo>.match.json` et deux fichiers annexes,
`<démo>.entities.parquet` et `<démo>.packets.parquet`. La visionneuse lit le
document de match dans son onglet Match.

## Le document de match {#the-match-document}

`<démo>.match.json` (le document de match) contient au premier niveau `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` et `selfCheck` (la liste complète : [Référence des commandes](../cli-reference.md)). En clair : la carte et la couche, les versions du jeu et du moteur, l'heure d'enregistrement, la durée, et :

- **les équipes** : numéro, faction et tout ce que leur état a transmis (tickets, disponibilités, commandant), au fil des changements ;
- **les escouades** : numéro, équipe, nom, créateur, chef, membres ;
- **l'état de la partie** : nom et réglages du serveur, mode de jeu, état et identifiant de la partie, rotations de cartes et de couches, votes, minuteurs, message du jour ;
- **les acteurs** : chaque véhicule, déployable, emplacement, caisse de munitions et hélicoptère - classe, lieu et moment d'apparition, moment de disparition, propriétaire, et leur état transmis (santé, état de construction, sièges...) ;
- **une ligne par joueur** : positions à pied et dans les véhicules, distance parcourue, classes de soldat jouées, véhicules utilisés, changements d'équipe, sièges occupés, et tout ce que l'état du joueur a transmis (ping, niveau, rôle, siège actuel...) ; et une ligne par bot ;
- **les événements** comptés, le **recensement des propriétés** (combien de fois les propriétés de chaque classe ont été envoyées) et le **recensement des appels distants**, les tirs et impacts, ce qui n'a **pas** été lu, et les diagnostics du lecteur ;
- **le fichier et l'en-tête** : chaque champ du bloc d'information et de l'en-tête de la démo, la table des blocs, les tables d'export des champs réseau (`net_field_exports`), les raisons de fermeture des canaux, et les classes trouvées pour les objets que les exports ne nomment pas (`stream.class_resolution`) ;
- **la vérification** (`selfCheck.completeness`, voir [Vérification](#verification)).

Les identifiants en ligne (Steam, EOS) sont volontairement omis.

Un coup d'œil rapide sur une démo convertie :

```bash
python -c "import json; d = json.load(open('out/<carte>/<démo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Vérification {#completeness}

Ce lecteur suit la règle que partagent tous les convertisseurs 3DHeat : décoder ce qui peut être lu
maintenant, garder le reste en entier, et dire combien de chaque sorte il a traité ([Les convertisseurs gardent tout](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Chaque document de match
contient `selfCheck.completeness` : pour chaque type d'élément rencontré dans la démo, le nombre `seen` (vus),
`decoded` (décodés), `partial` (décodés en partie et gardés en entier), `raw` (gardés en entier seulement) et `lost`
(perdus, qui doit valoir 0). Les types sont comptés là où le lecteur les rencontre : `file.info`, `chunk.<genre>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<classe>`, `rpc:<classe>`, `block:<objet>`, `subobject.*`.

Sur les vraies démos lues, `lost` vaut 0 : leurs éléments vont de quelques centaines de milliers à plusieurs millions ; environ la moitié se décodent entièrement, le reste est partiel ou brut.

**Lu** (dans la table et le document de match) :

- le bloc d'information, l'en-tête de la démo (chaque champ ; deux octets de fin non identifiés sont gardés en hexadécimal), la table des blocs ;
- chaque trame, paquet et bunch (découpés entiers en ce qu'ils contiennent), chaque acteur ouvert (avec son lieu d'apparition, sa rotation, son échelle et sa vitesse) et fermé (avec la raison : `Destroyed`, `Dormancy`...) ;
- chaque propriété répliquée, dans la mesure où ses bits l'indiquent ([Décodage des propriétés](how-it-works.md#decodage-des-proprietes)), positions issues de `FRepMovement` et du composant de mouvement des hélicoptères, les blessures, la santé des véhicules, les sièges ;
- chaque appel distant par son nom, avec ses paramètres lorsque la démo exporte le groupe de la fonction : tirs (`fire`) et impacts sur véhicules (`hit`) dans la table ;
- les tables d'export des champs réseau et les GUID réseau (leur nombre ; les chemins sont dans le fichier annexe des entités).

**Gardé brut** (en entier, avec ce qui en est lu à côté) :

- `<démo>.entities.parquet`, colonnes `time`, `type` (`<classe>.<propriété>`, `<classe>.<appel>`, ou le nom de l'objet), `name` (la classe de l'acteur), `entity` (le GUID réseau de l'acteur, comme la colonne `entity` de la table), `kind`, `object` (le sous-objet), `channel`, `handle`, `group` (le chemin de classe du groupe d'export), `decoded` (JSON), `bits` et `payload` (les bits, du moins significatif, complétés à l'octet) :
  - chaque mise à jour de propriété (`kind` `property`), mouvement compris, avec ce qui est décodé ; brut seulement là où rien ne l'est (poignées sans nom, structures comme `RotationReplicatedMovement` des tourelles, et propriétés laissées en bits) ;
  - chaque appel distant et chaque champ de delta personnalisé (`rpc`), les paramètres décodés quand le groupe de la fonction a été exporté ; brut sinon (`RepInventory`, `PlayerStateData`) ;
  - chaque bloc de contenu d'un objet dont la classe n'a pas pu être trouvée (`block` : `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), avec son en-tête décodé ;
  - chaque canal d'acteur ouvert et fermé (`open`, `close`), chaque sous-objet supprimé ou détruit ;
  - le contexte dont un décodeur ultérieur a besoin pour lire le fichier seul : chaque export de champ réseau (`export.field` : chemin de groupe, poignée, nom de propriété, somme de contrôle) et chaque GUID réseau exporté (`export.guid` : son chemin, son parent et ses drapeaux), au moment où le flux les a donnés.
- `<démo>.packets.parquet`, colonnes `time`, `type`, `name`, `channel`, `offset` (dans le fichier), `decoded`, `bits`, `payload` : le bloc d'information, le bloc d'en-tête, chaque bloc de point de contrôle (un point de contrôle est l'état de chaque acteur à cet instant, que le flux depuis le début contient aussi), chaque bloc d'événement, et chaque trame, paquet ou bunch qui ne se lit pas (un bunch par démo : le bunch d'ouverture de l'acteur spectateur de l'enregistreur), en entier.

Les lignes des entités sont regroupées par `kind`, `type` et `entity`, chacune dans l'ordre du temps ; triez par `time` pour l'ordre du flux.

**Non disponible :**

- ce qu'une démo de serveur n'enregistre pas : les commandes des clients, ce que le joueur voyait ;
- les effets côté client : marqueurs de touche, sons, texte du journal des éliminations (le serveur envoie les appels, pas leur affichage) ;
- les identifiants en ligne décodés : gardés seulement en bits (voir [Données personnelles](limits.md#donnees-personnelles)).
