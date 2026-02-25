---
name: polymarket-pro
description: 使用 Polymarket 的官方 CLI（命令行界面）可以浏览市场、在 CLOB（Centralized Order Book，集中式订单簿）上进行交易、管理持仓以及分析链上数据。该工具具备市场搜索、订单簿分析、限价单/市价单下达、持仓管理以及高级的 CTF（Contract Trading Framework，合约交易框架）操作等功能。
version: 1.0.0
author: Liwa
requirements:
  - polymarket CLI (brew install or shell script)
  - jq (for JSON processing)
  - wallet (private key or created via CLI)
tags:
  - polymarket
  - prediction-markets
  - trading
  - cli
  - defi
  - crypto
---
# Polymarket CLI 技能

此技能允许您使用官方的 `polymarket` CLI 工具与 Polymarket 预测市场进行交互。与 Polyclaw（用于管理自动交易）不同，此技能为您提供对交易、研究和投资组合管理的直接、细粒度的控制。

## 安装

### 快速安装（macOS/Linux）

```bash
brew tap Polymarket/polymarket-cli https://github.com/Polymarket/polymarket-cli
brew install polymarket
```

### Shell 脚本（所有平台）

```bash
curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
```

### 验证安装

```bash
polymarket --version
polymarket --help
```

---

## 钱包设置

### 提供私钥的三种方式

1. **CLI 标志**：`--private-key 0xabc...`
2. **环境变量**：`export POLYMARKET_PRIVATE_KEY=0xabc...`
3. **配置文件**：`~/.config/polymarket/config.json`

### 创建新钱包

```bash
# Generate new wallet (saves to config)
polymarket wallet create

# Or force overwrite existing
polymarket wallet create --force

# Import existing private key
polymarket wallet import 0xabc123...

# Check wallet address
polymarket wallet address

# Full wallet info
polymarket wallet show
```

### 交易前的授权（必需）

```bash
# Check current approval status
polymarket approve check
polymarket approve check 0xYOUR_ADDRESS

# Set approvals (sends 6 on-chain txs, needs MATIC for gas)
polymarket approve set
```

---

## 输出格式

每个命令都支持 `-o json` 或 `-o table`（默认）：

```bash
# Human-readable table
polymarket markets list --limit 3

# JSON for scripts/agents
polymarket -o json markets list --limit 3

# Pipe to jq for specific fields
polymarket -o json markets search "bitcoin" | jq '.[].question'
```

---

## 市场研究

### 浏览市场

```bash
# List markets with filters
polymarket markets list --limit 10
polymarket markets list --active true --order volume_num
polymarket markets list --closed false --limit 50 --offset 25

# Get specific market by ID or slug
polymarket markets get 12345
polymarket markets get will-trump-win-the-2024-election

# Search markets
polymarket markets search "bitcoin" --limit 5
polymarket markets search "election" --limit 10
```

### 事件（分组市场）

```bash
# List events
polymarket events list --limit 10
polymarket events list --tag politics --active true

# Get specific event
polymarket events get 500

# Get tags for event
polymarket events tags 500
```

### 标签与系列

```bash
# Browse tags
polymarket tags list
polymarket tags get politics
polymarket tags related politics

# Series (recurring events)
polymarket series list --limit 10
polymarket series get 42
```

### 订单簿分析（无需钱包）

```bash
# Check price
polymarket clob price TOKEN_ID --side buy
polymarket clob midpoint TOKEN_ID
polymarket clob spread TOKEN_ID

# Batch prices
polymarket clob batch-prices "TOKEN1,TOKEN2" --side buy
polymarket clob midpoints "TOKEN1,TOKEN2"

# Order book
polymarket clob book TOKEN_ID

# Last trade
polymarket clob last-trade TOKEN_ID

# Price history
polymarket clob price-history TOKEN_ID --interval 1d --fidelity 30

# Market metadata
polymarket clob tick-size TOKEN_ID
polymarket clob fee-rate TOKEN_ID
polymarket clob neg-risk TOKEN_ID
```

**价格历史间隔**：`1m`、`1h`、`6h`、`1d`、`1w`、`max`

---

## 交易（CLOB）

### 下单

```bash
# Limit order (buy 10 shares at $0.50)
polymarket clob create-order \
  --token TOKEN_ID \
  --side buy --price 0.50 --size 10

# Market order (buy $5 worth)
polymarket clob market-order \
  --token TOKEN_ID \
  --side buy --amount 5

# Post multiple orders at once
polymarket clob post-orders \
  --tokens "TOKEN1,TOKEN2" \
  --side buy \
  --prices "0.40,0.60" \
  --sizes "10,10"

# Order types: GTC (default), FOK, GTD, FAK
# Add --post-only for limit orders
```

### 管理订单

```bash
# View your orders
polymarket clob orders
polymarket clob orders --market 0xCONDITION...

# Get specific order
polymarket clob order ORDER_ID

# Cancel orders
polymarket clob cancel ORDER_ID
polymarket clob cancel-orders "ORDER1,ORDER2"
polymarket clob cancel-market --market 0xCONDITION...
polymarket clob cancel-all
```

### 查看余额与交易记录

```bash
# Collateral balance (USDC)
polymarket clob balance --asset-type collateral

# Conditional token balance
polymarket clob balance --asset-type conditional --token TOKEN_ID

# Update balance cache
polymarket clob update-balance --asset-type collateral

# Your trades
polymarket clob trades

# Order details with scoring
polymarket clob order-scoring ORDER_ID
```

---

## 区块链数据

### 投资组合与持仓

```bash
# Current positions
polymarket data positions 0xWALLET_ADDRESS
polymarket data closed-positions 0xWALLET_ADDRESS

# Portfolio value
polymarket data value 0xWALLET_ADDRESS

# Trade history
polymarket data trades 0xWALLET_ADDRESS --limit 50

# Activity summary
polymarket data activity 0xWALLET_ADDRESS
```

### 市场数据

```bash
# Token holders
polymarket data holders 0xCONDITION_ID

# Open interest
polymarket data open-interest 0xCONDITION_ID

# Volume by event
polymarket data volume EVENT_ID

# Leaderboards
polymarket data leaderboard --period month --order-by pnl --limit 10
polymarket data builder-leaderboard --period week
polymarket data builder-volume --period month
```

---

## CTF 操作

适用于高级用户的条件性代币框架操作。

```bash
# Split USDC into YES/NO tokens
polymarket ctf split --condition 0xCONDITION... --amount 10

# Merge tokens back to USDC
polymarket ctf merge --condition 0xCONDITION... --amount 10

# Redeem winning tokens after resolution
polymarket ctf redeem --condition 0xCONDITION...

# Redeem neg-risk positions
polymarket ctf redeem-neg-risk --condition 0xCONDITION... --amounts "10,5"

# Calculate condition IDs (read-only)
polymarket ctf condition-id --oracle 0xORACLE... --question 0xQUESTION... --outcomes 2
polymarket ctf collection-id --condition 0xCONDITION... --index-set 1
polymarket ctf position-id --collection 0xCOLLECTION...
```

`--amount` 以 USDC 为单位（例如，`10` 表示 $10）。默认的 `--partition` 值为二进制（`1,2`）。

---

## 桥接（存入资金）

```bash
# Get deposit addresses (EVM, Solana, Bitcoin)
polymarket bridge deposit 0xWALLET_ADDRESS

# Supported assets
polymarket bridge supported-assets

# Check deposit status
polymarket bridge status 0xDEPOSIT_ADDRESS
```

---

## 奖励与 API

```bash
# Check rewards
polymarket clob rewards --date 2024-06-15
polymarket clob earnings --date 2024-06-15
polymarket clob reward-percentages
polymarket clob current-rewards
polymarket clob market-reward 0xCONDITION...

# API key management
polymarket clob api-keys
polymarket clob create-api-key
polymarket clob delete-api-key

# Account status
polymarket clob account-status
polymarket clob notifications
```

---

## 交互式 Shell

```bash
# Enter interactive mode
polymarket shell

# Example session:
# polymarket> markets list --limit 3
# polymarket> clob book 48331043336612883...
# polymarket> exit
```

支持命令历史记录——有助于探索性分析。

---

## 常见工作流程

### 研究 → 交易流程

```bash
# 1. Find interesting markets
polymarket markets search "bitcoin" --limit 5

# 2. Deep dive on a market
polymarket markets get bitcoin-above-100k

# 3. Check order book
polymarket clob book TOKEN_ID

# 4. Check price history
polymarket clob price-history TOKEN_ID --interval 1d

# 5. Place trade
polymarket clob market-order --token TOKEN_ID --side buy --amount 10
```

### 监控投资组合

```bash
# Check positions
polymarket data positions 0xYOUR_ADDRESS
polymarket data value 0xYOUR_ADDRESS

# Check open orders
polymarket clob orders

# Check recent trades
polymarket clob trades

# Check PnL via leaderboard
polymarket data leaderboard --period month --order-by pnl
```

### 套利检测

```bash
# Batch check prices across markets
polymarket -o json markets list --limit 50 | jq '.[] | select(.volumeNum > 10000) | {question: .question, prices: .outcomePrices}'

# Check spread
polymarket clob spread TOKEN_ID

# Check multiple midpoints
polymarket clob midpoints "TOKEN1,TOKEN2,TOKEN3"
```

---

## 错误处理

| 情况 | 对策 |
|-----------|--------|
| API 错误 | 查看 `polymarket status` 以确认 API 是否正常运行 |
| 余额不足 | 使用 `polymarket clob balance --asset-type collateral` 检查余额 |
| 需要授权 | 运行 `polymarket approve set`（需要 MATIC） |
| 订单被拒绝 | 检查订单参数和滑点设置 |
| 钱包未配置 | 运行 `polymarket wallet create` 或设置私钥 |

---

## 快速参考

```bash
# Help
polymarket --help
polymarket markets --help
polymarket clob --help

# Status
polymarket status
polymarket clob ok
polymarket wallet show

# Setup
polymarket setup              # Guided wizard
polymarket wallet create     # New wallet
polymarket approve set        # Approve contracts

# Markets
polymarket markets list --limit 10
polymarket markets search "keyword"
polymarket markets get MARKET_ID

# Trading
polymarket clob create-order --token ID --side buy --price 0.50 --size 10
polymarket clob market-order --token ID --side buy --amount 5
polymarket clob cancel-all

# Portfolio
polymarket clob balance --asset-type collateral
polymarket data positions 0xADDRESS
polymarket clob trades

# Data
polymarket clob price TOKEN_ID --side buy
polymarket clob book TOKEN_ID
polymarket data leaderboard --period month
```

---

## 高级技巧

1. **使用 JSON 输出进行自动化**：`-o json` 可以使用 `jq` 进行脚本编写。
2. **批量操作**：使用逗号分隔的列表来提高效率。
3. **价格历史数据分析**：使用 `--interval 1d --fidelity 30` 获取每日蜡烛图数据。
4. **跟踪做市商奖励**：查看 `clob order-scoring` 以获取订单奖励信息。
5. **大额交易**：对于较大额度的交易，使用 CTF（Conditional Token Framework）可能比 CLOB 更具成本效率。

---

## 与 Polyclaw 的区别

| 特性 | Polyclaw | Polymarket CLI |
|---------|----------|----------------|
| 交易模式 | 自动交易代理 | 手动/直接操作 |
| 代币创建 | 支持（通过 Clanker） | 不支持 |
| 市场发现 | 由 AI 支持 | 手动搜索 |
| 社交功能 | 自动发布 | 手动操作 |
| 订单簿访问 | 有限 | 完整访问 |
| CTF 操作 | 不支持 | 支持 |
| 奖励跟踪 | 通过仪表板显示 | 通过完整 API 提供 |
| 控制级别 | 高级 | 低级 |

**当您需要自动交易并使用性能代币时，请使用 Polyclaw。**  
**当您需要直接控制、进行套利或使用自定义策略时，请使用 Polymarket CLI。**