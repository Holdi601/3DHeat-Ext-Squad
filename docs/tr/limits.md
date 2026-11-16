---
title: "Sınırlar, güncellemeler ve koşullar"
nav_order: 7
lang: "tr"
source: limits.md
source_hash: "8a9c7c448411"
nav_exclude: true
search_exclude: true
---
# Sınırlar, güncellemeler ve koşullar {#limits-updates-and-terms}

## Okunmayanlar {#not-read}

- **Kimin kimi öldürdüğü ve askerlere isabetle verilen hasar.** Bunlar silahların ve oyuncu durumlarının uzak çağrılarının isabet sonuçlarında taşınır (`HitResultsZeroBased`, `MulticastOnImpact.Hit`). Yapıları okunmaz; entities yan dosyasında bütün olarak tutulurlar. Yalnızca kurbanların canı çözülür.
- **Botun takımı.** Bir botun durumu, takımı olabilecek bir sayı taşır; doğrulanmadı, kullanılmıyor.
- **Bir askerin gövdesinin yaw'unun ötesinde yana baktığı yer.**

## Oyun güncellemeleri {#game-updates}

Okuyucu, motorun tekrar biçimine ve birkaç Squad sınıf ve özellik adına bağlıdır. Göremediği özellik düzenlerine bağlı değildir: onları tekrarın kendisi adlandırır.

**Bir Squad güncellemesiyle neler bozulabilir:**

- **Bir motor yükseltmesi.** Squad, v10.4 ile UE 5.7'ye geçti; bu orada denenmedi. Yükseltme bunch başlığını, doğuş verisini ya da `FRepMovement`'i değiştirebilir. Bunlar, adımın bilindiği yerde kodda sürüme göre kapılanmıştır. Bilinmeyen adımlar (`ENG_PARTIAL_CUSTOM_EXPORTS`, sondaki hareket biti) v10.3.1'in yaptığına sabitlenmiştir.
- **Iris çoğaltması.** Squad Iris'e geçerse, parçaların içindeki akış yeni olur ve bu okuyucu onu okuyamaz. Squad v10.3.1 klasik sistemi kullanır (ReplicationGraph çalıştırır).
- **Yeniden adlandırılan sınıflar ya da özellikler.** Squad oyuncu, takım ya da manga sınıflarını ya da özelliklerini yeniden adlandırırsa, adlar ya da takımlar kaybolur; ama konumlar kaybolmaz.
- **Hata olunca ne olur.** Biçim değiştiğinde okuyucu, tanılamalarda akış hataları ya da hareket hatalarıyla yüksek sesle başarısız olur. Sessizce yanlış konumlar üretmez: `FRepMovement` yalnızca bitleri tam olarak tuttuğunda kabul edilir.

## Kişisel veriler {#personal-data}

Bir demo, sunucudaki herkesin adlarını ve çevrimiçi kimliklerini tutar. Tablo ve maç belgesi adları taşır, kimlikleri değil. Yan dosyalar her özelliğin bitlerini tutar; bu yüzden kimlikleri demonun tuttuğu gibi tutarlar (çözülmeden). Hepsini demonun kendisi gibi görün.

## Lisans ve kaynaklar {#licence-and-sources}

MIT; bkz. [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE). Buradaki her şey bu paket için yazıldı. Hiçbir üçüncü taraf kodu eklenmedi ya da bağlanmadı: tek bağımlılıklar pyarrow (Apache-2.0) ve numpy (BSD-3-Clause).

Biçim hakkındaki bilgiler şu kaynaklardan geldi:

- **Unreal.Core**, [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) içinde (MIT). Genel Unreal tekrar düzenini anlatır: bilgi bloğu, parçalar, kareler, bunch'lar ve net alan dışa aktarmaları.
- **[squad-replay](https://github.com/Codycody31/squad-replay)** (MPL-2.0). Ayrıştırıcısı; Squad v10.3.1'in yazdığı düzen, sürüm denetimleri ve hangi Squad sınıflarının kadro verisi taşıdığı için okundu. Yayımlanmış test demoları ve anlık görüntü sayıları bağımsız bir çapraz denetim olarak kullanıldı. Kodundan hiçbir şey kopyalanmadı ya da çevrilmedi: bu okuyucu farklı yapılandırılmıştır (tam paketler üzerinde Python bit arşivi, kısmi bunch'lar bitlerle birleştirilmiş, özellikler adla gönderilmiş). Onun yapmadığı iki şey demolarda bu okuyucu tarafından bulundu: üçüncü kısmi bunch bayrağı ve sondaki hareket biti.

Bu paket, bir Squad sunucusunun yazdığı demo dosyalarını okur; oyuna, koduna ya da arşivlerine dokunmaz ve oyundan hiçbir şey içermez ya da yeniden dağıtmaz. Yazdıkları sizin makinenizde kalır.

3DHeat'in Offworld Industries ile bir bağlantısı yoktur ve Offworld Industries tarafından onaylanmamıştır. Squad ve ilgili adlar ile ticari markalar sahiplerine aittir.

Hak sahipleri: <https://github.com/Holdi601/3DHeat-Ext-Squad/issues> adresinde bir issue açın - hızlı yanıt veririz ve istek üzerine her şeyi kaldırırız.
