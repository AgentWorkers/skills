---
name: usage-visualizer
description: OpenClaw 提供高级使用统计功能和高保真度的可视化报告。当用户请求使用报告（usage report/usage stats/用量汇报/用量统计）时，系统会首先同步最新的日志数据，然后再生成报告。
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

**使用可视化工具**是一款专为OpenClaw设计的高保真分析引擎，它能够将原始的会话日志转换为专业且可操作的可视化报告。该工具更注重**令牌使用模式**和**模型效率**，而非简单的成本追踪。

## ✨ 主要功能

- 📊 **高分辨率可视化报告**：生成包含30天SVG趋势线和多维图表的水平PPT风格卡片。
- ⚡ **以令牌为中心的分析**：深入分析输入/输出令牌，包括Anthropic提示的缓存（读/写）性能。
- 📉 **效率指标**：自动计算每百万令牌的成本和缓存节省情况，以帮助您优化模型选择。
- 🔄 **零配置同步**：自动检测OpenClaw会话日志，并将其同步到本地SQLite数据库中，实现快速、幂等的查询。
- 🔔 **智能警报**：基于阈值的监控功能，支持每日/每周/每月的使用情况，并提供灵活的通知格式。
- 🎨 **美观的控制台输出**：提供简洁且包含表情符号的文本摘要，便于快速查看。

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

### 可视化报告（推荐的一步流程）
首先需要同步日志，然后生成报告图像。

```bash
# Today image report (sync + render)
python3 scripts/run_usage_report.py --mode image --period today

# Weekly image report (sync + render)
python3 scripts/run_usage_report.py --mode image --period week

# Monthly image report (sync + render)
python3 scripts/run_usage_report.py --mode image --period month
```

**手动分割流程（旧版本）**：

```bash
python3 scripts/fetch_usage.py
python3 scripts/generate_report_image.py --today
```

### 文本摘要
在控制台中查看简洁的摘要：

```bash
# Current day summary (sync + text)
python3 scripts/run_usage_report.py --mode text --period today

# Direct report (without auto sync)
python3 scripts/report.py --period today --text

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

1. **数据提取**：定期扫描`~/.openclaw/agents/*/sessions/*.jsonl`文件以获取新消息。
2. **数据标准化**：将来自不同提供者的元数据统一映射到统一的模式中（令牌、缓存命中次数、成本）。
3. **数据持久化**：将标准化的数据存储在本地SQLite数据库中，确保同步操作的幂等性。
4. **数据渲染**：使用本地HTML模板生成SVG图表，并通过无头渲染器捕获高分辨率的PNG图像。

## 📝 故障排除

- **图像渲染失败**：确保已安装`html2image`工具和兼容的浏览器（Chrome/Chromium）。在Linux服务器上，确保`Xvfb`或无头环境可用。
- **日志丢失**：如果您在自定义目录中运行，请检查`OPENCLAW_WORKSPACE`环境变量是否设置正确。
- **Python错误**：确保已安装Python 3.8及以上版本以及`requirements.txt`中列出的所有依赖包。

## 📄 许可证
MIT