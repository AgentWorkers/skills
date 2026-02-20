---
name: expense-tracker
description: "基于聊天的个人开支管理工具。用户可以用简单的语言记录开支、监控预算、生成支出报告并管理开支类别。适用于需要记录开支、查看预算、查看支出汇总、设置预算限制或查询支出情况的情况。触发事件包括：用户输入“我花了钱”、“记录开支”、“我总共花了多少钱”、“预算”、“支出报告”以及“添加购买记录”。"
---# 费用追踪技能

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

当用户提到支出时，提取以下信息：

| 字段 | 是否必填 | 提取方法 |
|-------|----------|----------------|
| **金额** | 是 | 金额格式："$45", "45 dollars", "forty-five bucks", "45.99" |
| **商家** | 是 | 位于 "at", "from", "to" 之后的名称，或根据上下文确定的商家名称 |
| **类别** | 自动匹配 | 根据 `references/categories.json` 中的关键词与商家/上下文进行匹配 |
| **日期** | 默认为今天 | "today", "yesterday", "last Tuesday", "on 2/14" 等明确日期 |
| **备注** | 可选 | 用户添加的额外信息 — "用于聚会", "工作开支" |

### 解析示例

| 用户输入 | 金额 | 商家 | 类别 | 日期 | 备注 |
|-----------|--------|--------|----------|------|-------|
| "在 Costco 花了 45 美元" | 45 | Costco | 食品杂货 | 今天 | |
| "昨天在 Chipotle 吃午饭花了 18 美元" | 18 | Chipotle | 餐饮 | 昨天 | |
| "电费 120 美元" | 120 | 电力公司 | 公共事业 | 今天 | |
| "在 Shell 加满油，花了 55 美元" | 55 | Shell | 汽油/交通 | 今天 | |
| "Netflix 15.99 美元" | 15.99 | Netflix | 订阅服务 | 今天 | |
| "在 Target 花了 200 美元购买生日用品" | 200 | Target | 购物 | 今天 | 生日用品 |
| "从 Amazon 领到了 35 美元的退款" | -35 | Amazon | 购物 | 今天 | 退款 |
| "支付了 2000 美元的房租" | 2000 | 房东 | 房屋 | 今天 | |
| "昨天在 Starbucks 花了 5.50 美元" | 5.50 | Starbucks | 餐饮 | 昨天 | |
| "带狗去看兽医，花了 280 美元" | 280 | 兽医 | 宠物 | 今天 | |
| "汽车保险 180 美元" | 180 | 汽车保险 | 保险 | 今天 | |

### 模糊类别的处理

当一个商家可能属于多个类别时（例如 "Walmart" 可能属于食品杂货或购物）：

1. **首先猜测最可能的类别**：根据上下文选择最合适的类别
2. **与用户确认**："我在 Walmart 记录了 85 美元作为 **食品杂货** — 这样对吗？还是更像是购物？"
3. **记住用户的偏好**：如果用户进行了更正，记录下其偏好以便将来参考

当没有任何类别匹配时，使用 **杂项** 并询问用户："我应该把这个记录在哪个具体类别下？"

---

## 2. 命令

### `/add` — 记录开支

明确记录一笔开支。

**用法：** `/add <金额> <商家> [类别] [日期] [备注]`

**实现方式：** 运行 `add-expense.sh` 脚本：
```bash
bash skills/expense-tracker/scripts/add-expense.sh <amount> "<category>" "<vendor>" "<date>" "<notes>"
```

**示例：**
- `/add 45 Costco` → 记录在 Costco 的 45 美元开支，自动分类，日期为今天
- `/add 18.50 Chipotle Dining yesterday` → 记录昨天在 Chipotle 的 18.50 美元餐饮开支
- `/add -35 Amazon Shopping 2026-02-10 "退款 for headphones"` → 记录 2026-02-10 日从 Amazon 的 35 美元退款

大多数情况下，用户不会使用 `/add` 命令 — 他们通常只会说 "在 Costco 花了 45 美元"，然后系统会自动解析。

### `/spending` — 查看开支

查询开支，支持可选过滤条件。

**用法：** `/spending [时间段] [类别]`

**实现方式：** 运行 `query.sh` 脚本：
```bash
bash skills/expense-tracker/scripts/query.sh [--from DATE] [--to DATE] [--category CAT] [--format summary|detail|json]
```

**示例：**
- `/spending` → 当前月份的总览
- `/spending this week` → 本周的开支
- `/spending Dining` → 本月所有的餐饮开支
- `/spending February detail` → 二月份的详细开支明细
- "我在食品杂货上花了多少钱？" → 使用 `--category Groceries` 进行查询
- "我上周花了多少钱？" → 使用适当的日期范围进行查询

**格式选项：**
- `summary`（默认） — 按类别统计总数
- `detail` — 显示所有字段的详细列表
- `json` — 原始 JSON 输出

### `/budget` — 预算状态

检查开支是否超出预算限制。

**用法：** `/budget [月份]`

**实现方式：** 运行 `budget-check.sh` 脚本：
```bash
bash skills/expense-tracker/scripts/budget-check.sh [YYYY-MM]
```

**示例：**
- `/budget` → 当前月份的预算状态
- `/budget 2026-01` → 查看一月份的预算情况
- "我的预算怎么样？" → 运行预算检查

**还支持调整预算：**
- "将我的餐饮预算设置为 400 美元" → 更新 `references/budgets.json`
- "我的食品杂货预算是多少？" → 从 budgets.json 中读取

### `/categories` — 查看/管理类别

显示可用类别或重新分类开支。

**示例：**
- `/categories` → 列出所有类别
- `/categories Dining` → 显示餐饮类别及其最近的开支记录
- "将开支 #12 移到 Entertainment 类别" → 更新账目类别

---

## 3. 类别自动匹配

使用 `references/categories.json` 将商家与类别进行匹配。匹配规则如下：

1. **精确匹配**：检查商家名称（小写）是否包含任何关键词
2. **部分匹配**：检查商家名称是否是某个关键词的子字符串
3. **上下文线索**：根据周围的文字判断类别（例如 "在...吃饭" → 餐饮，"在...加油" → 汽油/交通）
4. **备用选项**：将开支记录为 **杂项**

### 可用类别
食品杂货（Groceries）、餐饮（Dining）、汽油/交通（Gas/Transport）、订阅服务（Subscriptions）、健康/健身（Health/Fitness）、娱乐（Entertainment）、购物（Shopping）、公共事业（Utilities）、住房（Housing）、个人护理（Personal Care）、教育（Education）、礼物（Gifts）、旅行（Travel）、保险（Insurance）、宠物（Pets）、杂项（Miscellaneous）。

### 多个匹配时的优先级
1. 最具体的关键词优先（例如 "Costco gas" 优先于 "Groceries"）
2. 用户消息中的上下文
3. 用户对该商家的历史消费习惯
4. 询问用户

---

## 4. 预算跟踪

预算配置保存在 `references/budgets.json` 中。用户可以编辑该文件来设置预算限制。

### 警告阈值

| 阈值 | 表情符号 | 动作 |
|-----------|-------|--------|
| < 50% | ⚪ | 不发出警报 |
| 50–79% | 🟢 | 仅提供信息提示 |
| 80–99% | 🟡 | 主动警告："注意 — 餐饮开支占您 300 美元预算的 85%" |
| ≥ 100% | 🔴 | 警告："您的餐饮预算已超出（300 美元中的 312 美元）"

### 警告时机

- **每次记录开支时**：记录后自动检查预算。仅在预算超过 80% 时发出警告。
- **执行 `/budget` 命令时**：显示所有类别的详细预算情况。
- **每周**：在生成每周报告时，包含预算状态部分。

### 主动预算提醒

当某笔开支使某个类别的支出超过 80% 时，会添加备注：

> ✅ 开支 #24：2026-02-17 在 Olive Garden 花了 45.00 美元（餐饮）
> ⚠️ 注意 — 二月份的餐饮开支已达到 300 美元预算的 85%（275 美元）

当开支超过 100% 时：

> ✅ 开支 #25：2026-02-19 在 Thai Palace 花了 38.00 美元（餐饮）
> 🔴 餐饮开支已超出您的预算（300 美元中的 313 美元）

---

## 5. 报告生成

### 周报

使用 `templates/weekly-report.md` 作为模板。当用户请求 "每周报告" 或类似内容时生成报告。

**生成方法**：运行 `query.sh` 来获取指定日期范围的开支数据，然后使用模板格式化结果：

```bash
# Get this week's data
bash skills/expense-tracker/scripts/query.sh --from 2026-02-10 --to 2026-02-16 --format json

# Get last week for comparison
bash skills/expense-tracker/scripts/query.sh --from 2026-02-03 --to 2026-02-09 --format json

# Get budget status
bash skills/expense-tracker/scripts/budget-check.sh
```

报告内容包括：类别明细、主要开支项目、预算状态以及环比趋势。

### 月报

使用 `templates/monthly-report.md` 作为模板。在用户请求 "月报" 或类似内容时生成报告。

```bash
# Current month data
bash skills/expense-tracker/scripts/query.sh --from 2026-02-01 --to 2026-02-28 --format json

# Previous month for comparison
bash skills/expense-tracker/scripts/query.sh --from 2026-01-01 --to 2026-01-31 --format json

# Budget check
bash skills/expense-tracker/scripts/budget-check.sh 2026-02
```

报告内容包括：完整的类别明细、主要开支项目、环比数据以及月度对比（如果 `budgets.json` 中设置了收入信息）。

---

## 6. 特殊情况处理

### 退款

- 检测关键词："refund", "returned", "got back", "credit", "reimbursement"
- 将退款记录为负数：`add-expense.sh -35 "Shopping" "Amazon" "2026-02-15" "refund"`
- 退款会减少预算中的相应类别总额

### 分摊开支

- "和 Sarah 分摊了 80 美元的晚餐费用" → 记录 40 美元（用户承担的部分）
- "在酒吧分摊了 300 美元的费用" → 记录 40 美元
- 确认分摊情况："正在记录您的份额：在酒吧花费了 40 美元（餐饮）。对吗？"

### 定期开支

- 该技能不自动安排定期开支
- 当用户提到 "再次订阅 Netflix" 或 "支付月度健身费用" 时，视为新的开支记录
- AI 可以提醒用户："需要在下个月提醒您吗？"（但不会自动创建新记录）

### 多项购买

- "在 Target 花了 150 美元购买食品杂货和衣服" → 询问用户是记录为一笔开支还是分开记录
- 如果需要分开记录：按类别创建单独的条目
- 如果只购买了一项：选择主要类别或询问用户
- "在 Panera 吃午饭和喝咖啡，花了 22 美元" → 可以记录为单一的餐饮开支

### 多货币（可选）

- 如果用户提到外币：例如 "在巴黎花了 50 欧元"
- 记录原始金额并注明货币：`add-expense.sh 55 "Travel" "Paris restaurant" "2026-02-15" "€50 EUR"`
- 为预算计算转换为美元（询问用户汇率或使用近似值）
- 默认行为：除非用户特别说明，否则假设使用美元

### 更正

- "实际上在 Costco 的花费是 52 美元，不是 45 美元" → 查找最近的 Costco 支出记录并更新金额
- "删除开支 #12" → 从账本中删除该条目（使用 jq 按 ID 过滤）
- "将开支 #12 移到 Entertainment 类别" → 更新类别字段

### 无开支的日子

- 除非用户要求，否则不会在无开支的日子发出警报
- 在报告中，将无开支的日子显示为正数（表示节省）

---

## 7. 对话模式

AI 应能自然地处理以下对话：

| 用户输入 | AI 动作 |
|-----------|-----------|
| "在 Costco 花了 45 美元" | 解析 → 记录开支 → 检查预算 |
| "我这个月花了多少钱？" | 运行查询并生成当前月份的开支汇总 |
| "我超出预算了吗？" | 运行预算检查并显示状态 |
| "生成每周报告" | 根据模板生成每周报告 |
| "我在食品杂货上花了多少钱？" | 查询食品杂货和餐饮类别的开支 |
| "我从 Amazon 领到了 20 美元的退款" | 记录为负数并确认 |
| "和 Jake 分摊了 90 美元的晚餐费用" | 计算各自承担的金额并记录 |
| "最后那笔开支应该归类为娱乐，而不是购物" | 更新最近条目的类别 |
| "将食品杂货预算设置为 700 美元" | 更新 `budgets.json` |
| "我的餐饮预算还剩多少？" | 计算当前月份的预算余额 |
| "显示上周的所有开支" | 根据日期范围查询并显示详细信息 |
| "我这个月最大的开支是什么？" | 查询并按金额排序 |
| "取消上一笔开支" | 从账本中删除最近的记录 |
| "昨天在 Starbucks 花了 5.50 美元" | 根据日期记录开支 |
| "兽医费用是 280 美元" | 记录为宠物类别 |
| "汽车保险费用是 180 美元" | 记录为保险类别 |
| "我在 Target 花了大约 50 美元" | 记录 50 美元并确认金额 |
| "我从工作单位收到了 45 美元的退款" | 记录为负数（退款） |
| "我这个月在食品杂货上花了多少钱？" | 查询食品杂货和餐饮类别的开支 |
| "比较这个月和上个月的开支" | 生成环比数据 |

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

### 账本条目（expenses/ledger.json）

```json
[
  {
    "id": 1,
    "amount": 45.00,
    "category": "Groceries",
    "vendor": "Costco",
    "date": "2026-02-17",
    "notes": "",
    "created_at": "2026-02-17T23:32:00Z"
  },
  {
    "id": 2,
    "amount": -35.00,
    "category": "Shopping",
    "vendor": "Amazon",
    "date": "2026-02-17",
    "notes": "refund for headphones",
    "created_at": "2026-02-17T23:45:00Z"
  }
]
```

### 关键规则
- **ID**：递增的整数，不得重复使用
- **金额**：始终使用数字。正数表示开支，负数表示退款
- **日期**：ISO 8601 格式的日期（YYYY-MM-DD）
- **类别**：必须与 `references/categories.json` 中的名称匹配
- **created_at**：条目创建时的 UTC 时间戳

---

## 10. 脚本参考

所有脚本位于 `skills/expense-tracker/scripts/` 目录下，需要使用 `bash` 命令执行：

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
- `金额` — 数字（退款时使用负数）
- **类别**：`categories.json` 中的类别名称
- **商家**：商家名称
- **日期**：YYYY-MM-DD 格式（默认为今天）
- **备注**：可选的描述信息

**query.sh** `[--from DATE] [--to DATE] [--category CAT] [--vendor TEXT] [--format FMT]`
- `--from`：起始日期（包含当天）
- `--to`：结束日期（包含当天）
- `--category`：按类别名称过滤
- `--vendor`：按商家名称过滤（部分匹配，不区分大小写）
- `--format`：`summary`（默认）、`detail` 或 `json`

**budget-check.sh** `[YYYY-MM]`
- 可选参数：月份（默认为当前月份）
- 出错代码 0 表示一切正常；出错代码 1 表示至少有一个类别的支出超过了预算阈值（80%）