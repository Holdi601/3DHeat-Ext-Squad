---
title: Underhålla dokumentationen
nav_order: 91
lang: sv
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Underhålla dokumentationen {#maintaining-these-docs}

En checklista för varje utgåva, så att sidorna aldrig hamnar efter koden.

1. **Generera referensen på nytt.** `python tools/gen_docs_reference.py` skriver om [Kommandoreferens](../cli-reference.md) från programmets egen `--help` och utdatakolumner. `python tools/gen_docs_reference.py --check` avslutas med 1 när den incheckade sidan är föråldrad.
2. **Lista vad som ändrats.** `git log v<VERSION>..HEAD --oneline`, där `<VERSION>` är den senast släppta versionen (filen `VERSION` vid utgivning). Ge varje ny funktion, alternativ och utdatakolumn en plats på en sida, och en rad i avsnittet **Docs** i [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Oberoende granskning.** Någon som inte skrev sidorna läser README och varje ändrad sida, bilderna inkluderade, tre gånger: som en nybörjare som aldrig använt en terminal, som en åttaåring, och som en expert som kontrollerar varje alternativ mot `--help`. Exemplen använder påhittade namn och siffror bara.
4. **Åtgärda** allt granskningen hittar.
5. **Översättningar.** Varje översatt sida noterar hashvärdet för den engelska sida den gjordes från. Översätt på nytt de sidor vars engelska källa ändrats, och granska sedan varje språk: tydlig text, rätt diagramtexter, samma ord som visarens egna översatta gränssnitt.
6. **Kör testerna** (`pytest`).
7. **Publicera** först efter ägarens godkännande.

## Översättningar: kommandona {#translations-the-commands}

Webbplatsen är översatt till 3DHeat-visarens 40 språk: engelska i `docs/`, varje annat språk i `docs/<lang>/` med samma filnamn. `tools/docs_i18n.py` sköter bokföringen:

```bash
python tools/docs_i18n.py hashes             # efter varje engelsk ändring: spara varje sidas hash
python tools/docs_i18n.py svg-strings        # efter varje bildändring: texterna att översätta
python tools/docs_i18n.py status             # per språk: aktuella, föråldrade och saknade sidor
python tools/docs_i18n.py todo --lang de     # de tyska sidorna att (över)översätta
python tools/docs_i18n.py svg-build --lang de    # tyska bilder från docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # märk de tyska sidorna med deras engelska hash
python tools/docs_i18n.py check              # avslutas med 1 när hashar eller texter är föråldrade
```

Översätt bara det `todo` listar: behåll Markdown, länkar, kod, fil- och kolumnnamn som de är, översätt titlar och bildbeskrivningar, och använd 3DHeat-visarens egna ord för dess knappar och paneler (dess `src/i18n/locales/<lang>/`). Genererade referenssidor och terminalbilder förblir engelska. På webbplatsen säger en föråldrad översättning det och länkar till den engelska sidan; en saknad sida faller tillbaka till engelska. Språkmenyn i sidhuvudet och startsidans omdirigering efter webbläsarens språk kommer från `docs/_includes/`.
