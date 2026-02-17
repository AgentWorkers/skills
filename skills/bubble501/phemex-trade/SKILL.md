---
name: phemex-trade
description: 在 Phemex 上进行交易（USDT-M 期货、Coin-M 期货、现货）——下订单、管理头寸、查看余额以及查询市场数据。
homepage: https://github.com/betta2moon/phemex-trade-mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["mcporter", "phemex-trade-mcp"], "env": ["PHEMEX_API_KEY", "PHEMEX_API_SECRET"] },
        "primaryEnv": "PHEMEX_API_KEY",
        "install":
          [
            {
              "id": "mcporter",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (node)",
            },
            {
              "id": "phemex-trade-mcp",
              "kind": "node",
              "package": "phemex-trade-mcp",
              "bins": ["phemex-trade-mcp"],
              "label": "Install Phemex MCP server (node)",
            },
          ],
      },
  }
---
# Phemex 交易

您可以通过 `phemex-trade-mcp` 服务器在 Phemex 上进行交易。该服务器支持 USDT-M 期货、Coin-M 期货以及现货市场。

## 如何调用工具

使用 `mcporter` 在 `phemex-trade-mcp` 服务器上调用相关工具：

```bash
PHEMEX_API_KEY=$PHEMEX_API_KEY PHEMEX_API_SECRET=$PHEMEX_API_SECRET PHEMEX_API_URL=${PHEMEX_API_URL:-https://api.phemex.com} mcporter call --stdio "phemex-trade-mcp" <tool_name> --args '<json>' --output json
```

对于仅用于读取市场数据的工具（`get_ticker`、`get_orderbook`、`get_klines`、`get_recent_trades`、`get_funding_rate`），无需 API 密钥：

```bash
mcporter call --stdio "phemex-trade-mcp" get_ticker --args '{"symbol":"BTCUSDT"}' --output json
```

## 合约类型

所有工具都接受一个可选的 `contractType` 参数：

- `linear`（默认值）——USDT-M 永续期货。合约代码以 `USDT` 结尾（例如：`BTCUSDT`）。
- `inverse`——Coin-M 永续期货。合约代码以 `USD` 结尾（例如：`BTCUSD`）。
- `spot`——现货交易。合约代码以 `USDT` 结尾（例如：`BTCUSDT`）。服务器会在 API 请求前自动添加前缀 `s`。

## 工具列表

### 市场数据（无需授权）

- `get_ticker` — 24 小时价格行情。参数：`{"symbol":"BTCUSDT"}`
- `get_orderbook` — 订单簿（30 个层次）。参数：`{"symbol":"BTCUSDT"}`
- `get_klines` — K 线图数据。参数：`{"symbol":"BTCUSDT","resolution":3600,"limit":100}``
- `get_recent_trades` — 最新交易记录。参数：`{"symbol":"BTCUSDT"}`
- `get_funding_rate` — 垂直保证金费率历史记录。参数：`{"symbol":".BTCFR8H","limit":20}`

### 账户信息（仅限读取，需要授权）

- `get_account` — 账户余额和保证金信息。参数：`{"currency":"USDT","contractType":"linear"}`
- `get_spot_wallet` — 现货钱包余额。参数：`{}`
- `get_positions` — 当前持仓及盈亏情况。参数：`{"currency":"USDT","contractType":"linear"}`
- `get_open_orders` — 开仓订单信息。参数：`{"symbol":"BTCUSDT"}`
- `get_order_history` — 已平仓/成交订单记录。参数：`{"symbol":"BTCUSDT","limit":50}``
- `get_trades` — 交易执行历史记录。参数：`{"symbol":"BTCUSDT","limit":50}`

### 交易操作（需要授权）

- `place_order` — 下单。参数：`{"symbol":"BTCUSDT","side":"Buy","orderQty":"0.01","ordType":"Market"}`
- `amend_order` — 修改已开仓订单。参数：`{"symbol":"BTCUSDT","orderID":"xxx","price":"95000"}`
- `cancel_order` — 取消订单。参数：`{"symbol":"BTCUSDT","orderID":"xxx"}`
- `cancel_all_orders` — 取消某个合约的所有订单。参数：`{"symbol":"BTCUSDT"}`
- `set_leverage` — 设置杠杆率。参数：`{"symbol":"BTCUSDT","leverage":10}``
- `switch_pos_mode` — 切换交易模式（单向/对冲）。参数：`{"symbol":"BTCUSDT","targetPosMode":"OneWay"}`

### 资金转移（需要授权）

- `transfer_funds` — 在现货和期货账户之间转移资金。参数：`{"currency":"USDT","amount":"100","direction":"spot_to_futures"}`
- `get_transfer_history` — 资金转移历史记录。参数：`{"currency":"USDT","limit":20}`

## 安全规则

1. **下单前务必确认。** 在调用 `place_order` 之前，务必向用户明确展示订单的详细信息（合约代码、方向、数量、类型、价格），并获取用户确认。
2. **取消所有订单前务必确认。** 在调用 `cancel_all_orders` 之前，先列出所有未平仓订单并获取用户确认。
3. **解释杠杆率变化的影响。** 在调用 `set_leverage` 之前，务必向用户解释杠杆率变化带来的风险（杠杆率越高，清算风险越大）。
4. **交易前提供必要信息。** 在建议用户进行交易前，务必展示当前持仓和账户余额，以便用户做出明智的决策。
5. **严禁自动交易。** 未经用户明确指令，不得自动下单。用户必须明确指示交易内容。

## 常见工作流程

- **查看价格**：```bash
mcporter call --stdio "phemex-trade-mcp" get_ticker --args '{"symbol":"BTCUSDT"}' --output json
```
- **下达市价买单（USDT-M 期货）**：```bash
PHEMEX_API_KEY=$PHEMEX_API_KEY PHEMEX_API_SECRET=$PHEMEX_API_SECRET PHEMEX_API_URL=${PHEMEX_API_URL:-https://api.phemex.com} mcporter call --stdio "phemex-trade-mcp" place_order --args '{"symbol":"BTCUSDT","side":"Buy","orderQty":"0.01","ordType":"Market"}' --output json
```
- **下达限价卖单（Coin-M 期货）**：```bash
PHEMEX_API_KEY=$PHEMEX_API_KEY PHEMEX_API_SECRET=$PHEMEX_API_SECRET PHEMEX_API_URL=${PHEMEX_API_URL:-https://api.phemex.com} mcporter call --stdio "phemex-trade-mcp" place_order --args '{"symbol":"BTCUSD","side":"Sell","orderQty":"10","ordType":"Limit","price":"100000","contractType":"inverse"}' --output json
```
- **买入现货**：```bash
PHEMEX_API_KEY=$PHEMEX_API_KEY PHEMEX_API_SECRET=$PHEMEX_API_SECRET PHEMEX_API_URL=${PHEMEX_API_URL:-https://api.phemex.com} mcporter call --stdio "phemex-trade-mcp" place_order --args '{"symbol":"BTCUSDT","side":"Buy","orderQty":"10","ordType":"Market","contractType":"spot","qtyType":"ByQuote"}' --output json
```
- **查看持仓**：```bash
PHEMEX_API_KEY=$PHEMEX_API_KEY PHEMEX_API_SECRET=$PHEMEX_API_SECRET PHEMEX_API_URL=${PHEMEX_API_URL:-https://api.phemex.com} mcporter call --stdio "phemex-trade-mcp" get_positions --args '{"currency":"USDT"}' --output json
```

## 设置步骤

1. 在 [https://phemex.com](https://phemex.com) 注册 Phemex 账户。
2. 创建 API 密钥（进入“账户” → “API 管理”）。
3. 设置环境变量 `PHEMEX_API_KEY` 和 `PHEMEX_API_SECRET`。
4. （可选）设置 `PHEMEX_API_URL`（生产环境默认为 `https://api.phemex.com`；测试环境使用 `https://testnet-api.phemex.com`）。
5. （可选）设置 `PHEMEX_MAX_ORDER_VALUE` 以限制单笔订单的最大金额（单位：USD）。