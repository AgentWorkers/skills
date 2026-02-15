---
name: x402-wach
description: 由 WACH.AI 提供支持的 DeFi 风险分析工具包，通过 x402 支付方式使用。目前支持 ERC-20 和 Solana SPL 类型的代币资产风险分析。当用户需要检查代币的安全性、评估 DeFi 风险、检测恶意网站（“蜜罐”）、分析流动性、持有人分布或以太坊、Polygon、Base、BSC、Solana 上智能合约的漏洞时，可以使用该工具包。在 Base 平台上，每次查询的费用为 0.01 美元。
license: MIT
compatibility: Requires Node.js 18+, npm, network access, and a funded EVM wallet (USDC on Base).
metadata:
  author: quillai-network
  version: "1.0"
  endpoint: https://x402.wach.ai/verify-token
  payment: 0.01 USDC on Base (automatic via x402)
---

# x402-wach — DeFi风险分析工具

这是一个由WACH.AI提供支持的DeFi风险分析工具，使用x402 HTTP支付协议进行处理。所有支付操作都是自动完成的（每个请求的费用为0.01 USDC，基于Base网络）。

**目前支持的功能：**

- **资产风险分析**：支持ERC-20代币（Ethereum、Polygon、Base、BSC）和Solana SPL代币

## 何时使用此工具

当用户需要执行以下操作时，可以使用此工具：
- **评估特定代币或资产的风险**；
- **检查代币的安全性**或判断其是否为钓鱼网站/陷阱；
- **获取代币风险评分**（整体评分、代码评分、市场评分）；
- **分析代币持有者分布**（大户集中度、主要持有者、交易所钱包）；
- **审查流动性状况**（总流动性、交易对、去中心化交易所（DEX））；
- **检查智能合约的安全性**（所有权信息、铸造权限、冻结权限、黑名单、暂停机制）；
- **查询代币市场数据**（价格、市值、24小时交易量、供应量）。

## 安装

可以通过npm全局安装此工具的命令行界面（CLI）：

```bash
npm install -g @quillai-network/x402-wach
```

或者将其本地安装到项目中：

```bash
npm install @quillai-network/x402-wach
```

验证安装是否成功：

```bash
x402-wach --version
```

## 设置

安装完成后，请按照以下步骤进行配置，以便开始代币分析：

### 1. 创建或导入钱包

您需要一个EVM钱包来签名x402支付请求。

```bash
# Option A — Generate a brand new wallet
x402-wach wallet create

# Option B — Import an existing wallet by private key
x402-wach wallet import
```

钱包文件存储在`~/.x402-wach/wallet.json`中，并具有受限的文件权限（仅所有者可读写）。

### 2. 为钱包充值

每次代币分析的费用为0.01 USDC（基于Base网络）。请将USDC发送到您的钱包地址。

```bash
# Check your wallet address
x402-wach wallet info
```

您可以通过https://bridge.base.org将USDC从Ethereum或其他区块链桥接至Base网络。

### 3. 准备就绪

随时可以运行设置指南以开始使用该工具：

```bash
x402-wach guide
```

## 支持的区块链

| 简称 | 区块链            | 代币标准          | 适用范围                          |
| ---------- | ------------------- | -------------- | -------------------------------- |
| `eth`      | Ethereum           | ERC-20             | Ethereum主网上的代币                     |
| `pol`      | Polygon             | ERC-20             | Polygon上的代币                     |
| `base`     | Base                | ERC-20             | Base上的代币                     |
| `bsc`      | Binance Smart Chain | BEP-20             | BSC上的代币                     |
| `sol`      | Solana              | SPL               | Solana上的代币                     |

## 命令

### 分析代币风险

```bash
x402-wach verify-risk <TOKEN_ADDRESS> <CHAIN_SHORT_NAME>
```

**参数：**
- `TOKEN_ADDRESS`：代币的合约地址
  - EVM区块链：以`0x`开头，后跟40个十六进制字符（例如：`0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`）
  - Solana地址：32–44个base58字符的字符串（例如：`6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN`）
- `CHAIN_SHORT_NAME`：`eth`、`pol`、`base`、`bsc`、`sol`之一

**示例：**

```bash
# Analyze USDC on Ethereum
x402-wach verify-risk 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 eth

# Analyze TRUMP on Solana
x402-wach verify-risk 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN sol

# Analyze USDC on Base
x402-wach verify-risk 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 base
```

### 钱包管理

```bash
# Create a new wallet
x402-wach wallet create

# Import an existing wallet by private key
x402-wach wallet import

# View wallet address and file location
x402-wach wallet info
```

### 其他命令

```bash
# List all supported chains
x402-wach chains

# Step-by-step setup guide
x402-wach guide

# Help
x402-wach --help
```

## 程序化使用

该工具的SDK也可作为Node.js/TypeScript库使用：

```typescript
import { verifyTokenRisk, validateTokenAddress } from "@quillai-network/x402-wach";

// Always validate before calling (avoids wasting USDC on invalid inputs)
const validation = validateTokenAddress("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "eth");
if (!validation.valid) {
  console.error(validation.error);
} else {
  const report = await verifyTokenRisk("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "eth");
  console.log(report);
}
```

## 输出结构

风险分析报告包含以下内容（如可用）：
- **市场数据**：价格、市值、24小时交易量、价格变动、总供应量；
- **风险评分**：整体评分、代码评分、市场评分（0–100%）；
- **钓鱼网站分析**：判断代币是否为钓鱼网站，以及相关的买卖/转账费用信息；
- **持有者信息**：总持有者数量、主要持有者（包括交易所钱包）及持有比例；
- **流动性**：总流动性（以USDC计）、交易对数量、主要去中心化交易所；
- **代码分析**：所有权检查、铸造/冻结权限、黑名单机制、暂停机制；
- **社交与社区信息**：Twitter、Discord、Telegram链接及官方网站信息。

## 特殊情况与错误处理：
- **地址格式错误**：CLI会在发送请求前（以及任何支付操作前）验证地址格式。EVM地址必须以`0x`开头，后跟40个十六进制字符；Solana地址必须是32–44个base58字符。
- **地址链路错误**：CLI会检测地址是否正确，并提示使用正确的区块链。
- **代币不存在**：如果在选定的区块链上找不到该代币，会显示错误信息而非空报告。
- **USDC不足**：如果钱包资金不足，x402支付会失败，并提示用户充值。
- **未配置钱包**：CLI会提示用户运行`x402-wach wallet create`或`x402-wach wallet import`命令来创建或导入钱包。

## 重要说明：
- 每次分析费用为0.01 USDC（基于Base网络），通过x402支付协议自动扣除。
- 无论分析的代币位于哪个区块链，支付始终在Base网络上完成。
- 钱包文件存储在`~/.x402-wach/wallet.json`中，具有受限的文件权限（仅所有者可访问）。
- 在调用`verify-risk`之前，请务必验证代币地址和区块链信息，以避免为无效请求支付费用。
- 该工具仅用于DeFi风险分析，目前主要支持ERC-20/SPL代币的风险分析，未来将支持更多类型的分析。