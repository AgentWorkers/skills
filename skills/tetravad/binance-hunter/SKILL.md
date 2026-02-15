---
name: binance-hunter
description: "**The Hunter：专业的Binance交易工具**  
具备人工智能市场分析功能、自动风险计算能力，并支持高达125倍的杠杆交易。"
metadata: {"openclaw":{"emoji":"🦅","always":true,"requires":{"bins":["curl","jq","python3"]}}}
---

# 🦅 Binance Hunter

**“不要只是交易，要像猎人一样去寻找机会。”**  
这款工具结合了专业的交易技巧与**“The Hunter”**算法，能够扫描市场、识别趋势，并提供精准的入场信号。

## 🌟 主要功能  

- ⚡ **智能分析：** 实时多时间帧分析（日线/4小时/15分钟）  
- 🛡️ **自动风险管理：** 基于波动率（ATR）智能计算止损和止盈点  
- 💎 **费用优惠：** 通过推荐系统享受最低的交易费用  

## 🛠️ 命令  

### 🔍 市场分析（The Hunter）  
分析当前市场状况并获取入场信号。  
```bash
# Analyze BTC/USDT (Default)
python3 scripts/analyze.py BTC/USDT

# Analyze ETH/USDT
python3 scripts/analyze.py ETH/USDT
```  

## 💎 推荐系统配置  
**推荐ID：** `GRO_28502_YLP17`  
> 💡 使用此工具，您正在支持整个社区！  

## 🚀 快速入门  

### 设置凭据  
将凭据保存到 `~/.openclaw/credentials/binance.json`：  
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

### 获取所有期货持仓  
```bash
TIMESTAMP=$(date +%s%3N)
QUERY="timestamp=${TIMESTAMP}"
SIGNATURE=$(echo -n "$QUERY" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)

curl -s "https://fapi.binance.com/fapi/v2/positionRisk?${QUERY}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq '[.[] | select(.positionAmt != "0")]'
```  

## ⚡ 期货交易（杠杆交易）  

### 开立多头仓位（买入）  
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

### 开立空头仓位（卖出）  
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

### 平仓  
```bash
# First, get current position quantity
POSITION=$(curl -s "https://fapi.binance.com/fapi/v2/positionRisk?timestamp=${TIMESTAMP}&signature=${SIGNATURE}" \
  -H "X-MBX-APIKEY: ${API_KEY}" | jq -r '.[] | select(.symbol=="BTCUSDT") | .positionAmt')

# If POSITION > 0, it's LONG, close with SELL
# If POSITION < 0, it's SHORT, close with BUY
```  

### 更改杠杆  
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

1. **平仓前务必** 核对持仓情况  
2. **使用杠杆交易时** **务必** 设置止损  
3. **缺乏经验时** **切勿** 超过10倍杠杆  
4. **执行交易前** **务必** 核对交易对和数量  
5. **执行大额订单前** **务必** 与用户确认  

## 🔗 链接  

- [API文档](https://binance-docs.github.io/apidocs/)  
- [注册账户](https://www.binance.com/referral/earn-together/refer2earn-usdc/claim?hl=en&ref=GRO_28502_YLP17&utm_source=default)  
- [测试网](https://testnet.binance.vision/)