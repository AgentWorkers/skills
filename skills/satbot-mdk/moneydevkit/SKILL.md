---
name: moneydevkit
description: 使用 moneydevkit，您可以在任何网站上接受付款。无论您是在构建一个销售商品的网站、添加结账/支付墙功能，还是将支付功能集成到 Next.js 或 Replit 应用程序中，moneydevkit 都能满足您的需求。它支持固定价格、按需付费的模式，同时还能处理产品、客户和订单的管理。其底层技术基于 Bitcoin Lightning，因此支持全球范围内的支付，且无需银行账户即可使用。
---

# moneydevkit

您可以在5分钟内将支付功能添加到任何Web应用程序中。支持两种框架：Next.js和Replit（Express + Vite）。

## 工作流程

### 1. 获取凭证

**选项A — MCP：**

MCP提供了两种服务：
- **未认证**（`/mcp/`）——用于创建新账户和生成凭证
- **已认证**（`/mcp/account/`）——用于在设置完成后管理账户（需要OAuth认证）

创建新账户的步骤：
```
claude mcp add moneydevkit --transport http https://mcp.moneydevkit.com/mcp/
```

获取凭证后，切换到已认证的MCP界面以获得完整的账户管理权限：
```
claude mcp add moneydevkit --transport http https://mcp.moneydevkit.com/mcp/account/
```

**选项B — CLI：**
```bash
npx @moneydevkit/create
```

**选项C — 仪表板：**
在[moneydevkit.com](https://moneydevkit.com)注册并创建一个应用程序。

所有选项都会生成两个值：
- `MDK_ACCESS_TOKEN` — API密钥
- `MDK_MNEMONIC` — 钱包助记词

将这两个值添加到`.env`文件中（或Replit的Secrets配置、Vercel的环境变量等）。这两个值都是必需的。

### 2. 选择框架并按照其指南操作

- **Next.js** → 阅读[references/nextjs.md](references/nextjs.md)
- **Replit (Express + Vite)** → 阅读[references/replit.md]

### 3. 创建产品（可选）

对于固定价格的商品，可以通过仪表板或MCP来创建产品：
```
mcporter call moneydevkit.create-product name="T-Shirt" priceAmount=2500 currency=USD
```
然后使用`type: 'PRODUCTS'`类型进行结算，并提供产品ID。

对于动态金额（小费、捐款、发票等），可以直接使用`type: 'AMOUNT'`类型进行结算。

### 4. 部署

将应用程序部署到Vercel（Next.js）或Replit。确保在生产环境中设置了`MDK_ACCESS_TOKEN`和`MDK_MNEMONIC`。

⚠️ 在传递环境变量时，请使用`printf`而不是`echo`——末尾的换行符可能导致认证失败。

## 结算类型

| 类型 | 使用场景 | 必需字段 |
|------|----------|----------------|
| `AMOUNT` | 动态金额、小费、发票 | `amount`, `currency` |
| `PRODUCTS` | 销售仪表板上的产品 | `product`（产品ID） |

## 定价选项

- **固定价格** — 设置具体的金额（以美分或完整satoshis为单位）
- **自由定价** — 客户自行选择金额（在产品设置中设置`amountType: 'CUSTOM'`）

## 货币单位

- `USD` — 金额以美分为单位（例如：500 = $5.00）
- `SAT` — 金额以完整的satoshis为单位

## 客户信息

收集客户信息以便追踪购买记录并支持退款：
```ts
await createCheckout({
  // ...checkout fields
  customer: { email: 'jane@example.com', name: 'Jane', externalId: 'user-123' },
  requireCustomerData: ['email', 'name'] // show form for missing fields
})
```

## MCP工具

如果已连接到[MCP服务器](https://mcp.moneydevkit.com/mcp/account/)，可以使用以下工具：

- `create-app` / `list-apps` / `update-app` / `rotate-api-key` — 管理应用程序
- `create-product` / `list-products` / `get-product` / `update-product` / `delete-product`
- `create-customer` / `list-customers` / `get-customer` / `update-customer` / `delete-customer`
- `list-checkouts` / `get-checkout` — 查看结算记录
- `list-orders` / `get-order` — 查看已完成的交易
- `search-docs` — 搜索moneydevkit的文档

## 文档

完整文档：[docs.moneydevkit.com](https://docs.moneydevkit.com)