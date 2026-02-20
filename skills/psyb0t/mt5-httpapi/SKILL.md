---
name: mt5-httpapi
description: 通过 REST API 进行 MetaTrader 5 交易：获取市场数据、下达/修改/关闭订单、管理持仓以及查询交易历史记录。当您需要通过 MetaTrader 5 与外汇/加密货币/股票市场进行交互时，可以使用此方法。
compatibility: Requires curl and a running mt5-httpapi instance. MT5_API_URL env var must be set.
metadata:
  author: psyb0t
  homepage: https://github.com/psyb0t/mt5-httpapi
---
# mt5-httpapi

这是一个基于MetaTrader 5的REST API，运行在Windows虚拟机中。您可以使用普通的HTTP/JSON协议与之进行交互，无需使用任何MT5相关的库或依赖Windows系统。只需使用`curl`命令即可。

有关安装和配置的详细信息，请参阅[references/setup.md](references/setup.md)。

## 设置

该API应该已经处于运行状态。请设置基础URL：

```bash
export MT5_API_URL=http://localhost:6542
```

每个终端都有自己的端口（在`terminals.json`文件中配置）。如果同时运行多个终端，请将`MT5_API_URL`设置为您想要连接的终端的端口。

**验证方法：**运行`curl $MT5_API_URL/ping`，应返回`{"status": "ok"}`。如果返回其他内容，说明API尚未启动（可能仍在初始化中——系统会自动尝试重新连接）。

## 工作原理

- `GET`用于查询数据；
- `POST`用于创建新的交易订单；
- `PUT`用于修改现有交易订单；
- `DELETE`用于关闭或取消交易订单。
所有请求的数据格式均为JSON。

## 错误响应

```json
{"error": "description of what went wrong"}
```

## 交易前必查项（切勿跳过）

在下达任何交易指令之前，请务必检查以下内容：
1. 执行`GET /account`请求，确保`trade_allowed`的值为`true`；
2. 执行`GET /symbols/SYMBOL`请求，确认`trade_mode`的值为`4`（表示允许进行全额交易）；
3. 再次执行`GET /symbols/SYMBOL`请求，检查`trade_contract_size`的值：1手EURUSD的交易相当于100,000欧元，而非1欧元；
4. 执行`GET /terminal`请求，确保`connected`的值为`true`。

## API参考文档

### 系统状态

```bash
curl $MT5_API_URL/ping
# {"status": "ok"}

curl $MT5_API_URL/error
# {"code": 1, "message": "Success"}
```

### 终端信息

```bash
curl $MT5_API_URL/terminal
curl -X POST $MT5_API_URL/terminal/init
curl -X POST $MT5_API_URL/terminal/shutdown
```

`/terminal`接口的关键字段包括：`connected`、`trade_allowed`、`build`、`company`。

### 账户信息

```bash
curl $MT5_API_URL/account
```

```json
{
    "login": 12345678,
    "balance": 10000.0,
    "equity": 10000.0,
    "margin": 0.0,
    "margin_free": 10000.0,
    "margin_level": 0.0,
    "leverage": 500,
    "currency": "USD",
    "trade_allowed": true,
    "margin_so_call": 70.0,
    "margin_so_so": 20.0
}
```

### 交易品种信息

```bash
curl $MT5_API_URL/symbols
curl "$MT5_API_URL/symbols?group=*USD*"
curl $MT5_API_URL/symbols/EURUSD
curl $MT5_API_URL/symbols/EURUSD/tick
curl "$MT5_API_URL/symbols/EURUSD/rates?timeframe=H4&count=100"
curl "$MT5_API_URL/symbols/EURUSD/ticks?count=100"
```

支持的時間框架包括：`M1`、`M2`、`M3`、`M4`、`M5`、`M6`、`M10`、`M12`、`M15`、`M20`、`M30`、`H1`、`H2`、`H3`、`H4`、`H6`、`H8`、`H12`、`D1`、`W1`、`MN1`。

每个交易品种的关键字段包括：`bid`（买价）、`ask`（卖价）、`digits`（价格显示精度）、`trade_contract_size`（单笔交易合约大小）、`trade_tick_value`（交易最小刻度值）、`trade_tick_size`（交易最小跳动幅度）、`volume_min`（最小交易量）、`volume_max`（最大交易量）、`volume_step`（交易量步长）、`spread`（点差）、`swap_long`（多头掉期费用）、`swap_short`（空头掉期费用）、`trade_stops_level`（止损/止盈水平）、`trade_mode`（交易模式）。

### 订单信息

```bash
# Place market order
curl -X POST $MT5_API_URL/orders \
  -H 'Content-Type: application/json' \
  -d '{"symbol": "EURUSD", "type": "BUY", "volume": 0.1, "sl": 1.08, "tp": 1.10}'

# List pending orders
curl $MT5_API_URL/orders
curl "$MT5_API_URL/orders?symbol=EURUSD"
curl $MT5_API_URL/orders/42094812

# Modify pending order
curl -X PUT $MT5_API_URL/orders/42094812 \
  -H 'Content-Type: application/json' \
  -d '{"price": 1.09, "sl": 1.07, "tp": 1.11}'

# Cancel pending order
curl -X DELETE $MT5_API_URL/orders/42094812
```

订单类型包括：`BUY`（买入）、`SELL`（卖出）、`BUY_LIMIT`（限价买入）、`SELL_LIMIT`（限价卖出）、`BUY_STOP`（止损买入）、`SELL_STOP`（止损卖出）、`BUY_STOP_LIMIT`（限价止损买入）、`SELL_STOP_LIMIT`（限价止损卖出）。

订单执行策略包括：`FOK`（立即成交）、`IOC`（市价成交，默认值）、`RETURN`（取消订单）。

订单有效期包括：`GTC`（永久有效）、`DAY`（当日有效）、`SPECIFIED`（指定时间有效）、`SPECIFIED_DAY`（指定日期有效）。

必填字段包括：`symbol`（交易品种代码）、`type`（订单类型）、`volume`（交易量）。`price`字段对于市价订单会自动填充。

### 交易结果

```json
{
    "retcode": 10009,
    "deal": 40536203,
    "order": 42094820,
    "volume": 0.1,
    "price": 1.0950,
    "comment": "Request executed"
}
```

`retcode`值为10009表示交易成功；其他值表示交易过程中出现错误。

### 持仓信息

```bash
curl $MT5_API_URL/positions
curl "$MT5_API_URL/positions?symbol=EURUSD"
curl $MT5_API_URL/positions/42094820

# Update SL/TP
curl -X PUT $MT5_API_URL/positions/42094820 \
  -H 'Content-Type: application/json' \
  -d '{"sl": 1.085, "tp": 1.105}'

# Close full position
curl -X DELETE $MT5_API_URL/positions/42094820

# Partial close
curl -X DELETE $MT5_API_URL/positions/42094820 \
  -H 'Content-Type: application/json' \
  -d '{"volume": 0.05}'
```

关键持仓字段包括：`ticket`（订单编号）、`type`（0表示买入，1表示卖出）、`volume`（交易量）、`price_open`（开盘价）、`price_current`（当前价）、`sl`（止损价）、`tp`（止盈价）、`profit`（利润）、`swap`（掉期费用）。

### 历史交易记录

```bash
curl "$MT5_API_URL/history/orders?from=$(date -d '1 day ago' +%s)&to=$(date +%s)"
curl "$MT5_API_URL/history/deals?from=$(date -d '1 day ago' +%s)&to=$(date +%s)"
```

查询历史交易记录时需要提供`from`和`to`参数，这两个参数以Unix纪元秒为单位。

每笔交易的详细信息包括：`type`（0表示买入，1表示卖出）、`entry`（0表示开仓，1表示平仓）、`profit`（开仓时的利润，平仓时的实际盈亏）。

## 交易头寸管理

```
risk_amount     = balance * risk_pct
sl_distance     = ATR * multiplier
ticks_in_sl     = sl_distance / trade_tick_size
risk_per_lot    = ticks_in_sl * trade_tick_value
volume          = risk_amount / risk_per_lot
```

交易量需向下取整到最接近的`volume_step`，并且必须满足`[volume_min, volume_max]`的范围。请确保`volume * trade_contract_size * price`的计算结果在账户余额的合理范围内。

## 使用提示：
- 始终检查`retcode`的值：10009表示交易成功，其他值表示存在问题；
- 使用`GET /error`命令来调试失败的交易；
- `deviation`字段表示订单的最大滑点（默认值为20点，波动较大的市场可能会调整该值）；
- 根据订单类型选择合适的执行策略（`FOK`、`IOC`或`RETURN`）；
- `Candle time`字段表示蜡烛图的开盘时间，而非收盘时间；
- `trade_stops_level`表示止损/止盈水平，以点数表示，且至少等于当前价格与止损/止盈价之间的最小距离；
- 在下达订单前，请确认市场是否处于开放交易时段（通过`trade_mode`字段判断）。