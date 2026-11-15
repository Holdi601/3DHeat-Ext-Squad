---
title: "Eine Demo aufnehmen"
nav_order: 2
lang: de
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Eine Demo aufnehmen {#recording-a-demo}

Squad-Demos werden **auf dem Server** aufgenommen, nicht vom Spiel-Client.

1. In der `Admins.cfg` des Servers gibst du der Gruppe des Admins die Berechtigung `demos`.
2. In der Konsole des Spiels führst du `AdminDemoRec <name>` aus, wenn das Match beginnt.
   Ein Admin muss das im Spiel selbst eintippen; ein Bericht sagt, dass RCON es nicht annimmt.
3. Spiele das Match, dann führe `AdminDemoStop` aus.
4. Die Demo wird nach `<server>/SquadGame/Saved/Demos/<name>.replay` geschrieben.
   Kopiere sie vom Server auf den Rechner, der sie umwandelt.

`Server.cfg` hat außerdem eine Einstellung `RecordDemos`, standardmäßig aus. Rechne mit etwa
70 bis 80 MB pro Stunde bei einem kleinen Match; die Größe für einen vollen 100-Spieler-Server
wurde nicht gemessen.

Eine Demo enthält die Namen und Online-IDs aller auf dem Server: Behandle sie als persönliche Daten
([Grenzen, Updates und Bedingungen](limits.md#personal-data)).

Weiter: [Demos umwandeln](converting.md).
