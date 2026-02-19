---
name: expense-tracker
description: 在结构化的 Markdown 文件中记录每日开支，并按月份进行分类。适用于用户需要记录支出、查看支出汇总、分析支出模式或管理个人财务的情况。支持设置支出类别、标签以及生成月度支出报告的功能。
---
# 开支追踪器

使用 Markdown 文件按月份记录和追踪每日开支。

## 快速入门

### 记录开支

```bash
python3 scripts/log_expense.py log <amount> <category> [--description "text"] [--tags "tag1,tag2"] [--date YYYY-MM-DD]
```

示例：

```bash
# Simple expense
python3 scripts/log_expense.py log 45000 Coffee

# With description
python3 scripts/log_expense.py log 250000 Dining --description "Lunch with team"

# With tags
python3 scripts/log_expense.py log 500000 Shopping --tags "clothes,sale" --description "New shirt"

# Specify date (for backdating)
python3 scripts/log_expense.py log 1200000 Vehicle --description "Gas" --date 2026-02-15
```

### 查看月度汇总

```bash
# Current month
python3 scripts/log_expense.py summary

# Specific month
python3 scripts/log_expense.py summary 2026-02

# JSON output (for parsing)
python3 scripts/log_expense.py summary 2026-02 --json
```

## 文件组织结构

开支文件存储在工作区根目录下的 `expenses/` 目录中：

```
expenses/
├── 2026-01.md
├── 2026-02.md
└── 2026-03.md
```

每个文件都包含一个 Markdown 表格：

```markdown
# Expenses - 2026-02

| Date | Category | Amount (VND) | Description | Tags |
|------|----------|-------------|-------------|------|
| 2026-02-17 | Coffee | 45,000 | | |
| 2026-02-17 | Dining | 250,000 | Lunch with team | |
| 2026-02-17 | Shopping | 500,000 | New shirt | clothes,sale |
```

## 分类

请参阅 `references/categories.md` 以获取常见的开支分类。根据需要使用现有分类或创建自定义分类。

常见分类：
- **住房** - 租金、水电费、家居开支
- **车辆** - 油费、维护费用、停车费
- **餐饮** - 餐厅、外卖
- **咖啡** - 咖啡馆
- **购物** - 衣物、电子产品、其他日常购物
- **娱乐** - 电影、游戏、爱好
- **医疗保健** - 药费、看医生
- **订阅服务** - Netflix、Spotify、健身房、应用程序
- **储蓄** - 投资、应急资金
- **债务偿还** - 贷款、信用卡还款
- **其他** - 其他各类开支

## 工作流程示例

### 从对话中记录每日开支

当用户提到支出时：

```bash
# User: "Just paid 35k for coffee"
python3 scripts/log_expense.py log 35000 Coffee

# User: "Grabbed lunch for 120k at Phở 24"
python3 scripts/log_expense.py log 120000 Dining --description "Phở 24"

# User: "Filled up gas, 400k"
python3 scripts/log_expense.py log 400000 Vehicle --description "Gas"
```

### 月度回顾

```bash
# Get summary
python3 scripts/log_expense.py summary 2026-02

# Read the expense file to see details
cat expenses/2026-02.md
```

### 分析开支模式

```bash
# Get JSON for analysis
python3 scripts/log_expense.py summary 2026-02 --json

# Compare multiple months
python3 scripts/log_expense.py summary 2026-01 --json > jan.json
python3 scripts/log_expense.py summary 2026-02 --json > feb.json
```

## 提示

- **批量记录**：用户可以一次性告知多笔开支，系统会全部记录下来。
- **保持分类一致性**：使用相同的分类名称以便于生成准确的汇总。
- **使用标签进行筛选**：为子分类添加标签（例如 “工作”、“周末”、“紧急”）。
- **添加描述**：添加有助于日后识别开支的上下文信息。
- **定期回顾**：建议每月进行一次汇总，以追踪开支模式。

## 与财务目标的整合

在追踪开支时，请考虑以下几点：
- **预算管理**：将每月总支出与目标预算进行比较。
- **分析开支模式**：识别支出较高的类别。
- **应急资金**：跟踪储蓄进度。
- **债务管理**：监控债务偿还情况。
- **财务比率**：计算开支占收入的百分比。

## 脚本参考

### log_expense.py

**命令：**
- `log` - 添加一笔开支记录
- `summary` - 查看月度汇总

**log 命令的参数：**
- `amount` - 开支金额（单位：越南盾，必填）
- `category` - 分类名称（必填）
- `--description/-d` - 可选描述
- `--tags/-t` - 可选标签（用逗号分隔）
- `--date` - 可选日期（格式：YYYY-MM-DD，默认为今天）
- `--workspace` - 可选工作区路径（默认为 ~/.openclaw/workspace）

**summary 命令的参数：**
- `year_month` - 可选年份和月份（默认为当前月份）
- `--json` - 以 JSON 格式输出结果
- `--workspace` - 可选工作区路径

**输出结果：**
- 在 `expenses/` 目录中创建/更新 Markdown 文件。
- 显示文件位置及确认信息。
- 汇总显示总支出、开支数量及按类别的细分情况。