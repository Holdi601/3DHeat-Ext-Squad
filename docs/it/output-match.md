---
title: Il documento della partita e i file accessori
nav_order: 5
lang: it
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Il documento della partita e i file accessori {#the-match-document-and-sidecars}

Accanto alla tabella, ogni demo produce `<demo>.match.json` e due file accessori,
`<demo>.entities.parquet` e `<demo>.packets.parquet`. Il visualizzatore legge il documento della
partita nella sua scheda Partita.

## Il documento della partita {#the-match-document}

`<demo>.match.json` (il documento della partita) contiene al primo livello `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` e `selfCheck` (l'elenco completo: [Riferimento dei comandi](../cli-reference.md)). In parole: la mappa e il livello, le versioni del gioco e del motore, il momento della registrazione, la durata, e:

- **le squadre**: numero, fazione e tutto ciò che il loro stato ha replicato (biglietti, disponibilità, comandante) man mano che cambiava;
- **i plotoni**: numero, squadra, nome, creatore, capo, membri;
- **lo stato della partita**: nome e impostazioni del server, modalità di gioco, stato e id della partita, rotazioni di mappe e livelli, votazioni, timer, il messaggio del giorno;
- **gli attori**: ogni veicolo, dispositivo schierabile, postazione, cassa di munizioni ed elicottero - classe, dove e quando è stato creato, quando è sparito, di chi era, e il suo stato replicato (salute, stato di costruzione, posti...);
- **una riga per ogni giocatore**: campioni a piedi e nei veicoli, distanza percorsa, classi di soldato giocate, veicoli usati, cambi di squadra, posti occupati, e tutto ciò che lo stato del giocatore ha replicato (ping, livello, ruolo, posto attuale...); e una riga per ogni bot;
- **gli eventi** contati, il **censimento delle proprietà** (quante volte sono state inviate le proprietà di ogni classe) e il **censimento delle chiamate remote**, i colpi e i colpi a segno, ciò che **non** è stato letto, e la diagnostica del lettore;
- **il file e l'intestazione**: ogni campo del blocco di informazioni e dell'intestazione della demo, la tabella dei blocchi, le tabelle di esportazione dei campi di rete (`net_field_exports`), i motivi di chiusura dei canali, e le classi trovate per gli oggetti che le esportazioni non nominano (`stream.class_resolution`);
- **il controllo automatico** (`selfCheck.completeness`, vedi [Completezza](#completeness)).

Gli ID online (Steam, EOS) sono lasciati fuori di proposito.

Uno sguardo rapido a una demo convertita:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Completezza {#completeness}

Questo lettore segue la regola che condividono tutti i convertitori 3DHeat: decodificare ciò che si
può leggere ora, conservare il resto per intero, e dire quanto ne è stato decodificato per ogni tipo
([I convertitori conservano tutto](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)).
Ogni documento della partita ha `selfCheck.completeness`: per ogni tipo di elemento incontrato nella
demo, quanti sono stati `seen` (visti), `decoded` (decodificati), `partial` (decodificati in parte e
conservati per intero), `raw` (conservati solo per intero) e `lost` (perduti, deve essere 0). I tipi
vengono contati nel punto in cui il lettore li incontra: `file.info`, `chunk.<kind>`, `frame`,
`packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`,
`rpc:<class>`, `block:<object>`, `subobject.*`.

Sulle demo reali lette, `lost` è 0: i loro elementi vanno da centinaia di migliaia a milioni; circa
la metà si decodifica del tutto, il resto è parziale o grezzo.

**Letti** (nella tabella e nel documento della partita):

- il blocco di informazioni, l'intestazione della demo (ogni campo; due byte finali non noti sono conservati in esadecimale), la tabella dei blocchi;
- ogni frame, pacchetto e bunch (scomposto per intero in ciò che contiene), ogni attore aperto (con la sua posizione di creazione, rotazione, scala e velocità) e chiuso (con il motivo: `Destroyed`, `Dormancy`...);
- ogni proprietà replicata, per quanto i suoi bit dicono ([Decodifica delle proprietà](how-it-works.md#decoding-properties)), posizioni da `FRepMovement` e dal componente di movimento degli elicotteri, le perdite, la salute dei veicoli, i posti;
- ogni chiamata remota per nome, con i suoi parametri dove la demo esporta il gruppo della funzione: i colpi (`fire`) e i colpi ai veicoli (`hit`) nella tabella;
- le tabelle di esportazione dei campi di rete e i GUID di rete (il loro numero; i percorsi sono nel file accessorio delle entità).

**Conservati grezzi** (per intero, con accanto ciò che se ne legge):

- `<demo>.entities.parquet`, colonne `time`, `type` (`<class>.<property>`, `<class>.<call>`, oppure il nome dell'oggetto), `name` (la classe dell'attore), `entity` (il GUID di rete dell'attore, come `entity` della tabella), `kind`, `object` (il sotto-oggetto), `channel`, `handle`, `group` (il percorso di classe del gruppo di esportazione), `decoded` (JSON), `bits` e `payload` (i bit, dal meno significativo, riempiti fino a byte interi):
  - ogni aggiornamento di proprietà (`kind` `property`), movimento compreso, con ciò che è decodificato; grezzo solo dove non c'è nulla da decodificare (handle senza nome, strutture come `RotationReplicatedMovement` delle torrette, e proprietà lasciate come bit);
  - ogni chiamata remota e ogni campo di delta personalizzato (`rpc`), con i parametri decodificati dove il gruppo della funzione è stato esportato; grezzo dove non lo è (`RepInventory`, `PlayerStateData`);
  - ogni blocco di contenuto di un oggetto la cui classe non è stata trovata (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), con la sua intestazione decodificata;
  - ogni canale di attore aperto e chiuso (`open`, `close`), ogni sotto-oggetto eliminato o distrutto;
  - il contesto che un decodificatore successivo richiede per leggere il file da solo: ogni esportazione di campo di rete (`export.field`: percorso del gruppo, handle, nome della proprietà, checksum) e ogni GUID di rete esportato (`export.guid`: il suo percorso, l'esterno e i flag), nel momento in cui il flusso li ha forniti.
- `<demo>.packets.parquet`, colonne `time`, `type`, `name`, `channel`, `offset` (nel file), `decoded`, `bits`, `payload`: il blocco di informazioni, il blocco di intestazione, ogni blocco di checkpoint (un checkpoint è lo stato di ogni attore nel suo momento, che anche il flusso dall'inizio contiene), ogni blocco di eventi, e ogni frame, pacchetto o bunch che non si legge (un bunch per demo: il bunch di apertura dell'attore spettatore del registratore), per intero.

Le righe delle entità sono raggruppate per `kind`, `type` ed `entity`, ciascuna in ordine temporale; ordinale per `time` per l'ordine del flusso.

**Non disponibili:**

- ciò che una demo di server non registra: gli input dei client, ciò che un giocatore vedeva;
- gli effetti lato client: i segnali di colpo, i suoni, il testo della lista delle uccisioni (il server invia le chiamate, non la loro visualizzazione);
- gli ID online decodificati: conservati solo come bit (vedi [Dati personali](limits.md#personal-data)).
