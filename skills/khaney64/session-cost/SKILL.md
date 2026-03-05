---
name: session-cost
description: 分析 OpenClaw 会话日志，以按代理（agent）和模型（model）分组报告令牌使用情况、成本以及性能指标。当用户询问 API 使用情况、令牌使用量、会话成本或需要使用情况汇总时，可以使用此功能。
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["node"]}}}
---
# 会话成本分析

该工具用于分析 OpenClaw 会话日志，统计每个代理和模型的令牌使用情况、成本及性能指标。

默认情况下，会扫描 `~/.openclaw/agents/` 目录下的所有代理。每个代理的会话数据存储在 `~/.openclaw/agents/<name>/sessions/` 目录中。

## 快速入门

```bash
# Summary across all agents
node scripts/session-cost.js

# Show all session details
node scripts/session-cost.js --details

# Show details for a specific session (searches across all agents)
node scripts/session-cost.js --details abc123
```

## 命令选项

- `--path <dir>` — 指定要扫描的 `.jsonl` 文件所在的目录（会覆盖自动代理检测功能）
- `--agent <name>` — 按代理名称进行筛选（例如：`main`、`codegen`）
- `--offset <time>` — 仅显示过去 N 个时间单位内的会话数据（例如：`30m`、`2h`、`7d`）
- `--provider <name>` — 按模型提供商进行筛选（例如：`anthropic`、`openai`、`ollama` 等）
- `--details [session-id]` — 显示单个会话的详细信息。可以指定会话 ID 来查看该会话的详细信息（在所有代理中搜索对应的 `.jsonl` 文件）
- `--table` — 以紧凑的表格格式显示详细信息（需结合 `--details` 使用）
- `--format <type>` — 输出格式：`text`（默认）、`json` 或 `discord`
- `--json` — 是 `--format json` 的简写形式（为了向后兼容）
- `--help`, `-h` — 显示帮助信息

## 使用示例

```bash
# Last 24 hours summary
node scripts/session-cost.js --offset 24h

# Only the main agent
node scripts/session-cost.js --agent main

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

# Custom path with details (overrides agent discovery, scans exact directory)
node scripts/session-cost.js --path /other/dir --details

# Single session detail (found automatically across agents)
node scripts/session-cost.js --details 9df7a399-8254-411b-a875-e7337df73d29

# Anthropic sessions from last 24h in table format
node scripts/session-cost.js --provider anthropic --offset 24h --details --table
```

## 输出格式

### 文本格式（默认）

结果首先按代理分组，然后在每个代理内部按模型分组显示。最后会显示每个代理的子总计以及所有代理的总计。

```
Found 52 .jsonl files across 2 agents, 52 matched

====================================================================================================
SUMMARY BY AGENT
====================================================================================================

Agent: main

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

  anthropic/claude-opus-4-6
  --------------------------------------------------------------------------------
    Sessions: 5
    Tokens:   250,000 (input: 180,000, output: 70,000)
    ...

Agent: codegen

  anthropic/claude-sonnet-4-5-20250929
  --------------------------------------------------------------------------------
    Sessions: 17
    ...

====================================================================================================
GRAND TOTAL
====================================================================================================
  main                 — 35 sessions, $15.8200
  codegen              — 17 sessions, $8.5600

All agents (2)
--------------------------------------------------------------------------------
  Sessions: 52
  Tokens:   ...
  Cost:     $24.3800
  ...
```

当系统中只有一个代理时，总计部分会显示为“所有模型（N）”。

### 文本详细信息（`--details`）

会显示每个会话的详细信息（包括会话 ID、代理名称、模型名称、会话时长、时间戳、令牌使用情况、缓存操作及成本），随后会显示该代理/模型的汇总信息。

### 表格格式（`--details --table`）

以表格形式显示详细信息。当系统中有多个代理时，会包含一个“代理”列。

### JSON 格式（`--format json`）

结果按代理进行嵌套显示。每个代理的条目中包含其模型相关的汇总信息以及代理级别的总计数据。最顶层的 `grandTotal` 列显示所有代理的总计。

### Discord 格式（`--format discord`）

专为聊天平台（如 Discord、Slack 等）优化：格式简洁，易于阅读，不使用表格。

```
💰 **Usage Summary**
(last 24h)

**Total Cost:** $24.38
**Total Tokens:** 2.1M
**Sessions:** 52

**By Agent:**
• main: $15.82 (35 sessions)
• codegen: $8.56 (17 sessions)

**By Provider:**
• anthropic: $22.50 (1.9M tokens)
• openai: $1.88 (200K tokens)

**Top Models:**
• anthropic/claude-sonnet-4.5: $18.20 (1.5M tokens)
• anthropic/claude-opus-4: $4.30 (400K tokens)
• openai/gpt-4o: $1.88 (200K tokens)
```

只有当系统中存在多个代理时，才会显示“按代理分组”的部分。

## 输出字段

- **Agent** — 代理名称（从 `~/.openclaw/agents/` 目录下的代理文件夹名推断得出）
- **Sessions** — 分析的会话文件数量
- **Tokens** — 总令牌数、输入令牌数和输出令牌数
- **Cache** — 缓存操作的读写令牌数
- **Cost** — 总成本（分为输入成本、输出成本、缓存读操作成本和缓存写操作成本）
- **Duration** — 会话时长（仅限详细信息模式下显示）
- **Timestamps** — 会话的开始和结束时间戳（仅限详细信息模式下显示）

## 注意事项

- 如果指定了 `--path` 参数，系统将仅扫描该目录下的代理数据。代理名称会从路径中自动推断（例如：`.../agents/main/sessions` → “main”）。
- 可以同时使用 `--agent` 和 `--provider` 参数进行联合筛选（例如：`--agent main --provider anthropic`）。
- 使用 `--details <id>` 可以在所有代理中查找指定 ID 的会话文件。