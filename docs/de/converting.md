---
title: "Demos umwandeln"
nav_order: 3
lang: de
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demos umwandeln {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Schritt für Schritt {#step-by-step}

Noch nie in der Kommandozeile gearbeitet? Lies zuerst [Bevor du anfängst](before-you-start.md).

1. Einmal installieren: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   ein Terminal in diesem Ordner öffnen, `python -m pip install -e .` ausführen
   (Python 3.10 oder neuer; es bringt pyarrow und numpy mit).
2. Lege die `.replay`-Dateien in einen Ordner, oder nenne sie einzeln.
3. Führe `heat3d-squad-demo <folder> -o out` aus.
4. Du solltest pro Demo eine Zeile sehen: ihre Schicht, Spieler und Zeilen und wohin die Tabelle
   geschrieben wurde. Jede Demo wird zu vier losen Dateien in `out/<map>/` (kein
   `.3dheat`-Container); lade die `.parquet` im 3DHeat-Viewer.

![Ein Lauf auf einer synthetischen Demo](../assets/img/run.svg)

Das Bild zeigt einen Lauf auf einer Demo, die die Tests selbst bauen (`tests/test_stream.py`),
nicht auf einem echten Match.

## Optionen {#options}

| Option | Standard | Wirkung |
|---|---|---|
| `demos` (eine oder mehrere) | - | `.replay`-Dateien, oder Ordner, die sie enthalten |
| `-o`, `--out` | erforderlich | der Ordner, in den geschrieben wird; jede Demo kommt nach `<out>/<map>/` |
| `--flat` | aus | schreibt direkt in den Ordner, ohne den `<map>/`-Ordner |
| `--json` | aus | gibt pro Demo eine JSON-Zeile auf der Standardausgabe aus (für Programme, die den Befehl aufrufen): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; eine Demo, die fehlschlug, gibt `demo`, `ok: false` und `error` aus |
| `--version` | - | zeigt die Version an und hört auf |

Jede Option, so wie das Programm sie ausgibt: [Befehlsreferenz](../cli-reference.md).

Der Map-Ordner ist der Name der Map, aus dem Level-Pfad genommen, den die Demo angibt
(`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` ergibt `<Map>`).

Exit-Status: 0, wenn jede Demo umgewandelt wurde; 1, wenn eine fehlschlug (die anderen
werden trotzdem geschrieben) oder wenn keine `.replay`-Datei gefunden wurde.

## Was herauskommt {#what-comes-out}

| Datei | Was sie enthält |
|---|---|
| `<demo>.parquet` | die Tabelle: Positionen und Ereignisse, eine Zeile je Eintrag ([Die Tabelle](output-table.md)) |
| `<demo>.match.json` | das Match-Dokument ([Das Match-Dokument](output-match.md)) |
| `<demo>.entities.parquet` | Begleitdatei: jede Eigenschafts-Aktualisierung und jeder Remote-Aufruf, vollständig |
| `<demo>.packets.parquet` | Begleitdatei: die Chunks der Datei und alles, was nicht gelesen werden konnte, vollständig |

Die Tabelle und das Match-Dokument sind dasselbe Paar, das auch das 3DHeat-CS2-Werkzeug schreibt.
Der Viewer öffnet die Tabelle direkt und lässt die Begleitdateien weg, wenn ein ganzer
Ordner geladen wird.

## Beispiele {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

`D:\SquadDemos` ist ein Beispielordner auf Laufwerk D: nimm deinen eigenen.
