---
title: "Maç belgesi ve yan dosyalar"
nav_order: 5
lang: tr
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# Maç belgesi ve yan dosyalar {#the-match-document-and-sidecars}

Tablonun yanında her demo `<demo>.match.json` ile iki yan dosya alır: `<demo>.entities.parquet` ve `<demo>.packets.parquet`. Görüntüleyici maç belgesini Maç sekmesinde okur.

## Maç belgesi {#the-match-document}

`<demo>.match.json` (maç belgesi) en üst düzeyde şunları tutar: `map`, `layer`, `level_path`, `game_version`, `engine_version`, `recorded_unix`, `duration_s`, `teams`, `squads`, `game_state`, `actors`, `players`, `rows`, `events`, `not_read`, `file`, `header`, `chunks`, `stream`, `shots` ve `selfCheck` (tam liste: [Komut başvurusu](../cli-reference.md)). Sözcüklerle: haritayı ve katmanı, oyunun ve motorun sürümlerini, kayıt zamanını, uzunluğu ve şunları:

- **takımlar**: numara, fraksiyon ve değiştikçe durumlarının çoğalttığı her şey (biletler, kullanılabilirlikler, komutan);
- **mangalar**: numara, takım, ad, kurucu, lider, üyeler;
- **oyun durumu**: sunucu adı ve ayarları, oyun modu, maç durumu ve kimliği, harita ve katman rotasyonları, oylar, zamanlayıcılar, günün mesajı;
- **aktörler**: her araç, konuşlandırılabilir öğe, mevzi, mühimmat sandığı ve helikopter: sınıfı, nerede ve ne zaman doğduğu, ne zaman gittiği, kimin olduğu ve çoğalttığı durum (can, inşa durumu, koltuklar...);
- **her oyuncu için bir satır**: yayadayken ve araçlardayken örnekler, yürünen mesafe, oynanan asker sınıfları, kullanılan araçlar, takım değişiklikleri, oturulan koltuklar ve oyuncu durumunun çoğalttığı her şey (ping, seviye, rol, o anki koltuk...); her bot için de bir satır;
- sayılan **olaylar**, **özellik sayımı** (her sınıfın özelliklerinin ne sıklıkla gönderildiği) ve **uzak çağrı sayımı**, atışlar ve isabetler, **okunmayan** şeyler ve okuyucunun tanılamaları;
- **dosya ve başlık**: bilgi bloğunun ve demo başlığının her alanı, parça tablosu, net alan dışa aktarma tabloları (`net_field_exports`), kanalların kapanma nedenleri ve dışa aktarmaların adını vermediği nesneler için bulunan sınıflar (`stream.class_resolution`);
- **öz denetim** (`selfCheck.completeness`, bkz. [Tamlık](#completeness)).

Çevrimiçi kimlikler (Steam, EOS) bilerek dışarıda bırakılır.

Dönüştürülmüş bir demoya hızlı bir bakış:

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## Tamlık {#completeness}

Bu okuyucu, 3DHeat dönüştürücülerinin ortak kuralını izler: şimdi okunabilen her şeyi çözer, gerisini bütün olarak tutar ve her türden ne kadarını yaptığını söyler ([Dönüştürücüler her şeyi tutar](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)). Her maç belgesinde `selfCheck.completeness` vardır: demoda karşılaşılan her öğe türü için kaç tanesinin `seen` (görülen), `decoded` (çözülen), `partial` (kısmen çözülüp bütün olarak tutulan), `raw` (yalnızca bütün olarak tutulan) ve `lost` (0 olmalı) olduğu. Türler, okuyucunun onlarla karşılaştığı yerde sayılır: `file.info`, `chunk.<kind>`, `frame`, `packet`, `bunch`, `open`, `close`, `export.field`, `export.guid`, `external`, `property:<class>`, `rpc:<class>`, `block:<object>`, `subobject.*`.

Okunan gerçek demolarda `lost` 0'dır: öğeleri yüz binlerden milyonlara kadar gider; yaklaşık yarısı tamamen çözülür, geri kalanı kısmen ya da ham kalır.

**Okunanlar** (tabloya ve maç belgesine):

- bilgi bloğu, demo başlığı (her alan; bilinmeyen iki sondaki bayt hex olarak tutulur), parça tablosu;
- her kare, paket ve bunch (taşıdıklarına bölünmüş olarak bütün), açılan her aktör (doğduğu yer, dönüşü, ölçeği ve hızıyla) ve kapanan her aktör (nedeniyle: `Destroyed`, `Dormancy`...);
- her çoğaltılan özellik, bitlerinin söylediği kadarıyla ([Özellikleri çözme](how-it-works.md#decoding-properties)); `FRepMovement`'ten ve helikopterlerin hareket bileşeninden konumlar; kayıplar, araçların canı, koltuklar;
- her uzak çağrı adıyla, demo fonksiyonun grubunu dışa aktardığında parametreleriyle: atışlar (`fire`) ve araç isabetleri (`hit`) tabloya;
- net alan dışa aktarma tabloları ve net GUID'ler (sayıları; yolları entities yan dosyasında).

**Ham tutulanlar** (bütün olarak, yanında okunan kısmıyla):

- `<demo>.entities.parquet`, sütunlar `time`, `type` (`<class>.<property>`, `<class>.<call>` ya da nesnenin adı), `name` (aktörün sınıfı), `entity` (aktörün net GUID'i, tablodaki `entity` gibi), `kind`, `object` (alt nesne), `channel`, `handle`, `group` (dışa aktarma grubunun sınıf yolu), `decoded` (JSON), `bits` ve `payload` (bitler, en düşükten başlayarak, tam baytlara tamamlanmış):
  - her özellik güncellemesi (`kind` `property`), hareket dahil, çözülebilen kısmıyla; yalnızca hiçbir şey çözülemediğinde ham (adsız tutamaçlar, taretlerin `RotationReplicatedMovement` gibi yapıları ve bit olarak kalan özellikler);
  - her uzak çağrı ve özel delta alanı (`rpc`), fonksiyonun grubu dışa aktarıldıysa parametreleri çözülmüş; aksi halde ham (`RepInventory`, `PlayerStateData`);
  - sınıfı bulunamayan bir nesnenin her içerik bloğu (`block`: `Buoyancy`, `GameplayTasksComponent`, `AmmoRackComponent`...), başlığı çözülmüş;
  - açılan ve kapanan her aktör kanalı (`open`, `close`), silinen ya da yok edilen her alt nesne;
  - dosyayı tek başına okuyacak sonraki bir çözücünün ihtiyaç duyduğu bağlam: her net alan dışa aktarması (`export.field`: grup yolu, tutamaç, özellik adı, sağlama toplamı) ve dışa aktarılan her net GUID (`export.guid`: yolu, dış nesnesi ve bayrakları), akışın onları verdiği zamanda.
- `<demo>.packets.parquet`, sütunlar `time`, `type`, `name`, `channel`, `offset` (dosyadaki yeri), `decoded`, `bits`, `payload`: bilgi bloğu, başlık parçası, her denetim noktası parçası (denetim noktası, her aktörün o andaki durumudur; baştan gelen akış da bunu tutar), her olay parçası ve okunmayan her kare, paket ya da bunch (demo başına bir bunch: kaydediciye ait izleyicinin açılış bunch'ı), bütün olarak.

Entities satırları `kind`, `type` ve `entity`'ye göre gruplanır; her grup zaman sırasındadır. Akışın sırası için `time`'a göre sıralayın.

**Mevcut değil:**

- bir sunucu demosunun kaydetmediği şeyler: istemcilerin girdileri, bir oyuncunun gördükleri;
- istemci tarafı etkiler: isabet işaretleri, sesler, öldürme akışının metni (sunucu çağrıları gönderir, onların ekranda gösterimini değil);
- çözülmüş çevrimiçi kimlikler: yalnızca bit olarak tutulur (bkz. [Kişisel veriler](limits.md#personal-data)).
