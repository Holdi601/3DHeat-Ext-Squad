---
title: Teorainneacha, nuashonruithe agus téarmaí
nav_order: 7
lang: "ga"
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Teorainneacha, nuashonruithe agus téarmaí {#limits-updates-and-terms}

## Gan léamh {#not-read}

- **Cé a mharaigh cé, agus damáiste do shaighdiúirí de réir buille.** Taistealaíonn siad i dtorthaí buille glaonna cianda na n-arm agus staideanna na n-imreoirí (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), nach léitear a struchtúr; coinnítear iad iomlán sa chomhad cliatháin entities. Ní dhíchódaítear ach sláinte na n-íospartach.
- **Foireann an bhota.** Iompraíonn staid bhota uimhir a d'fhéadfadh a foireann a bheith; níl sé deimhnithe, ní úsáidtear é.
- **An áit a mbreathnaíonn saighdiúir ar an taobh** thar yaw an choirp.

## Nuashonruithe cluiche {#game-updates}

Braitheann an léitheoir ar fhormáid athsheinm an innill agus ar chúpla ainm aicme agus airí Squad. Ní bhraitheann sé ar leaganacha airí nach bhfeiceann sé: ainmníonn an athsheinm féin iad.

**An rud a d'fhéadfadh briseadh le nuashonrú Squad:**

- **Uasghrádú innill.** Bhog Squad go UE 5.7 le v10.4, agus níor tástáladh é seo ansin. Is féidir leis an uasghrádú ceannteideal an bhunch, na sonraí spawn nó `FRepMovement` a athrú. Tá siad cuachta le leagan sa chód nuair is eol an chéim. Tá céimeanna anaithnide (`ENG_PARTIAL_CUSTOM_EXPORTS`, an giotán gluaiseachta deiridh) greamaithe de na rudaí a dhéanann v10.3.1.
- **Macasamhlú Iris.** Dá n-athródh Squad go Iris, bheadh an sruth taobh istigh de na codanna nua agus ní léifeadh an léitheoir seo é. Úsáideann Squad v10.3.1 an córas clasaiceach (ritheann sé ReplicationGraph).
- **Aicmí nó airí athainmnithe.** Dá n-athainmneodh Squad a aicmí imreora, foirne nó scuaide nó a n-airí, bheadh ainmneacha nó foirne ar iarraidh, ach ní bheadh suíomhanna.
- **Cad a tharlaíonn nuair a theipeann.** Nuair a athraíonn an fhormáid, teipeann an léitheoir go hard le hearráidí sruthanna nó le hearráidí gluaiseachta sna diagnóisic. Ní tháirgeann sé suíomhanna mícheart go ciúin: ní ghlactar le `FRepMovement` ach amháin nuair a bhíonn a ghiotáin cruinn.

## Sonraí pearsanta {#personal-data}

Coinníonn demo ainmneacha agus ID ar líne gach duine ar an bhfreastalaí. Iompraíonn an tábla agus cáipéis an chluiche ainmneacha, ní ID. Coinníonn na comhaid chliatháin giotáin gach airí, mar sin coinníonn siad na ID mar a dhéanann an demo (gan díchódú). Caith leo go léir mar a chaitheann tú leis an demo féin.

## Ceadúnas agus foinsí {#licence-and-sources}

MIT; féach [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Scríobhadh gach rud anseo don phacáiste seo. Níl cód tríú páirtí san áireamh ná nasctha: is iad pyarrow (Apache-2.0) agus numpy (BSD-3-Clause) na spleáchais amháin.

Tháinig fíricí faoin bhformáid ó na foinsí seo:

- **Unreal.Core** i [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Déanann sé cur síos ar leagan amach ginearálta athsheinm Unreal: an bloc faisnéise, codanna, frámaí, bunches agus onnmhairithe réimsí líonra.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Léadh a parsálaí le haghaidh an leagan amach mar a scríobhann Squad v10.3.1 é, le haghaidh na seiceálacha leagain, agus le haghaidh na n-aicmí Squad a iompraíonn sonraí ainmniúcháin. Baineadh úsáid as a demos tástála foilsithe agus as a chomhaireamh scáthghrianghraf mar chros-seiceáil neamhspleách. Níor cóipeáladh ná níor aistríodh aon chuid dá chód: tá an léitheoir seo struchtúrtha ar bhealach difriúil (cartlann ghiotán Python thar phaicéid iomlána, bunches páirteacha ceangailte giotán ar ghiotán, airí seolta de réir ainm), agus aimsíodh dhá rud nach ndéanann sé ar na demos féin: an tríú bratach bunch páirteach agus an giotán gluaiseachta deiridh.

Is trádmharc de chuid Offworld Industries é Squad. Léann an pacáiste seo comhaid a scríobhann freastalaí Squad; ní bhaineann sé leis an gcluiche, lena chód ná lena chartlanna. Ní deir polasaí ceadúnúcháin agus riaracháin freastalaí Offworld faic faoi demos a thaifead nó a anailísiú. Toirmisceann EULA Squad an cluiche féin a aisinnealtóireacht, rud nach ndéanann seo.
