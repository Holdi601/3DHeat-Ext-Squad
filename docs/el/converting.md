---
title: Μετατροπή demo
nav_order: 3
lang: el
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Μετατροπή demo {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Βήμα προς βήμα {#step-by-step}

Δεν έχετε ξαναδουλέψει με τη γραμμή εντολών; Διαβάστε πρώτα το [Πριν ξεκινήσετε](before-you-start.md).

1. Εγκαταστήστε μία φορά: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`,
   ανοίξτε τερματικό μέσα σε αυτόν τον φάκελο, τρέξτε `python -m pip install -e .`
   (Python 3.10 ή νεότερη· φέρνει μαζί τα pyarrow και numpy).
2. Βάλτε τα αρχεία `.replay` σε έναν φάκελο, ή δώστε τα ένα ένα στην εντολή.
3. Τρέξτε `heat3d-squad-demo <folder> -o out`.
4. Θα δείτε μία γραμμή για κάθε demo: το επίπεδο του, τους παίκτες και τις γραμμές του,
   και πού γράφτηκε ο πίνακας. Κάθε demo γίνεται τέσσερα χαλαρά αρχεία μέσα στο `out/<map>/` (όχι
   κοντέινερ `.3dheat`)· φορτώστε το `.parquet` στον προβολέα 3DHeat.

![Μια εκτέλεση σε ένα συνθετικό demo](../assets/img/run.svg)

Η εικόνα δείχνει μια εκτέλεση σε demo που φτιάχνουν τα τεστ (`tests/test_stream.py`),
όχι σε πραγματικό αγώνα.

## Επιλογές {#options}

| Επιλογή | Προεπιλογή | Τι κάνει |
|---|---|---|
| `demos` (ένα ή περισσότερα) | - | αρχεία `.replay`, ή φάκελοι που τα περιέχουν |
| `-o`, `--out` | απαιτείται | ο φάκελος όπου γράφεται· κάθε demo πάει στο `<out>/<map>/` |
| `--flat` | ανενεργό | γράφει κατευθείαν μέσα στον φάκελο, χωρίς τον φάκελο `<map>/` |
| `--json` | ανενεργό | τυπώνει μία γραμμή JSON ανά demo στην έξοδο (για προγράμματα που καλούν την εντολή): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`· ένα demo που απέτυχε τυπώνει `demo`, `ok: false` και `error` αντί για αυτά |
| `--version` | - | τυπώνει την έκδοση και σταματά |

Κάθε επιλογή, όπως την τυπώνει το πρόγραμμα: [Αναφορά εντολών](../cli-reference.md).

Ο φάκελος του χάρτη είναι το όνομα του χάρτη, όπως προκύπτει από τη διαδρομή επιπέδου που αναφέρει το demo
(το `/Game/Maps/<Map>/Gameplay_Layers/<Layer>` δίνει `<Map>`).

Κωδικός εξόδου: 0 όταν μετατράπηκε κάθε demo· 1 όταν απέτυχε κάποιο (τα άλλα γράφονται κανονικά)
ή όταν δεν βρέθηκε κανένα αρχείο `.replay`.

## Τι βγαίνει {#what-comes-out}

| Αρχείο | Τι περιέχει |
|---|---|
| `<demo>.parquet` | ο πίνακας: θέσεις και γεγονότα, μία γραμμή το καθένα ([Ο πίνακας](output-table.md)) |
| `<demo>.match.json` | το έγγραφο αγώνα ([Το έγγραφο αγώνα](output-match.md)) |
| `<demo>.entities.parquet` | βοηθητικό αρχείο: κάθε ενημέρωση ιδιοτήτων και κάθε απομακρυσμένη κλήση, ολόκληρα |
| `<demo>.packets.parquet` | βοηθητικό αρχείο: τα κομμάτια του αρχείου και ό,τι δεν διαβάστηκε, ολόκληρα |

Ο πίνακας και το έγγραφο αγώνα είναι το ίδιο ζεύγος που γράφει και το εργαλείο 3DHeat CS2.
Ο προβολέας ανοίγει τον πίνακα κατευθείαν και αφήνει έξω τα βοηθητικά αρχεία όταν φορτώνεται ολόκληρος φάκελος.

## Παραδείγματα {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # every demo in a folder
heat3d-squad-demo one.replay two.replay -o out --flat  # straight into out/
heat3d-squad-demo D:\SquadDemos -o out --json          # one JSON line per demo
```

Το `D:\SquadDemos` είναι παράδειγμα φακέλου στον δίσκο D: χρησιμοποιήστε τον δικό σας.
