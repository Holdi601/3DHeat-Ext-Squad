---
title: 转换录像
nav_order: 3
lang: "zh"
source: converting.md
source_hash: "e8c77423085b"
nav_exclude: true
search_exclude: true
---
# 转换录像 {#converting-demos}

```text
heat3d-squad-demo <demos or folders> -o <folder> [--flat] [--json]
python -m heat3d_ext_squad ...          同上，无需安装
```

## 逐步说明 {#step-by-step}

第一次使用命令行？请先阅读 [开始之前](before-you-start.md)。

1. 安装一次：`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`，
   在该文件夹中打开终端，运行 `python -m pip install -e .`
   （需要 Python 3.10 或更高版本；它会自动安装 pyarrow 和 numpy）。
2. 把 `.replay` 文件放进一个文件夹，或者逐个指定文件名。
3. 运行 `heat3d-squad-demo <folder> -o out`。
4. 每个录像会输出一行信息：它的层级、玩家数和行数，以及表格被写到了哪里。每个录像会在 `out/<map>/` 中生成四个散开的文件（不是 `.3dheat` 容器）；在 3DHeat 查看器中加载 `.parquet` 文件即可。

![对一个示例录像的运行结果](../assets/img/run.svg)

图片展示的是测试程序构建的一个示例录像（`tests/test_stream.py`）上的运行结果，而不是真实的对局。

## 选项 {#options}

| 选项 | 默认值 | 作用 |
|---|---|---|
| `demos`（一个或多个） | - | `.replay` 文件，或者存放它们的文件夹 |
| `-o`、`--out` | 必填 | 写入的目标文件夹；每个录像写入 `<out>/<map>/` |
| `--flat` | 关闭 | 直接写入该文件夹，不再创建 `<map>/` 子文件夹 |
| `--json` | 关闭 | 为每个录像在标准输出打印一行 JSON（供其他程序调用本命令）：`demo`、`ok`、`parquet`、`match`、`sidecars`、`lost`、`rows`、`players`、`layer`、`recorded_unix`；转换失败的录像则打印 `demo`、`ok: false` 和 `error` |
| `--version` | - | 打印版本号并退出 |

每个选项的完整说明，即程序自己打印的内容：[命令参考](../cli-reference.md)。

地图文件夹使用录像中记录的关卡路径里的地图名（`/Game/Maps/<Map>/Gameplay_Layers/<Layer>` 对应 `<Map>`）。

退出状态：当所有录像都转换成功时为 0；当有任何一个失败（其余录像仍会写出）或者找不到任何 `.replay` 文件时为 1。

## 输出内容 {#what-comes-out}

| 文件 | 内容 |
|---|---|
| `<demo>.parquet` | 表格：位置和事件，每行一条（[表格](output-table.md)） |
| `<demo>.match.json` | 对局文档（[对局文档](output-match.md)） |
| `<demo>.entities.parquet` | 附属文件：每一次属性更新和远程调用，完整保留 |
| `<demo>.packets.parquet` | 附属文件：文件的数据块，以及未能读取的所有内容，完整保留 |

表格和对局文档与 3DHeat CS2 工具输出的是同一对文件。加载整个文件夹时，查看器直接打开表格，并忽略附属文件。

## 示例 {#examples}

```bash
heat3d-squad-demo D:\SquadDemos -o out                 # 一个文件夹中的所有录像
heat3d-squad-demo one.replay two.replay -o out --flat  # 直接写入 out/
heat3d-squad-demo D:\SquadDemos -o out --json          # 每个录像输出一行 JSON
```

`D:\SquadDemos` 是 D 盘上的示例文件夹：请使用你自己的路径。
