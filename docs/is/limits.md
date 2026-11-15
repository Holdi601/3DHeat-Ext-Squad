---
title: "Takmarkanir, uppfærslur og skilmálar"
nav_order: 7
lang: is
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# Takmarkanir, uppfærslur og skilmálar {#limits-updates-and-terms}

## Ekki lesið {#not-read}

- **Hver drap hvern, og skaði á hermönnum eftir höggi.** Þetta berst í höggniðurstöðum fjarkalla vopna og leikmannsstöðu (`HitResultsZeroBased`, `MulticastOnImpact.Hit`), en gerð þeirra er ekki lesin; þau eru geymd í heild í entities-hliðarskránni. Aðeins heilsa fórnarlambanna er afkóðuð.
- **Lið bots.** Staða bots ber tölu sem gæti verið lið hans; ekki staðfest, ekki notað.
- **Hvert hermaður lítur til hliðar** umfram sveigju (yaw) líkamans.

## Leikjauppfærslur {#game-updates}

Lesarinn byggir á afritunarsniði vélarinnar og örfáum Squad-flokka- og eigindanöfnum. Hann byggir ekki á eigindauppsetningum sem hann sér ekki: upptakan nefnir þær sjálf.

**Hvað getur bilað við Squad-uppfærslu:**

- **Vélaruppfærsla.** Squad færðist yfir í UE 5.7 með v10.4 og þetta er óprófað þar. Uppfærslan getur breytt bunch-hausnum, spawn-gögnunum eða `FRepMovement`. Þetta er bundið við útgáfu í kóðanum þar sem skrefið er þekkt. Óþekkt skref (`ENG_PARTIAL_CUSTOM_EXPORTS`, síðasti hreyfibitinn) eru fest við það sem v10.3.1 gerir.
- **Iris-afritun.** Ef Squad skipti yfir í Iris væri straumurinn inni í bútunum nýr og þessi lesari læsi hann ekki. Squad v10.3.1 notar klassíska kerfið (það keyrir ReplicationGraph).
- **Endurnefndir flokkar eða eigindir.** Ef Squad endurnefndi leikmanna-, liðs- eða sveitarflokka sína eða eigindir þeirra myndu nöfn eða lið vanta, en staðsetningar ekki.
- **Hvað gerist við bilun.** Þegar sniðið breytist bilar lesarinn hátt og skýrt með straumvillum eða hreyfivillum í greiningarupplýsingunum. Hann býr ekki hljóðlega til rangar staðsetningar: `FRepMovement` er aðeins samþykkt þegar bitar þess ganga nákvæmlega upp.

## Persónuupplýsingar {#personal-data}

Demo geymir nöfn og nettengd auðkenni allra á þjóninum. Taflan og leikjaskjalið bera nöfn, ekki auðkenni. Hliðarskrárnar geyma bita hverrar eigindar, svo þær geyma auðkennin eins og demo-ið gerir (óafkóðuð). Farðu með þær allar eins og demo-ið sjálft.

## Leyfi og heimildir {#licence-and-sources}

MIT; sjá [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Allt hér var skrifað fyrir þennan pakka. Enginn kóði frá þriðja aðila er innifalinn eða tengdur: einu ósjálfstæðin eru pyarrow (Apache-2.0) og numpy (BSD-3-Clause).

Upplýsingar um sniðið komu úr þessum heimildum:

- **Unreal.Core** í [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) (MIT). Það lýsir almennri uppbyggingu Unreal-upptöku: upplýsingablokkinni, bútum, römmum, bunch-um og net field exports.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Þáttari (parser) þess var lesinn til að fá uppbygginguna eins og Squad v10.3.1 skrifar hana, útgáfuskoðanirnar og hvaða Squad-flokkar bera hópskráargögn. Birt prófunardemo þess og snapshot-talningar voru notuð sem óháð víxlskoðun. Enginn kóði þess var afritaður eða þýddur: þessi lesari er byggður öðruvísi (Python-bitaskjalasafn yfir heila pakka, hlutabunch sameinuð á bitastigi, eigindum úthlutað eftir nafni), og tvennt sem það gerir ekki fannst hér á demo-unum sjálfum: þriðji hlutabunch-fáninn og síðasti hreyfibitinn.

Squad er vörumerki Offworld Industries. Þessi pakki les skrár sem Squad-þjónn skrifar; hann snertir ekki leikinn, kóða hans né skjalasöfn. Stefna Offworld um þjónaleyfi og stjórnun segir ekkert um upptöku eða greiningu á demo. EULA Squad bannar öfuga verkfræði (reverse engineering) á leiknum sjálfum, sem þetta gerir ekki.
