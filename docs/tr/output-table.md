---
title: "Tablo"
nav_order: 4
lang: "tr"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# Tablo: `<demo>.parquet` {#the-table-parquet}

Örnek ya da olay başına bir satır. Bir örnek, sunucu aktörün hareketini çoğalttığında alınır: hareket ederken en fazla saniyede 8 kez (demonun kayıt hızı).

![Sentetik bir demo tablosunun ilk satırları](../assets/img/table.svg)

## Sütunlar {#columns}

| Sütun | Nedir |
|---|---|
| `time` | kayıt başladığından beri geçen saniye |
| `x`, `y`, `z` | Unreal birimleriyle (santimetre) konum, Z yukarı |
| `dirX`, `dirY`, `dirZ` | bir askerin nereye baktığı: gövdenin yaw açısı ve bakışın pitch açısı, birim vektör olarak (bir aracınki: düz) |
| `yaw`, `pitch` | aynısı derece cinsinden; `pitch` ufuktan yukarı, yalnızca askerler için |
| `health` | o andaki asker, bot ya da aracın canı, sunucunun gönderdiği yerde (yaralıyken bir askerin canı 0'ın altına düşer) |
| `speed` | çoğaltılan hız, cm/s |
| `player` | oyuncunun adı; bir bot için `bot <id>`; kimsenin sahip olmadığı bir araç ya da konuşlandırılabilir öğe için sınıfı; bir araç silahından yapılan atış için o araçta oturan oyuncu |
| `team`, `faction` | Squad'un takım numarası (1, 2) ve fraksiyon kurulumu, **o andaki**: oyuncular taraf değiştirebilir |
| `squad` | manga numarası; bir mangada değilse -1 |
| `event` | satırın ne olduğu (aşağıda) |
| `pawn` | asker blueprint'i (bir bot için `SQSquidBot`), araç ya da `fire` için silah |
| `seat` | bir taret ya da yolcu koltuğu için koltuğun kendi pawn'ı |
| `detail` | `fire` için atışı yerleştiren silah çağrısı, `hit` için hasar türü, `removed` için kanalın neden kapandığı (`Destroyed`, `Dormancy`...) |
| `entity` | satırın hakkında olduğu aktör (net GUID'i): yan dosyaların satırlarındaki `entity` |
| `match` | demonun adı |

## Olaylar {#events}

| `event` | Satırı | Ne |
|---|---|---|
| `position` | yayadaki bir asker ya da bot | bir hareket örneği |
| `vehicle` | kara aracındaki ya da helikopterdeki bir asker | aracın konumunda bir örnek |
| `wounded`, `revived`, `death` | askerler ve botlar | olayın yeri |
| `spawn`, `damaged`, `destroyed`, `removed` | araçlar, konuşlandırılabilir öğeler, mevziler, sandıklar, helikopterler | yerleri |
| `seat` | bir oyuncu | bir koltuğa oturdu |
| `fire` | atıcı | bir atış: nereden çıktığı, yönü `yaw`/`pitch`/`dirX..Z` olarak |
| `hit` | araç | bir araç isabeti: nereye |

Olaylar nasıl okunur, [Demo nasıl okunur](how-it-works.md#how-the-events-are-read) sayfasında anlatılır.

## Görüntüleyicide {#in-the-viewer}

Parquet dosyasının sonundaki bilgi, `heat3d` anahtarı altında okuma talimatlarını taşır: Z yukarı, hiçbir eksen aynalanmaz, birim ölçeği 1. Bu yüzden görüntüleyicinin sütun eşlemesine ihtiyacı yoktur. Tabloyu Isı haritası sekmesinde yükleyin; görüntüleyicinin [Veri ekleme](https://holdi601.github.io/3DHeat/getting-data-in.html) ve [Sütun eşlemesi](https://holdi601.github.io/3DHeat/column-mapping.html) sayfalarına bakın.
