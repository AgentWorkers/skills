---
name: usage-visualizer
description: OpenClaw 提供了高级的使用统计功能和高保真的可视化报告工具。通过专业的 PPT 风格的报表，您可以追踪令牌消耗情况、模型运行效率以及提示信息的缓存节省情况。
metadata:
  openclaw:
    emoji: "📊"
    os:
      - darwin
      - linux
    requires:
      bins:
        - python3
---
# 使用可视化工具

**使用可视化工具**（Usage Visualizer）是一款专为 OpenClaw 设计的高保真分析工具，它能够将原始会话日志转换为专业且易于使用的可视化报告。该工具更注重 **令牌使用模式** 和 **模型效率**，而非简单的成本追踪。

## ✨ 主要功能

- 📊 **高分辨率可视化报告**：生成包含 30 天 SVG 趋势线和多维图表的水平式 PPT 风格报告。
- ⚡ **以令牌为中心的分析**：深入分析输入/输出令牌，包括 Anthropic 提示的缓存（读/写）性能。
- 📉 **效率指标**：自动计算每百万令牌的成本和缓存节省情况，以帮助您优化模型选择。
- 🔄 **零配置同步**：自动检测 OpenClaw 会话日志，并将其同步到本地的 SQLite 数据库中，实现快速且可重复的查询。
- 🔒 **注重隐私**：会话日志仅在本地处理；外部传输（Webhook）是可选的，并且需要明确配置。
- 🔔 **智能警报**：基于阈值的监控功能，支持每日/每周/每月的使用情况统计，并提供灵活的通知格式。
- 🎨 **美观的控制台输出**：提供简洁的文本摘要，方便快速查看。

## 🚀 快速入门

```bash
# Clone the repository
git clone https://github.com/VintLin/usage-visualizer.git
cd usage-visualizer

# Install dependencies
pip install -r requirements.txt

# Initial full sync of historical logs
python3 scripts/fetch_usage.py --full

# Generate your first visual report (Today)
python3 scripts/generate_report_image.py --today
```

## 📈 使用指南

### 可视化报告
该可视化工具会生成高保真的 PNG 图像，直接保存到您的工作空间中。

```bash
# Today's report card
python3 scripts/generate_report_image.py --today

# Weekly overview
python3 scripts/generate_report_image.py --period week

# Last 30 days trend
python3 scripts/generate_report_image.py --period month
```

### 文本摘要
在控制台中查看简洁的摘要：

```bash
# Current day summary
python3 scripts/report.py --period today

# Detailed JSON output for integrations
python3 scripts/report.py --json
```

### 预算与使用监控
设置限制，以便在使用量激增时收到警报。

```bash
# Alert if daily usage exceeds $10
python3 scripts/alert.py --budget-usd 10 --period today
```

## 🛠 项目结构

```
usage-visualizer/
├── assets/                     # Sample reports and UI assets
├── config/                     # Configuration templates
├── scripts/
│   ├── fetch_usage.py          # Log parser and SQLite sync engine
│   ├── calc_cost.py            # Model pricing and savings logic
│   ├── store.py                # Database interface
│   ├── report.py               # Text/JSON reporting
│   ├── html_report.py          # HTML/SVG template engine
│   ├── generate_report_image.py # PNG renderer (headless browser)
│   └── alert.py                # Monitoring and alert logic
├── SKILL.md                    # Skill definition
└── README.md                   # Full documentation
```

## 🧠 工作原理

1. **数据提取**：定期扫描 `~/.openclaw/agents/*/sessions/*.jsonl` 文件以获取新消息。
2. **数据标准化**：将来自不同提供者的元数据统一到统一的格式中（令牌、缓存命中次数、成本）。
3. **数据持久化**：将标准化后的数据存储在本地 SQLite 数据库中，确保同步操作的可重复性。
4. **数据渲染**：使用本地 HTML 模板生成 SVG 图表，然后通过无头渲染器生成高分辨率的 PNG 图像。

## 📝 故障排除

- **图像渲染失败**：确保已安装 `html2image` 工具以及兼容的浏览器（Chrome/Chromium）。在 Linux 服务器上，确保 `Xvfb` 或无头环境可用。
- **日志缺失**：如果您在自定义目录中运行，请检查 `OPENCLAW_WORKSPACE` 环境变量是否设置正确。
- **隐私注意事项**：请注意，会话日志包含对话历史记录。虽然该工具在本地处理这些日志，但请确保您同意将统计信息（成本/令牌）保存在本地 SQLite 数据库中或通过可选的 Webhook 发送。
- **Python 错误**：确保已安装 Python 3.8 及 `requirements.txt` 中列出的所有依赖包。

## 📄 许可证
MIT