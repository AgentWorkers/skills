---
name: gate-exchange-affiliate
version: "2026.3.13"
updated: "2026-03-13"
description: "**门币交易所（Gate Exchange）联盟计划数据查询与管理技能**  
当用户询问其联盟合作伙伴的佣金、交易量、净费用、客户数量、交易用户信息，或希望申请加入联盟计划时，可使用此技能。该技能支持查询最近180天的数据（API每次请求仅支持查询30天的数据，如需查询更长时间的数据，需由代理自行分批次处理）。  
**重要提示：**  
- API中的`user_id`参数指的是“交易者”（trader），而非“佣金接收者”（commission receiver）；除非另有明确说明，否则请勿使用该参数。  
- API返回的汇总数据需通过自定义脚本进行计算，不能简单地进行求和操作。  
**关键时间限制：**  
所有查询时间均基于用户系统的当前日期（UTC+8时区）进行计算。  
- 对于相对时间描述（如“过去7天”、“过去30天”、“本周”、“上个月”），需先从当前日期减去相应天数，然后将开始日期和结束日期分别转换为UTC+8时区的00:00:00和23:59:59格式，再转换为Unix时间戳。  
- 绝不允许使用未来的时间戳作为查询条件；如需时间戳，请通过系统函数获取，切勿手动生成。  
- `to`参数的值必须始终小于或等于当前的Unix时间戳。  
**常用查询短语：**  
- “我的联盟数据”（My Affiliate Data）  
- “本周佣金”（Commission This Week）  
- “合作伙伴收益”（Partner Earnings）  
- “团队绩效”（Team Performance）  
- “客户交易量”（Customer Trading Volume）  
- “返利收入”（Rebate Income）  
- “申请加入联盟计划”（Apply for Affiliate Program）"
---
# 门交换联盟计划助理

负责查询和管理门交换联盟/合作伙伴计划的相关数据，包括佣金追踪、团队绩效分析以及申请指导。

## 通用规则

在继续操作之前，请阅读并遵守共享的运行时规则：
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

## 重要通知

- **角色**：此技能仅使用合作伙伴 API。用户查询中的“联盟成员”一词指的是合作伙伴角色。
- **时间限制**：每个 API 请求最多支持 30 天的数据查询。对于超过 30 天（最多 180 天）的查询，代理需要将其拆分为多个 30 天的时段。
- **身份验证**：需要带有合作伙伴权限的 `X-Gate-User-Id` 请求头。
- **关键提示 - user_id 参数**：在 `commission_history` 和 `transaction_history` API 中，`user_id` 参数用于筛选“交易者/交易用户”，而非“佣金接收者”。仅在明确查询特定交易者的贡献时使用此参数。对于一般的佣金查询，请勿使用 `user_id` 参数。
- **数据聚合**：在从 API 响应列表中计算总数时，应根据业务规则使用自定义聚合逻辑。切勿简单地对所有数值求和，因为这可能会由于数据结构和业务逻辑的原因导致错误结果。
- **⚠️ 关键提示 - 时间限制**：所有查询时间均基于用户系统的当前日期（UTC+8 时区）进行计算。对于“过去 7 天”、“过去 30 天”、“本周”等相对时间描述，通过从当前日期减去请求的天数来计算开始日期，然后将开始日期和结束日期分别转换为 UTC+8 时区的 00:00:00 和 23:59:59，再将其转换为 Unix 时间戳。**切勿使用未来的时间戳作为查询条件**。`to` 参数必须始终小于或等于当前时间戳。如果用户指定了未来的日期，请拒绝查询并说明只能查询历史数据。

## 可用的 API（仅限合作伙伴）

| API 端点 | 描述 | 时间限制 |
|--------------|-------------|------------|
| `GET /rebate/partner/transaction_history` | 获取被推荐用户的交易记录 | 每个请求最多 30 天 |
| `GET /rebate/partner/commission_history` | 获取被推荐用户的佣金记录 | 每个请求最多 30 天 |
| `GET /rebate/partner/sub_list` | 获取下属列表（用于统计客户数量） | 无时间参数 |

**注意**：代理 API（`/rebate/agency/*`）已弃用，不在此技能中使用。

## ⚠️ 关键 API 使用警告

### user_id 参数说明
- **切勿在一般佣金查询中使用 `user_id` 参数**
- 在 `commission_history` 和 `transaction_history` API 中，`user_id` 参数用于筛选**交易者/交易用户**，而非佣金接收者。
- 仅在明确查询特定交易者的贡献时使用 `user_id` 参数（例如：“UID 123456 的交易量”）。
- 对于“我的佣金”、“我的收益”等查询，请**勿使用 user_id 参数**。

### 数据聚合规则
- **切勿简单地对 API 响应列表中的所有数值求和**
- 使用自定义聚合逻辑，考虑以下因素：
  - 业务规则和数据关系
  - 资产类型分组
  - 适当的过滤和去重
  - 时间段边界
- 由于数据结构的复杂性，简单求和可能会导致错误结果。

## 核心指标

1. **佣金金额**：来自 `commission_history` 的总佣金收益
2. **交易量**：来自 `transaction_history` 的总交易金额
3. **净费用**：来自 `transaction_history` 的总费用
4. **客户数量**：来自 `sub_list` 的下属总数
5. **交易用户**：来自 `transaction_history` 的唯一用户数量

## 工作流程

### 第 1 步：解析用户查询

识别查询类型并提取参数。

需要提取的关键数据：
- `query_type`：概览 | 特定时间 | 特定指标 | 特定用户 | 团队报告 | 申请
- `time_range`：默认为 7 天或用户指定的时间段
- `metric`：佣金 | 交易量 | 费用 | 客户数量 | 交易用户（如果是指定指标）
- `user_id`：特定用户的 ID（如果是指定用户的查询）

### 第 2 步：验证时间范围

检查请求的时间范围是否有效，并确定是否需要拆分。

需要提取的关键数据：
- `needs_splitting`：布尔值（如果超过 30 天则为 true）
- `segments`：如果需要拆分，则为时间段数组
- `error`：如果时间范围超过 180 天，则为错误字符串

### 第 3 步：调用合作伙伴 API

根据查询类型，调用相应的合作伙伴 API。

**关键提醒**：
- 除非明确查询特定交易者的贡献，否则切勿使用 `user_id` 参数。
- API 响应中的 `user_id` 代表交易者，而非佣金接收者。
- 对于“我的佣金”等查询，请完全省略 `user_id` 参数。

对于概览或特定时间的查询：
- 使用时间参数调用 `/rebate/partner/transaction_history`（不使用 `user_id`）
- 使用时间参数调用 `/rebate/partner/commission_history`（不使用 `user_id`）
- 调用 `/rebate/partner/sub_list` 以获取客户数量

对于特定指标的查询：
- 仅根据指标调用所需的 API（除非另有指定，否则不使用 `user_id`）

对于特定用户的查询：
- 使用 `user_id` 参数调用 API（这将显示该特定交易者的贡献）

需要提取的关键数据：
- `transactions`：交易记录数组
- `commissions`：佣金记录数组
- `subordinates`：团队成员数组
- `total_count`：用于分页的总记录数

### 第 4 步：处理分页

如果 `total > limit`，则实施分页以获取所有数据。

需要提取的关键数据：
- `all_data`：分页后的完整数据集
- `pages_fetched`：执行的 API 调用次数

### 第 5 步：聚合数据

从原始 API 响应中计算所需的指标。

**重要提示**：根据业务规则使用自定义聚合逻辑。切勿简单地对所有数值求和。
- 考虑数据关系和业务逻辑。
- 适当处理不同的资产类型。
- 应用正确的分组和过滤规则。

需要提取的关键数据：
- `commission_amount`：根据业务规则聚合的佣金金额
- `trading_volume`：根据正确规则聚合的交易金额
- `net_fees`：根据正确规则聚合的费用
- `customer_count`：来自 `sub_list` 的总数
- `trading_users`：唯一用户 ID 的数量

### 第 6 步：格式化响应

根据查询类型使用模板生成适当的响应。

## 判断逻辑总结

| 条件 | 状态 | 操作 |
|-----------|--------|--------|
| 查询类型 = 概览 | ✅ | 使用默认的 7 天时间范围，调用所有 3 个 API |
| 查询类型 = 特定时间 | ✅ | 解析时间范围，检查是否需要拆分 |
| 查询类型 = 特定指标 | ✅ | 仅调用所需的 API |
| 查询类型 = 特定用户 | ✅ | 在 API 调用中添加 `user_id` 过滤条件（注意：`user_id` 代表交易者，而非接收者） |
| 查询类型 = 团队报告 | ✅ | 调用所有 API，生成综合报告 |
| 查询类型 = 申请 | ✅ | 不需要 API 调用，直接返回申请指导 |
| 时间范围 ≤30 天 | ✅ | 每个端点调用一次 API |
| 时间范围 >30 天且 ≤180 天 | ✅ | 拆分为多个 30 天的时段 |
| 时间范围 >180 天 | ❌ | 返回错误：“仅支持查询过去 180 天内的数据” |
| 相对时间描述（例如，“过去 7 天”） | ✅ | 根据当前 UTC+8 日期计算，转换为 00:00:00-23:59:59 UTC+8，然后转换为 Unix 时间戳 |
| 用户指定了未来日期 | ❌ | 拒绝查询——只能查询历史数据 |
| `to` 参数 > 当前时间戳 | ❌ | 拒绝查询——调整为当前时间或更早的时间 |
| API 返回 403 错误 | ❌ | 返回“无联盟成员权限”错误 |
| API 返回空数据 | ⚠️ | 将指标显示为 0，而不是错误 |
| 响应中的总数超过限制 | ✅ | 实施分页 |
| `user_id` 不在下属列表中 | ❌ | 返回“用户不在推荐网络中” |
| UID 格式无效 | ❌ | 返回格式错误信息 |
| 用户请求“我的佣金” | ✅ | 不使用 `user_id` 参数——查询所有佣金 |
| 用户指定了交易者 UID | ✅ | 使用 `user_id` 参数按该交易者进行筛选 |

## 报告模板

```markdown
# Affiliate Data Report

**Query Type**: {query_type}
**Time Range**: {from_date} to {to_date}
**Generated**: {timestamp}

## Metrics Summary

| Metric | Value |
|--------|-------|
| Commission Amount | {commission_amount} USDT |
| Trading Volume | {trading_volume} USDT |
| Net Fees | {net_fees} USDT |
| Customer Count | {customer_count} |
| Trading Users | {trading_users} |

## Details

{Additional details based on query type:
- For user-specific: User type, join date
- For team report: Top contributors, composition breakdown
- For comparison: Period-over-period changes}

## Notes

{Any relevant notes:
- Data retrieved in X segments (if split)
- Pagination: X pages fetched
- Warnings or limitations}

---
*For more details, visit the affiliate dashboard: https://www.gate.com/referral/affiliate*
```

## 使用场景

### 情况 1：概览查询（未指定时间）

**触发条件**：“我的联盟数据”、“显示我的合作伙伴统计信息”、“联盟仪表板”

**默认时间范围**：过去 7 天

**输出模板**：
```
Your affiliate data overview (last 7 days):
- Commission Amount: XXX USDT
- Trading Volume: XXX USDT
- Net Fees: XXX USDT
- Customer Count: XXX
- Trading Users: XXX

For detailed data, visit the affiliate dashboard: {dashboard_url}
```

### 情况 2：特定时间查询

**触发条件**：“本周的佣金”、“上个月的佣金”、“3 月的收益”

**时间处理**：
- 所有时间均基于用户系统的当前日期（UTC+8 时区）进行计算。
- 将日期范围转换为 UTC+8 时区的 00:00:00（开始）和 23:59:59（结束），然后转换为 Unix 时间戳。
- 如果时间范围 ≤30 天：调用一次 API。
- 如果时间范围 >30 天且 ≤180 天：拆分为多个 30 天的时段。
- 如果时间范围 >180 天：返回错误：“仅支持查询过去 180 天内的数据”。

**代理拆分逻辑**（针对超过 30 天的情况）：
```
Example: User requests 60 days (2026-01-01 to 2026-03-01 in UTC+8)
Convert to UTC+8 00:00:00 and 23:59:59, then to Unix timestamps:
1. 2026-01-01 00:00:00 UTC+8 to 2026-01-31 23:59:59 UTC+8 (31 days -> adjust to 30)
2. 2026-01-31 00:00:00 UTC+8 to 2026-03-01 23:59:59 UTC+8 (29 days)
Call each segment separately with converted timestamps, then merge results.
```

**输出模板**：
```
Your affiliate data for {time_range}:
- Commission Amount: XXX USDT
- Trading Volume: XXX USDT
- Net Fees: XXX USDT
- Customer Count: XXX
- Trading Users: XXX
```

### 情况 3：特定指标查询

**触发条件**：
- 佣金：“我的佣金收入”、“佣金收益”、“佣金金额”
- 交易量：“团队交易量”、“总交易量”
- 费用：“收取的净费用”、“费用贡献”
- 客户数量：“客户数量”、“团队规模”、“推荐数量”
- 交易用户：“活跃交易者”、“交易用户数量”

**输出模板**：
```
Your {metric_name} for the last 7 days: XXX {unit}

For detailed data, visit the affiliate dashboard: {dashboard_url}
```

### 情况 4：特定用户贡献

**触发条件**：“UID 123456 的贡献”、“用户 123456 的交易量”、“用户 123456 的佣金金额”

**重要提示**：`user_id` 参数用于筛选“交易者”，而非“佣金接收者”。这显示的是该特定交易者的交易活动和产生的佣金，而不是他们收到的佣金。

**参数**：
- 必需参数：`user_id`（要查询的特定交易者的 UID）
- 可选参数：时间范围（默认为过去 7 天）

**输出模板**：
```
UID {user_id} contribution (last 7 days):
- Commission Amount: XXX USDT (commission generated from this trader's activity)
- Trading Volume: XXX USDT (this trader's trading volume)
- Fees: XXX USDT (fees from this trader's trades)
```

### 情况 5：团队绩效报告

**触发条件**：“团队绩效”、“联盟报告”、“合作伙伴分析”

**处理流程**：
1. 调用 `sub_list` 获取团队成员。
2. 调用 `transaction_history` 获取交易数据。
3. 调用 `commission_history` 获取佣金数据。
4. 进行聚合和分析。

**输出模板**：
```
=== Team Performance Report ({time_range}) ===

📊 Team Overview
- Total Members: XXX (Sub-agents: X, Direct: X, Indirect: X)
- Active Users: XXX (XX.X%)
- New Members: XXX

💰 Trading Data
- Total Volume: XXX,XXX.XX USDT
- Total Fees: X,XXX.XX USDT
- Average Volume per User: XX,XXX.XX USDT

🏆 Commission Data
- Total Commission: XXX.XX USDT
- Spot Commission: XXX.XX USDT (XX%)
- Futures Commission: XXX.XX USDT (XX%)

👑 Top 5 Contributors
1. UID XXXXX - Volume XXX,XXX USDT / Commission XX.X USDT
2. ...
```

### 情况 6：联盟申请指导

**触发条件**：“申请成为联盟成员”、“成为合作伙伴”、“加入联盟计划”

**输出**（无需 API 调用）：
```
You can apply to become a Gate Exchange affiliate and earn commission from referred users' trading.

Application Process:
1. Open the affiliate application page
2. Fill in application information
3. Submit application
4. Wait for platform review

Application Portal: https://www.gate.com/referral/affiliate

Benefits:
- Earn commission from referred users
- Access to marketing materials
- Dedicated support team
- Performance analytics dashboard
```

## 错误处理

### 非联盟成员
```
Your account does not have affiliate privileges. 
To become an affiliate, please apply at: https://www.gate.com/referral/affiliate
```

### 时间范围超过 180 天
```
Query supports maximum 180 days of historical data.
Please adjust your time range.
```

### 无数据可用
```
No data found for the specified time range.
Please check if you have referred users with trading activity during this period.
```

### 未找到 UID
```
UID {user_id} not found in your referral network.
Please verify the user ID.
```

### UID 不是下属
```
UID {user_id} is not part of your referral network.
You can only query data for users you've referred.
```

### 子账户限制
```
Sub-accounts cannot query affiliate data.
Please use your main account.
```

## API 参数参考

### transaction_history
```
Parameters:
- currency_pair: string (optional) - e.g., "BTC_USDT"
- user_id: integer (optional) - IMPORTANT: This is the TRADER's ID, not commission receiver
- from: integer (required) - start timestamp (unix seconds)
- to: integer (required) - end timestamp (unix seconds)
- limit: integer (default 100) - max records per page
- offset: integer (default 0) - pagination offset

Response: {
  total: number,
  list: [{
    transaction_time, user_id (trader), group_name, 
    fee, fee_asset, currency_pair, 
    amount, amount_asset, source
  }]
}
```

### commission_history
```
Parameters:
- currency: string (optional) - e.g., "USDT"
- user_id: integer (optional) - IMPORTANT: This is the TRADER's ID who generated the commission
- from: integer (required) - start timestamp
- to: integer (required) - end timestamp
- limit: integer (default 100)
- offset: integer (default 0)

Response: {
  total: number,
  list: [{
    commission_time, user_id (trader), group_name,
    commission_amount, commission_asset, source
  }]
}
```

### sub_list
```
Parameters:
- user_id: integer (optional) - filter by user ID
- limit: integer (default 100)
- offset: integer (default 0)

Response: {
  total: number,
  list: [{
    user_id, user_join_time, type
  }]
}
Type: 1=Sub-agent, 2=Indirect customer, 3=Direct customer
```

## 分页策略

当总数据量超过限制时，使用分页策略获取完整数据：
```python
offset = 0
all_data = []
while True:
    result = call_api(limit=100, offset=offset)
    all_data.extend(result['list'])
    if len(result['list']) < 100 or offset + 100 >= result['total']:
        break
    offset += 100

# IMPORTANT: Apply custom aggregation logic after collecting all data
# DO NOT simply sum values - consider business rules and data relationships
```

## 时间处理

- API 接受以秒为单位的 Unix 时间戳（而非毫秒）。
- **⚠️ 关键时间计算规则**：
  - 所有查询时间均基于用户系统的当前日期（UTC+8 时区）进行计算。
  - 对于任何相对时间描述（“过去 7 天”、“过去 30 天”、“本周”、“过去一个月”等）：
    1. 获取当前系统的当前日期（UTC+8 时区）。
    2. 从当前日期减去请求的天数来计算开始日期。
    3. 将这两个日期转换为 UTC+8 时区的 00:00:00（开始时间）和 23:59:59（结束时间）。
    4. 将这些 UTC+8 时间转换为 Unix 时间戳。
    5. 使用这些时间戳进行 API 调用。
  - **切勿使用未来的时间戳作为查询条件**。
  - `to` 参数必须始终小于或等于当前的 Unix 时间戳。
  - 如果用户指定了未来的日期，请拒绝查询并说明只能查询历史数据。

- **时间转换示例**（假设当前日期为 2026-03-13（UTC+8）：
  - “过去 7 天”查询：
    - 开始日期：2026-03-07（7 天前）
    - 从：2026-03-07 00:00:00 UTC+8 → Unix 时间戳
    - 到：2026-03-13 23:59:59 UTC+8 → Unix 时间戳
  - “过去 30 天”查询：
    - 开始日期：2026-02-12（30 天前）
    - 从：2026-02-12 00:00:00 UTC+8 → Unix 时间戳
    - 到：2026-03-13 23:59:59 UTC+8 → Unix 时间戳
  - “本周”查询（假设周从周一开始）：
    - 开始日期：2026-03-09（当前周的周一）
    - 从：2026-03-09 00:00:00 UTC+8 → Unix 时间戳
    - 到：2026-03-13 23:59:59 UTC+8 → Unix 时间戳

- 每个 API 请求最多支持 30 天的数据，必要时进行拆分。

## 金额格式化

- 将字符串金额转换为数字进行计算。
- 以适当的精度显示金额（USD：2 位小数，BTC：8 位小数）。
- 对于较大的数字，添加千位分隔符。

## MCP 依赖项

此技能需要安装以下 MCP 工具：
- 启用了 rebate/partner 端点的 `gate-mcp`。

如果未安装，请提示用户安装：
```bash
npm install -g gate-mcp
```

## 验证示例

### 测试用例

1. **基本概览**
   - 查询：“显示我的联盟数据”
   - 预期结果：显示过去 7 天的指标。

2. **时间范围**
   - 查询：“过去 60 天的佣金”
   - 预期结果：拆分为 2 次 30 天的请求，并汇总结果。

3. **特定指标**
   - 查询：“我有多少客户？”
   - 预期结果：调用 `sub_list` 并返回总数。

4. **用户贡献**
   - 查询：“UID 12345 本月的交易量”
   - 预期结果：使用 `user_id` 过滤器调用 `transaction_history`。

5. **错误情况**
   - 查询：“过去 200 天的数据”
   - 预期结果：返回关于 180 天限制的错误信息。

6. **申请**
   - 查询：“如何成为联盟成员？”
   - 预期结果：无需 API 调用，直接返回申请指导。