---
name: MetaMask Agent Wallet
description: 控制一个沙箱化的 MetaMask 浏览器扩展钱包，用于执行自主的区块链交易。该钱包具备可配置的权限保护机制，包括支出限额、链路允许列表（chain allowlists）、协议限制以及审批阈值等设置。仅支持 MetaMask（不支持其他钱包）。
tags:
  - crypto
  - metamask
  - wallet
  - ethereum
  - defi
  - web3
  - blockchain
  - automation
  - browser
---

# MetaMask 代理钱包技能

该技能用于控制一个沙箱化的 MetaMask 钱包，以实现自主的区块链交易，并提供可配置的权限控制机制。

## 概述

该技能允许 AI 代理通过专用的 MetaMask 钱包与去中心化应用（dapps）交互并执行交易。所有操作均受用户定义的约束条件（如消费限额、协议允许列表、审批阈值）的约束。

**安全模型：** 代理在独立的浏览器配置文件中控制一个单独的钱包。切勿使用您的主要钱包。

## 设置

### 1. 安装依赖项

```bash
cd metamask-agent-skill
npm install
npx playwright install chromium
```

### 2. 创建代理钱包配置文件

```bash
npm run setup
```

此操作将：
- 在 `~/.agent-wallet/chrome-profile` 下创建一个新的 Chrome 配置文件
- 安装 MetaMask 扩展程序
- 指导您完成钱包的创建（使用新的助记词）

### 3. 为钱包充值

向代理钱包转移少量资金：
- 用于支付交易费用的 ETH（建议 0.01–0.05 ETH）
- 用于操作的代币（建议从少量开始，例如 50 美元 USDC）

### 4. 配置权限

编辑 `permissions.json` 以设置您的约束条件：

```json
{
  "constraints": {
    "spendLimit": {
      "daily": "50000000",    // $50 in 6-decimal format
      "perTx": "10000000"     // $10 max per transaction
    },
    "allowedChains": [1, 137, 42161],
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

**示例：`connect https://app.uniswap.org`**

### 执行代币交换
```
swap <amount> <token-in> for <token-out> [on <dex>]
```
在允许的去中心化交易所（DEX）上执行代币交换。

**示例：`swap 0.01 ETH for USDC on uniswap`**

### 发送代币
```
send <amount> <token> to <address>
```
将代币发送到指定地址（在消费限额范围内）。

**示例：`send 10 USDC to 0x1234...`**

### 签署消息
```
sign <message>
```
签署任意消息。请谨慎使用此功能。

### 查看余额
```
balance [token]
```
显示钱包余额。

### 查看交易历史
```
history [count]
```
显示代理的近期交易记录及其结果。

## 约束条件

所有操作在执行前都会检查 `permissions.json` 中的配置：

| 约束条件 | 描述 |
|------------|-------------|
| `spendLimit.daily` | 每 24 小时的最大消费金额（美元） |
| `spendLimit.perTx` | 每次交易的最大消费金额（美元） |
| `allowedChains` | 允许的链 ID 列表 |
| `allowedProtocols` | 允许的合约地址列表 |
| `blockedMethods` | 被禁止的功能选择器 |
| `requireApproval.above` | 需要用户确认的阈值 |

### 审批流程

当交易金额超过 `requireApproval.above` 时：
1. 代理暂停操作
2. 记录交易详情
3. 代理提示：“此交易需要审批：[详情]”
4. 用户必须明确批准后代理才能继续执行交易

## 安全性

- **独立配置文件：** 代理使用独立的 Chrome 配置文件，不会影响您的主要浏览器。
- **独立钱包：** 代理钱包与您的主钱包完全分离。
- **消费限额：** 硬性限制防止过度消费。
- **协议允许列表：** 只允许调用白名单中的合约。
- **完整日志记录：** 每次交易意图和结果都会被记录。
- **撤销权限：** 在 `permissions.json` 中设置 `"revoked": true` 可以禁用所有操作。

## 日志记录

所有交易都会被记录到 `~/.agent-wallet/logs/` 目录中：

```json
{
  "timestamp": 1706900000000,
  "action": "swap",
  "intent": { "to": "0x...", "value": "0", "data": "0x..." },
  "guardResult": { "allowed": true },
  "outcome": "confirmed",
  "txHash": "0x..."
}
```

使用 `history` 命令可以查看最近的交易记录。

## 故障排除

- **“协议不允许”**：将合约地址添加到 `permissions.json` 的 `allowedProtocols` 列表中。
- **超出每日限额**：等待 24 小时或增加 `spendLimit.daily` 的值。
- **未检测到 MetaMask 弹窗**：确保浏览器配置文件路径正确且 MetaMask 已安装。
- **交易模拟失败**：可能是去中心化应用尝试调用被禁止的功能或使用了不受支持的链。

## 架构

```
src/
├── index.ts          # Main entry point
├── browser.ts        # Playwright browser management
├── wallet.ts         # MetaMask interaction primitives
├── guard.ts          # Permission enforcement
├── logger.ts         # Transaction logging
├── price.ts          # USD price estimation
├── types.ts          # TypeScript types
└── config.ts         # Configuration loading
```

## 与 Gator 的集成

当 Gator 账户可用时，`permissions.json` 可以被链上的权限验证信息取代。此时，权限验证将基于 Gator 的权限注册表进行，而非本地配置。