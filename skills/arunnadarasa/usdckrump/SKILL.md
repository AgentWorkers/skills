---
name: usdc-dance-evvm-payment
description: >
  **使用 USDC Krump (USDC.k) 通过 x402 在 Story Aeneid EVVM 上进行支付**  
  该功能支持 EVVM 的原生适配器（token 上不使用 EIP-3009 协议），同时也支持旧的 Bridge 适配器。支付过程中需要提供 `PRIVY_APP_ID` 和 `PRIVY_APP_SECRET`（对于旧路径来说，这些信息代表私钥）。这些凭据由用户自行提供，不会被该技能程序存储。
version: 1.2.0
author: OpenClaw USDC Krump
tags: [payment, evvm, x402, usdc, layerzero, story-aeneid, openclaw, privy, bridge, usdc-krump]
requires: [privy]
---
# USDC Krump（USDC.k）支付技能

该技能允许OpenClaw代理通过**x402协议**在**Story Aeneid EVVM**上使用**USDC Krump（USDC.k）**进行支付，支持使用**Privy服务器钱包**或私钥。

## 使用范围

本技能提供了通过x402协议在Story Aeneid上进行USDC Krump（USDC.k）支付的**说明和参数参考**。可执行代码、示例和脚本（例如EVVM存款、双代理流程）均位于完整的[USDC Krump仓库](https://github.com/arunnadarasa/usdckrump)中；请使用该仓库来运行脚本或集成支付逻辑。只有在用户明确请求支付并且配置了所需凭据的情况下，才能创建钱包或发起支付。

## 所需凭据

该技能**不存储或提供**凭据。您必须提供以下其中一种方式：

- **Privy（推荐）**：设置`PRIVY_APP_ID`和`PRIVY_APP_SECRET`（例如，在`~/.openclaw/openclaw.json`的`env_vars`中，或作为环境变量）。这些信息可以从[dashboard.privy.io](https://dashboard.privy.io)获取。
- **旧版/私钥**：对于旧的`payViaEVVM`路径，必须提供付款人的私钥（例如`AGENT_PRIVATE_KEY`）。建议使用Privy管理的钱包，尽量避免将私钥存储在明文环境变量中。

## 功能特点

- ✅ **Privy集成**：支持使用Privy服务器钱包进行代理交易
- ✅ **x402协议**：采用EIP-3009风格的认证；支持**EVVM原生适配器**（Core内部余额）或旧版适配器（EIP-3009）
- ✅ **EVVM集成**：通过EVVM Core（ID 1140）进行支付路由
- ✅ **EVVM存款**：提供将USDC.k存入EVVM Treasury的脚本，以便付款人拥有用于原生适配器的内部余额
- ✅ **双代理示例**：支持直接x402、旧版适配器和**原生适配器**（`two-agents-x402-native.ts`）
- ✅ **基于策略的安全性**：通过Privy策略设置消费限制和防护措施
- ✅ **收款跟踪**：`checkPaymentStatus(receiptId, adapterAddress, rpcUrl)`

## 先决条件

1. **Privy账户**（对于使用Privy路径的情况）：从[dashboard.privy.io](https://dashboard.privy.io)获取凭据。
2. 已安装**Privy技能**：使用`clawhub install privy`命令进行安装。
3. 配置OpenClaw：添加所需的凭据（见上述**所需凭据**部分）。对于Privy，需将其添加到`~/.openclaw/openclaw.json`中：

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

### 在使用原生适配器之前进行EVVM存款

EVVM Core会处理**内部账本余额**，但不会从钱包中提取代币。对于**EVVM原生x402适配器**，付款人必须先向EVVM存款USDC.k。请在完整的[USDC Krump仓库](https://github.com/arunnadarasa/usdckrump)中运行相关命令：

```bash
cd lz-bridge
PRIVATE_KEY=0x<payer_key> DEPOSIT_AMOUNT=1000000 npm run evvm:deposit-usdck
```

之后，可以使用`useNativeAdapter: true`并设置相应的原生适配器地址。

### 选项1：使用Privy钱包（推荐）

代码参考（请在您的环境中实现，或使用仓库的`src/`目录中的代码）：

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

### 选项2：使用私钥（旧版）

代码参考（运行时请使用仓库的`src/`目录中的代码）：

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

在完整的[USDC Krump仓库]中运行以下命令：

```bash
AGENT_A_PRIVATE_KEY=0x... AGENT_B_ADDRESS=0x... npx tsx examples/two-agents-x402-native.ts
```

有关直接x402和旧版适配器的流程，请参阅仓库中的`examples/README-two-agents-x402.md`文件。

## 配置

### 所需地址（Story Aeneid测试网）

- **EVVM Core**：`0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b`
- **EVVM ID**：`1140`
- **USDC.k（BridgeUSDC）**：`0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5`
- **EVVM原生x402适配器**：`0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc` — 使用`useNativeAdapter: true`时需要先存款
- **Bridge EVVM适配器（旧版）**：`0x00ed0E80E5EAE285d98eC50236aE97e2AF615314` — 使用EIP-3009协议

### 网络详情

- **链**：Story Aeneid测试网
- **链ID**：`1315`
- **原生货币**：IP
- **RPC**：`https://aeneid.storyrpc.io`

## Privy集成

该技能与[Privy OpenClaw技能](https://docs.privy.io/recipes/agent-integrations/openclaw-agentic-wallets)集成，支持以下功能：

- **自主钱包管理**：代理可以拥有自己的Privy服务器钱包
- **基于策略的安全性**：使用Privy策略设置消费限制、限制链或白名单合约
- **无需存储私钥**：Privy负责安全地管理密钥
- **交易签名**：Privy通过API处理EIP-3009和EIP-191签名

### 为您的代理创建Privy钱包

请指示您的OpenClaw代理执行以下操作：

> “在Story Aeneid测试网上使用Privy为您创建一个以太坊钱包”

代理将创建一个Privy服务器钱包，并返回钱包ID。

### 设置策略

设置消费限制和规则：

> “创建一个Privy策略，将每次交易的USDC Krump（USDC.k）支付金额限制在10 USDC.k以内”
> “将此消费限制策略应用到我的Privy钱包”

## 函数

### `payViaEVVMWithPrivy(options)`

使用Privy钱包通过x402协议处理支付。

**参数：**
- `walletId`、`to`、`toIdentity`、`amount`、`receiptId`、`adapterAddress`、`usdcDanceAddress`、`evvmCoreAddress`、`evvmId`、`rpcUrl`（参见选项1的示例）
- `useNativeAdapter`：设置为`true`以使用EVVM原生x402适配器（付款人必须先通过Treasury存款USDC.k）
- `privyAppId`、`privyAppSecret`：可选；如果未提供，请使用环境变量

**返回值**：交易收据

### `payViaEVVM(options)`（旧版）

直接使用私钥处理支付（不建议在生产环境中使用）。

### `checkPaymentStatus(receiptId, adapterAddress, rpcUrl)`

检查支付是否成功处理。

## 示例

在完整的[USDC Krump仓库](https://github.com/arunnadarasa/usdckrump)的`examples/`目录中，可以找到以下示例：

- `two-agents-x402-native.ts` — 使用EVVM原生适配器的双代理示例（推荐）
- `two-agents-x402-simulation.ts` — 使用旧版Bridge适配器的双代理示例
- `two-agents-x402-direct.ts` — 直接使用x402协议的传输示例
- `agent-payment-privy-example.ts` — 使用Privy钱包的示例
- `agent-payment-example.ts` — 使用私钥的示例（旧版）

有关EVVM存款步骤和所有流程的详细信息，请参阅仓库中的`examples/README-two-agents-x402.md`文件。

## 安全注意事项

凭据**仅由用户提供**；该技能不会存储或传输任何敏感信息。只有在用户明确请求支付并且您已配置了所需凭据的情况下，才能创建钱包或发起支付（见**所需凭据**部分）。

⚠️ **使用Privy钱包时**：

1. **设置策略**：始终配置消费限制和规则（例如每次交易的最大金额、允许的链/合约）。
2. **先进行测试**：在主网或使用实际资金之前，先在测试网上进行测试并使用少量资金。
3. **监控活动**：定期检查Privy控制台中的钱包活动。
4. **定期更换凭据**：如果凭据被泄露，请立即更换Privy App Secret。
5. **优先使用Privy钱包**：建议使用Privy管理的钱包，避免直接存储私钥。

## 系统要求

- Node.js 18+版本及ethers.js v6（从完整仓库运行代码时）
- 已安装**Privy技能**：使用`clawhub install privy`命令进行安装
- 具备访问Story Aeneid RPC端点的权限
- 所需凭据：`PRIVY_APP_ID`和`PRIVY_APP_SECRET`（使用Privy路径时），或付款人的私钥（使用旧版路径时）

## 许可证

MIT许可证