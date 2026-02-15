---
name: groww
description: 在 Groww（印度券商平台）上交易股票并管理投资组合。当用户询问有关印度股票的信息、NSE/BSE 的股价、投资组合持仓情况、下达买卖订单、查询订单状态或任何与 Groww 相关的交易问题时，可以使用该功能。该平台支持实时报价、LTP（最近成交价）、OHLC（开盘价、最高价、最低价、收盘价）数据、历史蜡烛图以及订单管理功能。
---

# Groww Trading

通过 Groww 进行印度股票的交易。支持投资组合管理、市场数据查询以及订单执行功能。

## 设置

1. 从 Groww 应用程序中获取 API 密钥：  
   转到 “Stocks” → “Settings” → “API Trading” → “Generate API key”。

2. 将 API 密钥添加到 OpenClaw 的配置文件中：
   ```bash
   openclaw configure
   # Add env: GROWW_API_KEY=your_key_here
   ```

## MCP 服务器的使用

groww-mcp 服务器已经配置完成。可以通过 mcporter 调用相关工具：
   ```bash
# Portfolio
mcporter call groww-mcp.portfolio

# Market data
mcporter call groww-mcp.market-data action=live-quote symbol=TATAMOTORS
mcporter call groww-mcp.market-data action=ltp symbols=TATAMOTORS,RELIANCE
mcporter call groww-mcp.market-data action=ohlc symbol=TCS

# Orders
mcporter call groww-mcp.place_order symbol=TATAMOTORS quantity=10 side=BUY type=MARKET
mcporter call groww-mcp.order_status orderId=ABC123
mcporter call groww-mcp.cancel_order orderId=ABC123
```

## 直接使用 API（备用方案）

如果 MCP 出现问题，可以直接使用 Groww 的 API：

### 基本 URL
```
https://api.groww.in/v1/
```

### 请求头
```bash
Authorization: Bearer $GROWW_API_KEY
Accept: application/json
Content-Type: application/json
```

### 端点

**投资组合/持仓：**
```bash
curl -H "Authorization: Bearer $GROWW_API_KEY" -H "Accept: application/json" \
  "https://api.groww.in/v1/holdings/user"
```

**实时报价：**
```bash
curl -H "Authorization: Bearer $GROWW_API_KEY" -H "Accept: application/json" \
  "https://api.groww.in/v1/live-data/quote?exchange=NSE&segment=CASH&trading_symbol=TATAMOTORS"
```

**最新成交价（LTP）：**
```bash
curl -H "Authorization: Bearer $GROWW_API_KEY" -H "Accept: application/json" \
  "https://api.groww.in/v1/live-data/ltp?segment=CASH&exchange_symbols=NSE:TATAMOTORS,NSE:RELIANCE"
```

**开盘价、最高价、最低价、收盘价（OHLC）：**
```bash
curl -H "Authorization: Bearer $GROWW_API_KEY" -H "Accept: application/json" \
  "https://api.groww.in/v1/live-data/ohlc?segment=CASH&exchange_symbols=NSE:TATAMOTORS"
```

**历史K线数据：**
```bash
curl -H "Authorization: Bearer $GROWW_API_KEY" -H "Accept: application/json" \
  "https://api.groww.in/v1/historical/candle/range?exchange=NSE&segment=CASH&trading_symbol=TATAMOTORS&interval=5m&start_time=2024-06-01T09:15:00&end_time=2024-06-01T15:30:00"
```

**下单：**
```bash
curl -X POST -H "Authorization: Bearer $GROWW_API_KEY" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"trading_symbol":"TATAMOTORS","quantity":10,"validity":"DAY","exchange":"NSE","segment":"CASH","product":"CNC","order_type":"MARKET","transaction_type":"BUY"}' \
  "https://api.groww.in/v1/order/create"
```

**订单状态：**
```bash
curl -H "Authorization: Bearer $GROWW_API_KEY" -H "Accept: application/json" \
  "https://api.groww.in/v1/order/detail/{groww_order_id}?segment=CASH"
```

**取消订单：**
```bash
curl -X POST -H "Authorization: Bearer $GROWW_API_KEY" \
  -H "Accept: application/json" -H "Content-Type: application/json" \
  -d '{"segment":"CASH","groww_order_id":"ABC123"}' \
  "https://api.groww.in/v1/order/cancel"
```

## 股票代码

使用 NSE（National Stock Exchange of India）的股票代码：
- TATAMOTORS, RELIANCE, TCS, INFY, HDFCBANK
- WIPRO, ICICIBANK, SBIN, BHARTIARTL, ITC

## 市场交易时间

- 开盘前：上午 9:00 - 9:15（IST 时间）
- 交易时间：上午 9:15 - 下午 3:30（IST 时间）
- 周一至周五（节假日除外）

## 示例查询命令

- “显示我的 Groww 投资组合”
- “TATAMOTORS 的价格是多少？”
- “以 4200 的价格买入 10 股 RELIANCE 股票”
- “以限价 4200 卖出 5 股 TCS 股票”
- “取消订单 ABC123”
- “获取 INFY 的历史数据”