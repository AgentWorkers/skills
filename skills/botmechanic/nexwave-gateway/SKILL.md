---
name: nexwave-gateway
description: 通过 Circle Gateway 和 Circle 可编程钱包实现跨链 USDC 的统一管理：您可以在任何支持的链上存入 USDC，查看您的统一余额，并在 <500 毫秒内将 USDC 铸造到任何目标链上。整个过程无需使用任何桥接服务，也无需暴露私钥。
version: 1.1.0
tags:
  - usdc
  - circle
  - gateway
  - crosschain
  - defi
  - payments
  - agent-commerce
  - circle-wallet
  - arc
author: nexwave
requiredEnv:
  - CIRCLE_API_KEY
  - CIRCLE_ENTITY_SECRET
  - CIRCLE_WALLET_SET_ID
dependencies:
  - eltontay/circle-wallet
---

# Nexwave Gateway — 为 OpenClaw 代理提供的统一跨链 USDC 服务

## 该功能的用途

Circle Gateway 为您提供了一个 **统一的 USDC 余额**，您可以在任何支持的链上即时访问该余额，整个过程耗时不到 500 毫秒。无需在以太坊（Ethereum）、Base、Avalanche 等链上分别持有 USDC，只需将 USDC 存入 Gateway，即可在其他链上立即提取。

这与传统的桥接（bridging）机制有本质区别：无需依赖流动性池或桥接服务提供商，也无需等待 15 分钟。Gateway 的操作流程为：存款 → 签署燃烧意图（burn intent）→ 接收验证结果 → 提取 USDC，整个过程在 500 毫秒内完成。

## 支持的链（测试网）

| 链名 | 域名 ID | USDC 地址 |
|---|---|---|
| 以太坊 Sepolia | 0 | `0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238` |
| Base Sepolia | 6 | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| Arc 测试网 | 26 | `0x3600000000000000000000000000000000000000` |

**注意：** Arc 是 Circle 专为该功能开发的 L1 区块链，其中 USDC 是原生气体（gas）代币。因此无需额外支付气体费用，USDC 可用于所有操作。Arc 的交易确认速度最快，仅需约 0.5 秒。

**Gateway 合同（所有 EVM 链上的地址相同）：**
- Gateway 钱包：`0x0077777d7EBA4688BDeF3E311b846F25870A19B9`
- Gateway 发行器（Minter）：`0x0022222ABE238Cc2C7Bb1f21003F0a260052475B`

**Gateway API（测试网）：** `https://gateway-api-testnet.circle.com/v1`

## 先决条件

1. 拥有 Circle 开发者账户及 API 密钥和实体秘钥（https://console.circle.com）
2. 已安装 `circle-wallet` 插件（通过 `clawhub install eltontay/circle-wallet`），并配置好 ETH-SEPOLIA、BASE-SEPOLIA 和 ARC-TESTNET 链上的钱包
3. 从 https://faucet.circle.com 获取测试网 USDC（每个地址每链每天可获取 20 USDC，每 2 小时一次）
4. 拥有用于支付 gas 的测试网 ETH（在 Sepolia/Base Sepolia 上使用 Google 提供的 faucet；在 Arc 上，USDC 即为原生气体代币）
5. 安装 Node.js，并安装 `viem`、`dotenv` 以及 `@circle-fin/developer-controlled-wallets` 包

## 使用方法

### 第 1 步：设置项目

运行设置脚本以初始化项目并安装所有依赖项：

```bash
cd /path/to/nexwave-gateway && bash setup.sh
```

此操作会创建一个 `gateway-app/` 目录，其中包含所有预先配置好的文件。

### 第 2 步：查询 Gateway 信息及您的余额

```bash
cd gateway-app && node check-balance.js
```

通过调用 Gateway API 查询支持的链，并显示您在所有链上的统一 USDC 余额。

### 第 3 步：向 Gateway 存入 USDC

```bash
node deposit.js
```

将 USDC 存入以太坊 Sepolia 和 Arc 测试网上的 Gateway 钱包合约。存款完成后，您的统一余额会被记入账户。Arc 的交易确认速度约为 0.5 秒；以太坊的交易确认可能需要长达 20 分钟。

### 第 4 步：即时跨链转账 USDC

```bash
node transfer.js
```

创建燃烧意图（burn intent），通过 Circle 可编程钱包（MPC，无需使用原始私钥）进行签名，然后将签名后的意图提交给 Gateway API 进行验证，并在 Base Sepolia 上提取 USDC。验证结果通常会在 500 毫秒内返回。

## 关键概念

**统一余额：** 将 USDC 存入任意链上的 Gateway 后，系统会为您的账户创建一个统一余额。该余额不绑定于特定链，可在所有支持的链上使用。

**燃烧意图（Burn Intent）：** 如需将统一余额转移到特定链，需签署一个燃烧意图（EIP-712 格式的数据结构），指定来源链、目标链、转账金额和接收者。签名过程通过 Circle 的 MPC 可编程钱包完成，无需使用原始私钥，确保安全性。

**Circle 可编程钱包（Circle Programmable Wallets）：** 该功能使用 Circle 提供的开发者可控钱包，通过多方计算（MPC）进行签名，私钥不会被暴露。签名操作在服务器端完成，从而避免代理使用过程中私钥泄露的风险。

**验证结果（Attestation）：** Gateway API 生成的签名验证结果，用于授权在目标链上进行交易。您需要将此验证结果提交给目标链上的 Gateway 发行器合约以提取 USDC。

**费用：** 在早期试用期间（截至 2026 年 6 月 30 日），费用为 0.5 个基点（0.005%）；此外还需支付链上交易的气体费用。

## 流程图

```
Agent deposits USDC on Chain A
        │
        ▼
Gateway Wallet Contract (approve + deposit)
        │
        ▼
Wait for chain finality → Unified balance credited
        │
        ▼
Agent signs burn intent (EIP-712 via Circle MPC Wallets)
        │
        ▼
Submit to Gateway API ──► Attestation returned (<500ms)
        │
        ▼
Submit attestation to Gateway Minter on Chain B
        │
        ▼
USDC minted on Chain B for recipient
```

## 代理使用场景

- **多链套利：** 即时访问任意链上的 USDC，利用价格差异获利
- **跨链支付：** 用统一余额在任意链上支付服务费用
- **资金管理：** 将多个链上的 USDC 集中到一个账户
- **代理间交易：** 在一个链上接收付款后，立即在另一个链上支出
- **资金效率：** 无需预先在多个链上分散 USDC

## 常见问题及解决方法

- **“余额不足”：** 存款后请等待链上的交易确认完成。以太坊可能需要 20 分钟，Arc 只需约 0.5 秒。
- **“Gateway 存款未生效”：** Gateway API 需要等待区块确认。在以太坊上请耐心等待。
- **气体费用问题：** 在以太坊/Base 上需要使用测试网 ETH 作为气体费用；在 Arc 上，USDC 即为原生气体代币。
- **提款限制：** 每个地址每天每链可通过 faucet.circle.com 获取 20 USDC，每 2 小时一次。

## 参考资料

- Circle Gateway 文档：https://developers.circle.com/gateway
- Circle 可编程钱包：https://developers.circle.com/wallets
- Circle 钱包插件（ClawHub）：https://clawhub.ai/eltontay/circle-wallet
- Arc 测试网文档：https://docs.arc.network
- Gateway 快速入门指南：https://developers.circle.com/gateway/quickstarts/unified-balance-evm
- 完整快速入门代码：https://github.com/circlefin/evm-gateway-contracts/tree/master/quickstart
- Circle 提款工具：https://faucet.circle.com
- Gateway API 参考：https://gateway-api-testnet.circle.com/v1/info