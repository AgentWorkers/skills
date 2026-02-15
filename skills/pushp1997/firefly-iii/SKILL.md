---
name: firefly-iii
description: 通过 Firefly III API 管理个人财务。当用户询问预算、交易、账户、分类、储蓄计划、订阅服务或财务报告时，可以使用该 API。该 API 支持创建、列出和更新交易记录；管理账户和余额；设置预算；以及跟踪储蓄目标。
---

# Firefly III

Firefly III 是一个自托管的个人财务管理工具。该工具提供了用于管理个人财务的 API 接口。

## 配置

所需环境：
- `FIREFLY_URL`：基础 URL（例如：`https://budget.example.com`）
- `FIREFLY_TOKEN`：个人访问令牌（存储在 `~/.firefly_token` 文件中）

获取令牌：登录 Firefly III → 选择 “OAuth” → “个人访问令牌” → “创建新令牌”

## API 基础知识

```bash
TOKEN=$(cat ~/.firefly_token)
BASE="$FIREFLY_URL/api/v1"
curl -s "$BASE/endpoint" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json"
```

## 核心接口端点

### 账户（Accounts）
```bash
# List accounts
curl "$BASE/accounts?type=asset" # asset|expense|revenue|liability
# Create account
curl -X POST "$BASE/accounts" -d '{
  "name": "Bank Account",
  "type": "asset",
  "account_role": "defaultAsset",
  "currency_code": "EUR"
}'
```

账户类型：`asset`（资产）、`expense`（支出）、`revenue`（收入）、`liability`（负债）
账户角色：`defaultAsset`（默认账户）、`savingAsset`（储蓄账户）、`sharedAsset`（共享账户）、`ccAsset`（信用卡账户）

### 交易（Transactions）
```bash
# List transactions
curl "$BASE/transactions?type=withdrawal&start=2026-01-01&end=2026-01-31"
# Create withdrawal (expense)
curl -X POST "$BASE/transactions" -d '{
  "transactions": [{
    "type": "withdrawal",
    "date": "2026-01-15",
    "amount": "50.00",
    "description": "Groceries",
    "source_name": "Bank Account",
    "destination_name": "Supermarket",
    "category_name": "Groceries"
  }]
}'
# Create deposit (income)
curl -X POST "$BASE/transactions" -d '{
  "transactions": [{
    "type": "deposit",
    "date": "2026-01-01",
    "amount": "3000.00",
    "description": "Salary",
    "source_name": "Employer",
    "destination_name": "Bank Account",
    "category_name": "Salary"
  }]
}'
# Create transfer
curl -X POST "$BASE/transactions" -d '{
  "transactions": [{
    "type": "transfer",
    "date": "2026-01-05",
    "amount": "500.00",
    "description": "Savings",
    "source_name": "Bank Account",
    "destination_name": "Savings Account"
  }]
}'
```

交易类型：`withdrawal`（取款）、`deposit`（存款）、`transfer`（转账）

### 分类（Categories）
```bash
# List categories
curl "$BASE/categories"
# Create category
curl -X POST "$BASE/categories" -d '{"name": "Groceries"}'
```

### 预算（Budgets）
```bash
# List budgets
curl "$BASE/budgets"
# Create budget
curl -X POST "$BASE/budgets" -d '{"name": "Food", "active": true}'
# Set budget limit for period
curl -X POST "$BASE/budgets/{id}/limits" -d '{
  "start": "2026-01-01",
  "end": "2026-01-31",
  "amount": "500.00"
}'
```

### 储蓄目标（Piggy Banks）
```bash
# List piggy banks
curl "$BASE/piggy-banks"
# Create piggy bank
curl -X POST "$BASE/piggy-banks" -d '{
  "name": "Vacation Fund",
  "target_amount": "2000.00",
  "accounts": [{"account_id": "1"}],
  "start_date": "2026-01-01",
  "target_date": "2026-12-31",
  "transaction_currency_code": "EUR"
}'
# Add money to piggy bank
curl -X POST "$BASE/piggy-banks/{id}/events" -d '{"amount": "100.00"}'
```

### 订阅服务（Subscriptions）
```bash
# List subscriptions
curl "$BASE/subscriptions"
# Create subscription
curl -X POST "$BASE/subscriptions" -d '{
  "name": "Netflix",
  "amount_min": "12.99",
  "amount_max": "12.99",
  "date": "2026-01-15",
  "repeat_freq": "monthly",
  "currency_code": "EUR"
}'
```

重复频率：`weekly`（每周）、`monthly`（每月）、`quarterly`（每季度）、`half-yearly`（每半年）、`yearly`（每年）

### 循环交易（Recurring Transactions）
```bash
# List recurring transactions
curl "$BASE/recurrences"
# Create recurring transaction
curl -X POST "$BASE/recurrences" -d '{
  "type": "withdrawal",
  "title": "Rent",
  "first_date": "2026-01-01",
  "repeat_until": "2026-12-31",
  "repetitions": [{
    "type": "monthly",
    "moment": "1"
  }],
  "transactions": [{
    "amount": "1000.00",
    "description": "Monthly rent",
    "source_id": "1",
    "destination_name": "Landlord",
    "category_name": "Rent"
  }]
}'
```

### 规则（自动分类）（Rules）
```bash
# List rules
curl "$BASE/rules"
# Create rule
curl -X POST "$BASE/rules" -d '{
  "title": "Categorize groceries",
  "trigger": "store-journal",
  "active": true,
  "strict": false,
  "triggers": [
    {"type": "description_contains", "value": "ALDI"}
  ],
  "actions": [
    {"type": "set_category", "value": "Groceries"}
  ]
}'
```

触发条件类型：`description_contains`（描述中包含特定关键词）、`description_starts`（描述以特定字符串开头）、`description_ends`（描述以特定字符串结尾）、`amount_less`（金额小于某值）、`amount_more`（金额大于某值）、`source_account_is`（来源账户为特定账户）等
操作类型：`set_category`（设置分类）、`set_budget`（设置预算）、`add_tag`（添加标签）、`set_description`（设置描述）等

### 标签（Tags）
```bash
# List tags
curl "$BASE/tags"
# Create tag
curl -X POST "$BASE/tags" -d '{"tag": "vacation"}'
```

### 报告与汇总（Reports & Summary）
```bash
# Account balance over time
curl "$BASE/accounts/{id}/transactions?start=2026-01-01&end=2026-01-31"
# Get current balances
curl "$BASE/accounts" | jq '.data[] | {name: .attributes.name, balance: .attributes.current_balance}'
```

## 常见操作

### 按类别查看支出（Get spending by category）
```bash
curl "$BASE/categories" | jq '.data[] | {name: .attributes.name, spent: .attributes.spent}'
```

### 查看预算进度（Get budget progress）
```bash
curl "$BASE/budgets" | jq '.data[] | {name: .attributes.name, spent: .attributes.spent}'
```

### 搜索交易（Search transactions）
```bash
curl "$BASE/search/transactions?query=groceries&limit=25"
```

## 错误处理

- `422 Unprocessable Entity`：错误响应中包含未填写的必填字段
- `401 Unauthorized`：令牌过期或无效
- `404 Not Found`：资源不存在

## 使用提示

- 使用 `source_name`/`destination_name` 自动创建支出/收入账户
- 分类用于对交易进行分类，而预算用于设置支出限制
- 储蓄目标需要关联到某个资产账户
- 可以使用规则在交易创建时自动对其进行分类