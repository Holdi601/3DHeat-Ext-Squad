---
title: Mača dokuments un papildfaili
nav_order: 5
lang: "lv"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Mača dokuments un papildfaili {#the-match-document-and-sidecars}

Blakus tabulai katrs demo saņem `<demo>.match.json` un divus papildfailus,
`<demo>.entities.parquet` un `<demo>.packets.parquet`. Skatītājs lasa mača dokumentu savā
Mača cilnē.

## Mača dokuments {#the-match-document}

`<demo>.match.json` (mača dokuments) augšējā līmenī satur `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` un `selfCheck` (pilnais saraksts: [Komandu atsauce](../cli-reference.md)). Vārdos: karte un līmenis, spēles un motora versijas, ieraksta laiks, garums un:

- **komandas**: numurs, frakcija un viss, ko to stāvoklis replicēja (biļetes, pieejamība, komandieris), mainoties;
- **squad**: numurs, komanda, nosaukums, veidotājs, vadītājs, dalībnieki;
- **spēles stāvoklis**: servera nosaukums un iestatījumi, spēles režīms, mača stāvoklis un ID, karšu un līmeņu rotācijas, balsojumi, taimeri, dienas ziņojums;
- **aktori**: katrs transportlīdzeklis, deployable, ierīkojums, munīcijas kaste un helikopters - klase, kur un kad tas parādījās, kad tas aizgāja, kam tas piederēja, un tā replicētais stāvoklis (veselība, būvēšanas stāvoklis, sēdekļi...);
- **rinda katram spēlētājam**: paraugi kājām un transportlīdzekļos, nobrauktais attālums, karavīru klases, ko spēlētājs ir spēlējis, izmantotie transportlīdzekļi, komandu maiņas, ieņemtie sēdekļi un viss, ko spēlētāja stāvoklis replicēja (ping, līmenis, loma, pašreizējais sēdeklis...); un rinda katram botam;
- **notikumi**, kas saskaitīti, **īpašību uzskaite** (cik bieži katras klases īpašības tika nosūtītas) un **attālo izsaukumu uzskaite**, šāvieni un trāpījumi, kas **nav** nolasīts, un lasītāja diagnostika;
- **fails un galvene**: katrs informācijas bloka un demo galvenes lauks, fragmentu tabula, tīkla lauku eksporta tabulas (`net_field_exports`), kanālu aizvēršanas iemesli un klases, kas atrastas objektiem, ko eksporti nenosauc (`stream.class_resolution`);
- **pašpārbaude** (`selfCheck.completeness`, skat. [Pilnība](#completeness)).

Tiešsaistes ID (Steam, EOS) ir apzināti izlaisti.

Ātrs skats uz konvertētu demo:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Pilnība {#completeness}

Šis lasītājs seko noteikumam, ko ievēro visi 3DHeat konvertētāji: dekodēt to, ko var nolasīt tagad, paturēt pārējo pilnībā un pateikt, cik daudz no katra veida tas ir nolasījis ([Konvertētāji saglabā visu](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Katram mača dokumentam ir `selfCheck.completeness`: katram sastaptā vienuma veidam, cik ir `seen` (redzēti), `decoded` (dekodēti), `partial` (dekodēti daļēji un paturēti pilnībā), `raw` (paturēti tikai pilnībā) un `lost` (jābūt 0). Veidi tiek skaitīti tur, kur lasītājs tos sastop: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Īstajos nolasītajos demo `lost` ir 0: to vienumu skaits ir no simtiem tūkstošu līdz miljoniem; apmēram puse dekodējas pilnībā, pārējie ir daļēji vai neapstrādāti.

**Nolasīts** (tabulā un mača dokumentā):

- informācijas bloks, demo galvene (katrs lauks; divi nezināmi beigu baiti tiek saglabāti kā heksadecimāls) un fragmentu tabula;
- katrs kadrs, paketa un grupa (sadalīti pilnībā pēc tā, ko tie satur), katrs atvērtais aktors (ar tā parādīšanās vietu, rotāciju, mērogu un ātrumu) un aizvērtais (ar iemeslu: `Destroyed`, `Dormancy`...);
- katra replicētā īpašība, cik tālu to atļauj tās biti ([Īpašību dekodēšana](how-it-works.md#decoding-properties)), pozīcijas no `FRepMovement` un no helikopteru kustības komponenta, nāves gadījumi, transportlīdzekļu veselība, sēdekļi;
- katrs attālais izsaukums pēc nosaukuma, ar tā parametriem, kur demo eksportē funkcijas grupu: šāvieni (`fire`) un transportlīdzekļu trāpījumi (`hit`) tabulā;
- tīkla lauku eksporta tabulas un tīkla GUID (to skaits; ceļi ir papildfailā entities).

**Paturēts neapstrādāts** (pilnībā, ar to, kas no tā ir nolasīts, blakus):

- `<demo>.entities.parquet`, kolonnas `time`, `type` (`<class>.<property>`, `<class>.<call>` vai objekta nosaukums), `name` (aktora klase), `entity` (aktora tīkla GUID, kā tabulas `entity`), `kind`, `object` (apakšobjekts), `channel`, `handle`, `group` (eksporta grupas klases ceļš), `decoded` (JSON), `bits` un `payload` (biti, no zemākā, aizpildīti līdz pilniem baitiem):
  - katrs īpašības atjauninājums (`kind` `property`), arī kustība, ar to, kas ir dekodēts; neapstrādāts tikai tad, kad nekas nav dekodēts (nenosauktie rokturi, struktūras, piemēram, torņu `RotationReplicatedMovement`, un īpašības, kas palikušas kā biti);
  - katrs attālais izsaukums un pielāgotais delta lauks (`rpc`), parametri dekodēti, kur funkcijas grupa tika eksportēta; neapstrādāts, kur nē (`RepInventory`, `PlayerStateData`);
  - katrs satura bloks objektam, kura klasi nevarēja atrast (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), ar tā galveni dekodētu;
  - katrs aktoru kanāls, kas tika atvērts un aizvērts (`open`, `close`), katrs apakšobjekts, kas tika dzēsts vai iznīcināts;
  - konteksts, ko vēlāks dekodētājs vajag, lai nolasītu failu vienatnē: katrs tīkla lauka eksports (`export.field`: grupas ceļš, rokturis, īpašības nosaukums, kontrolsumma) un katrs eksportētais tīkla GUID (`export.guid`: tā ceļš, ārējais objekts un karogi), tādā laikā, kādā straume tos deva.
- `<demo>.packets.parquet`, kolonnas `time`, `type`, `name`, `channel`, `offset` (failā), `decoded`, `bits`, `payload`: informācijas bloks, galvenes fragments, katrs kontrolpunkta fragments (kontrolpunkts ir katra aktora stāvoklis tā laikā, ko arī straume no sākuma satur), katrs notikumu fragments un katrs kadrs, paketa vai grupa, kas nenolasās (viena grupa katrā demo: servera ierakstītāja pašu skatītāja aktora atvēršanas grupa), pilnībā.

Papildfailu rindas ir sagrupētas pēc `kind`, `type` un `entity`, katra laika secībā; kārto pēc `time`, lai iegūtu straumes secību.

**Nav pieejams:**

- tas, ko servera demo neieraksta: klientu ievades, ko redzēja spēlētājs;
- klienta pusē notiekošie efekti: trāpījumu marķieri, skaņas, nogalināšanas saraksta teksts (serveris sūta izsaukumus, nevis to attēlojumu);
- dekodēti tiešsaistes ID: paturēti tikai kā biti (skat. [Personas dati](limits.md#personal-data)).
