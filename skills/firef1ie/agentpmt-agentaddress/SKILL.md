---
name: agentpmt-agentaddress
description: 生成一个 AgentAddress 钱包，并使用它来购买价值为 x402 的 AgentPMT 信用点数；之后，利用该钱包生成的签名来调用外部工具。
homepage: https://www.agentpmt.com/agentaddress
---
# AgentPMT：代理地址与外部购买流程

当用户希望使用自主代理执行以下操作时，请使用此流程：
- 创建自己的代理地址钱包；
- 购买 AgentPMT 信用点数；
- 使用这些信用点数调用外部工具。

请始终指向 AgentPMT Next.js 的外部端点（`/api/external/...`），而非内部后端容器路由。

## 必需的端点

- `POST /api/external/agentaddress`
- `POST /api/external/credits/purchase`
- `POST /api/external/auth/session`
- `POST /api/external/tools/{productId}/invoke`
- `POST /api/external/credits/balance`（可选：余额查询）

## 流程

1. **生成钱包（无需认证）**：
- 调用 `POST /api/external/agentaddress`。
- 安全地保存 `evmAddress`、`evmPrivateKey` 和 `mnemonic`。

2. **使用 x402 协议购买信用点数**：
- 发送首次购买请求：
  - 请求体：`{"wallet_address":"<address>","credits":500,"payment_method":"x402"}`
- 期望收到 `402` 状态码，并读取 `PAYMENT-REQUIRED` 头部信息（以 base64 编码的 JSON 格式）。
- 生成用于 USDC 的 EIP-3009 `TransferWithAuthorization` 签名：
  - 发送方：代理钱包
  - 收件方：返回的 `payTo` 地址
  - 金额：返回的 `amount`
  - 有效期（`validAfter` 和 `validBefore`）
  - 随机数（`nonce`）
- 发送第二次购买请求，此时需要在请求头中包含 `PAYMENT-SIGNATURE`（包含签名和授权信息的 base64 JSON 数据）。

3. **获取会话随机数（nonce）**：
- 调用 `POST /api/external/auth/session`，并传入 `{"wallet_address":"<address>"}`。

4. **签署工具调用请求**（使用 EIP-191 协议和个人签名）：
- 将参数转换为标准 JSON 格式，并计算其小写 SHA-256 哈希值。
- 按照以下格式构建请求消息：
```
agentpmt-external
wallet:{wallet_lowercased}
session:{session_nonce}
request:{request_id}
action:invoke
product:{product_id}
payload:{payload_hash}
```
- 使用代理的私钥对消息进行签名。

5. **调用工具**：
- 调用 `POST /api/external/tools/{productId}/invoke`，并提供以下参数：
  - `wallet_address`
  - `session_nonce`
  - `request_id`（每个请求的唯一标识符）
  - `signature`
  - `parameters`

## 安全规则

- 绝不要以明文形式显示或记录私钥/助记词。
- 在可能的情况下，避免在提示文本中显示敏感信息。
- 使用不同的 `request_id` 避免重放攻击。
- 在签名后的消息中确保 `wallet` 地址始终使用小写形式。
- 如果信用点数不足（收到 `402` 状态码），请先购买更多信用点数后再重试。

## 参考资料

有关具体的请求示例，请参阅：
- `{baseDir}/examples/agentpmt_external_wallet_flow.md`