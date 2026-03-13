---
name: gpu-cli
description: 通过一个带有前置检查（preflight checks）和预算/时间限制的守护程序（wrapper，即 `runner.sh`），可以安全地运行本地的 `GPU` 命令。
argument-hint: runner.sh gpu [subcommand] [flags]
allowed-tools: Bash(runner.sh*), Read
---
# GPU CLI技能（稳定版本）

使用此技能可以从您的代理程序中运行本地的`gpu`二进制文件。该技能仅支持调用内置的`runner.sh`脚本（该脚本会内部调用`gpu`），并仅允许进行只读文件操作。

**功能说明：**
- 执行您指定的`gpu`命令（例如：`runner.sh gpu status --json`、`runner.sh gpu run python train.py`）。
- 建议先执行`gpu doctor --json`以进行预检查，然后再执行`gpu status --json`。
- 将执行结果输出到聊天界面；使用`--json`选项可获取结构化的数据输出。

**安全与权限范围：**
- 允许使用的工具：`Bash(runner.sh*)`、`Read`权限。该技能不请求网络访问权限；`gpu`脚本负责处理自身的网络通信。
- 请避免使用命令链或重定向操作；请直接使用`runner.sh gpu ...`命令进行操作。
- 您需要直接与提供者支付费用；使用此技能可能会启动付费的容器（pod）。

**常用指令：**
- “运行`runner.sh gpu status --json`并总结容器的运行状态。”
- “运行`runner.sh gpu doctor --json`并汇总出现的故障信息。”
- “运行`runner.sh gpu inventory --json --available`，并推荐每小时费用低于0.50美元的GPU资源。”
- “运行`runner.sh gpu run echo hello`，然后输出结果。”

**注意事项：**
- 对于图像处理、视频处理或大语言模型（LLM）相关的任务，请要求代理程序添加相应的参数（例如：`--gpu-type "RTX 4090"`、`-p 8000:8000`或`--rebuild`）。