---
name: zyfai
description: 在 Base、Arbitrum 和 Plasma 平台上，您可以通过任何以太坊钱包获得收益。当用户希望其资金产生被动收益（即无需主动操作即可获得收益）时，可以使用该功能。系统会部署一个与用户以太坊地址（EOA）关联的非托管子账户（Safe），实现自动化的收益优化，并允许用户随时进行存款和取款操作。
---
# Zyfai — 为任何钱包生成收益

将任何以太坊钱包转换为能够产生收益的账户。

## 功能概述

当用户希望从他们的加密货币中获取收益时，Zyfai 会为他们创建一个与现有钱包（EOA，即Externally Owned Account）关联的子账户（安全智能钱包）。存入该子账户的资金会自动在各种 DeFi 协议中进行优化。用户始终保持完全控制权，并可以随时提取资金。

```
┌─────────────────┐      ┌──────────────────────┐
│   User's EOA    │ ───► │  Zyfai Subaccount    │
│  (their wallet) │      │  (Safe smart wallet) │
│                 │      │                      │
│  Owns & controls│      │  • Auto-rebalancing  │
│                 │      │  • Yield optimization│
│                 │      │  • Non-custodial     │
└─────────────────┘      └──────────────────────┘
```

**关键点：**
- 子账户**由用户的 EOA 拥有**——只有用户才能提取资金
- 会话密钥支持**自动再平衡**，但无法将资金提取到其他地址
- 相同的 EOA 在所有链上对应相同的子账户地址

## 使用流程

```
1. DEPLOY    →  Create subaccount linked to user's wallet
2. SESSION   →  Enable automated yield optimization  
3. DEPOSIT   →  Send funds to subaccount (starts earning)
4. WITHDRAW  →  Pull funds back to wallet (anytime)
```

## 先决条件

- **API 密钥**——可以通过编程方式获取（见下文），或在 [sdk.zyf.ai](https://sdk.zyf.ai) 手动获取
- **钱包连接**——可以是钱包提供商（浏览器）或安全密钥管理工具（服务器）
- **Node.js 18+**

```bash
npm install @zyfai/sdk viem
```

### 编程方式获取 API 密钥（适用于代理）

代理可以无需人工干预自行生成 API 密钥。您需要代理的钱包地址（公钥）。

```bash
POST https://sdk.zyf.ai/api/sdk-api-keys/create
Content-Type: application/json

{
  "clientName": "my-agent",
  "walletAddress": "0x...",
  "email": "agent@example.com"
}
```

**响应：**
```json
{
  "success": true,
  "message": "SDK API key created successfully. Store the apiKey securely - it cannot be retrieved later!",
  "data": {
    "id": "936...",
    "apiKey": "zyfai_361ad41d083c2fe.....",
    "keyPrefix": "zyfai_361ad4",
    "clientName": "my-agent",
    "ownerWalletAddress": "0x..."
  }
}
```

> **重要提示：** 请安全存储 `apiKey`——该密钥无法事后恢复。密钥与提供的钱包地址相关联。

## 支持的链

| 链路    | ID    |
|----------|-------|
| Arbitrum | 42161 |
| Base     | 8453  |
| Plasma   | 9745  |

## 重要提示：始终使用 EOA 地址

在调用 SDK 方法时，**必须使用 EOA 地址**（用户的钱包地址）作为 `userAddress`——切勿使用子账户/安全钱包的地址。SDK 会自动从 EOA 推导出子账户地址。

## 钱包连接方式

SDK 支持多种钱包连接方式。根据您的安全需求和部署环境进行选择。

### 选项 1：钱包提供商（推荐用于浏览器/dApps）

使用 MetaMask 等注入式钱包提供商。私钥始终保留在用户的钱包中。

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// Connect using injected wallet provider (MetaMask, WalletConnect, etc.)
await sdk.connectAccount(window.ethereum, 8453);
```

**安全性：** 私钥始终保存在用户的钱包中。SDK 仅在需要时请求签名。

### 选项 2：Viem WalletClient（推荐用于服务器代理）

使用预先配置的 viem WalletClient。这是服务器端代理的推荐方式，因为它支持与安全密钥管理解决方案的集成。

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

// Create wallet client with your preferred key management
// Option A: From environment variable (simple but requires secure env management)
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);

// Option B: From KMS (AWS, GCP, etc.) - recommended for production
// const account = await getAccountFromKMS();

// Option C: From Wallet-as-a-Service (Turnkey, Privy, etc.)
// const account = await turnkeyClient.getAccount();

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(),
});

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// Connect using the WalletClient
await sdk.connectAccount(walletClient, 8453);
```

**安全性：** WalletClient 提供了与以下安全密钥管理解决方案的集成：
- **AWS KMS** / **GCP Cloud KMS** — 硬件支持的密钥存储
- **Turnkey** / **Privy** / **Dynamic** — 钱包即服务（Wallet-as-a-Service）提供商
- **硬件钱包** — 通过 WalletConnect 或类似工具

### 选项 3：私钥字符串（仅限开发使用）

直接使用私钥。

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// WARNING: Only use for development. Never hardcode private keys in production.
await sdk.connectAccount(process.env.PRIVATE_KEY, 8453);
```

**安全警告：** 在环境变量中存储原始私钥存在安全风险。对于生产环境中的自主代理，请使用选项 2 并配合适当的密钥管理解决方案。

## 安全性对比

| 方法 | 安全性级别 | 使用场景 |
|--------|---------------|----------|
| 钱包提供商 | 高 | 浏览器 dApps、面向用户的应用 |
| WalletClient + KMS | 高 | 生产环境中的服务器代理 |
| WalletClient + WaaS | 高 | 生产环境中的服务器代理 |
| 私钥字符串 | 低 | 仅限开发/测试环境 |

## 分步操作

### 1. 连接到 Zyfai

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// For browser: use wallet provider
await sdk.connectAccount(window.ethereum, 8453);

// For server: use WalletClient (see Wallet Connection Options above)
const walletClient = createWalletClient({
  account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
  chain: base,
  transport: http(),
});
await sdk.connectAccount(walletClient, 8453);
```

### 2. 部署子账户

```typescript
const userAddress = "0x..."; // User's EOA (NOT the subaccount address!)
const chainId = 8453; // Base

// Check if subaccount exists
const wallet = await sdk.getSmartWalletAddress(userAddress, chainId);
console.log(`Subaccount: ${wallet.address}`);
console.log(`Deployed: ${wallet.isDeployed}`);

// Deploy if needed
if (!wallet.isDeployed) {
  const result = await sdk.deploySafe(userAddress, chainId, "conservative");
  console.log("Subaccount deployed:", result.safeAddress);
}
```

**策略选项：**
- `"conservative"` — 稳定的收益，较低的风险
- `"aggressive"` — 较高的收益，较高的风险

### 3. 启用收益优化

```typescript
await sdk.createSessionKey(userAddress, chainId);

// Always verify the session key was activated
const user = await sdk.getUserDetails();
if (!user.user.hasActiveSessionKey) {
  // Session key not active — retry the process
  console.log("Session key not active, retrying...");
  await sdk.createSessionKey(userAddress, chainId);
  
  // Verify again
  const userRetry = await sdk.getUserDetails();
  if (!userRetry.user.hasActiveSessionKey) {
    throw new Error("Session key activation failed after retry. Contact support.");
  }
}
console.log("Session key active:", user.user.hasActiveSessionKey);
```

这允许 Zyfai 自动重新分配资金。会话密钥**无法**将资金提取到任意地址——只能在协议范围内进行优化。

> **重要提示：** 在调用 `createSessionKey` 之后，务必通过 `getUserDetails().user.hasActiveSessionKey` 来验证会话密钥是否处于活动状态。如果返回 `false`，请重试该过程。会话密钥必须处于活动状态才能使自动收益优化功能生效。

### 4. 存入资金

```typescript
// Deposit 10 USDC (6 decimals)
await sdk.depositFunds(userAddress, chainId, "10000000");
```

资金从用户的 EOA 转移到子账户，并立即开始产生收益。

### 5. 提取资金

```typescript
// Withdraw everything
await sdk.withdrawFunds(userAddress, chainId);

// Or withdraw partial (5 USDC)
await sdk.withdrawFunds(userAddress, chainId, "5000000");
```

资金会返回到用户的 EOA。提取操作是异步处理的。

### 6. 断开连接

```typescript
await sdk.disconnectAccount();
```

## 完整示例

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

async function startEarningYield(userAddress: string) {
  const sdk = new ZyfaiSDK({ apiKey: process.env.ZYFAI_API_KEY! });
  const chainId = 8453; // Base
  
  // Connect using WalletClient (recommended for server agents)
  const walletClient = createWalletClient({
    account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
    chain: base,
    transport: http(),
  });
  await sdk.connectAccount(walletClient, chainId);
  
  // Deploy subaccount if needed (always pass EOA as userAddress)
  const wallet = await sdk.getSmartWalletAddress(userAddress, chainId);
  if (!wallet.isDeployed) {
    await sdk.deploySafe(userAddress, chainId, "conservative");
    console.log("Subaccount created:", wallet.address);
  }
  
  // Enable automated optimization
  await sdk.createSessionKey(userAddress, chainId);
  
  // Verify session key is active
  const user = await sdk.getUserDetails();
  if (!user.user.hasActiveSessionKey) {
    console.log("Session key not active, retrying...");
    await sdk.createSessionKey(userAddress, chainId);
    const userRetry = await sdk.getUserDetails();
    if (!userRetry.user.hasActiveSessionKey) {
      throw new Error("Session key activation failed. Contact support.");
    }
  }
  
  // Deposit 100 USDC
  await sdk.depositFunds(userAddress, chainId, "100000000");
  console.log("Deposited! Now earning yield.");
  
  await sdk.disconnectAccount();
}

async function withdrawYield(userAddress: string, amount?: string) {
  const sdk = new ZyfaiSDK({ apiKey: process.env.ZYFAI_API_KEY! });
  const chainId = 8453; // Base
  
  // Connect using WalletClient
  const walletClient = createWalletClient({
    account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
    chain: base,
    transport: http(),
  });
  await sdk.connectAccount(walletClient, chainId);
  
  // Withdraw funds (pass EOA as userAddress)
  if (amount) {
    // Partial withdrawal
    await sdk.withdrawFunds(userAddress, chainId, amount);
    console.log(`Withdrawn ${amount} (6 decimals) to EOA`);
  } else {
    // Full withdrawal
    await sdk.withdrawFunds(userAddress, chainId);
    console.log("Withdrawn all funds to EOA");
  }
  
  await sdk.disconnectAccount();
}
```

## API 参考

| 方法 | 参数 | 描述 |
|--------|--------|-------------|
| `connectAccount` | `(walletClientOrProvider, chainId)` | 与 Zyfai 进行身份验证 |
| `getSmartWalletAddress` | `(userAddress, chainId)` | 获取子账户地址和状态 |
| `deploySafe` | `(userAddress, chainId, strategy)` | 创建子账户 |
| `createSessionKey` | `(userAddress, chainId)` | 启用自动优化 |
| `depositFunds` | `(userAddress, chainId, amount)` | 存入 USDC（保留 6 位小数） |
| `withdrawFunds` | `(userAddress, chainId, amount?)` | 提取资金（如未指定金额，则提取全部） |
| `getPositions` | `(userAddress, chainId?)` | 获取活跃的 DeFi 位置 |
| `getAvailableProtocols` | `(chainId)` | 获取可用的协议和池 |
| `getAPYPerStrategy` | `(crossChain?, days?, strategyType?)` | 获取保守/激进策略的年化收益率（APY） |
| `getUserDetails` | `()` | 获取已认证的用户信息 |
| `getOnchainEarnings` | `(walletAddress)` | 获取收益数据 |
| `updateUserProfile` | `(params)` | 更新策略、协议、资金分配和跨链设置 |
| `registerAgentOnIdentityRegistry` | `(smartWallet, chainId)` | 在 ERC-8004 身份注册表上注册代理 |
| `disconnectAccount` | `()` | 结束会话 |

**注意：** 所有接受 `userAddress` 的方法都要求提供用户的 EOA 地址，而非子账户/安全钱包的地址。

## 数据相关方法

### getPositions

获取用户在所有协议中的活跃 DeFi 位置。可选地按链进行过滤。

**参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| userAddress | string | 是 | 用户的 EOA 地址 |
| chainId | SupportedChainId | 否 | 可选：按特定链 ID 过滤 |

**示例：**

```typescript
// Get all positions across all chains
const positions = await sdk.getPositions("0xUser...");

// Get positions on Arbitrum only
const arbPositions = await sdk.getPositions("0xUser...", 42161);
```

**返回值：**

```typescript
interface PositionsResponse {
  success: boolean;
  userAddress: string;
  positions: Position[];
}
```

### getAvailableProtocols

获取特定链上可用的 DeFi 协议和池及其年化收益率（APY）数据。

```typescript
const protocols = await sdk.getAvailableProtocols(42161); // Arbitrum

protocols.protocols.forEach((protocol) => {
  console.log(`${protocol.name} (ID: ${protocol.id})`);
  if (protocol.pools) {
    protocol.pools.forEach((pool) => {
      console.log(`  Pool: ${pool.name} - APY: ${pool.apy || "N/A"}%`);
    });
  }
});
```

返回值：
```typescript
interface ProtocolsResponse {
  success: boolean;
  chainId: SupportedChainId;
  protocols: Protocol[];
}
```

### getUserDetails

获取当前已认证的用户信息，包括智能钱包、使用的链、协议和设置。需要 SIWE 身份验证。

```typescript
await sdk.connectAccount(walletClient, chainId);
const user = await sdk.getUserDetails();

console.log("Smart Wallet:", user.user.smartWallet);
console.log("Chains:", user.user.chains);
console.log("Has Active Session:", user.user.hasActiveSessionKey);
```

返回值：
```typescript
interface UserDetailsResponse {
  success: boolean;
  user: {
    id: string;
    address: string;
    smartWallet?: string;
    chains: number[];
    protocols: Protocol[];
    hasActiveSessionKey: boolean;
    email?: string;
    strategy?: string;
    telegramId?: string;
    walletType?: string;
    autoSelectProtocols: boolean;
    autocompounding?: boolean;
    omniAccount?: boolean;
    crosschainStrategy?: boolean;
    agentName?: string;
    customization?: Record<string, string[]>;
  };
}
```

### updateUserProfile

更新已认证用户的配置信息，包括策略、协议、资金分配和跨链设置。需要 SIWE 身份验证。

**参数：**

```typescript
interface UpdateUserProfileRequest {
  /** Investment strategy: "conservative" for safer yields, "aggressive" for higher risk/reward */
  strategy?: "conservative" | "aggressive";

  /** Array of protocol IDs to use for yield optimization */
  protocols?: string[];

  /** Enable omni-account feature for cross-chain operations */
  omniAccount?: boolean;

  /** Enable automatic compounding of earned yields (default: true) */
  autocompounding?: boolean;

  /** Custom name for your agent */
  agentName?: string;

  /** Enable cross-chain strategy execution */
  crosschainStrategy?: boolean;

  /** Enable position splitting across multiple protocols */
  splitting?: boolean;

  /** Minimum number of splits when position splitting is enabled (1-4) */
  minSplits?: number;
}
```

**返回值：**

```typescript
interface UpdateUserProfileResponse {
  success: boolean;
  userId: string;
  smartWallet?: string;
  chains?: number[];
  strategy?: string;
  protocols?: string[];
  omniAccount?: boolean;
  autocompounding?: boolean;
  agentName?: string;
  crosschainStrategy?: boolean;
  executorProxy?: boolean;
  splitting?: boolean;
  minSplits?: number;
}
```

**示例：**

```typescript
// Update strategy from conservative to aggressive
await sdk.updateUserProfile({
  strategy: "aggressive",
});

// Configure specific protocols
const protocolsResponse = await sdk.getAvailableProtocols(8453);
const selectedProtocols = protocolsResponse.protocols
  .filter(p => ["Aave", "Compound", "Moonwell"].includes(p.name))
  .map(p => p.id);

await sdk.updateUserProfile({
  protocols: selectedProtocols,
});

// Enable position splitting (distribute across multiple protocols)
await sdk.updateUserProfile({
  splitting: true,
  minSplits: 3, // Split across at least 3 protocols
});

// Verify changes
const userDetails = await sdk.getUserDetails();
console.log("Strategy:", userDetails.user.strategy);
console.log("Splitting:", userDetails.user.splitting);
```

> **跨链策略：** 仅当用户**明确请求**时才启用跨链功能。要使跨链功能生效，`crosschainStrategy` 和 `omniAccount` 必须都设置为 `true`。切勿默认启用跨链设置。

**注意事项：**
- **策略：** 可以随时更改。后续的再平衡操作将使用新的策略。
- **协议：** 在更新之前，请使用 `getAvailableProtocols(chainId)` 获取有效的协议 ID。
- **智能资金分配（minSplits = 1）：** 默认模式。为了最大化收益，资金会自动分配到多个 DeFi 池中——但前提是这样做有利可图。系统会根据当前市场情况和机会智能判断是否需要分配资金。
- **强制分配（minSplits > 1）：** 当 `minSplits` 设置为 2、3 或 4 时，资金会至少分配到这么多池中，以实现更好的风险分散（最多可分配到 4 个 DeFi 池）。这能确保无论市场状况如何，资金都会被分配。
- **跨链：** 需要同时满足 `crosschainStrategy: true` 和 `omniAccount: true` 的条件。只有在用户明确请求跨链收益优化时才能启用。链的配置在初次设置时确定，之后无法更改。
- **自动复利：** 默认启用。如果设置为 `true`，收益会自动再投资。
- 智能钱包地址、链和 `executorProxy` 无法通过此方法进行更新。

### getAPYPerStrategy

根据策略类型（保守或激进）、时间周期和链配置获取全球年化收益率（APY）。在部署前可以使用此方法比较不同策略的预期收益。

**参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| crossChain | boolean | 否 | 如果设置为 `true`，则返回跨链策略的年化收益率；如果设置为 `false`，则返回单链的年化收益率 |
| days | number | 否 | 计算年化收益率的时间周期（可选值：`7`、`15`、`30`、`60`） |
| strategyType | string | 否 | 策略风险类型（`conservative` 或 `aggressive`） |

**示例：**

```typescript
// Get 7-day APY for conservative single-chain strategy
const conservativeApy = await sdk.getAPYPerStrategy(false, 7, 'conservative');
console.log("Conservative APY:", conservativeApy.data);

// Get 30-day APY for aggressive cross-chain strategy
const aggressiveApy = await sdk.getAPYPerStrategy(true, 30, 'aggressive');
console.log("Aggressive APY:", aggressiveApy.data);

// Compare strategies
const conservative = await sdk.getAPYPerStrategy(false, 30, 'conservative');
const aggressive = await sdk.getAPYPerStrategy(false, 30, 'aggressive');
console.log(`Conservative 30d APY: ${conservative.data[0]?.apy}%`);
console.log(`Aggressive 30d APY: ${aggressive.data[0]?.apy}%`);
```

**返回值：**

```typescript
interface APYPerStrategyResponse {
  success: boolean;
  count: number;
  data: APYPerStrategy[];
}

interface APYPerStrategy {
  strategyType: string;
  apy: number;
  period: number;
  crossChain: boolean;
}
```

### getOnchainEarnings

获取钱包的链上收益，包括总收益、当前收益和累计收益。

```typescript
const earnings = await sdk.getOnchainEarnings(smartWalletAddress);

console.log("Total earnings:", earnings.data.totalEarnings);
console.log("Current earnings:", earnings.data.currentEarnings);
console.log("Lifetime earnings:", earnings.data.lifetimeEarnings);
```

返回值：
```typescript
interface OnchainEarningsResponse {
  success: boolean;
  data: {
    walletAddress: string;
    totalEarnings: number;
    currentEarnings: number;
    lifetimeEarnings: number;
    unrealizedEarnings?: number;
    currentEarningsByChain?: Record<string, number>;
    unrealizedEarningsByChain?: Record<string, number>;
    lastCheckTimestamp?: string;
  };
}
```

### registerAgentOnIdentityRegistry (ERC-8004)

根据 ERC-8004 标准，在身份注册表上注册您的 Zyfai 代理。此方法用于 OpenClaw 代理的注册。它会从 IPFS 获取包含代理元数据的 `tokenUri`，然后将其注册到链上。

**支持的链：**

| 链路 | 链 ID |
|-------|----------|
| Base | 8453 |
| Arbitrum | 42161 |

**参数：**

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| smartWallet | string | 是 | 要注册为代理的 Zyfai 智能钱包地址 |
| chainId | SupportedChainId | 是 | 链 ID（仅支持 8453 或 42161） |

**示例：**

```typescript
const sdk = new ZyfaiSDK({ apiKey: "your-api-key" });
await sdk.connectAccount(walletClient, 8453);

// Get smart wallet address
const walletInfo = await sdk.getSmartWalletAddress(userAddress, 8453);
const smartWallet = walletInfo.address;

// Register agent on Identity Registry
const result = await sdk.registerAgentOnIdentityRegistry(smartWallet, 8453);

console.log("Registration successful:");
console.log("  Tx Hash:", result.txHash);
console.log("  Chain ID:", result.chainId);
console.log("  Smart Wallet:", result.smartWallet);
```

**返回值：**

```typescript
interface RegisterAgentResponse {
  success: boolean;
  txHash: string;
  chainId: number;
  smartWallet: string;
}
```

**工作原理：**

1. 从 Zyfai API 获取 `tokenUri`（存储在 IPFS 上的代理元数据）
2. 将 `register(tokenUri)` 调用编码为适用于身份注册表合约的命令
3. 从连接的钱包发送交易
4. 等待链上的确认

## 安全性

- **非托管模式**——用户的 EOA 拥有子账户
- **会话密钥的使用受到限制**——只能用于再平衡操作，无法用于提取资金到其他地址
- **确定性**——相同的 EOA 在所有链上对应相同的子账户
- **灵活的密钥管理**——支持使用钱包提供商、WalletClients 或 KMS 集成

### 密钥管理最佳实践

对于**生产环境中的自主代理**，我们建议：
1. **使用带有安全密钥存储解决方案的 WalletClient**（不要使用原始私钥）
2. **与 KMS（如 AWS KMS、GCP Cloud KMS）集成**以实现硬件支持的密钥存储
3. **考虑使用 Wallet-as-a-Service 提供商（如 Turnkey、Privy 或 Dynamic）**
4. **切勿在源代码中硬编码**私钥
5. **定期轮换密钥并实施密钥撤销机制**

## 故障排除

### 不同链上的子账户地址不匹配

对于相同的 EOA，子账户地址在所有链上应该**完全一致**。如果发现地址不同：

```typescript
// Check addresses on both chains
const baseWallet = await sdk.getSmartWalletAddress(userAddress, 8453);
const arbWallet = await sdk.getSmartWalletAddress(userAddress, 42161);

if (baseWallet.address !== arbWallet.address) {
  console.error("Address mismatch! Contact support.");
}
```

**如果地址不匹配：**
1. 尝试在受影响的链上重新部署子账户
2. 如果问题仍然存在，请通过 Telegram 联系支持：[@paul_zyfai](https://t.me/paul_zyfai)

### “未找到存款地址”错误

这表示钱包尚未在后台注册。解决方法：
1. 先调用 `deploySafe()`——即使子账户已经部署在链上，此操作也会将其注册到后台
2. 然后重新尝试 `createSessionKey()`

### “签名无效”错误

这通常表示：
- 提供的钱包/签名者与用户指定的 EOA 不匹配
- 链上的安全钱包地址与 SDK 预期的地址不一致

请确保您使用的钱包与用户的 EOA 相匹配。

## 资源

- **获取 API 密钥：** [sdk.zyf.ai](https://sdk.zyf.ai) 或通过编程方式访问 `POST /api/sdk-api-keys/create`
- **文档：** [docs.zyf.ai](https://docs.zyf.ai)
- **演示：** [github.com/ondefy/zyfai-sdk-demo](https://github.com/ondefy/zyfai-sdk-demo)
- **MCP 服务器：** [mcp.zyf.ai](https://mcp.zyf.ai/mcp) — 可与 Claude 或其他兼容 MCP 的代理一起使用
- **代理注册：** [zyf.ai/.well-known/agent-registration.json](https://www.zyf.ai/.well-known/agent-registration.json)