---
name: wallet-api
description: 与 BudgetBakers 钱包 API 交互以获取个人财务数据。当用户需要通过 REST API 从他们的钱包应用程序中查询账户、类别、交易记录、预算或模板时，可以使用此功能。需要设置 WALLET_API_TOKEN 环境变量。
---
# 钱包API技能

用于与BudgetBakers的钱包个人财务API进行交互。

## 先决条件

1. 需要订阅**高级钱包计划**才能使用API。
2. 从[web.budgetbakers.com/settings/apiTokens](https://web.budgetbakers.com/settings/apiTokens)获取**API令牌**。
3. 设置`WALLET_API_TOKEN`环境变量。

## 快速入门

```bash
export WALLET_API_TOKEN="your_token_here"
./scripts/wallet-api.sh me
```

## API参考

请参阅[references/api-reference.md]，以了解以下内容：
- 认证详情
- 速率限制（每小时500次请求）
- 查询过滤语法（文本和范围过滤）
- 分页参数
- 数据同步行为
- 代理提示

## 可用命令

| 命令 | 描述 |
|---------|-------------|
| `me` | 当前用户信息 |
| `accounts` | 列出账户 |
| `categories` | 列出类别 |
| `records` | 列出交易记录 |
| `budgets` | 列出预算 |
| `templates` | 列出模板 |

## 查询参数

所有列表端点支持以下参数：
- `limit`（默认值：30，最大值：100）
- `offset`（默认值：0）

### 过滤示例

**最近的交易记录：**
```bash
./wallet-api.sh records "recordDate=gte.2025-02-01&limit=50"
```

**金额范围：**
```bash
./wallet-api.sh records "amount=gte.100&amount=lte.500"
```

**文本搜索：**
```bash
./wallet-api.sh records "note=contains-i.grocery"
```

**类别 + 日期：**
```bash
./wallet-api.sh records "categoryId=eq.<id>&recordDate=gte.2025-01-01"
```

### 过滤前缀

| 前缀 | 含义 |
|--------|---------|
| `eq.` | 完全匹配 |
| `contains.` | 包含（区分大小写） |
| `contains-i.` | 包含（不区分大小写） |
| `gt.` | 大于 |
| `gte.` | 大于或等于 |
| `lt.` | 小于 |
| `lte.` | 小于或等于 |

## 常见工作流程

### 获取账户余额
```bash
./wallet-api.sh accounts
```

### 列出组织的类别
```bash
./wallet-api.sh categories
```

### 最近的支出记录
```bash
./wallet-api.sh records "recordDate=gte.2025-02-01&limit=100"
```

### 按收款人过滤
```bash
./wallet-api.sh records "payee=contains-i.amazon"
```

## 数据同步注意事项

- 初始同步时可能会返回409 Conflict错误——请等待并重试。
- 应用程序的最新更改可能不会立即显示。
- 请查看`X-Last-Data-Change-At`头部字段以确认数据是否是最新的。

## 速率限制处理

- 当每小时请求次数超过500次时，会收到`429 Too Many Requests`错误。
- 请关注`X-RateLimit-Remaining`头部字段以了解剩余的请求次数。
- 为防止速率限制问题，请设置`agentHints=true`。