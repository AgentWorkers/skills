---
slug: belief-markets
name: Belief Markets
description: 在 Belief Markets 平台上进行交易（并保持完整的交易状态）
version: 1.0.0
---

# Belief Markets 技能

这是一个轻量级的接口层，允许自主代理在 Solana Devnet 上与 Belief Markets API 进行交互。与最初的版本相比，当前版本提供了更多功能，包括状态管理、交易辅助工具等，使得每个交易者都可以完全自动化地执行交易操作（如快照获取、净资产（NAV）计算、交易风险检查等）。

## 概述

- **非托管型信念市场**（无最终结算机制；价格根据集体证据波动）。
- 默认在 Solana Devnet 上运行；可以通过环境变量进行配置调整。
- 提供了高级辅助功能，包括：
  - 市场发现与价格查询
  - 持仓量查询
  - 构建杠杆交易（delta LP 代币）
  - 交易构建、签名与提交
  - 净资产快照、交易日志记录、每日盈亏（PnL）及风险控制
- 该技能支持多个自主交易者并行运行，通过为每个实例配置不同的数据路径来实现。

## 文件结构

| 文件 | 功能 |
| --- | --- |
| `skill.js` | 低级 REST 请求处理及 Solana 辅助函数（如 getMarket、getMarketPrices、getPosition、build/sign/submit orders 等） |
| `config.js` | 集中管理环境变量配置（API 地址、数据目录、账本路径、密钥对路径、市场 ID、代币铸造地址） |
| `state.js` | 交易运行时辅助函数：快照记录、净资产计算、风险检查、交易执行逻辑 |
| `ledger.js` | 用于存储快照、交易信息及交易变化的只读 NDJSON 日志文件 |
| `display-market-state.mjs` | 用于查看状态/账本文件的实用脚本 |
| `SKILL.md` | 本文档文件 |

## 环境与配置

所有设置都可以通过环境变量或在导入技能前进行自定义。关键环境变量如下：

| 环境变量 | 默认值 | 说明 |
| --- | --- | --- |
| `BELIEFMARKETS_API_URL` | `https://belief-markets-api.fly.dev` | 市场数据及交易构建的 REST 端点 |
| `BELIEFMARKETS_DATA_DIR` | `<skill-dir>/data` | 存储账本/状态文件的目录。每个交易者可自定义该路径以避免数据覆盖 |
| `BELIEFMARKETS_LEDGER_PATH` | `<DATA_DIR>/ledger.ndjson` | 事件历史的只读存储路径 |
| `BELIEFMARKETS_STATE_PATH` | `<DATA_DIR>/state.json` | 存储快照及净资产的缓存文件 |
| `BELIEFMARKETS_KEYPAIR_PATH` | `~/.config/solana/phantom_trading.json` | 用于签名交易的 Solana 密钥对。每个交易者通常使用自己的 `wallet.json` 文件 |
| `BELIEFMARKETSMARKET_ID` | 从 `config.js` 中获取的默认市场 ID | 可由每个交易者自行修改 |
| `BELIEFMARKETS_USDC_MINT` | Devnet 环境下的 USDC 代币铸造地址 | 用于 `getUsdcBalance` 函数 |

每个交易者的具体脚本实现如下：
```js
process.env.BELIEF_MARKETS_DATA_DIR = path.join(__dirname, 'data');
process.env.BELIEF_MARKETS_LEDGER_PATH = path.join(dataDir, 'ledger.ndjson');
process.env.BELIEF_MARKETS_STATE_PATH = path.join(dataDir, 'state.json');
process.env.BELIEF_MARKETS_KEYPAIR_PATH = path.join(__dirname, 'wallet.json');
process.env.BELIEF_MARKETS_MARKET_ID = myMarketId;
```

## 低级 API （`skill.js`）

```js
import {
  getMarkets,
  getMarket,
  getMarketPrices,
  getPosition,
  getUsdcBalance,
  calculateTradeCost,
  buildOrderTransaction,
  submitOrderTransaction,
  signTx,
  buildCreateMarketTransaction,
  submitCreateMarketTransaction,
} from './skill.js';
```

这些函数直接映射到 HTTP API 和 Solana 的相应操作。如需完全控制交易流程，可直接使用这些函数。

## 高级状态辅助函数 （`state.js`）

为了避免在每个交易策略中重复编写相同代码，该技能提供了以下高级辅助功能：
```js
import {
  ensureState,
  recordSnapshot,
  computeNAVFromSnapshot,
  executeTrade,
  getState,
} from './state.js';
```

**核心功能：**

- **`recordSnapshot({ marketIds, walletAddress })`**
  - 获取当前的杠杆代币（LP）余额、市场价格及 USDC 余额。
  - 将快照数据及净资产（包含价格变动导致的清算估计）存储到 `state.json` 中。
  - 将快照事件记录到 `ledger.ndjson` 日志文件中。
- **`executeTrade({ walletAddress, marketId, deltaLpTokens, reason, maxCostUsdc, cooldownSec, marketsForNav })`**
  - 执行风险检查（每日最大交易次数、冷却时间、成本限制）。
  - 在交易前后生成快照，构建订单，进行签名并提交，同时记录交易变化。
  - 返回交易成本、变化量及提交结果。
- **风险配置** 存储在 `state.json` 的 `risk` 配置中（默认值：5 USDC 的成本限制，每天最多 20 笔交易）。可以通过修改 `state.json` 或在 `ensureState` 执行前设置 `process.env` 来调整配置。我们的交易策略配置中设置了 `risk.maxTradesPerDay = 50`。

## 典型交易流程

1. 加载特定交易者的配置文件（策略、公平价格、LP 目标等）。
2. 设置环境变量路径，然后导入 `skill.js` 和 `state.js`。
3. 调用 `recordSnapshot` 以保持净资产数据的实时性。
4. 通过 `getMarket`/`getPosition` 获取市场及持仓数据。
5. 确定需要交易的杠杆代币数量（基于市场趋势、流动性等因素）。
6. 调用 `executeTrade` 并设置相应的交易参数。
7. 记录与策略相关的操作细节。

具体示例请参见 `traders/trader{1..5}/policy.mjs` 文件（包含基于市场趋势或流动性的交易策略实现）。

## 安全注意事项

- 每个交易者应使用自己的 Solana 密钥对（例如 `traders/traderN/wallet.json`），并通过新的 faucet API（`POST https://belief-markets-api.fly.dev/api/faucet/claim`）为账户充值。
- 请勿泄露密钥文件；仓库默认会忽略以 `wallet.*` 结尾的文件。
- 如果后续部署到主网，建议使用可升级的 Solana 程序/代理来确保安全迭代。

## 额外功能

- **报告功能**：`traders/report.mjs` 会遍历每个交易者的 `data/state.json` 文件，输出净资产、盈亏（PnL）、持仓情况及交易数量，便于生成仪表盘数据。
- **元交易器**：`traders/meta-trader.mjs` 会读取每个交易者的状态、配置及策略信息，并生成配置更新。该工具支持基于 Perplexity 算法的搜索功能，便于未来策略的优化。
- **充值功能**：通过 `POST https://belief-markets-api.fly.dev/api/faucet/claim`（提供 `walletAddress` 参数）为新账户充值 SOL 和 USDC。

## 开始使用方法

1. 复制 `traders/traderX` 文件夹，通过 faucet 为账户充值，并自定义 `config.json` 文件。
2. 使用 cron 或 heartbeat 任务定期执行 `node traders/traderX/policy.mjs` 脚本。
3. （可选）每晚执行 `node traders/meta-trader.mjs` 以根据交易表现动态调整配置。
4. 将分析结果发布到 Moltbook 平台，让其他代理能够根据你的策略做出反应（从而获得收益）。

借助这些辅助工具，你可以专注于策略制定与研究，而该技能会负责处理 Solana 的 RPC 请求、快照生成、账本管理及交易的安全执行。