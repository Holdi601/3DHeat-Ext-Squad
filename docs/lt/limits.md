---
title: "Apribojimai, atnaujinimai ir sąlygos"
nav_order: 7
lang: lt
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Apribojimai, atnaujinimai ir sąlygos {#limits-updates-and-terms}

## Neskaitoma {#not-read}

- **Kas ką nužudė ir žala kareiviams pagal pataikymą.** Tai keliauja per ginklų ir žaidėjo būsenų nuotolinių kvietimų
  pataikymo rezultatus (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), kurių struktūra neskaitoma; jie išsaugomi visi
  šalutiniame veikėjų faile. Dekoduojama tik aukų sveikata.
- **Boto komanda.** Boto būsena turi skaičių, kuris gali būti jo komanda; nepatvirtinta, nenaudojama.
- **Kur kareivis žiūri į šonus** už kūno posūkio ribų.

## Žaidimo atnaujinimai {#game-updates}

Skaitytuvas priklauso nuo variklio įrašo formato ir keleto Squad klasių bei savybių pavadinimų. Jis nepriklauso
nuo savybių išdėstymų, kurių nemato: tuos išdėstymus įrašas pats įvardija.

**Kas gali sugesti atnaujinus Squad:**

- **Variklio atnaujinimas.** Squad perėjo prie UE 5.7 su v10.4, o tai čia neišbandyta. Atnaujinimas gali pakeisti bunch antraštę,
  atsiradimo duomenis ar `FRepMovement`. Tai priklauso nuo versijos kode tose vietose, kur žingsnis žinomas. Nežinomi žingsniai
  (`ENG_PARTIAL_CUSTOM_EXPORTS`, paskutinis judėjimo bitas) fiksuoti pagal tai, ką daro v10.3.1.
- **Iris replikacija.** Jei Squad perjungtų į Iris, srautas dalyse būtų naujas ir šis skaitytuvas jo neskaitytų. Squad v10.3.1
  naudoja klasikinę sistemą (ji veikia su ReplicationGraph).
- **Pervadinti klasės ar savybės.** Jei Squad pervadintų savo žaidėjo, komandos ar būrio klases ar jų savybes, pavadinimų ar
  komandų pasigestų, bet pozicijų – ne.
- **Kas nutinka gedimo atveju.** Kai formatas pasikeičia, skaitytuvas garsiai nutrūksta su srauto ar judėjimo klaidomis diagnostikoje.
  Jis neišduoda tyliai klaidingų pozicijų: `FRepMovement` priimamas tik tada, kai jo bitai tiksliai susideda.

## Asmens duomenys {#personal-data}

Demo saugo visų serveryje esančių žmonių vardus ir tiesioginio ryšio ID. Lentelėje ir rungtynių dokumente yra vardai, ne ID.
Šalutiniai failai saugo kiekvienos savybės bitus, todėl juose ID yra tokie, kaip demo (nedekoduoti). Traktuokite visus juos
kaip patį demo failą.

## Licencija ir šaltiniai {#licence-and-sources}

MIT; žr. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Viskas čia parašyta šiam paketui. Jokio trečiųjų
šalių kodo nėra nei įtraukta, nei susieta: vienintelės priklausomybės yra pyarrow (Apache-2.0) ir numpy (BSD-3-Clause).

Faktai apie formatą paimti iš šių šaltinių:

- **Unreal.Core** iš [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Jame aprašytas bendrasis Unreal įrašo išdėstymas:
  informacijos blokas, dalys, kadrai, bunch'ai ir tinklo lauko eksportai.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Jo skaitytuvas buvo perskaitytas dėl išdėstymo, kaip jį rašo Squad v10.3.1,
  dėl versijos patikrinimų ir dėl to, kurios Squad klasės saugo sąrašo duomenis. Jo paskelbti testiniai demo ir skaičiai buvo naudoti kaip
  nepriklausomas patikrinimas. Nė vienas jo kodas nebuvo nukopijuotas ar išverstas: šis skaitytuvas sukurtas kitaip (Python bitų archyvas
  virš visų paketų, dalinai bunch'ai jungiami bit po bito, savybės skirstomos pagal pavadinimą), o du dalykai, kurių jis nedaro, rasti čia
  pačiuose demo: trečioji dalinio bunch'o žymė ir paskutinis judėjimo bitas.

Squad yra Offworld Industries prekių ženklas. Šis paketas skaito failus, kuriuos rašo Squad serveris; jis nesiskverbia į žaidimą, jo kodą ar archyvus.
Offworld serverių licencijavimo ir administravimo politika nieko nesako apie demo įrašymą ar analizę. Squad EULA draudžia žaidimo atvirkštinę inžineriją,
ko čia nedaroma.
