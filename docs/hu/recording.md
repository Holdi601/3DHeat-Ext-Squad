---
title: "Demó felvétele"
nav_order: 2
lang: hu
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Demó felvétele {#recording-a-demo}

A Squad-demókat **a szerveren** rögzítik, nem a játékkliens.

1. A szerver `Admins.cfg` fájljában adja meg az admin csoportjának a `demos` jogosultságot.
2. A játék konzolján futtassa az `AdminDemoRec <name>` parancsot, amikor a meccs elkezdődik.
   Ezt egy adminnak magában a játékban kell begépelnie; egy jelentés szerint az RCON nem fogadja el.
3. Játssza le a meccset, majd futtassa az `AdminDemoStop` parancsot.
4. A demó ide íródik: `<server>/SquadGame/Saved/Demos/<name>.replay`. Másolja le a szerverről arra
   a gépre, amelyen átalakítja.

A `Server.cfg` fájlban van egy `RecordDemos` beállítás is, alapértelmezetten kikapcsolva. Egy kis
meccsnél óránként nagyjából 70-80 MB-ra számítson; egy teljes, 100 játékosos szerver méretét nem mérték meg.

A demó tartalmazza a szerveren lévők mindenkijének nevét és online azonosítóját: kezelje személyes
adatként ([Korlátok, frissítések és feltételek](limits.md#personal-data)).

Következő: [Demók átalakítása](converting.md).
