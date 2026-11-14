---
title: Recording a demo
nav_order: 2
---

# Recording a demo

Squad demos are recorded **on the server**, not by the game client.

1. In the server's `Admins.cfg`, give the admin's group the `demos`
   permission.
2. In the game's console, run `AdminDemoRec <name>` when the match starts.
   An admin has to type this in the game itself; one report says RCON does
   not accept it.
3. Play the match, then run `AdminDemoStop`.
4. The demo is written to `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Copy it off the server to the machine that converts it.

`Server.cfg` also has a `RecordDemos` setting, off by default. Expect roughly
70 to 80 MB per hour for a small match; the size for a full 100-player server
has not been measured.

A demo holds the names and online ids of everyone on the server: treat it as
personal data ([Limits, updates and terms](limits.md#personal-data)).

Next: [Converting demos](converting.md).
