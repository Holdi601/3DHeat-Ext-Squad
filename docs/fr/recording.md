---
title: "Enregistrer une démo"
nav_order: 2
lang: "fr"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Enregistrer une démo {#recording-a-demo}

Les démos Squad sont enregistrées **sur le serveur**, et non par le client de jeu.

1. Dans le fichier `Admins.cfg` du serveur, donnez au groupe de l'admin la
   permission `demos`.
2. Dans la console du jeu, tapez `AdminDemoRec <nom>` au début de la partie.
   Un admin doit taper cette commande dans le jeu lui-même ; un signalement dit que RCON
   ne l'accepte pas.
3. Jouez la partie, puis tapez `AdminDemoStop`.
4. La démo est écrite dans `<serveur>/SquadGame/Saved/Demos/<nom>.replay`.
   Copiez-la depuis le serveur vers l'ordinateur qui la convertit.

`Server.cfg` contient aussi un réglage `RecordDemos`, désactivé par défaut. Comptez
environ 70 à 80 Mo par heure pour une petite partie ; la taille d'un serveur complet
de 100 joueurs n'a pas été mesurée.

Une démo contient les noms et les identifiants en ligne de tous les joueurs du serveur :
traitez-la comme une donnée personnelle ([Limites, mises à jour et conditions](limits.md#personal-data)).

Suite : [Convertir les démos](converting.md).
