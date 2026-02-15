---
name: Agent Wallet
description: 代理的钱包。使用此技能可以安全地创建一个钱包，代理可以使用该钱包进行转账、交易以及任何基于以太坊虚拟机（EVM）链的交易。
---

# 代理钱包

使用此技能可以安全地为代理创建一个钱包，用于转账、交换以及执行任何以太坊虚拟机（EVM）链上的交易，同时确保代理永远不会接触到私钥。创建钱包后，可以设置支出策略，代理便能够在您定义的规则范围内进行代币转账、交换以及与智能合约交互。

**代理永远无法看到私钥**。所有交易都在服务器端通过智能账户执行。钱包所有者可以通过可配置的策略来控制代理的权限。

## 配置

- **基础 API 地址：** 如果设置了 `SAFESKILLS_API_URL` 环境变量，请使用该地址；否则默认使用 `https://safeskill-production.up.railway.app`。
- **前端 URL：** 如果设置了 `SAFESKILLS_FRONTEND_URL` 环境变量，请使用该地址；否则默认使用 `https://safeskill-production.up.railway.app`。

所有 API 请求都需要一个 **Bearer 令牌**（在创建钱包时返回的 API 密钥）。

```
Authorization: Bearer <API_KEY>
```

## 快速入门

### 1. 创建钱包

为代理创建一个新的智能账户钱包。此操作会在服务器端生成私钥（您无法看到私钥的具体内容），同时创建一个 ZeroDev 智能账户，并返回一个 API 密钥以及钱包所有者的声明 URL。

```bash
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/secrets" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "EVM_WALLET",
    "memo": "My agent wallet",
    "chainId": 84532
  }'
```

响应内容包括：
- `apiKey` —— 请安全保管此密钥，将其用作所有后续请求的 **Bearer 令牌**。
- `claimUrl` —— 请将此链接分享给用户，以便他们可以声明钱包的所有权并设置支出策略。
- `address` —— 智能账户的地址。

创建完成后，告知用户：
> “这是您的钱包声明 URL：`<claimUrl>`。请使用此链接来声明所有权、设置支出策略并监控代理的 wallet 活动。”

### 2. 获取钱包地址

```bash
curl -X GET "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/address" \
  -H "Authorization: Bearer <API_KEY>"
```

### 3. 查看余额

```bash
# Native balance only
curl -X GET "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/balance" \
  -H "Authorization: Bearer <API_KEY>"

# With ERC-20 tokens
curl -X GET "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/balance?tokens=0xTokenAddr1,0xTokenAddr2" \
  -H "Authorization: Bearer <API_KEY>"
```

### 4. 转账 ETH 或代币

```bash
# Transfer native ETH
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/transfer" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xRecipientAddress",
    "amount": "0.01"
  }'

# Transfer ERC-20 token
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/transfer" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xRecipientAddress",
    "amount": "100",
    "token": "0xTokenContractAddress"
  }'
```

### 5. 交换代币

使用 0x 提供的 DEX 流动性来交换代币。

```bash
# Preview a swap (no execution, just pricing)
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/swap/preview" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "sellToken": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "buyToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "sellAmount": "0.1",
    "chainId": 1
  }'

# Execute a swap
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/swap/execute" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "sellToken": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "buyToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "sellAmount": "0.1",
    "chainId": 1,
    "slippageBps": 100
  }'
```

- `sellToken` / `buyToken`：代币合约的地址。对于原生 ETH，使用 `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`。
- `sellAmount`：可读的出售数量（例如，“0.1”表示 0.1 ETH）。
- `chainId`：用于交换的链（1 = Ethereum，137 = Polygon，42161 = Arbitrum，10 = Optimism，8453 = Base 等）。
- `slippageBps`：可选的滑点容忍度（以基点表示，100 表示 1%）。默认值为 100。

预览端点会返回预期的购买金额、路由信息和费用，而不会实际执行交易。执行端点会通过智能账户完成交换操作，并自动处理 ERC20 同意流程。

### 6. 发送任意交易

通过发送自定义的调用数据（calldata）来与任何智能合约进行交互。

```bash
curl -X POST "${SAFESKILLS_API_URL:-https://safeskill-production.up.railway.app}/api/skills/evm-wallet/send-transaction" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "0xContractAddress",
    "data": "0xCalldata",
    "value": "0"
  }'
```

## 策略

钱包所有者可以通过声明 URL 设置策略来控制代理的权限。如果某笔交易违反了策略，API 会拒绝该交易或要求通过 Telegram 进行人工审批。

| 策略 | 功能 |
|--------|-------------|
| **Address allowlist** | 仅允许向特定地址进行转账/调用。|
| **Token allowlist** | 仅允许转移特定的 ERC-20 代币。|
| **Function allowlist** | 仅允许调用特定的合约函数（通过 4 字节的地址选择器）。|
| **Spending limit (per tx)** | 每笔交易的最高花费金额（以美元计）。|
| **Spending limit (daily)** | 每 24 小时的最高花费金额（以美元计）。|
| **Spending limit (weekly)** | 每 7 天的最高花费金额（以美元计）。|
| **Require approval** | 每笔交易都需要通过 Telegram 进行人工审批。|
| **Approval threshold** | 金额超过指定阈值的交易需要人工审批。|

如果没有设置任何策略，则默认允许所有操作。一旦所有者声明了钱包并设置了策略，代理就会在这些规则范围内进行操作。

## 重要说明

- **切勿尝试访问原始的私钥信息**。私钥始终保存在服务器端，这正是该功能的核心所在。
- 请务必保存钱包创建时生成的 API 密钥，因为这是身份验证的唯一方式。
- 创建钱包后，请务必将声明 URL 分享给用户。
- 默认的链 ID 为 `84532`（Base Sepolia 测试网）。根据需要进行调整。
- 如果交易被拒绝，可能是由于违反了某些策略。请告知用户通过声明 URL 检查他们的策略设置。
- 如果交易需要审批，系统会返回 `status: "pending_approval"` 的状态。钱包所有者会收到 Telegram 通知，要求他们批准或拒绝交易。