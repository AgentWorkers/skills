---
name: AI CFO
description: "全功能人工智能首席财务官（Full AI Chief Financial Officer）：将 Mercury Banking 与 Stripe 连接起来，实现实时商业智能分析。支持每日现金状况查询、自动化的损益表（P&L）生成、收入追踪、费用分类、现金流预测、烧钱速度（burn rate）警报以及每周财务报告的生成。"
homepage: https://github.com/aiwithabidi/ai-cfo-skill
license: MIT
compatibility: ">=0.9.0"
metadata: {"emoji":"📊","requires":["MERCURY_API_TOKEN","STRIPE_API_KEY","OPENROUTER_API_KEY"],"primaryEnv":"MERCURY_API_TOKEN","homepage":"https://agxntsix.ai"}
---
# 📊 AI CFO

**Agent6ix LLC 的全功能 AI 首席财务官**

该工具将 Mercury Banking 与 Stripe 连接起来，实现实时商业智能分析。支持每日现金状况查看、自动利润与损失（P&L）计算、收入追踪、费用分类、现金流预测、燃烧率（burn rate）警报以及每周财务报告的生成。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `dashboard` | 全面财务仪表盘——显示余额、月收入（MRR）、燃烧率及项目持续时间（runway） |
| `transactions` | 带有 AI 分类的最近交易记录 |
| `pnl` | 任意日期范围的利润与损失（P&L）报表 |
| `cashflow` | 30/60/90 天的现金流分析及预测 |
| `revenue` | Stripe 收入明细——包括月收入（MRR）、新客户与重复客户收入 |
| `expenses` | 分类后的费用记录，附带趋势分析和异常检测功能 |
| `report` | 每周/每月的高管财务报告 |
| `budget` | 按类别设置和追踪预算 |
| `runway` | 计算燃烧率和项目持续时间（runway） |
| `invoice` | 未支付的 Stripe 发票及账龄信息 |

## 环境变量

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `MERCURY_API_TOKEN` | 是 | Mercury Banking 的 API 令牌（仅限读取） |
| `STRIPE_API_KEY` | 是 | Stripe 的秘密密钥（仅限读取） |
| `OPENROUTER_API_KEY` | 是 | 用于 AI 交易分类 |

## 使用方法

```bash
python3 scripts/ai_cfo.py dashboard
python3 scripts/ai_cfo.py transactions --days 30
python3 scripts/ai_cfo.py pnl --start 2026-01-01 --end 2026-01-31
python3 scripts/ai_cfo.py cashflow
python3 scripts/ai_cfo.py revenue
python3 scripts/ai_cfo.py expenses --days 30
python3 scripts/ai_cfo.py report --period weekly
python3 scripts/ai_cfo.py budget --set Marketing 5000
python3 scripts/ai_cfo.py runway
python3 scripts/ai_cfo.py invoice
```

## 日常自动化流程

```bash
# Add to cron for daily 8 AM brief
python3 scripts/cfo_cron.py
```

## 数据存储

所有数据存储在 `.data/sqlite/cfo.db` 文件中：
- 分类后的交易记录 |
- 预算分配信息 |
- 每日数据快照 |
- 每月利润与损失（P&L）快照

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **您的企业需要 AI CFO 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)