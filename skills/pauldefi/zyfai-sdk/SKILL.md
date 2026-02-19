---
name: zyfai
description: 在 Base、Arbitrum 和 Plasma 平台上，用户可以通过任何以太坊钱包获得收益。当用户希望其资金产生被动收益（即无需主动操作即可获得收益）时，可以使用该功能。系统会为用户部署一个非托管的子账户（Safe），该子账户与用户的以太坊地址（EOA）关联，并自动优化收益获取过程，同时用户可以随时进行存款和取款操作。
---
# Zyfai — 为任何钱包提供收益生成功能

将任何以太坊钱包转换为能够产生收益的账户。

## 功能介绍

当用户希望从他们的加密货币中获取收益时，Zyfai会为他们现有的钱包（EOA，Externally Owned Account）创建一个**子账户**（安全的智能钱包）。存入该子账户的资金会自动在各种DeFi协议中进行优化配置。用户始终保持完全控制权，并可以随时提取资金。

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
- 子账户**由用户的EOA拥有**——只有用户自己才能提取资金
- 会话密钥支持**自动再平衡**，但无法将资金提取到其他地址
- 同一EOA在所有链上对应相同的子账户地址

## 使用流程

```
1. DEPLOY    →  Create subaccount linked to user's wallet
2. SESSION   →  Enable automated yield optimization  
3. DEPOSIT   →  Send funds to subaccount (starts earning)
4. WITHDRAW  →  Pull funds back to wallet (anytime)
```

## 先决条件

- **API密钥**——可以通过编程方式获取（详见下文），或手动从 [sdk.zyf.ai](https://sdk.zyf.ai) 获取
- 用户EOA的**私钥**（必须由代理提供）
- **Node.js 18+** 版本

```bash
npm install @zyfai/sdk viem
```

### 程序化生成API密钥（代理端）

代理可以无需人工干预自行生成API密钥：

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

> **重要提示：** 请安全保管API密钥——一旦生成，将无法再次获取。该密钥与提供的钱包地址相关联。

## 支持的链

| 链      | ID     |
|---------|-------|
| Arbitrum | 42161   |
| Base     | 8453    |
| Plasma   | 9745    |

## 重要提示：始终使用EOA地址

在调用SDK方法时，**务必使用EOA地址**（即用户的钱包地址）作为 `userAddress` 参数——切勿使用子账户或Safe钱包的地址。SDK会自动从EOA地址推导出子账户地址。

## 分步操作

### 1. 连接Zyfai

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// Use the private key provided by the agent
await sdk.connectAccount(privateKey, 8453); // chainId
```

**重要提示：** 请始终使用代理有权访问的私钥。该私钥必须与你要操作的EOA地址相匹配。

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

这允许Zyfai自动重新分配资金。会话密钥**不能**将资金提取到任意地址——只能在协议内部进行资金优化。

> **重要提示：** 在调用 `createSessionKey` 后，务必通过 `getUserDetails().user.hasActiveSessionKey` 方法验证会话密钥是否处于激活状态。如果返回 `false`，请重新尝试。只有当会话密钥处于激活状态时，自动收益优化功能才能生效。

### 4. 存入资金

```typescript
// Deposit 10 USDC (6 decimals)
await sdk.depositFunds(userAddress, chainId, "10000000");
```

资金从EOA账户转移到子账户，并立即开始产生收益。

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

| 方法        | 参数            | 描述                                      |
|------------|-----------------|-----------------------------------------|
| `connectAccount` | `(privateKey, chainId)`    | 与Zyfai进行身份验证                        |
| `getSmartWalletAddress` | `(userAddress, chainId)`    | 获取子账户地址及状态                        |
| `deploySafe`     | `(userAddress, chainId, strategy)` | 创建子账户                                      |
| `createSessionKey` | `(userAddress, chainId)`    | 启用自动优化功能                              |
| `depositFunds` | `(userAddress, chainId, amount)` | 存入USDC（保留6位小数）                        |
| `withdrawFunds` | `(userAddress, chainId, amount?)` | 提取资金（如未指定金额，则提取全部）                   |
| `getPositions` | `(userAddress, chainId?)`    | 获取当前的DeFi投资组合                         |
| `getAvailableProtocols` | `(chainId)`      | 获取可用的DeFi协议及池                         |
| `getAPYPerStrategy` | `(crossChain?, days?, strategyType?)` | 获取保守型/激进型策略的年化收益率（APY）           |
| `getUserDetails` | `()`            | 获取已认证用户的详细信息                        |
| `getOnchainEarnings` | `(walletAddress)`      | 获取用户在链上的收益数据                        |
| `updateUserProfile` | `(params)`        | 更新用户的策略、协议、资金分配及跨链设置                   |
| `registerAgentOnIdentityRegistry` | `(smartWallet, chainId)` | 在ERC-8004身份注册表中注册代理                     |
| `disconnectAccount` | `()`            | 结束当前会话                                  |

**注意：** 所有接受 `userAddress` 参数的方法都要求提供**EOA地址**，而非子账户或Safe钱包的地址。

## 数据相关方法

### getPositions

获取用户在所有链上的活跃DeFi投资组合。可选择按链进行过滤。

**参数：**

| 参数          | 类型            | 是否必填            | 描述                                      |
|---------------|-----------------|-----------------------------------------|
| userAddress     | string          | ✅               | 用户的EOA地址                               |
| chainId        | SupportedChainId     | ❌             | 可选：按特定链ID过滤                         |

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

获取特定链上可用的DeFi协议及池，并显示年化收益率（APY）数据。

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

获取当前已认证用户的详细信息，包括智能钱包信息、所使用的链、协议及设置。需要SIWE认证。

```typescript
await sdk.connectAccount(privateKey, chainId);
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

更新已认证用户的配置信息，包括策略、协议、资金分配及跨链设置。需要SIWE认证。

**参数：**

```typescript
sdk.updateUserProfile(params: UpdateUserProfileRequest): Promise<UpdateUserProfileResponse>
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

> **跨链策略：** 仅当用户**明确请求**时才启用跨链功能。要使用跨链功能，`crosschainStrategy` 和 `omniAccount` 两个参数都必须设置为 `true`。默认情况下，跨链功能是禁用的。

**注意事项：**
- **策略：** 可以随时更改。后续的资金再平衡操作将使用新的策略。
- **协议：** 在更新前，请使用 `getAvailableProtocols(chainId)` 获取有效的协议ID。
- **智能资金分配（minSplits = 1）：** 默认模式。系统会根据当前市场状况和机会自动将资金分配到多个DeFi池中，以最大化收益。如果没有合适的投资机会，资金可能不会被分配。
- **强制资金分配（minSplits > 1）：** 当 `minSplits` 设置为2、3或4时，资金会至少分配到相应数量的池中，以实现更好的风险分散。无论市场状况如何，系统都会确保资金被分配。
- **跨链功能：** 需要同时满足 `crosschainStrategy: true` 和 `omniAccount: true` 的条件。用户必须明确请求才能启用跨链收益优化。链的配置在初次设置时确定，之后无法通过此方法更改。
- **自动复利：** 默认启用。如果设置为 `true`，收益会自动再投资。
- 智能钱包地址、链及 `executorProxy` 无法通过此方法进行更新。

### getAPYPerStrategy

根据策略类型（保守型或激进型）、时间周期和链配置，获取全球年化收益率（APY）。在部署前，可以使用此方法比较不同策略的预期收益。

**参数：**

| 参数          | 类型            | 是否必填            | 描述                                      |
|---------------|-----------------|-----------------------------------------|
| crossChain     | boolean         | ❌             | 如果设置为 `true`，则返回跨链策略的APY；否则返回单链策略的APY     |
| days          | number           | ❌             | 计算APY的时间周期（7、15、30或60天）                     |
| strategyType     | string          | ❌             | 策略的风险类型（`conservative` 或 `aggressive`）           |

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

**返回值：**

```typescript
const earnings = await sdk.getOnchainEarnings(smartWalletAddress);

console.log("Total earnings:", earnings.data.totalEarnings);
console.log("Current earnings:", earnings.data.currentEarnings);
console.log("Lifetime earnings:", earnings.data.lifetimeEarnings);
```

### registerAgentOnIdentityRegistry (ERC-8004)

根据ERC-8004标准，在身份注册表中注册你的Zyfai代理。此方法用于OpenClaw代理的注册。它会从IPFS获取代理的元数据（存储为`tokenUri`），然后在链上完成注册。

**支持的链：**

| 链      | Chain ID     |
|---------|----------|-----------------------------------------|
| Base     | 8453       |                                              |
| Arbitrum | 42161     |                                              |

**参数：**

| 参数          | 类型            | 是否必填            | 描述                                      |
| smartWallet    | string          | ✅             | 要注册为代理的Zyfai智能钱包地址                         |
| chainId     | SupportedChainId     | ✅             | 链ID（仅支持8453或42161）                         |

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

1. 从Zyfai API获取代理的元数据（存储在IPFS上），生成`tokenUri`。
2. 将 `register(tokenUri)` 请求编码后发送到身份注册表合约。
3. 通过连接的钱包发送交易请求。
4. 等待链上的确认结果。

## 安全性

- **非托管模式**——用户的EOA拥有子账户的所有权。
- **会话密钥的使用受到限制**——仅可用于资金再平衡，无法用于其他操作。
- **确定性**——同一EOA在所有链上对应相同的子账户地址。

## 故障排除

### 不同链上的子账户地址不匹配

对于同一EOA，所有链上的子账户地址应该**完全一致**。如果发现地址不一致：

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

这意味着钱包尚未在后台注册。解决方法：
1. 先调用 `deploySafe()`——即使子账户已经部署在链上，此操作也会将其注册到后台。
2. 然后重新尝试调用 `createSessionKey()`。

### 出现“Invalid signature”错误

通常表示：
- 提供的私钥与用户的EOA不匹配。
- 链上的Safe钱包地址与SDK预期的地址不一致。

请确认你使用的私钥与用户的EOA地址相匹配。

## 资源链接

- **获取API密钥：** [sdk.zyf.ai](https://sdk.zyf.ai) 或通过 `POST /api/sdk-api-keys/create` 程序化获取
- **文档：** [docs.zyf.ai](https://docs.zyf.ai)
- **演示版本：** [github.com/ondefy/zyfai-sdk-demo](https://github.com/ondefy/zyfai-sdk-demo)
- **MCP服务器：** [mcp.zyf.ai](https://mcp.zyf.ai/mcp)——可与Claude或其他兼容的代理工具配合使用
- **代理注册：** [zyf.ai/.well-known/agent-registration.json](https://www.zyf.ai/.well-known/agent-registration.json)