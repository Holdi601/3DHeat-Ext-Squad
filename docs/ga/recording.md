---
title: Demo a thaifeadadh
nav_order: 2
lang: ga
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Demo a thaifeadadh {#recording-a-demo}

Taifeadtar demos Squad **ar an bhfreastalaí**, ní ag cliant an chluiche.

1. I `Admins.cfg` an fhreastalaí, tabhair an cead `demos` do ghrúpa an riarthóra.
2. I gconsól an chluiche, rith `AdminDemoRec <name>` nuair a thosaíonn an cluiche.
   Caithfidh riarthóir é seo a chlóscríobh sa chluiche féin; deir tuarascáil amháin nach nglacann
   RCON leis.
3. Imir an cluiche, ansin rith `AdminDemoStop`.
4. Scríobhtar an demo chuig `<server>/SquadGame/Saved/Demos/<name>.replay`.
   Cóipeáil den fhreastalaí é chuig an meaisín a thiontaíonn é.

Tá socrú `RecordDemos` ann freisin in `Server.cfg`, múchta de réir réamhshocraithe. Bí ag súil le thart ar
70 go 80 MB san uair do chluiche beag; níor tomhaiseadh an méid d'fhreastalaí iomlán
100 imreoir.

Coinníonn demo ainmneacha agus ID ar líne gach duine ar an bhfreastalaí: caith leis mar
shonraí pearsanta ([Teorainneacha, nuashonruithe agus téarmaí](limits.md#personal-data)).

Ar aghaidh: [Demos a thiontú](converting.md).
