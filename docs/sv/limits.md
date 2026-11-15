---
title: Begränsningar, uppdateringar och villkor
nav_order: 7
lang: "sv"
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Begränsningar, uppdateringar och villkor {#limits-updates-and-terms}

## Läses inte {#not-read}

- **Vem som dödade vem, och skada på soldater per träff.** Dessa färdas i träffresultaten för vapnens och spelarnas tillståndsobjekts fjärranrop (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), vars struktur inte läses; de sparas hela i sidofilen för entiteter. Bara offrens hälsa avkodas.
- **Botens lag.** Ett bottillstånd bär ett tal som kan vara dess lag; inte bekräftat, inte använt.
- **Var en soldat tittar åt sidan** utöver kroppens gir.

## Speluppdateringar {#game-updates}

Läsaren är beroende av motorns repriseformat och en handfull Squad-klass- och egenskapsnamn. Den är inte beroende av egenskapslayouter den inte kan se: repriserna namnger dem själva.

**Vad som kan gå sönder med en Squad-uppdatering:**

- **En motoruppgradering.** Squad gick över till UE 5.7 med v10.4, och det är inte testat där. Uppgraderingen kan ändra buntens huvud, spawn-datan eller `FRepMovement`. Dessa är versionsstyrda i koden där steget är känt. Okända steg (`ENG_PARTIAL_CUSTOM_EXPORTS`, den avslutande rörelsebiten) är fastlagda till vad v10.3.1 gör.
- **Iris-replikering.** Om Squad bytte till Iris skulle strömmen inuti delarna vara ny, och den här läsaren skulle inte läsa den. Squad v10.3.1 använder det klassiska systemet (det kör ReplicationGraph).
- **Omdöpta klasser eller egenskaper.** Om Squad döpt om sina spelar-, lag- eller truppklasser eller deras egenskaper skulle namn eller lag saknas, men positionerna skulle inte göra det.
- **Vad som händer vid fel.** När formatet ändras misslyckas läsaren högljutt med strömfel eller rörelsefel i diagnostiken. Den producerar inte tyst fel positioner: `FRepMovement` godkänns bara när dess bitar stämmer exakt.

## Personuppgifter {#personal-data}

En demo innehåller namn och online-ID:n för alla på servern. Tabellen och matchdokumentet bär namn, inte ID:n. Sidofilerna behåller varje egenskaps bitar, så de innehåller ID:n som demon gör (inte avkodade). Behandla alla som demon själv.

## Licens och källor {#licence-and-sources}

MIT; se [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Allt här skrevs för det här paketet. Ingen kod från tredje part ingår eller länkas: de enda beroendena är pyarrow (Apache-2.0) och numpy (BSD-3-Clause).

Fakta om formatet kom från de här källorna:

- **Unreal.Core** i [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Den beskriver det generiska Unreal-repriselayouten: infoblocket, delarna, bildrutorna, buntarna och exporterna för nätfält.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Dess läsare lästes för layouten så som Squad v10.3.1 skriver den, för versionskontrollerna, och för vilka Squad-klasser som bär lagdata. Dess publicerade testdemos och räkningar av poster användes som en oberoende kontroll. Ingen av dess kod kopierades eller översattes: den här läsaren är uppbyggd på ett annat sätt (ett Python-bitarkiv över hela paket, delvisa buntar sammanfogade bitvis, egenskaper skickade efter namn), och två saker den inte gör hittades här på demos själva: den tredje flaggan för delvisa buntar och den avslutande rörelsebiten.

Squad är ett varumärke för Offworld Industries. Paketet läser filer som en Squad-server skriver; det rör inte spelet, dess kod eller dess arkiv. Offworlds policy för serverlicensiering och administration säger ingenting om inspelning eller analys av demos. Squads EULA förbjuder omvänd utveckling av spelet självt, vilket detta inte gör.
