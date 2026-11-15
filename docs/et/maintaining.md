---
title: "Nende dokumentide hooldamine"
nav_order: 91
lang: et
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Nende dokumentide hooldamine {#maintaining-these-docs}

Väljalaske kohta kontrollnimekiri, et leheküljed ei jääks koodist maha.

1. **Genereeri viide uuesti.** `python tools/gen_docs_reference.py` kirjutab
   [Käsu viide](../cli-reference.md) uuesti programmi enda `--help` ja väljundveergude
   järgi. `python tools/gen_docs_reference.py --check` lõpetab koodiga 1, kui
   committitud leht on vananenud.
2. **Loetle, mis muutus.** `git log v<VERSION>..HEAD --oneline`, kus
   `<VERSION>` on viimane välja antud versioon (fail `VERSION` väljalasbel). Anna iga
   uuele funktsioonile, valikule ja väljundveerule koht lehel ning rida
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md)
   jaotisesse **Docs**.
3. **Sõltumatu ülevaatus.** Keegi, kes ei kirjutanud lehti, loeb README-d ja iga muudetud
   lehte, pildid kaasa arvatud, kolm korda: algajana, kes pole kunagi terminali kasutanud,
   8-aastasena ja eksperdina, kes kontrollib iga valikut `--help`-i vastu. Näited kasutavad
   ainult väljamõeldud nimesid ja numbreid.
4. **Paranda** kõik, mida ülevaatus leiab.
5. **Tõlked.** Iga tõlgitud leht salvestab selle inglisekeelse lehe räsi, millest see tehti.
   Tõlgi uuesti need lehed, mille inglisekeelne allikas muutus, seejärel vaata üle iga keel:
   selge tekst, õiged diagrammisildid, samad sõnad, mis vaataja enda tõlgitud liideses.
6. **Käivita testid** (`pytest`).
7. **Lükka üles** ainult omaniku loal.

## Tõlked: käsud {#translations-the-commands}

Sait on tõlgitud 3DHeat vaataja 40 keelde: inglise keeles `docs/`, iga teine keel
kaustas `docs/<lang>/` samade failinimedega. `tools/docs_i18n.py` teeb arvepidamise:

```bash
python tools/docs_i18n.py hashes             # pärast igat inglisekeelset muudatust: salvesta iga lehe räsi
python tools/docs_i18n.py svg-strings        # pärast igat pildimuudatust: tõlgitavad sildid
python tools/docs_i18n.py status             # keele kohta: ajakohased, vananenud, puuduvad lehed
python tools/docs_i18n.py todo --lang de     # saksa keele lehed, mida (uuesti) tõlkida
python tools/docs_i18n.py svg-build --lang de    # saksa pildid failist docs/assets/i18n/svg/de.json
python tools/docs_i18n.py finish --lang de   # märgi saksa lehed nende inglisekeelse räsiga
python tools/docs_i18n.py check              # lõpetab koodiga 1, kui räsid või sildid on vananenud
```

Tõlgi ainult see, mida `todo` loetleb: säilita Markdown, lingid, kood, failide ja veergude
nimed; tõlgi pealkirjad ja pildikirjeldused ning kasuta vaataja enda sõnu tema nuppude ja
paneelide jaoks (tema `src/i18n/locales/<lang>/`). Genereeritud viitelehed ja terminalipildid
jäävad inglise keeles. Saidil ütleb vananenud tõlge seda ja lingib inglisekeelsele lehele;
puuduv tõlge taandub inglise keelele. Päise keelemenüü ja avalehe brauseri keele ümbersuunamine
tulevad kaustast `docs/_includes/`.
