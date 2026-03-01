---
name: zyfai
description: 在 Base、Arbitrum 和 Plasma 平台上，您可以通过任何以太坊钱包获得收益。当用户希望其资金产生被动收益（即无需主动操作即可获得收益）时，可以使用此功能。系统会部署一个与用户的外部账户（EOA，Externally Owned Account）关联的非托管、确定性的子账户（Safe），实现自动化的收益优化，并允许用户随时进行存款和取款操作。
---
# Zyfai — 适用于任何钱包的收益生成服务

让任何以太坊钱包都能访问收益生成账户。

## 功能简介

当用户希望从自己的加密货币中获取收益时，Zyfai 会为用户创建一个 **确定性子账户**（Safe 智能钱包），该子账户与用户的现有钱包（EOA，Externally Owned Account）关联。存入该子账户的资金会自动在各种 DeFi 协议中进行优化。用户始终保持完全控制权，并可随时提取资金。

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
- 子账户 **归用户 EOA 所有** — 只有用户自己才能提取资金
- 会话密钥支持 **自动再平衡**，但无法将资金提取到其他地址
- 同一 EOA 在所有链上对应相同的子账户地址

## 使用流程

```
1. DEPLOY    →  Create a deterministic subaccount linked to user's wallet
2. SESSION   →  Enable automated yield optimization  
3. DEPOSIT   →  Send funds to subaccount (starts earning)
4. WITHDRAW  →  Pull funds back to wallet (anytime)
```

## 先决条件

- **API 密钥** — 可通过编程方式获取（详见下文），或手动在 [sdk.zyf.ai](https://sdk.zyf.ai) 获取
- **钱包连接** — 可以使用钱包提供商（浏览器）或安全密钥管理工具（服务器端）
- **Node.js 18+** 版本

```bash
npm install @zyfai/sdk viem
```

### 编程方式获取 API 密钥（适用于代理）

代理可以无需人工干预即可自行生成 API 密钥。您需要提供代理的钱包地址（公钥）。

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

> **重要提示：** 请妥善保管 `apiKey`，因为无法事后重新生成。该密钥与提供的钱包地址紧密关联。

## 支持的区块链

| 区块链 | ID    |
|----------|-------|
| Arbitrum | 42161 |
| Base     | 8453  |
| Plasma   | 9745  |

## 重要提示：始终使用 EOA 地址

调用 SDK 方法时，**必须使用 EOA 地址**（用户的钱包地址），而非子账户地址。SDK 会自动从 EOA 生成子账户地址。

## 钱包连接方式

SDK 支持多种钱包连接方式，请根据您的安全需求和部署环境进行选择：

### 选项 1：钱包提供商（推荐用于浏览器/dApps）

使用 MetaMask 等钱包提供商。私钥始终保留在用户的钱包中。

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// Connect using injected wallet provider (MetaMask, WalletConnect, etc.)
await sdk.connectAccount(window.ethereum, 8453);
```

**安全性说明：** 私钥始终存储在用户的钱包中，SDK 仅在需要时请求签名。

### 选项 2：Viem WalletClient（推荐用于服务器端代理）

使用预配置的 viem WalletClient。这是服务器端代理的推荐方案，因为它支持与安全密钥管理工具的集成。

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

**安全性说明：** WalletClient 可与以下安全密钥管理工具集成：
- **AWS KMS** / **GCP Cloud KMS** — 硬件加密的密钥存储服务
- **Turnkey** / **Privy** / **Dynamic** — 钱包即服务（Wallet-as-a-Service）提供商
- **硬件钱包** — 通过 WalletConnect 等方式连接

### 选项 3：直接使用私钥字符串（仅限开发环境）

**安全警告：** 在环境变量中直接使用私钥存在安全风险。在生产环境中，建议使用选项 2 并配合合适的密钥管理工具。

## 安全性对比

| 方法 | 安全性 | 适用场景 |
|--------|---------------|----------|
| 钱包提供商 | 高 | 浏览器 dApps、面向用户的应用程序 |
| WalletClient + KMS | 高 | 生产环境中的服务器代理 |
| WalletClient + WaaS | 高 | 生产环境中的服务器代理 |
| 直接使用私钥字符串 | 低 | 仅限开发/测试环境 |

## 操作步骤

### 1. 连接 Zyfai

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

**策略选择：**
- `"conservative"` — 稳定的收益，较低的风险
- `"aggressive"` — 更高的收益，但风险也更高

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

这将允许 Zyfai 自动重新分配资金。会话密钥 **仅限于在协议内部** 使用，无法将资金提取到其他地址。

> **重要提示：** 在调用 `createSessionKey` 后，务必通过 `getUserDetails().user.hasActiveSessionKey` 检查会话密钥是否处于激活状态。如果返回 `false`，请重新尝试。会话密钥必须处于激活状态才能实现自动收益优化。

### 4. 存入资金

```typescript
// Deposit 10 USDC (6 decimals)
await sdk.depositFunds(userAddress, chainId, "10000000");
```

资金从用户的 EOA 转入子账户并立即开始产生收益。

### 5. 提取资金

```typescript
// Withdraw everything
await sdk.withdrawFunds(userAddress, chainId);

// Or withdraw partial (5 USDC)
await sdk.withdrawFunds(userAddress, chainId, "5000000");
```

资金将返回到用户的 EOA。提取操作为异步处理。

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

| 方法 | 参数 | 说明 |
|--------|--------|-------------|
| `connectAccount` | `(walletClientOrProvider, chainId)` | 与 Zyfai 进行身份验证 |
| `getSmartWalletAddress` | `(userAddress, chainId)` | 获取子账户地址及状态 |
| `deploySafe` | `(userAddress, chainId, strategy)` | 创建子账户 |
| `createSessionKey` | `(userAddress, chainId)` | 启用自动优化功能 |
| `depositFunds` | `(userAddress, chainId, amount)` | 存入 USDC（保留 6 位小数） |
| `withdrawFunds` | `(userAddress, chainId, amount?)` | 提取资金（如未指定金额，则提取全部） |
| `getPositions` | `(userAddress, chainId?)` | 获取当前的 DeFi 投资组合 |
| `getAvailableProtocols` | `(chainId)` | 获取可用的 DeFi 协议及池 |
| `getAPYPerStrategy` | `(crossChain?, days?, strategyType?)` | 获取不同策略的年化收益率（APY） |
| `getUserDetails` | `()` | 获取已认证的用户信息 |
| `getOnchainEarnings` | `(walletAddress)` | 获取收益数据 |
| `updateUserProfile` | `(params)` | 更新用户配置（策略、协议、资金分配方式、跨链设置） |
| `registerAgentOnIdentityRegistry` | `(smartWallet, chainId)` | 在 ERC-8004 身份注册表中注册代理 |
| `disconnectAccount` | `()` | 结束会话 |

**注意：** 所有接受 `userAddress` 的方法都要求提供用户的 EOA 地址，而非子账户地址。

## 数据相关方法

### getPositions

获取用户在所有区块链上的活跃 DeFi 投资组合。可选择按特定区块链进行过滤。

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| userAddress | string | 是 | 用户的 EOA 地址 |
| chainId | SupportedChainId | 否 | 可选：按特定区块链 ID 过滤 |

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

获取指定区块链上的可用 DeFi 协议及池信息，包括年化收益率（APY）数据。

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

**返回值：**

```typescript
interface ProtocolsResponse {
  success: boolean;
  chainId: SupportedChainId;
  protocols: Protocol[];
}
```

### getUserDetails

获取当前已认证的用户信息，包括智能钱包信息、使用的区块链、协议及设置。需要 SIWE 身份验证。

```typescript
await sdk.connectAccount(walletClient, chainId);
const user = await sdk.getUserDetails();

console.log("Smart Wallet:", user.user.smartWallet);
console.log("Chains:", user.user.chains);
console.log("Has Active Session:", user.user.hasActiveSessionKey);
```

**返回值：**

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

更新用户的配置信息，包括策略、协议、资金分配方式及跨链设置。需要 SIWE 身份验证。

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

> **跨链策略：** 仅当用户 **明确请求** 时才启用跨链功能。要使用跨链功能，`crosschainStrategy` 和 `omniAccount` 都必须设置为 `true`。默认情况下，跨链功能是禁用的。

**注意事项：**
- **策略：** 可随时更改。后续的再平衡操作将使用新的策略。
- **协议：** 在更新前，请使用 `getAvailableProtocols(chainId)` 获取有效的协议 ID。
- **智能资金分配（minSplits = 1）：** 默认模式。系统会根据当前市场状况智能分配资金到多个 DeFi 池中以实现收益最大化；若无合适机会，则不会进行分配。
- **强制分配（minSplits > 1）：** 当 `minSplits` 设置为 2、3 或 4 时，资金会分配到至少相应数量的池中，以提高风险分散效果（最多可分配到 4 个池）。
- **跨链：** 需同时满足 `crosschainStrategy: true` 和 `omniAccount: true` 的条件。用户必须明确请求才能启用跨链功能。区块链配置在初次设置时确定，无法通过此方法更改。
- **自动复利：** 默认启用。启用后，收益会自动再投资。
- 智能钱包地址、使用的区块链及 `executorProxy` 无法通过此方法更改。

### getAPYPerStrategy

根据策略类型（保守或激进）、时间周期及区块链配置获取年化收益率（APY）。用于在部署前比较不同策略的预期收益。

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| crossChain | boolean | 否 | 如果设置为 `true`，则返回跨链策略的年化收益率；否则返回单链策略的年化收益率 |
| days | number | 否 | 计算年化收益率的时间周期（7、15、30 或 60 天） |
| strategyType | string | 否 | 策略类型（`conservative` 或 `aggressive`） |

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

获取钱包在链上的总收益、当前收益及累计收益。

```typescript
const earnings = await sdk.getOnchainEarnings(smartWalletAddress);

console.log("Total earnings:", earnings.data.totalEarnings);
console.log("Current earnings:", earnings.data.currentEarnings);
console.log("Lifetime earnings:", earnings.data.lifetimeEarnings);
```

**返回值：**

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

根据 ERC-8004 标准，在身份注册表中注册您的 Zyfai 代理。此方法用于 OpenClaw 代理的注册。它会从 IPFS 获取代理的元数据，并将其注册到链上。

**支持的区块链：**

| 区块链 | ID    |
|----------|-------|
| Base | 8453 |
| Arbitrum | 42161 |

**参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| smartWallet | string | 是 | 要注册的 Zyfai 智能钱包地址 |
| chainId | SupportedChainId | 是 | 需要注册的区块链 ID（仅限 8453 或 42161） |

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

1. 从 Zyfai API 获取代理的元数据（存储在 IPFS 上的 `tokenUri`）。
2. 将 `register(tokenUri)` 调用编码后发送到身份注册表合约。
3. 通过连接的钱包发送交易请求。
4. 等待链上的确认。

## 安全性说明：

- **非托管模式** — 子账户归用户 EOA 所有。
- **会话密钥的使用受到限制** — 仅用于资金再平衡，无法用于资金提取。
- **确定性原则**：同一 EOA 在所有区块链上对应相同的子账户。
- **灵活的密钥管理方式**：支持使用钱包提供商、WalletClient 或 KMS 等工具。

### 密钥管理最佳实践

对于 **生产环境中的自主代理**，我们建议：
1. **使用带有安全密钥管理功能的 WalletClient**（避免直接使用私钥）。
2. **结合 KMS（如 AWS KMS、GCP Cloud KMS）进行硬件加密的密钥存储**。
3. **考虑使用 Wallet-as-a-Service 服务（如 Turnkey、Privy 或 Dynamic）**。
4. **切勿在源代码中硬编码私钥**。
5. **定期轮换密钥并实施密钥撤销机制**。

## 常见问题及解决方法

### 不同区块链上的子账户地址不一致

同一 EOA 在所有区块链上的子账户地址应保持一致。如果发现地址不同，请：

```typescript
// Check addresses on both chains
const baseWallet = await sdk.getSmartWalletAddress(userAddress, 8453);
const arbWallet = await sdk.getSmartWalletAddress(userAddress, 42161);

if (baseWallet.address !== arbWallet.address) {
  console.error("Address mismatch! Contact support.");
}
```

**解决方法：**
1. 尝试在受影响的区块链上重新部署子账户。
2. 如果问题仍然存在，请通过 Telegram 联系技术支持：[@paul_zyfai](https://t.me/paul_zyfai)

### 错误提示：“Deposit address not found”

这表示钱包尚未在后台注册。解决方法：
1. 先调用 `deploySafe()` — 即使子账户已部署在链上，此操作也会将其注册到后台。
2. 然后重新尝试 `createSessionKey()`。

### 错误提示：“Invalid signature”

通常表示：
- 提供的钱包或签名者信息与用户 EOA 不匹配。
- 链上的智能钱包地址与 SDK 预期的地址不一致。

请确保使用的钱包与用户的 EOA 信息一致。

## 相关资源：

- **获取 API 密钥：** [sdk.zyf.ai](https://sdk.zyf.ai) 或通过编程方式（`POST /api/sdk-api-keys/create`）
- **文档：** [docs.zyf.ai](https://docs.zyf.ai)
- **演示版：** [github.com/ondefy/zyfai-sdk-demo](https://github.com/ondefy/zyfai-sdk-demo)
- **MCP 服务器：** [mcp.zyf.ai](https://mcp.zyf.ai/mcp) — 可与 Claude 或其他 MCP 兼容的代理工具配合使用。
- **代理注册：** [zyf.ai/.well-known/agent-registration.json](https://www.zyf.ai/.well-known/agent-registration.json)