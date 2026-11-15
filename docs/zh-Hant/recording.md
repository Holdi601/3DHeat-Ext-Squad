---
title: "錄製對戰"
nav_order: 2
lang: "zh-Hant"
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# 錄製對戰 {#recording-a-demo}

Squad 的對戰是在**伺服器上**錄製的，不是由遊戲客戶端錄製。

1. 在伺服器的 `Admins.cfg` 中，給管理員所屬的群組 `demos` 權限。
2. 比賽開始時，在遊戲的主控台中執行 `AdminDemoRec <name>`。
   必須由管理員在遊戲內親自輸入這個指令；有一份回報指出 RCON 不接受此指令。
3. 比賽結束後，執行 `AdminDemoStop`。
4. 對戰會寫入 `<server>/SquadGame/Saved/Demos/<name>.replay`。
   請把它從伺服器複製到負責轉換的電腦上。

`Server.cfg` 也有 `RecordDemos` 設定，預設為關閉。小型比賽大約每小時會產生 70 到 80 MB；完整 100 人伺服器的大小尚未測量。

對戰檔案包含伺服器上每個人的名稱與線上 ID：請把它當作個人資料處理（[限制、更新與條款](limits.md#personal-data)）。

下一步：[轉換對戰](converting.md)。
