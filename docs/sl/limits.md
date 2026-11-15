---
title: "Omejitve, posodobitve in pogoji"
nav_order: 7
lang: sl
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Omejitve, posodobitve in pogoji {#limits-updates-and-terms}

## Ni prebrano {#not-read}

- **Kdo je koga ubil in poškodbe vojakov z zadetkom.** Te potujejo v rezultatih zadetkov
  oddaljenih klicev orožij in stanj igralcev (`HitResultsZeroBased`, `MulticastOnImpact.Hit`),
  katerih zgradba ni prebrana; v spremljevalni datoteki entities so ohranjeni v celoti.
  Prebrano je samo zdravje žrtev.
- **Ekipa bota.** Stanje bota nosi številko, ki je morda njegova ekipa; ni potrjeno, ni
  uporabljeno.
- **Kam vojak gleda vstran** onkraj zasuka telesa (yaw).

## Posodobitve igre {#game-updates}

Bralnik je odvisen od formata posnetkov motorja in peščice imen razredov in lastnosti Squad.
Ni odvisen od zapisov lastnosti, ki jih ne vidi: posnetek jih poimenuje sam.

**Kaj se lahko pokvari s posodobitvijo Squad:**

- **Nadgradnja motorja.** Squad je z v10.4 prešel na UE 5.7, to pa ni preizkušeno. Nadgradnja lahko
  spremeni glavo snopa, podatke o nastanku ali `FRepMovement`. Ti so v kodi vezani na različico tam,
  kjer je korak znan. Neznani koraki (`ENG_PARTIAL_CUSTOM_EXPORTS`, zadnji bit gibanja) so vezani na to,
  kar počne v10.3.1.
- **Iris replikacija.** Če bi Squad prešel na Iris, bi bil tok znotraj delov nov in tega bralnika ne bi
  bral. Squad v10.3.1 uporablja klasični sistem (poganja ReplicationGraph).
- **Preimenovani razredi ali lastnosti.** Če bi Squad preimenoval svoje razrede igralca, ekipe ali
  skupine ali njihove lastnosti, bi manjkala imena ali ekipe, položaji pa ne.
- **Kaj se zgodi ob napaki.** Ko se format spremeni, bralnik glasno odpove z napakami toka ali gibanja
  v diagnostiki. Tiho ne ustvari napačnih položajev: `FRepMovement` je sprejet samo, kadar se njegovi
  biti natančno seštejejo.

## Osebni podatki {#personal-data}

Posnetek vsebuje imena in spletne ID-je vseh na strežniku. Tabela in dokument tekme nosita imena, ne
ID-jev. Spremljevalni datoteki hranita vse bite vsake lastnosti, zato hranita ID-je tako, kot jih ima
posnetek (ne dekodirane). Obravnavaj vse kot sam posnetek.

## Licenca in viri {#licence-and-sources}

MIT; glej [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Vse tukaj je bilo
napisano za ta paket. Nobena koda tretjih oseb ni vključena ali povezana: edine odvisnosti sta pyarrow
(Apache-2.0) in numpy (BSD-3-Clause).

Podatki o formatu so prišli iz teh virov:

- **Unreal.Core** v [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor)
  (MIT). Opisuje splošno zgradbo posnetka Unreal: blok podatkov, dele, okvirje, snope in izvoze omrežnih polj.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Njegov bralnik je bil prebran
  zaradi zgradbe, kot jo Squad v10.3.1 zapisuje, zaradi preverjanj različic in zaradi tega, kateri razredi
  Squad nosijo podatke o seznamu igralcev. Njegovi objavljeni testni posnetki in števila posnetkov so bili
  uporabljeni kot neodvisno navzkrižno preverjanje. Nobena njegova koda ni bila kopirana ali prevedena:
  ta bralnik je zgrajen drugače (bitni arhiv v Pythonu nad celotnimi paketi, delni snopi združeni bit za bitom,
  lastnosti razpošiljane po imenu), dve stvari, ki jih ne počne, pa sta bili ugotovljeni na samih posnetkih:
  tretja zastavica delnega snopa in zadnji bit gibanja.

Squad je blagovna znamka Offworld Industries. Ta paket bere datoteke, ki jih zapisuje strežnik Squad; ne
dotika se igre, njene kode ali njenih arhivov. Pravilnik Offworld o licenciranju in upravljanju strežnikov
ne govori o snemanju ali analizi posnetkov. Squadova licenčna pogodba (EULA) prepoveduje povratni inženiring
same igre, kar to ne počne.
