---
name: mamo
description: 在 Base (Moonwell) 平台上，您可以与 Mamo DeFi 的收益策略进行交互。您可以存入或提取 USDC、cbBTC、MAMO 或 ETH 到这些自动化收益策略中，同时查看年化收益率（APY）和账户状态。
version: 1.0.0
metadata: {"clawdbot":{"emoji":"🐮","category":"defi","requires":{"bins":["node"]}}}
---

# Mamo — DeFi 收益聚合器（基于 Base 链）

Mamo 是由 Moonwell 在 Base 链上开发的一款 DeFi 收益聚合器。它为用户部署智能合约，将这些用户的存款分配到 Moonwell 的核心市场以及 Morpho 金库中，以实现最优化的收益，并自动复利奖励。

**链：** Base（8453）
**策略类型：** USDC 稳定币借贷、cbBTC 借贷、ETH 借贷、MAMO 质押

## 设置

```bash
cd ~/clawd/skills/mamo/scripts  # or wherever this skill lives
npm install
export MAMO_WALLET_KEY=0x...     # wallet private key
export MAMO_RPC_URL=https://...  # optional, defaults to Base public RPC
```

## 命令

```bash
# Create a yield strategy (deploys your personal strategy contract via on-chain factory)
node mamo.mjs create usdc_stablecoin
node mamo.mjs create cbbtc_lending
node mamo.mjs create eth_lending

# Deposit tokens (approve + deposit to your strategy contract)
node mamo.mjs deposit 100 usdc
node mamo.mjs deposit 0.5 cbbtc

# Withdraw tokens
node mamo.mjs withdraw 50 usdc
node mamo.mjs withdraw all cbbtc

# Account overview — wallet balances + strategy positions
node mamo.mjs status

# Current APY rates
node mamo.mjs apy
node mamo.mjs apy usdc_stablecoin
```

## 工作原理

1. **创建策略**：调用链上的 StrategyFactory 来部署属于用户钱包的代理合约。
2. **存款**：通过 CLI 批准代币支出，然后向用户的策略合约调用 `deposit(amount)` 函数进行存款。
3. **收益累积**：策略会将资金分配到 Moonwell 和 Morpho 之间，并通过 CowSwap 自动复利奖励。
4. **取款**：只有账户所有者（即用户钱包）才能进行取款。资金会直接返回到用户的钱包中。

策略地址存储在本地文件 `~/.config/mamo/strategies.json` 中（用户自定义的策略可能不会在链上注册表中更新）。

## 关键地址

| 代币 | 地址            |
|-------|---------------------|
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| cbBTC | `0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf` |
| MAMO | `0x7300b37dfdfab110d83290a29dfb31b1740219fe` |
| 注册表 | `0x46a5624C2ba92c08aBA4B206297052EDf14baa92` |

## 安全提示：

- 使用 **专用热钱包**，而非你的主要资金存储地址。
- 仅存放你愿意放在热钱包中的资金。
- 将 `MAMO_WALLET_KEY` 存储在环境变量中，切勿保存在永久性文件中。
- 所有交易在发送前都会进行模拟测试。