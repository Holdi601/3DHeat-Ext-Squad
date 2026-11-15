---
title: Maintaining these docs
nav_order: 91
---

# Maintaining these docs

A checklist for each release, so the pages never fall behind the code.

1. **Regenerate the reference.** `python tools/gen_docs_reference.py` rewrites
   [Command reference](cli-reference.md) from the program's own `--help` and
   output columns. `python tools/gen_docs_reference.py --check` exits 1 when
   the committed page is stale.
2. **List what changed.** `git log v<VERSION>..HEAD --oneline`, where
   `<VERSION>` is the last released version (the `VERSION` file at release).
   Give every new feature, option and output column a place on a page, and a
   row in the **Docs** section of [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Independent review.** Someone who did not write the pages reads the
   README and every changed page, the pictures included, three times: as a
   beginner who has never used a terminal, as an 8-year-old, and as an expert
   who checks every option against `--help`. Examples use made-up names and
   numbers only.
4. **Fix** everything the review finds.
5. **Translations.** Every translated page records the hash of the English page
   it was made from. Translate again the pages whose English source changed,
   then review each language: clear text, correct diagram labels, the same
   words as the viewer's own translated interface.
6. **Run the tests** (`pytest`).
7. **Push** only after the owner's go-ahead.
