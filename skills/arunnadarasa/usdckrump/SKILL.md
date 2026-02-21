---
name: usdc-dance-evvm-payment
description: 通过 Story Aeneid EVVM 的 x402 协议使用 USDC Krump (USDC.k) 进行支付。该协议支持 EVVM 的原生适配器（Token 上未启用 EIP-3009），同时也支持旧的 Bridge 适配器。支持使用私钥（Privy Key）进行交易。
version: 1.2.0
author: OpenClaw USDC Krump
tags: [payment, evvm, x402, usdc, layerzero, story-aeneid, openclaw, privy, bridge, usdc-krump]
requires: [privy]
---
# USDC Krump（USDC.k）EVVM支付功能

该功能允许OpenClaw代理通过**x402协议**在**Story Aeneid EVVM**上使用**USDC Krump（USDC.k）**进行支付，支持使用**Privy服务器钱包**或私钥。

## 主要特性

- ✅ **Privy集成**：支持使用Privy服务器钱包进行自主交易
- ✅ **x402协议**：采用EIP-3009风格的认证机制；支持**EVVM原生适配器**（直接使用核心账户余额）或传统适配器（通过token进行EIP-3009通信）
- ✅ **EVVM集成**：通过EVVM Core（ID 1140）进行支付路由
- ✅ **EVVM存款**：提供脚本将USDC.k存入EVVM Treasury，以便支付方拥有可用于原生适配器的账户余额
- ✅ **双代理示例**：包含直接使用x402协议、传统适配器以及原生适配器的示例代码（`two-agents-x402-native.ts`）
- ✅ **基于策略的安全性**：支持设置支出限制和防护机制
- ✅ **交易状态查询**：提供`checkPaymentStatus(receiptId, adapterAddress, rpcUrl)`函数来查询交易状态

## 先决条件

1. **Privy账户**：请从[dashboard.privy.io](https://dashboard.privy.io)获取账户凭证
2. **已安装Privy插件**：执行`clawhub install privy`命令进行安装
3. **OpenClaw配置**：需将Privy账户信息添加到`~/.openclaw/openclaw.json`文件中：

```json
{
  "env": {
    "vars": {
      "PRIVY_APP_ID": "your-app-id",
      "PRIVY_APP_SECRET": "your-app-secret"
    }
  }
}
```

## 快速入门

### 在使用原生适配器之前先进行EVVM存款

EVVM Core会直接操作账户的**内部余额**，而不会从钱包中提取token。对于**EVVM原生x402适配器**，支付方必须先向EVVM中存入USDC.k（操作步骤见`lz-bridge`文件）：

```bash
cd lz-bridge
PRIVATE_KEY=0x<payer_key> DEPOSIT_AMOUNT=1000000 npm run evvm:deposit-usdck
```

之后，可以设置`useNativeAdapter: true`并使用相应的原生适配器地址。

### 选项1：使用Privy钱包（推荐）

```typescript
import { payViaEVVMWithPrivy } from './src/index';

// EVVM Native adapter (no EIP-3009 on token; payer must have deposited USDC.k via Treasury)
const receipt = await payViaEVVMWithPrivy({
  walletId: 'privy-wallet-id',
  to: recipientAddress,
  amount: '1000000', // 1 USDC.k (6 decimals)
  receiptId: 'payment_123',
  adapterAddress: '0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc', // EVVM Native x402 adapter
  usdcDanceAddress: '0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5', // USDC.k (BridgeUSDC)
  evvmCoreAddress: '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b',
  evvmId: 1140,
  rpcUrl: 'https://aeneid.storyrpc.io',
  useNativeAdapter: true,
});
```

### 选项2：使用私钥（传统方式）

```typescript
import { payViaEVVM } from './src/index';

const receipt = await payViaEVVM({
  from: agentAddress,
  to: recipientAddress,
  amount: '1000000',
  receiptId: 'payment_123',
  privateKey: agentPrivateKey,
  adapterAddress: '0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc', // Native adapter
  usdcDanceAddress: '0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5',
  evvmCoreAddress: '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b',
  evvmId: 1140,
  rpcUrl: 'https://aeneid.storyrpc.io',
  useNativeAdapter: true,
});
```

### 双代理原生示例

```bash
AGENT_A_PRIVATE_KEY=0x... AGENT_B_ADDRESS=0x... npx tsx examples/two-agents-x402-native.ts
```

详细示例代码请参见`examples/README-two-agents-x402.md`文件。

## 配置信息

### 必需的地址（Story Aeneid测试网）

- **EVVM Core**：`0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b`
- **EVVM ID**：`1140`
- **USDC.k（BridgeUSDC）**：`0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5`
- **EVVM原生x402适配器**：`0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc` — 使用`useNativeAdapter: true`时需要先存入USDC.k
- **Bridge EVVM适配器（传统方式）**：`0x00ed0E80E5EAE285d98eC50236aE97e2AF615314` — 通过token进行EIP-3009通信

### 网络设置

- **链**：Story Aeneid测试网
- **链ID**：`1315`
- **原生货币**：IP
- **RPC**：`https://aeneid.storyrpc.io`

## Privy集成

该功能与[Privy OpenClaw插件](https://docs.privy.io/recipes/agent-integrations/openclaw-agentic-wallets)集成，提供以下优势：

- **自主钱包管理**：代理可以拥有自己的Privy服务器钱包
- **基于策略的安全性**：支持设置支出限制、限制可访问的链或白名单合约
- **无需存储私钥**：Privy负责安全地管理私钥
- **交易签名**：Privy通过API生成EIP-3009和EIP-191格式的交易签名

### 为代理创建Privy钱包

命令示例：

> “在Story Aeneid测试网上使用Privy为你的代理创建一个以太坊钱包”

代理将创建一个Privy服务器钱包，并返回钱包ID。

### 设置策略

可以设置支出限制，例如：

> “创建一个策略，限制每次交易使用USDC Krump（USDC.k）的金额不超过10 USDC.k”
> “将此支出限制策略应用到我的Privy钱包”

## 函数说明

### `payViaEVVMWithPrivy(options)`

使用Privy钱包通过x402协议处理支付请求：

**参数：**
- `walletId`：钱包ID
- `to`：收款方地址
- `toIdentity`：收款方身份
- `amount`：支付金额
- `receiptId`：交易收据ID
- `adapterAddress`：适配器地址
- `usdcDanceAddress`：相关地址
- `evvmCoreAddress`：EVVM Core地址
- `evvmId`：EVVM ID
- `rpcUrl`：RPC端点地址（参见选项1的示例）
- `useNativeAdapter`：设置为`true`时，表示使用EVVM原生适配器（支付方需先存入USDC.k）
- `privyAppId`、`privyAppSecret`：可选参数；如未提供则使用环境变量

**返回值**：交易收据

### `payViaEVVM(options)`（传统方式）

使用私钥直接处理支付请求（不推荐在生产环境中使用）

### `checkPaymentStatus(receiptId, adapterAddress, rpcUrl)`

用于查询交易是否已成功处理

## 示例代码

详细示例代码请参见`examples/`目录：
- `two-agents-x402-native.ts`：使用EVVM原生适配器的示例
- `two-agents-x402-simulation.ts`：使用传统桥接适配器的示例
- `two-agents-x402-direct.ts`：直接使用x402协议的示例
- `agent-payment-privy-example.ts`：使用Privy钱包的示例
- `agent-payment-example.ts`：使用私钥的示例

有关EVVM存款步骤及完整流程，请参阅`examples/README-two-agents-x402.md`文件。

## 安全注意事项

⚠️ **重要提示**：
- 使用Privy钱包时，请务必：
  - 设置合理的支出限制
  - 在生产环境使用前先在测试网上进行测试
  - 定期检查钱包活动
  - 如果私钥被盗，立即更换Privy App Secret

## 系统要求

- Node.js 18及以上版本
- ethers.js v6
- 已安装Privy插件（`clawhub install privy`）
- 具备访问Story Aeneid RPC端点的权限
- 拥有Privy账户及相应的App ID和App Secret

## 许可证

MIT许可证