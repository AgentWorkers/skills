---
name: treeline
description: 通过 Treeline Money 与您的财务信息进行互动。您可以查询余额、支出、预算和交易记录。
user-invocable: true
homepage: https://treeline.money
metadata: {"openclaw":{"emoji":"🌲","requires":{"bins":["tl"]},"install":[{"id":"tl-mac","kind":"download","url":"https://github.com/treeline-money/treeline/releases/latest/download/tl-macos-arm64","bins":["tl"],"label":"Install Treeline CLI (macOS)","os":["darwin"]},{"id":"tl-linux","kind":"download","url":"https://github.com/treeline-money/treeline/releases/latest/download/tl-linux-x64","bins":["tl"],"label":"Install Treeline CLI (Linux)","os":["linux"]},{"id":"tl-win","kind":"download","url":"https://github.com/treeline-money/treeline/releases/latest/download/tl-windows-x64.exe","bins":["tl.exe"],"label":"Install Treeline CLI (Windows)","os":["win32"]}]}}
---
# Treeline Money

**与您的财务数据进行交流。**您可以提出诸如“我的净资产是多少？”、“我在食品杂货上花了多少钱？”或“我是否超出了预算？”等问题，并从您自己的财务数据中立即获得答案。

---

## 快速入门

```bash
# 1. Install the CLI (OpenClaw handles this automatically)

# 2. Enable demo mode (sample data)
tl demo on

# 3. Try it out
tl status
```

---

## 首次设置

> **对于代理（agents）：** 如果 `tl` 命令出现“命令未找到”的错误，说明需要安装 CLI。OpenClaw 会通过技能元数据自动完成安装。请先从演示模式开始，以便用户可以立即尝试查询。

使用 `tl --version` 命令验证 CLI 是否已安装。建议从演示模式开始使用，以便用户可以立即尝试查询。

**可选：** 下载 [桌面应用程序](https://treeline.money/download) 以可视化地查看您的数据。

### 演示模式

演示模式会加载示例数据，用户无需连接银行即可尝试查询：

```bash
tl demo on
```

如需切换到真实数据，请参考以下步骤：
```bash
tl demo off
```

演示数据与真实数据是分开的。

### CLI 行为说明

- `tl demo on` 会输出成功信息；如果程序似乎卡住了，请稍等几秒钟（首次运行时会初始化数据库）。
- 使用 `tl demo status` 命令确认演示模式是否已启用。
- 由于数据库初始化的原因，某些命令在首次运行时可能需要几秒钟。
- 如果看到关于缺少表的错误，请再次运行 `tl demo on`。

### 连接真实数据

当用户准备好从演示模式过渡到使用真实数据时，请引导他们按照以下链接中的指南设置数据源。

数据源选项：
- **SimpleFIN**（每月 1.50 美元，适用于美国和加拿大用户）
- **Lunch Flow**（大约每月 3 美元，全球适用）
- **CSV 导入**（免费）

设置指南：[银行同步](https://treeline.money/docs/integrations/bank-sync/) · [CSV 导入](https://treeline.money/docs/integrations/csv-import/)

设置完成后，使用 `tl sync` 命令导入银行交易记录，或使用 `tl import` 命令导入 CSV 文件。

---

## 什么是 Treeline？

[Treeline Money](https://treeline.money) 是一款以本地数据为主导的个人财务管理应用程序。所有数据都存储在您设备上的本地 DuckDB 数据库中。无需云账户或订阅服务（同步服务为可选），您可以完全通过 SQL 查询访问您的财务数据。

---

## 限制

**不支持加密数据库。** 如果用户在 Treeline 中启用了数据库加密功能，CLI 命令将无法正常使用。用户需要：
- 如果希望 OpenClaw 能访问加密数据，请禁用加密功能；
- 或者直接使用 Treeline 应用程序来处理加密数据库。

如果遇到“数据库已加密”的错误，请向用户解释这一限制。

---

## 响应格式

**所有用于移动端/聊天的响应格式如下：**
- 使用项目符号，而非 Markdown 表格格式。
- 为了便于阅读，数字应四舍五入（例如显示为 $1,234 而不是 $1,234.56）。
- 先给出答案，再提供详细信息。
- 保持响应简洁——聊天不是用于查看电子表格的地方。
- 使用换行符分隔不同部分。

**示例良好的响应：**
```
Your net worth is $125k

Assets: $180k
- Retirement: $85k
- Savings: $25k
- Checking: $10k
- Home equity: $60k

Liabilities: $55k
- Mortgage: $52k
- Credit cards: $3k
```

**示例不良的响应：**
```
| Account | Type | Balance |
|---------|------|---------|
| My 401k Account | asset | 85234.56 |
...
```

---

## CLI 命令

### 读取命令（可自由执行）

这些命令仅用于读取数据，执行它们是安全的：

```bash
tl status              # Quick account summary with balances
tl status --json       # Same, but JSON output

tl query "SQL" --json  # Run any SQL query (database opened in read-only mode)
tl sql "SQL" --json    # Same as tl query (alias)

tl backup list         # List available backups
tl doctor              # Check database health
tl demo status         # Check if demo mode is on/off
```

> **注意：** `tl query` 和 `tl sql` 命令默认以只读模式打开数据库。除非指定了 `--allow-writes` 参数，否则它们无法修改数据（详见下面的写入命令）。

**使用 `tl status` 命令可以快速查看余额**——这比执行 SQL 查询更快。

### 写入命令（请先获得用户确认）

这些命令会修改本地数据。**在执行这些命令之前，请务必先获得用户的确认**，除非用户在 `PERMISSIONS.md` 文件中明确允许了这些操作（详见 [代理权限](#agent-permissions)）。

```bash
tl query "SQL" --allow-writes --json  # Run a SQL query with write access
tl sql "SQL" --allow-writes --json    # Same (alias)

tl sync                # Sync accounts/transactions from bank integrations
tl sync --dry-run      # Preview what would sync (read-only, safe to run)

tl import FILE -a ACCOUNT          # Import transactions from CSV
tl import FILE -a ACCOUNT --dry-run  # Preview import without applying (read-only, safe to run)
tl import FILE -a ACCOUNT --json   # JSON output for scripting

tl backup create       # Create a backup
tl backup restore NAME # Restore a backup

tl compact             # Compact database (reclaim space, optimize)

tl tag "groceries" --ids ID1,ID2  # Apply tags to transactions

tl demo on|off         # Toggle demo mode (sample data)
```

> **提示：** `--dry-run` 变体命令是只读的，执行时无需用户确认。可以在请求用户确认实际操作之前使用它们进行预览。

**如果用户反馈查询速度较慢，可以使用 `tl compact` 命令**——该命令可以优化数据库性能。

### CSV 导入说明

`tl import` 命令会自动从 CSV 文件的标题行中检测列映射。大多数银行的 CSV 文件都可以直接使用该命令导入：

```bash
tl import bank_export.csv --account "Chase Checking"
```

`--account` 或 `-a` 标志用于指定账户名称（不区分大小写，支持子字符串匹配）或 UUID。

**在使用 `tl import` 命令之前，请务必使用 `--dry-run` 命令先预览，以确保列名被正确检测到：**

```bash
tl import bank_export.csv -a "Checking" --dry-run --json
```

**所有导入参数**（`--account` 除外均为可选参数）：

| 参数 | 用途 | 示例 |
|------|---------|---------|
| `--date-column` | 替换日期列 | `--date-column "Post Date"` |
| `--amount-column` | 替换金额列 | `--amount-column "Amt"` |
| `--description-column` | 替换描述列 | `--description-column "Memo"` |
| `--debit-column` | 使用借方列代替金额列 | `--debit-column "Debit"` |
| `--credit-column` | 使用贷方列代替金额列 | `--credit-column "Credit"` |
| `--balance-column` | 显示当前余额（生成快照） | `--balance-column "Balance"` |
| `--flip-signs` | 反转金额符号（适用于信用卡交易记录） | `--flip-signs` |
| `--debit-negative` | 将借方金额显示为负数 | `--debit-negative` |
| `--skip-rows N` | 跳过前 N 行 | `--skip-rows 3` |
| `--number-format` | 数字格式（`us`, `eu`, `eu_space`） | `--number-format eu` |
| `--profile NAME` | 加载已保存的配置文件 | `--profile chase` |
| `--save-profile NAME` | 将设置保存为配置文件 | `--save-profile chase` |
| `--dry-run` | 不导入数据的情况下进行预览 | `--dry-run` |
| `--json` | 输出 JSON 格式 | `--json` |

**代理常用的参数组合：**

```bash
# Step 1: Find the account UUID
tl status --json

# Step 2: Preview import
tl import transactions.csv -a "550e8400-e29b-41d4-a716-446655440000" --dry-run --json

# Step 3: Execute import
tl import transactions.csv -a "550e8400-e29b-41d4-a716-446655440000" --json
```

在重新导入数据时，系统会自动检测并跳过重复的交易记录。

---

## 代理权限

**在执行任何写入命令之前，请检查此技能目录下的 `PERMISSIONS.md` 文件。**

如果该文件存在，请阅读其中的内容，了解用户已预先批准哪些写入命令。已预先批准的命令可以无需确认即可执行。其他所有写入命令在执行前仍需用户明确确认。

如果 `PERMISSIONS.md` 文件不存在，请**在执行任何写入命令之前务必先询问用户**。

**`PERMISSIONS.md` 文件的模板：**

```markdown
# Treeline Agent Permissions

Commands listed here are pre-approved — the agent can run them without
asking for confirmation each time. Remove a line to require confirmation.

## Allowed write commands
- tl sync
- tl backup create
- tl demo on|off
```

---

## 用户上下文信息

**在回答财务相关问题之前，请检查此技能目录下的 `CONTEXT.md` 文件。**

如果该文件存在，请先阅读其中的内容——其中包含用户特定的信息：
- 账户类型（例如退休账户、投资账户等）
- 标签规则和资金流动规则
- 插件配置
- 个人偏好设置

**当发现用户的设置发生变化时：**
- 对于较小的调整，可以在 `CONTEXT.md` 中记录下来，并简要说明更改内容。
- 对于重要的假设或更正内容，请询问用户：“是否希望将这些信息保存到您的 Treeline 财务设置中？”

有关更多详细信息，请参阅文末的 [用户上下文信息模板](#user-context-pattern) 部分。

---

## 快速参考

### 净资产
```bash
tl query "
WITH latest AS (
  SELECT DISTINCT ON (account_id) account_id, balance
  FROM sys_balance_snapshots
  ORDER BY account_id, snapshot_time DESC
)
SELECT
  SUM(CASE WHEN a.classification = 'asset' THEN s.balance ELSE 0 END) as assets,
  SUM(CASE WHEN a.classification = 'liability' THEN ABS(s.balance) ELSE 0 END) as liabilities,
  SUM(CASE WHEN a.classification = 'asset' THEN s.balance ELSE -ABS(s.balance) END) as net_worth
FROM accounts a
JOIN latest s ON a.account_id = s.account_id
" --json
```

### 账户余额
```bash
tl query "
WITH latest AS (
  SELECT DISTINCT ON (account_id) account_id, balance
  FROM sys_balance_snapshots
  ORDER BY account_id, snapshot_time DESC
)
SELECT a.name, a.classification, a.institution_name, s.balance
FROM accounts a
JOIN latest s ON a.account_id = s.account_id
ORDER BY s.balance DESC
" --json
```

### 实际支出（不包括内部转账）

请查看 `CONTEXT.md` 文件中的 `internal_transfer_tags` 设置。默认的过滤规则如下：
```bash
tl query "
SELECT SUM(ABS(amount)) as total_spent
FROM transactions
WHERE amount < 0
  AND transaction_date >= date_trunc('month', current_date)
  AND NOT (tags && ARRAY['transfer', 'savings', 'investment'])
" --json
```

### 按标签分类的支出
```bash
tl query "
SELECT tags, SUM(ABS(amount)) as spent
FROM transactions
WHERE amount < 0
  AND transaction_date >= '2026-01-01' AND transaction_date < '2026-02-01'
  AND tags IS NOT NULL AND tags != '[]'
GROUP BY tags
ORDER BY spent DESC
" --json
```

### 最近的交易记录
```bash
tl query "
SELECT t.description, t.amount, t.transaction_date, a.name as account
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
ORDER BY t.transaction_date DESC
LIMIT 10
" --json
```

---

## 数据库架构

### 核心表格

**accounts** 表：
| 列名 | 说明 |
|--------|-------------|
| `account_id` | UUID 主键 |
| `name` | 账户显示名称 |
| `classification` | 账户类型（资产或负债） |
| `account_type` | `credit`、`investment`、`Loan`、`other` 或 `null` |
| `institution_name` | 银行/金融机构名称 |
| `currency` | 货币代码（例如 `USD`） |
| `is_manual` | 常量字段，表示数据是手动添加的还是同步来的 |

**sys_balance_snapshots** 表——余额数据的真实来源：
| 列名 | 说明 |
|--------|-------------|
| `snapshot_id` | UUID 主键 |
| `account_id` | 外键，关联到 `accounts` 表 |
| `balance` | 快照时的账户余额 |
| `snapshot_time` | 数据记录的时间 |
| `source` | 数据来源（同步、手动添加等）

**transactions** 表：
| 列名 | 说明 |
|--------|-------------|
| `transaction_id` | UUID 主键 |
| `account_id` | 外键，关联到 `accounts` 表 |
| `amount` | 交易金额（负数表示支出） |
| `description` | 交易描述 |
| `transaction_date` | 交易发生时间 |
| `posted_date` | 交易结算时间 |
| `tags` | 交易标签数组 |

### 标签与分类

**标签** 是 Treeline 的核心概念——每笔交易都可以关联多个标签。

**分类** 来自 `plugin_budget` 插件，该插件会将标签映射到预算类别。并非所有用户都安装了此插件。

---

## 插件系统

插件都有自己的 DuckDB 数据表结构：`plugin_<name>.*`

### 查看已安装的插件
```bash
tl query "
SELECT schema_name
FROM information_schema.schemata
WHERE schema_name LIKE 'plugin_%'
" --json
```

### 常见插件及其数据表结构

**plugin_budget.categories** 表——预算分类：
| 列名 | 说明 |
|--------|-------------|
| `category_id` | UUID 主键 |
| `month` | 日期格式（`YYYY-MM`） |
| `type` | 类型（收入或支出） |
| `name` | 分类名称 |
| `expected` | 预算金额 |
| `tags` | 用于匹配的标签数组 |

**plugin_goals.goals** 表——储蓄目标：
| 列名 | 说明 |
|--------|-------------|
| `id` | UUID 主键 |
| `name` | 目标名称 |
| `target_amount` | 目标金额 |
| `target_date` | 目标完成日期 |
| `completed` | 是否已完成 |
| `active` | 是否处于活动状态 |

**plugin_subscriptions** 表——检测到的定期费用记录

**plugin_cashflow** 表——现金流预测

**plugin_emergency_fund** 表——紧急基金管理

请查看 `CONTEXT.md` 文件，了解用户已安装了哪些插件以及这些插件提供了哪些功能。

---

## 常用操作模式

### 获取当前余额

始终使用最新的数据快照：
```sql
WITH latest AS (
  SELECT DISTINCT ON (account_id) account_id, balance
  FROM sys_balance_snapshots
  ORDER BY account_id, snapshot_time DESC
)
SELECT a.name, s.balance
FROM accounts a
JOIN latest s ON a.account_id = s.account_id
```

### 标签的使用

标签是以数组形式存储的：
```sql
-- Contains a specific tag
WHERE tags @> ARRAY['groceries']

-- Contains any of these tags
WHERE tags && ARRAY['food', 'dining']

-- Note: UNNEST doesn't work in all contexts in DuckDB
-- Instead, GROUP BY tags directly
```

### 日期过滤
```sql
-- This month
WHERE transaction_date >= date_trunc('month', current_date)

-- Specific month
WHERE transaction_date >= '2026-01-01'
  AND transaction_date < '2026-02-01'
```

### 预算与实际支出对比
```sql
SELECT
  c.name,
  c.expected,
  COALESCE(SUM(ABS(t.amount)), 0) as actual,
  c.expected - COALESCE(SUM(ABS(t.amount)), 0) as remaining
FROM plugin_budget.categories c
LEFT JOIN transactions t ON t.tags && c.tags
  AND t.amount < 0
  AND t.transaction_date >= (c.month || '-01')::DATE
  AND t.transaction_date < (c.month || '-01')::DATE + INTERVAL '1 month'
WHERE c.month = strftime(current_date, '%Y-%m')
  AND c.type = 'expense'
GROUP BY c.category_id, c.name, c.expected
```

---

## 问题处理方式

| 用户提出的问题 | 处理方法 |
|-----------|----------|
| “我的净资产是多少？” | 执行净资产查询 |
| “账户余额是多少？” | 执行账户余额查询 |
| “[某类别] 的支出是多少？” | 使用 `name ILIKE '%X%'` 进行过滤 |
| “我在 [某项支出] 上花了多少钱？” | 执行实际支出查询（排除内部转账记录） |
| “我的支出是否超出了预算？” | 需要预算插件来比较预算与实际支出 |
| “最近的交易记录有哪些？” | 按时间降序排序并限制结果数量 |
| “我的储蓄情况如何？” | 按账户类型或名称过滤账户 |
| “关于退休账户的信息？” | 使用关键词（如 401k、IRA 等）进行过滤 |
| “导入 CSV 文件” / “上传交易记录” | 指导用户使用 `tl import` 命令，使用 `--dry-run` 预览数据 |
| “从 [银行名称] 导入数据” | 根据银行的 CSV 格式使用 `tl import` 命令 |

---

## 提示

1. **始终使用 `--json` 选项** 以获得可解析的输出格式。
2. **金额显示为带符号的形式**——负数表示支出。
3. **使用 `classification` 字段区分资产和负债。
4. **余额数据存储在快照中**，而不是 `accounts` 表中。
5. **请查阅 `CONTEXT.md` 文件以了解用户的账户类型和标签规则**。

---

## 用户上下文信息模板

在安装此技能后，请创建 `CONTEXT.md` 文件来存储用户的个性化设置。这样既能保持技能的通用性，又能实现个性化功能。

**`CONTEXT.md` 文件的模板：**

```markdown
# Treeline User Context
*Auto-updated by your assistant as it learns your setup*

## Account Notes
<!-- What specific accounts mean, e.g.: -->
<!-- - "Company 401k" = retirement account -->
<!-- - "Home Equity" = home value estimate (manual) -->

## Tag Conventions
<!-- How the user uses tags -->

## Cash Flow Rules
<!-- Tags to exclude from "true spending" calculations -->
internal_transfer_tags: [transfer, savings, investment]

## Income Sources
<!-- Known income sources for better reporting -->

## Active Plugins
<!-- Which plugins are installed and relevant -->

## Preferences
<!-- Reporting style, rounding, spouse-friendly mode, etc. -->

## Learned Facts
<!-- Anything else discovered about the user's financial setup -->
```

**维护说明：**
- 对于小的调整，简要说明更改内容。
- 在记录重要信息之前，请先征求用户确认。
- 定期根据实际数据验证设置（账户信息或标签可能会发生变化）。

---

## 隐私声明

所有数据都存储在本地（`~/.treeline/treeline.duckdb` 文件中）。除非用户明确要求，否则切勿在对话之外分享任何交易描述或账户详细信息。