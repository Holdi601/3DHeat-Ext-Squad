---
title: Begrænsninger, opdateringer og vilkår
nav_order: 7
lang: da
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Begrænsninger, opdateringer og vilkår {#limits-updates-and-terms}

## Ikke læst {#not-read}

- **Hvem der dræbte hvem, og skade på soldater ved træf.** Disse rejser i træfresultaterne fra våbnenes og spillertilstandenes remote calls (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), hvis struktur ikke læses; de gemmes helt i entitets-sidefilen. Kun ofrenes helbred afkodes.
- **Botens hold.** En bots tilstand bærer et tal, der kan være dens hold; ikke bekræftet, ikke brugt.
- **Hvor en soldat kigger sidelæns** ud over kroppens yaw.

## Spilopdateringer {#game-updates}

Læseren afhænger af motorens replay-format og en håndfuld Squad-klassenavne og egenskabsnavne. Den afhænger ikke af egenskabslayouts, den ikke kan se: replayen navngiver dem selv.

**Hvad der kan gå i stykker med en Squad-opdatering:**

- **En motoropgradering.** Squad gik til UE 5.7 med v10.4, og det er ikke testet dér. Opgraderingen kan ændre bunch-headeren, spawn-data eller `FRepMovement`. Disse er versionsstyret i koden, hvor skridtet kendes. Ukendte skridt (`ENG_PARTIAL_CUSTOM_EXPORTS`, den afsluttende bevægelsesbit) er fastlagt til det, v10.3.1 gør.
- **Iris-replikering.** Hvis Squad skiftede til Iris, ville streamen inde i bidderne være ny, og denne læser ville ikke kunne læse den. Squad v10.3.1 bruger det klassiske system (det kører ReplicationGraph).
- **Omdøbte klasser eller egenskaber.** Hvis Squad omdøbte sine spiller-, hold- eller squadklasser eller deres egenskaber, ville navne eller hold forsvinde, men positionerne ville ikke.
- **Hvad der sker ved fejl.** Når formatet ændres, fejler læseren højlydt med streamfejl eller bevægelsesfejl i diagnosticeringen. Den producerer ikke stille forkerte positioner: `FRepMovement` accepteres kun, når dens bits går præcist op.

## Personlige data {#personal-data}

En demo indeholder navnene og online-ID'erne på alle på serveren. Tabellen og kampdokumentet bærer navne, ikke ID'er. Sidefilerne gemmer hver egenskabs bits, så de holder ID'erne, som demoen gør (ikke afkodet). Behandl alle dem som selve demoen.

## Licens og kilder {#licence-and-sources}

MIT; se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Alt her er skrevet til denne pakke. Ingen kode fra tredjepart er inkluderet eller linket: de eneste afhængigheder er pyarrow (Apache-2.0) og numpy (BSD-3-Clause).

Fakta om formatet kom fra disse kilder:

- **Unreal.Core** i [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Den beskriver det generiske Unreal-replay-layout: infoblokken, bidderne, frames, bunches og eksporterne af netfelter.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Dets parser blev læst for layoutet, sådan som Squad v10.3.1 skriver det, for versionstjekkene, og for hvilke Squad-klasser der bærer rosterdata. Dets udgivne testdemoer og optællinger af snapshots blev brugt som uafhængig krydstjek. Ingen af dets kode blev kopieret eller oversat: denne læser er opbygget anderledes (et Python-bit-arkiv over hele pakker, delvise bunches samlet bitvis, egenskaber sendt videre efter navn), og to ting, det ikke gør, blev fundet her på demoerne selv: det tredje delvise bunch-flag og den afsluttende bevægelsesbit.

Squad er et varemærke tilhørende Offworld Industries. Denne pakke læser filer, som en Squad-server skriver; den rører ikke spillet, dets kode eller dets arkiver. Offworlds politik for serverlicensering og administration siger intet om optagelse eller analyse af demoer. Squads EULA forbyder reverse engineering af selve spillet, og det gør denne pakke ikke.
