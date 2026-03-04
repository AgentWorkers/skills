---
name: leak-check
description: 扫描会话日志以查找泄露的凭据。该工具会对比 JSONL 格式的会话文件与已知的凭据模式，然后报告哪些 AI 提供商接收了这些数据。
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["node"]}}}
---
# 信息泄露检测

该脚本会扫描 OpenClaw 会话的 JSONL 文件，以检测是否存在敏感信息的泄露。它会报告数据实际来自哪个 AI 提供商（如 Anthropic、OpenAI、Google 等），同时会忽略内部传输过程中的数据复制或回显操作。

## 快速入门

```bash
# Check for leaked credentials (default: discord format)
node scripts/leak-check.js

# JSON output
node scripts/leak-check.js --format json
```

## 配置

需要检测的敏感信息配置信息存储在 `leak-check.json` 文件中。脚本会按以下顺序查找该文件：
1. **技能目录**（`./leak-check.json`）——为了保持与旧版本的兼容性
2. **`~/.openclaw/credentials/leak-check.json`**——推荐的位置（该文件会在通过 ClawHub 更新技能时被保留）

由于 ClawHub 会在更新技能时清除技能目录中的文件，请将配置文件放置在 `~/.openclaw/credentials/` 目录下，以避免数据丢失：

```bash
mkdir -p ~/.openclaw/credentials
cp leak-check.json ~/.openclaw/credentials/leak-check.json
```

您也可以通过 `--config` 参数指定配置文件的路径：

```json
[
  { "name": "Discord", "search": "abc*xyz" },
  { "name": "Postmark", "search": "k7Qm9x" }
]
```

**重要提示：** 请勿在该文件中存储完整的敏感信息。只需存储足够用于唯一识别这些信息的片段即可（例如，使用 `contains`、`begins-with` 或 `ends-with` 等匹配条件）。

**通配符模式：**
- `abc*` — 以 “abc” 开头
- `*xyz` — 以 “xyz” 结尾
- `abc*xyz` — 以 “abc” 开头且以 “xyz” 结尾
- `abc`（不使用通配符） — 包含 “abc” 这个字符串
- `""`（空字符串） — 跳过该条敏感信息

## 选项

- `--format <type>` — 输出格式：`discord`（默认）或 `json`
- `--config <path>` — 配置文件的路径（默认为 `./leak-check.json`，其次为 `~/.openclaw/credentials/leak-check.json`）
- `--help`, `-h` — 显示帮助信息

## 输出结果

### Discord 格式（默认）

```
🔐 **Credential Leak Check**

⚠️ **2 leaked credentials found**

**Discord Token**
• Session: `abc12345` | 2026-02-14 18:30 UTC | Provider: anthropic

**Postmark**
• Session: `def67890` | 2026-02-10 09:15 UTC | Provider: anthropic
```

如果未检测到泄露：

```
🔐 **Credential Leak Check**
✅ No leaked credentials found (checked 370 files, 7 credentials)
```

### 配置回显

如果在 OpenClaw 会话期间读取或修改了 `leak-check.json` 配置文件，那么这些配置信息会以 **配置回显** 的形式出现在会话的 JSONL 日志中。脚本会将其单独标记为配置回显，而非真正的信息泄露：

```
📋 **3 possible config echoes** (session contains leak-check config)

• **Discord**: 1 session
...

✅ No credential leaks beyond config echoes
```

配置回显会在每次运行脚本时持续显示，直到相关会话文件被删除。要清除这些回显，请从 `~/.openclaw/agents/main/sessions/` 目录中删除该会话文件：

```bash
rm ~/.openclaw/agents/main/sessions/<session-uuid>.jsonl
```

**提示：** 在 OpenClaw 会话期间请避免读取或引用 `leak-check.json` 文件。如果发生了这种情况，请记录下会话 ID 并将其删除。

### JSON 格式

```json
{
  "leaks": [
    {
      "credential": "Discord Token",
      "session": "abc12345",
      "timestamp": "2026-02-14T18:30:00.000Z",
      "provider": "anthropic"
    }
  ],
  "configEchoes": [
    {
      "credential": "Gateway",
      "session": "b175e53c",
      "timestamp": "2026-02-19T18:00:30.067Z",
      "provider": "minimax-portal",
      "configEcho": true
    }
  ],
  "summary": {
    "filesScanned": 370,
    "credentialsChecked": 7,
    "leaksFound": 2,
    "configEchoesFound": 1
  }
}
```

## 安全性

该脚本仅用于本地环境，并且具有 **只读** 的权限。通过检查 `scripts/leak-check.js` 文件，可以确认以下安全特性：
- **无网络访问** — 不使用 `http`、`https`、`net`、`dgram`、`fetch`、`WebSocket` 或任何网络 API
- **无子进程** — 不使用 `child_process`、`exec`、`spawn` 或 `execSync`
- **无外部依赖** — 完全不依赖任何 npm 包，仅使用 Node.js 的内置模块（`fs`、`path`、`os`）
- **无动态代码执行** — 不使用 `eval()`、`Function()` 或动态的 `require()`/`import()`
- **无文件写入** — 仅使用 `fs.readFileSync`、`fs.existsSync` 和 `fs.readdirSync`；不会创建、修改或删除任何文件
- **无环境变量访问** — 不读取 `process.env`
- **输出仅限控制台（stdout）** — 所有结果都输出到控制台，不会发送到其他地方

### 自我验证

请确认脚本中未使用任何未预期的 API：

```bash
grep -E 'require\(|import |http|fetch|net\.|dgram|child_process|exec|spawn|eval\(|Function\(|\.write|\.unlink|\.rename|process\.env' scripts/leak-check.js
```

**预期输出：** 文件开头仅包含三次内置的 `require()` 调用：

```
const fs = require('fs');
const path = require('path');
const os = require('os');
```