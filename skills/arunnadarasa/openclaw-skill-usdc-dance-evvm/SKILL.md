---
name: usdc-dance-evvm-payment
description: 使用 Privy 服务器钱包，通过 x402 协议使用 USDC.d 在 Story Aeneid EVVM 上进行支付。在 LayerZero 支持 Story Aeneid 之前，将使用 BridgeUSDC（自定义桥接工具）进行转账。
version: 1.1.0
author: LayerZero Story Aeneid Integration
tags: [payment, evvm, x402, usdc, layerzero, story-aeneid, openclaw, privy, bridge]
requires: [privy]
---
# USDC.d EVVM支付功能

该功能允许OpenClaw代理通过**x402协议**在**Story Aeneid EVVM**上使用**USDC.d**（USDC Dance）代币进行自动支付，且支付过程依赖于**Privy服务器钱包**。

## 主要特性

- ✅ **Privy集成**：使用Privy服务器钱包进行代理的自主交易
- ✅ **支持x402协议**：通过EIP-3009 `transferWithAuthorization`实现无需gas的支付
- ✅ **EVVM集成**：通过EVVM Core实现无缝的支付路由
- ✅ **自动支付**：代理之间可以无需人工干预即可相互支付
- ✅ **Story Aeneid上的USDC.d**：通过自定义桥接器（Base Sepolia → Story Aeneid）支持USDC.d；当LayerZero支持Story Aeneid时，可使用LayerZero路径
- ✅ **基于策略的安全性**：利用Privy的策略来控制交易行为
- ✅ **交易记录追踪**：提供支付收据以供验证和会计使用

## 先决条件

1. **Privy账户**：从[dashboard.privy.io](https://dashboard.privy.io)获取账户凭证
2. **已安装Privy插件**：执行`clawhub install privy`
3. **OpenClaw配置**：将Privy账户凭证添加到`~/.openclaw/openclaw.json`文件中：

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

### 选项1：使用Privy钱包（推荐）

```typescript
import { payViaEVVMWithPrivy } from './src/index';

// Agent makes payment using Privy wallet (Bridge USDC.d on Story Aeneid testnet)
const receipt = await payViaEVVMWithPrivy({
  walletId: 'privy-wallet-id',
  to: humanOwnerAddress,
  amount: '1000000', // 1 USDC.d (6 decimals)
  receiptId: 'payment_123',
  adapterAddress: '0x00ed0E80E5EAE285d98eC50236aE97e2AF615314', // Bridge EVVM adapter
  usdcDanceAddress: '0x5f7aEf47131ab78a528eC939ac888D15FcF40C40', // BridgeUSDC
  evvmCoreAddress: '0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b',
  evvmId: 1140,
  rpcUrl: 'https://aeneid.storyrpc.io'
});
```

### 选项2：使用私钥（旧版本）

```typescript
import { payViaEVVM } from './src/index';

const receipt = await payViaEVVM({
  from: agentAddress,
  to: humanOwnerAddress,
  amount: '1000000',
  receiptId: 'payment_123',
  privateKey: agentPrivateKey,
  adapterAddress: '0x00ed0E80E5EAE285d98eC50236aE97e2AF615314', // Bridge EVVM adapter
  usdcDanceAddress: '0x5f7aEf47131ab78a528eC939ac888D15FcF40C40', // BridgeUSDC
  // ... other options
});
```

## 配置

### 所需地址（Story Aeneid测试网）

- **EVVM Core**：`0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b`
- **EVVM ID**：`1140`
- **USDC.d代币（桥接器）**：`0x5f7aEf47131ab78a528eC939ac888D15FcF40C40` — 用于BridgeUSDC（在LayerZero支持Story Aeneid之前使用）
- **支付适配器（桥接器）**：`0x00ed0E80E5EAE285d98eC50236aE97e2AF615314` — 用于BridgeUSDC的EVVMPaymentAdapter

**当LayerZero支持Story Aeneid时**：您可以切换到LayerZero的USDC.d和适配器；具体配置请参考lz-bridge部署指南。

### 网络详情

- **链**：Story Aeneid测试网
- **链ID**：`1315`
- **原生货币**：IP
- **RPC**：`https://aeneid.storyrpc.io`

## Privy集成

该功能与[Privy OpenClaw插件](https://docs.privy.io/recipes/agent-integrations/openclaw-agentic-wallets)集成，实现以下功能：

- **自主钱包管理**：代理拥有自己的Privy服务器钱包
- **基于策略的安全性**：使用Privy策略来限制支出、指定可访问的链或白名单合约
- **无需存储私钥**：Privy负责安全的密钥管理
- **交易签名**：Privy通过API生成EIP-3009和EIP-191交易签名

### 为代理创建Privy钱包

请您的OpenClaw代理执行以下命令：

> “在Story Aeneid测试网上使用Privy为我创建一个以太坊钱包”

代理将创建一个Privy服务器钱包，并返回钱包ID。

### 设置策略

创建支出限制：

> “创建一个策略，将每次USDC.d支付的金额限制为10 USDC.d”

> “将此支出限制策略应用到我的Privy钱包”

## 函数

### `payViaEVVMWithPrivy(options)`

使用Privy钱包通过x402协议在EVVM上处理支付。

**参数：**
- `walletId`：Privy钱包ID
- `to`：收款人地址（人类所有者或其他代理）
- `toIdentity`：可选的EVVM用户名（如果使用地址，则留空）
- `amount`：支付金额（USDC.d的最小单位，保留6位小数）
- `receiptId`：唯一的交易收据标识符
- `adapterAddress`：EVVMPaymentAdapter合约地址（用于BridgeUSDC）
- `usdcDanceAddress`：USDC.d代币合约地址（在当前测试网中使用BridgeUSDC）
- `evvmCoreAddress`：EVVM Core合约地址
- `evvmId`：EVVM实例ID（Story Aeneid为1140）
- `rpcUrl`：Story Aeneid的RPC端点
- `privyAppId`：Privy应用ID（可选，如未提供则使用环境变量）
- `privyAppSecret`：Privy应用密钥（可选，如未提供则使用环境变量）

**返回值**：交易收据

### `payViaEVVM(options)`（旧版本）

直接使用私钥处理支付（不建议在生产环境中使用）。

### `checkPaymentStatus(receiptId, adapterAddress, rpcUrl)`

检查支付是否成功处理。

## 示例

请查看`examples/`目录中的示例文件：
- `agent-payment-privy-example.ts`：使用Privy钱包的示例
- `agent-payment-example.ts`：使用私钥的示例（旧版本）

## 安全注意事项

⚠️ **重要提示**：使用Privy钱包时，请务必：
1. **设置策略**：始终配置支出限制
2. **先进行测试**：在实际使用真实资金前先在测试网上进行测试
3. **监控活动**：定期检查Privy钱包的交易活动
4. **更换凭证**：如果凭证被泄露，立即更换Privy应用密钥

## 确保满足以下要求：

- Node.js 18及以上版本
- ethers.js v6
- 已安装Privy插件（执行`clawhub install privy`）
- 具有访问Story Aeneid RPC端点的权限
- 拥有包含App ID和App Secret的Privy账户

## 许可证

MIT许可证