---
title: La tabella
nav_order: 4
lang: "it"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# La tabella: `<demo>.parquet` {#the-table-parquet}

Una riga per ogni campione o evento. Un campione viene preso ogni volta che il server ha replicato
il movimento dell'attore, fino a 8 volte al secondo (la frequenza di registrazione della demo)
mentre si muove.

![Le prime righe della tabella di una demo sintetica](../assets/img/table.svg)

## Colonne {#columns}

| Colonna | Cosa è |
|---|---|
| `time` | secondi dall'inizio della registrazione |
| `x`, `y`, `z` | posizione in unità Unreal (centimetri), Z verso l'alto |
| `dirX`, `dirY`, `dirZ` | dove guarda un soldato: la rotazione del corpo sull'asse verticale (imbardata) e l'inclinazione dello sguardo, come vettore unitario (per un veicolo: orizzontale) |
| `yaw`, `pitch` | le stesse cose in gradi; `pitch` è l'inclinazione verso l'alto dall'orizzonte, solo per i soldati |
| `health` | la salute del soldato, del bot o del veicolo in quel momento, dove il server l'ha inviata (quella di un soldato scende sotto 0 quando è ferito) |
| `speed` | la velocità replicata, cm/s |
| `player` | il nome del giocatore; `bot <id>` per un bot; per un veicolo o un dispositivo che nessuno possiede, la sua classe; per un colpo da un'arma di un veicolo, il giocatore seduto su quel veicolo |
| `team`, `faction` | il numero di squadra di Squad (1, 2) e la sua configurazione di fazione, **in quel momento**: i giocatori possono cambiare schieramento |
| `squad` | il numero del plotone, -1 quando non è in un plotone |
| `event` | che cosa rappresenta la riga (sotto) |
| `pawn` | il blueprint del soldato (`SQSquidBot` per un bot), il veicolo, o per `fire` l'arma |
| `seat` | per un posto di mitragliatrice o di passeggero, il pawn stesso del posto |
| `detail` | per `fire` la chiamata dell'arma che ha piazzato il colpo, per `hit` il tipo di danno, per `removed` il motivo per cui il canale si è chiuso (`Destroyed`, `Dormancy`...) |
| `entity` | l'attore a cui si riferisce la riga (il suo GUID di rete): l'`entity` delle righe dei file accessori |
| `match` | il nome della demo |

## Eventi {#events}

| Evento | Sulla riga di | Cosa |
|---|---|---|
| `position` | un soldato o un bot a piedi | un campione di movimento |
| `vehicle` | un soldato su un veicolo di terra o su un elicottero | un campione nella posizione del veicolo |
| `wounded`, `revived`, `death` | soldati e bot | dove è accaduto |
| `spawn`, `damaged`, `destroyed`, `removed` | veicoli, dispositivi schierabili, postazioni, casse di munizioni, elicotteri | dove si trovavano |
| `seat` | un giocatore | ha preso un posto |
| `fire` | chi spara | un colpo: da dove è partito, la sua direzione come `yaw`/`pitch`/`dirX..Z` |
| `hit` | il veicolo | un colpo al veicolo: dove |

Come vengono letti gli eventi è spiegato in [Come viene letta una demo](how-it-works.md#how-the-events-are-read).

## Nel visualizzatore {#in-the-viewer}

Il footer del file Parquet contiene le istruzioni di lettura sotto la chiave `heat3d`: Z verso
l'alto, nessun asse specchiato, scala unitaria 1, quindi il visualizzatore non ha bisogno di
alcuna mappatura delle colonne. Carica la tabella nella scheda Mappa di calore; vedi
[Come caricare i dati](https://holdi601.github.io/3DHeat/getting-data-in.html) e
[Mappatura delle colonne](https://holdi601.github.io/3DHeat/column-mapping.html) nella
documentazione del visualizzatore.
