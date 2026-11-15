---
title: Cáipéis an chluiche agus na comhaid chliatháin
nav_order: 5
lang: "ga"
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Cáipéis an chluiche agus na comhaid chliatháin {#the-match-document-and-sidecars}

Taobh leis an tábla, faigheann gach demo `<demo>.match.json` agus dhá chomhad cliatháin,
`<demo>.entities.parquet` agus `<demo>.packets.parquet`. Léann an t-amharcán
cáipéis an chluiche ina chluaisín Cluiche.

## Cáipéis an chluiche {#the-match-document}

Coinníonn `<demo>.match.json` (cáipéis an chluiche) ar a barrleibhéal `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` agus `selfCheck` (an liosta iomlán: [Tagairt orduithe](../cli-reference.md)). I bhfocail: an léarscáil agus an layer, leaganacha an chluiche agus an innill, am an taifeadta, fad, agus:

- **na foirne**: uimhir, faction agus gach rud a mhacasamhlaigh a staid (ticéid, infhaighteachtaí, ceannasaí) de réir mar a d'athraigh sé;
- **na scuaidí**: uimhir, foireann, ainm, cruthaitheoir, ceannaire, baill;
- **staid an chluiche**: ainm agus socruithe an fhreastalaí, mód cluiche, staid agus id an chluiche, rothlaithe léarscáileanna agus layer, vótaí, amadóirí, teachtaireacht an lae;
- **na haisteoirí**: gach gluaisteán, earra imlonnaithe, bunaí, cás ammo agus héileacaptar - aicme, cá agus cathain a spawnadh é, cathain a d'imigh sé, cé leis, agus a staid mhacasamhlaithe (sláinte, staid tógála, suíocháin...);
- **líne do gach imreoir**: samplaí ar shiúl na gcos agus i ngluaisteáin, achar siúlta, aicmí saighdiúirí a imríodh, gluaisteáin a úsáideadh, athruithe foirne, suíocháin a glacadh, agus gach rud a mhacasamhlaigh staid an imreora (ping, leibhéal, ról, suíochán reatha...); agus líne do gach bot;
- **na himeachtaí** comhairthe, an **daonáireamh airí** (cé chomh minic a seoladh airí gach aicme) agus an **daonáireamh glaonna cianda**, na lámhaigh agus na buillí, cad **nár** léadh, agus diagnóisic an léitheora;
- **an comhad agus an ceannteideal**: gach réimse den bhloc faisnéise agus de cheannteideal an demo, tábla na gcodanna, na táblaí onnmhairithe réimsí líonra (`net_field_exports`), cúiseanna dúnta na gcainéal, agus na haicmí a aimsíodh do rudaí nach ainmníonn na honnmhairithe (`stream.class_resolution`);
- **an féin-seic** (`selfCheck.completeness`, féach [Iomláine](#completeness)).

Fágtar ID ar líne (Steam, EOS) ar lár d'aon ghnó.

Súil thapa ar demo tiontaithe:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Iomláine {#completeness}

Leanann an léitheoir seo an riail a roinneann gach tiontaire 3DHeat: díchódaigh an méid is féidir a léamh anois, coinnigh an chuid eile iomlán, agus abair cé mhéad de gach cineál a rinneadh ([Coinníonn tiontairí gach rud](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Tá `selfCheck.completeness` i ngach cáipéis chluiche: in aghaidh gach cineál míre a casadh sa demo, cé mhéad a bhí `seen`, `decoded`, `partial` (díchódaithe go páirteach agus coinnithe iomlán), `raw` (coinnithe iomlán amháin) agus `lost` (caithfidh 0 a bheith ann). Comhairtear na cineálacha san áit a gcasann an léitheoir leo: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Ar na demos fíora a léadh, is 0 é `lost`: ritheann a míreanna ó na céadta mílte go dtí milliúin; déantar thart ar leath a dhíchódú go hiomlán, tá an chuid eile páirteach nó amh.

**Léite** (isteach sa tábla agus i ncáipéis an chluiche):

- an bloc faisnéise, ceannteideal an demo (gach réimse; coinnítear dhá bheart deiridh nach bhfuil aithne orthu mar heicsidheachúlach), tábla na gcodanna;
- gach fráma, paicéad agus bunch (scoilte iomlán ina bhfuil iontu), gach aisteoir a osclaíodh (lena shuíomh spawn, rothlú, scála agus treoluas) agus a dúnadh (agus cén fáth: `Destroyed`, `Dormancy`...);
- gach aireach macasamhlaithe, chomh fada agus a deir a ghiotáin ([Airí a dhíchódú](how-it-works.md#decoding-properties)), suíomhanna ó `FRepMovement` agus ó chomhpháirt ghluaiseachta na n-héileacaptar, na taismigh, sláinte gluaisteán, suíocháin;
- gach glao cianda de réir ainm, lena pharaiméadair nuair a onnmhairíonn an demo grúpa na feidhme: lámhaigh (`fire`) agus buillí ar ghluaisteáin (`hit`) isteach sa tábla;
- na táblaí onnmhairithe réimsí líonra agus na net GUIDs (a n-uimhir; tá na cosáin sa chomhad cliatháin entities).

**Coinnithe amh** (iomlán, leis an méid a léitear de taobh leis):

- `<demo>.entities.parquet`, colúin `time`, `type` (`<class>.<property>`, `<class>.<call>`, nó ainm an réad), `name` (aicme an aisteora), `entity` (net GUID an aisteora, mar `entity` an tábla), `kind`, `object` (an fho-réad), `channel`, `handle`, `group` (cosán aicme an ghrúpa onnmhairithe), `decoded` (JSON), `bits` agus `payload` (na giotáin, an ceann is ísle ar dtús, líonta amach go beart iomlán):
  - gach nuashonrú airí (`kind` `property`), an ghluaiseacht san áireamh, leis an méid atá díchódaithe; amh san áit amháin nach bhfuil aon rud (láimhseálacha gan ainm, struchtúir mar `RotationReplicatedMovement` tuirléad, agus airí fágtha mar ghiotáin);
  - gach glao cianda agus réimse delta saincheaptha (`rpc`), na paraiméadair díchódaithe nuair a onnmhairíodh grúpa na feidhme; amh nuair nach ndearnadh (`RepInventory`, `PlayerStateData`);
  - gach bloc ábhair de réad nach bhféadfaí a aicme a aimsiú (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), a cheannteideal díchódaithe;
  - gach cainéal aisteora a osclaíodh agus a dúnadh (`open`, `close`), gach fo-réad a scriosadh nó a millíodh;
  - an comhthéacs a theastaíonn ó dhíchódóir níos déanaí chun an comhad a léamh leis féin: gach onnmhairiú réimse líonra (`export.field`: cosán grúpa, láimhseáil, ainm airí, seicsum) agus gach net GUID onnmhairithe (`export.guid`: a chosán, a sheachtrach agus brataí), ag an am a thug an sruth iad.
- `<demo>.packets.parquet`, colúin `time`, `type`, `name`, `channel`, `offset` (sa chomhad), `decoded`, `bits`, `payload`: an bloc faisnéise, an chuid cheannteidil, gach cuid seicphointe (is é seicphointe staid gach aisteora ag a am, atá sa sruth ón tús freisin), gach cuid imeachta, agus gach fráma, paicéad nó bunch nach léitear (bunch amháin in aghaidh an demo: bunch oscailte aisteora féachadóra an taifeadáin féin), iomlán.

Tá sraitheanna entities grúpáilte de réir `kind`, `type` agus `entity`, gach ceann in ord ama; sórtáil de réir `time` d'ord an tsrutha.

**Níl ar fáil:**

- an méid nach dtaifeadann demo freastalaí: ionchuir chliant, cad a chonaic imreoir;
- éifeachtaí cliantaí: marcóirí buille, fuaimeanna, téacs fotha maruithe (seolann an freastalaí na glaonna, ní a dtaispeáint);
- ID ar líne díchódaithe: coinnithe mar ghiotáin amháin (féach [Sonraí pearsanta](limits.md#personal-data)).
