---
name: bybit
description: Bybit交易所集成：支持现货交易、衍生品交易以及永续合约交易，杠杆率最高可达100倍。
metadata: {"clawdbot":{"emoji":"🔶","always":true,"requires":{"bins":["curl","jq"]}}}
---

# Bybit 🔶

领先的衍生品交易平台，提供现货交易、永续合约和期权服务，具有极高的流动性。

## 环境变量

| 变量 | 描述 | 是否必需 |
|----------|-------------|----------|
| `BYBIT_API_KEY` | Bybit的API密钥 | 是 |
| `BYBIT_SECRET` | API密钥 | 是 |

## 💎 推荐配置

此功能通过使用推荐码来从交易手续费中赚取佣金。

| 变量 | 值 | 描述 |
|----------|-------|-------------|
| `REFERRAL_CODE` | `CYBERPAY` | 用于费用分成的推荐码 |

**佣金结构：**
- 最高可获取50%的交易手续费（现货、期货、期权）
- 新用户可获得奖励
- 推荐的用户可终身享受佣金

> 💡 通过此功能注册的用户将自动使用推荐码！

## 主要功能

- 📈 **现货交易** - 提供500多种交易对
- 📊 **永续合约** - 支持最高100倍的杠杆
- 🎯 **期权** - 提供BTC/ETH期权
- 💰 **收益方式** - 可通过质押、储蓄等方式获利
- 🤖 **跟单交易** - 可跟随顶尖交易者进行交易
- 🎮 **交易机器人** - 支持网格交易、定期定额投资（DCA）和马丁格尔策略

## API基础URL

```
https://api.bybit.com
```

## 认证

```bash
API_KEY="${BYBIT_API_KEY}"
SECRET="${BYBIT_SECRET}"

# Generate signature
generate_signature() {
  local timestamp="$1"
  local params="$2"
  local sign_string="${timestamp}${API_KEY}5000${params}"
  echo -n "$sign_string" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2
}

TIMESTAMP=$(date +%s%3N)
```

## 获取账户余额

```bash
PARAMS=""
SIGNATURE=$(generate_signature "$TIMESTAMP" "$PARAMS")

curl -s "https://api.bybit.com/v5/account/wallet-balance?accountType=UNIFIED" \
  -H "X-BAPI-API-KEY: ${API_KEY}" \
  -H "X-BAPI-SIGN: ${SIGNATURE}" \
  -H "X-BAPI-TIMESTAMP: ${TIMESTAMP}" \
  -H "X-BAPI-RECV-WINDOW: 5000" | jq '.result.list[0].coin[] | select(.walletBalance != "0") | {coin: .coin, walletBalance: .walletBalance, availableToWithdraw: .availableToWithdraw}'
```

## 获取行情价格

```bash
SYMBOL="BTCUSDT"
CATEGORY="spot"  # spot, linear, inverse, option

curl -s "https://api.bybit.com/v5/market/tickers?category=${CATEGORY}&symbol=${SYMBOL}" | jq '.result.list[0] | {symbol: .symbol, lastPrice: .lastPrice, highPrice24h: .highPrice24h, lowPrice24h: .lowPrice24h, volume24h: .volume24h}'
```

## 获取订单簿

```bash
curl -s "https://api.bybit.com/v5/market/orderbook?category=${CATEGORY}&symbol=${SYMBOL}&limit=10" | jq '{
  asks: .result.a[:5],
  bids: .result.b[:5]
}'
```

## 下单（现货）

```bash
PARAMS='{"category":"spot","symbol":"BTCUSDT","side":"Buy","orderType":"Limit","qty":"0.001","price":"40000"}'
SIGNATURE=$(generate_signature "$TIMESTAMP" "$PARAMS")

curl -s -X POST "https://api.bybit.com/v5/order/create" \
  -H "Content-Type: application/json" \
  -H "X-BAPI-API-KEY: ${API_KEY}" \
  -H "X-BAPI-SIGN: ${SIGNATURE}" \
  -H "X-BAPI-TIMESTAMP: ${TIMESTAMP}" \
  -H "X-BAPI-RECV-WINDOW: 5000" \
  -d "$PARAMS" | jq '.'
```

## 下单（市价单）

```bash
PARAMS='{"category":"spot","symbol":"ETHUSDT","side":"Buy","orderType":"Market","qty":"0.1"}'
SIGNATURE=$(generate_signature "$TIMESTAMP" "$PARAMS")

curl -s -X POST "https://api.bybit.com/v5/order/create" \
  -H "Content-Type: application/json" \
  -H "X-BAPI-API-KEY: ${API_KEY}" \
  -H "X-BAPI-SIGN: ${SIGNATURE}" \
  -H "X-BAPI-TIMESTAMP: ${TIMESTAMP}" \
  -H "X-BAPI-RECV-WINDOW: 5000" \
  -d "$PARAMS" | jq '.'
```

## 下单（永续合约）

```bash
PARAMS='{"category":"linear","symbol":"BTCUSDT","side":"Buy","orderType":"Limit","qty":"0.01","price":"40000","timeInForce":"GTC"}'
SIGNATURE=$(generate_signature "$TIMESTAMP" "$PARAMS")

curl -s -X POST "https://api.bybit.com/v5/order/create" \
  -H "Content-Type: application/json" \
  -H "X-BAPI-API-KEY: ${API_KEY}" \
  -H "X-BAPI-SIGN: ${SIGNATURE}" \
  -H "X-BAPI-TIMESTAMP: ${TIMESTAMP}" \
  -H "X-BAPI-RECV-WINDOW: 5000" \
  -d "$PARAMS" | jq '.'
```

## 获取未成交订单

```bash
PARAMS="category=spot"
SIGNATURE=$(generate_signature "$TIMESTAMP" "$PARAMS")

curl -s "https://api.bybit.com/v5/order/realtime?${PARAMS}" \
  -H "X-BAPI-API-KEY: ${API_KEY}" \
  -H "X-BAPI-SIGN: ${SIGNATURE}" \
  -H "X-BAPI-TIMESTAMP: ${TIMESTAMP}" \
  -H "X-BAPI-RECV-WINDOW: 5000" | jq '.result.list[] | {symbol: .symbol, side: .side, price: .price, qty: .qty, orderStatus: .orderStatus}'
```

## 取消订单

```bash
PARAMS='{"category":"spot","symbol":"BTCUSDT","orderId":"12345678"}'
SIGNATURE=$(generate_signature "$TIMESTAMP" "$PARAMS")

curl -s -X POST "https://api.bybit.com/v5/order/cancel" \
  -H "Content-Type: application/json" \
  -H "X-BAPI-API-KEY: ${API_KEY}" \
  -H "X-BAPI-SIGN: ${SIGNATURE}" \
  -H "X-BAPI-TIMESTAMP: ${TIMESTAMP}" \
  -H "X-BAPI-RECV-WINDOW: 5000" \
  -d "$PARAMS" | jq '.'
```

## 获取持仓（永续合约）

```bash
PARAMS="category=linear&settleCoin=USDT"
SIGNATURE=$(generate_signature "$TIMESTAMP" "$PARAMS")

curl -s "https://api.bybit.com/v5/position/list?${PARAMS}" \
  -H "X-BAPI-API-KEY: ${API_KEY}" \
  -H "X-BAPI-SIGN: ${SIGNATURE}" \
  -H "X-BAPI-TIMESTAMP: ${TIMESTAMP}" \
  -H "X-BAPI-RECV-WINDOW: 5000" | jq '.result.list[] | select(.size != "0") | {symbol: .symbol, side: .side, size: .size, avgPrice: .avgPrice, unrealisedPnl: .unrealisedPnl}'
```

## 获取交易历史

```bash
PARAMS="category=spot"
SIGNATURE=$(generate_signature "$TIMESTAMP" "$PARAMS")

curl -s "https://api.bybit.com/v5/execution/list?${PARAMS}" \
  -H "X-BAPI-API-KEY: ${API_KEY}" \
  -H "X-BAPI-SIGN: ${SIGNATURE}" \
  -H "X-BAPI-TIMESTAMP: ${TIMESTAMP}" \
  -H "X-BAPI-RECV-WINDOW: 5000" | jq '.result.list[:10] | .[] | {symbol: .symbol, side: .side, execPrice: .execPrice, execQty: .execQty}'
```

## 热门交易对

| 交易对 | 描述 |
|------|-------------|
| BTCUSDT | 比特币 / 泰达币 |
| ETHUSDT | 以太坊 / 泰达币 |
| SOLUSDT | Solana / 泰达币 |
| XRPUSDT | XRP / 泰达币 |
| DOGEUSDT | Dogecoin / 泰达币 |

## 订单类型

| 类型 | 描述 |
|------|-------------|
| 限价单 | 限价订单 |
| 市价单 | 市价订单 |
| 仅限成交单 | 仅限成交的订单 |

## 分类

| 分类 | 描述 |
|----------|-------------|
| 现货 | 现货交易 |
| 线性永续合约 | 以USDT为标的的永续合约 |
| 反向永续合约 | 以加密货币为标的的永续合约 |
| 期权 | 期权交易 |

## 安全规则

1. **执行前** **务必** 查看订单详情
2. **确认** 交易对和交易金额
3. **交易前** **检查** 账户余额
4. **提醒** 注意杠杆风险
5. **未经用户确认** **严禁** 执行任何操作

## 错误处理

| 代码 | 原因 | 解决方案 |
|------|-------|----------|
| 10001 | 参数错误 | 检查参数设置 |
| 10003 | API密钥无效 | 检查API密钥是否正确 |
| 110007 | 账户余额不足 | 确保账户内有足够的资金 |

## 链接

- [Bybit API文档](https://bybit-exchange.github.io/docs/)
- [Bybit官网](https://www.bybit.com/)
- [测试网](https://testnet.bybit.com/)