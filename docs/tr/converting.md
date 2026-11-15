---
title: "Demoları dönüştürme"
nav_order: 3
lang: "tr"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# Demoları dönüştürme {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          the same, without installing
```

## Adım adım {#step-by-step}

Komut satırında yeni misiniz? Önce [Başlamadan önce](before-you-start.md) sayfasını okuyun.

1. Bir kez kurun: `git clone https://github.com/Holdi601/3DHeat-Ext-Squad`, terminalde o klasörü açın ve `python -m pip install -e .` çalıştırın (Python 3.10 veya daha yeni; pyarrow ve numpy'yi de getirir).
2. `.replay` dosyalarını bir klasöre koyun ya da tek tek adlarını verin.
3. `heat3d-squad-demo <folder> -o out` çalıştırın.
4. Her demo için bir satır görmelisiniz: katmanı, oyuncuları ve satırları ile tablonun nereye yazıldığını. Her demo `out/<map>/` içinde dört düz dosyaya dönüşür (`.3dheat` kapsayıcı değil); `.parquet` dosyasını 3DHeat görüntüleyicisinde yükleyin.

![Sentetik bir demo üzerinde bir çalıştırma](../assets/img/run.svg)

Resim, testlerin oluşturduğu bir demo üzerinde (`tests/test_stream.py`) yapılan bir çalıştırmayı gösterir, gerçek bir maçı değil.

## Seçenekler {#options}

| Seçenek | Varsayılan | Ne yapar |
|---|---|---|
| `demos` (bir ya da daha fazla) | - | `.replay` dosyaları ya da bunları tutan klasörler |
| `-o`, `--out` | gerekli | yazılacak klasör; her demo `<out>/<map>/` içine gider |
| `--flat` | kapalı | doğrudan klasöre yazar, `<map>/` klasörü olmadan |
| `--json` | kapalı | her demo için stdout'a bir JSON satırı yazar (komutu çağıran programlar için): `demo`, `ok`, `parquet`, `match`, `sidecars`, `lost`, `rows`, `players`, `layer`, `recorded_unix`; başarısız bir demo bunun yerine `demo`, `ok: false` ve `error` yazar |
| `--version` | - | sürümü yazar ve durur |

Her seçenek, programın yazdığı gibi: [Komut başvurusu](../cli-reference.md).

Harita klasörü, demonun adını verdiği seviye yolundan alınan haritanın adıdır (`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` `<Map>` verir).

Çıkış durumu: her demo dönüştürüldüğünde 0; herhangi biri başarısız olduğunda (diğerleri yine de yazılır) ya da hiç `.replay` dosyası bulunmadığında 1.

## Ne çıkar {#what-comes-out}

| Dosya | İçerir |
|---|---|
| `<demo>.parquet` | tablo: konumlar ve olaylar, satır başına biri ([Tablo](output-table.md)) |
| `<demo>.match.json` | maç belgesi ([Maç belgesi](output-match.md)) |
| `<demo>.entities.parquet` | yan dosya: her özellik güncellemesi ve uzak çağrı, bütün olarak |
| `<demo>.packets.parquet` | yan dosya: dosyanın parçaları ve okunamayan her şey, bütün olarak |

Tablo ve maç belgesi, 3DHeat CS2 aracının yazdığı çiftin aynısıdır. Görüntüleyici tabloyu doğrudan açar; bütün bir klasör yüklendiğinde yan dosyaları dışarıda bırakır.

## Örnekler {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # bir klasördeki her demo
heat3d-squad-demo one.replay two.replay -o out --flat  # doğrudan out/ içine
heat3d-squad-demo D:\SquadDemos -o out --json          # demo başına bir JSON satırı
```

`D:\SquadDemos` D sürücüsünde örnek bir klasördür: kendinizinkini kullanın.
