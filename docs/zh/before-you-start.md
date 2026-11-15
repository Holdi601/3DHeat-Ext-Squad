---
title: 开始之前
nav_order: 1.5
lang: "zh"
source: before-you-start.md
source_hash: "ca4b6281fdfc"
nav_exclude: true
search_exclude: true
---
# 开始之前 {#before-you-start}

第一次使用命令行？本页带你从零开始完成第一次运行。
只需花大约十分钟，做一次即可。

## 1. 安装 Python {#install-python}

本工具需要 **Python 3.10 或更高版本**。

- **Windows：** 从 [python.org/downloads](https://www.python.org/downloads/) 下载 Python 并运行安装程序。在第一个界面勾选 **Add python.exe to PATH**，
  然后点击 **Install Now**。
- **macOS 和 Linux：** 系统中通常已经有 Python 3。页面中写 `python` 的地方，请输入 `python3`。

## 2. 获取本工具 {#get-this-tool}

打开 [github.com/Holdi601/3DHeat-Ext-Squad](https://github.com/Holdi601/3DHeat-Ext-Squad)，点击绿色的 **Code** 按钮，然后点击 **Download ZIP**，
解压到你选择的文件夹中。如果你使用 git：`git clone https://github.com/Holdi601/3DHeat-Ext-Squad`。

## 3. 在该文件夹中打开终端 {#open-a-terminal-in-that-folder}

终端是一个用来输入命令的窗口。

- **Windows：** 在资源管理器中打开该文件夹，点击地址栏，输入
  `powershell` 并按回车。一个蓝色或黑色的窗口会打开，并且已经位于该文件夹中。
- **macOS：** 打开 **终端（Terminal）**，输入 `cd `（注意后面有一个空格），把文件夹拖进窗口，然后按回车。

`cd` 的意思是“切换文件夹”：`cd C:\Tools\3DHeat-Ext-Squad` 会进入那个文件夹。

## 4. 安装本工具 {#install-the-tool}

输入以下内容并按回车：

```bash
python -m pip install -e .
```

结束时你应该会看到：`Successfully installed heat3d-ext-squad-demo-...`。

## 5. 运行 {#run-it}

```bash
heat3d-squad-demo --version
```

你应该会看到类似下面的内容：

```text
heat3d-squad-demo 0.1.0
```

下一步：[录制录像](recording.md)，然后是 [转换录像](converting.md)。

## 如何阅读这些页面中的命令 {#how-to-read-the-commands-on-these-pages}

| 你看到的 | 含义 |
|---|---|
| `<folder>` | 占位符：请改为你自己的值，不要输入 `< >` |
| `[--force]` | 可选：可以省略，也可以按所示原样输入 |
| `a\|b` | 二选一：输入 `a` 或 `b` |
| `# a note` | 给你的注释：不要输入 |
| `"C:\My Files\x"` | 路径中有空格时，请加上引号 |
| `D:\Demos` | Windows 文件夹的示例：请使用你自己的路径 |

## 出现问题时 {#when-something-goes-wrong}

| 提示信息 | 怎么办 |
|---|---|
| `'python' is not recognized` | 未安装 Python，或者没有勾选 PATH 选项：重新安装并勾选（或者输入 `py` 代替 `python`）。 |
| `'heat3d-squad-demo' is not recognized` | 在工具所在的文件夹中重新执行第 4 步，或者输入 `python -m heat3d_ext_squad` 代替 `heat3d-squad-demo`：两者效果相同。 |
| `No module named heat3d_ext_squad` | 你不在工具所在的文件夹中，或者第 4 步失败了：用 `cd` 进入该文件夹，然后执行第 4 步。 |
| `No module named pip` | 运行 `python -m ensurepip`，然后执行第 4 步。 |
| 其他任何情况 | 阅读信息的最后一行，然后带着这一行在 GitHub 上提交 issue。 |

每条命令结束时都会给出一个**退出状态**：0 表示成功。要查看它，在 PowerShell 中输入 `echo $LASTEXITCODE`，在 macOS 和 Linux 中输入 `echo $?`。
