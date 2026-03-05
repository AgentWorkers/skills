---
name: maestro-bitcoin
description: 使用 SIWX + JWT + x402 认证机制通过 HTTP 查询 Maestro Bitcoin API；在生产环境中默认使用 Ethereum 主网，并且只需满足最低限度的钱包使用要求。
---
# Maestro Bitcoin 技能

使用此技能，可以通过 HTTP 直接调用 Maestro Bitcoin 的端点，并遵循当前的 x402 客户端流程。

## 默认的生产网络策略（优先使用主网）

- 首选生产网络：`eip155:1`（Ethereum 主网）。
- 备选生产网络：`eip155:8453`（Base 主网），仅在用户请求 Base 网络或批准回退方案时使用。
- 默认情况下使用生产网络主机。
- 仅在用户明确要求进行测试/阶段测试时使用 `dev.` 主机变体。
- 对于主网请求，切勿自动切换到测试网。

## 请求所需的最小前提条件

仅请求支付和签名所需的信息：

- 钱包选项 A：用于专用 EVM 签名的 `PRIVATE_KEY`。
- 钱包选项 B：运行时已有的 CDP Agent 钱包签名器。
- 可选的 `WALLET_NETWORK`（默认为 `eip155:1`，用于生产环境）。

## 资金要求（仅针对所选网络）

- 足够的 `USDC` 以支付所选金额。
- 适量的 `ETH` 作为交易手续费。

**注意：** 不要请求 x402 流程所需的 API 密钥。

## 客户端交互流程（预期操作）

1. 从 `https://docs.gomaestro.org/bitcoin` 阅读端点规范。
2. 发送请求时不要包含身份验证头。
3. 服务器会返回 `402 Payment Required` 的响应，响应体中包含以下内容：
   - `accepts`（可接受的支付选项）
   - `extensions.sign-in-with-x`（`domain`、`nonce`、`statement`、`issued_at`、`expiration_time`、`supported_chains`）

4. 构建 EIP-4361 SIWX 消息，并使用 EIP-191 签名（`personal_sign`）。
5. 重新发送请求，并在请求头中添加 `Sign-In-With-X`（base64 JSON 格式：`{"message": "...", "signature": "0x..."}`）。
6. 服务器会返回 `Authorization: Bearer <token>`，如果资金不足，则会再次返回 `402` 响应。
7. 在所选网络的允许范围内选择信用购买金额。
8. 使用所选金额和已签名的 ERC-3009 授权信息构建 `X-PAYMENT`（base64 JSON 格式）。
9. 重新发送请求，请求头中包含 `Authorization: Bearer <token>` 和 `X-PAYMENT: <base64 payload>`。
10. 如果请求成功（返回 `200` 状态码），则返回 API 响应体以及相关的支付/信用元数据。
11. 之后再次发送请求时，仅在资金不足的情况下才需要提供 JWT。

## 信用购买金额规则

- 基本信用成本：每笔信用额为 $0.000025。
- 购买金额必须在允许的范围内。

**当前限制：**

- 最小购买金额：$0.10（4,000 信用额）
- 最大购买金额：$50.00（2,000,000 信用额）

**常见购买金额示例：**

- $1.00 -> 40,000 信用额
- $5.00 -> 200,000 信用额
- $10.00 -> 400,000 信用额

## 需要处理的请求头信息

**请求头：**
- `Sign-In-With-X`（SIWX 身份验证尝试）
- `Authorization: Bearer <jwt>`（会话令牌）
- `X-PAYMENT`（信用购买数据）

**响应头：**
- `Authorization`（SIWX 之后的新 JWT）
- `X-Credits-Remaining`（剩余信用额）
- `X-Credit-Cost`（信用成本）
- `X-Credits-Purchased`（已购买的信用额）
- `Payment-Response`（结算元数据，base64 JSON 格式）

## 网络选择规则

- 对于生产环境用户，默认优先使用主网。
- 始终选择实时挑战返回的网络（`supported_chains`/`accepts`）。
- 如果仅提供测试网网络，请在用户确认后使用该网络。
- 不要硬编码接收方、资产或金额信息。

## 探索器交易查询

当收到 `Payment-Response` 时，提取交易哈希和网络地址，并返回对应的探索器链接。

**主网映射：**
- `eip155:1` -> `https://etherscan.io/tx/<transaction_hash>`
- `eip155:8453` -> `https://basescan.org/tx/<transaction_hash>`

**常见测试网映射：**
- `eip155:11155111` -> `https://sepolia.etherscan.io/tx/<transaction_hash>`
- `eip155:84532` -> `https://sepolia.basescan.org/tx/<transaction_hash>`

**如果映射信息未知，** 仍然返回原始的交易哈希和网络地址。

## 代理程序规则

- 实现应保持简洁且针对特定端点设计。
- 支持两种签名方式：`PRIVATE_KEY` 或 CDP Agent 钱包签名器。
- 在首次进行生产环境支付请求之前，请先进行确认。
- 如果支付失败（仍返回 `402` 响应），请报告以下信息：
  - 选定的网络
  - 选择的购买金额
  - 用于签名的钱包地址
  - 下一步操作建议（补充 USDC 或重新执行 SIWX 和支付操作）

## 主要参考资料：**
- `https://docs.gomaestro.org/bitcoin`