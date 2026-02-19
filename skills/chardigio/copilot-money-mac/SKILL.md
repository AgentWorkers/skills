---
name: copilot-money
description: 从 Copilot Money Mac 应用程序中查询和分析个人财务数据。当用户询问其支出、交易记录、账户余额、预算或财务趋势时，可以使用此功能。
---
# Copilot Money

从 Copilot Money Mac 应用程序中查询本地数据，以分析交易记录、消费模式、账户余额、投资情况和预算。数据存储在 SQLite 数据库（用于存储交易记录和余额）以及 Firestore 的 LevelDB 缓存中（用于存储重复性支出（如房租、Netflix 费用）和预算信息。

## 数据库位置

```
~/Library/Group Containers/group.com.copilot.production/database/CopilotDB.sqlite
```

## 数据库模式

### Transactions 表

所有财务交易的主体表。

| 列名 | 类型 | 描述 |
|--------|------|-------------|
| id      | TEXT | 主键 |
| date    | DATE | 交易日期 |
| name     | TEXT | 商户/交易名称 |
| original_name | TEXT | 银行提供的原始名称 |
| amount    | DOUBLE | 交易金额（正数表示支出） |
| iso_currency_code | TEXT | 货币代码（例如 "USD"） |
| account_id | TEXT | 关联的账户信息 |
| category_id | TEXT | 交易所属类别 |
| pending   | BOOLEAN | 交易是否待处理 |
| recurring | BOOLEAN | 交易是否为重复性支出 |
| recurring_id | TEXT | 重复性支出的详细信息（存储在 Firestore 中） |
| user_note | TEXT | 用户添加的备注 |
| user_deleted | BOOLEAN | 是否被用户标记为已删除 |

### accountDailyBalance 表

每个账户的每日余额快照。

| 列名 | 类型 | 描述 |
|--------|------|-------------|
| date    | TEXT | 快照日期 |
| account_id | TEXT | 账户信息 |
| current_balance | DOUBLE | 当日余额 |
| available_balance | DOUBLE | 可用余额 |

## Firestore 缓存（LevelDB）

部分数据存储在 Firestore 的本地 LevelDB 缓存中，而非 SQLite 数据库中。

**存储位置：**
```
~/Library/Containers/com.copilot.production/Data/Library/Application Support/firestore/__FIRAPP_DEFAULT/copilot-production-22904/main/*.ldb
```

### 数据集合

| 集合名 | 描述 |
|------------|-------------|
| items     | 关联的银行账户/金融机构信息 |
| investment_prices | 历史股票价格 |
| investment_performance | 每项投资的加权回报（TWR） |
| investment_splits | 股票分割历史记录 |
| securities | 股票/基金的元数据 |
| users/.../budgets | 预算信息（金额、类别ID） |
| users/.../recurrings | 重复性支出信息 |
| amazon     | 亚马逊订单匹配数据 |

### 重复性支出定义

| 字段名 | 描述 |
|-------|-------------|
| name     | 显示名称（例如 "房租"、"Netflix"） |
| match_string | 用于匹配的交易名称（例如 "CHECK PAID"） |
| plaid_category_id | 重复性支出的类别ID |
| state    | "active"（活跃）或 "inactive"（不活跃） |

### 不存储在 SQLite 中的数据

- **重复性支出名称**：如 "房租"、"Netflix" 等便于人类阅读的名称 |
- **预算金额**：每个类别的月度预算 |
- **投资数据**：持有的股票/基金信息、价格、收益情况、分割历史 |
- **账户/金融机构名称**：如 Chase、Fidelity 等 |
- **类别名称**：如餐厅、旅行、食品杂货等

### 从 LevelDB 中提取数据

- **列出所有重复性支出名称：**
```bash
for f in ~/Library/Containers/com.copilot.production/Data/Library/Application\ Support/firestore/__FIRAPP_DEFAULT/copilot-production-22904/main/*.ldb; do
  strings "$f" 2>/dev/null | grep -B10 "^state$" | grep -A1 "^name$" | grep -v "^name$" | grep -v "^--$"
done | sort -u | grep -v "^$"
```

- **列出所有数据集合：**
```bash
for f in ~/Library/Containers/com.copilot.production/Data/Library/Application\ Support/firestore/__FIRAPP_DEFAULT/copilot-production-22904/main/*.ldb; do
  strings "$f" 2>/dev/null
done | grep -oE "documents/[a-z_]+/" | sort | uniq -c | sort -rn
```

- **查找类别名称：**
```bash
for f in ~/Library/Containers/com.copilot.production/Data/Library/Application\ Support/firestore/__FIRAPP_DEFAULT/copilot-production-22904/main/*.ldb; do
  strings "$f" 2>/dev/null
done | grep -iE "^(groceries|restaurants|shopping|entertainment|travel|transportation|utilities)$" | sort -u
```

## 常用查询

- **最近的交易记录：**
```sql
SELECT date, name, amount, category_id
FROM Transactions
WHERE user_deleted = 0
ORDER BY date DESC
LIMIT 20;
```

- **每月支出汇总：**
```sql
SELECT strftime('%Y-%m', date) as month, SUM(amount) as total
FROM Transactions
WHERE amount > 0 AND user_deleted = 0
GROUP BY month
ORDER BY month DESC;
```

- **按类别划分的支出：**
```sql
SELECT category_id, SUM(amount) as total, COUNT(*) as count
FROM Transactions
WHERE amount > 0 AND user_deleted = 0 AND date >= date('now', '-30 days')
GROUP BY category_id
ORDER BY total DESC;
```

- **搜索交易记录：**
```sql
SELECT date, name, amount
FROM Transactions
WHERE name LIKE '%SEARCH_TERM%' AND user_deleted = 0
ORDER BY date DESC;
```

- **列出所有重复性支出记录：**
```sql
SELECT DISTINCT name, recurring_id
FROM Transactions
WHERE recurring = 1 AND user_deleted = 0
ORDER BY name;
```

## 使用方法

使用 `sqlite3` 查询数据库：

```bash
sqlite3 ~/Library/Group\ Containers/group.com.copilot.production/database/CopilotDB.sqlite "YOUR_QUERY"
```

- 如需格式化输出结果，请使用以下代码：
```bash
sqlite3 -header -column ~/Library/Group\ Containers/group.com.copilot.production/database/CopilotDB.sqlite "YOUR_QUERY"
```

## 注意事项：

- 类别 ID 是不可见的字符串；在分析时可以按这些 ID 进行分组（类别名称存储在 Firestore 缓存中）
- 金额的正负值分别表示支出和收入
- 使用 `user_deleted = 0` 来过滤已删除的交易记录
- 两个数据库都在应用程序中持续被使用；仅读访问是安全的
- SQLite 中的 `recurring_id` 用于关联 Firestore 中的重复性支出记录
- 在 LevelDB 文件中使用 `strings` 格式来提取可读的数据