# 价值追踪技能

该技能用于追踪并量化您的人工智能助手所产生的价值。它可以计算节省的时间，并根据不同类别应用不同的费率来计算投资回报率（ROI），从而证明人工智能助手的实际效果。

## 重要性

人工智能助手确实能节省时间，但具体能节省多少时间呢？该技能能够记录：
- 每项任务所节省的时间
- 根据具体类别计算产生的价值（战略工作与运营工作的价值不同）
- 随时间变化的ROI（提供每日/每周/每月的汇总数据）

## 快速入门

```bash
# Log a task manually
./tracker.py log tech "Set up Toast API integration" -H 2

# Auto-detect category from description
./tracker.py log auto "Researched competitor pricing strategies" -H 1.5

# View summaries
./tracker.py summary today
./tracker.py summary week
./tracker.py summary month

# Generate markdown report
./tracker.py report week > weekly-value-report.md

# Export JSON for dashboards
./tracker.py export --format json
```

## 类别及默认费率

| 类别 | 默认费率 | 适用范围 |
|----------|--------------|---------|
| 战略 | $150/小时 | 规划、决策、高级思考 |
| 研究 | $100/小时 | 市场调研、数据分析、深入研究 |
| 财务 | $100/小时 | 财务分析、报告编制、预测 |
| 技术 | $85/小时 | 集成、自动化、脚本开发 |
| 销售 | $75/小时 | 客户关系管理（CRM）、销售流程管理、外联工作 |
| 营销 | $65/小时 | 内容制作、社交媒体推广、活动策划 |
| 运营 | $50/小时 | 电子邮件处理、日程安排、常规任务 |

请编辑 `config.json` 文件以根据您的实际情况自定义费率。

## 自动检测关键词

当使用 `log auto` 选项时，该技能会根据关键词自动识别任务所属的类别：
- **战略**：计划、策略、决策、路线图、愿景
- **研究**：研究、分析、竞争对手、市场、调查
- **财务**：财务、预算、预测、收入、成本
- **技术**：API、集成、脚本、自动化、代码开发
- **销售**：客户关系管理（CRM）、销售流程、潜在客户、外联工作
- **营销**：内容制作、社交媒体推广、活动策划、新闻通讯
- **运营**：电子邮件处理、日程安排、会议安排、任务分类

## 配置

请编辑 `config.json` 文件以进行相关配置：

```json
{
  "currency": "$",
  "default_rate": 75,
  "rates_by_category": {
    "strategy": 150,
    "research": 100,
    "finance": 100,
    "tech": 85,
    "sales": 75,
    "marketing": 65,
    "ops": 50
  }
}
```

## 数据存储

任务数据存储在技能目录下的 `data.json` 文件中。请定期备份这些数据。

## 与仪表板的集成

使用 `tracker.py export` 命令可以将数据导出为 JSON 格式，以便用于网页仪表板或其他工具。

## 使用建议：
1. **保持一致性**——在完成任务后立即记录相关数据。
2. **使用自动检测功能**——比手动分类更快捷。
3. **每周进行回顾**——积累的价值比您想象的要快。
4. **自定义费率**——确保费率与您的实际每小时成本/价值相匹配。

## 示例输出

```
📊 Value Summary (This Week)
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Hours:  12.5h
Total Value:  $1,087
Avg Rate:     $87/hr

By Category:
  🎯 strategy    2.0h    $300
  🔍 research    3.5h    $350
  ⚙️ tech        4.0h    $340
  🔧 ops         3.0h    $150

Top Tasks:
  • Competitor analysis deep dive (3.5h)
  • Toast API integration (2.0h)
  • Q2 planning session (2.0h)
```

---

*创造价值，追踪价值，证明价值。*