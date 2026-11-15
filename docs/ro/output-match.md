---
title: "Documentul de meci și fișierele auxiliare"
nav_order: 5
lang: "ro"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Documentul de meci și fișierele auxiliare {#the-match-document-and-sidecars}

Lângă tabel, fiecare demo primește `<demo>.match.json` și două fișiere auxiliare,
`<demo>.entities.parquet` și `<demo>.packets.parquet`. Vizualizatorul citește documentul de meci în fila sa Meci.

## Documentul de meci {#the-match-document}

`<demo>.match.json` (documentul de meci) conține la nivelul de sus `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` și `selfCheck` (lista completă: [Referința comenzilor](../cli-reference.md)). Pe scurt: harta și nivelul, versiunile jocului și ale motorului, momentul înregistrării, durata și:

- **echipele**: numărul, fracțiunea și tot ce a replicat starea lor (bilete, disponibilități, comandant), pe măsură ce s-a schimbat;
- **scuadroanele**: numărul, echipa, numele, creatorul, liderul, membrii;
- **starea jocului**: numele și setările serverului, modul de joc, starea și identificatorul meciului, rotațiile hărților și ale nivelurilor, voturile, cronometrele, mesajul zilei;
- **actorii**: fiecare vehicul, dispozitiv desfășurabil, punct de tragere, cutie de muniție și elicopter - clasa, unde și când a apărut, când a dispărut, al cui era și starea sa replicată (sănătate, stare de construcție, locuri...);
- **o linie pentru fiecare jucător**: mostre pe jos și în vehicule, distanța parcursă, clasele de soldat jucate, vehiculele folosite, schimbările de echipă, locurile ocupate și tot ce a replicat starea jucătorului (ping, nivel, rol, locul curent...); și o linie pentru fiecare bot;
- **evenimentele** numărate, **recensământul proprietăților** (de câte ori a fost trimisă fiecare proprietate a fiecărei clase) și **recensământul apelurilor de la distanță**, focurile și loviturile, ce **nu** s-a citit, și diagnosticele cititorului;
- **fișierul și antetul**: fiecare câmp al blocului de informații și al antetului demo-ului, tabelul bucăților, tabelele de export ale câmpurilor de rețea (`net_field_exports`), motivele de închidere ale canalelor și clasele găsite pentru obiectele pe care exporturile nu le numesc (`stream.class_resolution`);
- **autoverificarea** (`selfCheck.completeness`, vedeți [Completitudinea](#completeness)).

ID-urile online (Steam, EOS) sunt lăsate deoparte intenționat.

O privire rapidă asupra unui demo convertit:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Completitudinea {#completeness}

Acest cititor urmează regula pe care o respectă toate convertoarele 3DHeat: decodează ce se poate citi acum, păstrează restul întreg și spune câtul din fiecare fel a fost citit ([Convertoarele păstrează tot](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Fiecare document de meci are `selfCheck.completeness`: pentru fiecare tip de element întâlnit în demo, câte au fost `seen` (văzute), `decoded` (decodate), `partial` (decodate parțial și păstrate întregi), `raw` (doar păstrate întregi) și `lost` (trebuie să fie 0). Tipurile se numără acolo unde le întâlnește cititorul: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

La demo-urile reale citite, `lost` este 0: elementele lor se numără de la sute de mii la milioane; aproximativ jumătate se decodează complet, restul sunt parțiale sau brute.

**Citit** (în tabel și în documentul de meci):

- blocul de informații, antetul demo-ului (fiecare câmp; doi octeți finali necunoscuți sunt păstrați în hexazecimal), tabelul bucăților;
- fiecare cadru, pachet și pachet parțial (bunch) (împărțit întreg în ce conține), fiecare actor deschis (cu locul său de apariție, rotația, scara și viteza) și închis (cu motivul: `Destroyed`, `Dormancy`...);
- fiecare proprietate replicată, pe cât spun biții ei ([Decodarea proprietăților](how-it-works.md#decoding-properties)), pozițiile din `FRepMovement` și din componenta de mișcare a elicopterelor, victimele, sănătatea vehiculelor, locurile;
- fiecare apel de la distanță după nume, cu parametrii săi acolo unde demo-ul exportă grupul funcției: focurile (`fire`) și loviturile vehiculelor (`hit`) în tabel;
- tabelele de export ale câmpurilor de rețea și identificatorii net GUID (numărul lor; căile sunt în fișierul auxiliar cu entități).

**Păstrat brut** (întreg, cu ce s-a citit din el alături):

- `<demo>.entities.parquet`, coloanele `time`, `type` (`<class>.<property>`, `<class>.<call>`, sau numele obiectului), `name` (clasa actorului), `entity` (net GUID-ul actorului, ca `entity` din tabel), `kind`, `object` (subobiectul), `channel`, `handle`, `group` (calea clasei grupului de export), `decoded` (JSON), `bits` și `payload` (biții, de la cel mai puțin semnificativ, completați până la octeți întregi):
  - fiecare actualizare de proprietate (`kind` `property`), inclusiv mișcarea, cu ce s-a decodat; brută doar acolo unde nu se decodează nimic (handle-uri nenumite, structuri precum `RotationReplicatedMovement` al turelelor și proprietăți lăsate ca biți);
  - fiecare apel de la distanță și câmp delta personalizat (`rpc`), cu parametrii decodați acolo unde grupul funcției a fost exportat; brut acolo unde nu (`RepInventory`, `PlayerStateData`);
  - fiecare bloc de conținut al unui obiect a cărui clasă nu a putut fi găsită (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), cu antetul său decodat;
  - fiecare canal de actor deschis și închis (`open`, `close`), fiecare subobiect șters sau distrus;
  - contextul pe care îl cere un decodor ulterior ca să citească fișierul singur: fiecare export de câmp de rețea (`export.field`: calea grupului, handle-ul, numele proprietății, suma de control) și fiecare net GUID exportat (`export.guid`: calea, părintele și indicatorii săi), la momentul la care le-a dat fluxul.
- `<demo>.packets.parquet`, coloanele `time`, `type`, `name`, `channel`, `offset` (în fișier), `decoded`, `bits` și `payload`: blocul de informații, bucata de antet, fiecare bucată de punct de control (un punct de control este starea fiecărui actor la momentul său, pe care fluxul de la început o conține și el), fiecare bucată de eveniment și fiecare cadru, pachet sau pachet parțial care nu se citește (un singur pachet parțial per demo: pachetul de deschidere al actorului de spectator al înregistratorului), întreg.

Rândurile fișierului auxiliar cu entități sunt grupate după `kind`, `type` și `entity`, fiecare în ordinea timpului; sortați după `time` pentru ordinea fluxului.

**Nu este disponibil:**

- ce nu înregistrează un demo de server: intrările clienților, ce a văzut un jucător;
- efectele de partea clientului: marcajele de lovitură, sunetele, textul listei de eliminări (serverul trimite apelurile, nu afișarea lor);
- ID-urile online decodate: păstrate doar ca biți (vedeți [Date personale](limits.md#personal-data)).
