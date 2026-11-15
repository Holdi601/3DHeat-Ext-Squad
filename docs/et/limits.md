---
title: "Piirangud, uuendused ja tingimused"
nav_order: 7
lang: et
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Piirangud, uuendused ja tingimused {#limits-updates-and-terms}

## Ei loeta {#not-read}

- **Kes kellele tappis ja kui palju kahju tehti sõdurile tabamuse kaupa.** Need liiguvad relvade ja mängijaolekute kaugkäskude tabamustulemustes (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), mille struktuuri ei loeta; need hoitakse lisafailis entities tervena. Dekodeeritakse ainult ohvrite tervis.
- **Boti meeskond.** Boti olek sisaldab numbrit, mis võib olla tema meeskond; ei ole kinnitatud, ei kasutata.
- **Kuhu sõdur külgsuunas vaatab** väljaspool keha pöördenurka.

## Mängu uuendused {#game-updates}

Lugeja sõltub mootori replay-vormingust ja mõnest Squadi klassi- ja omadusenimest. See ei sõltu omaduste paigutustest, mida ta ei näe: replay nimetab need ise.

**Mis võib Squadi uuendusega puruneda:**

- **Mootori uuendus.** Squad läks v10.4-ga üle UE 5.7-le, ja see pole seal testitud. Uuendus võib muuta bunchi päist, spawni andmeid või `FRepMovement`'i. Need on koodis versioonist sõltuvad seal, kus samm on teada. Tundmatud sammud (`ENG_PARTIAL_CUSTOM_EXPORTS`, lõpu liikumisbitt) on seatud sellele, mida v10.3.1 teeb.
- **Iris-replikatsioon.** Kui Squad läheks Irisele, oleks tükkide sees olev voog uus ja seda lugeja ei loeks. Squad v10.3.1 kasutab klassikalist süsteemi (see töötab ReplicationGraphiga).
- **Ümbernimetatud klassid või omadused.** Kui Squad nimetaks ümber mängija-, meeskonna- või squadiklassid või nende omadused, kaoksid nimed ja meeskonnad, aga asukohad mitte.
- **Mis juhtub tõrke korral.** Kui vorming muutub, teatab lugeja valjuhäälselt voo- või liikumisvigadest diagnostikas. See ei anna vaikselt valesid asukohti: `FRepMovement` võetakse vastu ainult siis, kui tema bitid lõppkokkuvõttes täpselt klapivad.

## Isikuandmed {#personal-data}

Demo sisaldab kõigi serveril olevate inimeste nimesid ja veebi-ID-sid. Tabel ja mängu dokument kannavad nimesid, mitte ID-sid. Lisafailid hoiavad iga omaduse bitte, nii et need sisaldavad ID-sid nii nagu demo (dekodeerimata). Kohtle neid kõiki nagu demo ise.

## Litsents ja allikad {#licence-and-sources}

MIT; vaata [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Kõik siin kirjutati selle paketi jaoks. Mitte ühtegi kolmanda osapoole koodi ei ole kaasas ega lingitud: ainsad sõltuvused on pyarrow (Apache-2.0) ja numpy (BSD-3-Clause).

Faktid vormingu kohta pärinevad neist allikatest:

- **Unreal.Core** projektis [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). See kirjeldab üldist Unreali replay-paigutust: infoplokki, tükke, kaadreid, bunche ja võrgu-väljade eksporte.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Selle parserit loeti paigutuse jaoks, nagu Squad v10.3.1 seda kirjutab, versioonikontrollide jaoks ja selle jaoks, millised Squadi klassid kannavad koosseisuandmeid. Selle avaldatud testdemosid ja loendusi kasutati sõltumatu kontrollina. Ühtegi selle koodi ei kopeeritud ega tõlgitud: see lugeja on üles ehitatud teisiti (Pythoni bitiarhiiv terve paketi kohta, osalised bunchid ühendatakse bititi, omadused suunatakse nime järgi), ja kaks asja, mida see ei tee, leiti siin endi demodelt: kolmas osalise bunchi lipp ja lõpu liikumisbitt.

Squad on Offworld Industriesi kaubamärk. See pakett loeb faile, mida Squadi server kirjutab; see ei puuduta mängu, selle koodi ega arhiive. Offworldi serverilitsentsimise ja administreerimise poliitika ei ütle midagi demode salvestamise ja analüüsimise kohta. Squadi EULA keelab mängu enda pöördprojekteerimise, mida see ei tee.
