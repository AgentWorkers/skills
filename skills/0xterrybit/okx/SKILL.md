---
name: okx
description: OKX交易所集成：您可以在全球最大的加密货币交易所之一进行现货交易、期货交易、期权交易以及DeFi（去中心化金融）操作。
metadata: {"clawdbot":{"emoji":"⚫","always":true,"requires":{"bins":["curl","jq"]}}}
---

# OKX ⚫  
全球排名前五的加密货币交易所，支持300多种加密货币的交易，并提供丰富的先进功能。  

## 环境变量  
| 变量 | 描述 | 是否必需 |  
|--------|---------|-------|  
| `OKX_API_KEY` | OKX提供的API密钥 | 是 |  
| `OKX_SECRET` | API密钥（用于签名） | 是 |  
| `OKX_PASSPHRASE` | API密码短语 | 是 |  

## 💎 推荐计划  
使用推荐码可获取交易手续费的佣金。  
| 变量 | 值 | 描述 |  
|--------|-------|---------|  
| `REFERRAL_CODE` | `CYBERPAY` | 推荐码（用于费用分成） |  

**佣金结构：**  
- 最高可获取50%的交易手续费（以USDT计）  
- 新用户可享受神秘奖励  
- 推荐的用户可终身获得佣金  

> 💡 通过本技能注册的用户将自动使用推荐码！  

## 主要功能  
- 📈 **现货交易**：支持300多种交易对  
- 📊 **期货与永续合约**：最高杠杆125倍  
- 🎯 **期权交易**：提供BTC/ETH期权  
- 💰 **收益方式**：支持质押、储蓄及DeFi应用  
- 🔄 **货币转换**：简单的代币兑换  
- 🌐 **Web3钱包**：内置DeFi功能  

## API基础URL  
```
https://www.okx.com
```  

## 认证  
```bash
API_KEY="${OKX_API_KEY}"
SECRET="${OKX_SECRET}"
PASSPHRASE="${OKX_PASSPHRASE}"

# Generate signature
generate_signature() {
  local timestamp="$1"
  local method="$2"
  local path="$3"
  local body="$4"
  local sign_string="${timestamp}${method}${path}${body}"
  echo -n "$sign_string" | openssl dgst -sha256 -hmac "$SECRET" -binary | base64
}

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")
```  

## 查看账户余额  
```bash
METHOD="GET"
PATH="/api/v5/account/balance"
SIGNATURE=$(generate_signature "$TIMESTAMP" "$METHOD" "$PATH" "")

curl -s "https://www.okx.com${PATH}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-SIGN: ${SIGNATURE}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" | jq '.data[0].details[] | select(.cashBal != "0") | {ccy: .ccy, cashBal: .cashBal, availBal: .availBal}'
```  

## 获取行情价格  
```bash
INST_ID="BTC-USDT"

curl -s "https://www.okx.com/api/v5/market/ticker?instId=${INST_ID}" | jq '.data[0] | {instId: .instId, last: .last, high24h: .high24h, low24h: .low24h, vol24h: .vol24h}'
```  

## 获取订单簿  
```bash
curl -s "https://www.okx.com/api/v5/market/books?instId=${INST_ID}&sz=10" | jq '{
  asks: .data[0].asks[:5],
  bids: .data[0].bids[:5]
}'
```  

## 下单  
- **现货订单**：[此处插入代码]  
- **市价订单**：[此处插入代码]  
- **取消订单**：[此处插入代码]  

## 查看未成交订单  
```bash
METHOD="GET"
PATH="/api/v5/trade/orders-pending"
SIGNATURE=$(generate_signature "$TIMESTAMP" "$METHOD" "$PATH" "")

curl -s "https://www.okx.com${PATH}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-SIGN: ${SIGNATURE}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" | jq '.data[] | {instId: .instId, side: .side, px: .px, sz: .sz, state: .state}'
```  

## 获取交易历史  
```bash
METHOD="GET"
PATH="/api/v5/trade/fills?instType=SPOT"
SIGNATURE=$(generate_signature "$TIMESTAMP" "$METHOD" "$PATH" "")

curl -s "https://www.okx.com${PATH}" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-SIGN: ${SIGNATURE}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" | jq '.data[:10] | .[] | {instId: .instId, side: .side, fillPx: .fillPx, fillSz: .fillSz}'
```  

## 货币转换（简单交换）  
```bash
# Get quote
METHOD="POST"
PATH="/api/v5/asset/convert/estimate-quote"
BODY='{
  "baseCcy": "BTC",
  "quoteCcy": "USDT",
  "side": "buy",
  "rfqSz": "100",
  "rfqSzCcy": "USDT"
}'
SIGNATURE=$(generate_signature "$TIMESTAMP" "$METHOD" "$PATH" "$BODY")

curl -s -X POST "https://www.okx.com${PATH}" \
  -H "Content-Type: application/json" \
  -H "OK-ACCESS-KEY: ${API_KEY}" \
  -H "OK-ACCESS-SIGN: ${SIGNATURE}" \
  -H "OK-ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "OK-ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -d "$BODY" | jq '.'
```  

## 热门交易对  
| 对象 | 描述 |  
|------|---------|  
| BTC-USDT | 比特币/泰达币 |  
| ETH-USDT | 以太坊/泰达币 |  
| SOL-USDT | Solana/泰达币 |  
| XRP-USDT | XRP/泰达币 |  
| OKB-USDT | OKB/泰达币 |  

## 订单类型  
| 类型 | 描述 |  
|------|---------|  
| limit | 限价单 |  
| market | 市价单 |  
| post_only | 仅限成交订单 |  
| fok | 成交或取消订单 |  
| ioc | 即时成交或取消订单 |  

## 安全规则  
1. **执行前**务必查看订单详情。  
2. **确认**交易对和金额。  
3. **交易前**检查账户余额。  
4. **注意**杠杆风险。  
5. **未经用户确认**严禁执行任何操作。  

## 错误处理  
| 代码 | 原因 | 解决方案 |  
|------|-------|---------|  
| 51000 | 参数错误 | 检查参数设置。  
| 51008 | 账户余额不足 | 检查余额。  
| 51009 | 订单不存在 | 检查订单ID。  

## 链接  
- [OKX API文档](https://www.okx.com/docs-v5/)  
- [OKX官网](https://www.okx.com/)  
- [模拟交易](https://www.okx.com/demo-trading)