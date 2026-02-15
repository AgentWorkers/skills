---
name: agentledger
description: **AI代理的费用追踪与会计管理功能**  
支持记录购买信息、设定预算、生成支出报告以及管理多币种财务数据——所有数据均存储在本地。支持导入Privacy.com卡的交易记录，支持自然语言查询，支持CSV/JSON格式的数据导出。适用于需要为代理的购买行为生成财务审计追踪的情况。
metadata: {"openclaw": {"requires": {"bins": ["node"]}}}
---

# AgentLedger - 人工智能代理费用追踪系统

## 概述
AgentLedger 是一款会计工具，它可以记录您的每一笔交易，跟踪多个账户的支出情况，并提供详细的报告。使用该工具可以帮助您维护完整的财务记录。

**重要提示**：请在购买后立即记录交易。该工具专为人工智能代理设计，用于追踪其自身的费用（如 API 使用费用、工具订阅费用等）。

## 核心功能

### 1. 记录交易
每当您进行任何购买时，请立即记录该交易：
```javascript
// In Node.js context, require the ledger
const AgentLedger = require('./src/ledger.js');
const ledger = new AgentLedger();

// Log a transaction
await ledger.logTransaction({
  amount: 29.99,
  currency: 'USD',
  vendor: 'OpenAI',
  description: 'GPT-4 API credits',
  category: 'API/Services',
  account: 'privacy-card-1',
  context: 'Needed additional tokens for user project analysis',
  receiptUrl: 'https://platform.openai.com/receipts/xyz',
  confirmationId: 'sub_1234567890'
});
```

**命令行接口（CLI）用法**（支持位置参数和命名参数）：
```bash
# Positional style
node src/cli.js log 29.99 "OpenAI" "GPT-4 API credits" --category="API/Services"

# Named parameter style  
node src/cli.js log --amount=29.99 --vendor="OpenAI" --description="GPT-4 API credits" --category="API/Services" --context="Monthly API refill"
```

### 2. 查看当前支出
```javascript
// Get spending summary
const summary = await ledger.getSummary('this-month');
console.log(`Total spent this month: $${summary.total}`);

// Check specific category
const apiSpending = await ledger.getCategorySpending('API/Services', 'this-month');
```

### 3. 生成报告
```javascript
// Monthly report
const report = await ledger.generateReport('monthly', { month: '2024-01' });

// Custom date range
const customReport = await ledger.generateReport('custom', {
  startDate: '2024-01-01',
  endDate: '2024-01-31'
});
```

### 4. 预算管理
```javascript
// Set monthly budget for API services
await ledger.setBudget('API/Services', 500, 'monthly');

// Check budget status
const budgetStatus = await ledger.checkBudget('API/Services');
if (budgetStatus.isNearLimit) {
  console.log(`Warning: ${budgetStatus.percentUsed}% of API budget used`);
}
```

## 分类
请使用以下预定义的分类来进行一致的支出记录：
- **API/服务**：API 使用费用、SaaS 订阅费用
- **基础设施**：托管服务、域名费用、CDN 费用
- **营销**：广告费用、社交媒体工具费用
- **工具**：软件许可证费用、实用工具费用
- **订阅服务**：按月/每年自动续费的订阅服务
- **其他**：其他杂项费用

## 账户集成
如果您的账户使用了 Privacy.com 卡，该系统会自动检测相关交易数据：
```javascript
// If you have Privacy.com JSON exports in workspace/privacy/
await ledger.importPrivacyTransactions('./privacy/card-1.json');
```

### 手动账户设置
```javascript
// Register a new payment method
await ledger.addAccount({
  id: 'stripe-main',
  name: 'Main Stripe Account',
  type: 'credit_card',
  currency: 'USD'
});
```

## 自然语言查询
您可以提出如下问题：
- “我这个月花了多少钱在 API 密钥上？”
- “昨天那笔 20 美元的费用是什么？”
- “显示上个季度的所有基础设施费用”
- “我的营销支出是否超出了预算？”

CLI 可以处理这些查询：
```bash
node src/cli.js query "API spending this month"
node src/cli.js find "OpenAI" --last-week
```

## 时间范围
支持以下自然语言时间范围：
- `today`（今天）
- `yesterday`（昨天）
- `this-week`（本周）
- `last-week`（上周）
- `this-month`（本月）
- `last-month`（上个月）
- `this-quarter`（本季度）
- `last-quarter`（上季度）
- `this-year`（今年）
- `last-year`（去年）
- `last-30-days`（过去 30 天）
- `last-90-days`（过去 90 天）

## 数据导出
```javascript
// Export to CSV
await ledger.exportTransactions('csv', './exports/transactions.csv');

// Export to JSON
await ledger.exportTransactions('json', './exports/transactions.json');
```

## CLI 快速参考
以下是人工智能代理需要掌握的基本命令：
```bash
# Initialize (run once)
node src/cli.js init

# Log transactions (supports both styles)
node src/cli.js log 29.99 "OpenAI" "API credits" --category="API/Services"
node src/cli.js log --amount=29.99 --vendor="OpenAI" --description="API credits" --category="API/Services"

# Check current spending
node src/cli.js summary                    # This month
node src/cli.js summary --period="today"   # Today only
node src/cli.js summary --period="this-week" # This week

# Set and check budgets
node src/cli.js budget set "API/Services" 500    # Set monthly budget
node src/cli.js budget status                    # Check all budgets

# Generate detailed reports  
node src/cli.js report monthly
node src/cli.js report --type=category
node src/cli.js report --type=vendor

# Search transactions
node src/cli.js find "OpenAI"                    # Search by vendor
node src/cli.js find "API" --category="API/Services"  # Search by category
node src/cli.js find --min-amount=50             # Find large expenses

# Export data
node src/cli.js export csv                       # Export to CSV
node src/cli.js export --format=json            # Export to JSON

# Natural language queries
node src/cli.js query "How much did I spend on APIs this month?"
node src/cli.js query "What was that $25 charge?"

# Import from Privacy.com
node src/cli.js import privacy ./privacy-export.json
```

## 文件存储
- 交易记录：`workspace/ledger/transactions.json`
- 账户信息：`workspace/ledger/accounts.json`
- 预算信息：`workspace/ledger/budgets.json`
- 设置信息：`workspace/ledger/settings.json`

## 最佳实践
1. **立即记录**：不要拖延，购买发生时立即记录交易。
2. **提供背景信息**：说明购买的原因。
3. **使用统一的分类**：遵循预定义的分类标准。
4. **保存收据**：存储交易确认编号和收据链接。
5. **设置预算**：为每个类别设定支出上限。
6. **定期审查**：定期生成报告以监控支出情况。

## 错误处理与特殊情况
该系统能够优雅地处理常见错误：

### 输入验证
- **负数金额**：会被拒绝（仅接受正数金额）。
- **缺少必填字段**：会显示带有使用示例的错误信息。
- **无效货币**：会被接受（不进行验证，假设用户知道自己在做什么）。
- **过长的描述**：会完整显示而不会被截断。

### 数据安全
- **自动备份**：每次保存数据前都会进行备份。
- **数据恢复**：可以从备份文件中自动恢复数据。
- **空时间段**：会显示 $0.00 的总额。
- **多货币支持**：在汇总和报告中会正确区分不同货币。

### 错误恢复示例
```bash
# If you see "Could not load transactions" message:
# The system automatically tries to recover from backup
# Your data should be restored automatically

# Manual backup check
ls workspace/ledger/*.backup  # Check if backups exist
```

## 安全性与隐私
- **仅存储在本地**：所有数据都保存在 `workspace/ledger/` 目录下的 JSON 文件中。
- **不使用外部 API**：核心功能可离线使用。
- **不存储敏感信息**：不会存储实际的卡号或密码。
- **账户别名**：使用描述性名称（如 `privacy-card-1` 或 `company-amex`）。
- **收据链接**：仅存储收据的链接，而不是收据内容本身。