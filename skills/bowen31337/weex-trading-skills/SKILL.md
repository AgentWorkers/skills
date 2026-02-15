---
name: weex-trading
description: **WEEX期货交易所集成**：您可以在WEEX平台上交易USDT-M永续期货，杠杆率最高可达125倍。
metadata:
  emoji: "🔵"
  category: "trading"
  tags: ["crypto", "futures", "trading", "weex", "derivatives"]
  requires:
    bins: ["curl", "jq", "python3", "openssl"]
  compatibility:
    - claude
    - openai
    - gemini
    - llama
    - mistral
    - any-agent
---

# WEEX期货交易 🔵

这是一个OpenAI代理技能，用于在WEEX交易所进行USDT保证金永续期货交易，支持最高125倍的杠杆。

> **Open Agent Skill**：该技能适用于任何支持bash/curl命令的AI代理，包括Claude、GPT、Gemini、LLaMA、Mistral等基于LLM的代理。

## 主要功能

- 📊 **期货交易**：支持USDT永续合约交易，杠杆最高可达125倍
- 💰 **账户管理**：可查看账户余额、持仓情况以及调整保证金设置
- 📈 **市场数据**：提供实时行情数据（包括股票代码、订单簿、K线图和资金费率）
- 🎯 **高级订单**：支持触发式订单、止盈/止损订单以及条件订单
- 🤖 **AI集成**：记录AI的交易决策过程
- 🔌 **通用兼容性**：适用于所有支持shell命令的AI代理

## 环境变量

| 变量 | 说明 | 是否必需 |
|----------|-------------|----------|
| `WEEX_API_KEY` | WEEX的API密钥 | 是 |
| `WEEX_API_SECRET` | API密钥签名 | 是 |
| `WEEX_PASSPHRASE` | API访问密码 | 是 |
| `WEEX_BASE_URL` | API基础URL | 否（默认值：https://api-contract.weex.com） |

## 认证

```bash
API_KEY="${WEEX_API_KEY}"
SECRET="${WEEX_API_SECRET}"
PASSPHRASE="${WEEX_PASSPHRASE}"
BASE_URL="${WEEX_BASE_URL:-https://api-contract.weex.com}"

TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")

# Generate signature
generate_signature() {
  local method="$1"
  local path="$2"
  local body="$3"
  local message="${TIMESTAMP}${method}${path}${body}"
  echo -n "$message" | openssl dgst -sha256 -hmac "$SECRET" -binary | base64
}
```

---

# 市场数据接口（无需认证）

## 获取服务器时间

```bash
curl -s "${BASE_URL}/capi/v2/market/time" | jq '.'
```

## 获取所有合约信息

```bash
curl -s "${BASE_URL}/capi/v2/market/contracts" | jq '.data[] | {symbol: .symbol, baseCoin: .underlying_index, quoteCoin: .quote_currency, contractVal: .contract_val, minLeverage: .minLeverage, maxLeverage: .maxLeverage, tickSize: .tick_size, sizeIncrement: .size_increment}'
```

## 获取单个合约信息

```bash
SYMBOL="cmt_btcusdt"

curl -s "${BASE_URL}/capi/v2/market/contracts?symbol=${SYMBOL}" | jq '.data'
```

## 获取股票代码价格

```bash
SYMBOL="cmt_btcusdt"

curl -s "${BASE_URL}/capi/v2/market/ticker?symbol=${SYMBOL}" | jq '.data | {symbol: .symbol, last: .last, high: .high_24h, low: .low_24h, volume: .volume_24h, markPrice: .markPrice}'
```

## 获取所有股票代码

```bash
curl -s "${BASE_URL}/capi/v2/market/tickers" | jq '.data[] | {symbol: .symbol, last: .last, change: .priceChangePercent, volume: .volume_24h}'
```

## 获取订单簿信息

```bash
SYMBOL="cmt_btcusdt"

curl -s "${BASE_URL}/capi/v2/market/depth?symbol=${SYMBOL}&limit=15" | jq '.data | {asks: .asks[:5], bids: .bids[:5]}'
```

## 获取最近的交易记录

```bash
SYMBOL="cmt_btcusdt"
LIMIT="50"

curl -s "${BASE_URL}/capi/v2/market/trades?symbol=${SYMBOL}&limit=${LIMIT}" | jq '.data[] | {time: .time, price: .price, size: .size, side: (if .isBuyerMaker then "sell" else "buy" end)}'
```

## 获取K线图数据

```bash
SYMBOL="cmt_btcusdt"
GRANULARITY="1h"    # 1m, 5m, 15m, 30m, 1h, 4h, 12h, 1d, 1w
LIMIT="100"

curl -s "${BASE_URL}/capi/v2/market/candles?symbol=${SYMBOL}&granularity=${GRANULARITY}&limit=${LIMIT}" | jq '.data[] | {timestamp: .[0], open: .[1], high: .[2], low: .[3], close: .[4], volume: .[5]}'
```

## 获取指数价格

```bash
SYMBOL="cmt_btcusdt"

curl -s "${BASE_URL}/capi/v2/market/index?symbol=${SYMBOL}" | jq '.data | {symbol: .symbol, index: .index, timestamp: .timestamp}'
```

## 获取未平仓合约数量

```bash
SYMBOL="cmt_btcusdt"

curl -s "${BASE_URL}/capi/v2/market/open_interest?symbol=${SYMBOL}" | jq '.data[] | {symbol: .symbol, openInterest: .base_volume, value: .target_volume}'
```

## 获取当前资金费率

```bash
SYMBOL="cmt_btcusdt"

curl -s "${BASE_URL}/capi/v2/market/currentFundRate?symbol=${SYMBOL}" | jq '.data[] | {symbol: .symbol, rate: .fundingRate, nextSettlement: .timestamp}'
```

## 获取历史资金费率

```bash
SYMBOL="cmt_btcusdt"
LIMIT="20"

curl -s "${BASE_URL}/capi/v2/market/getHistoryFundRate?symbol=${SYMBOL}&limit=${LIMIT}" | jq '.data[] | {symbol: .symbol, rate: .fundingRate, settleTime: .fundingTime}'
```

## 获取下一次资金调整时间

```bash
SYMBOL="cmt_btcusdt"

curl -s "${BASE_URL}/capi/v2/market/funding_time?symbol=${SYMBOL}" | jq '.data | {symbol: .symbol, nextFundingTime: .fundingTime}'
```

---

# 账户接口（需要认证）

## 获取账户资产信息

```bash
PATH_URL="/capi/v2/account/assets"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data[] | {coin: .coinName, available: .available, frozen: .frozen, equity: .equity, unrealizedPnl: .unrealizePnl}'
```

## 获取带设置信息的账户列表

```bash
PATH_URL="/capi/v2/account/getAccounts"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data'
```

## 根据货币名称获取单个账户信息

```bash
COIN="USDT"

PATH_URL="/capi/v2/account/getAccount?coin=${COIN}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data'
```

## 获取用户设置

```bash
SYMBOL="cmt_btcusdt"

PATH_URL="/capi/v2/account/settings?symbol=${SYMBOL}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data'
```

## 更改杠杆比例

```bash
SYMBOL="cmt_btcusdt"
LEVERAGE="20"
MARGIN_MODE="1"        # 1=Cross, 3=Isolated

PATH_URL="/capi/v2/account/leverage"
BODY="{\"symbol\":\"${SYMBOL}\",\"marginMode\":${MARGIN_MODE},\"longLeverage\":\"${LEVERAGE}\",\"shortLeverage\":\"${LEVERAGE}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 调整持仓保证金（仅限隔离账户）

```bash
POSITION_ID="123456789"      # Isolated position ID
AMOUNT="100"                 # Positive to add, negative to reduce

PATH_URL="/capi/v2/account/adjustMargin"
BODY="{\"coinId\":2,\"isolatedPositionId\":${POSITION_ID},\"collateralAmount\":\"${AMOUNT}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 自动补充保证金（仅限隔离账户）

```bash
POSITION_ID="123456789"      # Isolated position ID
AUTO_APPEND="true"           # true to enable, false to disable

PATH_URL="/capi/v2/account/modifyAutoAppendMargin"
BODY="{\"positionId\":${POSITION_ID},\"autoAppendMargin\":${AUTO_APPEND}}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 获取账户账单历史

```bash
COIN="USDT"
LIMIT="20"

PATH_URL="/capi/v2/account/bills"
BODY="{\"coin\":\"${COIN}\",\"limit\":${LIMIT}}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.data'
```

---

# 持仓接口（需要认证）

## 获取所有持仓信息

```bash
PATH_URL="/capi/v2/account/position/allPosition"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data[] | select(.size != "0") | {symbol: .symbol, side: .side, size: .size, leverage: .leverage, unrealizedPnl: .unrealizePnl, entryPrice: .avg_cost}'
```

## 获取单个持仓信息

```bash
SYMBOL="cmt_btcusdt"

PATH_URL="/capi/v2/account/position/singlePosition?symbol=${SYMBOL}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data[] | {symbol: .symbol, side: .side, size: .size, leverage: .leverage, unrealizedPnl: .unrealizePnl, entryPrice: .avg_cost, liquidationPrice: .liq_price}'
```

## 更改保证金模式

```bash
SYMBOL="cmt_btcusdt"
MARGIN_MODE="1"        # 1=Cross, 3=Isolated

PATH_URL="/capi/v2/account/position/changeHoldModel"
BODY="{\"symbol\":\"${SYMBOL}\",\"marginMode\":${MARGIN_MODE},\"separatedMode\":1}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

---

# 订单接口（需要认证）

## 下单（市价单）

```bash
SYMBOL="cmt_btcusdt"
SIZE="10"              # Quantity in contracts
TYPE="1"               # 1=Open Long, 2=Open Short, 3=Close Long, 4=Close Short
CLIENT_OID="order_$(date +%s)"

PATH_URL="/capi/v2/order/placeOrder"
BODY="{\"symbol\":\"${SYMBOL}\",\"client_oid\":\"${CLIENT_OID}\",\"size\":\"${SIZE}\",\"type\":\"${TYPE}\",\"order_type\":\"0\",\"match_price\":\"1\",\"price\":\"0\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 下单（限价单）

```bash
SYMBOL="cmt_btcusdt"
SIZE="10"
TYPE="1"               # 1=Open Long
PRICE="90000"          # Limit price
ORDER_TYPE="0"         # 0=Normal, 1=Post-only, 2=FOK, 3=IOC
CLIENT_OID="limit_$(date +%s)"

PATH_URL="/capi/v2/order/placeOrder"
BODY="{\"symbol\":\"${SYMBOL}\",\"client_oid\":\"${CLIENT_OID}\",\"size\":\"${SIZE}\",\"type\":\"${TYPE}\",\"order_type\":\"${ORDER_TYPE}\",\"match_price\":\"0\",\"price\":\"${PRICE}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 获取未成交订单

```bash
PATH_URL="/capi/v2/order/current"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data[] | {orderId: .order_id, symbol: .symbol, side: .type, price: .price, size: .size, status: .status}'
```

## 获取订单详情

```bash
ORDER_ID="1234567890"

PATH_URL="/capi/v2/order/detail?orderId=${ORDER_ID}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data'
```

## 获取订单历史记录

```bash
SYMBOL="cmt_btcusdt"
LIMIT="50"

PATH_URL="/capi/v2/order/history?symbol=${SYMBOL}&limit=${LIMIT}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data[] | {orderId: .order_id, symbol: .symbol, side: .type, price: .price, size: .size, filledSize: .filled_qty, status: .status}'
```

## 获取交易成交信息

```bash
SYMBOL="cmt_btcusdt"
LIMIT="50"

PATH_URL="/capi/v2/order/fills?symbol=${SYMBOL}&limit=${LIMIT}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data[] | {tradeId: .trade_id, orderId: .order_id, symbol: .symbol, price: .price, size: .size, fee: .fee, time: .created_at}'
```

## 取消订单

```bash
ORDER_ID="1234567890"

PATH_URL="/capi/v2/order/cancel_order"
BODY="{\"orderId\":\"${ORDER_ID}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 取消所有订单

```bash
SYMBOL="cmt_btcusdt"    # Optional: omit to cancel all

PATH_URL="/capi/v2/order/cancelAllOrders"
BODY="{\"symbol\":\"${SYMBOL}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 平仓所有持仓

```bash
PATH_URL="/capi/v2/order/closePositions"
BODY="{}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

---

# 触发式订单接口（需要认证）

## 下单（止盈/止损订单）

```bash
SYMBOL="cmt_btcusdt"
SIZE="10"
TYPE="1"               # 1=Open Long, 2=Open Short, 3=Close Long, 4=Close Short
TRIGGER_PRICE="95000"  # Price that triggers the order
EXECUTE_PRICE="0"      # 0 for market, or limit price
TRIGGER_TYPE="1"       # 1=Fill price, 2=Mark price, 3=Index price
CLIENT_OID="trigger_$(date +%s)"

PATH_URL="/capi/v2/order/plan_order"
BODY="{\"symbol\":\"${SYMBOL}\",\"client_oid\":\"${CLIENT_OID}\",\"size\":\"${SIZE}\",\"type\":\"${TYPE}\",\"trigger_price\":\"${TRIGGER_PRICE}\",\"execute_price\":\"${EXECUTE_PRICE}\",\"trend_side\":\"1\",\"trigger_type\":\"${TRIGGER_TYPE}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 获取当前生效的触发式订单

```bash
SYMBOL="cmt_btcusdt"

PATH_URL="/capi/v2/order/currentPlan?symbol=${SYMBOL}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data[] | {orderId: .order_id, symbol: .symbol, triggerPrice: .trigger_price, size: .size, type: .type}'
```

## 获取触发式订单的历史记录

```bash
SYMBOL="cmt_btcusdt"
LIMIT="50"

PATH_URL="/capi/v2/order/historyPlan?symbol=${SYMBOL}&limit=${LIMIT}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "GET" "$PATH_URL" "")

curl -s "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" | jq '.data[] | {orderId: .order_id, symbol: .symbol, triggerPrice: .trigger_price, status: .status}'
```

## 取消触发式订单

```bash
ORDER_ID="1234567890"

PATH_URL="/capi/v2/order/cancel_plan"
BODY="{\"orderId\":\"${ORDER_ID}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

---

# 止盈/止损订单接口（需要认证）

## 下单（止盈/止损订单）

```bash
SYMBOL="cmt_btcusdt"
SIDE="1"               # 1=Long position, 2=Short position
TP_PRICE="100000"      # Take profit trigger price
SL_PRICE="85000"       # Stop loss trigger price
TP_SIZE="10"           # Take profit size (0 for entire position)
SL_SIZE="10"           # Stop loss size (0 for entire position)

PATH_URL="/capi/v2/order/placeTpSlOrder"
BODY="{\"symbol\":\"${SYMBOL}\",\"side\":\"${SIDE}\",\"tp_trigger_price\":\"${TP_PRICE}\",\"sl_trigger_price\":\"${SL_PRICE}\",\"tp_size\":\"${TP_SIZE}\",\"sl_size\":\"${SL_SIZE}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

## 修改止盈/止损订单

```bash
SYMBOL="cmt_btcusdt"
SIDE="1"               # 1=Long position, 2=Short position
TP_PRICE="105000"      # New take profit price
SL_PRICE="82000"       # New stop loss price

PATH_URL="/capi/v2/order/modifyTpSlOrder"
BODY="{\"symbol\":\"${SYMBOL}\",\"side\":\"${SIDE}\",\"tp_trigger_price\":\"${TP_PRICE}\",\"sl_trigger_price\":\"${SL_PRICE}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

---

# AI集成接口（需要认证）

## 上传AI交易日志

```bash
AI_LOG="Trading decision: Buy BTC based on momentum indicators"
ORDER_ID="1234567890"

PATH_URL="/capi/v2/order/uploadAiLog"
BODY="{\"orderId\":\"${ORDER_ID}\",\"aiLog\":\"${AI_LOG}\"}"
TIMESTAMP=$(python3 -c "import time; print(int(time.time() * 1000))")
SIGNATURE=$(generate_signature "POST" "$PATH_URL" "$BODY")

curl -s -X POST "${BASE_URL}${PATH_URL}" \
  -H "ACCESS-KEY: ${API_KEY}" \
  -H "ACCESS-SIGN: ${SIGNATURE}" \
  -H "ACCESS-PASSPHRASE: ${PASSPHRASE}" \
  -H "ACCESS-TIMESTAMP: ${TIMESTAMP}" \
  -H "Content-Type: application/json" \
  -d "$BODY" | jq '.'
```

---

# 参考表格

## 订单类型

| 类型 | 说明 |
|------|-------------|
| `1` | 开多（买入建仓） |
| `2` | 开空（卖出建仓） |
| `3` | 平多（卖出平仓） |
| `4` | 平空（买入平仓） |

## 执行类型

| order_type | 说明 |
|------------|-------------|
| `0` | 普通订单 |
| `1` | 仅限做市商（Post-only） |
| `2` | FOK（立即成交或取消） |
| `3` | IOC（立即成交或取消） |

## 价格类型

| match_price | 说明 |
|-------------|-------------|
| `0` | 限价单 |
| `1` | 市价单 |

## 保证金模式

| marginMode | 说明 |
|------------|-------------|
| `1` | 跨账户保证金 |
| `3` | 隔离账户保证金 |

## 触发类型

| trigger_type | 说明 |
|--------------|-------------|
| `1` | 最后成交价 |
| `2` | 标价 |
| `3` | 指数价格 |

## 常见交易对

| 对象 | 说明 |
|------|-------------|
| cmt_btcusdt | 比特币 / USDT |
| cmt_ethusdt | 以太坊 / USDT |
| cmt_solusdt | Solana / USDT |
| cmt_xrpusdt | XRP / USDT |
| cmt_dogeusdt | Dogecoin / USDT |
| cmt_bnbusdt | BNB / USDT |

---

# 安全规则

1. **在执行前**务必显示订单详情。
2. **核实**交易的货币对和数量。
3. **交易前**检查账户余额。
4. **提醒**注意杠杆风险（最高125倍）。
5. **未经用户确认**切勿执行任何操作。
6. **在执行前**确认是否需要平仓持仓。

---

# 错误代码

| 代码 | 说明 | 解决方案 |
|------|-------------|----------|
| `00000` | 成功 | - |
| `40001` | 参数无效 | 检查参数格式 |
| `40101` | API密钥/签名无效 | 核对凭证和时间戳 |
| `40301` | IP地址未在白名单中 | 将IP地址添加到白名单 |
| `42901 | 超过请求频率限制 | 减少请求频率 |
| `50001` | 内部错误 | 延迟后重试 |

---

# 请求频率限制

| 类别 | IP地址限制 | 用户ID限制 |
|----------|----------|-----------|
| 市场数据 | 每秒20次 | 不适用 |
| 账户信息 | 每秒10次 | 每秒10次 |
| 下单 | 每秒10次 | 每秒10次 |

---

# 额外资源

- [WEEX官网](https://www.weex.com)
- API基础URL：`https://api-contract.weex.com`
- [API参考文档](references/api_reference.md)