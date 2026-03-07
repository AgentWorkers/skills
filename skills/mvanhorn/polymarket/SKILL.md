---
name: polymarket
version: "1.1.0"
description: 在 Polymarket 的预测市场中进行查询和交易——查看赔率、热门市场、搜索事件、查看订单簿、下达交易指令以及管理持仓。现已向美国开发者开放。
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-polymarket
homepage: https://polymarket.com
metadata:
  openclaw:
    emoji: "📊"
    tags:
      - prediction-markets
      - polymarket
      - trading
      - odds
      - betting
---
# Polymarket

您可以通过终端查询 [Polymarket](https://polymarket.com) 的预测市场信息并进行交易。

## 设置

**仅读命令可立即使用**（无需安装）。

若需进行交易、查看订单簿或价格历史记录，请安装 [Polymarket CLI](https://github.com/Polymarket/polymarket-cli)：

```bash
curl -sSL https://raw.githubusercontent.com/Polymarket/polymarket-cli/main/install.sh | sh
```

若需进行交易，请先设置一个钱包：

```bash
python3 {baseDir}/scripts/polymarket.py wallet-setup
```

或者手动使用您的私钥配置 `~/.config/polymarket/config.json` 文件。详情请参阅 [CLI 文档](https://github.com/Polymarket/polymarket-cli)。

## 命令

### 浏览市场（无需使用 CLI）

```bash
# Trending/active markets
python3 {baseDir}/scripts/polymarket.py trending

# Search markets
python3 {baseDir}/scripts/polymarket.py search "trump"

# Get specific event by slug
python3 {baseDir}/scripts/polymarket.py event "fed-decision-in-october"

# Get markets by category
python3 {baseDir}/scripts/polymarket.py category politics
python3 {baseDir}/scripts/polymarket.py category crypto
```

### 订单簿与价格（需要 CLI，无需钱包）

```bash
# Order book for a token
python3 {baseDir}/scripts/polymarket.py book TOKEN_ID

# Price history
python3 {baseDir}/scripts/polymarket.py price-history TOKEN_ID --interval 1d
```

### 钱包（需要 CLI）

```bash
python3 {baseDir}/scripts/polymarket.py wallet-setup
python3 {baseDir}/scripts/polymarket.py wallet-show
python3 {baseDir}/scripts/polymarket.py wallet-balance
python3 {baseDir}/scripts/polymarket.py wallet-balance --token TOKEN_ID
```

### 交易（需要 CLI 和钱包）

所有交易执行前都需要使用 `--confirm` 选项。如果不使用该选项，交易仅会显示预览信息。

```bash
# Buy limit order: 10 shares at $0.50
python3 {baseDir}/scripts/polymarket.py --confirm trade buy --token TOKEN_ID --price 0.50 --size 10

# Sell limit order
python3 {baseDir}/scripts/polymarket.py --confirm trade sell --token TOKEN_ID --price 0.70 --size 10

# Market order: buy $5 worth
python3 {baseDir}/scripts/polymarket.py --confirm trade buy --token TOKEN_ID --market-order --amount 5
```

### 订单与持仓（需要 CLI 和钱包）

```bash
# List open orders
python3 {baseDir}/scripts/polymarket.py orders

# Cancel a specific order
python3 {baseDir}/scripts/polymarket.py --confirm orders --cancel ORDER_ID

# Cancel all orders
python3 {baseDir}/scripts/polymarket.py --confirm orders --cancel all

# View positions
python3 {baseDir}/scripts/polymarket.py positions
python3 {baseDir}/scripts/polymarket.py positions --address 0xYOUR_WALLET
```

## 示例对话：

- “特朗普在 2028 年获胜的概率是多少？”
- “Polymarket 上当前的热门话题是什么？”
- “在 Polymarket 上搜索比特币”
- “显示 [token] 的订单簿”
- “以 $0.45 的价格购买 [market] 上的 10 份 ‘YES’ 代币”
- “显示我的未平仓头寸”
- “取消我所有的订单”

## ⚠️ 安全提示

- **涉及真实资金。** 交易将在 Polygon 上使用真实的 USDC 进行。请仔细核对所有信息。
- **所有交易都必须使用 `--confirm` 选项。** 不使用该选项时，交易仅会显示预览信息。
- **CLI 仍处于测试阶段。** Polymarket 团队提醒：** “请自行承担风险，切勿使用大量资金进行交易。”
- **私钥安全**：您的私钥存储在 `~/.config/polymarket/config.json` 文件中，请妥善保管。
- **Gas 费用**：链上操作（如确认交易、拆分代币、赎回代币）需要支付 MATIC 作为手续费。

## API

仅读命令使用公开的 Gamma API（无需身份验证）：
- 基本 URL：`https://gamma-api.polymarket.com`

交易命令基于官方的 [Polymarket CLI](https://github.com/Polymarket/polymarket-cli)（Rust 编写的二进制程序）实现。