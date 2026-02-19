---
name: openclaw-cost-tracker
description: **跟踪 OpenClaw 的使用成本，并按日期和型号提供详细报告。** 支持生成每日、每周和每月的报告格式，适用于 Discord 及其他消息渠道。
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["jq"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (JSON parser)",
            },
          ],
      },
  }
---

# OpenClaw 成本追踪器

## 概述

该工具可精确追踪 OpenClaw 的使用成本，并提供按日期和模型类型划分的详细报告。它利用 `jq` 工具直接解析 OpenClaw 会话日志中的 JSON 数据，从而提取准确的成本信息。

支持多种报告格式：
- 日报（今日/昨日的成本）
- 周报（当前周的总成本/与上周的对比）
- 月报（当前月的总成本/同比增长）

## 快速入门

```bash
# Today's cost report
bash {baseDir}/scripts/cost_report.sh --today

# Yesterday's cost report
bash {baseDir}/scripts/cost_report.sh --yesterday

# Weekly cost report
bash {baseDir}/scripts/cost_report.sh --week

# Date range report
bash {baseDir}/scripts/cost_report.sh --from 2026-01-01 --to 2026-01-31
```

## 成本计算方法

该脚本直接从 OpenClaw 会话日志文件（`~/.openclaw/agents/*/sessions/*.jsonl`）中提取成本数据：
1. 使用 `jq` 解析 JSON 数据，定位 `message_usage.cost.total` 字段
2. 按日期和模型对成本数据进行汇总
3. 确保每个 API 调用的成本仅被计算一次

## Discord 输出格式

```
💰 OpenClaw Cost Report (2026-02-04)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Today's Total Cost: $XX.XX (🟢 -XX% vs yesterday)

📊 Model Details:
• claude-opus-4-5: $XX.XX (XX%)
• gpt-4o: $X.XX (X%)
• ...

📈 Weekly Total: $XXX.XX
```

## 安装要求

- `jq`：JSON 解析工具（使用 `brew install jq` 或 `apt install jq` 安装）
- 具有访问 OpenClaw 日志文件的权限