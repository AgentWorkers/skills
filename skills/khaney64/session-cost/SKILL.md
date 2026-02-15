---
name: session-cost
description: 分析 OpenClaw 会话日志，以报告按模型分组的令牌使用情况、成本和性能指标。当用户询问 API 使用情况、令牌使用量、会话成本或需要使用情况摘要时，可以使用此功能。
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["node"]}}}
---

# 会话成本分析

该工具用于分析 OpenClaw 会话日志，统计每个模型的令牌使用情况、成本及性能指标。

**注意：** 目前仅支持 `main` 代理（默认路径：`~/.openclaw/agents/main/sessions/`）。如果未来添加了其他代理，可以通过添加 `--agent` 参数来指定需要分析的代理的会话。

## 快速入门

```bash
# Summary of all sessions (default path: ~/.openclaw/agents/main/sessions/)
node scripts/session-cost.js

# Show all session details
node scripts/session-cost.js --details

# Show details for a specific session
node scripts/session-cost.js --details abc123
```

## 命令选项

- `--path <dir>` — 需要扫描的 `.jsonl` 文件目录（默认路径：`~/.openclaw/agents/main/sessions/`）
- `--offset <time>` — 仅显示过去 N 个时间单位内的会话（例如：`30m`、`2h`、`7d`）
- `--provider <name>` — 按模型提供者进行过滤（`anthropic`、`openai`、`ollama` 等）
- `--details [session-id]` — 显示单个会话的详细信息。可以传入会话 ID 来仅显示该会话的详细信息（文件格式为 `<id>.jsonl`）
- `--table` — 以紧凑的表格格式显示详细信息（需配合 `--details` 使用）
- `--format <type>` — 输出格式：`text`（默认）、`json` 或 `discord`
- `--json` — `--format json` 的简写形式（为了兼容旧版本）
- `--help`, `-h` — 显示帮助信息

## 使用示例

```bash
# Last 24 hours summary
node scripts/session-cost.js --offset 24h

# Last 7 days, JSON output
node scripts/session-cost.js --offset 7d --json

# Discord-friendly format (for bots/chat)
node scripts/session-cost.js --format discord

# Discord format with filters
node scripts/session-cost.js --format discord --offset 24h --provider anthropic

# Filter by provider
node scripts/session-cost.js --provider anthropic

# All sessions in compact table format
node scripts/session-cost.js --details --table

# Custom path with details
node scripts/session-cost.js --path /other/dir --details

# Single session detail
node scripts/session-cost.js --details 9df7a399-8254-411b-a875-e7337df73d29

# Anthropic sessions from last 24h in table format
node scripts/session-cost.js --provider anthropic --offset 24h --details --table
```

## 输出格式

### 文本摘要（默认格式）

```
Found 42 .jsonl files, 42 matched

====================================================================================================
SUMMARY BY MODEL
====================================================================================================

anthropic/claude-sonnet-4-5-20250929
--------------------------------------------------------------------------------
  Sessions: 30
  Tokens:   1,234,567 (input: 900,000, output: 334,567)
  Cache:    read: 500,000 tokens, write: 200,000 tokens
  Cost:     $12.3456
    Input:       $5.4000
    Output:      $5.0185
    Cache read:  $1.5000  (included in total, discounted rate)
    Cache write: $0.4271  (included in total)
```

### 详细信息（使用 `--details`）

以文本形式显示每个会话的详细信息，包括会话 ID、模型名称、持续时间、时间戳、令牌使用情况、缓存操作及成本，并附有模型汇总。

### 表格格式（使用 `--details --table`）

以表格形式显示详细信息，列包括：会话 ID、模型名称、持续时间、令牌使用量（读取/写入）、缓存操作及成本。

```
SESSION DETAILS
=============================================================================================================================
Model                           Duration  Tokens        Cache          Cost        Session
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
anthropic/claude-sonnet-4.5     45 min    128.5K        15.2K / 8.1K   $0.3245     abc123def456
anthropic/claude-opus-4         12 min    45.3K         2.1K / 1.5K    $0.8921     xyz789abc012
```

### JSON 格式（使用 `--format json`）

```json
{
  "models": {
    "anthropic/claude-sonnet-4-5-20250929": {
      "sessions": 30,
      "tokens": { "input": 900000, "output": 334567, "total": 1234567 },
      "cache": { "read": 500000, "write": 200000 },
      "cost": { "total": 12.3456, "input": 5.4, "output": 5.0185, "cacheRead": 1.5, "cacheWrite": 0.4271 }
    }
  },
  "grandTotal": { ... }
}
```

### Discord 格式（使用 `--format discord`）

专为聊天平台（如 Discord、Slack 等）优化，格式简洁，易于阅读（不包含表格）：

```
💰 **Usage Summary**
(last 24h)

**Total Cost:** $12.34
**Total Tokens:** 1.2M
**Sessions:** 42

**By Provider:**
• anthropic: $10.50 (950K tokens)
• openai: $1.84 (250K tokens)

**Top Models:**
• anthropic/claude-sonnet-4.5: $8.20 (800K tokens)
• openai/gpt-4o: $1.84 (250K tokens)
• anthropic/claude-opus-4: $2.30 (150K tokens)
```

## 输出字段

- **Sessions** — 分析的会话文件数量
- **Tokens** — 总令牌数、输入令牌数和输出令牌数
- **Cache** — 缓存操作的令牌数（读取/写入）
- **Cost** — 总成本（按输入令牌数、输出令牌数、缓存读取令牌数和缓存写入令牌数细分）
- **Duration** — 会话持续时间（以分钟为单位，仅限详细信息模式）
- **Timestamps** — 会话的开始和结束时间戳（仅限详细信息模式）