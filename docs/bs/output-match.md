---
title: "Dokument meča i pomoćne datoteke"
nav_order: 5
lang: bs
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Dokument meča i pomoćne datoteke {#the-match-document-and-sidecars}

Uz tabelu, svaki demo dobija `<demo>.match.json` i dvije pomoćne datoteke,
`<demo>.entities.parquet` i `<demo>.packets.parquet`. Preglednik čita
dokument meča u kartici Meč.

## Dokument meča {#the-match-document}

`<demo>.match.json` (dokument meča) na najvišem nivou sadrži `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` i `selfCheck` (puna lista: [Referenca naredbi](../cli-reference.md)). Riječima: mapu i sloj, verzije igre i enginea, vrijeme snimanja, trajanje, i:

- **timovi**: broj, frakcija i sve što je njihovo stanje replicirao (tiketi, dostupnosti, komandant) kako se mijenjalo;
- **odredi**: broj, tim, ime, tvorac, vođa, članovi;
- **stanje igre**: ime servera i postavke, način igre, stanje i id meča, rotacije mapa i slojeva, glasanja, tajmeri, poruka dana;
- **akteri**: svako vozilo, postavljivi objekat, utvrđeni položaj, sanduk s municijom i helikopter - klasa, gdje i kad je stvoren, kad je otišao, čiji je, i njegovo replicirano stanje (zdravlje, stanje gradnje, sjedala...);
- **red za svakog igrača**: uzorci pješice i u vozilima, pređena udaljenost, odigrane klase vojnika, korištena vozila, promjene tima, zauzeta sjedala, i sve što je stanje igrača replicirano (ping, nivo, uloga, trenutno sjedalo...); te red za svakog bota;
- **događaji** izbrojani, **popis svojstava** (koliko je puta poslano svojstvo svake klase) i **popis udaljenih poziva**, hici i pogoci, ono što **nije** pročitano, te dijagnostika čitača;
- **datoteka i zaglavlje**: svako polje bloka informacija i zaglavlja demoa, tabela chunk-ova, tabele izvoza mrežnih polja (`net_field_exports`), razlozi zatvaranja kanala i klase pronađene za objekte koje izvozi ne imenuju (`stream.class_resolution`);
- **samoprovjera** (`selfCheck.completeness`, vidi [Potpunost](#completeness)).

Online ID-ovi (Steam, EOS) namjerno su izostavljeni.

Brz pogled na pretvoreni demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Potpunost {#completeness}

Ovaj čitač slijedi pravilo koje dijele svi 3DHeat konverteri: dekodiraj što se sada može pročitati, ostatak čuvaj cjelovit i reci koliko si čega uradio ([Konverteri čuvaju sve](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Svaki dokument meča ima `selfCheck.completeness`: po vrsti stavke susretnute u demou, koliko ih je bilo `seen` (viđeno), `decoded` (dekodirano), `partial` (dijelom dekodirano i cjelovito sačuvano), `raw` (samo cjelovito sačuvano) i `lost` (izgubljeno; mora biti 0). Vrste se broje tamo gdje ih čitač susretne: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Na stvarnim pročitanim demoima `lost` je 0: njihove stavke idu od stotina hiljada do miliona; otprilike pola se dekodira u potpunosti, ostatak je djelomičan ili sirov.

**Pročitano** (u tabelu i dokument meča):

- blok informacija, zaglavlje demoa (svako polje; dva završna nepoznata bajta čuvaju se kao heksadecimalno), tabela chunk-ova;
- svaki frame, paket i bunch (razdvojeni cjelovito na ono što nose), svaki otvoren akter (s lokacijom spawna, rotacijom, skalom i brzinom) i zatvoren (s razlogom: `Destroyed`, `Dormancy`...);
- svako replicirano svojstvo, koliko god njegovi bitovi kažu ([Dekodiranje svojstava](how-it-works.md#decoding-properties)), pozicije iz `FRepMovement` i iz komponente kretanja helikoptera, žrtve, zdravlje vozila, sjedala;
- svaki udaljeni poziv po imenu, s parametrima gdje demo izvozi grupu funkcije: hici (`fire`) i pogoci u vozila (`hit`) u tabelu;
- tabele izvoza mrežnih polja i mrežni GUID-ovi (njihov broj; putanje su u pomoćnoj datoteci entiteta).

**Sačuvano sirovo** (cjelovito, s pročitanim dijelom pored):

- `<demo>.entities.parquet`, kolone `time`, `type` (`<class>.<property>`, `<class>.<call>` ili ime objekta), `name` (klasa aktera), `entity` (net GUID aktera, kao `entity` tabele), `kind`, `object` (podobjekat), `channel`, `handle`, `group` (putanja klase grupe izvoza), `decoded` (JSON), `bits` i `payload` (bitovi, najniži prvi, dopunjeni do cijelih bajtova):
  - svako ažuriranje svojstva (`kind` `property`), uključujući kretanje, s onim što je dekodirano; sirovo samo tamo gdje ništa nije dekodirano (neimenovani handle-ovi, strukture poput `RotationReplicatedMovement` kupola i svojstva ostavljena kao bitovi);
  - svaki udaljeni poziv i polje s prilagođenom razlikom (`rpc`), parametri dekodirani gdje je grupa funkcije izvezena; sirovo gdje nije (`RepInventory`, `PlayerStateData`);
  - svaki blok sadržaja objekta čija se klasa nije mogla naći (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), sa dekodiranim zaglavljem;
  - svaki otvoren i zatvoren kanal aktera (`open`, `close`), svaki obrisan ili uništen podobjekat;
  - kontekst koji kasniji dekoder treba da bi sam pročitao datoteku: svaki izvoz mrežnog polja (`export.field`: putanja grupe, handle, ime svojstva, kontrolni zbir) i svaki izvezeni mrežni GUID (`export.guid`: njegova putanja, outer i zastavice), u trenutku kad ih je tok dao.
- `<demo>.packets.parquet`, kolone `time`, `type`, `name`, `channel`, `offset` (u datoteci), `decoded`, `bits`, `payload`: blok informacija, chunk zaglavlja, svaki chunk kontrolne tačke (kontrolna tačka je stanje svakog aktera u svom trenutku, što drži i tok od početka), svaki chunk događaja, te svaki frame, paket ili bunch koji se ne čita (jedan bunch po demou: početni bunch vlastitog posmatrača snimača), cjelovito.

Redovi entiteta grupirani su po `kind`, `type` i `entity`, svaki u vremenskom redoslijedu; sortiraj po `time` za redoslijed toka.

**Nije dostupno:**

- ono što serverski demo ne snima: unosi klijenata, ono što je igrač vidio;
- efekti na strani klijenta: oznake pogodaka, zvukovi, tekst kill feeda (server šalje pozive, ne njihov prikaz);
- dekodirani online ID-ovi: čuvaju se samo kao bitovi (vidi [Lični podaci](limits.md#personal-data)).
