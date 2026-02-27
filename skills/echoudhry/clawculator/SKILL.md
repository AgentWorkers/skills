---
name: clawculator
description: 分析 OpenClaw 的运行成本并检测计费问题。源代码已完全打包在软件中，运行时无需下载任何额外文件；仅需节点二进制文件即可使用。
homepage: https://github.com/echoudhry/clawculator
user-invocable: true
metadata: {"openclaw":{"emoji":"🦞","requires":{"bins":["node"]}}}
---
## clawculator

这是一个用于 OpenClaw 的成本审计工具，能够检测配置文件、会话记录和工作区中的计费问题。该工具完全基于确定性逻辑进行检测，不使用人工智能、不进行网络请求，也不依赖任何外部服务。

**源代码已完整包含在该技能文件夹中。** 在运行时不会下载任何数据；您可以在运行前对所有文件进行审计。

**该工具会读取的文件：**
- `~/.openclaw/openclaw.json` —您的 OpenClaw 配置文件
- `~/.openclaw/agents/main/sessions/sessions.json` — 会话令牌的使用情况
- `~/clawd/` — 工作区的根目录文件数量（不读取文件内容）
- `/tmp/openclaw` — 日志目录（仅读取，如果存在）

**该工具可能写入的文件（仅在使用 `--md` 选项时）：**
- `./clawculator-report.md` — markdown 格式的报告文件
- 通过 `--out=PATH` 指定自定义输出路径

**该工具不会发起任何网络请求，也不会执行任何 shell 命令。**

**所有输出中的会话密钥都会被截断**（仅显示前 8 个字符并加上省略号），以避免泄露敏感信息。

---

**使用方法**

当用户输入 `clawculator`、`check my costs`、`analyze spend` 或 `cost report` 时，运行以下命令：

```bash
node {baseDir}/run.js --md
```

系统会立即将完整的 markdown 报告返回给用户。

**可选参数：**
- `--md` — 生成 markdown 报告并输出到标准输出（stdout）
- `--json` — 生成机器可读的 JSON 格式报告并输出到标准输出
- `--out=PATH` — 指定 markdown 报告的输出路径
- `node {baseDir}/run.js --help` — 查看完整的使用说明

**该工具可以检测以下问题：**
- 💓 在付费模型上运行的心跳检测脚本（而非 Ollama）
- 🔧 在付费模型上运行的技能轮询循环
- 📱 在主模型上自动加入的 WhatsApp 群组
- 🪝 在 Sonnet 系统上启用的钩子（如 boot-md、command-logger、session-memory）
- 💬 仍然持有会话令牌的孤立会话
- 🤖 过高的 `maxConcurrent` 值（导致成本激增）
- 📁 工作区根目录文件过多，导致资源占用过高
- ⚙️ 主模型的成本使用情况

所有检测结果都会附带相应的修复命令。