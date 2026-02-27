---
name: phemex-trade
description: >
  在 Phemex 上进行交易（USDT-M 期货、Coin-M 期货、现货交易）——可以下达订单、管理持仓、查看余额以及查询市场数据。适用于用户需要执行以下操作的场景：  
  (1) 查看 Phemex 上的加密货币价格或市场数据；  
  (2) 下达、修改或取消订单；  
  (3) 查看账户余额或持仓情况；  
  (4) 设置杠杆比例或切换持仓模式；  
  (5) 在现货钱包和期货钱包之间转移资金；  
  (6) 执行任何与 Phemex 交易所相关的操作。
homepage: https://github.com/betta2moon/phemex-trade-mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["phemex-cli"], "env": ["PHEMEX_API_KEY", "PHEMEX_API_SECRET"] },
        "primaryEnv": "PHEMEX_API_KEY",
        "install":
          [
            {
              "id": "phemex-trade-mcp",
              "kind": "node",
              "package": "phemex-trade-mcp",
              "bins": ["phemex-cli"],
              "label": "Install Phemex CLI (node)",
            },
          ],
      },
  }
---
# Phemex交易

您可以通过`phemex-cli`工具在Phemex上进行交易。该工具支持USDT-M期货、Coin-M期货以及现货市场。

## 开始之前

请确保您已安装了最新版本的`phemex-cli`：

```bash
npm install -g phemex-trade-mcp@latest
```

## 如何使用工具

您可以使用命令行参数来调用这些工具，也可以使用JSON格式的参数：

```bash
phemex-cli <tool_name> '{"param1":"value1","param2":"value2"}'
```

所有工具的输出均为JSON格式。系统会自动读取环境变量`PHEMEX_API_KEY`、`PHEMEX_API_SECRET`和`PHEMEX_API_URL`。

## 合约类型

每个工具都支持一个可选的`--contractType`参数：

- `linear`（默认值）——USDT-M永续期货。合约代码以`USDT`结尾（例如：`BTCUSDT`）。
- `inverse`——Coin-M永续期货。合约代码以`USD`结尾（例如：`BTCUSD`）。
- `spot`——现货交易。合约代码以`USDT`结尾（例如：`BTCUSDT`）。系统会在API请求前自动添加前缀`s`。

## 工具列表

### 市场数据（无需认证）

- `get_ticker`——24小时价格行情。示例：`phemex-cli get_ticker --symbol BTCUSDT`
- `get_orderbook`——订单簿（显示30个层次的数据）。示例：`phemex-cli get_orderbook --symbol BTCUSDT`
- `get_klines`——K线数据。示例：`phemex-cli get_klines --symbol BTCUSDT --resolution 3600 --limit 100`
- `get_recent_trades`——最近的交易记录。示例：`phemex-cli get_recent_trades --symbol BTCUSDT`
- `get_funding_rate`——资金费率历史记录。示例：`phemex-cli get_funding_rate --symbol .BTCFR8H --limit 20`

### 账户信息（仅读，需要认证）

- `get_account`——账户余额和保证金信息。示例：`phemex-cli get_account --currency USDT`
- `get_spot_wallet`——现货钱包余额。示例：`phemex-cli get_spot_wallet`
- `get_positions`——当前持仓及盈亏情况。示例：`phemex-cli get_positions --currency USDT`
- `get_open_orders`——未成交订单。示例：`phemex-cli get_open_orders --symbol BTCUSDT`
- `get_order_history`——已成交/已平仓订单记录。示例：`phemex-cli get_order_history --symbol BTCUSDT --limit 50`
- `get_trades`——交易执行历史记录。示例：`phemex-cli get_trades --symbol BTCUSDT --limit 50`

### 交易操作（需要认证）

- `place_order`——下达订单（市价单、限价单、止损单、止损限价单）。关键参数包括：
  - `--symbol`：交易合约代码
  - `--side`：买入/卖出
  - `--orderQty`：订单数量
  - `--ordType`：订单类型（市价/限价/止损/止损限价）
  - `--price`：订单价格
  - `--stopPx`：止损/止损限价价格
  - `--timeInForce`：订单执行方式（GoodTillCancel/PostOnly/ImmediateOrCancel/FillOrKill）
  - `--reduceOnly`：是否允许部分成交
  - `--posSide`：持仓方向（多头/空头/合并）
  - `--stopLoss`：止损价格
  - `--takeProfit`：止盈价格
  - `--qtyType`：订单数量单位（仅适用于现货合约）：
    - `linear`（USDT-M）：订单数量 = 基础货币数量（例如：`0.01`表示0.01 BTC）
    - `inverse`（Coin-M）：订单数量 = 合约数量（例如：`10`表示10份合约）
    - `spot`：订单数量单位取决于`--qtyType`：
      - `ByBase`（默认）：以基础货币计算（例如：`0.01`表示0.01 BTC）
      - `ByQuote`：以报价货币计算（例如：`50`表示50 USDT的BTC）
    - 示例：`phemex-cli place_order --symbol BTCUSDT --side Buy --orderQty 0.01 --ordType Market`
- `amend_order`——修改未成交订单。示例：`phemex-cli amend_order --symbol BTCUSDT --orderID xxx --price 95000`
- `cancel_order`——取消单个订单。示例：`phemex-cli cancel_order --symbol BTCUSDT --orderID xxx`
- `cancel_all_orders`——取消某个合约的所有订单。示例：`phemex-cli cancel_all_orders --symbol BTCUSDT`
- `set_leverage`——设置杠杆比率。示例：`phemex-cli set_leverage --symbol BTCUSDT --leverage 10`
- `switch_pos_mode`——切换持仓模式（单向/对冲）。示例：`phemex-cli switch_pos_mode --symbol BTCUSDT --targetPosMode OneWay`

### 资金转移（需要认证）

- `transfer_funds`——在现货账户和期货账户之间转移资金。示例：`phemex-cli transfer_funds --currency USDT --amount 100 --direction spot_to_futures`
- `get_transfer_history`——资金转移历史记录。示例：`phemex-cli get_transfer_history --currency USDT --limit 20`

## 安全规则

1. **下达订单前务必确认。** 在调用`place_order`之前，务必向用户明确展示订单的详细信息（合约代码、方向、数量、类型、价格），并获取用户的确认。
2. **取消所有订单前务必确认。** 在调用`cancel_all_orders`之前，先列出所有未成交的订单并获取用户的确认。
3. **解释杠杆率变更的影响。** 在调用`set_leverage`之前，务必向用户说明杠杆率变更的后果（杠杆率越高，清算风险越大）。
4. **交易前提供相关信息。** 在建议用户进行交易前，务必展示当前的持仓情况和账户余额，以便用户做出明智的决策。
5. **严禁自动交易。** 未经用户明确指令，切勿自动下达订单。

## 常见操作流程

- **查看价格**：```bash
phemex-cli get_ticker --symbol BTCUSDT
```
- **下达市价买单（USDT-M期货）**：```bash
phemex-cli place_order --symbol BTCUSDT --side Buy --orderQty 0.01 --ordType Market
```
- **下达限价卖单（Coin-M期货）**：```bash
phemex-cli place_order --symbol BTCUSD --side Sell --orderQty 10 --ordType Limit --price 100000 --contractType inverse
```
- **买入现货**：```bash
phemex-cli place_order --symbol BTCUSDT --side Buy --orderQty 10 --ordType Market --contractType spot --qtyType ByQuote
```
- **查看持仓**：```bash
phemex-cli get_positions --currency USDT
```

## 设置账户

1. 在[https://phemex.com](https://phemex.com)注册Phemex账户。
2. 创建API密钥（进入“账户” → “API管理”）。
3. 设置环境变量`PHEMEX_API_KEY`和`PHEMEX_API_SECRET`。
4. （可选）设置`PHEMEX_API_URL`（默认为测试网地址`https://testnet-api.phemex.com`；实际交易请设置为`https://api.phemex.com`）。
5. （可选）设置`PHEMEX_MAX_ORDER_VALUE`以限制单笔订单的最大金额（单位：USD）。