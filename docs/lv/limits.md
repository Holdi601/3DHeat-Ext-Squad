---
title: Ierobežojumi, atjauninājumi un noteikumi
nav_order: 7
lang: "lv"
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Ierobežojumi, atjauninājumi un noteikumi {#limits-updates-and-terms}

## Netiek nolasīts {#not-read}

- **Kas kuru nogalināja un bojājumi karavīriem pa trāpījumiem.** Tie ceļo trāpījumu rezultātos
  ieroču un spēlētāju stāvokļa attālajos izsaukumos (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), kuru
  struktūra netiek nolasīta; tie tiek paturēti pilnībā papildfailā entities. Tiek dekodēta tikai upuru veselība.
- **Bota komanda.** Bota stāvoklī ir skaitlis, kas var būt tā komanda; nav apstiprināts, netiek izmantots.
- **Kur karavīrs skatās sāniski** pāri ķermeņa virzienam.

## Spēles atjauninājumi {#game-updates}

Lasītājs ir atkarīgs no motora atkārtošanas formāta un no neliela skaita Squad klašu un īpašību nosaukumu. Tas nav atkarīgs no īpašību izkārtojumiem, ko tas nevar redzēt: tos ieraksts nosauc pats.

**Kas var salūzt, ja Squad tiek atjaunināts:**

- **Motora jauninājums.** Squad ar v10.4 pārgāja uz UE 5.7, un tas šeit nav pārbaudīts. Jauninājums var mainīt grupas galveni, parādīšanās datus vai `FRepMovement`. Tie ir atkarīgi no versijas kodā, kur solis ir zināms. Nezināmi soļi (`ENG_PARTIAL_CUSTOM_EXPORTS`, pēdējais kustības bits) ir piesaistīti tam, ko dara v10.3.1.
- **Iris replikācija.** Ja Squad pārslēgtos uz Iris, straume fragmentos būtu jauna, un šis lasītājs to nenolasītu. Squad v10.3.1 izmanto klasisko sistēmu (tā darbina ReplicationGraph).
- **Pārdēvētas klases vai īpašības.** Ja Squad pārdēvētu savas spēlētāju, komandu vai squad klases vai to īpašības, nosaukumi vai komandas pazustu, bet pozīcijas nē.
- **Kas notiek, ja kaut kas neizdodas.** Kad formāts mainās, lasītājs skaļi neizdodas ar straumes kļūdām vai kustības kļūdām diagnostikā. Tas klusi neražo nepareizas pozīcijas: `FRepMovement` tiek pieņemts tikai tad, kad tā biti precīzi sakrīt.

## Personas dati {#personal-data}

Demo satur visu servera spēlētāju vārdus un tiešsaistes ID. Tabulā un mača dokumentā ir vārdi, nevis ID. Papildfailos ir katra īpašības biti, tāpēc tie satur ID tā, kā tos satur demo (nedekodēti). Izturieties pret visiem šiem failiem tāpat kā pret pašu demo.

## Licence un avoti {#licence-and-sources}

MIT; skat. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Viss šeit ir rakstīts šai pakotnei. Nav iekļauts un nav saistīts neviens trešās puses kods: vienīgās atkarības ir pyarrow (Apache-2.0) un numpy (BSD-3-Clause).

Faktus par formātu guva no šiem avotiem:

- **Unreal.Core** [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Tas apraksta vispārīgo Unreal atkārtošanas izkārtojumu: informācijas bloku, fragmentus, kadrus, grupas un tīkla lauku eksportus.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Tā parsētājs tika lasīts par izkārtojumu, kādu Squad v10.3.1 to raksta, par versiju pārbaudēm un par to, kuras Squad klases satur dalībnieku datus. Tā publicētie testa demo un skaitļi tika izmantoti kā neatkarīga pārbaude. Neviens no tā kodiem nav kopēts vai tulkots: šis lasītājs ir citādi strukturēts (Python bitu arhīvs pār veseliem paketēm, daļējas grupas savienotas pa bitiem, īpašības izsūtītas pēc nosaukuma), un divas lietas, ko tas nedara, tika atrastas šeit uz pašiem demo: trešais daļējas grupas karogs un pēdējais kustības bits.

Squad ir Offworld Industries preču zīme. Šī pakotne nolasa failus, ko raksta Squad serveris; tā neskar spēli, tās kodu vai arhīvus. Offworld servera licencēšanas un administrēšanas politika neko nesaka par demo ierakstīšanu vai analīzi. Squad EULA aizliedz spēles reversēšanu, ko šī pakotne nedara.
