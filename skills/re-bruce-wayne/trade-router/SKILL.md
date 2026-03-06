---
name: traderouter
description: 通过 TradeRouter API 执行 Solana 交易、提交受 MEV 保护的交易、扫描钱包余额以及基于市场资本值的限价/追踪订单。当用户需要执行以下操作时可以使用该 API：在 Solana 上交换 SPL 代币（买入或卖出）、查看钱包中的代币持有情况、通过受 MEV 保护的交易通道提交已签名的交易、下达限价订单（以目标市场资本值为条件进行买入/卖出）、设置追踪止损订单（trailing_sell/trailing_buy）、下达组合订单（限价+TWAP、追踪+TWAP、限价+追踪、限价+追踪+TWAP）、管理现有订单（查看、列出、取消、延长订单有效期），或实现定期定额投资（DCA）策略。无需 API 密钥——仅需提供钱包地址即可。支持的 REST 端点包括：POST /swap、POST /holdings、POST /protect；用于下达限价订单的 WebSocket 端点为 wss://api.traderouter.ai/ws。
---
# TradeRouter

这是一个用于Solana的交换构建器和限价订单引擎。

**基础URL:** `https://api.traderouter.ai`
**WebSocket连接:** `wss://api.traderouter.ai/ws`
**官方网站:** https://traderouter.ai
**认证方式:** 无需API密钥。仅使用钱包地址进行身份验证。
**内容类型:** 所有REST请求都必须指定`Content-Type: application/json`。

---

## 使用本技能前的注意事项

**保持WebSocket连接活跃:** 发送限价订单、追踪订单以及进行订单管理（取消、延长订单、列出订单）需要保持与`wss://api.traderouter.ai/ws`的连接处于打开状态。服务器仅通过该连接发送`order_filled`响应；如果连接断开，您需要重新连接并重新注册才能接收订单执行结果。只要您有未完成的订单，就必须保持WebSocket连接活跃。在连接断开后，请重新连接并重新注册。

**订单管理的认证:** WebSocket上的订单放置和取消操作需要通过“挑战-响应”流程进行认证：服务器会发送一个带有随机数（nonce）的挑战；客户端必须使用钱包的私钥（Ed25519算法）对随机数进行签名，并发送包含`wallet_address`和签名后的`register`请求。只有在服务器返回`registered`且`authenticated: true`时，客户端才能放置或取消订单。这种认证方式是通过签名的随机数来验证钱包身份的——无需单独的API密钥。

**服务来源:** 本文档仅描述了API的接口信息。服务的官方网站是`https://traderouter.ai`（API地址为`api.traderouter.ai`）。

**MEV保护:** `/post /protect`端点接受已签名的交易，并使用`Jito`和**质押连接通道**来处理这些交易。

**风险提示:** 无需API密钥；唯一需要的身份验证信息是钱包地址。

---

## 如何使用不同的端点

| 客户操作 | 对应端点 | 方法 |
|-------------|----------|--------|
| 即时买卖代币 | `POST /swap` → 签名 → `POST /protect` | REST请求 |
| 查看钱包中的代币余额 | `POST /holdings` | REST请求 |
| 提交已签名的交易（带有MEV保护） | `POST /protect` | REST请求 |

---

## 使用前须知

### 维护WebSocket连接

- 发送限价订单、追踪订单以及进行订单管理（取消、延长订单）需要保持与`wss://api.traderouter.ai/ws`的连接处于打开状态。
- 服务器仅通过该连接发送`order_filled`响应；如果连接断开，您需要重新连接并重新注册才能接收订单执行结果。
- 为了能够接收和执行订单，必须在整个订单有效期内保持WebSocket连接活跃。
- 在连接断开后，请重新连接并重新注册。

### 订单管理的认证

- WebSocket上的订单放置和取消操作需要通过“挑战-响应”流程进行认证：
  - 服务器发送一个带有随机数（nonce）的挑战；
  - 客户必须使用钱包的私钥（Ed25519算法）对随机数进行签名，并发送包含`wallet_address`和签名后的`register`请求。
  - 只有在服务器返回`registered`且`authenticated: true`时，客户端才能放置或取消订单。
- 这种认证方式是通过签名的随机数来验证钱包身份的——无需单独的API密钥。

### 服务起源

本文档仅描述了API的接口信息。服务的官方网站是`https://traderouter.ai`（API地址为`api.traderouter.ai`）。

---

## 各端点的使用场景

| 客户意图 | 对应端点 | 方法 |
|-------------|----------|--------|
| 即时买卖代币 | `POST /swap` → 签名 → `POST /protect` | REST请求 |
| 查看钱包中的代币余额 | `POST /holdings` | REST请求 |
| 提交已签名的交易（带有MEV保护） | `POST /protect` | REST请求 |

---

## 相关代码块

### POST /swap — 构建未签名的交换交易

返回一个**未签名**的交易（格式为base58）。客户端必须对交易进行签名，然后通过`POST /protect`发送。

### 请求参数

```json
{
  "wallet_address": "钱包地址",
  "token_address": "代币地址",
  "action": "买入" 或 "卖出",
  "amount": "交易金额" (仅限买入),
  "holdings_percentage": "持有百分比" (仅限卖出)
}
```

### 成功响应

```json
{
  "pool_type": "交易路由的DEX类型" (例如：`raydium`, `pumpswap`, `orca`, `meteora`)
}
```

### 错误响应

```json
{
  "code": "422" | 请求无效 |
  "400" | 请求错误 |
  "Error running simulation" | 当前路径无法执行交易（可能是DEX已关闭、余额为零或路径无效）
}
```

---

## 使用说明

### 如何选择合适的端点

根据您的具体操作，选择相应的API端点和方法。请参考上述文档中的说明。