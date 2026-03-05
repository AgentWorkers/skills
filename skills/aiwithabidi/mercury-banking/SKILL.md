---
name: mercury-banking
description: Mercury banking API integration — accounts, balances, transactions, financial summaries, AI transaction categorization, and cash flow analysis. The only Mercury banking skill on ClawHub. Use for business banking, financial tracking, and expense management.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, Mercury banking account
metadata: {"openclaw": {"emoji": "\ud83c\udfe6", "requires": {"env": ["MERCURY_API_KEY"]}, "primaryEnv": "MERCURY_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 🏦 Mercury Banking

Mercury Banking 提供了与 OpenClaw 代理集成的 API，支持账户管理、交易处理、现金流分析以及基于人工智能的财务洞察功能。

## 必需条件

| 变量        | 是否必需 | 说明                                      |
|------------|---------|-----------------------------------------|
| `MERCURY_API_KEY` | ✅      | Mercury API 令牌（[获取方式](https://app.mercury.com/settings/tokens)       |
| `OPENROUTER_API_KEY` | 可选    | 用于人工智能分类和财务摘要功能                         |

## 快速入门

```bash
# List all accounts and balances
python3 {baseDir}/scripts/mercury_api.py accounts

# Recent transactions
python3 {baseDir}/scripts/mercury_api.py transactions <account_id>

# Transactions with date filter
python3 {baseDir}/scripts/mercury_api.py transactions <account_id> --start 2026-01-01 --end 2026-01-31

# Search transactions
python3 {baseDir}/scripts/mercury_api.py transactions <account_id> --search "Stripe"

# Cash flow analysis
python3 {baseDir}/scripts/mercury_api.py cashflow <account_id> --days 30

# AI categorize transactions
python3 {baseDir}/scripts/mercury_api.py categorize <account_id> --days 30

# Financial summary
python3 {baseDir}/scripts/mercury_api.py summary <account_id> --period weekly
```

## 命令

### `accounts`
列出所有 Mercury 账户的信息，包括当前余额、账户类型和状态。

### `transactions <account_id>`
查询指定账户的交易记录，支持以下筛选条件：
- `--start YYYY-MM-DD` / `--end YYYY-MM-DD` — 时间范围
- `--search "term"` — 根据交易对手或描述进行筛选
- `--limit N` — 最大返回结果数量（默认 50 条）
- `--status pending|sent|cancelled|failed` — 根据交易状态进行筛选

### `cashflow <account_id>`
分析指定账户在指定时间段内的现金流：
- `--days N` — 回顾时间段（默认 30 天）
- 显示总流入额、总流出额、净现金流、日均值以及资金消耗率

### `categorize <account_id>`
利用人工智能对交易进行分类（需要 `OPENROUTER_API_KEY`）：
- `--days N` — 回顾时间段（默认 30 天）
- 将交易分为不同类别（如工资、SaaS 服务费用、收入等）
- 输出各类别的总额及占比

### `summary <account_id>`
生成财务摘要：
- `--period weekly|monthly` — 摘要周期
- 包括主要支出项目、收入来源、现金状况及趋势分析

## Mercury API 说明

- **基础 URL：** `https://api.mercury.com/api/v1`
- **认证方式：** 在请求头中添加 Bearer 令牌
- **请求限制：** 请注意 API 的请求次数限制；脚本会自动处理分页请求
- **沙箱环境：** Mercury 提供沙箱环境供测试使用

## 开发者信息
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
本功能属于 OpenClaw 代理的 **AgxntSix Skill Suite** 套件的一部分。

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)