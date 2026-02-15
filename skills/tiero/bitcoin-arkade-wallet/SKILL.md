---
name: arkade
description: 通过 Arkade（离链方式）、在链上（通过内置/外部工具）以及 Lightning Network 来发送和接收比特币。同时支持 USDC/USDT 稳定币的交易。
read_when:
  - user wants to send or receive Bitcoin
  - user mentions Arkade, Ark, or offchain Bitcoin
  - user wants to use Lightning Network
  - user wants to swap BTC for stablecoins (USDC, USDT)
  - user wants to on-ramp or off-ramp Bitcoin
  - user wants to get paid onchain or pay someone onchain
  - user mentions boarding address or VTXOs
  - user wants instant Bitcoin payments
requires: []
metadata:
  emoji: "₿"
---

# Arkade 技能

支持通过 Arkade 在链下（offchain）、链上（onchain）以及 Lightning Network 进行比特币的发送和接收；同时支持通过 LendaSwap 在 BTC 与稳定币（USDC/USDT）之间进行兑换。

**支付方式：**
- **链下（Arkade）**：在 Arkade 钱包之间进行即时交易
- **链上**：通过 onboard 地址接收链上支付；通过 offboard 地址进行链上支付
- **Lightning Network**：通过 Boltz 换算机制进行支付和接收

**默认服务器：** https://arkade.computer

## 代理安全规则

**重要提示：** 以下命令会涉及实际资金操作。代理在执行这些命令之前必须始终请求用户的明确确认，并显示交易金额和目的地：
- `send` — 将比特币发送到 Arkade 地址
- `offboard` — 将链下 BTC 转移到链上比特币地址
- `onboard` — 将链上 BTC 转入 Arkade
- `ln-pay` — 支付 Lightning 发票
- `swap-to-stable` / `swap-to-btc` — 执行稳定币兑换
- `swap-claim` / `swap-refund` — 提取或退款已完成的兑换

以下命令为只读命令（`address`、`balance`、`history`、`ln-invoice`、`ln-fees`、`ln-limits`、`ln-pending`、`swap-quote`、`swap-pairs`、`swap-status`、`swap-pending`、`boarding-address`），执行这些命令无需用户确认：

**钱包初始化：** `init` 命令会生成一个新的私钥，并将其存储在 `~/.arkade-wallet/config.json` 文件中（权限设置为 `0600`）。所有其他命令在执行前都需要先运行 `init`。代理在首次运行 `init` 命令时必须通知用户并获得其确认。

## 安装

### 快速启动（无需安装）

```bash
# Using pnpm (recommended)
pnpm dlx @arkade-os/skill init
pnpm dlx @arkade-os/skill address

# Using npx
npx -y -p @arkade-os/skill arkade init
npx -y -p @arkade-os/skill arkade address
```

### 全局安装

```bash
# Install globally
npm install -g @arkade-os/skill
# or
pnpm add -g @arkade-os/skill

# Then use directly
arkade init
arkade address
```

### 作为依赖项安装

```bash
npm install @arkade-os/skill
# or
pnpm add @arkade-os/skill
```

## 命令行接口（CLI）命令

> **注意：** 下面的示例直接使用了 `arkade` 命令（假设已全局安装）。  
> 对于 pnpm：`pnpm dlx @arkade-os/skill <command>`  
> 对于 npx：`npx -y -p @arkade-os/skill arkade <command>`

### 钱包管理

```bash
# Initialize wallet (auto-generates private key, default server: arkade.computer)
arkade init

# Initialize with custom server
arkade init https://custom-server.com

# Show Ark address (for receiving offchain Bitcoin)
arkade address

# Show boarding address (for onchain deposits)
arkade boarding-address

# Show balance breakdown
arkade balance
```

### 比特币交易

```bash
# Send sats to an Ark address
arkade send <ark-address> <amount-sats>

# Example: Send 50,000 sats
arkade send ark1qxyz... 50000

# View transaction history
arkade history
```

### 链上支付（Onboard/Offboard）

```bash
# Get paid onchain: Receive BTC to your boarding address, then onboard to Arkade
# Step 1: Get your boarding address
arkade boarding-address

# Step 2: Have someone send BTC to your boarding address

# Step 3: Onboard the received BTC to make it available offchain
arkade onboard

# Pay onchain: Send offchain BTC to any onchain Bitcoin address
arkade offboard <btc-address>

# Example: Pay someone at bc1 address
arkade offboard bc1qxyz...
```

### Lightning Network

```bash
# Create a Lightning invoice to receive payment
arkade ln-invoice <amount-sats> [description]

# Example: Create invoice for 25,000 sats
arkade ln-invoice 25000 "Coffee payment"

# Pay a Lightning invoice
arkade ln-pay <bolt11-invoice>

# Show swap fees
arkade ln-fees

# Show swap limits
arkade ln-limits

# Show pending swaps
arkade ln-pending
```

### 稳定币兑换（LendaSwap）

```bash
# Get quote for BTC to stablecoin swap
arkade swap-quote <amount-sats> <from> <to>

# Example: Quote 100,000 sats to USDC on Polygon
arkade swap-quote 100000 btc_arkade usdc_pol

# Show available trading pairs
arkade swap-pairs
```

**支持的代币：**
- `btc_arkade` - Arkade 上的比特币  
- `usdc_pol` - Polygon 上的 USDC  
- `usdc_eth` - Ethereum 上的 USDC  
- `usdc_arb` - Arbitrum 上的 USDC  
- `usdt_pol` - Polygon 上的 USDT  
- `usdt_eth` - Ethereum 上的 USDT  
- `usdt_arb` - Arbitrum 上的 USDT  

## 开发工具包（SDK）使用方法

```typescript
import { Wallet, SingleKey } from "@arkade-os/sdk";
import {
  ArkadeBitcoinSkill,
  ArkaLightningSkill,
  LendaSwapSkill,
} from "@arkade-os/skill";

// Create wallet (default server: arkade.computer)
const wallet = await Wallet.create({
  identity: SingleKey.fromHex(privateKeyHex),
  arkServerUrl: "https://arkade.computer",
});

// === Bitcoin Operations ===
const bitcoin = new ArkadeBitcoinSkill(wallet);

// Get addresses
const arkAddress = await bitcoin.getArkAddress();
const boardingAddress = await bitcoin.getBoardingAddress();

// Check balance
const balance = await bitcoin.getBalance();
console.log("Total:", balance.total, "sats");
console.log("Offchain available:", balance.offchain.available, "sats");
console.log("Onchain pending:", balance.onchain.total, "sats");

// Send Bitcoin
const result = await bitcoin.send({
  address: recipientArkAddress,
  amount: 50000,
});
console.log("Sent! TX:", result.txid);

// === Lightning Operations ===
const lightning = new ArkaLightningSkill({
  wallet,
  network: "bitcoin",
});

// Create invoice
const invoice = await lightning.createInvoice({
  amount: 25000,
  description: "Coffee payment",
});
console.log("Invoice:", invoice.bolt11);

// Pay invoice
const payment = await lightning.payInvoice({
  bolt11: "lnbc...",
});
console.log("Paid! Preimage:", payment.preimage);

// === Stablecoin Swaps ===
const lendaswap = new LendaSwapSkill({ wallet });

// Get quote
const quote = await lendaswap.getQuoteBtcToStablecoin(100000, "usdc_pol");
console.log("You'll receive:", quote.targetAmount, "USDC");

// Execute swap
const swap = await lendaswap.swapBtcToStablecoin({
  targetAddress: "0x...", // EVM address
  targetToken: "usdc_pol",
  targetChain: "polygon",
  sourceAmount: 100000,
});
console.log("Swap ID:", swap.swapId);
```

## 配置

**数据存储：** `~/.arkade-wallet/config.json`

私钥会在首次使用时自动生成并存储在本地，不会通过 CLI 参数或标准输出显示。无需设置任何环境变量。LendaSwap API 可公开访问。

## 技能接口

### ArkadeBitcoinSkill

- `getArkAddress()` — 获取用于接收链下支付的 Arkade 地址  
- `getBoardingAddress()` — 获取用于接收链上支付的 onboard 地址  
- `getBalance()` — 获取余额明细  
- `send(params)` — 将比特币发送到 Arkade 地址（链下）  
- `getTransactionHistory()` — 获取交易历史记录  
- `onboard(params)` — 在链上接收支付：将链上 BTC 转换为链下 BTC  
- `offboard(params)` — 在链上支付：将链下 BTC 发送到任意链上地址  
- `waitForIncomingFunds(timeout?)` — 等待资金到账  

### ArkaLightningSkill

- `createInvoice(params)` — 创建 Lightning 发票  
- `payInvoice(params)` — 支付 Lightning 发票  
- `getFees()` — 获取兑换费用  
- `getLimits()` — 获取兑换限额  
- `getPendingSwaps()` — 获取待处理的兑换请求  
- `getSwapHistory()` — 获取兑换历史记录  
- `isAvailable()` — 检查 Lightning Network 是否可用  

### LendaSwapSkill

- `getQuoteBtcToStablecoin(amount, token)` — 提供 BTC 到稳定币的兑换报价  
- `getQuoteStablecoinToBtc(amount, token)` — 提供稳定币到 BTC 的兑换报价  
- `swapBtcToStablecoin(params)` — 将 BTC 兑换为稳定币  
- `swapStablecoinToBtc(params)` — 将稳定币兑换为 BTC  
- `getSwapStatus(swapId)` — 获取兑换状态  
- `getPendingSwaps()` — 获取待处理的兑换请求  
- `getSwapHistory()` — 获取兑换历史记录  
- `getAvailablePairs()` — 获取可用的交易对  
- `claimSwap(swapId)` — 提取已完成的兑换金额  
- `refundSwap(swapId)` — 退款已过期的兑换  

## 支持的网络**

Arkade 支持多个比特币网络：
- `bitcoin` — 主网  
- `testnet` — 测试网  
- `signet` — Signet 网络  
- `regtest` — 本地测试网  
- `mutinynet` — Mutiny 网络  

## 技术支持

- GitHub：https://github.com/arkade-os/skill  
- 文档：https://docs.arkadeos.com