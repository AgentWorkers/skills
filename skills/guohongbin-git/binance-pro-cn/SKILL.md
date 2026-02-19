---
name: binance-pro-cn
description: "币安专业版 | Binance Pro  
完整整合了币安的所有功能：  
- 现货/合约交易（Spot/futures trading）  
- 杠杆交易（Leverage trading）  
- 质押服务（Staking）  
关键词：  
币安（Binance）、交易（Trading）"
metadata:
  openclaw:
    emoji: 🟡
    fork-of: "https://clawhub.ai"
---
# Binance Pro 🟡

这是一套专门用于在Binance（全球最大的加密货币交易所）进行交易的专业技能指南。

## 🚀 快速入门

### 设置凭据

将凭据保存到 `~/.openclaw/credentials/binance.json` 文件中：
```json
{
  "apiKey": "YOUR_API_KEY",
  "secretKey": "YOUR_SECRET_KEY"
}
```

### 环境变量（可选）
```bash
export BINANCE_API_KEY="your_api_key"
export BINANCE_SECRET="your_secret_key"
```

## 📊 基本查询

### 查看现货余额
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://api.binance.com/api/v3/account?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '[.balances[] | select(.free != "0.00000000")]'
```

### 获取当前价格
```bash
curl -s "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT" | jq '.'
```

### 获取所有期货头寸
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://fapi.binance.com/fapi/v2/positionRisk?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '[.[] | select(.positionAmt != "0")]'
```

## ⚡ 期货交易（杠杆交易）

### 开立多头头寸（买入）
```bash
SYMBOL="BTCUSDT"
SIDE="BUY"
QUANTITY="0.001"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=${SIDE}&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### 开立空头头寸（卖出）
```bash
SYMBOL="BTCUSDT"
SIDE="SELL"
QUANTITY="0.001"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=${SIDE}&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### 设置止损
```bash
SYMBOL="BTCUSDT"
SIDE="SELL"  # To close LONG use SELL, to close SHORT use BUY
STOP_PRICE="75000"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=${SIDE}&type=STOP_MARKET&stopPrice=${STOP_PRICE}&closePosition=true&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### 设置止盈
```bash
SYMBOL="BTCUSDT"
SIDE="SELL"  # To close LONG use SELL, to close SHORT use BUY
TP_PRICE="85000"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=${SIDE}&type=TAKE_PROFIT_MARKET&stopPrice=${TP_PRICE}&closePosition=true&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### 平仓（市价）
```bash
# First, get current position quantity
POSITION=$(curl -s "https://fapi.binance.com/fapi/v2/positionRisk?timestamp=${TIMESTAMP}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq -r '.[] | select(.symbol=="BTCUSDT") | .positionAmt')

# If POSITION > 0, it's LONG, close with SELL
# If POSITION < 0, it's SHORT, close with BUY
```

### 更改杠杆比例
```bash
SYMBOL="BTCUSDT"
LEVERAGE="10"  # 1 to 125

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&leverage=${LEVERAGE}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://fapi.binance.com/fapi/v1/leverage?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

## 📈 现货交易

### 买入（市价）
```bash
SYMBOL="ETHUSDT"
QUANTITY="0.1"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=BUY&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://api.binance.com/api/v3/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### 卖出（市价）
```bash
SYMBOL="ETHUSDT"
QUANTITY="0.1"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&side=SELL&type=MARKET&quantity=${QUANTITY}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X POST "https://api.binance.com/api/v3/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

## 🔧 实用工具

### 查看未成交订单
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

# Futures
curl -s "https://fapi.binance.com/fapi/v1/openOrders?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### 取消订单
```bash
SYMBOL="BTCUSDT"
ORDER_ID="123456789"

TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&orderId=${ORDER_ID}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s -X DELETE "https://fapi.binance.com/fapi/v1/order?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.'
```

### 查看交易历史
```bash
SYMBOL="BTCUSDT"
TIMESTAMP=$(date +%s%3N)
QUERY="symbol=${SYMBOL}&timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://fapi.binance.com/fapi/v1/userTrades?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '.[-10:]'
```

## 🏦 期货详细余额
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://fapi.binance.com/fapi/v2/balance?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '[.[] | select(.balance != "0")]'
```

## 📋 热门交易对

| 交易对 | 说明 |
|------|-------------|
| BTCUSDT | 比特币 |
| ETHUSDT | 以太坊 |
| BNBUSDT | BNB |
| SOLUSDT | Solana |
| XRPUSDT | XRP |
| DOGEUSDT | Dogecoin |
| ADAUSDT | Cardano |
| AVAXUSDT | Avalanche |

## ⚠️ 安全规则

1. **在平仓前**务必核实你的头寸情况。
2. **进行杠杆交易时**必须设置止损。
3. **没有交易经验的情况下**，**切勿使用超过10倍的杠杆**。
4. **执行交易前**请确认交易对和数量。
5. **执行大额交易前**请与用户确认。

## 🔗 链接

- [API文档](https://binance-docs.github.io/apidocs/)
- [注册账户](https://accounts.binance.com/register?ref=CPA_00F3AR52CL)
- [测试网](https://testnet.binance.vision/)

---
*本技能由Total Easy Software的Clayton Martins创建*