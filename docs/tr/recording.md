---
title: "Demo kaydetme"
nav_order: 2
lang: "tr"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# Demo kaydetme {#recording-a-demo}

Squad demoları oyun istemcisi tarafından değil, **sunucuda** kaydedilir.

1. Sunucunun `Admins.cfg` dosyasında, yöneticinin grubuna `demos` iznini verin.
2. Maç başladığında oyunun konsolunda `AdminDemoRec <name>` çalıştırın. Bunu bir yöneticinin oyunun kendisinde yazması gerekir; bir rapora göre RCON bunu kabul etmiyor.
3. Maçı oynayın, sonra `AdminDemoStop` çalıştırın.
4. Demo `<server>/SquadGame/Saved/Demos/<name>.replay` konumuna yazılır. Onu sunucudan, dönüştürecek makineye kopyalayın.

`Server.cfg` dosyasında varsayılan olarak kapalı bir `RecordDemos` ayarı da vardır. Küçük bir maç için saatte yaklaşık 70 ila 80 MB bekleyin; tam 100 oyunculu bir sunucunun boyutu ölçülmedi.

Bir demo, sunucudaki herkesin adlarını ve çevrimiçi kimliklerini tutar: onu kişisel veri gibi görün ([Sınırlar, güncellemeler ve koşullar](limits.md#personal-data)).

Sonraki adım: [Demoları dönüştürme](converting.md).
