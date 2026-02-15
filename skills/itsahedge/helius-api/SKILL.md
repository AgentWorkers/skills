---
name: helius-api
description: >
  Query Solana data via the Helius API. Use when the user asks about Solana wallet balances,
  token holdings, NFT holdings, transaction history, transfer activity, wallet identity/labels,
  wallet funding sources, parsing transactions, or other Solana on-chain data. Triggers on:
  "solana wallet", "sol balance", "solana transactions", "wallet history", "who funded this wallet",
  "wallet identity", "solana transfers", "solana NFTs", "helius", "check solana address",
  "solana data", "parse transaction", "enhanced transactions", "transaction details".
---

# Helius API

通过 REST 端点查询 Solana 的综合数据。需要使用环境变量 `HELIUS_API_KEY`。

## 设置

```bash
export HELIUS_API_KEY="your-key-here"
```

请在 <https://dashboard.helius.dev> 获取 API 密钥。

## 基本 URL

- **钱包 API:** `https://api.helius.xyz/v1/wallet/{address}/...?api-key=KEY`
- **增强型交易:** `https://api-mainnet.helius-rpc.com/v0/...?api-key=KEY`

认证方式：使用查询参数 `?api-key=$HELIUS_API_KEY` 或 `X-Api-Key` 头部字段。

## 钱包 API 端点

| 端点 | 路径 | 描述 |
|----------|------|-------------|
| 账户余额 | `/v1/wallet/{address}/balances` | 显示代币持有量及对应的 USD 价值 |
| 交易历史 | `/v1/wallet/{address}/history` | 显示包含余额变化的交易记录 |
| 转账记录 | `/v1/wallet/{address}/transfers` | 显示代币的转账活动（发送/接收） |
| 账户信息 | `/v1/wallet/{address}/identity` | 显示钱包的标签（如交易所、使用的协议） |
| 批量查询账户信息 | `/v1/wallet/batch-identity` (POST) | 一次查询最多 100 个地址的信息 |
| 资金来源 | `/v1/wallet/{address}/funded-by` | 显示钱包的初始资金来源 |

## 增强型交易端点

| 端点 | 路径 | 描述 |
|----------|------|-------------|
| 解析交易记录 | `/v0/transactions/` (POST) | 将交易签名解析为人类可读的数据 |
| 交易历史 | `/v0/addresses/{address}/transactions` | 提供带有类型、时间等过滤条件的交易历史记录 |

## 参考文件

请查阅以下文件以获取详细的参数、响应格式和示例：

- **账户余额**（投资组合、持有代币、USD 价值）：[references/balances.md](references/balances.md)
- **交易历史**（钱包交易记录、盈亏情况、税务报告）：[references/history.md](references/history.md)
- **转账记录**（发送/接收的转账、支付追踪）：[references/transfers.md](references/transfers.md)
- **账户信息**（钱包标签、交易所识别）：[references/identity.md](references/identity.md)
- **资金来源**（资金来源、防止欺诈行为）：[references/funded-by.md](references/funded-by.md)
- **增强型交易**（解析交易记录、增强型交易历史）：[references/enhanced-transactions.md](references/enhanced-transactions.md)

## 实现说明

- 可使用 `curl` 或 `fetch` 进行请求，无需安装任何 SDK。
- 所有端点返回 JSON 格式的数据。
- 分页功能：使用 `page` 参数（查询账户余额）或 `before`/cursor 参数（查询交易历史/转账记录）。
- 每次请求的默认限制为 100 条记录。
- 使用钱包 API 每次请求会消耗 100 个信用点数。
- 如果钱包信息未知，`Identity` 端点会返回 404 错误，请妥善处理。
- 如果钱包从未接收过 SOL，`Funded By` 端点会返回 404 错误。
- 增强型交易使用不同的基础 URL（`api-mainnet.helius-rpc.com`）。