---
title: "Dokument tekme in spremljevalni datoteki"
nav_order: 5
lang: "sl"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Dokument tekme in spremljevalni datoteki {#the-match-document-and-sidecars}

Poleg tabele dobi vsak posnetek `<posnetek>.match.json` in dve spremljevalni datoteki,
`<posnetek>.entities.parquet` in `<posnetek>.packets.parquet`. Pregledovalnik bere
dokument tekme na zavihku Tekma.

## Dokument tekme {#the-match-document}

`<posnetek>.match.json` (dokument tekme) ima na najvišji ravni `map`, `layer`,
`level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`,
`teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`,
`file`, `header`, `chunks`, `stream`, `shots` in `selfCheck` (celoten seznam:
[Priročnik ukazov](../cli-reference.md)). Z besedami: zemljevid in plast, različici igre
in pogona, čas snemanja, dolžina in:

- **ekipe**: številka, frakcija in vse, kar je njihovo stanje posredovalo (tikete,
  razpoložljivosti, poveljnika), ko se je spremenilo;
- **skupine**: številka, ekipa, ime, ustvarjalec, vodja, člani;
- **stanje igre**: ime strežnika in nastavitve, način igre, stanje in id tekme,
  rotacije zemljevidov in plasti, glasovanja, časovniki, dnevno sporočilo;
- **akterji**: vsako vozilo, postavljivi objekt, strelni položaj, skladišče streliva
  in helikopter - razred, kje in kdaj je nastal, kdaj je izginil, čigav je bil in
  njegovo posredovano stanje (zdravje, stanje gradnje, sedeži ...);
- **vrstica za vsakega igralca**: vzorci peš in v vozilih, prehojena razdalja, razredi
  vojakov, ki jih je igral, uporabljena vozila, menjave ekipe, zasedeni sedeži in
  vse, kar je posredovalo stanje igralca (ping, raven, vloga, trenutni sedež ...);
  in vrstico za vsakega bota;
- **dogodki** prešteti, **popis lastnosti** (kako pogosto so bile poslane lastnosti
  posameznega razreda) in **popis oddaljenih klicev**, streli in zadetki, kar **ni**
  bilo prebrano, ter diagnostika bralnika;
- **datoteka in glava**: vsako polje bloka podatkov in glave posnetka, tabela delov,
  tabele izvoza omrežnih polj (`net_field_exports`), razlogi zaprtja kanalov in
  razredi, najdeni za objekte, ki jih izvozi ne poimenujejo (`stream.class_resolution`);
- **samopreverba** (`selfCheck.completeness`, glej [Popolnost](#completeness)).

Spletni identifikatorji (Steam, EOS) so namenoma izpuščeni.

Hiter pogled na pretvorjen posnetek:

```bash
python -c "import json; d = json.load(open('out/<zemljevid>/<posnetek>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Popolnost {#completeness}

Ta bralnik sledi pravilu, ki ga delijo vsi pretvorniki 3DHeat: prebere, kar se da
prebrati zdaj, preostalo ohrani v celoti in pove, koliko vsake vrste je prebral
([Pretvorniki ohranijo vse](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)).
Vsak dokument tekme ima `selfCheck.completeness`: za vsako vrsto elementa, na katerega
naleti v posnetku, koliko jih je bilo `seen` (videno), `decoded` (prebrano),
`partial` (prebrano delno in ohranjeno v celoti), `raw` (ohranjeno samo v celoti) in
`lost` (mora biti 0). Vrste se štejejo tam, kjer jih bralnik sreča: `file.info`,
`chunk.<vrsta>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`,
`export.guid`, `external`, `property:<razred>`, `rpc:<razred>`, `block:<objekt>`,
`subobject.*`.

Na prebranih pravih posnetkih je `lost` 0: njihovih elementov je od sto tisoč do
nekaj milijonov; približno polovica se prebere popolnoma, ostali so delni ali surovi.

**Prebrano** (v tabelo in dokument tekme):

- blok podatkov, glava posnetka (vsako polje; dva neznana zadnja bajta sta ohranjena
  kot šestnajstiška števila), tabela delov;
- vsak okvir, paket in snop (razdeljen v celoti na to, kar nosi), vsak odprt akter
  (s položajem nastanka, rotacijo, merilom in hitrostjo) in zaprt (z razlogom:
  `Destroyed`, `Dormancy`...);
- vsaka replicirana lastnost, kolikor pove njen zapis ([Dekodiranje lastnosti](how-it-works.md#decoding-properties)),
  položaji iz `FRepMovement` in iz gibalne komponente helikopterjev, ranjenci, zdravje
  vozil, sedeži;
- vsak oddaljeni klic po imenu, s parametri, kjer posnetek izvozi skupino funkcije:
  streli (`fire`) in zadetki vozil (`hit`) v tabelo;
- tabele izvoza omrežnih polj in omrežni GUID-i (njihovo število; poti so v
  spremljevalni datoteki entities).

**Ohranjeno surovo** (v celoti, s tem, kar je prebrano, ob strani):

- `<posnetek>.entities.parquet`, stolpci `time`, `type` (`<razred>.<lastnost>`,
  `<razred>.<klic>`, ali ime objekta), `name` (razred akterja), `entity` (mrežni GUID
  akterja, kot `entity` v tabeli), `kind`, `object` (podobjekt), `channel`, `handle`,
  `group` (pot razreda skupine izvoza), `decoded` (JSON), `bits` in `payload` (biti,
  od najnižjega, dopolnjeni do celih bajtov):
  - vsaka posodobitev lastnosti (`kind` `property`), tudi gibanje, s tem, kar je
    dekodirano; surovo samo tam, kjer ni nič dekodirano (neimenovani ročaji,
    strukture, kot je `RotationReplicatedMovement` pri turretih, in lastnosti, ki so
    ostale kot biti);
  - vsak oddaljeni klic in polje custom-delta (`rpc`), parametri dekodirani, kjer je bila
    skupina funkcije izvožena; surovo, kjer ne (`RepInventory`, `PlayerStateData`);
  - vsak vsebinski blok objekta, katerega razreda ni bilo mogoče najti (`block`:
    `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent` ...), z dekodirano glavo;
  - vsak kanal akterja, odprt in zaprt (`open`, `close`), vsak podobjekt, izbrisan ali
    uničen;
  - kontekst, ki ga poznejši dekoder potrebuje, da prebere datoteko sama: vsako
    omrežno polje izvoza (`export.field`: pot skupine, ročaj, ime lastnosti, kontrolna
    vsota) in vsak izvoženi omrežni GUID (`export.guid`: njegova pot, nadrejeni objekt
    in zastavice), ob času, ko ga je tok dal.
- `<posnetek>.packets.parquet`, stolpci `time`, `type`, `name`, `channel`, `offset` (v
  datoteki), `decoded`, `bits`, `payload`: blok podatkov, blok glave, vsak blok kontrolne
  točke (kontrolna točka je stanje vsakega akterja v njenem času, ki ga ima tudi tok od
  začetka), vsak blok dogodkov ter vsak okvir, paket ali snop, ki se ne prebere (en snop
  na posnetek: začetni snop opazovalca, ki je snemal), v celoti.

Vrstice entities so razvrščene po `kind`, `type` in `entity`, vsaka v časovnem
vrstnem redu; za vrstni red toka razvrsti po `time`.

**Ni na voljo:**

- kar strežnik ne snema: vnosi odjemalcev, kar je igralec videl;
- učinki na odjemalcu: oznake zadetkov, zvoki, besedilo seznama ubojev (strežnik
  pošlje klice, ne njihovega prikaza);
- dekodirani spletni ID-ji: ohranjeni so samo kot biti (glej [Osebni podatki](limits.md#personal-data)).
