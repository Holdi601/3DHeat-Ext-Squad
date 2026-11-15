---
title: Begrensninger, oppdateringer og vilkår
nav_order: 7
lang: no
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Begrensninger, oppdateringer og vilkår {#limits-updates-and-terms}

## Ikke lest {#not-read}

- **Hvem som drepte hvem, og skade på soldater per treff.** Disse reiser i treffresultatene av våpnenes og spillertilstandenes fjernkall (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), hvis struktur ikke er lest; de holdes hele i sidefilen for entiteter. Bare ofrenes helse er dekodet.
- **Boten sitt lag.** En bots tilstand har et tall som kan være laget; ikke bekreftet, ikke brukt.
- **Der en soldat ser til siden** utover kroppens gir.

## Spilloppdateringer {#game-updates}

Leseren avhenger av motorens replay-format og et håndfull Squad-klasse- og egenskapsnavn. Den avhenger ikke av egenskapsoppsett den ikke kan se: replayet navngir dem selv.

**Dette kan gå i stykker med en Squad-oppdatering:**

- **En motoroppgradering.** Squad gikk til UE 5.7 med v10.4, og dette er ikke testet der. Oppgraderingen kan endre bunch-hodet, spawn-dataene eller `FRepMovement`. Disse er versjonsstyrt i koden der steget er kjent. Ukjente steg (`ENG_PARTIAL_CUSTOM_EXPORTS`, den avsluttende bevegelsesbiten) er låst til det v10.3.1 gjør.
- **Iris-replikering.** Hvis Squad gikk over til Iris, ville strømmen inne i bitene være ny, og denne leseren ville ikke lese den. Squad v10.3.1 bruker det klassiske systemet (det kjører ReplicationGraph).
- **Omdøpte klasser eller egenskaper.** Hvis Squad ga nytt navn til sine spiller-, lag- eller troppklasser eller deres egenskaper, ville navn eller lag bli borte, men posisjoner ville ikke det.
- **Hva som skjer ved feil.** Når formatet endres, feiler leseren høylytt med strømfeil eller bevegelsesfeil i diagnostikken. Den lager ikke stille feil posisjoner: `FRepMovement` godtas bare når bitene stemmer helt.

## Personopplysninger {#personal-data}

En demo holder navnene og nett-ID-ene til alle på serveren. Tabellen og kampdokumentet har navn, ikke ID-er. Sidefilene beholder hver egenskaps biter, så de holder ID-ene slik demoen gjør (ikke dekodet). Behandle alle sammen som demoen selv.

## Lisens og kilder {#licence-and-sources}

MIT; se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Alt her er skrevet for denne pakken. Ingen tredjepartskode er inkludert eller lenket: de eneste avhengighetene er pyarrow (Apache-2.0) og numpy (BSD-3-Clause).

Fakta om formatet kommer fra disse kildene:

- **Unreal.Core** i [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Den beskriver det generelle Unreal-replay-oppsettet: infoblokken, bitene, rammene, bunchene og eksporten av nettfelt.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Dens parser ble lest for oppsettet slik Squad v10.3.1 skriver det, for versjonskontrollene, og for hvilke Squad-klasser som bærer tropp-data. Dens publiserte testdemoer og telletall ble brukt som en uavhengig kontroll. Ingen av koden ble kopiert eller oversatt: denne leseren er bygget annerledes (et Python-bitarkiv over hele pakker, delvise bunches satt sammen bit for bit, egenskaper sendt etter navn), og to ting den ikke gjør ble funnet her på demoene selv: det tredje flagget for delvise bunches og den avsluttende bevegelsesbiten.

Squad er et varemerke for Offworld Industries. Denne pakken leser filer en Squad-server skriver; den rører ikke spillet, dets kode eller arkiver. Offworld sin serverlisensiering og administrasjonspolicy sier ingenting om opptak eller analyse av demoer. Squad sin EULA forbyr reverse engineering av selve spillet, noe dette ikke gjør.
