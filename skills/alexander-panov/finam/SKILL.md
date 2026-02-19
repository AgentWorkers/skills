---
name: finam
description: 使用 Finam Trade API 执行交易、管理投资组合、访问实时市场数据、浏览市场资产以及分析资产波动性。
metadata: '{"openclaw": {"emoji": "📈", "homepage": "https://tradeapi.finam.ru/", "requires": {"bins": ["curl", "jq", "python3"], "env": ["FINAM_API_KEY", "FINAM_ACCOUNT_ID"]}, "primaryEnv": "FINAM_API_KEY"}}'
---
# Finam Trade API 技能

## 设置

在使用 API 之前，请获取并存储 JWT 令牌（`$FINAM_API_KEY` 和 `$FINAM_ACCOUNT_ID` 已经设置）：

```shell
export FINAM_JWT_TOKEN=$(curl -sL "https://api.finam.ru/v1/sessions" \
--header "Content-Type: application/json" \
--data '{"secret": "'"$FINAM_API_KEY"'"}' | jq -r '.token')
```

**注意：** 令牌在 15 分钟后失效。如果收到认证错误，请重新运行此命令。

## 市场资产

### 列出可用的交易所和股票

**符号格式：** 所有符号必须采用 `ticker@mic` 格式（例如，`SBER@MISX`）
**基础 MIC 代码：**
- `MISX` - 莫斯科交易所
- `RUSX` - RTS
- `XNGS` - NASDAQ/NGS
- `XNMS` - NASDAQ/NNS
- `XNYS` - 纽约证券交易所

查看所有支持的交易所及其 MIC 代码：

```shell
jq -r '.exchanges[] | "\(.mic) - \(.name)"' assets/exchanges.json
```

列出特定交易所上的股票：

```shell
MIC="MISX"
LIMIT=20
jq -r ".$MIC[:$LIMIT] | .[] | \"\(.symbol) - \(.name)\"" assets/equities.json
```

### 按名称搜索资产

在所有交易所中按名称（不区分大小写）查找股票：

```shell
QUERY="apple"
jq -r --arg q "$QUERY" 'to_entries[] | .value[] | select(.name | ascii_downcase | contains($q)) | "\(.symbol) - \(.name)"' assets/equities.json
```

### 按成交量排名前 N 名的股票

按交易量降序排列，列出每个市场中最活跃的 100 只股票：

```shell
N=10
jq -r ".[:$N] | .[] | \"\(.ticker) - \(.name)\"" assets/top_ru_equities.json
```

```shell
N=10
jq -r ".[:$N] | .[] | \"\(.ticker) - \(.name)\"" assets/top_us_equities.json
```

## 账户管理

### 获取账户投资组合

检索投资组合信息，包括持仓、余额和损益：

```shell
curl -sL "https://api.finam.ru/v1/accounts/$FINAM_ACCOUNT_ID" \
  --header "Authorization: $FINAM_JWT_TOKEN" | jq
```

## 市场数据

### 获取最新报价

获取当前的买卖价格和最新交易记录：

```shell
SYMBOL="SBER@MISX"
curl -sL "https://api.finam.ru/v1/instruments/$SYMBOL/quotes/latest" \
  --header "Authorization: $FINAM_JWT_TOKEN" | jq
```

### 获取订单簿（深度）

查看当前的订单簿（包括买卖价格）：

```shell
SYMBOL="SBER@MISX"
curl -sL "https://api.finam.ru/v1/instruments/$SYMBOL/orderbook" \
  --header "Authorization: $FINAM_JWT_TOKEN" | jq
```

### 获取最近的交易记录

列出最近执行的交易记录：

```shell
SYMBOL="SBER@MISX"
curl -sL "https://api.finam.ru/v1/instruments/$SYMBOL/trades/latest" \
  --header "Authorization: $FINAM_JWT_TOKEN" | jq
```

### 获取历史价格数据（OHLCV）

根据指定的时间范围获取历史价格数据：

```shell
SYMBOL="SBER@MISX"
TIMEFRAME="TIME_FRAME_D"
START_TIME="2024-01-01T00:00:00Z"
END_TIME="2024-04-01T00:00:00Z"
curl -sL "https://api.finam.ru/v1/instruments/$SYMBOL/bars?timeframe=$TIMEFRAME&interval.startTime=$START_TIME&interval.endTime=$END_TIME" \
  --header "Authorization: $FINAM_JWT_TOKEN" | jq
```

**可用的时间范围：**
- `TIME_FRAME_M1`、`M5`、`M15`、`M30` - 分钟（1、5、15、30）
- `TIME_FRAME_H1`、`H2`、`H4`、`H8` - 小时（1、2、4、8）
- `TIME_FRAME_D` - 日
- `TIME_FRAME_W` - 周
- `TIME_FRAME_MN` - 月
- `TIME_FRAME_QR` - 季度

**日期格式（RFC 3339）：**
- 格式：`YYYY-MM-DDTHH:MM:SSZ` 或 `YYYY-MM-DDTHH:MM:SS+HH:MM`
- `startTime` - 包含在结果中（时间范围的开始时间）
- `endTime` - 不包含在结果中（时间范围的结束时间）
- 例如：
  - `2024-01-15T10:30:00Z`（UTC）
  - `2024-01-15T10:30:00+03:00`（莫斯科时间，UTC+3）

## 新闻

### 获取最新市场新闻

获取并显示最新的新闻标题。无需 JWT 令牌。

俄罗斯市场新闻
```shell
curl -sL "https://www.finam.ru/analysis/conews/rsspoint/" | python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.stdin).getroot()
for item in reversed(root.findall('.//item')):
    print(f'* {item.findtext('title','')}. {item.findtext('description','').split('...')[0]}')
"
```

美国市场新闻
```shell
curl -sL "https://www.finam.ru/international/advanced/rsspoint/" | python3 -c "
import sys, xml.etree.ElementTree as ET
root = ET.parse(sys.stdin).getroot()
for item in reversed(root.findall('.//item')):
    print(f'* {item.findtext('title','')}. {item.findtext('description','').split('...')[0]}')
"
```

**参数：**
- 将 `[:10]` 更改为任意数字，以控制显示的新闻标题数量

## 订单管理

> **重要提示：** 在下达或取消任何订单之前，必须明确确认用户的详细信息并获得他们的批准。请说明完整的订单参数（符号、方向、数量、类型、价格），并在执行前等待确认。

### 下单

**订单类型：**
- `ORDER_TYPEMARKET` - 市场订单（立即执行，无需 `limitPrice`）
- `ORDER_TYPE_LIMIT` - 限价订单（需要 `limitPrice`）

```shell
curl -sL "https://api.finam.ru/v1/accounts/$FINAM_ACCOUNT_ID/orders" \
  --header "Authorization: $FINAM_JWT_TOKEN" \
  --header "Content-Type: application/json" \
  --data "$(jq -n \
    --arg symbol   "SBER@MISX" \
    --arg quantity "10" \
    --arg side     "SIDE_BUY" \
    --arg type     "ORDER_TYPE_LIMIT" \
    --arg price    "310.50" \
    '{symbol: $symbol, quantity: {value: $quantity}, side: $side, type: $type, limitPrice: {value: $price}}')" \
  | jq
```

**参数：**
- `symbol` - 交易工具（例如，`SBER@MISX`）
- `quantity.value` - 股票/合约数量
- `side` - `SIDE_BUY` 或 `SIDE_SELL`
- `type` - `ORDER_TYPEMARKET` 或 `ORDER_TYPE_LIMIT`
- `limitPrice` - 仅适用于 `ORDER_TYPE_LIMIT`（市场订单可省略）

### 获取订单状态

检查特定订单的状态：

```shell
ORDER_ID="12345678"
curl -sL "https://api.finam.ru/v1/accounts/$FINAM_ACCOUNT_ID/orders/$ORDER_ID" \
  --header "Authorization: $FINAM_JWT_TOKEN" | jq
```

### 取消订单

取消待处理的订单：

```shell
ORDER_ID="12345678"
curl -sL --request DELETE "https://api.finam.ru/v1/accounts/$FINAM_ACCOUNT_ID/orders/$ORDER_ID" \
  --header "Authorization: $FINAM_JWT_TOKEN" | jq
```

## 脚本

### 波动性扫描器

扫描给定市场中波动性最高的 100 只股票，并根据过去 60 天的年化历史波动性（收盘价与开盘价之差）打印出这些股票。

**用法：**
```shell
python3 scripts/volatility.py [ru|us] [N]
```

**参数：**
- `ru` / `us` — 扫描的市场（默认：`ru`）
- `N` — 显示的结果数量（默认：`10`）

**示例：**
```shell
# Top 10 most volatile Russian stocks
python3 scripts/volatility.py ru 10

# Top 5 most volatile US stocks
python3 scripts/volatility.py us 5
```