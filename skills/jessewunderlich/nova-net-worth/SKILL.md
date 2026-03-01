---
name: nova-net-worth
description: 查询您的 Nova Net Worth 财务数据——包括净资产、账户信息、持仓情况、财务目标、支出记录、交易明细以及 AI 分析结果和财务健康状况。当用户询问有关财务、资金、净资产、账户余额、投资组合、股票、财务目标、消费习惯、预算、储蓄、投资、债务或财务健康状况的问题时，可以使用此功能。该功能需要 NOVA_API_KEY 环境变量（请从 app.novanetworth.com 的“设置”→“集成”中获取 API 密钥）。
metadata:
  openclaw:
    requires:
      env:
        - NOVA_API_KEY
---
# Nova 财产价值 API 功能

通过 Agent API v1 查询您的完整财务信息。

## 设置

使用您的 Nova API 密钥设置 `NOVA_API_KEY` 环境变量：
```bash
export NOVA_API_KEY=nova_your_key_here
```

您可以在以下地址生成 API 密钥：**app.novanetworth.com → 设置 → 集成**
需要 SuperNova（每月 $19.99）或 Galaxy（企业级）订阅才能使用此功能。

## 快速入门

对于任何关于“我的财务状况如何？”或每日财务概览的问题，可以使用以下复合端点：
```bash
node scripts/nova-api.js briefing --pretty
```

## 可用命令

运行 `scripts/nova-api.js` 并配合相应的子命令来执行操作：
```bash
# Full financial briefing (RECOMMENDED — one call gets everything)
node scripts/nova-api.js briefing
node scripts/nova-api.js briefing --pretty    # Human-readable format

# Net worth summary
node scripts/nova-api.js summary

# All accounts with balances, grouped by type
node scripts/nova-api.js accounts

# Recent transactions with filtering
node scripts/nova-api.js transactions
node scripts/nova-api.js transactions --days 7 --limit 20
node scripts/nova-api.js transactions --category FOOD_AND_DRINK
node scripts/nova-api.js transactions --account acct_123
node scripts/nova-api.js transactions --since 2026-02-20T00:00:00Z  # Delta polling

# Financial goals with progress
node scripts/nova-api.js goals

# Monthly spending by category
node scripts/nova-api.js spending
node scripts/nova-api.js spending --months 3

# AI-generated financial insights
node scripts/nova-api.js insights

# Net worth trend over time
node scripts/nova-api.js history
node scripts/nova-api.js history --days 90

# Financial health score breakdown
node scripts/nova-api.js health

# Investment holdings and positions
node scripts/nova-api.js holdings                    # All holdings
node scripts/nova-api.js holdings --pretty           # Human-readable with gain/loss
node scripts/nova-api.js holdings --account acct_123 # Filter by account
node scripts/nova-api.js holdings --summary          # Aggregate by ticker across accounts
```

所有命令都支持 `--pretty` 选项（生成易于阅读的格式）或 `--json` 选项（默认为原始 JSON 格式）。

## 选择合适的端点

| 用户问题 | 命令 | 原因 |
|---|---|---|
| “我的财务状况如何？” / “财务更新” | `briefing` | 一次性获取所有财务信息 |
| “我的净资产是多少？” | `summary` | 快速获取净资产概览 |
| “显示我的账户信息” / “我的储蓄金额是多少？” | `accounts` | 查看所有账户的余额 |
| “我在食品上花了多少钱？” / “最近的消费记录” | `transactions --category FOOD_AND_DRINK` | 过滤后的消费记录 |
| “每月支出明细” | `spending` | 按类别划分的支出情况 |
| “我是否按计划实现目标？” | `goals` | 目标进度跟踪 |
| “有什么财务建议吗？” | `insights` | 人工智能提供的建议 |
| “今年的净资产趋势” | `history --days 365` | 过去 365 天的财务数据 |
| “我的财务健康状况如何？” | `health` | 财务健康评分及建议 |
| “我持有哪些股票？” / “显示我的投资组合” | `holdings --pretty` | 显示股票持仓及盈亏情况 |
| “按股票代码汇总的总投资额” | `holdings --summary` | 跨账户汇总的投资额 |

## 响应格式

所有响应格式如下：`{ success: true, data: {...}, meta: { requestId, timestamp } }`

货币价值以 **分**（整数）为单位，并包含 `currency` 字段。显示时请将数值除以 100。
示例：`45840017` 表示 `$458,400.17`。

## 交易类别（Plaid）

常用的过滤类别：`FOOD_AND_DRINK`（食品和饮料）、`RENT_AND_UTILITIES`（租金和公用事业）、`TRANSPORTATION`（交通）、`GENERAL_MERCHANDISE`（日常用品）、`TRANSFER_OUT`（支出）、`TRANSFER_IN`（收入）、`LOAN_PAYMENTS`（贷款还款）、`ENTERTAINMENT`（娱乐）、`PERSONAL_CARE`（个人护理）、`MEDICAL`（医疗）、`TRAVEL`（旅行）、`INCOME`（收入）、`UNCATEGORIZED`（未分类）。

## 请求限制

- SuperNova：每小时 100 次请求
- Galaxy：每小时 1,000 次请求
- 请求头中的 `X-RateLimit-Remaining` 字段用于显示剩余的请求次数

## Delta 轮询

为了高效监控财务数据，可以使用 `--since` 选项并指定上次请求的时间戳：
```bash
node scripts/nova-api.js transactions --since 2026-02-25T12:00:00Z
```
这种方式仅返回自上次请求以来的新交易记录，从而减少数据传输量。

## 环境配置

- `NOVA_API_KEY`（必需）——您的 Nova API 密钥，以 `nova_` 开头。可在 app.novanetworth.com → 设置 → 集成 中生成。
- `NOVA_API_URL`（可选）——API 基本地址，默认为 `https://api.novanetworth.com`

## API 文档

- OpenAPI 规范：https://api.novanetworth.com/api-docs/openapi.yaml
- 交互式文档：https://novanetworth.com/api-docs
- 人工智能插件：https://novanetworth.com/.well-known/ai-plugin.json