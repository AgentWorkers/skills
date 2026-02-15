---
name: openclaw-cost-guard
description: 从 session JSONL 日志中跟踪 OpenClaw/Clawdbot 的令牌使用情况与成本消耗（优先使用实际发生的成本数据），生成每日/每周的汇总报告以及成本最高的会话记录，并执行预算检查（在超出预算时输出相应的退出代码）。该功能可用于监控支出情况、通过 cron 任务或警报机制来执行预算控制，同时应用节省令牌的策略以降低输出和工具调用的成本。
---

# OpenClaw 成本监控工具

当您需要以下功能时，请使用此工具：
- **精确的成本报告**（每日/每周/终身）
- **使用量最高的会话记录**
- **防止不必要的代币消耗**（除非用户主动要求，否则不会更改配置设置）

## 1) 数据来源（非常重要）

建议使用 **session JSONL** 日志文件（其中包含每次调用的使用情况以及实际产生的费用）：
- OpenClaw：`~/.openclaw/agents/*/sessions/*.jsonl`
- Legacy/compat：`~/.clawdbot/agents/*/sessions/*.jsonl`

**请勿** 仅根据 “当前上下文窗口” 中的代币信息来估算成本。

## 2) 快速命令

### 过去 7 天的每日成本
```bash
python3 {baseDir}/scripts/extract_cost.py --last-days 7
```

### 今日/昨日的成本
```bash
python3 {baseDir}/scripts/extract_cost.py --today
python3 {baseDir}/scripts/extract_cost.py --yesterday
```

### 使用量最高的会话记录
```bash
python3 {baseDir}/scripts/extract_cost.py --top-sessions 10
```

### 用于数据仪表盘的 JSON 输出格式
```bash
python3 {baseDir}/scripts/extract_cost.py --last-days 30 --json
```

## 3) 如果成本数据缺失（备用估算方法）

某些服务提供商可能未提供 `usage.cost` 数据。在这种情况下，您可以提供每百万代币的费用信息：
```bash
export PRICE_INPUT=1.75
export PRICE_OUTPUT=14
export PRICE_CACHE_READ=0.175
export PRICE_CACHE_WRITE=0
python3 {baseDir}/scripts/extract_cost.py --last-days 7
```

## 4) 预算警报

该工具可作为预算监控工具使用：
```bash
python3 {baseDir}/scripts/extract_cost.py --today --budget-usd 5
```

- 如果超出预算，系统会输出 **警报** 并以代码 **2** 退出（默认行为）。
- 对于非异常检查情况：
```bash
python3 {baseDir}/scripts/extract_cost.py --today --budget-usd 5 --budget-mode warn
```

### 将其集成到 Cron 任务中（推荐）

每天（或每小时）运行该工具，如果退出代码为 **2**，则自动向您发送 Telegram 消息。
（具体实现方式取决于您的 OpenClaw 配置；请勿在脚本中嵌入敏感信息。）

## 5) 节约代币的使用策略（指导 AI 行为）

当用户要求 “尽可能少地使用代币” 时，请遵循以下原则：
- **默认回复格式**：1–6 行文本，使用项目符号而非段落
- **最多只询问一个问题**（仅在确实需要更多信息时）
- **逐步披露信息**：仅在被请求时提供详细内容
- **工具调用**：批量执行，避免重复发送状态更新或浏览器请求
- **禁止将日志内容直接发送到聊天频道**：仅提供摘要并指向日志文件路径
- **严格限制**：每个任务最多进行 3 次网络请求（如搜索/数据获取）

用于自我约束的提示语：
> “请在 6 行以内回答问题。如需更多信息，请先获得许可。”