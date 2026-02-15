---
name: para-wallet
description: 使用 Para 的 MPC（Multi-Party Computation）基础设施创建区块链钱包并签署交易，确保私钥永远不会存储在单一位置。该系统通过三个 REST 端点支持 EVM（以太坊虚拟机）和 Solana 链路。
metadata:
  author: para
  version: "1.0"
  openclaw.requires.env: ["PARA_API_KEY"]
---

## 概述

Para 提供了一种多方计算（MPC, Multi-Party Computation）钱包服务，其中私钥被分割成多个份额，并且**永远不会在某个地方被重新组合**。这使得 Para 非常适合那些需要创建钱包并签署交易，但**从不持有完整私钥**的 AI 代理。

所有操作都使用 Para 的 REST API，并通过一个 API 密钥进行身份验证。

- **基础 URL（测试版）：** `https://api.beta.getpara.com`
- **基础 URL（生产版）：** `https://api.getpara.com`
- **身份验证：** 在每个请求的 `X-API-Key` 头部中传递您的 API 密钥
- **内容类型：** `application/json`
- **请求追踪：** 可选地传递 `X-Request-Id`（UUID）以进行追踪；如果省略，Para 会自动生成一个 ID

## 设置

1. 从 [developer.getpara.com](https://developer.getpara.com) 获取 API 密钥。
2. 设置环境变量：
   ```
   export PARA_API_KEY="your-secret-api-key"
   ```
3. 在开发过程中使用 **测试版** 基础 URL (`https://api.beta.getpara.com`)。在生产环境中请切换到生产版 URL。

## 创建钱包

**`POST /v1/wallets`**

为用户创建一个新的 MPC 钱包。`type`、`scheme` 和 `userIdentifier` 的每一种组合都对应一个唯一的钱包。尝试创建重复的钱包会返回 `409` 错误代码，并提示钱包 ID 已存在。

### 请求体

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `type` | string | 是 | 钱包类型：`EVM`、`SOLANA` 或 `COSMOS` |
| `userIdentifier` | string | 是 | 用户标识符（电子邮件、电话或自定义 ID） |
| `userIdentifierType` | string | 是 | 用户标识符类型：`EMAIL`、`PHONE`、`CUSTOM_ID`、`GUEST_ID`、`TELEGRAM`、`DISCORD` 或 `TWITTER` |
| `scheme` | string | 否 | 签名方案：`DKLS`、`CGGMP` 或 `ED25519`（根据钱包类型默认设置） |

### EVM 示例

```bash
curl -X POST https://api.beta.getpara.com/v1/wallets \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PARA_API_KEY" \
  -d '{
    "type": "EVM",
    "userIdentifier": "alice@example.com",
    "userIdentifierType": "EMAIL"
  }'
```

### Solana 示例

```bash
curl -X POST https://api.beta.getpara.com/v1/wallets \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PARA_API_KEY" \
  -d '{
    "type": "SOLANA",
    "userIdentifier": "alice@example.com",
    "userIdentifierType": "EMAIL"
  }'
```

### 响应（201 Created）

钱包的状态会从 `creating` 变为 `ready`。您需要不断轮询直到状态变为 `ready`。

```json
{
  "id": "0a1b2c3d-4e5f-6789-abcd-ef0123456789",
  "type": "EVM",
  "scheme": "DKLS",
  "status": "creating",
  "createdAt": "2024-01-15T09:30:00Z"
}
```

响应中包含一个 `Location` 头部，其中包含钱包的 URL：
```
Location: /v1/wallets/0a1b2c3d-4e5f-6789-abcd-ef0123456789
```

### 轮询状态

创建钱包后，通过 `GET /v1/wallets/{walletId}` 不断轮询，直到状态变为 `ready`：

```bash
# Poll every 1 second until the wallet is ready
WALLET_ID="0a1b2c3d-4e5f-6789-abcd-ef0123456789"
while true; do
  RESPONSE=$(curl -s https://api.beta.getpara.com/v1/wallets/$WALLET_ID \
    -H "X-API-Key: $PARA_API_KEY")
  STATUS=$(echo "$RESPONSE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
  if [ "$STATUS" = "ready" ]; then
    echo "$RESPONSE"
    break
  fi
  sleep 1
done
```

## 获取钱包状态

**`GET /v1/wallets/{walletId}`**

检索钱包的当前状态和详细信息。

### 请求

```bash
curl https://api.beta.getpara.com/v1/wallets/0a1b2c3d-4e5f-6789-abcd-ef0123456789 \
  -H "X-API-Key: $PARA_API_KEY"
```

### 响应（200 OK）

当钱包状态变为 `ready` 时，响应中会包含钱包的地址和公钥：

```json
{
  "id": "0a1b2c3d-4e5f-6789-abcd-ef0123456789",
  "type": "EVM",
  "scheme": "DKLS",
  "status": "ready",
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f...",
  "publicKey": "04a1b2c3d4e5f6...",
  "createdAt": "2024-01-15T09:30:00Z"
}
```

### 响应字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `id` | string | 唯一的钱包标识符（UUID） |
| `type` | string | 区块链网络：`EVM`、`SOLANA` 或 `COSMOS` |
| `scheme` | string | 签名方案：`DKLS`、`CGGMP` 或 `ED25519` |
| `status` | string | 状态：`creating` 或 `ready` |
| `address` | string | 钱包地址（状态为 `ready` 时提供） |
| `publicKey` | string | 公钥（状态为 `ready` 时提供） |
| `createdAt` | string | ISO 8601 格式的创建时间戳 |

## 签署数据

**`POST /v1/wallets/{walletId}/sign-raw`**

使用钱包的 MPC 密钥份额来签署任意数据。私钥永远不会被重新组合——每个份额分别进行签名，然后将结果合并。

**重要提示：** 在签名之前，钱包必须处于 `ready` 状态。

### 请求体

| 字段 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| `data` | string | 是 | 需要签署的数据，以 `0x` 开头的十六进制字符串形式提供 |

### EVM 示例

签署消息哈希（例如，交易的 keccak256 哈希）：

```bash
curl -X POST https://api.beta.getpara.com/v1/wallets/0a1b2c3d-4e5f-6789-abcd-ef0123456789/sign-raw \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PARA_API_KEY" \
  -d '{
    "data": "0x48656c6c6f20576f726c64"
  }'
```

### Solana 示例

签署序列化的 Solana 交易：

```bash
curl -X POST https://api.beta.getpara.com/v1/wallets/aabbccdd-1122-3344-5566-778899aabbcc/sign-raw \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PARA_API_KEY" \
  -d '{
    "data": "0x01000103b5d..."
  }'
```

### 响应（200 OK）

### 响应中的签名

返回的签名是一个没有 `0x` 前缀的十六进制字符串。

## 关键概念

### 钱包的唯一性

`type`、`scheme` 和 `userIdentifier` 的每一种组合都对应一个唯一的钱包。如果尝试创建重复的钱包，API 会返回 `409 Conflict` 错误，并在响应体中提供现有钱包的 ID。您可以使用这个 ID 来安全地重试或查找现有的钱包。

### 异步钱包创建

钱包创建是异步的。`POST /v1/wallets` 请求会立即返回 `status: "creating"` 的状态。您需要通过 `GET /v1/wallets/{walletId}` 不断轮询，直到状态变为 `"ready"`，之后才能使用该钱包进行签名。

### MPC 安全模型

Para 使用多方计算技术，因此私钥永远不会存在于任何单一的机器上。密钥份额会被分发到不同的参与者手中。当您调用 `sign-raw` 时，每个参与者都会使用自己的份额进行签名，最终结果会被合并成一个有效的签名。这意味着：

- 没有任何单一点可以被攻破并泄露私钥
- 代理可以在不拥有完整私钥的情况下签署交易
- 从区块链的角度来看，这种签名方式与常规签名具有相同的功能性

## 错误参考

所有错误响应都包含一个 `message` 字段，用于描述问题所在。

| 状态 | 错误信息 | 原因 | 应对措施 |
|--------|---------|-------|--------|
| 400 | `"type must be one of EVM, SOLANA, COSMOS"` | 请求体字段无效或缺失 | 检查必填字段和枚举值 |
| 401 | `"secret api key not provided"` | 缺少 `X-API-Key` 头部 | 在请求中添加 `X-API-Key` 头部并插入您的 API 密钥 |
| 403 | `"invalid secret api key"` | API 密钥错误或已被吊销 | 在 developer.getpara.com 确认您的 API 密钥是否有效 |
| 404 | `"wallet not found"` | 钱包 ID 不存在或不属于您的账户 | 检查钱包 ID |
| 409 | `"a wallet for this identifier and type already exists"` | 尝试创建重复的钱包 | 使用返回的 `walletId` 访问现有的钱包 |
| 500 | `"Internal Server Error"` | 服务器端错误 | 采用指数级退避策略重试 |

### 409 冲突响应

`409` 错误响应中会包含现有钱包的 ID，您可以使用该 ID 来访问该钱包：

```json
{
  "message": "a wallet for this identifier and type already exists",
  "walletId": "0a1b2c3d-4e5f-6789-abcd-ef0123456789"
}
```

## 完整示例：创建钱包并签名

```bash
# 1. Create an EVM wallet
RESPONSE=$(curl -s -X POST https://api.beta.getpara.com/v1/wallets \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PARA_API_KEY" \
  -d '{
    "type": "EVM",
    "userIdentifier": "agent-1@myapp.com",
    "userIdentifierType": "EMAIL"
  }')

WALLET_ID=$(echo "$RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Created wallet: $WALLET_ID"

# 2. Poll until ready
while true; do
  WALLET=$(curl -s https://api.beta.getpara.com/v1/wallets/$WALLET_ID \
    -H "X-API-Key: $PARA_API_KEY")
  STATUS=$(echo "$WALLET" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
  if [ "$STATUS" = "ready" ]; then
    echo "Wallet is ready"
    echo "$WALLET"
    break
  fi
  echo "Status: $STATUS — waiting..."
  sleep 1
done

# 3. Sign data
SIGNATURE=$(curl -s -X POST https://api.beta.getpara.com/v1/wallets/$WALLET_ID/sign-raw \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PARA_API_KEY" \
  -d '{"data": "0x48656c6c6f"}')

echo "Signature: $SIGNATURE"
```