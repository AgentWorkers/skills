---
name: monarch-money
description: 这是一个用于 Monarch Money 预算管理的 TypeScript 库和命令行工具（CLI）。用户可以通过日期、商家或交易金额来搜索交易记录，更新支出类别，查看账户和预算信息，并管理用户认证。该工具适用于用户需要查询 Monarch Money 的交易记录、对支出进行分类、查找特定交易，或希望自动化预算管理任务的情况。
metadata:
  clawdbot:
    requires:
      env: ["MONARCH_EMAIL", "MONARCH_PASSWORD", "MONARCH_MFA_SECRET"]
    install:
      - id: node
        kind: node
        package: "."
        bins: ["monarch-money"]
        label: "Install Monarch Money CLI"
---

# Monarch Money

这是一个用于Monarch Money预算自动化的命令行界面（CLI）和TypeScript库。

## 先决条件

### 环境变量（必需）

| 变量 | 必需 | 描述 |
|----------|----------|-------------|
| `MONARCH_EMAIL` | **是** | Monarch Money账户的电子邮件地址 |
| `MONARCH_PASSWORD` | **是** | Monarch Money账户的密码 |
| `MONARCH_MFA_SECRET` | **是** | 多因素认证（MFA）的TOTP密钥（详见下文） |

### 获取MFA密钥

Monarch Money支持多因素认证（MFA）。请按照以下步骤生成TOTP密钥：

1. 登录至 https://app.monarchmoney.com
2. 转到“设置” > “安全” > “双因素认证”
3. 如果MFA已启用：先禁用它，然后再重新启用以获取新的密钥
4. 当系统显示二维码时，点击“无法扫描？查看设置密钥”
5. 复制该密钥（格式为base32字符串，例如 `JBSWY3DPEHPK3PXP`）
6. 使用认证应用程序完成Monarch Money中的MFA设置
7. 设置 `MONARCH_MFA_SECRET` 环境变量：`export MONARCH_MFA_SECRET="YOUR_SECRET"`

## 快速入门

```bash
# Check setup
monarch-money doctor

# Login (uses env vars by default)
monarch-money auth login

# List transactions
monarch-money tx list --limit 10

# List categories
monarch-money cat list
```

## CLI命令

### 认证

```bash
# Login with environment variables
monarch-money auth login

# Login with explicit credentials
monarch-money auth login -e email@example.com -p password --mfa-secret SECRET

# Check auth status
monarch-money auth status

# Logout
monarch-money auth logout
```

### 交易

```bash
# List recent transactions
monarch-money tx list --limit 20

# Search by date
monarch-money tx list --start-date 2026-01-01 --end-date 2026-01-31

# Search by merchant
monarch-money tx list --merchant "Walmart"

# Get transaction by ID
monarch-money tx get <transaction_id>

# Update category
monarch-money tx update <id> --category <category_id>

# Update merchant name
monarch-money tx update <id> --merchant "New Name"

# Add notes
monarch-money tx update <id> --notes "My notes here"
```

### 类别

```bash
# List all categories
monarch-money cat list

# List with IDs (for updates)
monarch-money cat list --show-ids
```

### 账户

```bash
# List accounts
monarch-money acc list

# Show account details
monarch-money acc get <account_id>
```

### 诊断工具（Doctor）

```bash
# Run diagnostic checks
monarch-money doctor
```

检查内容：
- 环境变量是否已设置
- API连接是否正常
- 会话是否有效
- Node.js版本是否正确

## 库的使用方法

直接导入并使用TypeScript库：

```typescript
import { MonarchClient } from 'monarch-money';

const client = new MonarchClient({ baseURL: 'https://api.monarch.com' });

// Login
await client.login({
  email: process.env.MONARCH_EMAIL,
  password: process.env.MONARCH_PASSWORD,
  mfaSecretKey: process.env.MONARCH_MFA_SECRET
});

// Get transactions
const transactions = await client.transactions.getTransactions({ limit: 10 });

// Get categories
const categories = await client.categories.getCategories();

// Get accounts
const accounts = await client.accounts.getAll();
```

## 常见工作流程

### 查找并更新交易记录

```bash
# 1. Find the transaction
monarch-money tx list --date 2026-01-15 --merchant "Target"

# 2. Get category ID
monarch-money cat list --show-ids

# 3. Update the transaction
monarch-money tx update <transaction_id> --category <category_id>
```

### 按日期范围搜索交易记录

```bash
monarch-money tx list --start-date 2026-01-01 --end-date 2026-01-31 --limit 100
```

### 检查预算状态

```bash
monarch-money acc list
```

## 错误处理

| 错误 | 解决方案 |
|-------|----------|
| “未登录” | 运行 `monarch-money auth login` 命令登录 |
| “需要MFA验证码” | 设置 `MONARCH_MFA_SECRET` 环境变量 |
| “凭据无效” | 在 app.monarchmoney.com 确认电子邮件/密码是否正确 |
| “会话过期” | 重新运行 `monarch-money auth login` 命令登录 |

## 会话管理

会话信息会缓存在本地文件 `~/.mm/session.json` 中。初次登录后，后续命令会重用已保存的会话以提高执行效率。

要清除会话信息：运行 `monarch-money auth logout` 命令。

## 参考资料

- [API.md](references/API.md) - GraphQL API的详细信息及高级用法
- [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) - 常见问题及解决方法