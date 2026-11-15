---
title: Manutenzione di questa documentazione
nav_order: 91
lang: it
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Manutenzione di questa documentazione {#maintaining-these-docs}

Una lista di controllo per ogni rilascio, perché le pagine non restino mai indietro rispetto al codice.

1. **Rigenera il riferimento.** `python tools/gen_docs_reference.py` riscrive il [Riferimento dei comandi](../cli-reference.md) a partire dal `--help` del programma e dalle colonne di output. `python tools/gen_docs_reference.py --check` termina con 1 quando la pagina committata è obsoleta.
2. **Elenca ciò che è cambiato.** `git log v<VERSION>..HEAD --oneline`, dove `<VERSION>` è l'ultima versione rilasciata (il file `VERSION` al rilascio). Dai a ogni nuova funzione, opzione e colonna di output un posto in una pagina, e una riga nella sezione **Docs** di [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Revisione indipendente.** Qualcuno che non ha scritto le pagine legge il README e ogni pagina cambiata, immagini comprese, tre volte: come un principiante che non ha mai usato un terminale, come un bambino di 8 anni, e come un esperto che controlla ogni opzione con `--help`. Gli esempi usano solo nomi e numeri inventati.
4. **Correggi** tutto ciò che la revisione trova.
5. **Traduzioni.** Ogni pagina tradotta registra l'hash della pagina inglese da cui è nata. Traduci di nuovo le pagine la cui fonte inglese è cambiata, poi rivedi ogni lingua: testo chiaro, etichette corrette nei diagrammi, le stesse parole dell'interfaccia tradotta del visualizzatore.
6. **Esegui i test** (`pytest`).
7. **Pubblica** solo dopo il via libera del proprietario.

## Traduzioni: i comandi {#translations-the-commands}

Il sito è tradotto nelle 40 lingue del visualizzatore 3DHeat: l'inglese in `docs/`, ogni altra lingua in `docs/<lang>/` con gli stessi nomi di file. `tools/docs_i18n.py` tiene la contabilità:

```bash
python tools/docs_i18n.py hashes             # dopo ogni modifica all'inglese: registra l'hash di ogni pagina
python tools/docs_i18n.py svg-strings        # dopo ogni modifica alle immagini: le etichette da tradurre
python tools/docs_i18n.py status             # per lingua: pagine aggiornate, obsolete, mancanti
python tools/docs_i18n.py todo --lang de     # le pagine tedesche da (ri)tradurre
python tools/docs_i18n.py svg-build --lang de    # le immagini tedesche da docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # marca le pagine tedesche con l'hash inglese
python tools/docs_i18n.py check              # termina con 1 quando hash o etichette sono obsoleti
```

Traduci solo ciò che elenca `todo`: lascia invariati Markdown, collegamenti, codice, nomi di file e di colonne, traduci i titoli e le descrizioni delle immagini, e usa le parole del visualizzatore 3DHeat per i suoi pulsanti e pannelli (la sua cartella `src/i18n/locales/<lang>/`). Le pagine di riferimento generate e le immagini dei terminali restano in inglese. Sul sito, una traduzione obsoleta lo dice e rimanda alla pagina inglese; una traduzione mancante ricade sull'inglese. Il menu delle lingue dell'intestazione e il reindirizzamento della home page secondo la lingua del browser vengono da `docs/_includes/`.
