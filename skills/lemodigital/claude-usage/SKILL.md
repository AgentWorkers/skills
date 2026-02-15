---
name: claude-usage
description: 根据 OpenClaw 会话数据计算 Claude Max 的订阅使用情况。显示已消耗的信用额度、每周预算占比、5 小时速率限制窗口以及每次会话的使用情况。
---

# Claude Max 使用量计算器

根据 [she-llac.com/claude-limits](https://she-llac.com/claude-limits) 提供的反向工程信用系统，您可以跟踪自己的 Claude Max 订阅使用情况。

## 使用场景

当用户询问 Claude 的使用情况、剩余信用、订阅消耗量、速率限制，或想知道剩余预算时，可以使用此工具。

## 首次设置

需要用户提供以下信息：
1. **每周重置时间** — 可在 [claude.ai](https://claude.ai) 的“设置” > “使用情况”中查看（例如：“每周二下午 2:00 重置”）
2. **订阅计划**：`pro`（20 美元）、`5x`（100 美元）或 `20x`（200 美元）。默认为 `5x`。

将这些信息保存下来，避免用户重复输入：
```bash
python3 {SKILL_DIR}/scripts/claude-usage.py "2026-02-09 14:00" --plan 5x --save
```

## 命令

```bash
# Weekly overview (uses saved config after first --save)
python3 {SKILL_DIR}/scripts/claude-usage.py

# Override plan or timezone
python3 {SKILL_DIR}/scripts/claude-usage.py --plan 20x --tz "America/New_York"

# Top N sessions only
python3 {SKILL_DIR}/scripts/claude-usage.py --top 5

# Single session detail (substring match on key or id)
python3 {SKILL_DIR}/scripts/claude-usage.py --session "main"
python3 {SKILL_DIR}/scripts/claude-usage.py --session "9aadee"

# JSON output
python3 {SKILL_DIR}/scripts/claude-usage.py --json
```

## 功能展示

### 每周概览
- 使用的信用总额与每周预算对比（附带进度条）
- **5 小时滑动窗口**：当接近每 5 小时的速率限制时发出警告
- 按信用消耗量排序的所有会话
- 模型分类（Opus、Sonnet、Haiku、非 Claude 模型）

### 单个会话详情（使用 `--session` 命令）
- 消耗的信用及占每周预算的百分比
- 占总使用量的百分比（本次会话的花费占比）
- 令牌使用情况（输入/输出/缓存）
- 模型详细信息

## 信用计算公式

```
credits = (input_tokens + cache_write_tokens) × input_rate + output_tokens × output_rate
```

| 模型 | 输入速率 | 输出速率 |
|--------|-----------|-------------|
| Haiku  | 2/15      | 10/15       |
| Sonnet | 6/15      | 30/15       |
| Opus   | 10/15     | 50/15       |

缓存读取是**免费的**。非 Claude 模型（如 Gemini、Codex 等）不消耗 Claude 信用。

## 订阅计划与预算

| 订阅计划 | 每月费用 | 每 5 小时的信用消耗 | 每周信用消耗 |
|------|---------|-----------|-------------|
| Pro  | 20 美元     | 550,000   | 5,000,000   |
| 5x   | 100 美元    | 3,300,000 | 41,666,700  |
| 20x  | 200 美元    | 11,000,000| 83,333,300  |

## 系统要求

- Python 3.9 或更高版本
- 需要 OpenClaw 及相应的 JSONL 会话文件（文件路径通常为 `~/.openclaw/agents/main/sessions/`）