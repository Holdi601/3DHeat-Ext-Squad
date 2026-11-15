---
title: "限制、更新與條款"
nav_order: 7
lang: zh-Hant
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# 限制、更新與條款 {#limits-updates-and-terms}

## 未被讀取的內容 {#not-read}

- **誰殺了誰，以及士兵因命中而受到的傷害。** 這些資料會透過武器與玩家狀態的遠端呼叫的命中結果傳送（`HitResultsZeroBased`、`MulticastOnImpact.Hit`），而其結構尚未被讀取；它們完整保留在實體附屬檔中。只有受害者的生命值會被解碼。
- **機器人的隊伍。** 機器人的狀態中有一個數字，可能是它的隊伍；未經確認，也未被使用。
- **士兵向側面看的方向**，超出身體偏航角的部分。

## 遊戲更新 {#game-updates}

讀取器依賴引擎的對戰格式，以及少數 Squad 的類別與屬性名稱。它不依賴那些它看不見的屬性版面：對戰檔案會自行命名這些內容。

**Squad 更新可能造成的問題：**

- **引擎升級。** Squad 在 v10.4 升級到 UE 5.7，而這在此尚未測試。此升級可能會改變 bunch 標頭、生成資料或 `FRepMovement`。在程式碼中，已知變動的步驟都有依版本控制。未知的步驟（`ENG_PARTIAL_CUSTOM_EXPORTS`、尾端的移動位元）則固定為 v10.3.1 的做法。
- **Iris 複製。** 如果 Squad 改用 Iris，區塊內的串流將會是新的，而此讀取器無法讀取。Squad v10.3.1 使用傳統系統（它執行 ReplicationGraph）。
- **類別或屬性改名。** 如果 Squad 改了玩家、隊伍或小隊類別的名稱，或它們的屬性名稱，名稱或隊伍會遺失，但位置不會。
- **失敗時會發生什麼。** 格式改變時，讀取器會在診斷中以串流錯誤或移動錯誤大聲失敗。它不會悄悄產生錯誤的位置：只有當 `FRepMovement` 的位元完全吻合時才會接受。

## 個人資料 {#personal-data}

對戰檔案包含伺服器上每個人的名稱與線上 ID。表格與對戰文件只包含名稱，不含 ID。附屬檔保留每個屬性的位元，因此也包含 ID，與對戰檔案本身相同（未解碼）。請把它們全都當作對戰檔案本身來處理。

## 授權與來源 {#licence-and-sources}

MIT；見 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE)。這裡的一切都是為本套件撰寫的。沒有包含或連結任何第三方程式碼：唯一的相依項目是 pyarrow（Apache-2.0）與 numpy（BSD-3-Clause）。

關於格式的資訊，來源如下：

- **[FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor) 中的 Unreal.Core**（MIT）。它描述一般的 Unreal 對戰版面：資訊區塊、區塊、影格、bunch 與網路欄位匯出。
- **[squad-replay](https://github.com/Codycody31/squad-replay)**（MPL-2.0）。我們閱讀其解析器，以了解 Squad v10.3.1 寫入的版面、版本檢查，以及哪些 Squad 類別帶有名冊資料。其已發布的測試對戰與計數快照，被用作獨立的交叉驗證。其程式碼沒有被複製或翻譯：本讀取器的結構不同（以整個封包為單位的 Python 位元陣列、以位元方式接合部分 bunch、依名稱分派屬性），而有兩件它未做的事，是在對戰本身上發現的：第三個部分 bunch 旗標，以及尾端的移動位元。

Squad 是 Offworld Industries 的商標。本套件讀取 Squad 伺服器寫出的檔案；它不會觸及遊戲、其程式碼或其封存檔。Offworld 的伺服器授權與管理政策，對於錄製與分析對戰並無規定。Squad 的使用者授權協議禁止對遊戲本身進行逆向工程，而本套件並不這麼做。
