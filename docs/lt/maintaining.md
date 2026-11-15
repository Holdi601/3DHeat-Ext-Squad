---
title: "Šių dokumentų priežiūra"
nav_order: 91
lang: lt
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Šių dokumentų priežiūra {#maintaining-these-docs}

Kontrolinis sąrašas kiekvienam išleidimui, kad puslapiai niekada neatsiliktų nuo kodo.

1. **Perkurkite nuorodą.** `python tools/gen_docs_reference.py` perrašo
   [Komandų nuoroda](../cli-reference.md) pagal programos pačios `--help` ir išvesties stulpelius.
   `python tools/gen_docs_reference.py --check` baigiasi 1, kai įrašytas puslapis pasenęs.
2. **Susikurkite sąrašą to, kas pasikeitė.** `git log v<VERSION>..HEAD --oneline`, kur
   `<VERSION>` yra paskutinė išleista versija (failas `VERSION` išleidimo metu). Kiekvienai naujai funkcijai,
   parinkčiai ir išvesties stulpeliui suteikite vietą puslapyje ir eilutę
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md) **Docs** skyriuje.
3. **Nepriklausoma peržiūra.** Kas nors, kas nerašė puslapių, perskaito README ir kiekvieną pakeistą puslapį,
   įskaitant paveikslėlius, tris kartus: kaip pradedantysis, kuris niekada nenaudojo terminalo, kaip 8 metų vaikas ir kaip
   ekspertas, kuris patikrina kiekvieną parinktį pagal `--help`. Pavyzdžiuose naudojami tik išgalvoti vardai ir skaičiai.
4. **Ištaisykite** viską, ką randa peržiūra.
5. **Vertimai.** Kiekvienas išverstas puslapis įrašo angliško puslapio, iš kurio jis padarytas, maišos reikšmę.
   Iš naujo išverskite puslapius, kurių angliškas šaltinis pasikeitė, tada peržiūrėkite kiekvieną kalbą: aiškus tekstas,
   teisingos diagramų žymos, tie patys žodžiai kaip išverstoje žiūryklės sąsajoje.
6. **Paleiskite testus** (`pytest`).
7. **Įkelkite** tik gavę savininko leidimą.

## Vertimai: komandos {#translations-the-commands}

Svetainė išversta į 40 3DHeat žiūryklės kalbų: anglų kalba yra `docs/`, kiekviena kita kalba – `docs/<lang>/`
su tais pačiais failų pavadinimais. `tools/docs_i18n.py` tvarko apskaitą:

```bash
python tools/docs_i18n.py hashes             # po bet kokio anglų pakeitimo: įrašyti kiekvieno puslapio maišą
python tools/docs_i18n.py svg-strings        # po bet kokio paveikslėlio pakeitimo: žymos, kurias reikia išversti
python tools/docs_i18n.py status             # pagal kalbą: dabartiniai, pasenę, trūkstami puslapiai
python tools/docs_i18n.py todo --lang de     # vokiški puslapiai, kuriuos reikia (iš naujo) išversti
python tools/docs_i18n.py svg-build --lang de    # vokiški paveikslėliai pagal docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # pažymėti vokiškus puslapius jų angliškuoju maišu
python tools/docs_i18n.py check              # baigiasi 1, kai maišos ar žymos pasenusios
```

Verskite tik tai, ką nurodo `todo`: Markdown, nuorodas, kodą, failų ir stulpelių pavadinimus palikite, kaip yra;
verskite antraštes ir paveikslėlių aprašymus, o mygtukams ir skydeliams naudokite paties 3DHeat žiūryklės žodžius
(jo `src/i18n/locales/<lang>/`). Sugeneruoti nuorodų puslapiai ir terminalo paveikslėliai lieka angliški.
Svetainėje pasenęs vertimas tai pasako ir nuves į angliškąjį puslapį; trūkstamas puslapis rodomas angliškai.
Antraštės kalbų meniu ir pagrindinio puslapio naršyklės kalbos peradresavimas ateina iš `docs/_includes/`.
