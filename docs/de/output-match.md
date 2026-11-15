---
title: "Das Match-Dokument und die Begleitdateien"
nav_order: 5
lang: "de"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Das Match-Dokument und die Begleitdateien {#the-match-document-and-sidecars}

Neben der Tabelle bekommt jede Demo `<demo>.match.json` und zwei Begleitdateien,
`<demo>.entities.parquet` und `<demo>.packets.parquet`. Der Viewer liest das Match-Dokument im Match-Reiter.

## Das Match-Dokument {#the-match-document}

`<demo>.match.json` (das Match-Dokument) enthält auf oberster Ebene `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` und `selfCheck` (die vollständige Liste: [Befehlsreferenz](../cli-reference.md)). Mit Worten: die Map und die Schicht, die Spiel- und Engine-Versionen, die Aufnahmezeit, die Länge, und:

- **die Teams**: Nummer, Fraktion und alles, was ihr Zustand repliziert hat (Tickets, Verfügbarkeiten, Kommandant), wie es sich änderte;
- **die Squads**: Nummer, Team, Name, Gründer, Anführer, Mitglieder;
- **der Spielzustand**: Servername und Einstellungen, Spielmodus, Matchstatus und -id, Map- und Schicht-Rotationen, Abstimmungen, Timer, die Tagesnachricht;
- **die Akteure**: jedes Fahrzeug, jeder Verbrauchsgegenstand, jedes Geschütz, jede Munitionskiste und jeder Helikopter - Klasse, Ort und Zeit der Erzeugung, wann er verschwand, wem er gehörte, und sein replizierter Zustand (Gesundheit, Bauzustand, Sitze...);
- **eine Zeile für jeden Spieler**: Proben zu Fuß und in Fahrzeugen, zurückgelegte Strecke, gespielte Soldatenklassen, benutzte Fahrzeuge, Teamwechsel, eingenommene Sitze und alles, was der Spielerzustand repliziert hat (Ping, Level, Rolle, aktueller Sitz...); und eine Zeile für jeden Bot;
- **die Ereignisse** gezählt, die **Eigenschafts-Zählung** (wie oft die Eigenschaften jeder Klasse gesendet wurden) und die **Zählung der Remote-Aufrufe**, die Schüsse und Treffer, was **nicht** gelesen wurde, und die Diagnose des Lesers;
- **die Datei und der Header**: jedes Feld des Infoblocks und des Demo-Headers, die Chunk-Tabelle, die Net-Field-Exporttabellen (`net_field_exports`), die Schließgründe der Kanäle und die Klassen, die für Objekte gefunden wurden, die die Exporte nicht benennen (`stream.class_resolution`);
- **die Selbstprüfung** (`selfCheck.completeness`, siehe [Vollständigkeit](#completeness)).

Online-IDs (Steam, EOS) sind absichtlich weggelassen.

Ein kurzer Blick auf eine umgewandelte Demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Vollständigkeit {#completeness}

Dieser Leser folgt der Regel, die alle 3DHeat-Konverter teilen: jetzt dekodieren, was sich lesen lässt, den Rest ganz behalten und sagen, wie viel von jeder Art er gelesen hat ([Konverter behalten alles](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Jedes Match-Dokument hat `selfCheck.completeness`: pro Art von Element, das in der Demo angetroffen wurde, wie viele `seen` (gesehen), `decoded` (dekodiert), `partial` (teilweise dekodiert und ganz behalten), `raw` (nur ganz behalten) und `lost` (verloren, muss 0 sein) sind. Die Arten werden dort gezählt, wo der Leser sie antrifft: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Bei den echten gelesenen Demos ist `lost` 0: ihre Elemente laufen von hunderttausenden bis zu Millionen; etwa die Hälfte wird vollständig dekodiert, der Rest ist teilweise oder roh.

**Gelesen** (in die Tabelle und das Match-Dokument):

- der Infoblock, der Demo-Header (jedes Feld; zwei nachfolgende unbekannte Bytes werden als Hex behalten) und die Chunk-Tabelle;
- jeder Frame, jedes Paket und jedes Bündel (ganz aufgeteilt in das, was sie tragen), jeder geöffnete Akteur (mit Spawn-Ort, Rotation, Skalierung und Geschwindigkeit) und jeder geschlossene (mit dem Grund: `Destroyed`, `Dormancy`...);
- jede replizierte Eigenschaft, soweit ihre Bits es sagen ([Eigenschaften dekodieren](how-it-works.md#decoding-properties)), Positionen aus `FRepMovement` und aus der Helikopter-Bewegungskomponente, die Todesfälle, die Gesundheit der Fahrzeuge, die Sitze;
- jeder Remote-Aufruf mit Namen, mit seinen Parametern, wo die Demo die Gruppe der Funktion exportiert: Schüsse (`fire`) und Fahrzeugtreffer (`hit`) in die Tabelle;
- die Net-Field-Exporttabellen und die Net-GUIDs (ihre Anzahl; die Pfade stehen in der Begleitdatei der Entitäten).

**Roh behalten** (ganz, mit dem daneben, was davon gelesen wurde):

- `<demo>.entities.parquet`, Spalten `time`, `type` (`<class>.<property>`, `<class>.<call>` oder der Name des Objekts), `name` (die Klasse des Akteurs), `entity` (die Net-GUID des Akteurs, wie `entity` in der Tabelle), `kind`, `object` (das Unterobjekt), `channel`, `handle`, `group` (der Klassenpfad der Exportgruppe), `decoded` (JSON), `bits` und `payload` (die Bits, niedrigstes zuerst, auf volle Bytes aufgefüllt):
  - jede Eigenschafts-Aktualisierung (`kind` `property`), die Bewegung eingeschlossen, mit dem, was dekodiert wurde; roh nur dort, wo nichts dekodiert werden kann (unbenannte Handles, Strukturen wie `RotationReplicatedMovement` von Geschützen und Eigenschaften, die als Bits bleiben);
  - jeder Remote-Aufruf und jedes Custom-Delta-Feld (`rpc`), die Parameter dekodiert, wo die Gruppe der Funktion exportiert wurde; roh, wo nicht (`RepInventory`, `PlayerStateData`);
  - jeder Content-Block eines Objekts, dessen Klasse nicht gefunden werden konnte (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), mit dekodiertem Kopf;
  - jeder Akteur-Kanal, der geöffnet und geschlossen wurde (`open`, `close`), jedes Unterobjekt, das gelöscht oder zerstört wurde;
  - der Kontext, den ein späterer Dekodierer braucht, um die Datei allein zu lesen: jeder Net-Field-Export (`export.field`: Gruppenpfad, Handle, Eigenschaftsname, Prüfsumme) und jede exportierte Net-GUID (`export.guid`: ihr Pfad, Besitzer und Flags), zu dem Zeitpunkt, an dem der Stream sie lieferte.
- `<demo>.packets.parquet`, Spalten `time`, `type`, `name`, `channel`, `offset` (in der Datei), `decoded`, `bits`, `payload`: der Infoblock, der Header-Chunk, jeder Checkpoint-Chunk (ein Checkpoint ist der Zustand jedes Akteurs zu seiner Zeit, den der Stream vom Anfang an ebenfalls enthält), jeder Ereignis-Chunk und jeder Frame, jedes Paket oder Bündel, das sich nicht lesen lässt (ein Bündel pro Demo: das Eröffnungsbündel des eigenen Spectator-Akteurs des Aufzeichnenden), ganz.

Die Zeilen der Entitäten sind nach `kind`, `type` und `entity` gruppiert, jeweils in Zeitfolge; sortiere nach `time` für die Reihenfolge des Streams.

**Nicht verfügbar:**

- was ein Server-Demo nicht aufzeichnet: Eingaben der Clients, was ein Spieler sah;
- Effekte auf Client-Seite: Trefferanzeigen, Sounds, der Text des Killfeeds (der Server sendet die Aufrufe, nicht deren Anzeige);
- dekodierte Online-IDs: nur als Bits behalten (siehe [Persönliche Daten](limits.md#personal-data)).
