---
name: mt5-httpapi
description: 通过 REST API 进行 MetaTrader 5 交易——获取市场数据、下达/修改/平仓订单、管理持仓、查询交易历史记录。当您需要通过 MetaTrader 5 与外汇/加密货币/股票市场进行交互时，可以使用此方法。
homepage: https://github.com/psyb0t/docker-metatrader5-httpapi
user-invocable: true
metadata:
  { "openclaw": { "emoji": "📈", "primaryEnv": "MT5_API_URL", "requires": { "bins": ["curl"] } } }
---
# mt5-httpapi

这是一个基于MetaTrader 5的REST API，运行在Windows虚拟机中。你可以使用普通的HTTP/JSON协议与之交互，无需使用任何MT5相关的库或依赖Windows系统。只需使用`curl`命令即可轻松调用API。

## 适用场景

- 需要市场数据（如蜡烛图、价格跳动数据、合约规格）
- 需要下达、修改或平仓交易
- 需要查询账户信息（如余额、净值、保证金）
- 需要查看未平仓头寸或待处理订单
- 需要获取交易历史记录

## 不适用场景

- 用于技术分析计算（这些计算需要直接处理原始的价格跳动数据）
- 用于图表绘制或可视化（该API仅提供数据，不生成图表）
- 用于回测（该API仅支持实时/模拟交易）

## 设置

API应该已经处于运行状态。请设置基础URL：

```bash
export MT5_API_URL=http://localhost:6542
```

或者通过OpenClaw配置文件（`~/.openclaw/openclaw.json`）进行设置：

```json
{
  "skills": {
    "entries": {
      "mt5-httpapi": {
        "env": {
          "MT5_API_URL": "http://localhost:6542"
        }
      }
    }
  }
}
```

**验证方法：**运行`curl $MT5_API_URL/ping`。如果响应正常，则表示API已启动；否则请让用户按照[文档链接](https://github.com/psyb0t/docker-metatrader5-httpapi)进行设置。

## 工作原理

遵循标准的REST API规范：
- `GET`用于获取数据
- `POST`用于创建新订单
- `PUT`用于修改订单
- `DELETE`用于平仓或取消订单
- 所有的请求和响应数据均采用JSON格式

错误响应的通用格式如下：

```json
{"error": "description of what went wrong"}
```

## API参考

### 状态检查

```bash
# Is the API alive?
curl $MT5_API_URL/ping
```

### 常见响应字段

- `connected`：是否已连接到经纪商
- `trade_allowed`：是否允许交易
- `company`：当前使用的经纪商名称

```bash
# Initialize MT5 connection (usually auto-done, but use this if you get "MT5 not initialized" errors)
curl -X POST $MT5_API_URL/terminal/init
```

### 账户信息

```json
{"success": true}
```

### 合约规格

```bash
# Shut down MT5
curl -X POST $MT5_API_URL/terminal/shutdown
```

### 登录响应

```json
{
    "success": true,
    "login": 87654321,
    "server": "RoboForex-Demo",
    "balance": 10000.0
}
```

### 合约详情

```bash
# List all available symbols (returns array of symbol names)
curl $MT5_API_URL/symbols
```

### 市场数据

#### 蜡烛图数据（OHLCV格式）

```json
["EURUSD", "GBPUSD", "ADAUSD", "BTCUSD", ...]
```

可用的时间框架：`M1` `M2` `M3` `M4` `M5` `M6` `M10` `M12` `M15` `M20` `M30` `H1` `H2` `H3` `H4` `H6` `H8` `H12` `D1` `W1` `MN1`

#### 订单数据

```bash
# Filter symbols by group pattern
curl "$MT5_API_URL/symbols?group=*USD*"
```

#### 下单

```bash
# Market buy
curl -X POST $MT5_API_URL/orders \
  -H 'Content-Type: application/json' \
  -d '{"symbol": "ADAUSD", "type": "BUY", "volume": 1000}'

# Market buy with SL and TP
curl -X POST $MT5_API_URL/orders \
  -H 'Content-Type: application/json' \
  -d '{"symbol": "ADAUSD", "type": "BUY", "volume": 1000, "sl": 0.25, "tp": 0.35}'

# Market sell
curl -X POST $MT5_API_URL/orders \
  -H 'Content-Type: application/json' \
  -d '{"symbol": "ADAUSD", "type": "SELL", "volume": 1000}'

# Pending buy limit (triggers when price drops to 0.28)
curl -X POST $MT5_API_URL/orders \
  -H 'Content-Type: application/json' \
  -d '{"symbol": "ADAUSD", "type": "BUY_LIMIT", "volume": 1000, "price": 0.28, "sl": 0.25, "tp": 0.35}'
```

下单时需要提供的字段：
- `symbol`（合约代码）
- `type`（订单类型，如`BUY`、`SELL`等）
- `volume`（订单数量）
- 其他字段为可选参数

#### 管理待处理订单

```bash
# List all pending orders
curl $MT5_API_URL/orders

# Filter by symbol
curl "$MT5_API_URL/orders?symbol=EURUSD"

# Get specific order
curl $MT5_API_URL/orders/42094812
```

#### 管理已开仓头寸

```bash
# List all open positions
curl $MT5_API_URL/positions

# Filter by symbol
curl "$MT5_API_URL/positions?symbol=ADAUSD"

# Get specific position
curl $MT5_API_URL/positions/42094812
```

#### 历史记录

#### 预交易检查（务必执行）

在下达任何交易之前，必须进行以下检查，否则可能会导致资金损失：
1. **确认账户是否允许交易**：`GET /account` → 确保`trade_allowed`字段值为`true`。
2. **确认目标合约是否可交易**：`GET /symbols/SYMBOL` → 确认`trade_mode`字段值为4（表示可交易）。其他值表示该合约的交易受限或被禁用。
3. **确认合约规格**：`GET /symbols/SYMBOL` → 确认`trade_contract_size`字段的值。例如，外汇合约的合约大小通常为100,000（即1手等于100,000单位基础货币）。
4. **确认终端连接状态**：`GET /terminal` → 确保`connected`字段值为`true`。如果终端与经纪商断开连接，订单将无法提交。

## 典型工作流程

1. **检查连接状态**：`GET /ping`以确保API可用。
2. **查询账户信息**：`GET /account`以确认是否可以交易，并查看余额、净值和可用保证金。
3. **检查终端连接**：`GET /terminal`以确保终端已连接到经纪商。
4. **获取合约详情**：`GET /symbols/SYMBOL`以确认交易模式、合约大小、价格跳动单位等信息。
5. **获取市场数据**：`GET /symbols/SYMBOL/rates?timeframe=H4&count=100`以获取蜡烛图数据用于分析。
6. **获取当前价格**：`GET /symbols/SYMBOL/tick`以获取最新买卖价格。
7. **计算交易规模和风险**：根据合约规格和价格跳动单位计算风险。
8. **下达订单**：使用`POST /orders`命令下达订单。
9. **监控订单状态**：`GET /positions`以查看未平仓头寸。
10. **调整订单参数**：`PUT /positions/:ticket`以修改止损/止盈价格。
11. **平仓头寸**：`DELETE /positions/:ticket`以平仓头寸。
12. **查看交易历史**：`GET /history/deals`以查看交易详情。

## 位置管理示例

假设你想在H4时间框架内，以当前ATR的3倍作为止损价格，对某个合约进行1%的额度的交易：

1. 获取账户余额。
2. 获取合约详情。
3. 计算风险金额和所需订单数量。
4. 根据计算结果下达订单。

## 技术提示

- **务必在下单前确认交易权限和合约规格**。
- **务必检查`trade_contract_size`以避免错误。
- **务必关注`retcode`字段以判断交易是否成功。
- **使用`GET /error`进行故障排查**。
- **先使用模拟账户进行测试**。
- **注意市场交易时间**。
- **根据合约规格正确设置订单参数**。
- **`deviation`参数对市场订单至关重要**。