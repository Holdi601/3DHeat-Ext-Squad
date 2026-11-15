---
title: Registrare una demo
nav_order: 2
lang: "it"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Registrare una demo {#recording-a-demo}

Le demo di Squad si registrano **sul server**, non dal client di gioco.

1. Nel file `Admins.cfg` del server, dai al gruppo degli amministratori il permesso `demos`.
2. Nella console del gioco, esegui `AdminDemoRec <nome>` quando la partita inizia.
   L'amministratore deve digitarlo nel gioco stesso; una segnalazione dice che RCON non lo accetta.
3. Gioca la partita, poi esegui `AdminDemoStop`.
4. La demo viene scritta in `<server>/SquadGame/Saved/Demos/<nome>.replay`.
   Copiala dal server sul computer che la converte.

`Server.cfg` contiene anche un'impostazione `RecordDemos`, disattivata per impostazione predefinita.
Aspettati circa 70-80 MB per ora per una partita piccola; la dimensione per un server completo
da 100 giocatori non è stata misurata.

Una demo contiene i nomi e gli ID online di tutti i presenti sul server: trattala come dato
personale ([Limiti, aggiornamenti e condizioni](limits.md#personal-data)).

Poi: [Convertire le demo](converting.md).
