---
title: Vedligeholdelse af disse dokumenter
nav_order: 91
lang: da
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Vedligeholdelse af disse dokumenter {#maintaining-these-docs}

En tjekliste for hver udgivelse, så siderne aldrig halter efter koden.

1. **Generer referencen igen.** `python tools/gen_docs_reference.py` omskriver
   [Kommandoreference](../cli-reference.md) ud fra programmets egen `--help` og
   output-kolonnerne. `python tools/gen_docs_reference.py --check` afslutter med 1, når
   den committede side er forældet.
2. **List det, der er ændret.** `git log v<VERSION>..HEAD --oneline`, hvor
   `<VERSION>` er den sidst udgivne version (filen `VERSION` ved udgivelsen).
   Giv hver ny funktion, valgmulighed og outputkolonne en plads på en side, og en
   række i afsnittet **Docs** i [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Uafhængig gennemgang.** En person, der ikke skrev siderne, læser README og
   hver ændret side, billederne inklusive, tre gange: som en begynder, der aldrig har
   brugt en terminal, som en 8-årig, og som en professionel, der tjekker hver
   valgmulighed mod `--help`. Eksempler bruger kun opdigtede navne og tal.
4. **Ret** alt, gennemgangen finder.
5. **Oversættelser.** Hver oversat side noterer hashen af den engelske side, den
   blev lavet ud fra. Oversæt de sider igen, hvis engelske kilde er ændret,
   og gennemgå derefter hvert sprog: klar tekst, korrekte diagramtekster, de samme
   ord som viewerens egen oversatte grænseflade.
6. **Kør testene** (`pytest`).
7. **Push** først efter ejerens grønne lys.

## Oversættelser: kommandoerne {#translations-the-commands}

Siden er oversat til 3DHeat-viewerens 40 sprog: engelsk i `docs/`, hvert andet
sprog i `docs/<lang>/` med de samme filnavne. `tools/docs_i18n.py` står for bogholderiet:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Oversæt kun det, `todo` lister: behold Markdown, links, kode, fil- og kolonnenavne, som de er,
oversæt titler og billedbeskrivelser, og brug 3DHeat-viewerens egne ord til dens knapper
og paneler (dens `src/i18n/locales/<lang>/`). Genererede referencesider og terminalbilleder bliver
engelske. På siden viser en forældet oversættelse det og linker til den engelske side; en manglende
falder tilbage til engelsk. Sprogmenuen i sidehovedet og browsersprogets omdirigering på startsiden
kommer fra `docs/_includes/`.
