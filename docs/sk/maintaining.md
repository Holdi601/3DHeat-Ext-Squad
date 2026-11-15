---
title: "Údržba týchto dokumentov"
nav_order: 91
lang: "sk"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Údržba týchto dokumentov {#maintaining-these-docs}

Kontrolný zoznam pre každé vydanie, aby stránky nikdy nezaostali za kódom.

1. **Obnovte referenciu.** `python tools/gen_docs_reference.py` prepíše
   [Referenciu príkazov](../cli-reference.md) z vlastného `--help` programu a z jeho výstupných stĺpcov. `python tools/gen_docs_reference.py --check` skončí s 1, keď je odovzdaná stránka zastaraná.
2. **Vypíšte, čo sa zmenilo.** `git log v<VERSION>..HEAD --oneline`, kde `<VERSION>` je posledná vydaná verzia (súbor `VERSION` pri vydaní). Každá nová funkcia, možnosť a výstupný stĺpec musí mať miesto na stránke a riadok v sekcii **Docs** v [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md).
3. **Nezávislá kontrola.** Niekto, kto stránky nepísal, prečíta README a každú zmenenú stránku vrátane obrázkov tri razy: ako začiatočník, ktorý nikdy nepoužil terminál, ako osemročné dieťa a ako expert, ktorý overí každú možnosť voči `--help`. Príklady používajú len vymyslené mená a čísla.
4. **Opravte** všetko, čo kontrola nájde.
5. **Preklady.** Každá preložená stránka zapisuje hash anglickej stránky, z ktorej vznikla. Znova preložte stránky, ktorých anglický zdroj sa zmenil, a potom skontrolujte každý jazyk: zrozumiteľný text, správne popisky obrázkov, rovnaké slová ako preložené rozhranie prehliadača.
6. **Spustite testy** (`pytest`).
7. **Odošlite** až po súhlase vlastníka.

## Preklady: príkazy {#translations-the-commands}

Stránka je preložená do 40 jazykov prehliadača 3DHeat: angličtina je v `docs/`, každý ďalší jazyk v `docs/<lang>/` s rovnakými názvami súborov. `tools/docs_i18n.py` vedie evidenciu:

```bash
python tools/docs_i18n.py hashes             # po každej zmene v angličtine: zapíše hash každej stránky
python tools/docs_i18n.py svg-strings        # po každej zmene obrázka: popisky na preloženie
python tools/docs_i18n.py status             # pre každý jazyk: aktuálne, zastarané a chýbajúce stránky
python tools/docs_i18n.py todo --lang de     # nemecké stránky na (znovu)preloženie
python tools/docs_i18n.py svg-build --lang de    # nemecké obrázky z docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # označí nemecké stránky hashom anglickej stránky
python tools/docs_i18n.py check              # skončí s 1, keď sú hashe alebo popisky zastarané
```

Prekladajte len to, čo vypíše `todo`: Markdown, odkazy, kód, názvy súborov a stĺpcov nechajte tak, ako sú; prekladajte nadpisy a popisy obrázkov a na tlačidlá a panely prehliadača 3DHeat používajte jeho vlastné slová (jeho `src/i18n/locales/<lang>/`). Generované referenčné stránky a terminálové obrázky ostávajú v angličtine. Na webe zastaraný preklad to povie a odkáže na anglickú stránku; chýbajúci preklad sa vráti na angličtinu. Jazykové menu v hlavičke a presmerovanie domovskej stránky podľa jazyka prehliadača pochádzajú z `docs/_includes/`.
