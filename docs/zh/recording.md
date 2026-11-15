---
title: 录制录像
nav_order: 2
lang: zh
source: recording.md
source_hash: "5139aa7d896f"
nav_exclude: true
search_exclude: true
---
# 录制录像 {#recording-a-demo}

Squad 的录像是在**服务器上**录制的，而不是由游戏客户端录制。

1. 在服务器的 `Admins.cfg` 中，给管理员所在的组授予 `demos` 权限。
2. 对局开始时，在游戏的控制台中运行 `AdminDemoRec <name>`。
   管理员必须在游戏中亲自输入这条命令；有报告称 RCON 不接受它。
3. 进行完对局后，运行 `AdminDemoStop`。
4. 录像会被写入 `<server>/SquadGame/Saved/Demos/<name>.replay`。
   将它从服务器复制到用于转换的电脑上。

`Server.cfg` 中也有一个 `RecordDemos` 设置，默认关闭。小型对局的录像大约每小时 70 到 80 MB；满员 100 人服务器的大小尚未测量。

录像中包含服务器上每个人的名称和在线 ID：请将其视为个人数据（[限制、更新与条款](limits.md#personal-data)）。

下一步：[转换录像](converting.md)。
