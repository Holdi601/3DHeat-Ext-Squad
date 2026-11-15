---
title: "Kufizimet, përditësimet dhe kushtet"
nav_order: 7
lang: sq
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Kufizimet, përditësimet dhe kushtet {#limits-updates-and-terms}

## Çfarë nuk lexohet {#not-read}

- **Kush vrau kë, dhe dëmi mbi ushtarët sipas goditjes.** Këto udhëtojnë në rezultatet e goditjeve të thirrjeve në distancë të armëve dhe të gjendjeve të lojtarëve (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), struktura e të cilave nuk lexohet; ruhen të plota në skedarin anësor entities. Dekodohet vetëm shëndeti i viktimave.
- **Skuadra e botit.** Gjendja e një boti mban një numër që mund të jetë skuadra e tij; nuk u konfirmua, nuk përdoret.
- **Ku shikon një ushtar anash** përtej kthesës (yaw) së trupit.

## Përditësimet e lojës {#game-updates}

Lexuesi varet nga formati i riluajtjes së motorit dhe nga një grusht emrash klasash dhe vetish të Squad. Nuk varet nga strukturat e vetive që nuk i sheh: riluajtja i emërton vetë ato.

**Çfarë mund të prishë një përditësim i Squad:**

- **Një përmirësim i motorit.** Squad kaloi në UE 5.7 me v10.4, dhe kjo nuk është provuar atje. Përmirësimi mund të ndryshojë kokën e bunch-it, të dhënat e shfaqjes ose `FRepMovement`. Këto janë të lidhura me versionin në kod aty ku hapi njihet. Hapat e panjohur (`ENG_PARTIAL_CUSTOM_EXPORTS`, biti i fundit i lëvizjes) janë fiksuar sipas asaj që bën v10.3.1.
- **Replikimi Iris.** Nëse Squad kalonte në Iris, rrjedha brenda copave do të ishte e re dhe ky lexues nuk do ta lexonte. Squad v10.3.1 përdor sistemin klasik (ekzekuton ReplicationGraph).
- **Klasa ose veti të riemërtuara.** Nëse Squad riemërtonte klasat e lojtarit, skuadrës ose togës, ose vetitë e tyre, emrat ose skuadrat do të mungonin, por pozicionet jo.
- **Çfarë ndodh kur dështon.** Kur formati ndryshon, lexuesi dështon me zë të lartë, me gabime rrjedhe ose gabime lëvizjeje në diagnostikime. Nuk prodhon në heshtje pozicione të gabuara: `FRepMovement` pranohet vetëm kur bitet i dalin saktësisht.

## Të dhënat personale {#personal-data}

Një demo mban emrat dhe ID-të online të të gjithëve në server. Tabela dhe dokumenti i ndeshjes mbajnë emra, jo ID. Skedarët anësorë ruajnë bitet e çdo vetie, kështu që mbajnë ID-të ashtu si i ka demo (të padekoduara). Trajtoji të gjithë si vetë demon.

## Licenca dhe burimet {#licence-and-sources}

MIT; shih [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Çdo gjë këtu u shkrua për këtë paketë. Nuk përfshihet dhe nuk lidhet kod i palëve të treta: varësitë e vetme janë pyarrow (Apache-2.0) dhe numpy (BSD-3-Clause).

Faktet për formatin erdhën nga këto burime:

- **Unreal.Core** në [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Përshkruan skemën e përgjithshme të riluajtjes së Unreal: bllokun e informacionit, copat, frame-et, bunch-et dhe eksportet e fushave të rrjetit.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Parseri i tij u lexua për skemën ashtu si e shkruan Squad v10.3.1, për kontrollet e versionit, dhe për cilat klasa të Squad mbajnë të dhënat e listës. Demot e tij të provës të botuara dhe numrat e snapshot-eve u përdorën si kontroll i pavarur. Nuk u kopjua dhe nuk u përkthye asnjë kod i tij: ky lexues është strukturuar ndryshe (një arkiv bitesh në Python mbi paketa të plota, bunch-e të pjesshëm të bashkuar bit pas biti, veti të dërguara sipas emrit), dhe dy gjëra që ai nuk i bën u gjetën këtu në vetë demot: flamuri i tretë i bunch-it të pjesshëm dhe biti i fundit i lëvizjes.

Squad është markë tregtare e Offworld Industries. Kjo paketë lexon skedarë që i shkruan një server Squad; nuk prek lojën, kodin e saj ose arkivat e saj. Politika e Offworld për licencimin dhe administrimin e serverëve nuk thotë asgjë për regjistrimin ose analizimin e demove. EULA e Squad ndalon inxhinierinë e kundërt të vetë lojës, gjë që kjo nuk e bën.
