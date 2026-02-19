---
name: starling-bank
description: 通过 `starling-bank-mcp` 服务器来管理 Starling Bank 账户。您可以查询余额、查看交易记录、添加收款人、进行支付、管理储蓄目标以及追踪支出。当用户询问他们的银行余额、交易记录、支付情况、储蓄状况、直接扣款信息或任何与 Starling Bank 相关的操作时，可以使用该工具。使用此工具需要 `starling-bank-mcp` npm 包以及一个 Starling 个人访问令牌。
---
# Starling Bank

通过 `mcporter` 和 `starling-bank-mcp` 管理 Starling Bank 账户。

## 设置

### 1. 安装 MCP 服务器

```bash
npm i -g starling-bank-mcp
```

### 2. 获取个人访问令牌

在 [https://developer.starlingbank.com/](https://developer.starlingbank.com/) 上创建一个个人访问令牌（需要包含所需的权限范围）。

### 3. 配置 `mcporter`

```bash
mcporter config add starling \
  --command "node $(npm root -g)/starling-bank-mcp/dist/main.js" \
  --env STARLING_BANK_ACCESS_TOKEN="YOUR_TOKEN"
```

### 4. 验证配置

```bash
mcporter list starling --schema
```

## 快速参考

### 账户基础

```bash
# List accounts (get accountUid and default categoryUid)
mcporter call starling.accounts_list

# Get balance
mcporter call starling.account_balance_get accountUid=ACCOUNT_UID

# Get account holder info
mcporter call starling.account_holder_get

# Get sort code / account number
mcporter call starling.account_identifiers_get accountUid=ACCOUNT_UID
```

### 交易

```bash
# List transactions (ISO 8601 timestamps required)
mcporter call starling.transactions_list \
  accountUid=ACCOUNT_UID \
  categoryUid=CATEGORY_UID \
  minTransactionTimestamp=2026-01-01T00:00:00.000Z \
  maxTransactionTimestamp=2026-01-31T23:59:59.999Z

# Get single transaction detail
mcporter call starling.feed_item_get \
  accountUid=ACCOUNT_UID \
  categoryUid=CATEGORY_UID \
  feedItemUid=FEED_ITEM_UID
```

### 支付

```bash
# List payees
mcporter call starling.payees_list

# Create payee
mcporter call starling.payee_create \
  payeeName="John Smith" \
  payeeType=INDIVIDUAL \
  accountIdentifier=12345678 \
  bankIdentifier=608371 \
  bankIdentifierType=SORT_CODE \
  countryCode=GB

# Make payment (amount in minor units / pence)
mcporter call starling.payment_create \
  accountUid=ACCOUNT_UID \
  categoryUid=CATEGORY_UID \
  destinationPayeeAccountUid=PAYEE_ACCOUNT_UID \
  reference="Payment ref" \
  --args '{"amount":{"currency":"GBP","minorUnits":1000}}'
```

### 储蓄目标

```bash
# List goals
mcporter call starling.savings_goals_list accountUid=ACCOUNT_UID

# Create goal
mcporter call starling.savings_goal_create \
  accountUid=ACCOUNT_UID name="Emergency Fund" currency=GBP \
  --args '{"target":{"currency":"GBP","minorUnits":100000}}'

# Deposit into goal
mcporter call starling.savings_goal_deposit \
  accountUid=ACCOUNT_UID savingsGoalUid=GOAL_UID \
  --args '{"amount":{"currency":"GBP","minorUnits":5000}}'

# Withdraw from goal
mcporter call starling.savings_goal_withdraw \
  accountUid=ACCOUNT_UID savingsGoalUid=GOAL_UID \
  --args '{"amount":{"currency":"GBP","minorUnits":5000}}'
```

### 其他功能

```bash
# Direct debits
mcporter call starling.direct_debits_list accountUid=ACCOUNT_UID

# Standing orders
mcporter call starling.standing_orders_list \
  accountUid=ACCOUNT_UID categoryUid=CATEGORY_UID

# Cards
mcporter call starling.cards_list

# Lock/unlock card
mcporter call starling.card_lock_update cardUid=CARD_UID enabled=false
```

## 工作流程：首次设置

1. 运行 `accounts_list` 命令以获取 `accountUid` 和 `defaultCategory`（`categoryUid`）。
2. 将这些 ID 保存下来——它们是大多数操作所必需的。
3. 运行 `account_balance_get` 命令以验证访问权限是否正常。
4. 将账户详细信息存储在内存或配置文件中以供后续使用。

## 注意事项

- 所有金额均以 **最小单位**（便士）表示。例如：£10.50 = 1050。
- 时间戳必须遵循 **ISO 8601** 格式：`2026-02-17T00:00:00.000Z`。
- `categoryUid` 即 `accounts_list` 中返回的 `defaultCategory`，用于主账户的交易记录。
- 账户余额字段包括：`clearedBalance`（已结算金额）和 `effectiveBalance`（包括未结算金额）。
- 有关完整的工具架构，请参阅 [references/api-details.md](references/api-details.md)。