---
title: "Bu belgelerin bakımı"
nav_order: 91
lang: "tr"
source: maintaining.md
source_hash: "b0b7836a5545"
nav_exclude: true
search_exclude: true
---
# Bu belgelerin bakımı {#maintaining-these-docs}

Her sürüm için bir kontrol listesi; böylece sayfalar koddan asla geri kalmaz.

1. **Başvuruyu yeniden üretin.** `python tools/gen_docs_reference.py` [Komut başvurusu](../cli-reference.md) sayfasını programın kendi `--help` çıktısından ve çıktı sütunlarından yeniden yazar. `python tools/gen_docs_reference.py --check` ise kayıtlı sayfa eskiyse 1 ile çıkar.
2. **Neyin değiştiğini listeleyin.** `git log v<VERSION>..HEAD --oneline`; burada `<VERSION>`, son yayımlanan sürümdür (sürümde `VERSION` dosyası). Her yeni özelliğe, seçeneğe ve çıktı sütununa bir sayfada yer verin ve [`CHANGELOG.md`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/CHANGELOG.md) dosyasının **Docs** bölümüne bir satır ekleyin.
3. **Bağımsız inceleme.** Sayfaları yazmamış biri README'yi ve değişen her sayfayı, resimler dahil, üç kez okur: hiç terminal kullanmamış bir acemi olarak, sekiz yaşında bir çocuk olarak ve her seçeneği `--help` ile karşılaştıran bir uzman olarak. Örnekler yalnızca uydurma adlar ve sayılar kullanır.
4. **Düzeltin.** İnceleme ne bulursa düzeltin.
5. **Çeviriler.** Her çevrilmiş sayfa, yapıldığı İngilizce sayfanın özetini (hash) kaydeder. İngilizce kaynağı değişen sayfaları yeniden çevirin, sonra her dili inceleyin: açık metin, doğru şema etiketleri ve görüntüleyicinin kendi çevrilmiş arayüzündeki aynı sözcükler.
6. **Testleri çalıştırın** (`pytest`).
7. **Gönderin (push)** yalnızca sahibin onayından sonra.

## Çeviriler: komutlar {#translations-the-commands}

Site, 3DHeat görüntüleyicisinin 40 diline çevrilir: İngilizce `docs/` içinde, diğer her dil aynı dosya adlarıyla `docs/<lang>/` içinde. Kayıt tutma işini `tools/docs_i18n.py` yapar:

```bash
python tools/docs_i18n.py hashes             # İngilizce bir değişiklikten sonra: her sayfanın karmasını kaydet
python tools/docs_i18n.py svg-strings        # bir resim değişikliğinden sonra: çevrilecek etiketler
python tools/docs_i18n.py status             # dil başına: güncel, eski ve eksik sayfalar
python tools/docs_i18n.py todo --lang tr     # (yeniden) çevrilecek Türkçe sayfalar
python tools/docs_i18n.py svg-build --lang tr    # docs/assets/i18n/svg/tr.json dosyasından Türkçe resimler
python tools/docs_i18n.py finish --lang tr   # Türkçe sayfalara İngilizce karmayı damgala
python tools/docs_i18n.py check              # karmalar ya da etiketler eskiyse 1 ile çıkar
```

Yalnızca `todo`'nun listelediğini çevirin: Markdown'ı, bağlantıları, kodu, dosya ve sütun adlarını olduğu gibi bırakın; başlıkları ve resim açıklamalarını çevirin; düğmeler ve paneller için görüntüleyicinin kendi sözcüklerini kullanın (`src/i18n/locales/<lang>/`). Üretilmiş başvuru sayfaları ve terminal resimleri İngilizce kalır. Sitede eskimiş bir çeviri bunu söyler ve İngilizce sayfaya bağlanır; eksik bir çeviri İngilizceye döner. Üstbilgideki dil menüsü ve ana sayfanın tarayıcı dili yönlendirmesi `docs/_includes/` içinden gelir.
