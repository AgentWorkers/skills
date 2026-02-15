---
name: sponge-wallet
version: 1.0.0
description: 通过 Sponge Wallet API 管理加密钱包、转账、交易以及对账操作。
homepage: https://wallet.paysponge.com
user-invocable: true
metadata: {"openclaw":{"emoji":"\ud83e\uddfd","category":"finance","primaryEnv":"SPONGE_API_KEY","requires":{"env":["SPONGE_API_KEY"]}}}
---

# Sponge Wallet API - 代理技能指南

此技能仅用于文档说明，没有对应的本地命令行界面（CLI）。代理必须直接调用Sponge Wallet的REST API。

## 各步骤的重要性（简要说明）

- **注册与登录**：代理创建一个新的受管理的钱包，该钱包与一个人类所有者关联。所有者必须明确认领该代理。登录功能仅适用于已有账户的人类用户。
- **认领链接**：确保人类所有者将代理明确链接到他们的账户，并控制允许列表和资金操作。
- **凭证持久性**：`apiKey`仅返回一次（在代理优先模式下立即返回，或在标准模式下设备批准后返回）。如果丢失，必须重新注册或重新认证。

## 标准凭证存储（必需）

将API密钥存储在**一个规范的位置**：

- `~/.spongewallet/credentials.json`

推荐的文件内容：

---

## 基础URL与身份验证

- 基础URL：`https://apiwallet.paysponge.com`
- 身份验证头：`Authorization: Bearer <SPONGE_API_KEY>`
- 内容类型：`application/json`

快速的环境设置：

---

## 重要提示：AI代理必须使用`register`接口，而非`login`接口

### 1) 代理注册（仅限AI代理）

有两种模式：
- **标准设备流程**（默认）：在返回API密钥之前，必须经过人类用户的批准。
- **代理优先**（`agentFirst: true`）：代理立即获得API密钥，人类用户可以稍后进行认领。

**步骤1 — 开始注册（推荐使用代理优先模式）**
---

响应内容包括：
- `verificationUriComplete`（人类所有者的认领链接）
- `claimCode`, `deviceCode`, `expiresIn`, `interval`, `claimText`
- `apiKey`（在代理优先模式下立即返回）

将`apiKey`, `claimCode`, 和 `verificationUriComplete`（作为`claimUrl`）存储在`~/.spongewallet/credentials.json`中，以便在上下文重置时人类用户可以认领。

**步骤2 — 将认领链接发送给人类所有者**
人类用户登录后，可以选择发布推文内容并批准代理。

认领链接格式：
- `verificationUriComplete`（示例路径：`/device?code=ABCD-1234`)
- 基础URL是前端页面（生产环境或本地环境），因此只需将完整的`verificationUriComplete`传递给人类用户。

**步骤3 — 监听完成状态（仅限标准设备流程）**
---

成功后，响应中会包含`apiKey`。将其保存到`~/.spongewallet/credentials.json`中，并将其用作`SPONGE_API_KEY`。

注意：在**代理优先模式**下，您已经从步骤1中获得了`apiKey`。设备令牌将处于待认领状态，直到人类用户完成认领。

### 2) 人类登录（仅限现有账户）

**步骤1 — 请求设备代码**
---

**步骤2 — 监听令牌状态**（与代理相同）
---

## 工具调用模式

所有工具调用都是带有JSON负载的普通REST请求。

**常见请求头**
---

**关于代理ID的说明：**`agentId`在API密钥认证时是可选的。仅在使用用户会话（例如基于Privy的认证）或明确操作其他代理时才需要。

### 工具 -> 端点映射

| 工具 | 方法 | 路径 | 参数/请求体 |
|------|--------|------|-------------|
| `get_balance` | GET | `/api/balances` | 查询参数：`chain`, `allowedChains`, `onlyUsdc` |
| `get_solana_tokens` | GET | `/api/solana/tokens` | 查询参数：`chain` |
| `search_solana_tokens` | GET | `/api/solana/tokens/search` | 查询参数：`query`, `limit` |
| `evm_transfer` | POST | `/api/transfers/evm` | 请求体：`chain`, `to`, `amount`, `currency` |
| `solana_transfer` | POST | `/api/transfers/solana` | 请求体：`chain`, `to`, `amount`, `currency` |
| `solana_swap` | POST | `/api/transactions/swap` | 请求体：`chain`, `inputToken`, `outputToken`, `amount`, `slippageBps` |
| `base_swap` | POST | `/api/transactions/base-swap` | 请求体：`chain`, `inputToken`, `outputToken`, `amount`, `slippageBps` |
| `bridge` | POST | `/api/transactions/bridge` | 请求体：`sourceChain`, `destinationChain`, `token`, `amount`, `destinationToken`, `recipientAddress` |
| `get_transaction_status` | GET | `/api/transactions/status/{txHash}` | 查询参数：`chain` |
| `get_transaction_history` | GET | `/api/transactions/history` | 查询参数：`limit`, `chain` |
| `request_funding` | POST | `/api/funding-requests` | 请求体：`amount`, `reason`, `chain`, `currency` |
| `withdraw_to_main_wallet` | POST | `/api/wallets/withdraw-to-main` | 请求体：`chain`, `amount`, `currency` |
| `x402_fetch` | POST | `/api/x402/fetch` | 请求体：`url`, `method`, `headers`, `body`, `preferred_chain` |
| `discover_x402_services` | GET | `/api/x402/discover` | 查询参数：`type`, `limit`, `offset`, `include_catalog` |
| `polymarket` | POST | `/api/polymarket` | 请求体：`action`，以及特定于操作的参数（见下文） |
| `amazon_checkout` | POST | `/api/checkout` | 请求体：`checkoutUrl`, `amazonAccountId`, `shippingAddress`, `dryRun`, `clearCart` |
| `get_checkout_status` | GET | `/api/checkout/{sessionId}` | 查询参数：`agentId`（可选） |
| `get_checkout_history` | GET | `/api/checkout/history` | 查询参数：`agentId`, `limit`, `offset` |
| `amazon_search` | POST | `/api/checkout/amazon-search` | 请求体：`query`, `maxResults`, `region` |

注意：请求体使用驼峰命名法（例如`inputToken`, `slippageBps`）。

### Polymarket操作

`polymarket`端点是一个统一的工具。需要传递`action`以及特定于操作的参数：

| 操作 | 描述 | 必需参数 | 可选参数 |
|--------|-------------|-----------------|-----------------|
| `status` | 检查Polymarket账户状态和USDC.e余额 | — | — |
| `markets` | 搜索预测市场 | — | `query`, `limit` |
| `positions` | 查看当前市场头寸 | — | — |
| `orders` | 查看未成交和最近的订单 | — | — |
| `order` | 下单买入/卖出 | `outcome`, `side`, `size`, `price` | `market_slug` 或 `token_id`, `order_type` |
| `cancel` | 取消未成交订单 | `order_id` | — |
| `set_allowances` | 重置令牌授权 | — | — |
| `withdraw` | 从Safe钱包中提取USDC.e到任意地址 | `to_address`, `amount` | — |

**订单参数：**
- `market_slug`：市场URL slug（例如 `"will-bitcoin-hit-100k"`）——可以使用这个参数或`token_id`
- `token_id`：Polymarket条件令牌ID——可以使用这个参数或`market_slug`
- `outcome`：`"yes"` 或 `"no"`
- `side`：`"buy"` 或 `"sell"`
- `size`：股数（例如 `10`）
- `price`：概率价格（0.0–1.0，例如 `0.65` 表示每股0.65美分）
- `order_type`：`"GTC"`（默认），`"GTD"`, `"FOK"`, `"FAK"` |

**权限范围：** 交易操作（`order`, `cancel`, `set_allowances`, `withdraw`）需要`polymarket:trade`权限范围。读取操作（`status`, `markets`, `positions`, `orders`）需要`polymarket:read`权限范围。

**自动配置：** Polymarket Safe钱包会在首次使用时自动创建，无需手动设置。

### Amazon Checkout

使用已配置的Amazon账户购买产品。

**前提条件：**
- 必须通过仪表板或`/api/agents/:id/amazon-accounts`端点配置Amazon账户。
- 必须设置送货地址（可以在线设置或通过`/api/agents/:id/shipping-addresses`设置）。

**异步工作流程：**
1. 使用`POST /api/checkout`启动结账流程——返回一个`sessionId`。
2. 等待约60秒，直到结账流程完成。
3. 每10秒检查一次`GET /api/checkout/:sessionId`，直到状态变为`completed`或`failed`。

**状态变化：`pending` → `in_progress` → `completed` | `failed` | `cancelled`

**关键选项：**
- `dryRun: true` — 在下单前停止流程（适用于测试或预览总费用）
- `clearCart: true` — 在添加产品前清空Amazon购物车（默认行为）

**权限范围：** 结账操作需要`amazon_checkout`权限范围。

## 快速入门

### 1) 注册（仅限代理）
---

将认领链接分享给人类用户，然后立即存储`apiKey`（代理优先模式）。对于标准设备流程，在获得批准后检查令牌状态。

### 2) 查看余额
---

### 3) 在Base钱包中转移USDC
---

## 示例

### 在Solana上交换代币
---

### 在Base钱包中交换代币
---

### 跨链交换代币
---

### 查看交易状态
---

### 在Polymarket上检查状态
---

### 在Polymarket上搜索市场
---

### 在Polymarket上下单
---

### 在Polymarket上查看头寸
---

### 在Polymarket中提取USDC.e
---

### 使用Amazon Checkout开始购买
---

### 检查AmazonCheckout的状态
---

### 获取AmazonCheckout的历史记录
---

### 在Amazon上搜索产品
---

### 使用x402 Fetch（自动支付API）

`x402-fetch`工具会自动处理整个支付流程：
1. 向指定的URL发送HTTP请求。
2. 如果服务返回402 Payment Required（需要支付），则提取支付要求。
3. 使用代理的钱包（Base或Solana）创建并签署支付请求。
4. 重新发送请求，并添加`Payment-Signature`头部。
5. 返回最终API响应，其中包含`payment_made`和`payment_details`。

### 发现x402服务（Bazaar）

`x402_fetch`工具会从Bazaar和Sponge的精选目录中返回可用的x402支持服务。在调用`x402_fetch`之前，可以使用此功能来查找需要支付的API。

## 链路参考

**测试密钥**（`sponge_test_*`）：`sepolia`, `base-sepolia`, `solana-devnet`, `tempo`
**生产密钥**（`sponge_live_*`）：`ethereum`, `base`, `solana`

## 错误响应

错误会以JSON格式返回错误信息和HTTP状态码：

---

| 状态码 | 含义 | 常见原因 |
|--------|---------|--------------|
| 400 | 请求错误 | 缺少/无效的字段 |
| 401 | 未经授权 | 缺少或无效的API密钥 |
| 403 | 禁止访问 | 地址不在允许列表中或权限被拒绝 |
| 404 | 未找到 | 资源不存在 |
| 409 | 冲突 | 操作重复 |
| 429 | 请求过多 | 请稍后重试 |
| 500 | 服务器错误 | 临时问题；稍后重试 |

## 安全注意事项

- 绝不要在日志、帖子或截图中分享您的API密钥。
- 将API密钥存储在`~/.spongewallet/credentials.json`中，并限制文件的访问权限。
- 如果怀疑密钥被泄露，请及时更换密钥。

---

本文档专为代理设计。