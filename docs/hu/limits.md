---
title: "Korlátok, frissítések és feltételek"
nav_order: 7
lang: hu
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Korlátok, frissítések és feltételek {#limits-updates-and-terms}

## Nem olvasódik be {#not-read}

- **Ki ölte meg kit, és a katonákon okozott sérülés találatonként.** Ezek a fegyverek és
  játékosállapotok távoli hívásainak találati eredményeiben utaznak (`HitResultsZeroBased`,
  `MulticastOnImpact.Hit`), amelyek szerkezetét nem olvassuk; egészben megmaradnak az entities
  kísérőfájlban. Csak az áldozatok életerejét dekódoljuk.
- **A bot csapata.** Egy bot állapota tartalmaz egy számot, amely lehet a csapata; nincs megerősítve,
  nem használjuk.
- **Hogy egy katona oldalra néz-e** a test forgásán túl.

## Játékfrissítések {#game-updates}

Az olvasó a motor visszajátszási formátumától és néhány Squad-osztály- és tulajdonságnévtől függ.
Nem függ olyan tulajdonságelrendezésektől, amelyeket nem lát: a visszajátszás ezeket maga nevezi meg.

**Mi törhet el egy Squad-frissítéssel:**

- **Motorfrissítés.** A Squad a v10.4-gyel átállt az UE 5.7-re, és ez ott nincs tesztelve. A frissítés
  megváltoztathatja a köteg fejlécét, a megjelenési adatokat vagy a `FRepMovement`-et. Ezek a kódban
  verzióhoz kötöttek ott, ahol a lépés ismert. Az ismeretlen lépések (`ENG_PARTIAL_CUSTOM_EXPORTS`, a
  záró mozgásbit) ahhoz vannak rögzítve, amit a v10.3.1 csinál.
- **Iris-replikáció.** Ha a Squad Irisre váltana, a darabokon belüli folyam új lenne, és ez az olvasó
  nem olvasná. A Squad v10.3.1 a klasszikus rendszert használja (ReplicationGraph-ot futtat).
- **Átnevezett osztályok vagy tulajdonságok.** Ha a Squad átnevezte a játékos-, csapat- vagy rajosztályait
  vagy azok tulajdonságait, a nevek vagy a csapatok hiányozni fognak, de a pozíciók nem.
- **Mi történik hiba esetén.** Ha a formátum megváltozik, az olvasó hangosan elbukik: folyamhibákat vagy
  mozgáshibákat ír a diagnosztikába. Nem ad csendben hibás pozíciókat: a `FRepMovement`-et csak akkor
  fogadja el, ha a bitjei pontosan kiadódnak.

## Személyes adatok {#personal-data}

Egy demó tartalmazza a szerveren lévők mindenkijének nevét és online azonosítóját. A táblázat és a meccs
dokumentuma neveket tartalmaz, nem azonosítókat. A kísérőfájlok minden tulajdonság bitjeit megtartják,
így az azonosítókat úgy tartalmazzák, ahogy a demó (nincsenek dekódolva). Mindegyiket úgy kezelje, mint maga a demót.

## Licenc és források {#licence-and-sources}

MIT; lásd a [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE) fájlt.
Minden itt ehhez a csomaghoz íródott. Harmadik féltől származó kód nincs benne és nincs hivatkozva: az
egyetlen függőségek a pyarrow (Apache-2.0) és a numpy (BSD-3-Clause).

A formátumra vonatkozó tényeket ezektől a forrásoktól kaptuk:

- **Unreal.Core** a [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT)
  projektben. Ez az általános Unreal-visszajátszási elrendezést írja le: az információs blokkot, a darabokat,
  a kereteket, a köteget és a hálózati mezőexportokat.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Az elemzőjét azért olvastuk, hogy
  lássuk az elrendezést, ahogy a Squad v10.3.1 írja, a verzióellenőrzéseket, és azt, hogy mely Squad-osztályok
  hordoznak csapat-adatokat. Publikált tesztdemóit és a számlálásait független ellenőrzésként használtuk. Kódja
  egyikét sem másoltuk vagy fordítottuk le: ez az olvasó más felépítésű (Python bitarchívum a teljes
  csomagokon, a részleges kötegek bitenként összeillesztve, a tulajdonságok név szerint küldve), és két dolgot,
  amit az övé nem csinál, itt találtunk meg magukon a demókon: a harmadik részleges köteg-jelzőt és a záró
  mozgásbitet.

A Squad az Offworld Industries védjegye. Ez a csomag olyan fájlokat olvas, amelyeket a Squad-szerver ír; nem
nyúl a játékhoz, annak kódjához vagy archívumaihoz. Az Offworld szerverlicencelési és adminisztrációs
szabályzata nem mond semmit a demók rögzítéséről vagy elemzéséről. A Squad EULA-ja tiltja a játék
visszafejtését, amit ez nem csinál.
