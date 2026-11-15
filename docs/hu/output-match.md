---
title: "A meccsdokumentum és a kísérőfájlok"
nav_order: 5
lang: "hu"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# A meccsdokumentum és a kísérőfájlok {#the-match-document-and-sidecars}

A táblázat mellett minden demó kap egy `<demo>.match.json` fájlt és két kísérőfájlt,
a `<demo>.entities.parquet`-et és a `<demo>.packets.parquet`-et. A megjelenítő a meccs
dokumentumát a Meccs fülén olvassa be (a Meccs fül: `Meccs`).

## A meccsdokumentum {#the-match-document}

A `<demo>.match.json` (a meccsdokumentuma) legfelső szintjén ezek vannak: `map`, `layer`,
`level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`,
`game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`,
`shots` és `selfCheck` (a teljes lista: [Parancsleírás](../cli-reference.md)). Szavakkal: a térkép és a
pálya, a játék és a motor verziója, a rögzítés ideje, a hossz, és:

- **a csapatok**: számuk, frakciójuk, és minden, amit az állapotuk replikált (jegyek, rendelkezésre állások,
  parancsnok), ahogy változott;
- **a rajok**: számuk, csapatuk, nevük, létrehozójuk, vezetőjük, tagjaik;
- **a játék állapota**: a szerver neve és beállításai, a játékmód, a meccs állapota és azonosítója, a térkép-
  és pályarotációk, szavazások, időzítők, a napi üzenet;
- **az aktorok**: minden jármű, telepíthető eszköz, fegyverállás, lőszerláda és helikopter - osztálya, helye
  és ideje a megjelenésekor, az eltűnésének ideje, kié volt, és replikált állapota (életerő, építési állapot,
  ülések...);
- **egy sor minden játékosnak**: minta a gyalogos és a járműves részekből, a megtett távolság, a játszott
  katonaosztályok, a használt járművek, csapatváltások, az elfoglalt ülések, és mindaz, amit a játékosállapot
  replikált (ping, szint, szerep, aktuális ülés...); és egy sor minden botnak;
- **az események** megszámolva, a **tulajdonság-összeírás** (hogy egy-egy osztály tulajdonságait hányszor
  küldték) és a **távoli hívások összeírása**, a lövések és találatok, ami **nem** lett beolvasva, és az
  olvasó diagnosztikája;
- **a fájl és a fejléc**: az információs blokk és a demófejléc minden mezője, a darabtábla, a hálózati
  mezőexport-táblák (`net_field_exports`), a csatornák zárási okai, és azok az osztályok, amelyeket azoknak az
  objektumoknak találtunk, amelyeket az exportok nem neveznek meg (`stream.class_resolution`);
- **az önellenőrzés** (`selfCheck.completeness`, lásd [Teljesség](#completeness)).

Az online azonosítók (Steam, EOS) szándékosan kimaradnak.

Egy konvertált demó gyors megtekintése:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Teljesség {#completeness}

Ez az olvasó azt a szabályt követi, amelyet az összes 3DHeat konverter közösen használ: most dekódolja, ami
már most olvasható, a többit egészben megtartja, és elmondja, hogy az egyes fajtákból mennyit tett így
([A konverterek mindent megtartanak](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Minden
meccsdokumentumában van `selfCheck.completeness`: a demóban talált elemek típusonként megmutatják, hány volt
`seen` (látott), `decoded` (dekódolt), `partial` (részben dekódolt és egészben megtartott), `raw` (csak egészben
megtartott) és `lost` (ennek 0-nak kell lennie). A típusokat ott számolja meg, ahol találkozik velük: `file.info`,
`chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`,
`property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

A beolvasott valódi demókon a `lost` 0: elemeik százezrektől milliókig terjednek; körülbelül fele teljesen
dekódolódik, a többi részleges vagy nyers.

**Beolvasva** (a táblázatba és a meccsdokumentumába):

- az információs blokk, a demófejléc (minden mező; a két ismeretlen záró bájt hexadecimálisan megmarad), a
  darabtábla;
- minden keret, csomag és köteg (egészben szétbontva, abban, amit hordoznak), minden megnyitott aktor (a
  megjelenési helyével, forgatásával, méretarányával és sebességével) és lezárt aktor (az okkal: `Destroyed`,
  `Dormancy`...);
- minden replikált tulajdonság, amennyire a bitjei mondják ([Tulajdonságok dekódolása](how-it-works.md#decoding-properties)),
  a pozíciók a `FRepMovement`-ből és a helikopterek mozgáskomponenséből, a halálesetek, a járművek életereje,
  az ülések;
- minden távoli hívás név szerint, a paramétereivel, ahol a demó exportálja a függvény csoportját: a lövések
  (`fire`) és a járműtalálatok (`hit`) a táblázatba;
- a hálózati mezőexport-táblák és a hálózati GUID-ok (a számuk; az útvonalak az entities kísérőfájlban vannak).

**Nyersen megtartva** (egészben, a beolvasott részével együtt mellette):

- `<demo>.entities.parquet`, oszlopai: `time`, `type` (`<class>.<property>`, `<class>.<call>`, vagy az objektum
  neve), `name` (az aktor osztálya), `entity` (az aktor hálózati GUID-ja, mint a táblázat `entity` oszlopa),
  `kind`, `object` (az alobjektum), `channel`, `handle`, `group` (az exportcsoport osztályútvonala), `decoded`
  (JSON), `bits` és `payload` (a bitek, a legkisebb elöl, teljes bájtokra kitöltve):
  - minden tulajdonságfrissítés (`kind` `property`), a mozgással együtt, azzal, ami dekódolva van; nyers csak
    ott, ahol semmi más nincs (név nélküli kezelők, olyan szerkezetek, mint a torony `RotationReplicatedMovement`,
    és a bitként hagyott tulajdonságok);
  - minden távoli hívás és egyéni delta-mező (`rpc`), a paraméterekkel dekódolva, ahol a függvény csoportja
    exportálva volt; nyersen, ahol nem (`RepInventory`, `PlayerStateData`);
  - minden tartalmi blokk egy olyan objektumtól, amelynek osztályát nem lehetett megtalálni (`block`:
    `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), a fejlécével dekódolva;
  - minden aktor-csatorna megnyitása és lezárása (`open`, `close`), minden alobjektum törlése vagy megsemmisítése;
  - az a kontextus, amelyre egy későbbi dekódolónak szüksége van ahhoz, hogy a fájlt egymagában olvassa: minden
    hálózati mezőexport (`export.field`: csoportútvonal, kezelő, tulajdonságnév, ellenőrzőösszeg) és minden
    exportált hálózati GUID (`export.guid`: az útvonala, külső objektuma és jelzői), abban az időben, ahogy a folyam
    megadta őket.
- `<demo>.packets.parquet`, oszlopai: `time`, `type`, `name`, `channel`, `offset` (a fájlban), `decoded`, `bits`,
  `payload`: az információs blokk, a fejléc-darab, minden ellenőrzőpont-darab (az ellenőrzőpont minden aktor állapota
  az adott időben, amelyet a folyam az elejétől is tartalmaz), minden eseménydarab, és minden keret, csomag vagy köteg,
  amely nem olvasódik be (demónként egy köteg: az ügynök saját megfigyelőjének nyitó köteggé), egészben.

Az entities sorok `kind`, `type` és `entity` szerint csoportosítva, mindegyik időrendben; a folyam sorrendjéhez
rendezd `time` szerint.

**Nem elérhető:**

- ami egy szerverdemó nem rögzít: a kliensek bemenetei, és hogy egy játékos mit látott;
- kliensoldali hatások: találatjelzők, hangok, a gyilkossági lista szövege (a szerver a hívásokat küldi, nem
  azok megjelenítését);
- dekódolt online azonosítók: csak bitekként megtartva (lásd [Személyes adatok](limits.md#personal-data)).
