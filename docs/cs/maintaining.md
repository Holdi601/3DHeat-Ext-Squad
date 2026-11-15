---
title: "Údržba těchto dokumentů"
nav_order: 91
lang: "cs"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Údržba těchto dokumentů {#maintaining-these-docs}

Kontrolní seznam pro každé vydání, aby stránky nikdy nezaostaly za kódem.

1. **Přegenerujte přehled.** `python tools/gen_docs_reference.py` přepíše
   [Přehled příkazů](../cli-reference.md) podle nápovědy `--help` a výstupních sloupců
   přímo z programu. `python tools/gen_docs_reference.py --check` skončí s kódem 1, když
   je uložená stránka zastaralá.
2. **Vypište, co se změnilo.** `git log v<VERSION>..HEAD --oneline`, kde
   `<VERSION>` je poslední vydaná verze (soubor `VERSION` při vydání). Každá nová
   funkce, možnost a výstupní sloupec musí mít místo na stránce a řádek v sekci **Docs**
   v [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Nezávislá kontrola.** Někdo, kdo stránky nepsal, přečte README a každou změněnou
   stránku, včetně obrázků, třikrát: jako začátečník, který nikdy nepoužil terminál,
   jako osmiletý a jako odborník, který kontroluje každou možnost proti `--help`.
   Příklady používají jen vymyšlená jména a čísla.
4. **Opravte** vše, co kontrola najde.
5. **Překlady.** Každá přeložená stránka si zapisuje otisk anglické stránky, ze které
   vznikla. Znovu přeložte stránky, jejichž anglický zdroj se změnil, a pak zkontrolujte
   každý jazyk: srozumitelný text, správné popisky diagramů, stejná slova, jaká používá
   přeložené rozhraní prohlížeče 3DHeat.
6. **Spusťte testy** (`pytest`).
7. **Nahrajte** až po souhlasu vlastníka.

## Překlady: příkazy {#translations-the-commands}

Web je přeložen do 40 jazyků prohlížeče 3DHeat: angličtina je v `docs/`, každý další
jazyk v `docs/<lang>/` se stejnými názvy souborů. `tools/docs_i18n.py` vede evidenci:

```bash
python tools/docs_i18n.py hashes             # after any English change: record each page's hash
python tools/docs_i18n.py svg-strings        # after any picture change: the labels to translate
python tools/docs_i18n.py status             # per language: current, outdated, missing pages
python tools/docs_i18n.py todo --lang de     # the German pages to (re)translate
python tools/docs_i18n.py svg-build --lang de    # German pictures from docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # stamp the German pages with their English hash
python tools/docs_i18n.py check              # exit 1 when hashes or labels are stale
```

Překládejte jen to, co vypíše `todo`: Markdown, odkazy, kód, názvy souborů a sloupců
ponechte beze změny, překládejte nadpisy a popisy obrázků a pro tlačítka a panely
prohlížeče 3DHeat používejte jeho vlastní slova (`src/i18n/locales/<lang>/`).
Generované přehledové stránky a obrázky terminálu zůstávají anglicky. Na webu
zastaralý překlad to řekne a odkáže na anglickou stránku; chybějící překlad se
zobrazí anglicky. Jazykové menu v záhlaví a přesměrování podle jazyka prohlížeče
na domovské stránce pocházejí z `docs/_includes/`.
