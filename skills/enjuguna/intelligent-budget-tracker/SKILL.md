---
name: agent-money-tracker
description: 专为AI代理设计的智能预算跟踪与财务管理库：支持费用追踪、收入管理、预算制定、储蓄目标设定，以及利用大型语言模型（LLM）提供的数据分析与洞察功能。
---

# 代理资金追踪器（Agent Money Tracker）

这是一个TypeScript库，专为AI代理设计，用于追踪开支、收入、预算以及储蓄目标。该库利用基于LLM（Large Language Model）的自然语言处理技术来实现这些功能。**无需前端界面**，专为代理和机器人程序化使用而设计。

## 安装

```bash
npm install agent-money-tracker
```

---

## 使用方法

### 初始化预算追踪器

```typescript
import { clawhub } from 'agent-money-tracker';

// Initialize (required before any operations)
await clawhub.initialize();

// Or with custom storage path
await clawhub.initialize('/path/to/data');
```

### 花费追踪

```typescript
// Add an expense
await clawhub.addExpense(50, 'Food & Dining', 'Grocery shopping', {
  date: '2026-01-31',
  tags: ['weekly', 'essentials'],
  merchant: 'Whole Foods'
});

// Natural language input
await clawhub.addFromNaturalLanguage('spent $45 on uber yesterday');

// Get recent expenses
const expenses = clawhub.getExpenses({ limit: 10 });

// Filter by category and date range
const foodExpenses = clawhub.getExpenses({
  category: 'Food & Dining',
  startDate: '2026-01-01',
  endDate: '2026-01-31'
});
```

### 收入追踪

```typescript
// Add income
await clawhub.addIncome(5000, 'Salary', 'January salary', {
  date: '2026-01-15'
});

// Add freelance income
await clawhub.addIncome(500, 'Freelance', 'Website project');

// Get all income
const income = clawhub.getIncome();
```

### 预算管理

```typescript
// Create a monthly budget
await clawhub.createBudget('Food Budget', 'Food & Dining', 500, 'monthly', 0.8);

// Check budget status
const status = clawhub.getBudgetStatus();
// Returns: [{ budgetName, spent, limit, remaining, percentageUsed, status }]

// Get budget alerts
const alerts = clawhub.checkBudgetAlerts();
// Returns warnings when threshold or limit exceeded

// Get smart budget suggestions
const suggestions = clawhub.suggestBudgetLimits();
// Returns: [{ category, suggested, average, max }]
```

### 储蓄目标

```typescript
// Create a savings goal
await clawhub.createGoal('Emergency Fund', 10000, {
  description: '6 months expenses',
  deadline: '2026-12-31',
  priority: 'high'
});

// Add contribution
await clawhub.contributeToGoal('goal_abc123', 500, 'January savings');

// Check progress
const progress = clawhub.getGoalProgress();
// Returns: [{ goalName, targetAmount, currentAmount, percentageComplete, daysRemaining, onTrack }]
```

### 分析与报告

```typescript
// Monthly spending summary
const summary = clawhub.getSpendingSummary();
// Returns: { totalExpenses, totalIncome, netSavings, expensesByCategory, incomeByCategory }

// View monthly trends
const trends = clawhub.getMonthlyTrends(12);
// Returns: [{ date, expenses, income, netSavings }]

// Full monthly report
const report = clawhub.generateMonthlyReport(2026, 1);

// Compare to last month
const comparison = clawhub.compareToLastMonth();
// Returns: { expenseChange, incomeChange, topIncreases, topDecreases }
```

### 智能洞察

```typescript
// Generate AI-powered insights
const insights = await clawhub.generateInsights();
// Returns insights like:
// - "⚠️ Your dining expenses are 3x higher than usual"
// - "💡 Cancel unused subscriptions to save $50/month"
// - "🏆 You've tracked expenses for 7 consecutive days!"

// Get unread insights
const unreadInsights = clawhub.getInsights();
```

### 定期交易

```typescript
// Create recurring expense (e.g., Netflix subscription)
await clawhub.createRecurring(
  'expense', 15.99, 'Subscriptions', 'Netflix', 'monthly',
  { startDate: '2026-02-01' }
);

// Create recurring income (e.g., salary)
await clawhub.createRecurring(
  'income', 5000, 'Salary', 'Monthly salary', 'monthly'
);

// Process due recurring transactions
await clawhub.processRecurring();
```

### 数据管理

```typescript
// Get statistics
const stats = clawhub.getStats();
// Returns: { totalTransactions, totalExpenses, totalIncome, netSavings, avgExpense, topCategory }

// Get available categories
const categories = clawhub.getCategories();

// Export data
const jsonData = await clawhub.exportData();

// Create backup
const backupPath = await clawhub.backup();

// Get storage location
const dataPath = clawhub.getDataPath();
```

---

## 默认分类

### 花费分类
| 分类 | 图标 |
|------|------|
| 食物与餐饮 | 🍔 |
| 交通 | 🚗 |
| 购物 | 🛍️ |
| 账单与公用事业 | 💡 |
| 娱乐 | 🎬 |
| 健康与健身 | 💪 |
| 教育 | 📚 |
| 个人护理 | 💄 |
| 订阅服务 | 📱 |

### 收入分类
| 分类 | 图标 |
|------|------|
| 工资 | 💰 |
| 自由职业收入 | 💻 |
| 投资 | 📈 |
| 礼物 | 🎁 |

---

## 跨平台数据存储

数据存储在各个平台特定的位置：

| 平台 | 默认路径 |
|------|-------------|
| Windows | `%APPDATA%\clawhub` |
| macOS | `~/Library/Application Support/clawhub` |
| Linux | `~/.local/share/clawhub` |

可以通过环境变量进行自定义配置：
```bash
export CLAWHUB_DATA_PATH=/custom/path
```

---

## API参考摘要

| 方法 | 描述 |
|--------|-------------|
| `initialize(path?)` | 初始化预算追踪器 |
| `addExpense(amount, category, description, options?)` | 添加支出记录 |
| `addIncome(amount, category, description, options?)` | 添加收入记录 |
| `addFromNaturalLanguage(text)` | 从自然语言文本中解析并添加数据 |
| `createBudget(name, category, limit, period, threshold?)` | 创建预算 |
| `getBudgetStatus()` | 获取所有预算状态 |
| `checkBudgetAlerts()` | 获取预算警告/提醒 |
| `createGoal(name, target, options?)` | 创建储蓄目标 |
| `contributeToGoal(goalId, amount, note?)` | 为储蓄目标添加支出记录 |
| `getGoalProgress()` | 获取储蓄目标的进度 |
| `getSpendingSummary(start?, end?)` | 获取支出明细 |
| `getMonthlyTrends(months?)` | 获取每月趋势数据 |
| `generateMonthlyReport(year?, month?)` | 生成月度报告 |
| `generateInsights()` | 生成智能分析报告 |
| `createRecurring(type, amount, category, desc, freq, options?)` | 创建定期交易记录 |
| `processRecurring()` | 处理到期的定期交易 |
| `getStats()` | 获取交易统计数据 |
| `exportData()` | 将所有数据导出为JSON格式 |
| `backup()` | 创建带时间戳的备份文件 |