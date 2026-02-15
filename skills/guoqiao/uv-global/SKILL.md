---
name: uv-global
description: 为临时使用的 Python 脚本提供一个全局的 UV（User-Defined）环境，并允许该环境被重复使用。
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://github.com/guoqiao/skills/blob/main/uv-global/uv-global/SKILL.md","os":["darwin","linux"],"tags":["python","uv","global","venv"],"requires":{"anyBins":["brew","uv"]}}}
---

# UV Global

在 `~/.uv-global` 文件夹中创建并重用一个全局的 `uv` 环境，这样你就可以为快速、临时性的脚本安装 Python 依赖项，而不会污染系统的解释器环境。

这个设置非常快速，可以随时为临时任务提供一个共享的虚拟环境。

当用户需要使用未预装的 Python 包（如数据处理、网络爬虫等），且不需要创建完整的项目特定环境时，可以使用此功能。如果用户明确希望使用系统的 Python 解释器或项目内部的虚拟环境（`venv`），则可以跳过此步骤。

## 必备条件

必须已经安装了 `uv`。如果尚未安装，需要在 macOS/Linux 系统上使用 `brew`，或在 Linux 系统上使用 `curl` 来安装 `uv`。

## 安装

```bash
bash ${baseDir}/install.sh
```

脚本将执行以下操作：
- 通过 `brew`（macOS/Linux）或官方的 `curl` 安装程序来安装 `uv`（如果尚未安装）；
- 在 `~/.uv-global` 文件夹中创建一个全局的 `uv` 环境；
- 在 `~/.uv-global/.venv` 文件夹中创建一个包含常用 Python 包的虚拟环境；
- 在 `~/.uv-global/.venv/bin` 文件夹中创建一些有用的工具脚本（shims）。

[可选] 将虚拟环境的 `bin` 路径添加到系统的 `PATH` 环境变量中，这样 `python` 命令就会默认使用全局环境，并且这些工具脚本也能被使用：

```
export PATH=~/.uv-global/.venv/bin:$PATH
```

## 使用方法

对于任何需要额外依赖项的快速 Python 脚本，可以使用以下命令：

```bash
# install required packages into the global env
uv --project ~/.uv-global add <pkg0> <pkg1> ...

# write your code
touch script.py

# run your script using the global env
uv --project ~/.uv-global run script.py
```

提示：
- 脚本可以保存在任何位置；`--project ~/.uv-global` 参数可以确保脚本使用全局环境运行。
- 可以使用 `uv --project ~/.uv-global pip list` 命令来查看已安装的包。
- 如果某个任务发展成为一个真正的项目，建议切换到项目内部的虚拟环境，而不是使用这个全局环境。