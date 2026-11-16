---
title: Limiti, aggiornamenti e condizioni
nav_order: 7
lang: "it"
source: limits.md
source_hash: "8a9c7c448411"
nav_exclude: true
search_exclude: true
---
# Limiti, aggiornamenti e condizioni {#limits-updates-and-terms}

## Non letto {#not-read}

- **Chi ha ucciso chi, e i danni ai soldati colpo per colpo.** Questi viaggiano nei risultati dei colpi delle chiamate remote delle armi e degli stati dei giocatori (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), la cui struttura non viene letta; sono conservati per intero nel file accessorio delle entità. Viene decodificata solo la salute delle vittime.
- **La squadra del bot.** Lo stato di un bot contiene un numero che potrebbe essere la sua squadra; non confermato, non usato.
- **Dove un soldato guarda di lato**, oltre l'imbardata del corpo.

## Aggiornamenti del gioco {#game-updates}

Il lettore dipende dal formato di replay del motore e da una manciata di nomi di classi e proprietà di Squad. Non dipende dalle disposizioni delle proprietà che non può vedere: il replay le nomina da sé.

**Cosa può rompersi con un aggiornamento di Squad:**

- **Un aggiornamento del motore.** Squad è passato a UE 5.7 con la v10.4, e questo non è stato provato lì. L'aggiornamento può cambiare l'intestazione dei bunch, i dati di creazione o il `FRepMovement`. Questi sono legati alla versione nel codice dove il passo è noto. I passi sconosciuti (`ENG_PARTIAL_CUSTOM_EXPORTS`, il bit finale del movimento) sono fissati a ciò che fa la v10.3.1.
- **La replica Iris.** Se Squad passasse a Iris, il flusso dentro i blocchi sarebbe nuovo e questo lettore non lo leggerebbe. Squad v10.3.1 usa il sistema classico (usa ReplicationGraph).
- **Classi o proprietà rinominate.** Se Squad rinominasse le sue classi di giocatore, squadra o plotone, o le loro proprietà, nomi e squadre andrebbero persi, ma le posizioni no.
- **Cosa succede in caso di errore.** Quando il formato cambia, il lettore fallisce in modo evidente, con errori di flusso o di movimento nella diagnostica. Non produce in silenzio posizioni sbagliate: un `FRepMovement` viene accettato solo quando i suoi bit tornano esattamente.

## Dati personali {#personal-data}

Una demo contiene i nomi e gli ID online di tutti i presenti sul server. La tabella e il documento della partita riportano nomi, non ID. I file accessori conservano i bit di ogni proprietà, quindi contengono gli ID come li contiene la demo (non decodificati). Trattali tutti come la demo stessa.

## Licenza e fonti {#licence-and-sources}

MIT; vedi [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Tutto ciò che è qui è stato scritto per questo pacchetto. Non è incluso né collegato alcun codice di terzi: le uniche dipendenze sono pyarrow (Apache-2.0) e numpy (BSD-3-Clause).

Le informazioni sul formato provengono da queste fonti:

- **Unreal.Core** in [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Descrive il layout generico dei replay di Unreal: il blocco di informazioni, i blocchi, i frame, i bunch e le esportazioni dei campi di rete.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Il suo parser è stato letto per il layout come lo scrive Squad v10.3.1, per i controlli di versione e per le classi di Squad che contengono i dati dell'elenco dei giocatori. Le sue demo di prova pubblicate e i suoi conteggi di riferimento sono stati usati come verifica incrociata indipendente. Nessun suo codice è stato copiato o tradotto: questo lettore è strutturato in modo diverso (un archivio di bit in Python sui pacchetti interi, bunch parziali uniti a livello di bit, proprietà smistate per nome), e due cose che quel progetto non fa sono state trovate qui sulle demo stesse: il terzo flag dei bunch parziali e il bit finale del movimento.

Questo pacchetto legge i file demo che scrive un server di Squad; non tocca il gioco, il suo codice né i suoi archivi, e nulla del gioco è incluso o ridistribuito. Ciò che scrive resta sulla tua macchina.

3DHeat non è affiliato a Offworld Industries né approvato da Offworld Industries. Squad e i nomi e marchi correlati appartengono ai rispettivi proprietari.

Titolari dei diritti: aprite una issue su <https://github.com/Holdi601/3DHeat-Ext-Squad/issues> - rispondiamo rapidamente e rimuoviamo qualsiasi cosa su richiesta.
