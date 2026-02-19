---
name: moneydevkit
description: 使用 moneydevkit，您可以在任何网站上接受付款。无论您是在构建一个用于销售商品的平台、添加结账/支付墙功能，还是将支付功能集成到 Next.js 或 Replit 应用程序中，moneydevkit 都能满足您的需求。该工具支持固定价格、按需付费的模式，同时能够处理产品、客户和订单信息。其底层技术基于 Bitcoin Lightning，支持全球范围内的支付，且无需银行账户即可使用。
metadata:
  openclaw:
    requires:
      env:
        - MDK_ACCESS_TOKEN
        - MDK_MNEMONIC
      bins:
        - npx
    optional:
      bins:
        - mcporter
    endpoints:
      - https://mcp.moneydevkit.com
      - https://docs.moneydevkit.com
---
# moneydevkit

您可以在5分钟内将支付功能添加到任何Web应用程序中。支持两种框架：Next.js和Replit（Express + Vite）。

## 工作流程

### 1. 获取凭证

**选项A — MCP：**

MCP服务器提供两种服务：
- **未认证**（`/mcp/`）——用于创建新账户和生成凭证
- **已认证**（`/mcp/account/`）——用于设置账户后的管理（需要OAuth）

创建新账户的步骤：
```
claude mcp add moneydevkit --transport http https://mcp.moneydevkit.com/mcp/
```

获取凭证后，切换到已认证的MCP界面以获得完整的账户控制权限：
```
claude mcp add moneydevkit --transport http https://mcp.moneydevkit.com/mcp/account/
```

**选项B — CLI：**
```bash
npx @moneydevkit/create
```

**选项C — 通过仪表板：**
在 [moneydevkit.com](https://moneydevkit.com) 注册并创建一个应用程序。

所有选项都会生成两个值：
- `MDK_ACCESS_TOKEN` — API密钥
- `MDK_MNEMONIC` — 钱包助记词

请将这两个值添加到 `.env` 文件中（或使用Replit的Secrets功能、Vercel的环境变量等）。这两个值都是必需的。

### 2. 选择框架并遵循其文档指南

- **Next.js** → 阅读 [references/nextjs.md](references/nextjs.md)
- **Replit (Express + Vite)** → 阅读 [references/replit.md](references/replit.md)

### 3. 创建产品（可选）

对于固定价格的商品，可以通过仪表板或MCP来创建产品：
```
mcporter call moneydevkit.create-product name="T-Shirt" priceAmount=2500 currency=USD
```
然后使用 `type: 'PRODUCTS'` 和产品ID进行结算。

对于动态金额（小费、捐款、发票等），可以直接使用 `type: 'AMOUNT'` 进行结算。

### 4. 部署

将应用程序部署到Vercel或Replit。确保在生产环境中设置了 `MDK_ACCESS_TOKEN` 和 `MDK_MNEMONIC`。

⚠️ 在传递环境变量时，请使用 `printf` 而不是 `echo`，因为末尾的新行可能会导致授权失败。

## 结算类型

| 类型 | 使用场景 | 必需字段 |
|------|----------|----------------|
| `AMOUNT` | 动态金额、小费、发票 | `amount`, `currency` |
| `PRODUCTS` | 销售仪表板上的产品 | `product`（产品ID） |

## 定价选项

- **固定价格** — 设置具体的金额（以美分或完整satoshi为单位）
- **自由定价** — 客户自行选择金额（在产品设置中设置 `amountType: 'CUSTOM'`）

## 货币单位

- `USD` — 以美分为单位（例如：500 = $5.00）
- `SAT` — 以完整的satoshi为单位

## 客户信息

收集客户信息以追踪购买记录并支持退款：
```ts
await createCheckout({
  // ...checkout fields
  customer: { email: 'jane@example.com', name: 'Jane', externalId: 'user-123' },
  requireCustomerData: ['email', 'name'] // show form for missing fields
})
```

## MCP工具

如果已连接到 [moneydevkit MCP服务器](https://mcp.moneydevkit.com/mcp/account/)，可以使用以下工具：

- `create-app` / `list-apps` / `update-app` / `rotate-api-key` — 管理应用程序
- `create-product` / `list-products` / `get-product` / `update-product` / `delete-product`
- `create-customer` / `list-customers` / `get-customer` / `update-customer` / `delete-customer`
- `list-checkouts` / `get-checkout` — 查看结算记录
- `list-orders` / `get-order` — 查看已完成的支付记录
- `search-docs` — 搜索moneydevkit的文档

## 安全注意事项

⚠️ `MDK_MNEMONIC` 是钱包助记词——请将其视为私钥。
- **切勿将其提交到git仓库或通过聊天消息分享**
- **切勿在应用程序的输出或错误处理中记录该助记词**
- 使用 **环境变量** 或 **秘密管理工具**（如Vercel的环境变量、Replit的Secrets功能、AWS Secrets Manager等）
- 在生产环境中，建议为每个应用程序使用独立的密钥，而不是在多个项目中重复使用同一个助记词
- 该助记词用于控制接收付款的Lightning钱包——如果被泄露，资金可能会被盗
- 在使用主网之前，请先用 `signet/testnet` 的凭证进行测试

**MDK_ACCESS_TOKEN` 是专属于您的应用程序的API密钥。如果密钥被泄露，请通过仪表板或MCP（`rotate-api-key`）更换它。**

**该功能使用的外部端点：**
- `mcp.moneydevkit.com` — 用于账户管理的MCP服务器（HTTPS，OAuth）
- `docs.moneydevkit.com` — 文档资料

**源代码：** [@moneydevkit on npm](https://www.npmjs.com/org/moneydevkit) · [docs.moneydevkit.com](https://docs.moneydevkit.com)

## 文档

完整文档：[docs.moneydevkit.com](https://docs.moneydevkit.com)