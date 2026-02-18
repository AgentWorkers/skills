---
name: leak-check
description: 扫描会话日志以查找泄露的凭据。该工具会对比 JSONL 格式的会话文件与已知的凭据模式，并报告哪些 AI 提供商接收了这些数据。
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["node"]}}}
---
# 漏洞检测

扫描 OpenClaw 会话 JSONL 文件，以检测是否存在泄露的凭据。该工具会报告数据实际来自哪个 AI 提供商（如 Anthropic、OpenAI、Google 等），同时会忽略内部传输过程中的数据。

## 快速入门

```bash
# Check for leaked credentials (default: discord format)
node scripts/leak-check.js

# JSON output
node scripts/leak-check.js --format json
```

## 配置

需要检测的凭据信息存储在 `leak-check.json` 文件中：

```json
[
  { "name": "Discord", "search": "abc*xyz" },
  { "name": "Postmark", "search": "k7Qm9x" }
]
```

**重要提示：** 请勿在该文件中存储完整的凭据信息。只需存储足够用于通过包含（contains）、以……开头（begins-with）或以……结尾（ends-with）等操作来唯一识别该凭据的部分内容。

**通配符模式：**
- `abc*` — 以 “abc” 开头
- `*xyz` — 以 “xyz” 结尾
- `abc*xyz` — 以 “abc” 开头且以 “xyz” 结尾
- `abc` （不使用通配符） — 包含 “abc” 这个字符串
- `""` （空字符串） — 忽略该凭据

## 选项
- `--format <type>` — 输出格式：`discord`（默认）或 `json`
- `--config <path>` — 凭据配置文件的路径（默认为技能根目录下的 `leak-check.json`）
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

如果未检测到泄露的凭据，输出如下：

```
🔐 **Credential Leak Check**
✅ No leaked credentials found (checked 370 files, 7 credentials)
```

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
  "summary": {
    "filesScanned": 370,
    "credentialsChecked": 7,
    "leaksFound": 2
  }
}
```