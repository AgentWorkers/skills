---
name: expense-tracker
description: "只需说出你的支出情况，AI 会自动记录、分类，并将其与你的预算进行对比。无需使用任何应用程序或填写表格，整个过程非常便捷。支持自然语言输入，例如：“在 Costco 花了 45 美元”或“和 Jake 分摊了 90 美元的晚餐费用”。系统提供 16 个自动分类选项，每月会发送预算提醒，并生成周报和月报。整个系统完全在本地运行——你的支出数据会保存在你的设备上。"
version: "1.0.2"
category: finance
tags: [expenses, budget, finance, spending, personal-finance, tracking, reports, money, frugal, budgeting, natural-language, local]
---
# 费用追踪技能

通过自然对话来追踪、分类和预算个人开支。用户用通俗语言描述开支，AI会记录这些开支，监控预算并生成报告。

## 技能目录

```
skills/expense-tracker/
├── SKILL.md                    # This file — AI instructions
├── references/
│   ├── categories.json         # Category definitions + keyword matching
│   └── budgets.json            # Monthly budget limits (user-editable)
├── scripts/
│   ├── add-expense.sh          # Add expense to ledger
│   ├── query.sh                # Query/filter expenses
│   └── budget-check.sh         # Check spending vs budget
├── templates/
│   ├── weekly-report.md        # Weekly report template
│   └── monthly-report.md       # Monthly report template
└── expenses/
    └── ledger.json             # Transaction data (auto-created)
```

---

## 1. 自然语言开支解析

当用户提到花费时，提取以下信息：

| 字段 | 是否必填 | 提取方法 |
|-------|----------|----------------|
| **金额** | 是 | 金额格式："$45", "45 dollars", "forty-five bucks", "45.99" |
| **商家** | 是 | 位于 "at", "from", "to" 之后的名称，或根据上下文确定的商家名称 |
| **类别** | 自动匹配 | 根据 `references/categories.json` 中的关键词与商家/上下文进行匹配 |
| **日期** | 默认为今天 | "today", "yesterday", "last Tuesday", "on 2/14" 等具体日期 |
| **备注** | 可选 | 用户添加的额外信息，例如 "用于聚会"、"工作开支" |

### 解析示例

| 用户输入 | 金额 | 商家 | 类别 | 日期 | 备注 |
|-----------|--------|--------|----------|------|-------|
| "在 Costco 花了 45 美元" | 45 | Costco | 食品杂货 | today | |
| "昨天在 Chipotle 吃午饭花了 18 美元" | 18 | Chipotle | 餐饮 | yesterday | |
| "电费 120 美元" | 120 | 电力公司 | 公共事业 | today | |
| "在 Shell 加满油，花了 55 美元" | 55 | Shell | 油气/交通 | today | |
| "Netflix 账户花费 15.99 美元" | 15.99 | Netflix | 订阅服务 | today | |
| "在 Target 花了 200 美元购买生日用品" | 200 | Target | 购物 | today | birthday stuff |
| "从 Amazon 领回了 35 美元的退款" | -35 | Amazon | 购物 | today | refund |
| "支付了 2000 美元的房租" | 2000 | 房东 | 住房 | today | |
| "昨天在 Starbucks 花了 5.50 美元" | 5.50 | Starbucks | 餐饮 | yesterday | |
| "带狗去看兽医，花了 280 美元" | 280 | 兽医 | 宠物护理 | today | |
| "汽车保险费用 180 美元" | 180 | 汽车保险 | 保险 | today | |
| "在 Target 购买了食品杂货和衣服，共花费 150 美元" | 150 | Target | 购物 | ask user to split or pick | |

### 模糊类别的处理

当一个商家可能属于多个类别时（例如 "Walmart" 可能属于食品杂货或购物）：

1. **首先尝试最可能的类别**：根据上下文选择最合适的类别
2. **与用户确认**："我在 Walmart 记录了 85 美元的开支，是归类为 **食品杂货** 吗？还是更像是购物？"
3. **记住用户的偏好**：如果用户进行了更正，记录下其偏好以便后续使用

当没有匹配到合适的类别时，使用 **杂项** 并询问用户："这笔开支归类为杂项吗？"

---

## 2. 命令

### `/add` — 记录开支

明确记录一笔开支。

**使用方法：** `/add <金额> <商家> [类别] [日期] [备注]`

**实现方式：** 运行 `add-expense` 脚本：
```bash
bash skills/expense-tracker/scripts/add-expense.sh <amount> "<category>" "<vendor>" "<date>" "<notes>"
```

**示例：**
- `/add 45 Costco` → 记录在 Costco 的 45 美元开支，自动分类为食品杂货，日期为今天
- `/add 18.50 Chipotle Dining yesterday` → 记录在 Chipotle 的 18.50 美元餐饮开支，日期为昨天
- `/add -35 Amazon Shopping 2026-02-10 "退款 for headphones"` → 记录为 35 美元的退款

大多数情况下，用户不会使用 `/add` 命令，他们只会简单地说 "在 Costco 花了 45 美元"，然后系统会自动解析这些信息。

### `/spending` — 查看开支记录

可以按需查询开支记录。

**使用方法：** `/spending [时间段] [类别]`

**实现方式：** 运行 `query` 脚本：
```bash
bash skills/expense-tracker/scripts/query.sh [--from DATE] [--to DATE] [--category CAT] [--format summary|detail|json]
```

**示例：**
- `/spending` → 查看当前月份的开支总结
- `/spending this week` → 查看本周的开支记录
- `/spending Dining` → 查看本月的所有餐饮开支
- `/spending February detail` → 查看二月份的详细开支明细
- "我在食品杂货上花了多少钱？" → 使用 `--category Groceries` 查询
- "我上周花了多少钱？" → 使用适当的日期范围查询

**格式选项：**
- `summary`（默认）——按类别汇总
- `detail` — 显示所有字段的详细列表
- `json` — 显示原始的 JSON 格式

### `/budget` — 预算监控

检查实际开支与预算是否超标。

**使用方法：** `/budget [月份]`

**实现方式：** 运行 `budget-check` 脚本：
```bash
bash skills/expense-tracker/scripts/budget-check.sh [YYYY-MM]
```

**示例：**
- `/budget` → 查看当前月份的预算状况
- `/budget 2026-01` → 查看一月份的预算情况
- "我的预算情况如何？" → 运行预算检查

**还可以调整预算：**
- "将我的餐饮预算设置为 400 美元" → 使用 `jq --arg` 更新 `references/budgets.json` 文件
- "我的食品杂货预算是多少？" → 从 `budgets.json` 中读取预算信息

### `/categories` — 查看/管理类别

显示可用的类别或重新分类开支记录。

**示例：**
- `/categories` → 列出所有类别
- `/categories Dining` → 显示餐饮类别及其最近的开支记录
- "将开支 #12 移到娱乐类别" → 更新该开支的类别

---

## 3. 自动类别匹配

使用 `references/categories.json` 将商家与类别进行匹配。匹配规则如下：

1. **完全匹配关键词**：检查商家名称（小写）是否包含某个关键词
2. **部分匹配**：检查商家名称是否是某个关键词的子字符串
3. **上下文线索**：根据周围的文字判断类别（例如 "在...用餐" → 分类为餐饮）
4. **备用方案**：将开支归类为杂项

### 可用类别
食品杂货（Groceries）、餐饮（Dining）、燃气/交通（Gas/Transport）、订阅服务（Subscriptions）、健康/健身（Health/Fitness）、娱乐（Entertainment）、购物（Shopping）、公共事业（Utilities）、住房（Housing）、个人护理（Personal Care）、教育（Education）、礼物（Gifts）、旅行（Travel）、保险（Insurance）、宠物（Pets）、杂项（Miscellaneous）。

### 多个匹配时的优先级
1. 最具体的关键词优先（例如 "Costco gas" 优先于 "Groceries"）
2. 用户输入的上下文
3. 用户的历史消费习惯
4. 用户的明确指示

---

## 4. 预算跟踪

预算配置保存在 `references/budgets.json` 文件中。用户可以编辑该文件来设置自己的预算限制。

### 警告阈值

| 阈值 | 表情符号 | 动作 |
|-----------|-------|--------|
| < 50% | ⚪ | 不发出警报 |
| 50–79% | 🟢 | 仅提供信息提示 |
| 80–99% | 🟡 | 主动警告："注意：您的餐饮预算已达到 85%" |
| ≥ 100% | 🔴 | 警告："您的餐饮预算已超出 300 美元的预算（实际花费 312 美元）"

### 警告时机

- **每次记录开支时**：在记录后自动检查预算是否超标。只有当预算超过 80% 时才会发出警报。
- 执行 `/budget` 命令时：显示所有类别的详细预算情况。
- **每周**：在生成每周报告时，包含预算状态信息。

### 主动预算提醒

当某笔开支导致某个类别的预算超过 80% 时，会添加备注：

> ✅ 支出 #24：2026-02-17 在 Olive Garden 花费 45.00 美元（餐饮）
> ⚠️ 注意：您的餐饮预算已达到 275 美元（占预算 92%）

当预算超过 100% 时：

> ✅ 支出 #25：2026-02-19 在 Thai Palace 花费 38.00 美元（餐饮）
> 🔴 餐饮预算已超出 300 美元的预算（实际花费 313 美元）

---

## 5. 报告生成

### 周报

使用 `templates/weekly-report.md` 作为模板。当用户请求 "生成周报" 或类似信息时，根据该模板生成报告。

**生成方法：** 首先运行 `query.sh` 来获取指定日期范围的开支数据，然后使用模板格式化结果：

```bash
# Get this week's data
bash skills/expense-tracker/scripts/query.sh --from 2026-02-10 --to 2026-02-16 --format json

# Get last week for comparison
bash skills/expense-tracker/scripts/query.sh --from 2026-02-03 --to 2026-02-09 --format json

# Get budget status
bash skills/expense-tracker/scripts/budget-check.sh
```

报告内容包括：类别明细、最高开支项目、预算状况以及环比趋势。

### 月报

使用 `templates/monthly-report.md` 作为模板。当用户请求 "生成月报" 或类似信息时，生成月度报告。

```bash
# Current month data
bash skills/expense-tracker/scripts/query.sh --from 2026-02-01 --to 2026-02-28 --format json

# Previous month for comparison
bash skills/expense-tracker/scripts/query.sh --from 2026-01-01 --to 2026-01-31 --format json

# Budget check
bash skills/expense-tracker/scripts/budget-check.sh 2026-02
```

报告内容包括：完整的类别明细、最高开支项目、环比数据以及月度对比（如果预算中设置了收入信息）。

---

## 6. 特殊情况处理

### 退款

- 检测关键词："refund", "returned", "got back", "credit", "reimbursement"
- 将退款金额记录为负数：`add-expense.sh -35 "Shopping" "Amazon" "2026-02-15" "refund"`
- 退款会减少预算中的相应类别金额

### 分摊开支

- "与 Sarah 分摊了 80 美元的晚餐费用" → 记录 40 美元（用户应承担的部分）
- "在酒吧的消费分摊为三份，每人 120 美元" → 分别记录 40 美元
- 确认分摊情况："记录您的份额：在酒吧的消费为 40 美元（餐饮）"

### 定期开支

- 该技能不会自动安排定期开支的记录
- 当用户提到 "再次订阅 Netflix" 或 "支付月度健身费用" 时，会将其视为新的开支记录
- AI 可以提醒用户："需要在下个月提醒您吗？"（但不会自动创建新的记录）

### 多项购买

- "在 Target 花了 150 美元购买食品杂货和衣服" → 询问用户是合并记录还是分开记录
- 如果需要分开记录：按类别分别创建条目
- 如果只购买了一项：选择主要类别或询问用户具体是哪一项
- "在 Panera 吃午饭和喝咖啡，共花费 22 美元" → 可以合并记录为餐饮开支

### 多种货币

- 如果用户提到外币（例如 "在巴黎花费了 50 欧元"）：
  - 记录原始金额并注明货币：`add-expense.sh 55 "Travel" "Paris restaurant" "2026-02-15" "€50 EUR"`
  - 为预算计算转换为美元（询问用户汇率或使用近似值）
  - 默认行为：假设使用美元，除非用户另有说明

### 更正信息

- "实际上在 Costco 的花费是 52 美元，不是 45 美元" → 查找最近的开支记录并更新金额
- "删除开支记录 #12" → 使用 `jq --argjson id 12 'map(select(.id != $id))` 从账本中删除该记录（始终使用 `--arg/--argjson`，避免在过滤字符串中插入 ID）
- "将记录 #12 的类别更改为娱乐" → 更新该记录的类别

### 无开支的日子

- 除非用户特别要求，否则不会在无开支的日子发出警报
- 在报告中，将无开支的日子显示为正数（表示节省）

---

## 7. 对话流程

AI 应能自然地处理用户的对话，无需用户输入特定命令：

| 用户输入 | AI 动作 |
|-----------|-----------|
| "在 Costco 花了 45 美元" | 解析信息 → 记录开支 → 检查预算 |
| "我这个月花了多少钱？" | 查询当前月份的开支记录并生成摘要 |
| "我超出预算了吗？" | 检查预算状况并生成报告 |
| "生成周报" | 根据模板生成周报 |
| "我在食品杂货上花了多少钱？" | 查询食品杂货和餐饮类别的开支 |
| "我从 Amazon 领回了 20 美元的退款" | 记录退款金额并确认 |
| "与 Jake 分摊了 90 美元的晚餐费用" | 计算各自应承担的金额并记录 |
| "最后那笔开支应该归类为娱乐，而不是购物" | 更新最近记录的类别 |
| "将食品杂货预算设置为 700 美元" | 更新预算设置 |
| "我的餐饮预算还剩多少？" | 计算当前预算与已花费金额的差额 |
| "显示上周的所有开支记录" | 根据日期范围查询并生成详细报告 |
| "我这个月的最大开支项目是什么？" | 查询并排序开支金额 |
| "取消那笔开支记录" | 从账本中删除最近的开支记录 |
| "昨天在 Starbucks 花了 5.50 美元" | 根据日期记录开支 |
| "兽医费用是 280 美元" | 将其记录为宠物护理类别 |
| "汽车保险费用是 180 美元" | 将其记录为保险类别 |
| "我在 Target 花了大约 50 美元" | 根据用户提供的金额记录开支 |
| "我从工作单位获得了 45 美元的退款" | 将退款金额记录为负数 |
| "我这个月在食品杂货上花了多少钱？" | 合并计算食品杂货和餐饮类别的开支 |
| "比较这个月和上个月的开支" | 生成环比报告 |

---

## 8. 完整交互示例

```
User: spent $45 at Costco
AI: ✅ Expense #1: $45.00 at Costco (Groceries) on 2026-02-17

User: grabbed lunch at Chipotle for $12.50
AI: ✅ Expense #2: $12.50 at Chipotle (Dining) on 2026-02-17

User: $150 at Target yesterday
AI: I logged $150 at Target as **Shopping** — was this groceries or more of a general shopping trip?
User: shopping
AI: ✅ Expense #3: $150.00 at Target (Shopping) on 2026-02-16

User: how's my budget looking?
AI:
=== Budget Check: 2026-02 ===
  🟢 OK    Groceries        $345     / $600   (58%)
  🟡 WARN  Dining           $248     / $300   (83%)
  🟢 OK    Shopping         $280     / $300   (93%)
  ⚪ LOW   Gas/Transport    $85      / $250   (34%)
  ...
  TOTAL: $1,245.00 / $4,950 (25%)

⚠️ Heads up — Dining is at 83% and Shopping is at 93% of your February budget.

User: I got a refund from Amazon for $35
AI: ✅ Refund #4: $35.00 from Amazon (Shopping) on 2026-02-17
   Shopping is now at $245 / $300 (82%) for February.

User: weekly report
AI: [generates formatted weekly report from template]

User: set my dining budget to $400
AI: Updated Dining budget: $300 → $400 for this month. You're now at $248 / $400 (62%) — much more breathing room! 🟢
```

---

## 9. 数据格式参考

### 账本记录（expenses/ledger.json）

### 关键规则
- **ID**：递增的整数，不得重复使用
- **金额**：必须为数字，正数表示开支，负数表示退款
- **日期**：使用 ISO 8601 格式（YYYY-MM-DD）
- **类别**：必须与 `references/categories.json` 中的名称匹配
- **created_at**：记录创建时的 UTC 时间戳

---

## 10. 脚本参考

所有脚本位于 `skills/expense-tracker/scripts/` 目录中，需要使用 `bash` 命令来执行：

```bash
# Add an expense
bash skills/expense-tracker/scripts/add-expense.sh 45 "Groceries" "Costco" "2026-02-17" "weekly groceries"

# Query expenses
bash skills/expense-tracker/scripts/query.sh --from 2026-02-01 --to 2026-02-28 --category Dining --format summary

# Check budget
bash skills/expense-tracker/scripts/budget-check.sh 2026-02
```

### 脚本参数

**add-expense.sh** `<金额> <类别> <商家> [日期] [备注]`
- `amount` — 数字（退款金额用负数表示）
- `category` — 从 `categories.json` 中选择的类别名称
- `vendor` — 商家名称
- `date` — 日期格式（YYYY-MM-DD，默认为今天）
- `notes` — 可选的备注信息

**query.sh** `[--from DATE] [--to DATE] [--category CAT] [--vendor TEXT] [--format FMT]`
- `--from` — 开始日期（包含当天）
- `--to` — 结束日期（包含当天）
- `--category` — 按类别过滤
- `--vendor` — 按商家名称过滤（部分匹配，不区分大小写）
- `--format` — 输出格式（`summary`、`detail` 或 `json`）

**budget-check.sh** `[YYYY-MM]`
- 可选参数：月份（默认为当前月份）
- 返回代码 0 表示一切正常；返回代码 1 表示至少有一个类别的预算超过 80%

---

这些脚本用于实现费用追踪功能的各个方面，确保用户能够方便地管理和监控自己的开支。