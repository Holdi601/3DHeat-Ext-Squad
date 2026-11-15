---
title: Gravar una demo
nav_order: 2
lang: "ca"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Gravar una demo {#recording-a-demo}

Les demos de Squad es graven **al servidor**, no pel client del joc.

1. Al fitxer `Admins.cfg` del servidor, dona al grup de l'administrador el permís
   `demos`.
2. A la consola del joc, executa `AdminDemoRec <nom>` quan comenci la partida.
   Un administrador ho ha d'escriure al mateix joc; un informe diu que RCON no ho
   accepta.
3. Juga la partida i després executa `AdminDemoStop`.
4. La demo s'escriu a `<servidor>/SquadGame/Saved/Demos/<nom>.replay`.
   Copia-la del servidor a l'ordinador que la converteix.

`Server.cfg` també té una opció `RecordDemos`, desactivada per defecte. Compta amb
uns 70 a 80 MB per hora per a una partida petita; la mida d'un servidor complet
de 100 jugadors no s'ha mesurat.

Una demo conté els noms i els identificadors en línia de tots els del servidor: tracta-la
com a dada personal ([Límits, actualitzacions i condicions](limits.md#personal-data)).

Següent: [Convertir demos](converting.md).
