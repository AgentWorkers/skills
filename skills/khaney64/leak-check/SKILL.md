---
name: leak-check
description: 扫描会话日志以查找泄露的凭据。将 JSONL 格式的会话文件与已知的凭据模式进行比对，并报告哪些人工智能（AI）服务接收了这些数据。
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["node"]}}}
---
# 信息泄露检测

该脚本会扫描 OpenClaw 会话的 JSONL 文件，以检测是否存在敏感信息的泄露。它会报告数据实际来自哪个 AI 提供商（如 Anthropic、OpenAI、Google 等），同时会忽略内部传输过程中的数据复制或重复。

## 快速入门

```bash
# Check for leaked credentials (default: discord format)
node scripts/leak-check.js

# JSON output
node scripts/leak-check.js --format json
```

## 配置

需要检测的敏感信息配置文件位于 `leak-check.json` 中。脚本会按以下顺序查找该文件：
1. **技能目录**（`./leak-check.json`）——为了保持与旧版本的兼容性
2. **`~/.openclaw/credentials/leak-check.json`**——推荐的位置（该文件会在通过 ClawHub 更新技能时保留）

由于 ClawHub 会在更新时清空技能目录，因此请将配置文件放在 `~/.openclaw/credentials/` 目录下，以避免数据丢失：

```bash
mkdir -p ~/.openclaw/credentials
cp leak-check.json ~/.openclaw/credentials/leak-check.json
```

您也可以使用 `--config` 参数指定配置文件的路径：

```json
[
  { "name": "Discord", "search": "abc*xyz" },
  { "name": "Postmark", "search": "k7Qm9x" }
]
```

**重要提示：** 请不要在该文件中存储完整的敏感信息。只需存储足够用于唯一识别这些信息的片段即可（例如，使用 `contains`、`begins-with` 或 `ends-with` 等匹配条件）。

**通配符模式：**
- `abc*` — 以 “abc” 开头
- `*xyz` — 以 “xyz” 结尾
- `abc*xyz` — 以 “abc” 开头且以 “xyz” 结尾
- `abc`（不使用通配符） — 包含 “abc” 这个字符串
- `""`（空字符串） — 跳过该敏感信息

## 选项
- `--format <type>` — 输出格式：`discord`（默认）或 `json`
- `--config <path>` — 敏感信息配置文件的路径（默认为 `./leak-check.json`，其次为 `~/.openclaw/credentials/leak-check.json`）
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

### 配置信息重复出现的情况

如果在 OpenClaw 会话期间读取或讨论了 `leak-check.json` 配置文件，那么相关敏感信息匹配记录会出现在该会话的 JSONL 日志中。脚本会将这些记录单独标记为 **配置信息重复出现**（而非真正的信息泄露）：

```
📋 **3 possible config echoes** (session contains leak-check config)

• **Discord**: 1 session
...

✅ No credential leaks beyond config echoes
```

这些重复记录会在每次运行脚本时继续显示，直到对应的会话文件被删除。要清除这些记录，请从 `~/.openclaw/agents/main/sessions/` 目录中删除该会话文件：

```bash
rm ~/.openclaw/agents/main/sessions/<session-uuid>.jsonl
```

**提示：** 在 OpenClaw 会话期间请避免读取或引用 `leak-check.json` 文件。如果发生了这种情况，请记录下会话 ID 并将其删除。

### JSON 格式输出

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