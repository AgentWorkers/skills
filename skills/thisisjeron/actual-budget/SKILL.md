---
name: actual-budget
description: 通过官方的 Actual Budget Node.js API 查询和管理个人财务。该 API 可用于预算查询、交易导入/导出、账户管理、分类设置、规则配置、日程安排，以及与自托管的 Actual Budget 实例进行银行数据同步。
---

# Actual Budget API

这是 [Actual Budget](https://actualbudget.org) 的官方 Node.js API。该 API 以无头模式运行，可以处理从服务器同步的本地预算数据。

## 安装

```bash
npm install @actual-app/api
```

## 环境变量

| 变量        | 是否必填 | 说明                          |
|------------|---------|-----------------------------------------|
| `ACTUAL_SERVER_URL` | 是       | 服务器地址（例如：`https://actual.example.com`）         |
| `ACTUAL_PASSWORD` | 是       | 服务器密码                         |
| `ACTUALSYNC_ID` | 是       | 预算同步 ID（在“设置” → “高级” → “同步 ID”中设置）     |
| `ACTUAL_DATA_DIR` | 否       | 本地预算数据缓存目录（默认为当前工作目录）         |
| `ACTUAL_ENCRYPTION_PASSWORD` | 否       | 如果启用了端到端加密，则需要此密码           |
| `NODE_EXTRA_CA_CERTS` | 否       | 自签名证书的 CA 证书文件路径                 |

### 自签名证书

如果您的 Actual Budget 服务器使用自签名证书：

1. **建议做法：** 将该 CA 证书添加到系统的信任存储中；
2. **替代方案：** 设置 `NODE_EXTRA_CA_CERTS=/path/to/your-ca.pem` 以信任特定的 CA 证书。

**注意：** 避免完全禁用 TLS 验证，否则会面临中间人攻击的风险。

## 快速入门

```javascript
const api = require('@actual-app/api');

await api.init({
  dataDir: process.env.ACTUAL_DATA_DIR || '/tmp/actual-cache',
  serverURL: process.env.ACTUAL_SERVER_URL,
  password: process.env.ACTUAL_PASSWORD,
});

await api.downloadBudget(
  process.env.ACTUAL_SYNC_ID,
  process.env.ACTUAL_ENCRYPTION_PASSWORD ? { password: process.env.ACTUAL_ENCRYPTION_PASSWORD } : undefined
);

// ... do work ...

await api.shutdown();
```

## 核心概念

- **金额** 以分为单位（整数形式）：`$50.00` 表示 5000 分，`-1200` 表示 12 美元的支出；
- **日期** 使用 `YYYY-MM-DD` 格式，月份使用 `YYYY-MM` 格式；
- **ID** 为 UUID；可以使用 `getIDByName(type, name)` 根据名称查找相应的 ID；
- 可以使用 `api.utils.amountToInteger(123.45)` 将字符串 `123.45` 转换为整数 `12345`。

## 常见操作

### 获取预算概览
```javascript
const months = await api.getBudgetMonths();        // ['2026-01', '2026-02', ...]
const jan = await api.getBudgetMonth('2026-01');   // { categoryGroups, incomeAvailable, ... }
```

### 账户
```javascript
const accounts = await api.getAccounts();
const balance = await api.getAccountBalance(accountId);
const newId = await api.createAccount({ name: 'Checking', type: 'checking' }, 50000); // $500 initial
await api.closeAccount(id, transferToAccountId);  // transfer remaining balance
```

### 交易
```javascript
// Get transactions for date range
const txns = await api.getTransactions(accountId, '2026-01-01', '2026-01-31');

// Import with deduplication + rules (preferred for bank imports)
const { added, updated } = await api.importTransactions(accountId, [
  { date: '2026-01-15', amount: -2500, payee_name: 'Grocery Store', notes: 'Weekly run' },
  { date: '2026-01-16', amount: -1200, payee_name: 'Coffee Shop', imported_id: 'bank-123' },
]);

// Update a transaction
await api.updateTransaction(txnId, { category: categoryId, cleared: true });
```

### 类别与收款人
```javascript
const categories = await api.getCategories();
const groups = await api.getCategoryGroups();
const payees = await api.getPayees();

// Create
const catId = await api.createCategory({ name: 'Subscriptions', group_id: groupId });
const payeeId = await api.createPayee({ name: 'Netflix', category: catId });
```

### 预算金额
```javascript
await api.setBudgetAmount('2026-01', categoryId, 30000);  // budget $300
await api.setBudgetCarryover('2026-01', categoryId, true);
```

### 规则
```javascript
const rules = await api.getRules();
await api.createRule({
  stage: 'pre',
  conditionsOp: 'and',
  conditions: [{ field: 'payee', op: 'is', value: payeeId }],
  actions: [{ op: 'set', field: 'category', value: categoryId }],
});
```

### 时间表
```javascript
const schedules = await api.getSchedules();
await api.createSchedule({
  payee: payeeId,
  account: accountId,
  amount: -1500,
  date: { frequency: 'monthly', start: '2026-01-01', interval: 1, endMode: 'never' },
});
```

### 银行同步
```javascript
await api.runBankSync({ accountId });  // GoCardless/SimpleFIN
```

### 同步与关闭
```javascript
await api.sync();      // push/pull changes to server
await api.shutdown();  // always call when done
```

## ActualQL 查询

对于复杂的查询，可以使用 ActualQL：

```javascript
const { q, runQuery } = require('@actual-app/api');

// Sum expenses by category this month
const { data } = await runQuery(
  q('transactions')
    .filter({
      date: [{ $gte: '2026-01-01' }, { $lte: '2026-01-31' }],
      amount: { $lt: 0 },
    })
    .groupBy('category.name')
    .select(['category.name', { total: { $sum: '$amount' } }])
);

// Search transactions
const { data } = await runQuery(
  q('transactions')
    .filter({ 'payee.name': { $like: '%grocery%' } })
    .select(['date', 'amount', 'payee.name', 'category.name'])
    .orderBy({ date: 'desc' })
    .limit(20)
);
```

**运算符：** `$eq`、`$lt`、`$lte`、`$gt`、`$gte`、`$ne`、`$oneof`、`$regex`、`$like`、`$notlike`
**分组方式：** `.options({ splits: 'inline' | 'grouped' | 'all' })`

## 辅助函数
```javascript
// Look up ID by name
const acctId = await api.getIDByName('accounts', 'Checking');
const catId = await api.getIDByName('categories', 'Food');
const payeeId = await api.getIDByName('payees', 'Amazon');

// List budgets
const budgets = await api.getBudgets();  // local + remote files
```

## 转账

转账操作会使用特定的收款人信息。可以通过 `transfer_acct` 字段来查找转账的收款人：
```javascript
const payees = await api.getPayees();
const transferPayee = payees.find(p => p.transfer_acct === targetAccountId);
await api.importTransactions(fromAccountId, [
  { date: '2026-01-15', amount: -10000, payee: transferPayee.id }
]);
```

## 分组交易
```javascript
await api.importTransactions(accountId, [{
  date: '2026-01-15',
  amount: -5000,
  payee_name: 'Costco',
  subtransactions: [
    { amount: -3000, category: groceryCatId },
    { amount: -2000, category: householdCatId },
  ]
}]);
```

## 批量导入（新预算数据）

用于从其他应用程序迁移数据：
```javascript
await api.runImport('My-New-Budget', async () => {
  for (const acct of myData.accounts) {
    const id = await api.createAccount(acct);
    await api.addTransactions(id, myData.transactions.filter(t => t.acctId === id));
  }
});
```

## 参考文档

- 官方 API 文档：https://actualbudget.org/docs/api/reference
- ActualQL 文档：https://actualbudget.org/docs/api/actual-ql