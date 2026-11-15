---
title: 对局文档与附属文件
nav_order: 5
lang: zh
source: output-match.md
source_hash: "715bd3417e47"
nav_exclude: true
search_exclude: true
---
# 对局文档与附属文件 {#the-match-document-and-sidecars}

每个录像除了表格之外，还会生成 `<demo>.match.json` 和两个附属文件，
`<demo>.entities.parquet` 与 `<demo>.packets.parquet`。查看器在其对局标签页中读取对局文档。

## 对局文档 {#the-match-document}

`<demo>.match.json`（对局文档）的顶层包含 `map`、`layer`、`level_path`、`game_version`、`engine_version`、`recorded_unix`、`duration_s`、`teams`、`squads`、`game_state`、`actors`、`players`、`rows`、`events`、`not_read`、`file`、`header`、`chunks`、`stream`、`shots` 和 `selfCheck`（完整列表：[命令参考](../cli-reference.md)）。用文字说明，它包括：地图和关卡层、游戏和引擎版本、录制时间、时长，以及：

- **队伍**：编号、阵营，以及其状态中复制的全部内容（点数、可用性、指挥官），按变化记录；
- **小队**：编号、队伍、名称、创建者、队长、成员；
- **游戏状态**：服务器名称和设置、游戏模式、对局状态和 ID、地图和关卡轮换、投票、计时器、每日消息；
- **角色**：每一辆载具、可部署设备、炮位、弹药箱和直升机，包括类别、位置和生成时间、消失时间、所属者，以及其复制的状态（生命值、建造状态、座位……）；
- **每个玩家一行**：步行和乘车的采样、步行距离、扮演过的士兵职业、使用过的载具、换队记录、占据过的座位，以及玩家状态中复制的全部内容（延迟、等级、角色、当前座位……）；每个机器人也有一行；
- **事件**的计数、**属性普查**（每个类的属性被发送的次数）和**远程调用普查**、开火和击中、**未读取**的内容，以及读取器的诊断信息；
- **文件和文件头**：信息块和录像文件头的每个字段、数据块表、网络字段导出表（`net_field_exports`）、通道的关闭原因，以及为导出表未命名的对象找到的类（`stream.class_resolution`）；
- **自我检查**（`selfCheck.completeness`，见 [完整性](#completeness)）。

在线 ID（Steam、EOS）被有意省略。

快速查看一个已转换的录像：

```bash
python -c "import json; d = json.load(open('out/<map>/<demo>.match.json')); print(d['map'], d['layer'], d['duration_s'], len(d['players']))"
```

## 完整性 {#completeness}

本读取器遵循所有 3DHeat 转换工具共同的规则：能现在解码的就解码，其余的完整保留，并说明每一类内容保留了多少（[转换器保留一切](https://github.com/Holdi601/3DHeat/blob/main/docs/converters.md)）。每个对局文档都有 `selfCheck.completeness`：对于录像中遇到的每一类项目，给出 `seen`（见到的数量）、`decoded`（已完全解码）、`partial`（部分解码并完整保留）、`raw`（仅完整保留）和 `lost`（必须为 0）。项目的分类是在读取器遇到它们的地方统计的：`file.info`、`chunk.<kind>`、`frame`、`packet`、`bunch`、`open`、`close`、`export.field`、`export.guid`、`external`、`property:<class>`、`rpc:<class>`、`block:<object>`、`subobject.*`。

在所读取的真实录像上，`lost` 为 0：这些项目的数量从几十万到几百万不等；约一半可以完全解码，其余为部分解码或仅原样保留。

**已读取**（写入表格和对局文档）：

- 信息块、录像文件头（每个字段；两个未知的末尾字节以十六进制保留）、数据块表；
- 每一帧、每一个数据包和每一个数据束（完整拆分为其所携带的内容），每一个被打开的角色（包括其生成位置、旋转、缩放和速度），以及每一个被关闭的角色（并附上原因：`Destroyed`、`Dormancy`……）；
- 每一个复制的属性，只要其位能够说明（[解码属性](how-it-works.md#decoding-properties)），包括来自 `FRepMovement` 和直升机移动组件的位置、伤亡、载具生命值、座位；
- 每一次远程调用，按名称记录，若录像导出了该函数的组，则附带其参数：开火（`fire`）和载具击中（`hit`）写入表格；
- 网络字段导出表和网络 GUID（其数量；路径在实体附属文件中）。

**原样保留**（完整保留，旁边附有已读取的部分）：

- `<demo>.entities.parquet`，列为 `time`、`type`（`<class>.<property>`、`<class>.<call>`，或对象的名称）、`name`（角色的类）、`entity`（角色的网络 GUID，即表格中的 `entity`）、`kind`、`object`（子对象）、`channel`、`handle`、`group`（导出组的类路径）、`decoded`（JSON）、`bits` 和 `payload`（位，最低位在前，补齐为整字节）：
  - 每一次属性更新（`kind` 为 `property`），包括移动数据，并附上已解码的内容；只有在无法解码的情况下才保留原样（未命名的句柄、炮塔的 `RotationReplicatedMovement` 等结构，以及保留为位的属性）；
  - 每一次远程调用和自定义增量字段（`rpc`），若函数的组已导出则解码其参数；否则保留原样（`RepInventory`、`PlayerStateData`）；
  - 每一个类无法找到的对象的每个内容块（`block`：`Buoyancy`、`GameplayTasksComponent`、`AmmoRackComponent`……），并解码其块头；
  - 每一个被打开和关闭的角色通道（`open`、`close`），以及每一个被删除或销毁的子对象；
  - 后续解码器仅凭该文件即可读取所需的上下文：每个网络字段导出（`export.field`：组路径、句柄、属性名、校验和）以及每个导出的网络 GUID（`export.guid`：其路径、外层对象和标志），按数据流给出时的时间记录；
- `<demo>.packets.parquet`，列为 `time`、`type`、`name`、`channel`、`offset`（在文件中的位置）、`decoded`、`bits` 和 `payload`：信息块、文件头数据块、每一个检查点数据块（检查点是每个角色在其时间点的状态，从头开始的数据流中也包含这些状态）、每一个事件数据块，以及每一个无法读取的帧、数据包或数据束（每个录像一个数据束：录制者自身观战角色的开头数据束），完整保留。

附属文件的行按 `kind`、`type` 和 `entity` 分组，每组内按时间顺序排列；按 `time` 排序即可得到数据流的顺序。

**不可用的内容：**

- 服务器录像未记录的内容：客户端的输入，以及玩家所看到的画面；
- 客户端的效果：击中标记、声音、击杀信息的文字（服务器发送的是调用，而不是它们的显示）；
- 已解码的在线 ID：只保留为位（见 [个人数据](limits.md#personal-data)）。
