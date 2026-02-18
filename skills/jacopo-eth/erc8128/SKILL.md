---
name: erc8128
description: 使用 ERC-8128 标准，通过以太坊钱包对 HTTP 请求进行签名和验证。适用于构建需要基于钱包身份验证的 API、向 ERC-8128 端点发送签名请求、在服务器端实现请求验证，或处理代理到服务器的身份验证场景。本文档介绍了 @slicekit/erc8128 JavaScript 库以及 erc8128 命令行工具（CLI）的相关用法。
---
# ERC-8128：以太坊 HTTP签名

ERC-8128 在 RFC 9421（HTTP 消息签名）的基础上，增加了以太坊钱包的签名功能。它允许使用现有的以太坊密钥进行 HTTP 认证，无需额外的凭据。

📚 **完整文档：** [erc8128.slice.so](https://erc8128.slice.so)

## 使用场景

- **API 认证** — 已经上链的钱包可以用来向您的后端进行认证。
- **代理认证** — 机器人和代理可以使用它们的操作密钥来签署请求。
- **防重放** — 签名中包含随机数（nonce）和过期时间。
- **请求完整性** — 签名会验证 URL、方法、请求头以及请求体。

## 相关包

| 包名 | 用途 |
|---------|---------|
| `@slicekit/erc8128` | 用于签名和验证的 JavaScript 库 |
| `@slicekit/erc8128-cli` | 用于签署请求的命令行工具（`erc8128 curl`） |

## `@slicekit/erc8128` 库

### 签署请求

```typescript
import { createSignerClient } from '@slicekit/erc8128'
import type { EthHttpSigner } from '@slicekit/erc8128'
import { privateKeyToAccount } from 'viem/accounts'

const account = privateKeyToAccount('0x...')

const signer: EthHttpSigner = {
  chainId: 1,
  address: account.address,
  signMessage: async (msg) => account.signMessage({ message: { raw: msg } }),
}

const client = createSignerClient(signer)

// Sign and send
const response = await client.fetch('https://api.example.com/orders', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ amount: '100' }),
})

// Sign only (returns new Request with signature headers)
const signedRequest = await client.signRequest('https://api.example.com/orders')
```

### 验证请求

```typescript
import { createVerifierClient } from '@slicekit/erc8128'
import type { NonceStore } from '@slicekit/erc8128'
import { createPublicClient, http } from 'viem'
import { mainnet } from 'viem/chains'

// NonceStore interface for replay protection
const nonceStore: NonceStore = {
  consume: async (key: string, ttlSeconds: number): Promise<boolean> => {
    // Return true if nonce was successfully consumed (first use)
    // Return false if nonce was already used (replay attempt)
  }
}

const publicClient = createPublicClient({ chain: mainnet, transport: http() })
const verifier = createVerifierClient(publicClient.verifyMessage, nonceStore)

const result = await verifier.verifyRequest(request)

if (result.ok) {
  console.log(`Authenticated: ${result.address} on chain ${result.chainId}`)
} else {
  console.log(`Failed: ${result.reason}`)
}
```

### 签署选项

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `binding` | `"request-bound"` \| `"class-bound"` | 签署的内容 |
| `replay` | `"non-replayable"` \| `"replayable"` | 是否包含随机数（nonce） |
| `ttlSeconds` | `number` | 签名的有效期（秒） |
| `components` | `string[]` | 需要签名的额外组件 |
| `contentDigest` | `"auto"` \| `"recompute"` \| `"require"` \| `"off"` | 内容摘要的处理方式 |

- **`request-bound`**：签署 `@authority`、`@method`、`@path`、`@query`（如果存在）以及 `content-digest`（如果请求体存在）。每个请求都是唯一的。
- **`class-bound`**：仅签署您明确指定的组件。适用于类似的请求。需要提供 `components` 数组。

**详情请参阅：** [请求绑定](https://erc8128.slice.so/concepts/request-binding)

### 验证请求

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `maxValiditySec` | `number` | 最大允许的有效期（秒） |
| `clockSkewSec` | `number` | 允许的时间偏差（秒） |
| `replayable` | `boolean` | 是否允许不包含随机数的签名 |
| `classBoundPolicies` | `string[]` \| `string[][]` | 允许的组件组合 |

**详情请参阅：** [验证请求](https://erc8128.slice.so/guides/verifying-requests) 和 [VerifyPolicy](https://erc8128.slice.so/api/types#verifypolicy)

## `erc8128 curl` 命令行工具

有关命令行工具的使用方法，请参阅 [references/cli.md](references/cli.md)。

**快速示例：**

```bash
# GET with keystore
erc8128 curl --keystore ./key.json https://api.example.com/data

# POST with JSON
erc8128 curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"foo":"bar"}' \
  --keyfile ~/.keys/bot.key \
  https://api.example.com/submit

# Dry run (sign only)
erc8128 curl --dry-run -d @body.json --keyfile ~/.keys/bot.key https://api.example.com
```

**完整文档请参阅：** [CLI 使用指南](https://erc8128.slice.so/guides/cli)

## 常见用法模式

- **Express 中间件**  
- **代理签名（使用密钥文件）**  
- **验证签名失败的原因**  

**详情请参阅：** [VerifyFailReason](https://erc8128.slice.so/api/types#verifyfailreason)

## 密钥管理

对于代理和自动化系统：

| 方法 | 安全性 | 使用场景 |
|--------|----------|----------|
| `--keyfile` | 中等安全性 | 使用未加密的密钥文件，需设置文件权限 |
| `--keystore` | 高安全性 | 使用加密的 JSON 密钥库，需要密码 |
| `ETH_PRIVATE_KEY` | 低安全性 | 作为环境变量使用（不建议在生产环境中使用） |
| **签名服务** | 高安全性 | 将签名任务委托给外部服务（如 SIWA、AWAL） |

## 文档资源

- **完整文档：** [erc8128.slice.so](https://erc8128.slice.so)
- **快速入门：** [erc8128.slice.so/getting-started/quick-start](https://erc8128.slice.so/getting-started/quick-start)
- **概念说明：** [erc8128.slice.so/concepts/overview](https://erc8128.slice.so/concepts/overview)
- **API 参考：** [erc8128.slice.so/api/signRequest](https://erc8128.slice.so/api/signRequest)
- **ERC-8128 规范：** [GitHub](https://github.com/slice-so/ERCs/blob/d9c6f41183008285a0e9f1af1d2aeac72e7a8fdc/ERCS/erc-8128.md)