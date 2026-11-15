---
title: "Grenzen, Updates und Bedingungen"
nav_order: 7
lang: "de"
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Grenzen, Updates und Bedingungen {#limits-updates-and-terms}

## Nicht gelesen {#not-read}

- **Wer wen getötet hat, und Schaden an Soldaten pro Treffer.** Diese laufen in den Trefferergebnissen der
  Remote-Aufrufe der Waffen und Spielerzustände (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), deren Aufbau nicht
  gelesen wird; sie werden ganz in der Begleitdatei der Entitäten behalten. Nur die Gesundheit der Opfer wird dekodiert.
- **Das Team des Bots.** Der Zustand eines Bots enthält eine Zahl, die sein Team sein könnte; nicht bestätigt, nicht verwendet.
- **Wo ein Soldat seitlich schaut**, über den Gierwinkel des Körpers hinaus.

## Spiel-Updates {#game-updates}

Der Leser hängt vom Replay-Format der Engine und von einer Handvoll Klassen- und Eigenschaftsnamen von Squad ab.
Er hängt nicht von Eigenschafts-Layouts ab, die er nicht sehen kann: Die Replay-Datei benennt sie selbst.

**Was bei einem Squad-Update kaputtgehen kann:**

- **Ein Engine-Upgrade.** Squad ist mit v10.4 auf UE 5.7 umgestiegen, und das ist dort ungetestet. Das Upgrade kann
  den Bunch-Header, die Erzeugungsdaten oder `FRepMovement` ändern. Diese sind im Code versionsabhängig, wo der Schritt
  bekannt ist. Unbekannte Schritte (`ENG_PARTIAL_CUSTOM_EXPORTS`, das abschließende Bewegungsbit) sind auf das festgelegt,
  was v10.3.1 tut.
- **Iris-Replikation.** Wenn Squad auf Iris umgestellt hätte, wäre der Stream in den Chunks neu, und dieser Leser
  würde ihn nicht lesen. Squad v10.3.1 nutzt das klassische System (es läuft mit ReplicationGraph).
- **Umbenannte Klassen oder Eigenschaften.** Würde Squad seine Spieler-, Team- oder Squad-Klassen oder deren
  Eigenschaften umbenennen, würden Namen oder Teams fehlen, die Positionen aber nicht.
- **Was bei einem Fehler geschieht.** Ändert sich das Format, bricht der Leser laut ab, mit Stream- oder
  Bewegungsfehlern in der Diagnose. Er erzeugt nicht stillschweigend falsche Positionen: `FRepMovement` wird nur
  angenommen, wenn seine Bits genau aufgehen.

## Persönliche Daten {#personal-data}

Eine Demo enthält die Namen und Online-IDs aller auf dem Server. Die Tabelle und das Match-Dokument enthalten Namen,
keine IDs. Die Begleitdateien behalten alle Bits jeder Eigenschaft, also auch die IDs, so wie die Demo sie enthält
(nicht dekodiert). Behandle alle wie die Demo selbst.

## Lizenz und Quellen {#licence-and-sources}

MIT; siehe [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Alles hier wurde für dieses Paket
geschrieben. Kein fremder Code ist enthalten oder verlinkt: die einzigen Abhängigkeiten sind pyarrow (Apache-2.0)
und numpy (BSD-3-Clause).

Die Fakten über das Format stammen aus diesen Quellen:

- **Unreal.Core** in [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Es beschreibt
  den allgemeinen Unreal-Replay-Aufbau: den Infoblock, Chunks, Frames, Bündel und Net-Field-Exporte.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Dessen Parser wurde für den Aufbau gelesen,
  wie Squad v10.3.1 ihn schreibt, für die Versionsprüfungen und dafür, welche Squad-Klassen Kaderdaten tragen.
  Seine veröffentlichten Test-Demos und Zählwerte dienten als unabhängige Gegenprüfung. Kein Code davon wurde kopiert
  oder übersetzt: dieser Leser ist anders aufgebaut (ein Python-Bit-Archiv über ganze Pakete, geteilte Bündel bitweise
  zusammengefügt, Eigenschaften nach Namen zugeordnet), und zwei Dinge, die er nicht tut, wurden hier an den Demos
  selbst gefunden: das dritte Flag für geteilte Bündel und das abschließende Bewegungsbit.

Squad ist eine Marke von Offworld Industries. Dieses Paket liest Dateien, die ein Squad-Server schreibt; es greift
nicht in das Spiel, dessen Code oder Archive ein. Die Server-Lizenzierungs- und Verwaltungsrichtlinien von Offworld
sagen nichts über das Aufzeichnen oder Auswerten von Demos. Squads EULA verbietet das Reverse Engineering des Spiels
selbst, was dieses Paket nicht tut.
