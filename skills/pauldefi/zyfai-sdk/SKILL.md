---
name: zyfai
description: 在 Base、Arbitrum 和 Plasma 平台上，您可以通过任何以太坊钱包获得收益。当用户希望其资金产生被动收益（即无需主动操作即可获得收益）时，可以使用该功能。系统会为用户部署一个非托管子账户（Safe），该账户与用户的以太坊地址（EOA，Externally Owned Account）关联，实现自动化的收益优化，并允许用户随时进行存款和取款操作。
---

# Zyfai — 适用于任何钱包的收益生成工具

将任何以太坊钱包转换为能够产生收益的账户。

## 功能介绍

当用户希望从其持有的加密货币中获取收益时，Zyfai会为其创建一个与现有钱包（EOA，即Externally Owned Account）关联的子账户（安全智能钱包）。存入该子账户的资金会自动在各种DeFi（去中心化金融）协议中进行优化配置。用户始终拥有完全的控制权，并可以随时提取资金。

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
- 子账户由用户的EOA拥有——只有用户自己才能提取资金
- 会话密钥支持自动资金再平衡，但无法将资金提取到其他地址
- 同一EOA在所有链上对应相同的子账户地址

## 使用流程

```
1. DEPLOY    →  Create subaccount linked to user's wallet
2. SESSION   →  Enable automated yield optimization  
3. DEPOSIT   →  Send funds to subaccount (starts earning)
4. WITHDRAW  →  Pull funds back to wallet (anytime)
```

## 先决条件

- 从 [sdk.zyf.ai](https://sdk.zyf.ai) 获取 **API密钥**（用于连接钱包）
- 用户EOA的 **私钥**（必须由代理提供）
- 确保使用 **Node.js 18+** 或更高版本的开发环境

```bash
npm install @zyfai/sdk viem
```

## 支持的链

| 链      | ID     |
|---------|-------|
| Arbitrum | 42161   |
| Base     | 8453    |
| Plasma   | 9745    |

## 重要提示：始终使用EOA地址

在调用SDK方法时，**必须使用EOA地址**（即用户的钱包地址）作为 `userAddress` 参数，切勿使用子账户的地址。SDK会自动从EOA地址生成子账户地址。

## 步骤说明

### 1. 连接到Zyfai

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key" });

// Use the private key provided by the agent
await sdk.connectAccount(privateKey, 8453); // chainId
```

**重要提示：**务必使用代理有权访问的私钥。该私钥必须与你操作的EOA地址相匹配。

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
- `"conservative"`（保守型）——收益稳定，风险较低
- `"aggressive"`（激进型）——收益较高，风险也较高

### 3. 启用收益优化功能

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

这允许Zyfai自动对资金进行再平衡。会话密钥 **仅** 用于在协议内部进行资金操作，无法将资金提取到其他地址。

> **重要提示：** 在调用 `createSessionKey` 后，务必通过 `getUserDetails().user.hasActiveSessionKey` 方法检查会话密钥是否处于激活状态。如果返回 `false`，请重新尝试。只有当会话密钥处于激活状态时，收益优化功能才能正常工作。

### 4. 存入资金

```typescript
// Deposit 10 USDC (6 decimals)
await sdk.depositFunds(userAddress, chainId, "10000000");
```

资金会从用户的EOA账户转移到子账户，并立即开始产生收益。

### 5. 提取资金

```typescript
// Withdraw everything
await sdk.withdrawFunds(userAddress, chainId);

// Or withdraw partial (5 USDC)
await sdk.withdrawFunds(userAddress, chainId, "5000000");
```

资金会返回到用户的EOA账户。提取操作是异步处理的。

### 6. 断开连接

```typescript
await sdk.disconnectAccount();
```

## 完整示例

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";

async function startEarningYield(userAddress: string, privateKey: string) {
  const sdk = new ZyfaiSDK({ apiKey: process.env.ZYFAI_API_KEY! });
  const chainId = 8453; // Base
  
  // Connect using the agent's private key
  await sdk.connectAccount(privateKey, chainId);
  
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

async function withdrawYield(userAddress: string, privateKey: string, amount?: string) {
  const sdk = new ZyfaiSDK({ apiKey: process.env.ZYFAI_API_KEY! });
  const chainId = 8453; // Base
  
  // Connect using the agent's private key
  await sdk.connectAccount(privateKey, chainId);
  
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

## API参考

| 方法        | 参数        | 描述                                      |
|------------|------------|-----------------------------------------|
| `connectAccount` | `(privateKey, chainId)` | 用于与Zyfai进行身份验证                   |
| `getSmartWalletAddress` | `(userAddress, chainId)` | 获取子账户地址及状态                        |
| `deploySafe`    | `(userAddress, chainId, strategy)` | 创建子账户                                   |
| `createSessionKey` | `(userAddress, chainId)` | 启用自动优化功能                         |
| `depositFunds` | `(userAddress, chainId, amount)` | 存入USDC（保留6位小数）                        |
| `withdrawFunds` | `(userAddress, chainId, amount?)` | 提取资金（未指定金额时提取全部）                   |
| `getPositions` | `(userAddress, chainId?)` | 获取用户的所有DeFi投资位置                    |
| `getAvailableProtocols` | `(chainId)` | 获取可用的DeFi协议及池                         |
| `getAPYPerStrategy` | `(crossChain?, days?, strategyType?)` | 获取不同策略的年化收益率（APY）                |
| `getUserDetails` | `()`         | 获取已认证用户的详细信息                         |
| `getOnchainEarnings` | `(walletAddress)` | 获取用户的链上收益数据                         |
| `updateUserProfile` | `(params)`      | 更新用户的策略、协议、资金分配及跨链设置                 |
| `registerAgentOnIdentityRegistry` | `(smartWallet, chainId)` | 在ERC-8004身份注册表中注册代理                    |
| `disconnectAccount` | `()`         | 断开与Zyfai的连接                         |

**注意：** 所有接受 `userAddress` 参数的方法都要求提供用户的EOA地址，而非子账户的地址。

## 数据相关方法

### getPositions

获取用户在所有DeFi协议中的所有投资位置。可选地按链进行过滤。

**参数：**
- `userAddress` | string      | ✅         | 用户的EOA地址                         |
- `chainId`     | SupportedChainId | ❌         | 可选：按特定链ID进行过滤                         |

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

获取指定链上可用的DeFi协议及池，并提供相应的年化收益率（APY）数据。

**返回值：**

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

### getUserDetails

获取当前已认证用户的详细信息，包括智能钱包信息、使用的链、投资协议及设置。需要SIWE身份验证。

**返回值：**

```typescript
await sdk.connectAccount(privateKey, chainId);
const user = await sdk.getUserDetails();

console.log("Smart Wallet:", user.user.smartWallet);
console.log("Chains:", user.user.chains);
console.log("Has Active Session:", user.user.hasActiveSessionKey);
```

### updateUserProfile

更新用户的个人资料设置，包括投资策略、协议、资金分配及跨链选项。需要SIWE身份验证。

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

> **跨链策略：** 仅当用户 **明确请求** 时才启用跨链功能。要实现跨链操作，`crosschainStrategy` 和 `omniAccount` 两个参数都必须设置为 `true`。默认情况下，跨链功能是禁用的。

**注意事项：**
- **投资策略：** 可以随时更改。后续的资金再平衡将使用新的策略。
- **协议选择：** 在更新之前，请使用 `getAvailableProtocols(chainId)` 方法获取有效的协议ID。
- **智能资金分配（minSplits = 1）：** 默认模式。系统会根据当前市场状况和机会智能分配资金到多个DeFi池中，以最大化收益。如果没有合适的投资机会，资金可能不会被分配。
- **强制资金分配（minSplits > 1）：** 当 `minSplits` 设置为2、3或4时，资金会至少分配到4个DeFi池中，以实现更好的风险分散。无论市场状况如何，系统都会确保资金被分配。
- **跨链功能：** 需要同时满足 `crosschainStrategy: true` 和 `omniAccount: true` 的条件。用户必须明确启用跨链功能。链的配置在初次设置时确定，之后无法通过此方法更改。
- **自动复利：** 默认情况下启用。启用后，收益会自动再投资。
- 智能钱包地址、使用的链及 `executorProxy` 无法通过此方法进行更改。

### getAPYPerStrategy

根据策略类型（保守型或激进型）、时间周期及链配置，获取相应的年化收益率（APY）。在部署新策略前，可以使用此方法比较不同策略的预期收益。

**参数：**
- `crossChain` | boolean     | ❌         | 如果设置为 `true`，则返回跨链策略的APY；否则返回单链策略的APY       |
- `days`    | number       | ❌         | 计算APY的时间周期（7、15、30或60天）                 |
- `strategyType` | string      | ❌         | 投资策略类型（`conservative` 或 `aggressive`）           |

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

获取钱包的链上收益数据，包括累计收益、当前收益及总收益。

**返回值：**

```typescript
const earnings = await sdk.getOnchainEarnings(smartWalletAddress);

console.log("Total earnings:", earnings.data.totalEarnings);
console.log("Current earnings:", earnings.data.currentEarnings);
console.log("Lifetime earnings:", earnings.data.lifetimeEarnings);
```

### registerAgentOnIdentityRegistry (ERC-8004)

根据ERC-8004标准，在身份注册表中注册你的Zyfai代理。此方法用于OpenClaw代理的注册。它会从IPFS获取代理的元数据，并将其注册到链上。

**支持的链：**
- Base      | 8453       |
- Arbitrum    | 42161      |

**参数：**
- `smartWallet` | string      | ✅         | 要注册的Zyfai智能钱包地址                     |
- `chainId`     | SupportedChainId | ✅         | 需要注册的链ID（仅限8453或42161）                     |

**示例：**

```typescript
const sdk = new ZyfaiSDK({ apiKey: "your-api-key" });
await sdk.connectAccount(privateKey, 8453);

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

1. 从Zyfai API获取代理的元数据（存储在IPFS上）。
2. 将 `register(tokenUri)` 请求编码后发送到身份注册表合约。
3. 通过连接的钱包发送交易请求。
4. 等待链上的确认结果。

## 安全性说明

- **非托管模式**——用户的EOA拥有子账户的所有权。
- **会话密钥的使用受到限制**——仅可用于资金再平衡，无法用于资金提取。
- **确定性原则**——同一EOA在所有链上的子账户地址始终相同。

## 常见问题解决方法

### 不同链上的子账户地址不一致

对于同一EOA，所有链上的子账户地址应该 **完全相同**。如果发现地址不一致，请：
```typescript
// Check addresses on both chains
const baseWallet = await sdk.getSmartWalletAddress(userAddress, 8453);
const arbWallet = await sdk.getSmartWalletAddress(userAddress, 42161);

if (baseWallet.address !== arbWallet.address) {
  console.error("Address mismatch! Contact support.");
}
```

**解决方法：**
1. 尝试在受影响的链上重新部署子账户。
2. 如果问题仍然存在，请通过Telegram联系支持团队：[@paul_zyfai](https://t.me/paul_zyfai)

### 出现“Deposit address not found”错误

这表示钱包尚未在后台系统中注册。解决方法：
1. 先调用 `deploySafe()` 方法——即使子账户已经部署在链上，此步骤也能完成注册。
2. 然后重新尝试 `createSessionKey()` 方法。

### 出现“Invalid signature”错误

通常意味着：
- 提供的私钥与用户的EOA地址不匹配。
- 链上的智能钱包地址与SDK期望的地址不一致。

请确认你使用的私钥与用户的EOA地址相匹配。

## 相关资源

- 获取API密钥：[sdk.zyf.ai](https://sdk.zyf.ai)
- 文档：[docs.zyf.ai](https://docs.zyf.ai)
- 示例代码：[github.com/ondefy/zyfai-sdk-demo](https://github.com/ondefy/zyfai-sdk-demo)