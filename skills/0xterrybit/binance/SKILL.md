---
name: binance
description: **Binance交易所集成**：您可以在全球最大的加密货币交易所上进行现货交易、期货交易以及投资组合管理。
metadata: {"clawdbot":{"emoji":"🟡","always":true,"requires":{"bins":["curl","jq"]}}}
---

# Binance 🟡  
全球最大的加密货币交易所，提供600多种具有深厚流动性的加密货币交易服务。  

## 环境变量  
| 变量 | 描述 | 是否必填 |  
|----------|-------------|----------|  
| `BINANCE_API_KEY` | Binance的API密钥 | 是 |  
| `BINANCE_SECRET` | Binance的API密钥 | 是 |  

## 💎 推荐配置  
该功能通过使用推荐ID来获取交易手续费的分成。  
| 变量 | 值 | 描述 |  
|----------|-------|-------------|  
| `REFERRAL_ID` | `CYBERPAY` | 用于费用分成的推荐ID |  

**佣金结构：**  
- 标准佣金：最高20%的交易手续费  
- 持有500 BNB以上：最高50%的交易手续费  
- 推荐的用户可终身获得佣金  

> 💡 通过该功能注册的用户将自动使用该推荐ID！  

## 主要功能  
- 📈 **现货交易**：支持600多种交易对  
- 📊 **期货交易**：最高125倍杠杆  
- 💰 **收益方式**：质押、储蓄、流动性挖矿  
- 🔄 **转换**：简单的代币兑换  
- 📱 **投资组合**：追踪所有资产  

## API基础URL  
- 现货交易：`https://api.binance.com`  
- 期货交易：`https://fapi.binance.com`  
- 测试网：`https://testnet.binance.vision`  

## 认证  

```bash
API_KEY="${BINANCE_API_KEY}"
SECRET="${BINANCE_SECRET}"

# Generate signature
generate_signature() {
  local query_string="$1"
  echo -n "$query_string" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2
}

TIMESTAMP=$(date +%s%3N)
```  

## 获取账户信息  

```bash
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(generate_signature "$QUERY")

curl -s "https://api.binance.com/api/v3/account?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '{
    balances: [.balances[] | select(.free != "0.00000000" or .locked != "0.00000000")]
  }'
```  

## 获取价格  

```bash
SYMBOL="BTCUSDT"

curl -s "https://api.binance.com/api/v3/ticker/price?symbol=${SYMBOL}" | jq '.'
```  

## 获取订单簿  

```bash
curl -s "https://api.binance.com/api/v3/depth?symbol=${SYMBOL}&limit=10" | jq '{
  bids: .bids[:5],
  asks: .asks[:5]
}'
```  

## 下单（现货交易）  

```bash
SYMBOL="BTCUSDT"
SIDE="BUY"  # BUY or SELL
TYPE="LIMIT"  # LIMIT, MARKET, STOP_LOSS, etc.
QUANTITY="0.001"
PRICE="40000"

QUERY="symbol=${SYMBOL}&side=${SIDE}&type=${TYPE}&timeInForce=GTC&quantity=${QUANTITY}&price=${PRICE}&timestamp=${TIMESTAMP}"
SIGNATURE=$(generate_signature "$QUERY")

curl -s -X POST "https://api.binance.com/api/v3/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```  

## 下单（市价单）  

```bash
SYMBOL="ETHUSDT"
SIDE="BUY"
QUANTITY="0.1"

QUERY="symbol=${SYMBOL}&side=${SIDE}&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(generate_signature "$QUERY")

curl -s -X POST "https://api.binance.com/api/v3/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```  

## 获取未成交订单  

```bash
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(generate_signature "$QUERY")

curl -s "https://api.binance.com/api/v3/openOrders?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.[] | {symbol: .symbol, side: .side, price: .price, quantity: .origQty, status: .status}'
```  

## 取消订单  

```bash
SYMBOL="BTCUSDT"
ORDER_ID="12345678"

QUERY="symbol=${SYMBOL}&orderId=${ORDER_ID}&timestamp=${TIMESTAMP}"
SIGNATURE=$(generate_signature "$QUERY")

curl -s -X DELETE "https://api.binance.com/api/v3/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```  

## 获取交易历史  

```bash
SYMBOL="BTCUSDT"

QUERY="symbol=${SYMBOL}&timestamp=${TIMESTAMP}"
SIGNATURE=$(generate_signature "$QUERY")

curl -s "https://api.binance.com/api/v3/myTrades?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.[-10:] | .[] | {symbol: .symbol, price: .price, qty: .qty, time: .time}'
```  

## 期货交易：获取持仓情况  

```bash
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(generate_signature "$QUERY")

curl -s "https://fapi.binance.com/fapi/v2/positionRisk?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.[] | select(.positionAmt != "0") | {symbol: .symbol, positionAmt: .positionAmt, entryPrice: .entryPrice, unrealizedProfit: .unRealizedProfit}'
```  

## 转换（简单代币兑换）  

```bash
FROM_ASSET="USDT"
TO_ASSET="BTC"
FROM_AMOUNT="100"

# Get quote
QUERY="fromAsset=${FROM_ASSET}&toAsset=${TO_ASSET}&fromAmount=${FROM_AMOUNT}&timestamp=${TIMESTAMP}"
SIGNATURE=$(generate_signature "$QUERY")

curl -s -X POST "https://api.binance.com/sapi/v1/convert/getQuote?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```  

## 热门交易对  
| 对象 | 描述 |  
|------|-------------|  
| BTCUSDT | 比特币 / Tether |  
| ETHUSDT | 以太坊 / Tether |  
| BNBUSDT | BNB / Tether |  
| SOLUSDT | Solana / Tether |  
| XRPUSDT | XRP / Tether |  
| DOGEUSDT | Dogecoin / Tether |  

## 订单类型  
| 类型 | 描述 |  
|------|-------------|  
| LIMIT | 以指定价格下达限价单 |  
| MARKET | 以当前价格下达市价单 |  
| STOP_LOSS | 止损单 |  
| STOP_LOSS_LIMIT | 止损限价单 |  
| TAKE_PROFIT | 盈利单 |  
| TAKE_PROFIT_LIMIT | 盈利限价单 |  

## 安全规则  
1. **执行前** **务必** 查看订单详情  
2. **确认** 交易对象和金额  
3. **交易前** **检查** 账户余额  
4. **提醒** 期货交易的杠杆风险  
5. **未经用户确认** **严禁** 执行交易  

## 错误处理  
| 错误代码 | 原因 | 解决方案 |  
|-------|-------|----------|  
| `-1013` | 数量无效 | 检查单量过滤器 |  
| `-2010` | 账户余额不足 | 检查账户余额 |  
| `-1021` | 时间戳超出接收窗口 | 同步系统时间 |  

## 链接  
- [Binance API文档](https://binance-docs.github.io/apidocs/)  
- [Binance官网](https://www.binance.com/)  
- [测试网](https://testnet.binance.vision/)