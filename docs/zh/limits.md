---
title: 限制、更新与条款
nav_order: 7
lang: zh
source: limits.md
source_hash: "ef3802087acc"
nav_exclude: true
search_exclude: true
---
# 限制、更新与条款 {#limits-updates-and-terms}

## 未读取的内容 {#not-read}

- **谁击杀了谁，以及按击中计算的对士兵的伤害。** 这些信息在武器和玩家状态的远程调用中传递（`HitResultsZeroBased`、`MulticastOnImpact.Hit`），而其结构尚未读取；它们被完整保存在实体附属文件中。只解码了受害者的生命值。
- **机器人的队伍。** 机器人的状态中有一个数字，它可能是其队伍编号；尚未确认，也未使用。
- **士兵侧身观察的方向**，超出身体偏航角的部分。

## 游戏更新 {#game-updates}

读取器依赖于引擎的录像格式，以及少数 Squad 类和属性的名称。它不依赖于它看不到的属性布局：这些布局由录像自己标注。

**Squad 更新可能导致的问题：**

- **引擎升级。** Squad 在 v10.4 中升级到了 UE 5.7，但这一版本尚未测试。升级可能会改变数据束头、生成数据或 `FRepMovement`。在已知这些步骤的地方，代码会根据版本进行区分。未知的步骤（`ENG_PARTIAL_CUSTOM_EXPORTS`、末尾的移动位）则按 v10.3.1 的行为固定。
- **Iris 复制。** 如果 Squad 改用 Iris，数据块内的数据流将是新的，本读取器将无法读取。Squad v10.3.1 使用经典系统（它运行 ReplicationGraph）。
- **类或属性被重命名。** 如果 Squad 重命名了其玩家、队伍或小队类或它们的属性，名称或队伍信息会丢失，但位置信息不会。
- **出错时会怎样。** 当格式发生变化时，读取器会明确报错，在诊断信息中给出数据流错误或移动错误。它不会悄悄地产生错误的位置：只有当 `FRepMovement` 的位完全吻合时，才会接受它。

## 个人数据 {#personal-data}

录像中包含服务器上每个人的名称和在线 ID。表格和对局文档只包含名称，不包含 ID。附属文件保留了每个属性的位，因此其中包含的 ID 与录像中的一样（未解码）。请像对待录像本身一样对待所有这些文件。

## 许可证与来源 {#licence-and-sources}

MIT 许可证；参见 [`LICENSE`](https://github.com/Holdi601/3DHeat-Ext-Squad/blob/main/LICENSE)。这里的一切都是为本软件包专门编写的。不包含也不链接任何第三方代码：唯一的依赖是 pyarrow（Apache-2.0）和 numpy（BSD-3-Clause）。

关于格式的信息来源如下：

- **Unreal.Core**，见 [FortniteReplayDecompressor](https://github.com/Shiqan/FortniteReplayDecompressor)（MIT）。它描述了通用的虚幻录像布局：信息块、数据块、帧、数据束和网络字段导出。
- **[squad-replay](https://github.com/Codycody31/squad-replay)**（MPL-2.0）。我们阅读了它的解析器，以了解 Squad v10.3.1 写入的布局、版本检查，以及哪些 Squad 类携带名单数据。它发布的测试录像和快照计数被用作独立的交叉验证。它的代码没有被复制或翻译：本读取器的结构不同（基于整个数据包的 Python 位归档，按位拼接的部分数据束，按名称分派的属性），并且在录像本身上发现了它没有处理的两件事：第三个部分数据束标志，以及末尾的移动位。

Squad 是 Offworld Industries 的商标。本软件包读取的是 Squad 服务器写出的文件；它不会接触游戏本身、其代码或其归档。Offworld 的服务器许可和管理政策未对录制或分析录像作出规定。Squad 的最终用户许可协议禁止对游戏本身进行逆向工程，而本软件不做这件事。
