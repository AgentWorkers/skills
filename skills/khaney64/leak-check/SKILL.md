---
name: leak-check
description: 扫描会话日志以查找泄露的凭据。该工具会对比 JSONL 格式的会话文件与已知的凭据模式，然后报告哪些 AI 提供商接收了这些数据。
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["node"]}}}
---
# 漏洞检测

扫描 OpenClaw 会话的 JSONL 文件，以检测是否存在泄露的凭证信息。该工具会报告哪些真实的人工智能提供商（如 Anthropic、OpenAI、Google 等）接收了数据，同时会忽略内部传输过程中的数据回显。

## 快速入门

```bash
# Check for leaked credentials (default: discord format)
node scripts/leak-check.js

# JSON output
node scripts/leak-check.js --format json
```

## 配置

需要检测的凭证信息存储在 `leak-check.json` 文件中：

```json
[
  { "name": "Discord", "search": "abc*xyz" },
  { "name": "Postmark", "search": "k7Qm9x" }
]
```

**重要提示：** 请勿在该文件中存储完整的凭证信息。只需存储足够用于通过“包含”（contains）、“以……开头”（begins-with）或“以……结尾”（ends-with）等条件唯一标识凭证的部分内容即可。

**通配符模式：**
- `abc*` — 以 “abc” 开头
- `*xyz` — 以 “xyz” 结尾
- `abc*xyz` — 以 “abc” 开头且以 “xyz” 结尾
- `abc` （不使用星号） — 包含 “abc” 这个字符串
- `""` （空字符串） — 忽略该凭证

## 选项

- `--format <类型>` — 输出格式：`discord`（默认）或 `json`
- `--config <路径>` — 凭证配置文件的路径（默认为技能目录下的 `leak-check.json` 文件）
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

如果未检测到泄露的凭证信息，输出如下：

```
🔐 **Credential Leak Check**
✅ No leaked credentials found (checked 370 files, 7 credentials)
```

### 配置回显

如果在 OpenClaw 会话期间读取或讨论了 `leak-check.json` 配置文件，那么这些凭证匹配信息会出现在该会话的 JSONL 日志中。扫描工具会将其单独标记为 **配置回显**（config echoes），而非真正的凭证泄露：

```
📋 **3 possible config echoes** (session contains leak-check config)

• **Discord**: 1 session
...

✅ No credential leaks beyond config echoes
```

这些配置回显会在每次运行时持续显示，直到会话文件被删除。要清除这些回显，请从 `~/.openclaw/agents/main/sessions/` 目录中删除相应的会话文件：

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