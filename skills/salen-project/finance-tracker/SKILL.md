# Finance Tracker v2.0

这是一个功能齐全的个人财务管理工具，支持费用追踪、定期订阅管理、储蓄目标设定、多货币支持以及智能数据分析。

## 安装

```bash
clawdhub install finance-tracker
```

或者将程序添加到系统的 `PATH` 环境变量中：
```bash
export PATH="$PATH:/path/to/finance-tracker/bin"
```

## 快速入门

```bash
# Log an expense
finance add 50k "lunch at cafe"

# Log with currency conversion
finance add $20 "online purchase"

# See what you spent
finance report week

# Get smart insights
finance insights
```

---

## 核心命令

### 添加费用

```bash
finance add <amount> "<description>"
```

**金额格式：**
- `50000` — 纯数字形式
- `50k` — 带有 “k” 后缀（表示 50,000）
- `$50` — 美元，会自动转换为你的本地货币
- `€100` — 欧元
- `100 USD` — 明确指定货币

**示例：**
```bash
finance add 50000 "lunch"
finance add 50k "groceries"
finance add $25 "Netflix subscription"
```

### 撤销与编辑

```bash
# Remove last transaction
finance undo

# Edit a transaction
finance edit <id> --amount=60000
finance edit <id> --desc="dinner with friends"
finance edit <id> --category=food

# Delete specific transaction
finance delete <id>
```

### 查看与搜索

```bash
finance report [period]    # today, week, month, year, all
finance recent [n]         # last n transactions
finance search "food"      # search by keyword
```

---

## 🔄 定期费用

用于追踪自动重复发生的订阅费用和账单。

### 添加定期费用

```bash
finance recurring add <amount> "<description>" <frequency> [--day=N]
```

**频率选项：** 每日、每周、每两周、每月、每季度、每年

**示例：**
```bash
finance recurring add 110k "mobile provider" monthly --day=1
finance recurring add 50k "Netflix" monthly
finance recurring add 200k "gym membership" monthly --day=15
```

### 管理定期费用

```bash
finance recurring              # List all
finance recurring list         # Same as above
finance recurring due          # Show what's due today
finance recurring process      # Auto-log all due expenses
finance recurring remove <id>  # Deactivate
```

### 工作原理：

- 定期费用会自动记录下一次的到期日期。
- 系统会每天（或按设定的时间间隔）运行 `finance recurring process` 命令来自动记录这些费用。
- 每笔记录的费用都会显示在常规交易记录中。
- 每月的费用总额会汇总在定期费用报告中。

---

## 🎯 储蓄目标

帮助你设定财务目标并跟踪进度。

### 添加储蓄目标

```bash
finance goal add "<name>" <target> [--by=DATE] [--current=X]
```

**示例：**
```bash
finance goal add "New Laptop" 5000000 --by=2026-06-01
finance goal add "Emergency Fund" 10000000
finance goal add "Vacation" 3000000 --by=2026-08-01 --current=500000
```

### 跟踪进度

```bash
# Add to goal (increment)
finance goal update "Laptop" 500k

# Set exact amount
finance goal set "Laptop" 2000000

# View all goals
finance goal
finance goal list
```

### 目标功能：
- **截止日期提醒**：显示距离目标还剩多少天
- **每日/每周/每月目标**：显示为达成目标需要每天/每周节省多少金额
- **优先级设置**：高、中、低
- **达成目标奖励**：达成目标时会有提示！

---

## 💱 多货币支持

支持自动根据实时汇率进行货币转换。

### 查看汇率

```bash
finance rates              # Show all common rates
finance rates USD          # Specific currency rate
finance rates EUR
```

### 货币转换

```bash
finance convert 100 USD UZS
finance convert 50 EUR USD
```

### 在费用记录中自动转换货币

```bash
# These auto-convert to your default currency (UZS)
finance add $50 "Amazon purchase"
finance add €30 "App subscription"
finance add 100 USD "Online course"
```

### 设置默认货币

```bash
finance currency         # Show current
finance currency USD     # Change default
```

**汇率更新：** 每 6 小时自动更新一次汇率。

---

## 💡 智能数据分析

利用人工智能提供消费分析和建议。

```bash
finance insights    # Full insights report
finance summary     # Quick daily summary
finance digest      # Weekly digest
```

### 数据展示内容：
- **消费速度**：每日/每周/每月的消费平均值
- **周期对比**：本周与上周的对比情况
- **类别变化**：哪些类别的消费金额有所增减
- **异常检测**：标记出异常高的支出
- **目标进度**：显示每天需要节省的金额
- **到期提醒**：提醒你哪些订阅费用今天到期

### 示例输出

```
💡 Smart Insights
━━━━━━━━━━━━━━━━━━━━━

📈 Spending Velocity
   Daily avg: 85,000 UZS
   This month so far: 1,200,000 UZS
   Projected month total: 2,550,000 UZS

📊 This Week vs Last Week
   📈 Spending UP 23%
   This week: 595,000 UZS
   Last week: 484,000 UZS

🏷️ Notable Category Changes
   🍔 food: ↑ 45%
   🚗 transport: ↓ 20%

⚠️ Alerts
   • Unusually large expense: 350,000 on electronics

🎯 Savings Goals
   Need to save: 50,000 UZS/day
   Next deadline: Laptop in 45 days
```

---

## 收入与资产

### 记录收入

```bash
finance income 5000000 "salary"
finance income 500k "freelance project"
```

系统会自动识别收入类型：工资、自由职业收入、商业收入、投资收益、礼物收入

### 管理资产

```bash
finance asset add "Bank Account" 10000000 cash
finance asset add "Stocks" 5000000 stocks
finance asset add "Bitcoin" 2000000 crypto
finance asset remove "Old Account"
finance asset list
finance portfolio          # Net worth summary
```

资产类型包括：现金、股票、加密货币、房地产、储蓄、投资

---

## 分析功能

### 预算检查

```bash
finance budget 100k
```

显示：
- 当天的支出与预算的对比情况
- 本周的支出与每周预算的对比（每天显示 7 次）
- 剩余金额
- 超支警告

---

## 费用分类

系统会根据费用描述自动分类：

| 分类 | 关键词 |
|----------|----------|
| 🍔 食物 | 午餐、晚餐、咖啡馆、餐厅、食品杂货 |
| 🚗 交通 | 出租车、优步、公交车、地铁、燃油费用 |
| 🛍️ 购物 | 衣服、鞋子、购物费用 |
| 📱 科技产品 | 手机、笔记本电脑、耳机 |
| 🎮 娱乐 | 电影、游戏、Netflix、Spotify |
| 📚 教育 | 书籍、课程、学费 |
| 💊 健康 | 药品、药店、医生费用、健身费用 |
| 🏠 房产 | 租金、水电费、家具费用、网络费用 |
| 💇 个人消费 | 理发、美发、沙龙费用 |
| 🎁 礼物 | 赠品 |
| ✈️ 旅行 | 旅行费用、机票、酒店费用 |
| 🔄 定期订阅 | 定期支付的订阅服务 |

---

## 数据存储

所有数据都存储在本地目录 `~/.finance-tracker/` 中：

```
~/.finance-tracker/
├── transactions.json     # All expenses
├── FINANCE_LOG.md        # Human-readable log
├── portfolio.json        # Assets
├── income.json           # Income records
├── recurring.json        # Recurring expenses
├── goals.json            # Savings goals
└── exchange_rates.json   # Cached rates
```

## 数据导出

```bash
finance export csv
finance export json
```

---

## Telegram 集成

为了方便在聊天中快速记录费用，可以使用以下 Telegram 脚本：

```
"spent 50k lunch" → finance add 50000 "lunch"
"taxi 15k"        → finance add 15000 "taxi"
"coffee 8k"       → finance add 8000 "coffee"
```

### 自动处理集成

你还可以将 Finance Tracker 的配置添加到你的 HEARTBEAT.md 文件中，以实现自动化处理：

```markdown
## Finance (daily)
- Run: finance recurring process
- Run: finance summary
```

---

## 完整命令参考

```
EXPENSES:
  finance add <amt> "<desc>"        Log expense
  finance undo                      Remove last
  finance edit <id> [--amount=X]    Edit transaction
  finance delete <id>               Delete transaction
  finance report [period]           Spending report
  finance recent [n]                Recent transactions
  finance search "<query>"          Search

RECURRING:
  finance recurring                 List all
  finance recurring add ...         Add subscription
  finance recurring remove <id>     Remove
  finance recurring process         Log due items
  finance recurring due             Show due today

GOALS:
  finance goal                      List goals
  finance goal add "<name>" <target> [--by=DATE]
  finance goal update "<name>" <amt>
  finance goal set "<name>" <amt>
  finance goal remove "<name>"

CURRENCY:
  finance rates [currency]          Exchange rates
  finance convert <amt> <from> <to>
  finance currency [code]           Get/set currency

INCOME & ASSETS:
  finance income <amt> "<desc>"
  finance asset add/remove/list
  finance portfolio

ANALYSIS:
  finance insights                  Smart analysis
  finance summary                   Daily summary
  finance digest                    Weekly digest
  finance trends [days]
  finance compare [days]
  finance budget <daily>

OTHER:
  finance categories
  finance export [csv|json]
  finance help
```

---

## 使用技巧：
1. 使用 “k” 表示千位数（例如：`50k` 比 `50000` 更简洁）
2. 使用货币前缀（如 `$50`）可自动进行货币转换
3. 每天运行 `finance recurring process` 命令来自动记录定期费用
4. 运行 `finance digest` 命令获取每周的消费总结
5. 达成储蓄目标时及时更新目标
6. 运行 `finance budget 100k` 命令来监控预算执行情况

---

本软件由 Salen 开发。