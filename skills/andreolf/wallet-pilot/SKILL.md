---
name: WalletPilot
description: 适用于AI代理的通用浏览器钱包自动化工具。支持10种钱包，包括MetaMask、Rabby、Phantom、Trust Wallet、OKX、Coinbase等，兼容EVM和Solana区块链。提供可配置的安全机制，包括消费限额、链上允许列表（chain allowlists）以及审批阈值（approval thresholds）。
tags:
  - crypto
  - wallet
  - ethereum
  - solana
  - defi
  - web3
  - blockchain
  - automation
  - browser
  - metamask
  - rabby
  - coinbase
  - rainbow
  - phantom
  - trust-wallet
  - zerion
  - exodus
  - okx
  - backpack
---

# WalletPilot

这是一个专为AI代理设计的通用浏览器钱包自动化工具，能够控制任何基于浏览器的加密钱包，并提供可配置的权限保护机制。

## 支持的钱包

| 钱包 | EVM | Solana | 用户数量 |
|--------|-----|--------|-------|
| MetaMask | ✅ | - | 1亿+ |
| Rabby | ✅ | - | 100万+ |
| Coinbase Wallet | ✅ | - | 100万+ |
| Rainbow | ✅ | - | 50万+ |
| Phantom | ✅ | ✅ | 300万+ |
| Trust Wallet | ✅ | ✅ | 100万+ |
| Zerion | ✅ | ✅ | 10万+ |
| Exodus | ✅ | ✅ | 10万+ |
| OKX Wallet | ✅ | ✅ | 100万+ |
| Backpack | ✅ | ✅ | 50万+ |

## 概述

WalletPilot允许AI代理通过任何支持的钱包与去中心化应用（dapps）交互并执行交易。所有操作都受到用户定义的约束。

**安全模型：** 代理在一个独立的浏览器配置文件中管理钱包，切勿使用你的主钱包。

## 设置

### 1. 安装依赖项

```bash
cd wallet-pilot
npm install
npx playwright install chromium
```

### 2. 配置钱包提供者

编辑 `config.json` 以选择你的钱包：

```json
{
  "wallet": {
    "provider": "metamask",  // or: rabby, coinbase, rainbow, phantom
    "extensionPath": null    // auto-detect from Chrome, or provide path
  }
}
```

### 3. 创建代理钱包配置文件

```bash
npm run setup
```

此步骤会打开一个浏览器窗口，在其中：
- 安装/设置你选择的钱包扩展程序
- 创建一个新的钱包（生成新的助记词）
- 该配置文件将用于未来的自动化操作

### 4. 为钱包充值

向代理钱包转账少量资金：
- 推荐使用用于支付交易费用的代币（0.01-0.05 ETH/SOL）
- 用于操作的代币（建议从少量开始，例如50美元USDC）

### 5. 配置权限

编辑 `permissions.json`：

```json
{
  "constraints": {
    "spendLimit": {
      "daily": "50000000",
      "perTx": "10000000"
    },
    "allowedChains": [1, 137, 42161, 8453],
    "allowedProtocols": ["0x...uniswap", "0x...1inch"]
  }
}
```

## 可用的操作

### 连接到去中心化应用
```
connect <dapp-url>
```
导航到去中心化应用并连接代理钱包。

### 执行代币交换
```
swap <amount> <token-in> for <token-out> [on <dex>]
```
在允许的交易所（DEX）上执行代币交换。

### 发送代币
```
send <amount> <token> to <address>
```
将代币发送到指定地址（在可花费的限额范围内）。

### 签署消息
```
sign <message>
```
签署任意消息。

### 查看余额
```
balance [token]
```
显示钱包余额。

### 查看交易历史
```
history [count]
```
显示代理的最新交易记录。

## 约束条件

| 约束条件 | 描述 |
|------------|-------------|
| `spendLimit.daily` | 每24小时的最大花费金额（美元） |
| `spendLimit.perTx` | 每笔交易的最大花费金额（美元） |
| `allowedChains` | 允许使用的区块链ID |
| `allowedProtocols` | 允许使用的合约地址 |
| `blockedMethods` | 被禁止的功能 |
| `requireApproval.above` | 需要用户确认的阈值 |

## 添加新钱包

WalletPilot采用插件架构。要添加新钱包，请按照以下步骤操作：
1. 在 `src/wallets/` 目录下创建一个新的适配器。
2. 实现 `WalletAdapter` 接口。
3. 为钱包的UI元素添加相应的选择器。
4. 在 `src/wallets/index.ts` 中注册该适配器。
参考 `src/wallets/metamask.ts` 了解实现细节。

## 安全性

- **独立配置文件：** 代理使用独立的浏览器配置文件。
- **独立钱包：** 与主钱包完全分离。
- **花费限制：** 硬性限制防止过度消费。
- **协议白名单：** 只允许调用白名单中的合约。
- **完整日志记录：** 每笔交易都会被记录。
- **撤销功能：** 设置 `"revoked": true` 可以禁用所有操作。

## 架构

```
src/
├── index.ts              # Main entry point
├── browser.ts            # Playwright browser management
├── guard.ts              # Permission enforcement
├── logger.ts             # Transaction logging
├── price.ts              # USD price estimation
├── types.ts              # TypeScript types
├── config.ts             # Configuration loading
└── wallets/
    ├── index.ts          # Wallet adapter registry
    ├── adapter.ts        # Base adapter interface
    ├── metamask.ts       # MetaMask
    ├── rabby.ts          # Rabby
    ├── coinbase.ts       # Coinbase Wallet
    ├── rainbow.ts        # Rainbow
    ├── phantom.ts        # Phantom
    ├── trust.ts          # Trust Wallet
    ├── zerion.ts         # Zerion
    ├── exodus.ts         # Exodus
    ├── okx.ts            # OKX Wallet
    └── backpack.ts       # Backpack
```

## 对比：WalletPilot vs MetaMask（仅限MetaMask）

| 功能 | WalletPilot | MetaMask（仅限代理钱包） |
|---------|-------------|----------------------|
| 支持的钱包数量 | 支持5种以上钱包 | 仅支持MetaMask |
| 支持的区块链 | EVM + Solana | 仅支持EVM |
| 设置流程 | 可自由选择钱包 | 必须使用MetaMask |
| 复杂性 | 更高 | 更低 |
| 适用场景 | 需要管理多个钱包的组织 | 仅使用MetaMask的用户 |

如果你需要跨多个钱包的灵活性或Solana平台的支持，请选择 **WalletPilot**；
如果只需要简单的MetaMask设置，请选择 **MetaMask（仅限代理钱包）**。