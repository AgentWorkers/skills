---
name: pocketsmith
description: 通过 API 管理 PocketSmith 的交易记录、分类以及财务数据。
metadata: {"openclaw": {"category": "finance", "requires": {"env": ["POCKETSMITH_DEVELOPER_KEY"]}, "optional_env": ["POCKETSMITH_ALLOW_WRITES"]}}
---

# PocketSmith 技能

用于管理 PocketSmith 的交易记录和分类信息。支持列出、搜索、创建、更新和删除财务数据。

## 先决条件

请设置以下环境变量：
- `POCKETSMITH_DEVELOPER_KEY` - 您的 PocketSmith 开发者密钥（可在“设置” > “安全” > “管理开发者密钥”中获取）
- `POCKETSMITH_ALLOW_WRITES` - 设置为 `true` 以启用创建、更新和删除操作（出于安全考虑，默认情况下此功能是禁用的）

## 命令

所有命令均需在技能目录下使用 `uv run pocketsmith` 来执行。

### 认证

```bash
# Check authentication status and get user info
pocketsmith auth status

# Get current user details
pocketsmith me
```

### 交易记录

```bash
# Get a single transaction
pocketsmith transactions get <transaction_id>

# List transactions for a user
pocketsmith transactions list-by-user <user_id>
pocketsmith transactions list-by-user <user_id> --start-date 2024-01-01 --end-date 2024-12-31
pocketsmith transactions list-by-user <user_id> --search "coffee"
pocketsmith transactions list-by-user <user_id> --uncategorised
pocketsmith transactions list-by-user <user_id> --needs-review
pocketsmith transactions list-by-user <user_id> --type debit

# List transactions by account
pocketsmith transactions list-by-account <account_id>

# List transactions by category
pocketsmith transactions list-by-category <category_ids>  # comma-separated

# List transactions by transaction account
pocketsmith transactions list-by-transaction-account <transaction_account_id>

# Create a transaction (requires POCKETSMITH_ALLOW_WRITES=true)
pocketsmith transactions create <transaction_account_id> --payee "Store Name" --amount -50.00 --date 2024-01-15
pocketsmith transactions create <transaction_account_id> --payee "Salary" --amount 5000.00 --date 2024-01-01 --category-id 123

# Update a transaction (requires POCKETSMITH_ALLOW_WRITES=true)
pocketsmith transactions update <transaction_id> --category-id 456
pocketsmith transactions update <transaction_id> --payee "New Payee" --note "Updated note"
pocketsmith transactions update <transaction_id> --labels "groceries,essential"

# Delete a transaction (requires POCKETSMITH_ALLOW_WRITES=true)
pocketsmith transactions delete <transaction_id>
```

### 分类信息

```bash
# Get a single category
pocketsmith categories get <category_id>

# List all categories for a user
pocketsmith categories list <user_id>

# Create a category (requires POCKETSMITH_ALLOW_WRITES=true)
pocketsmith categories create <user_id> --title "New Category"
pocketsmith categories create <user_id> --title "Subcategory" --parent-id 123
pocketsmith categories create <user_id> --title "Bills" --colour "#ff0000" --is-bill true

# Update a category (requires POCKETSMITH_ALLOW_WRITES=true)
pocketsmith categories update <category_id> --title "Renamed Category"
pocketsmith categories update <category_id> --parent-id 456
pocketsmith categories update <category_id> --no-parent  # Make top-level
pocketsmith categories update <category_id> --colour "#00ff00"

# Delete a category (requires POCKETSMITH_ALLOW_WRITES=true)
pocketsmith categories delete <category_id>
```

### 标签

```bash
# List all labels for a user
pocketsmith labels list <user_id>
```

### 预算管理

```bash
# List budget for a user (per-category budget analysis)
pocketsmith budget list <user_id>
pocketsmith budget list <user_id> --roll-up true

# Get budget summary for a user
pocketsmith budget summary <user_id> --period months --interval 1 --start-date 2024-01-01 --end-date 2024-12-31

# Get trend analysis (requires category and scenario IDs)
pocketsmith budget trend <user_id> --period months --interval 1 --start-date 2024-01-01 --end-date 2024-12-31 --categories "123,456" --scenarios "1,2"

# Refresh forecast cache (requires POCKETSMITH_ALLOW_WRITES=true)
pocketsmith budget refresh <user_id>
```

## 交易记录过滤选项

在列出交易记录时，可以使用以下过滤条件：
- `--start-date` - 按日期过滤（格式为 YYYY-MM-DD）
- `--end-date` - 按日期过滤（格式为 YYYY-MM-DD）
- `--updated-since` - 仅显示在此时间之后更新的交易记录
- `--uncategorised` - 仅显示未分类的交易记录
- `--type` - 按交易类型过滤：`debit`（借方）或 `credit`（贷方）
- `--needs-review` - 仅显示需要审核的交易记录
- `--search` - 按收款人或备注内容进行搜索
- `--page` - 分页页码

## 分类信息创建/更新选项

在创建或更新分类信息时，可以使用以下参数：
- `--title` - 分类名称
- `--colour` - CSS 十六进制颜色（例如：`#ff0000`）
- `--parent-id` - 子分类的父分类 ID
- `--no-parent` - 将分类设置为顶级分类（仅用于更新）
- `--is-transfer` - 标记为转账分类（true/false）
- `--is-bill` - 标记为账单分类（true/false）
- `--roll-up` - 是否将分类数据汇总到父分类（true/false）
- `--refund-behaviour` - 仅显示借方交易（`debit_only`）或仅显示贷方交易（`credit_only`）

## 输出格式

所有命令的输出均为 JSON 格式。以下是一个交易记录的示例：

```json
{
  "id": 1234567,
  "payee": "Coffee Shop",
  "amount": -5.50,
  "date": "2024-01-15",
  "category": {
    "id": 123,
    "title": "Eating Out"
  },
  "transaction_account": {
    "id": 456,
    "name": "Checking Account"
  }
}
```

## 日期格式

所有日期均采用 `YYYY-MM-DD` 的格式（例如：`2024-01-15`）。

## 写入保护

出于安全考虑，**默认情况下** 禁用写入操作（创建、更新、删除）。如需启用这些操作，请执行以下操作：

```bash
export POCKETSMITH_ALLOW_WRITES=true
```

如果不启用写入保护，执行写入命令将会失败：

```json
{"error": "Write operations are disabled by default. Set POCKETSMITH_ALLOW_WRITES=true to enable create, update, and delete operations.", "hint": "export POCKETSMITH_ALLOW_WRITES=true"}
```

## 常见工作流程

- **搜索和分类交易记录**
- **组织分类信息**
- **审核交易记录**

```bash
# Find uncategorised transactions
pocketsmith transactions list-by-user 123456 --uncategorised

# Search for specific transactions
pocketsmith transactions list-by-user 123456 --search "Netflix"

# Categorize a transaction
pocketsmith transactions update 789012 --category-id 456
```
- **```bash
# List existing categories
pocketsmith categories list 123456

# Create a new subcategory
pocketsmith categories create 123456 --title "Streaming" --parent-id 789

# Move a category under a different parent
pocketsmith categories update 101112 --parent-id 789
```
- **```bash
# Find transactions needing review
pocketsmith transactions list-by-user 123456 --needs-review

# Mark as reviewed by updating
pocketsmith transactions update 789012 --needs-review false
```