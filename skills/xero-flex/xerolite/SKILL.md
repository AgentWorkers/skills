---
name: xerolite
description: "将 OpenClaw 与 Xerolite（IBKR）集成。使用场景包括：查询 Xerolite API、下订单以及搜索合约信息。"
metadata: {"openclaw":{"requires":{"bins":["node"]}}}
---
# Xerolite

**一个将 TradingView 与 Interactive Brokers 连接的交易桥梁。**

[Xerolite](https://www.xeroflex.com/xerolite/) 可以自动执行您的交易策略：它将 [TradingView](https://www.tradingview.com/) 中的警报信息发送到您的 [Interactive Brokers](https://www.interactivebrokers.com/) 账户，从而实现无需人工操作即可实时下达订单。您可以在 TradingView 中设计交易逻辑和警报规则，而 Xerolite 负责与 Interactive Brokers（通过 TWS 或 IB Gateway）的通信以及订单的执行。

该工具允许您的 OpenClaw 代理通过 Xerolite 的 REST API 来 **下达订单** 和 **查询合约信息**——这样您就可以在保持工作流程不变的情况下，通过自然语言或自动化方式来进行交易或查询证券代码。

## 包结构

```
skills/xerolite/
├── SKILL.md              # This file
├── scripts/
│   ├── xerolite.mjs      # CLI (order place, contract search)
└── references/
    └── API.md            # REST API guide
```

## 功能

- 通过 Xerolite REST API 下达订单。
- 通过 Xerolite REST API 查询合约信息。

## 命令

请在技能目录中使用这些命令（或在其他技能中通过 `{baseDir}` 来调用它们）。

**默认参数值**（可选；如未指定则使用默认值）：`--currency USD`、`--asset-class STOCK`、`--exch SMART`。

### 下达订单

必填参数：`--action`、`--qty`、`--symbol`。可选参数：`--currency`、`--asset-class`、`--exch`。

```bash
# Minimal (defaults: USD, STOCK, SMART)
node {baseDir}/scripts/xerolite.mjs order place --symbol AAPL --action BUY --qty 10

# Full
node {baseDir}/scripts/xerolite.mjs order place \
  --symbol AAPL \
  --currency USD \
  --asset-class STOCK \
  --exch SMART \
  --action BUY \
  --qty 10
```

发送到 `POST /api/internal/agent/order/place-order` 的 JSON 数据：

```json
{
  "name": "Agent",
  "action": "BUY",
  "qty": "10",
  "symbol": "AAPL",
  "currency": "USD",
  "asset_class": "STOCK",
  "exch": "SMART"
}
```

### 查询合约

必填参数：`--symbol`。可选参数：`--currency`、`--asset-class`、`--exch`。

```bash
# Minimal (defaults: USD, STOCK, SMART)
node {baseDir}/scripts/xerolite.mjs contract search --symbol AAPL

# Full
node {baseDir}/scripts/xerolite.mjs contract search \
  --symbol AAPL \
  --currency USD \
  --asset-class STOCK \
  --exch SMART
```

发送到 `POST /api/internal/agent/contract/search` 的 JSON 数据：

```json
{
  "brokerName": "IBKR",
  "symbol": "AAPL",
  "currency": "USD",
  "xeroAssetClass": "STOCK"
}
```

## REST API

有关此工具使用的订单和合约查询端点的详细信息，请参阅 [references/API.md](references/API.md)。

## 系统要求

- Node.js 18 及以上版本（内置了 `fetch` 模块）。
- **仅限 CLI 使用**：可选参数 `XEROLITE_API_URL` — Xerolite API 的基础 URL。如果未设置，默认值为 `http://localhost`（同一台机器或局域网）。当前版本不支持 API 密钥；未来版本可能会添加该功能。