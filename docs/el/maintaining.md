---
title: Συντήρηση αυτών των σελίδων
nav_order: 91
lang: "el"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Συντήρηση αυτών των σελίδων {#maintaining-these-docs}

Μια λίστα ελέγχου για κάθε έκδοση, ώστε οι σελίδες να μην μένουν πίσω από τον κώδικα.

1. **Ξαναδημιουργήστε την αναφορά.** Το `python tools/gen_docs_reference.py` ξαναγράφει την
   [Αναφορά εντολών](../cli-reference.md) από το δικό του `--help` του προγράμματος και από τις στήλες εξόδου.
   Το `python tools/gen_docs_reference.py --check` τερματίζει με κωδικό 1 όταν η σελίδα στο αποθετήριο είναι παλιά.
2. **Καταγράψτε τι άλλαξε.** `git log v<VERSION>..HEAD --oneline`, όπου το `<VERSION>` είναι η
   τελευταία κυκλοφορημένη έκδοση (το αρχείο `VERSION` κατά την κυκλοφορία). Δώστε σε κάθε νέα
   λειτουργία, επιλογή και στήλη εξόδου μια θέση σε μια σελίδα, και μια γραμμή στην ενότητα **Docs** του
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Ανεξάρτητος έλεγχος.** Κάποιος που δεν έγραψε τις σελίδες διαβάζει το README και κάθε αλλαγμένη σελίδα,
   και τις εικόνες, τρεις φορές: σαν αρχάριος που δεν έχει ξαναχρησιμοποιήσει τερματικό, σαν οκτάχρονος,
   και σαν ειδικός που ελέγχει κάθε επιλογή με το `--help`. Τα παραδείγματα χρησιμοποιούν μόνο
   φανταστικά ονόματα και αριθμούς.
4. **Διορθώστε** όσα βρει ο έλεγχος.
5. **Μεταφράσεις.** Κάθε μεταφρασμένη σελίδα καταγράφει το hash της αγγλικής σελίδας από την οποία
   έγινε. Μεταφράστε ξανά τις σελίδες των οποίων η αγγλική πηγή αλλάζει, και ελέγξτε κάθε γλώσσα: καθαρό
   κείμενο, σωστές ετικέτες στα διαγράμματα, και ίδιες λέξεις με τη μεταφρασμένη διεπαφή του ίδιου του προβολέα 3DHeat.
6. **Τρέξτε τα τεστ** (`pytest`).
7. **Ανεβάστε** μόνο μετά από την έγκριση του ιδιοκτήτη.

## Μεταφράσεις: οι εντολές {#translations-the-commands}

Ο ιστότοπος μεταφράζεται στις 40 γλώσσες του προβολέα 3DHeat: τα αγγλικά βρίσκονται στο `docs/`, κάθε άλλη
γλώσσα στο `docs/<lang>/` με τα ίδια ονόματα αρχείων. Το `tools/docs_i18n.py` κάνει τη λογιστική:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Μεταφράζετε μόνο όσα δείχνει το `todo`: κρατήστε το Markdown, τους συνδέσμους, τον κώδικα και τα ονόματα αρχείων
και στηλών όπως είναι, μεταφράστε τους τίτλους και τις περιγραφές εικόνων, και χρησιμοποιήστε τις δικές του
λέξεις του προβολέα 3DHeat για τα κουμπιά και τα πάνελ του (τον φάκελο `src/i18n/locales/<lang>/` του).
Οι αυτόματα παραγόμενες σελίδες αναφοράς και οι εικόνες τερματικού μένουν στα αγγλικά. Στον ιστότοπο, μια
παλιά μετάφραση το δηλώνει και συνδέει με την αγγλική σελίδα· μια μη υπάρχουσα πέφτει πίσω στα αγγλικά.
Το μενού γλωσσών της κεφαλίδας και η ανακατεύθυνση της αρχικής σελίδας με βάση τη γλώσσα του
περιηγητή έρχονται από το `docs/_includes/`.
