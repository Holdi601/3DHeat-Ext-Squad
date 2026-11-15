---
title: Limiti, aġġornamenti u termini
nav_order: 7
lang: mt
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Limiti, aġġornamenti u termini {#limits-updates-and-terms}

## Ma jinqarax {#not-read}

- **Min qatel lil min, u dannu lis-suldati b'daqqa.** Dawn jivvjaġġaw fir-riżultati tad-daqqiet tas-sejħiet remoti tal-armi u tal-player states (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), li l-istruttura tagħhom ma tinqarax; jinżammu sħaħ fis-sidecar tal-entities. Tiddekodifika biss is-saħħa tal-vittmi.
- **It-tim tal-bot.** L-istat ta' bot iġorr numru li jista' jkun it-tim tiegħu; mhux ikkonfermat, mhux użat.
- **Fejn iħares suldat lejn il-ġenb** lil hinn mill-yaw tal-ġisem.

## Aġġornamenti tal-logħba {#game-updates}

Il-qarrej jiddependi mill-format tar-replay tal-magna u minn ftit ismijiet ta' klassijiet u proprjetajiet ta' Squad. Ma jiddependix minn layouts ta' proprjetajiet li ma jistax jaraw: ir-replay innifsu jsemmihom.

**X'jista' jkisser aġġornament ta' Squad:**

- **Aġġornament tal-magna.** Squad mexa għal UE 5.7 mal-v10.4, u dan mhux ittestjat hemmhekk. L-aġġornament jista' jbiddel l-header tal-bunch, id-dejta tal-ispawn jew `FRepMovement`. Dawn huma ggwidati mill-verżjoni fil-kodiċi fejn il-pass huwa magħruf. Passi mhux magħrufa (`ENG_PARTIAL_CUSTOM_EXPORTS`, il-bit tal-moviment fl-aħħar) huma mwaħħla ma' dak li jagħmel v10.3.1.
- **Replikazzjoni Iris.** Jekk Squad jaqleb għal Iris, l-istream ġewwa l-chunks ikun ġdid u dan il-qarrej ma jaqrahx. Squad v10.3.1 juża s-sistema klassika (iħaddem ReplicationGraph).
- **Klassijiet jew proprjetajiet b'isem ġdid.** Jekk Squad jibdel l-isem tal-klassijiet tal-plejer, tat-tim jew tal-iskwadra jew tal-proprjetajiet tagħhom, l-ismijiet jew it-timijiet jonqsu, imma l-pożizzjonijiet le.
- **X'jiġri meta jfalli.** Meta l-format jinbidel, il-qarrej jfalli b'mod qawwi bi stream errors jew movement errors fid-dijanjostika. Ma jipproduċix pożizzjonijiet ħżiena bil-kwiet: `FRepMovement` jiġi aċċettat biss meta l-bits tiegħu jaqblu eżatt.

## Dejta personali {#personal-data}

Demo fiha l-ismijiet u l-online IDs ta' kulħadd fuq is-server. It-tabella u d-dokument tal-partita jġorru ismijiet, mhux IDs. Is-sidecars iżommu l-bits ta' kull proprjetà, għalhekk fihom l-IDs kif inhuma fid-demo (mhux iddekodifikati). Ittratta lil kollha bħad-demo nnifisha.

## Liċenzja u sorsi {#licence-and-sources}

MIT; ara [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Kull ħaġa hawn inkitbet għal dan il-pakkett. Ebda kodiċi ta' terzi mhu inkluż jew marbut: l-uniċi dipendenzi huma pyarrow (Apache-2.0) u numpy (BSD-3-Clause).

Il-fatti dwar il-format ġew minn dawn is-sorsi:

- **Unreal.Core** f'[FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Jiddeskrivi l-layout ġeneriku tar-replay ta' Unreal: l-info block, chunks, frames, bunches u net field exports.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Il-parser tiegħu nqara għal-layout kif jikteb Squad v10.3.1, għall-verifiki tal-verżjoni, u għal liema klassijiet ta' Squad iġorru d-dejta tar-roster. Id-demos tat-test tiegħu ppubblikati u l-għadd tas-snapshots intużaw bħala kontroll indipendenti. Ebda kodiċi tiegħu ma ġie kkopjat jew tradott: dan il-qarrej huwa strutturat differenti (arkivju tal-bits ta' Python fuq pakketti sħaħ, bunches parzjali magħquda bit-bit, proprjetajiet mibgħuta skont l-isem), u żewġ affarijiet li ma jagħmilx ġew misjuba hawn fuq id-demos nfushom: it-tielet flag tal-bunch parzjali u l-bit tal-moviment fl-aħħar.

Squad huwa trademark ta' Offworld Industries. Dan il-pakkett jaqra fajls li jikteb server ta' Squad; ma jmissx il-logħba, il-kodiċi tagħha jew l-arkivji tagħha. Il-politika ta' Offworld dwar il-liċenzjar u l-amministrazzjoni tas-servers ma tgħid xejn dwar ir-rekordjar jew l-analiżi tad-demos. L-EULA ta' Squad tipprojbixxi r-reverse engineering tal-logħba nnifisha, li dan ma jagħmilx.
