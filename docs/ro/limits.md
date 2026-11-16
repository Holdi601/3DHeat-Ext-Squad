---
title: "Limite, actualizări și condiții"
nav_order: 7
lang: "ro"
source: limits.md
source_hash: "8a9c7c448411"
nav_exclude: true
search_exclude: true
---
# Limite, actualizări și condiții {#limits-updates-and-terms}

## Ce nu se citește {#not-read}

- **Cine l-a ucis pe cine și daunele aduse soldaților lovitură cu lovitură.** Acestea circulă în rezultatele loviturilor din apelurile de la distanță ale armelor și ale stărilor jucătorilor (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), a căror structură nu este citită; ele sunt păstrate întregi în fișierul auxiliar cu entități. Doar sănătatea victimelor este decodată.
- **Echipa botului.** Starea unui bot poartă un număr care poate fi echipa lui; neconfirmat, nefolosit.
- **Unde se uită un soldat într-o parte**, dincolo de girația corpului.

## Actualizările jocului {#game-updates}

Cititorul depinde de formatul de replay al motorului și de o mână de nume de clase și proprietăți Squad. Nu depinde de aspectele proprietăților pe care nu le poate vedea: replay-ul le numește singur.

**Ce poate strica o actualizare Squad:**

- **O actualizare a motorului.** Squad a trecut la UE 5.7 odată cu v10.4, iar acest lucru nu a fost testat acolo. Actualizarea poate schimba antetul pachetelor, datele de apariție sau `FRepMovement`. Acestea sunt condiționate de versiune în cod acolo unde pasul este cunoscut. Pașii necunoscuți (`ENG_PARTIAL_CUSTOM_EXPORTS`, bitul final al mișcării) sunt fixați la ceea ce face v10.3.1.
- **Replicarea Iris.** Dacă Squad ar trece la Iris, fluxul din interiorul bucăților ar fi nou, iar acest cititor nu l-ar citi. Squad v10.3.1 folosește sistemul clasic (care rulează ReplicationGraph).
- **Clase sau proprietăți redenumite.** Dacă Squad și-ar redenumi clasele de jucător, de echipă sau de scuadron ori proprietățile lor, numele sau echipele ar lipsi, dar pozițiile nu.
- **Ce se întâmplă la eșec.** Când formatul se schimbă, cititorul eșuează vizibil, cu erori de flux sau de mișcare în diagnostice. Nu produce în liniște poziții greșite: `FRepMovement` se acceptă doar când biții săi se adună exact.

## Date personale {#personal-data}

Un demo conține numele și ID-urile online ale tuturor celor de pe server. Tabelul și documentul de meci conțin nume, nu ID-uri. Fișierele auxiliare păstrează biții fiecărei proprietăți, deci conțin ID-urile așa cum le are demo-ul (nedecodate). Tratați-le pe toate ca pe demo-ul însuși.

## Licență și surse {#licence-and-sources}

MIT; vedeți [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Totul de aici a fost scris pentru acest pachet. Nu este inclus și nici legat niciun cod terț: singurele dependențe sunt pyarrow (Apache-2.0) și numpy (BSD-3-Clause).

Informațiile despre format provin din aceste surse:

- **Unreal.Core** din [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Descrie aspectul generic al replay-urilor Unreal: blocul de informații, bucățile, cadrele, pachetele și exporturile câmpurilor de rețea.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Parserul său a fost citit pentru aspectul pe care îl scrie Squad v10.3.1, pentru verificările de versiune și pentru care clase Squad poartă date de tabel. Demo-urile sale de test și numărătorile de instantanee au servit drept verificare independentă. Niciun cod de-al său nu a fost copiat sau tradus: acest cititor este structurat altfel (o arhivă de biți Python peste pachete întregi, pachete parțiale unite pe biți, proprietăți trimise după nume), iar două lucruri pe care el nu le face au fost găsite aici, pe chiar demo-urile: al treilea indicator al pachetelor parțiale și bitul final al mișcării.

Acest pachet citește fișierele demo pe care le scrie un server Squad; nu atinge jocul, codul sau arhivele acestuia, iar nimic din joc nu este inclus sau redistribuit. Ce scrie rămâne pe mașina dumneavoastră.

3DHeat nu este afiliat cu Offworld Industries și nu este aprobat de Offworld Industries. Squad și numele și mărcile asociate aparțin proprietarilor lor.

Deținători de drepturi: deschideți un issue la <https://github.com/Holdi601/3DHeat-Ext-Squad/issues> - răspundem repede și eliminăm orice la cerere.
