---
name: arkade
description: 通过 Arkade（离线方式）、在链上（通过内置/外部工具）以及 Lightning Network 来发送和接收比特币。同时支持 USDC/USDT 稳定币的兑换。
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

# Arkade Skill

该技能支持通过Arkade（离线）、在链上（通过onboard/offboard方式）以及Lightning Network进行比特币的发送和接收；同时支持通过LendaSwap在BTC与稳定币（如USDC/USDT）之间进行兑换。

**支付方式：**
- **离线（Arkade）**：Arkade钱包之间的即时交易
- **在链上**：通过onboard地址接收在链上支付；通过offboard地址进行在链上支付
- **Lightning Network**：通过Boltz协议进行支付和接收

**默认服务器：** https://arkade.computer

## 安装

### 快速入门（无需安装）

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

## CLI命令

> **注意：** 下面的示例直接使用了`arkade`命令（假设已全局安装）。
> 对于pnpm：`pnpm dlx @arkade-os/skill <命令>`
> 对于npx：`npx -y -p @arkade-os/skill arkade <命令>`

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

### 在链上支付（Onboard/Offboard）

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
- `btc_arkade` - Arkade上的比特币
- `usdc_pol` - Polygon上的USDC
- `usdc_eth` - Ethereum上的USDC
- `usdc_arb` - Arbitrum上的USDC
- `usdt_pol` - Polygon上的USDT
- `usdt_eth` - Ethereum上的USDT
- `usdt_arb` - Arbitrum上的USDT

## SDK使用

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

私钥会在首次使用时自动生成并存储在本地，不会通过CLI参数或stdout暴露。无需设置环境变量。LendaSwap API是公开可访问的。

## 技能接口

### ArkadeBitcoinSkill

- `getArkAddress()` - 获取用于接收离线支付的Ark地址
- `getBoardingAddress()` - 获取用于接收在链上支付的onboard地址
- `getBalance()` - 获取余额明细
- `send(params)` - 向Ark地址发送比特币（离线）
- `getTransactionHistory()` - 获取交易历史记录
- `onboard(params)` - 在链上接收支付：将在链上的BTC转换为离线地址
- `offboard(params)` - 在链上支付：将离线BTC发送到任何在链上的地址
- `waitForIncomingFunds(timeout?)` - 等待接收资金

### ArkaLightningSkill

- `createInvoice(params)` - 创建Lightning发票
- `payInvoice(params)` - 支付Lightning发票
- `getFees()` - 获取交换费用
- `getLimits()` - 获取交换限额
- `getPendingSwaps()` - 获取待处理的交换请求
- `getSwapHistory()` - 获取交换历史记录
- `isAvailable()` - 检查是否支持Lightning网络

### LendaSwapSkill

- `getQuoteBtcToStablecoin(amount, token)` - 查询BTC兑换稳定币的报价
- `getQuoteStablecoinToBtc(amount, token)` - 查询稳定币兑换BTC的报价
- `swapBtcToStablecoin(params)` - 将BTC兑换为稳定币
- `swapStablecoinToBtc(params)` - 将稳定币兑换为BTC
- `getSwapStatus(swapId)` - 获取交换状态
- `getPendingSwaps()` - 获取待处理的交换请求
- `getSwapHistory()` - 获取交换历史记录
- `getAvailablePairs()` - 获取可用的交易对
- `claimSwap(swapId)` - 提取已完成的交换结果
- `refundSwap(swapId)` - 退款已过期的交换请求

## 支持的网络**

Arkade支持多个比特币网络：
- `bitcoin` - 主网（Mainnet）
- `testnet` - 测试网（Testnet）
- `signet` - Signet网络
- `regtest` - 本地Regtest网络
- `mutinynet` - Mutiny网络

## 支持资源

- GitHub仓库：https://github.com/arkade-os/skill
- 文档：https://docs.arkadeos.com