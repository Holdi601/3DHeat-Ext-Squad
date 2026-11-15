---
title: Convertire le demo
nav_order: 3
lang: "it"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Convertire le demo {#converting-demos}

```text
heat3d-squad-demo <demo o cartelle> -o <cartella> [--flat] [--json]
python -m heat3d_ext_squad ...          lo stesso, senza installare
```

## Passo per passo {#step-by-step}

Non hai mai usato la riga di comando? Leggi prima [Prima di iniziare](before-you-start.md).

1. Installa una volta sola: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   apri un terminale in quella cartella, esegui `python -m pip install -e .`
   (Python 3.10 o successivo; porta con sé pyarrow e numpy).
2. Metti i file `.replay` in una cartella, oppure indicali uno per uno.
3. Esegui `heat3d-squad-demo <cartella> -o out`.
4. Dovresti vedere una riga per ogni demo: il suo livello, i giocatori e le righe, e dove è
   finita la tabella. Ogni demo diventa quattro file separati in `out/<map>/` (non un
   contenitore `.3dheat`); carica il `.parquet` nel visualizzatore 3DHeat.

![Un'esecuzione su una demo sintetica](../assets/img/run.svg)

L'immagine mostra un'esecuzione su una demo creata dai test (`tests/test_stream.py`),
non su una partita vera.

## Opzioni {#options}

| Opzione | Predefinito | Cosa fa |
|---|---|---|
| `demos` (una o più) | - | file `.replay`, oppure cartelle che li contengono |
| `-o`, `--out` | obbligatoria | la cartella in cui scrivere; ogni demo va in `<out>/<map>/` |
| `--flat` | disattivata | scrive direttamente nella cartella, senza la sottocartella `<map>/` |
| `--json` | disattivata | stampa una riga di JSON per ogni demo sullo standard output (per i programmi che richiamano il comando): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; una demo fallita stampa `demo`, `ok: false` e `error` al suo posto |
| `--version` | - | stampa la versione e si ferma |

Ogni opzione, come la stampa il programma: [Riferimento dei comandi](../cli-reference.md).

Il nome della cartella della mappa è il nome della mappa preso dal percorso del livello che la
demo indica (`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` dà `<Map>`).

Stato di uscita: 0 quando tutte le demo sono state convertite; 1 quando una è fallita (le altre
vengono scritte comunque) o quando non è stato trovato nessun file `.replay`.

## Cosa viene prodotto {#what-comes-out}

| File | Cosa contiene |
|---|---|
| `<demo>.parquet` | la tabella: posizioni ed eventi, una riga ciascuno ([La tabella](output-table.md)) |
| `<demo>.match.json` | il documento della partita ([Il documento della partita](output-match.md)) |
| `<demo>.entities.parquet` | file accessorio: ogni aggiornamento di proprietà e ogni chiamata remota, per intero |
| `<demo>.packets.parquet` | file accessorio: i blocchi del file e tutto ciò che non è stato letto, per intero |

La tabella e il documento della partita sono la stessa coppia scritta dallo strumento 3DHeat CS2.
Il visualizzatore apre la tabella direttamente e lascia fuori i file accessori quando si carica
un'intera cartella.

## Esempi {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # ogni demo di una cartella
heat3d-squad-demo one.replay two.replay -o out --flat  # direttamente dentro out/
heat3d-squad-demo D:\SquadDemos -o out --json          # una riga JSON per demo
```

`D:\SquadDemos` è una cartella di esempio sul disco D: usa la tua.
