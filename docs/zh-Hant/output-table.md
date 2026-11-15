---
title: "表格"
nav_order: 4
lang: "zh-Hant"
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# 表格：`<demo>.parquet` {#the-table-parquet}

每一個取樣或事件佔一列。只要伺服器複製了 actor 的移動，就會取樣一次，移動時最多每秒 8 次（即對戰的錄製速率）。

![合成對戰表格的前幾列](../assets/img/table.svg)

## 欄位 {#columns}

| 欄位 | 內容 |
|---|---|
| `time` | 自錄製開始以來的秒數 |
| `x`、`y`、`z` | 以 Unreal 單位（公分）表示的位置，Z 軸朝上 |
| `dirX`、`dirY`、`dirZ` | 士兵的視線方向：身體的偏航角與視角的俯仰角，以單位向量表示（載具則是水平的） |
| `yaw`、`pitch` | 同樣的內容，以度為單位；`pitch` 為自地平線向上的角度，僅適用於士兵 |
| `health` | 當時士兵、機器人或載具的生命值，若伺服器有送出（士兵在受傷時可能降到 0 以下） |
| `speed` | 複製的速度，公分/秒 |
| `player` | 玩家的名稱；機器人為 `bot <id>`；無人擁有的載具或可部署物則為其類別；載具武器的射擊，則為坐在該載具上的玩家 |
| `team`、`faction` | Squad 的隊伍編號（1、2）與其陣營設定，**以當時為準**：玩家可以換邊 |
| `squad` | 小隊編號，不在小隊中時為 -1 |
| `event` | 這一列是什麼（見下文） |
| `pawn` | 士兵藍圖（機器人為 `SQSquidBot`）、載具，或對於 `fire` 而言為武器 |
| `seat` | 對於砲塔或乘客座位，為該座位自己的 pawn |
| `detail` | 對於 `fire`，為放置該次射擊的武器呼叫；對於 `hit`，為傷害類型；對於 `removed`，為通道關閉的原因（`Destroyed`、`Dormancy`……） |
| `entity` | 這一列所描述的 actor（其網路 GUID）：即附屬檔中列的 `entity` |
| `match` | 該對戰的名稱 |

## 事件 {#events}

| `event` | 出現在這些列 | 內容 |
|---|---|---|
| `position` | 步行中的士兵或機器人 | 一次移動取樣 |
| `vehicle` | 在地面載具或直升機中的士兵 | 在載具位置的一次取樣 |
| `wounded`、`revived`、`death` | 士兵與機器人 | 發生的位置 |
| `spawn`、`damaged`、`destroyed`、`removed` | 載具、可部署物、砲台、彈藥箱、直升機 | 它們當時所在的位置 |
| `seat` | 玩家 | 坐上座位 |
| `fire` | 射手 | 一次射擊：離開的位置，其方向為 `yaw`/`pitch`/`dirX..Z` |
| `hit` | 載具 | 一次載具命中：位置 |

事件如何被讀取，見[對戰如何被讀取](how-it-works.md#how-the-events-are-read)。

## 在檢視器中 {#in-the-viewer}

Parquet 的 footer 在 `heat3d` 鍵下帶有讀取說明：Z 軸朝上、沒有任何軸被鏡像、單位比例為 1，因此檢視器不需要任何欄位對應。請在熱圖分頁中載入表格；參見檢視器的
[載入資料](https://holdi601.github.io/3DHeat/getting-data-in.html)
與[欄位對應](https://holdi601.github.io/3DHeat/column-mapping.html)。
