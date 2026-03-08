---
name: clawculator
description: 分析 OpenClaw 的运行成本并检测计费问题。源代码已完全打包，运行时无需下载任何额外内容；仅需要节点二进制文件即可使用。
homepage: https://github.com/echoudhry/clawculator
user-invocable: true
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["node"]}}}
---
## clawculator

这是一个用于 OpenClaw 的成本审计工具，能够检测配置文件、会话记录和工作空间中的计费问题。该工具完全基于确定性逻辑进行检测，不使用人工智能、不进行网络请求，也不依赖任何外部组件。

**源代码已完整包含在该技能文件夹中。** 在运行时不会下载任何数据；您可以在执行该工具之前对所有文件进行审计。

**该工具会读取的文件：**
- `~/.openclaw/openclaw.json`：您的 OpenClaw 配置文件
- `~/.openclaw/agents/main/sessions/sessions.json`：会话令牌的使用情况
- `~/clawd/`：仅统计工作空间的根目录文件数量（不读取文件内容）
- `/tmp/openclaw`：日志目录（仅读取，如果存在的话）

**该工具可能写入的文件（仅在使用 `--md` 选项时）：**
- `./clawculator-report.md`：Markdown 格式的报告文件
- 通过 `--out=PATH` 指定自定义输出路径

**该工具不会发起任何网络请求，也不会执行任何 shell 命令。**

**所有输出中的会话密钥都会被截断**（仅显示前 8 个字符及省略号），以防止敏感信息被泄露。

---

**使用方法**

当用户输入 `clawculator`、`check my costs`、`analyze spend` 或 `cost report` 时，执行以下操作：

```bash
node {baseDir}/run.js --md
```

将完整的 Markdown 报告直接显示给用户。

当用户输入 `snapshot`、`share my grade`、`cost grade`、`clawcalculator snapshot` 或 `what's my grade` 时，执行以下操作：

```bash
node {baseDir}/run.js --snapshot
```

将终端输出结果直接显示给用户。该输出会显示用户的成绩（A+ 到 D）、成本范围、配置复杂度以及检测结果，非常适合截图分享。

**常用参数：**
- `--snapshot`：生成可分享的成绩卡片（适用于终端输出，可直接截图）
- `--md`：生成 Markdown 报告并输出到标准输出（stdout）
- `--json`：将检测结果以机器可读的 JSON 格式输出到标准输出
- `--out=PATH`：为 `--md` 指定自定义输出路径
- `node {baseDir}/run.js --help`：查看完整的使用说明

**该工具能检测到的问题包括：**
- 💓 在付费模型上使用了错误的模型（如 Ollama 而不是正确的模型）
- 🔧 在付费模型上存在持续运行的技能轮询循环
- 📱 在主模型上自动加入了 WhatsApp 群组
- 🪝 在 Sonnet 模型上启用了某些钩子（如 boot-md、command-logger、session-memory）
- 🤖 并发会话数量过高（可能导致成本激增）
- 📁 工作空间根目录文件过多，导致系统资源占用增加
- ⚙️ 主模型的成本使用情况异常

所有检测结果都会附带相应的修复命令。