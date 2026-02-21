---
name: leak-check
description: **扫描会话日志以查找泄露的凭据**：该功能会检查 JSONL 格式的会话文件，对比已知的凭据模式，并报告哪些 AI 提供商接收了这些数据。
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["node"]}}}
---
# 信息泄露检测

该脚本会扫描 OpenClaw 会话的 JSONL 文件，以检测是否存在敏感信息的泄露。它会报告哪些真实的人工智能服务提供商（如 Anthropic、OpenAI、Google 等）接收了数据，同时会忽略内部传输过程中的数据副本。

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
2. **`~/clawd/leak-check.json`**——推荐的位置（该文件在通过 ClawHub 更新技能时仍会保留）

由于 ClawHub 会在更新技能时清除技能目录中的文件，请将配置文件放置在 `~/clawd/` 目录下，以避免数据丢失：

```bash
mkdir -p ~/clawd
cp leak-check.json ~/clawd/leak-check.json
```

您也可以使用 `--config` 参数指定配置文件的路径。

```json
[
  { "name": "Discord", "search": "abc*xyz" },
  { "name": "Postmark", "search": "k7Qm9x" }
]
```

**重要提示：** 请勿在该文件中存储完整的敏感信息。只需存储足够用于唯一识别这些信息的片段即可（例如，通过包含、以某字符开头或以某字符结尾的方式进行匹配）。

**通配符模式：**
- `abc*` — 以 “abc” 开头
- `*xyz` — 以 “xyz” 结尾
- `abc*xyz` — 以 “abc” 开头且以 “xyz” 结尾
- `abc`（不使用通配符） — 包含 “abc” 这个字符串
- `""`（空字符串） — 忽略该敏感信息

## 选项

- `--format <类型>` — 输出格式：`discord`（默认）或 `json`
- `--config <路径>` — 敏感信息配置文件的路径（默认为 `./leak-check.json`，否则为 `~/clawd/leak-check.json`）
- `--help`, `-h` — 显示帮助信息

## 输出结果

### Discord（默认格式）

```
🔐 **Credential Leak Check**

⚠️ **2 leaked credentials found**

**Discord Token**
• Session: `abc12345` | 2026-02-14 18:30 UTC | Provider: anthropic

**Postmark**
• Session: `def67890` | 2026-02-10 09:15 UTC | Provider: anthropic
```

如果未检测到泄露信息：

```
🔐 **Credential Leak Check**
✅ No leaked credentials found (checked 370 files, 7 credentials)
```

### 配置信息副本

如果在 OpenClaw 会话期间读取或讨论了 `leak-check.json` 文件中的配置信息，这些配置信息将会出现在该会话的 JSONL 日志中。脚本会将其单独标记为 **配置信息副本**（而非真正的信息泄露），并予以报告：

```
📋 **3 possible config echoes** (session contains leak-check config)

• **Discord**: 1 session
...

✅ No credential leaks beyond config echoes
```

只要会话文件存在，这些配置信息副本就会持续出现在输出结果中。要清除这些副本，请从 `~/.openclaw/agents/main/sessions/` 目录中删除相应的会话文件：

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