---
title: "A dokumentáció karbantartása"
nav_order: 91
lang: hu
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# A dokumentáció karbantartása {#maintaining-these-docs}

Kiadásonként egy ellenőrzőlista, hogy az oldalak soha ne maradjanak le a kódtól.

1. **A referencia újragenerálása.** A `python tools/gen_docs_reference.py` újraírja a
   [Parancsleírás](../cli-reference.md) oldalt a program saját `--help` kimenetéből és
   a kimeneti oszlopokból. A `python tools/gen_docs_reference.py --check` 1 kóddal lép ki, ha
   a bekötött oldal elavult.
2. **Felsorolni, mi változott.** `git log v<VERSION>..HEAD --oneline`, ahol a `<VERSION>` a
   legutóbbi kiadott verzió (a `VERSION` fájl a kiadáskor). Minden új funkciónak, kapcsolónak és
   kimeneti oszlopnak legyen helye egy oldalon, és sora a
   [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md) **Docs**
   szakaszában.
3. **Független átnézés.** Valaki, aki nem írta az oldalakat, háromszor olvassa végig a
   README-t és minden módosult oldalt, a képekkel együtt: mint olyan kezdő, aki sosem használt
   terminált; mint egy nyolcéves; és mint szakértő, aki minden kapcsolót összevet a `--help`-pel.
   A példák csak kitalált neveket és számokat használnak.
4. **Javítani** mindent, amit az átnézés talál.
5. **Fordítások.** Minden lefordított oldal rögzíti annak az angol oldalnak a hash-ét, amelyből
   készült. Újra fordítandók azok az oldalak, amelyeknek az angol forrása megváltozott, majd minden
   nyelvet át kell nézni: világos szöveg, helyes ábrafeliratok, és ugyanazok a szavak, mint a 3DHeat
   megjelenítő saját lefordított felületén.
6. **A tesztek futtatása** (`pytest`).
7. **Csak a tulajdonos jóváhagyása után** tolja fel (push).

## Fordítások: a parancsok {#translations-the-commands}

Az oldal a 3DHeat megjelenítő 40 nyelvére van fordítva: az angol a `docs/` mappában, minden más nyelv a
`docs/<lang>/` mappában, ugyanazokkal a fájlnevekkel. A `tools/docs_i18n.py` végzi a nyilvántartást:

```bash
python tools/docs_i18n.py hashes             # bármilyen angol változás után: minden oldal hash-ének rögzítése
python tools/docs_i18n.py svg-strings        # bármilyen képváltozás után: a lefordítandó feliratok
python tools/docs_i18n.py status             # nyelvenként: naprakész, elavult, hiányzó oldalak
python tools/docs_i18n.py todo --lang de     # a német oldalak, amelyeket (újra) le kell fordítani
python tools/docs_i18n.py svg-build --lang de    # a német képek a docs/assets/i18n/svg/de.json alapján
python tools/docs_i18n.py finish --lang de   # a német oldalak bélyegzése az angol hash-sel
python tools/docs_i18n.py check              # 1 kóddal lép ki, ha a hash-ek vagy a feliratok elavultak
```

Csak azt fordítsa, amit a `todo` felsorol: a Markdownt, a linkeket, a kódot, a fájl- és oszlopneveket
hagyja úgy, ahogy vannak; fordítsa a címeket és a képleírásokat; a 3DHeat megjelenítő gombjainak és
paneljeinek saját szavait használja (a `src/i18n/locales/<lang>/` mappából). A generált referenciaoldalak
és a terminálképek angolok maradnak. A webhelyen az elavult fordítás ezt jelzi, és az angol oldalra
hivatkozik; a hiányzó oldal visszaesik az angolra. A fejléc nyelvmenüjét és a főoldal böngészőnyelv-átirányítását
a `docs/_includes/` adja.
