---
name: cost-tracker
description: AI spending monitor — track costs across OpenRouter models with daily, weekly, and monthly reports. Budget limits with alerts, per-model analysis, savings recommendations, and historical tracking via SQLite. Use for controlling AI costs and optimizing model selection.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, OpenRouter API key
metadata: {"openclaw": {"emoji": "\ud83d\udcb0", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 💰 成本追踪器

这是一个专为 OpenRouter 设计的 AI 开支监控工具。它可以追踪每种模型的使用成本，生成每日/每周/每月的报告，设置预算警报，并提供节省成本的建议。

## 使用方法

```bash
# Fetch and store current usage from OpenRouter
python3 {baseDir}/scripts/cost_tracker.py fetch

# Show spending reports
python3 {baseDir}/scripts/cost_tracker.py report --period daily
python3 {baseDir}/scripts/cost_tracker.py report --period weekly
python3 {baseDir}/scripts/cost_tracker.py report --period monthly

# Per-model breakdown
python3 {baseDir}/scripts/cost_tracker.py models

# Set monthly budget + check status
python3 {baseDir}/scripts/cost_tracker.py budget --set 25.00
python3 {baseDir}/scripts/cost_tracker.py budget --check

# Savings recommendations
python3 {baseDir}/scripts/cost_tracker.py savings

# Export data as JSON
python3 {baseDir}/scripts/cost_tracker.py export --format json
python3 {baseDir}/scripts/cost_tracker.py export --format csv
```

## 主要功能

- **实时数据获取**：从 OpenRouter 的 `/api/v1/auth/key` 端点获取实时开支数据
- **模型成本分析**：查看哪些模型导致了最高的成本支出
- **周期报告**：提供每日、每周和每月的开支汇总及趋势分析
- **预算警报**：设置预算限制，并在成本达到 80% 时发出警告
- **节省建议**：推荐能够承担相同工作负载的更便宜的模型
- **历史数据存储**：数据存储在 SQLite 数据库中，便于长期趋势分析
- **数据导出**：支持导出为 JSON 或 CSV 格式，以便导入电子表格

## 数据存储

所有数据均存储在 `{baseDir}/data/cost_tracker.db`（SQLite 数据库）中。

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube 频道](https://youtube.com/@aiwithabidi) | [GitHub 仓库](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)