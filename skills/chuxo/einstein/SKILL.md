---
name: einstein
description: >
  Blockchain analytics and DeFi intelligence via Einstein's x402 micropayment services.
  Use when user wants on-chain market analysis, token research, whale tracking, smart money
  tracking, rug pull scanning, launchpad monitoring (Pump.fun, Zora, Virtuals), portfolio
  analysis, MEV detection, cross-chain arbitrage, or Polymarket data. Supports Base, Ethereum,
  BSC, Arbitrum, Polygon, Optimism, zkSync, Solana. Costs $0.25-$1.15 USDC per query via
  x402 protocol on Base.
metadata:
  author: project-einstein
  version: "1.1.0"
  disable-model-invocation: true
  clawdbot:
    emoji: "🧠"
    homepage: "https://emc2ai.io"
    requires:
      bins: ["node", "curl"]
      env: ["EINSTEIN_X402_PRIVATE_KEY"]
---

# Einstein — 通过 x402 协议提供区块链分析服务

Einstein 提供了 27 种区块链分析服务，这些服务可以通过 x402 微支付（基于 Base 网络的 USDC）来使用。每次查询的费用根据复杂度不同，范围在 0.25 美元到 1.15 美元之间。

## 快速入门

```bash
# 1. Install dependencies (manual step — the setup wizard will NOT run npm for you)
cd packages/project-einstein/openclaw-skill/einstein && npm install

# 2. Set your private key via environment variable (recommended)
export EINSTEIN_X402_PRIVATE_KEY=0x_your_private_key_here

# 3. Or run the interactive setup wizard
node scripts/einstein-setup.mjs

# 4. List all services (free)
node scripts/einstein.mjs services

# 5. Run a query (will prompt for payment confirmation)
node scripts/einstein.mjs top-movers --chain base --limit 10
```

**所需条件：**
- Node.js 18 及以上版本
- 通过 `npm install` 安装所有依赖项（不会自动安装）
- 一个专门用于 x402 支付的钱包私钥（请勿使用您的主钱包）
- 设置 `EINSTEIN_X402_PRIVATE_KEY` 环境变量（推荐）；或者使用 `--save-config` 选项进行配置安装

## 服务分类

| 服务等级 | 原始价格 | 带 AI 分析的价格 | 提供的服务 |
|------|-------------|-------------|----------|
| 基础 | 0.25 美元 | 0.40 美元 | 最新代币信息、代币图表 |
| 标准 | 0.40 美元 | 0.55 美元 | 行情波动较大的代币、代币交易量、OHLCV 数据、虚拟资产信息、钱包持有情况、持有者集中度 |
| 平台级 | 0.60 美元 | 0.75 美元 | Zora 项目发布信息、Pump.fun 项目发布信息/交易量、BSC 测试版信息、流动性变化 |
| 高级 | 0.85 美元 | 1.00 美元 | 大额投资者信息、智能资金流动分析、顶级交易者信息、DEX 资本流动分析、代币抢购信息、Polymarket 活动信息 |
| 全面分析 | 1.00 美元 | 1.15 美元 | 投资报告、NFT 分析、MEV（最大价值提取）检测、套利机会扫描、诈骗行为检测、Polymarket 对比分析 |

**原始价格**：仅包含结构化数据。**带 AI 分析**：包含 AI 生成的分析结果和洞察（默认选项）。

## 免费服务

以下命令是免费的，无需支付 x402 费用或提供钱包私钥：

### Epstein 文件搜索

可以通过 DugganUSA 公共索引搜索美国司法部公布的 44,886 多份 Jeffrey Epstein 相关文件（2026 年 1 月发布）。

```bash
# Search by name
node scripts/einstein.mjs epstein-search --query "Ghislaine Maxwell" --limit 10

# Search by topic
node scripts/einstein.mjs epstein-search --query "flight logs" --limit 20

# Search by location
node scripts/einstein.mjs epstein-search --query "Little St James"
```

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--query <查询词>` | 搜索关键词 | — |
| `--limit <结果数量>` | 结果数量（1-500 条） | `10` |

## 使用示例

### 市场分析

```bash
# Top movers on Base in the last 24 hours
node scripts/einstein.mjs top-movers --chain base --timeperiod 1d --limit 10

# Top tokens by market cap on Ethereum
node scripts/einstein.mjs top-tokens --chain ethereum --limit 20

# Latest deployed tokens with liquidity
node scripts/einstein.mjs latest-tokens --chain base --limit 15
```

### 大额投资者与智能资金流动分析

```bash
# Track whale accumulation on Ethereum
node scripts/einstein.mjs whale-intel --chain ethereum --limit 10 --timeperiod 7d

# Smart money leaderboard on Base
node scripts/einstein.mjs smart-money --chain base --limit 20 --timeperiod 7d

# Capital-intensive DEX traders
node scripts/einstein.mjs dex-capital --chain base --limit 10 --timeperiod 3d
```

### 安全性与风险分析

```bash
# Scan a token for rug pull risk
node scripts/einstein.mjs rug-scan --chain ethereum --token 0x1234...abcd

# Detect MEV/sandwich attacks
node scripts/einstein.mjs mev-detect --chain ethereum --limit 10 --timeperiod 1d

# Identify early snipers on a token
node scripts/einstein.mjs token-snipe --chain base --token 0x1234...abcd --limit 20
```

### 新项目发布监控

```bash
# Latest Pump.fun launches on Solana
node scripts/einstein.mjs pump-launches --limit 15 --timeperiod 1d

# Pump.fun tokens about to graduate
node scripts/einstein.mjs pump-grads --limit 10

# Zora launches on Base
node scripts/einstein.mjs zora-launches --limit 10 --timeperiod 3d

# Virtuals Protocol agent tokens
node scripts/einstein.mjs virtuals --limit 10 --timeperiod 7d
```

### 投资组合与代币分析

```bash
# Check wallet holdings
node scripts/einstein.mjs wallet --chain ethereum --wallet 0xd8dA...

# Token holder concentration
node scripts/einstein.mjs holders --chain base --token 0x1234... --limit 50

# Token price chart
node scripts/einstein.mjs chart --chain base --token 0x1234... --timeperiod 7d

# OHLCV data for technical analysis
node scripts/einstein.mjs ohlcv --chain base --token 0x1234... --timeperiod 30d
```

### 高级报告

```bash
# Multi-chain investment report
node scripts/einstein.mjs investment-report --chains base,ethereum,bsc --limit 10 --timeperiod 7d

# Cross-chain arbitrage opportunities
node scripts/einstein.mjs arbitrage --chain ethereum --limit 10 --timeperiod 1d

# NFT collection analytics
node scripts/einstein.mjs nft-analytics --chain ethereum --limit 10 --timeperiod 7d
```

### 预测市场分析

```bash
# Polymarket events (Polygon)
node scripts/einstein.mjs polymarket --limit 10 --timeperiod 7d

# Compare Polymarket API vs chain data
node scripts/einstein.mjs polymarket-compare --limit 10
```

## 支付方式

Einstein 使用 **x402 协议**——一种基于 HTTP 的微支付标准。支付过程是自动完成的：
1. 您的请求发送到 Einstein 的接口
2. 服务器返回 HTTP 402 错误码，并要求您进行支付确认
3. 您需要使用私钥签署一个 USDC 转账请求（使用 EIP-3009 协议）
4. 重新发送请求时会包含支付签名
5. Coinbase 的 CDP 服务会完成 USDC 的转账
6. 您随后会收到分析结果

**无需注册账户、API 密钥或订阅服务。** 只需要拥有 Base 网络上的 USDC 和相应的私钥即可。

## 命令行工具参考

### `einstein.mjs`（查询工具）

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--chain <区块链网络>` | 需要查询的区块链网络 | `base` |
| `--limit <结果数量>` | 结果数量（1-500 条） | `10` |
| `--timeperiod <时间周期>` | 时间范围：1 天、3 天、7 天、30 天 | `7d` |
| `--token <代币合约地址>` | 需要查询的代币合约地址 | — |
| `--wallet <钱包地址>` | 使用的钱包地址 | — |
| `--chains <区块链网络列表>` | 用逗号分隔的区块链网络列表 | — |
| `--raw` | 仅返回原始数据（更便宜） | `false` |
| `--yes` / `-y` | 跳过支付确认提示 | `false` |

若要全局跳过支付确认提示，可以设置 `EINSTEIN_AUTO_CONFIRM=true`，或在 `config.json` 文件中添加 `"autoConfirm": true`。

### `einstein-setup.mjs`（配置工具）

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--key <私钥>` | 钱包私钥（跳过交互式提示） | — |
| `--url <Einstein API 地址>` | Einstein API 的基础 URL | `https://emc2ai.io` |
| `--chain <区块链网络>` | 默认区块链网络 | `base` |
| `--save-config` | 将配置信息写入文件（否则会输出到环境变量） | `false` |

**支持的区块链网络：** base、ethernet、bsc、solana、arbitrum、polygon、optimism、zksync

## 安全最佳实践

- **使用专用钱包**：为该服务创建一个专门的钱包，并存入少量 USDC。请勿使用您的主钱包或持有大量资金的钱包。
- **优先使用环境变量**：建议使用环境变量 `EINSTEIN_X402_PRIVATE_KEY`，因为这些变量不会被保存到文件中，从而降低数据泄露的风险。如果必须使用 `config.json`，请确保限制文件的访问权限。

**重要说明：**
- 每次付费查询都会生成一个 EIP-3009 协议的转账请求，用于授权从您的钱包向 Einstein 服务地址转移相应金额的 USDC。该签名是一次性使用的，并且具有时效限制。
- 默认情况下，每次付费前都会显示费用确认提示。若要自动执行查询，可以在命令行中添加 `--yes` 或 `-y`；或者全局设置 `EINSTEIN_AUTO_confirm=true`。
- **无需自动安装依赖项**：配置工具不会自动执行 `npm install`，您需要手动安装所有依赖项，以便了解实际安装了哪些包。
- **配置文件安全**：配置信息仅从环境变量和 `config.json` 文件中读取，不会扫描项目目录外的文件。

## 常见问题解决方法：

- **“未配置私钥”**：设置 `EINSTEIN_X402_PRIVATE_KEY` 环境变量，或运行 `node scripts/einstein-setup.mjs --save-config` 进行配置。
- **“支付被拒绝”/“余额不足”**：确保您的钱包中拥有足够的 USDC（Base 网络）。可以使用 [https://bridge.base.org] 进行资金转移。
- **“无法访问 emc2ai.io”**：检查网络连接，服务可能处于临时停机状态。
- **“未知服务”**：运行 `node scripts/einstein.mjs services` 查看所有可用命令。
- **“依赖项未安装”**：在项目目录中执行 `npm install`：`cd packages/project-einstein/openclaw-skill/einstein && npm install`。

## 参考资料：
- `references/services-catalog.md`：完整的服务目录及参数说明
- `references/payment-guide.md`：详细的 x402 支付协议指南
- `references/examples.md`：按类别分类的扩展使用示例