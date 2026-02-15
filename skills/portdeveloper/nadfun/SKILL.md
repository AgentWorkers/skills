# SKILL.md - NadFun 集成指南

**具有绑定曲线的 Monad 代币发行平台。** 可以进行代币交易、发行自己的代币、监控事件——所有这些操作都通过纯 viem 实现。

## 什么是 NadFun？

NadFun 是一个基于 Monad 区块链的去中心化代币发行平台。其主要特点包括：

- **绑定曲线交易**：代币的初始价格由绑定曲线决定；随着购买人数的增加，价格会上涨。
- **代币毕业**：当曲线达到目标储备量时，代币会转移到 DEX（Uniswap V3）进行交易。
- **代币创建**：任何人都可以创建代币，并设置代币的图片、元数据以及可选的初始购买价格。
- **实时事件**：实时流式显示代币的交易、创建和在 DEX 的交换情况。
- **历史数据**：可以查询过去的事件以用于分析和监控。

## 技能文档

本技能指南分为多个模块。首先阅读概述部分，然后深入了解具体的指南：

| 模块                   | 目的                               | 面向对象              |
| ------------------------ | ------------------------------------- | --------------------- |
| **SKILL.md** (此文件) | 架构、常量、设置                        | 所有人              |
| **QUOTE.md**             | 价格报价、曲线状态                         | 交易者、分析师            |
| **TRADING.md**           | 买卖交易、权限签名                         | 交易者、机器人            |
| **TOKEN.md**             | 余额、元数据、转账                         | 应用程序开发者           |
| **CREATE.md**            | 代币创建、图片上传                         | 代币创建者             |
| **INDEXER.md**           | 历史事件查询                           | 分析工具、仪表盘           |
| **AGENT-API.md**         | 用于交易数据和代币信息的 REST API                 | AI 代理、机器人            |

有关 API 下载/端点/头部信息的使用方法，请参阅 **AGENT-API.md**。

> **注意：** 要获取 API 密钥，您必须首先通过钱包签名登录 [nad.fun](https://nad.fun)。请参阅下面的 [认证](#authentication-login-flow) 部分了解登录流程，然后使用会话 cookie 通过 `POST /api-key` 创建 API 密钥。

## 技能文件

| 文件         | URL                          |
| ------------ | ---------------------------- |
| ABI.md       | https://nad.fun/abi.md       |
| AGENT-API.md | https://nad.fun/agent-api.md |
| CREATE.md    | https://nad.fun/create.md    |
| INDEXER.md   | https://nad.fun/indexer.md   |
| QUOTE.md     | https://nad.fun/quote.md     |
| TOKEN.md     | https://nad.fun/token.md     |
| TRADING.md   | https://nad.fun/trading.md   |
| WALLET.md    | https://nad.fun/wallet.md    |

```bash
mkdir -p ~/.nadfun/skills
curl -s https://nad.fun/skill.md > ~/.nadfun/skills/SKILL.md
curl -s https://nad.fun/abi.md > ~/.nadfun/skills/ABI.md
curl -s https://nad.fun/agent-api.md > ~/.nadfun/skills/AGENT-API.md
curl -s https://nad.fun/create.md > ~/.nadfun/skills/CREATE.md
curl -s https://nad.fun/indexer.md > ~/.nadfun/skills/INDEXER.md
curl -s https://nad.fun/quote.md > ~/.nadfun/skills/QUOTE.md
curl -s https://nad.fun/token.md > ~/.nadfun/skills/TOKEN.md
curl -s https://nad.fun/trading.md > ~/.nadfun/skills/TRADING.md
curl -s https://nad.fun/wallet.md > ~/.nadfun/skills/WALLET.md
```

## 快速了解

- **网络**：测试网（链号 10143）或主网（链号 143）
- **语言**：TypeScript/JavaScript
- **纯 viem**：所有示例都直接使用 viem 调用智能合约
- **费用**：请通过 REST 端点查询部署费用

## 网络常量

所有地址和端点信息均在此处。网络发生变化时请更新这些信息。

```typescript
const NETWORK = "testnet" // 'testnet' | 'mainnet'

const CONFIG = {
  testnet: {
    chainId: 10143,
    rpcUrl: "https://monad-testnet.drpc.org",
    apiUrl: "https://dev-api.nad.fun", // For token creation

    // Contract addresses
    DEX_ROUTER: "0x5D4a4f430cA3B1b2dB86B9cFE48a5316800F5fb2",
    BONDING_CURVE_ROUTER: "0x865054F0F6A288adaAc30261731361EA7E908003",
    LENS: "0xB056d79CA5257589692699a46623F901a3BB76f1",
    CURVE: "0x1228b0dc9481C11D3071E7A924B794CfB038994e",
    WMON: "0x5a4E0bFDeF88C9032CB4d24338C5EB3d3870BfDd",
    V3_FACTORY: "0xd0a37cf728CE2902eB8d4F6f2afc76854048253b",
    CREATOR_TREASURY: "0x24dFf9B68fA36f8400302e2babC3e049eA19459E",
  },
  mainnet: {
    chainId: 143,
    rpcUrl: "https://monad-mainnet.drpc.org",
    apiUrl: "https://api.nadapp.net",

    // Contract addresses
    DEX_ROUTER: "0x0B79d71AE99528D1dB24A4148b5f4F865cc2b137",
    BONDING_CURVE_ROUTER: "0x6F6B8F1a20703309951a5127c45B49b1CD981A22",
    LENS: "0x7e78A8DE94f21804F7a17F4E8BF9EC2c872187ea",
    CURVE: "0xA7283d07812a02AFB7C09B60f8896bCEA3F90aCE",
    WMON: "0x3bd359C1119dA7Da1D913D1C4D2B7c461115433A",
    V3_FACTORY: "0x6B5F564339DbAD6b780249827f2198a841FEB7F3",
    CREATOR_TREASURY: "0x42e75B4B96d7000E7Da1e0c729Cec8d2049B9731",
  },
}[NETWORK]
```

## 基础设置

每个技能指南都假设您已经熟悉 viem。以下是基础内容：

```typescript
import { createPublicClient, createWalletClient, http, privateKeyToAccount } from "viem"

const NETWORK = "testnet"
const CONFIG = {
  /* from above */
}[NETWORK]

// Create clients
const publicClient = createPublicClient({
  chain: {
    id: CONFIG.chainId,
    name: "Monad",
    nativeCurrency: { name: "MON", symbol: "MON", decimals: 18 },
    rpcUrls: { default: { http: [CONFIG.rpcUrl] } },
  },
  transport: http(CONFIG.rpcUrl),
})

const account = privateKeyToAccount("0x...")
const walletClient = createWalletClient({
  account,
  chain: publicClient.chain,
  transport: http(CONFIG.rpcUrl),
})
```

这是您的起点。所有其他模块都是基于此构建的。

## 认证（登录流程）

要访问需要会话保护的端点（如 API 密钥管理、账户设置等），您需要通过钱包签名进行认证。

### 登录流程

```typescript
import { createWalletClient, http, privateKeyToAccount } from "viem"

const account = privateKeyToAccount("0x...")
const walletClient = createWalletClient({
  account,
  chain: {
    id: CONFIG.chainId,
    name: "Monad",
    nativeCurrency: { name: "MON", symbol: "MON", decimals: 18 },
    rpcUrls: { default: { http: [CONFIG.rpcUrl] } },
  },
  transport: http(CONFIG.rpcUrl),
})

// Step 1: Request nonce
const nonceRes = await fetch(`${CONFIG.apiUrl}/auth/nonce`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ address: account.address }),
})
const { nonce } = await nonceRes.json()

// Step 2: Sign the nonce
const signature = await walletClient.signMessage({ message: nonce })

// Step 3: Create session
const sessionRes = await fetch(`${CONFIG.apiUrl}/auth/session`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    signature,
    nonce,
    chain_id: CONFIG.chainId,
  }),
})

// Extract session cookie from response headers
const sessionCookie = sessionRes.headers.get("set-cookie")
const { account_info } = await sessionRes.json()

console.log("Logged in as:", account_info.account_id)
```

### 使用会话 Cookie

```typescript
// Use session cookie for authenticated requests
const headers = { Cookie: sessionCookie }

// Example: Create API Key (requires session)
const apiKeyRes = await fetch(`${CONFIG.apiUrl}/api-key`, {
  method: "POST",
  headers: { ...headers, "Content-Type": "application/json" },
  body: JSON.stringify({ name: "My Bot", expires_in_days: 365 }),
})
const { api_key } = await apiKeyRes.json()
console.log("API Key:", api_key) // Store this securely!
```

### 注销

```typescript
await fetch(`${CONFIG.apiUrl}/auth/delete_session`, {
  method: "DELETE",
  headers: { Cookie: sessionCookie },
})
```

### TypeScript 接口

```typescript
interface AuthNonceRequest {
  address: string
}

interface AuthNonceResponse {
  nonce: string
}

interface AuthSessionRequest {
  signature: string
  nonce: string
  chain_id: number
  wallet_address?: string // Optional
}

interface AuthSessionResponse {
  account_info: {
    account_id: string
    nickname: string
    bio: string
    image_uri: string
  }
}
```

## 核心概念

### 绑定曲线

NadFun 上的代币都是从绑定曲线开始的。该曲线决定了代币的价格和可用性：

- **实际储备**：池中的 MON 和代币数量
- **虚拟储备**：用于计算曲线的初始虚拟储备量
- **K 常量**：保持 `x * y = k` 的价格公式
- **目标**：必须售出的代币数量以达到毕业条件

使用 `getCurveState(token)` 获取曲线状态 → 详见 **QUOTE.md**

### 代币毕业

当购买足够的代币时：

1. 曲线达到目标储备量
2. 流动性转移到 Uniswap V3 池
3. 代币从绑定曲线转移到 DEX
4. `isGraduated(token)` 返回 `true`

使用 `getProgress(token)` 查看进度（0-10000 = 0-100%）

### 动作 ID

在创建代币时，`actionId` 参数用于标识动作类型：

| actionId | 描述                |
| -------- | ---------------------- |
| 1        | 创建代币                |

调用 `create` 函数时始终使用 `actionId: 1`。

### 权限签名

EIP-2612 允许钱包直接签署批准交易，而无需发送单独的 `approve()` 请求：

1. 生成签名：`generatePermitSignature(token, spender, amount, deadline)`
2. 在交易中使用：`sellPermit({ ...params, ...signature })`
3. 无需额外调用 `approve` —— 从而节省 Gas

详情请参阅 **TRADING.md**。

## 常见模式

### 模式 1：简单交易

```typescript
// Get quote (3 args: token, amountIn, isBuy)
const [router, amountOut] = await publicClient.readContract({
  address: LENS,
  abi: lensAbi,
  functionName: "getAmountOut",
  args: [token, amountIn, true], // true = buy
})

// Buy with slippage protection (1 tuple arg)
const minOut = (amountOut * BigInt(995)) / BigInt(1000) // 0.5% slippage
const deadline = BigInt(Math.floor(Date.now() / 1000) + 300)
const tx = await walletClient.writeContract({
  address: router, // Use router returned from getAmountOut
  abi: bondingCurveRouterAbi,
  functionName: "buy",
  args: [
    {
      amountOutMin: minOut,
      token: token,
      to: account.address,
      deadline: deadline,
    },
  ],
  value: amountIn,
})
```

详情请参阅 **TRADING.md**。

### 模式 2：发行代币

```typescript
import { bondingCurveRouterAbi } from "./abis/router"

// Requires API_KEY and deployFeeAmount (see CREATE.md for feeConfig())

// 1. Upload image to Agent API (raw binary, NOT formData)
const imageRes = await fetch(`${CONFIG.apiUrl}/agent/token/image`, {
  method: "POST",
  headers: {
    "X-API-Key": API_KEY,
    "Content-Type": "image/png", // or 'image/jpeg', 'image/webp', 'image/svg+xml'
  },
  body: imageBuffer, // raw binary data (Buffer, Blob, or ArrayBuffer)
})
const { image_uri: imageUri } = await imageRes.json()

// 2. Upload metadata to Agent API
const metadataRes = await fetch(`${CONFIG.apiUrl}/agent/token/metadata`, {
  method: "POST",
  headers: { "Content-Type": "application/json", "X-API-Key": API_KEY },
  body: JSON.stringify({
    name: "My Token",
    symbol: "MTK",
    description: "My awesome token",
    image_uri: imageUri,
  }),
})
const { metadata_uri: metadataUri } = await metadataRes.json()

// 3. Mine salt via Agent API
const saltRes = await fetch(`${CONFIG.apiUrl}/agent/salt`, {
  method: "POST",
  headers: { "Content-Type": "application/json", "X-API-Key": API_KEY },
  body: JSON.stringify({
    creator: account.address,
    name: "My Token",
    symbol: "MTK",
    metadata_uri: metadataUri,
  }),
})
const { salt } = await saltRes.json()

// 4. Create token on-chain
const tx = await walletClient.writeContract({
  address: BONDING_CURVE_ROUTER,
  abi: bondingCurveRouterAbi,
  functionName: "create",
  args: [
    {
      name: "My Token",
      symbol: "MTK",
      tokenURI: metadataUri,
      amountOut: 0n, // Set > 0n for initial buy amount (in tokens)
      salt: salt,
      actionId: 1, // Token creation action identifier (always 1 for create)
    },
  ],
  value: deployFeeAmount, // plus optional initial buy MON if amountOut > 0
  gas, // Use estimated gas (see below)
})

console.log("Transaction:", tx)

// Gas estimation (recommended over hardcoded values)
const gasEstimate = await publicClient.estimateContractGas({
  address: CONFIG.BONDING_CURVE_ROUTER,
  abi: bondingCurveRouterAbi,
  functionName: "create",
  args: [
    { name: "My Token", symbol: "MTK", tokenURI: metadataUri, amountOut: 0n, salt, actionId: 1 },
  ],
  value: deployFeeAmount,
  account: account.address,
})
const gas = (gasEstimate * 120n) / 100n // 20% buffer for safety
```

详细步骤请参阅 **CREATE.md**。

## 用于 AI 代理的提示

使用以下提示来指导您的操作：

### 交易

- “获取代币 X 的价格报价（需要 0.1 MON）”
- “以 1% 的滑点价格购买 0.1 MON 的代币 X”
- “使用权限签名出售所有代币”
- “检查代币是否已经毕业”

### 代币信息

- “获取代币地址 X 的元数据”
- “查看我的 MON 余额”
- “获取毕业前可购买的代币数量”

### 创建代币

- “使用此图片创建名为 MyToken (MTK) 的代币”
- “为我的代币生成一个自定义地址”
- “查看代币创建费用”

### 分析

- “计算代币 X 的毕业进度”
- “获取代币 X 的绑定曲线状态”
- “跟踪已毕业代币的所有交易”
- “分析代币的创建速率”

## 所需文件

进行集成时，您需要以下文件：

```
abis/
├── curve.ts              # Bonding curve contract ABI
├── lens.ts               # Price quote ABI
├── router.ts             # DEX router ABI
├── token.ts              # ERC20 token ABI
└── v3*.ts                # Uniswap V3 ABIs

constants.ts              # Network configs, contract addresses
```

所有 ABI 的文档信息请参阅 **ABI.md**。

### ABI 导入指南

每个 ABI 都可以在 **ABI.md** 中找到。请参考相应的部分：

| ABI                     | ABI.md 的位置                          | 目的                          |
| ----------------------- | ------------------------------------------------- | -------------------------------- |
| `bondingCurveRouterAbi` | [BondingCurveRouter ABI](#bondingcurverouter-abi) | 代币创建、买卖交易         |
| `lensAbi`               | [Lens ABI](#lens-abi)                             | 价格报价、获取输出金额         |
| `curveAbi`              | [Curve ABI](#curve-abi)                           | 曲线状态、毕业检查           |
| `tokenAbi`              | [Token ABI](#token-abi)                           | ERC20 操作、权限签名         |

示例导入方式：

```typescript
// Copy the ABI from ABI.md into your project
import { bondingCurveRouterAbi } from "./abis/router"
import { lensAbi } from "./abis/lens"
```

## 安装

```bash
npm install viem
# or
pnpm add viem
# or
yarn add viem
```

## 依赖项

**仅需要纯 viem**，无需其他区块链库。

## 故障排除

### “找不到该合约”

您可能连接到了错误的网络。请检查 `NETWORK` 常量是否与您的设置匹配。

### “代币尚未毕业”

通过 Lens 合约查询 `getProgress()`。返回值范围为 0-10000；达到 10000（100%）表示代币已毕业。

### “交易被撤销”

1. 检查 `amountOutMin` —— 滑点可能设置过高或曲线发生了变化
2. 验证截止时间 —— 交易耗时过长
3. 确认是否有足够的余额 —— 在出售前需要先批准交易

## 下一步

根据您的需求选择相应的指南：

- **构建 DEX 机器人？** → 参阅 **TRADING.md**
- **创建仪表盘？** → 参阅 **INDEXER.md** 和 **QUOTE.md**
- **发行代币？** → 参阅 **CREATE.md**
- **查询代币信息？** → 参阅 **TOKEN.md**

每个指南都提供了完整的示例代码供您参考。

## 通用开发实践与故障排除

### 类型安全提示

在处理 ABI 时，始终使用 `as const` 断言。本模块中的所有 ABI 都使用了 `as const` 进行类型声明，以确保类型安全：

```typescript
// Types are automatically narrowed
const result = await contract.read.getAmountOut([...])
// result type is precisely bigint (not bigint | undefined)
```

使用 viem 的类型辅助函数进行类型安全的转换：

```typescript
import { Address, Hex } from "viem"
import { parseEther, formatEther } from "viem"

// Amounts
const wei = parseEther("1") // string -> bigint
const eth = formatEther(1000000000000000000n) // bigint -> string

// Addresses
const addr: Address = "0x..." // Validated address type

// Signatures
const sig: Hex = "0x..." // Hex string type
```

### 常见 ABI 错误

在与智能合约交互时，可能会遇到一些特定的错误。以下是常见 ABI 相关错误及其解决方法：

| 错误类型                   | 含义                                      |
| ----------------------- | ---------------------------------------------------------- |
| `InsufficientAmount`    | 输出金额低于 `amountOutMin`                              |
| `InsufficientAmountOut` | 输出金额不足                                 |
| `DeadlineExpired`       | 截止时间已过                                        |
| `Unauthorized`          | 调用者未获得授权                                      |
| `AlreadyGraduated`      | 代币已转移到 DEX                             |
| `BondingCurveLocked`    | 在毕业过程中曲线被锁定                             |
| `InvalidProof`          | Merkle 证明验证失败（特定于某些操作）                      |
| `AlreadyClaimed`        | 该证明对应的金额已被领取                         |
| `NotClaimable`          | 该代币尚不符合领取条件                         |
| `InsufficientBalance`   | 财库中的 MON 余额不足                         |

有关 viem 中的错误类型，请参阅：

```typescript
import { ContractFunctionExecutionError } from 'viem'

try {
  await contract.write.buy([...]) // or any contract interaction
} catch (error) {
  if (error instanceof ContractFunctionExecutionError) {
    console.log(error.shortMessage) // "InsufficientAmount", etc.
  }
}
```