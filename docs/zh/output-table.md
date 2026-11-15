---
title: 表格
nav_order: 4
lang: zh
source: output-table.md
source_hash: "0f3cfed1c108"
nav_exclude: true
search_exclude: true
---
# 表格：`<demo>.parquet` {#the-table-parquet}

每行对应一个采样或一个事件。只要服务器复制了角色的移动，就会进行一次采样，最多每秒 8 次（录像的录制频率），前提是角色在移动。

![一个合成录像表格的前几行](../assets/img/table.svg)

## 列 {#columns}

| 列 | 含义 |
|---|---|
| `time` | 自录制开始以来的秒数 |
| `x`、`y`、`z` | 位置，单位为虚幻单位（厘米），Z 轴朝上 |
| `dirX`、`dirY`、`dirZ` | 士兵的朝向：身体的偏航角和视角的俯仰角，以单位向量表示（载具则为水平） |
| `yaw`、`pitch` | 同样的内容，以角度表示；`pitch` 为相对地平线向上的角度，仅适用于士兵 |
| `health` | 该时刻士兵、机器人或载具的生命值，在服务器发送它的地方（受伤时士兵的生命值会降到 0 以下） |
| `speed` | 复制的速度，单位厘米/秒 |
| `player` | 玩家名称；机器人为 `bot <id>`；对于无人拥有的载具或可部署设备，为其类名；对于载具武器的射击，为坐在该载具上的玩家 |
| `team`、`faction` | Squad 的队伍编号（1、2）及其阵营设置，**以该时刻为准**：玩家可以换边 |
| `squad` | 小队编号，不在小队中时为 -1 |
| `event` | 该行是什么（见下文） |
| `pawn` | 士兵蓝图（机器人为 `SQSquidBot`）、载具，或者对于 `fire` 而言为武器 |
| `seat` | 对于炮塔或乘客座位，即该座位自身的角色 |
| `detail` | 对于 `fire`，为放置该次射击的武器调用；对于 `hit`，为伤害类型；对于 `removed`，为通道关闭的原因（`Destroyed`、`Dormancy`……） |
| `entity` | 该行所涉及的角色（其网络 GUID）：即附属文件中行的 `entity` |
| `match` | 录像的名称 |

## 事件 {#events}

| `event` | 出现在哪一行 | 内容 |
|---|---|---|
| `position` | 步行中的士兵或机器人 | 一次移动采样 |
| `vehicle` | 乘坐地面载具或直升机的士兵 | 载具位置上的一次采样 |
| `wounded`、`revived`、`death` | 士兵和机器人 | 发生的位置 |
| `spawn`、`damaged`、`destroyed`、`removed` | 载具、可部署设备、炮位、弹药箱、直升机 | 它们所在的位置 |
| `seat` | 玩家 | 入座 |
| `fire` | 射手 | 一次射击：子弹离开的位置，其方向为 `yaw`/`pitch`/`dirX..Z` |
| `hit` | 载具 | 载具被击中：击中位置 |

事件如何被读取，见 [如何读取录像](how-it-works.md#how-the-events-are-read)。

## 在查看器中 {#in-the-viewer}

Parquet 文件的页脚在 `heat3d` 键下包含读取说明：Z 轴朝上，没有镜像的轴，单位比例为 1，因此查看器无需进行列映射。
在热力图标签页中加载表格即可；参见查看器的 [数据导入](https://holdi601.github.io/3DHeat/getting-data-in.html)
和 [列映射](https://holdi601.github.io/3DHeat/column-mapping.html)。
