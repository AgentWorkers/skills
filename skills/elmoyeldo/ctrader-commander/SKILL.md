---
name: ctrader-commander
description: Place and manage cTrader orders (market, limit, stop), check open positions, fetch live quotes and OHLC candles, and query account balance and equity via a local HTTP proxy. No credentials or token required at call time.
homepage: https://github.com/LogicalSapien/ctrader-openapi-proxy
metadata: {"openclaw": {"emoji": "\ud83d\udcc8", "requires": {"bins": ["curl"]}, "homepage": "https://github.com/LogicalSapien/ctrader-openapi-proxy"}}
---

# cTrader Commander

该工具用于帮助用户执行以下操作：下订单、查看持仓或账户余额、获取实时价格、获取K线数据以及管理cTrader账户中的订单。

所有请求都会发送到 `http://localhost:9009`；用户名和密码存储在服务器的 `.env` 文件中，不会在请求过程中传递给客户端。

> **代理仓库：** https://github.com/LogicalSapien/ctrader-openapi-proxy  
> 克隆该仓库，将您的 `.env` 文件添加到项目中，然后运行 `make run` 命令启动代理服务，之后才能使用该工具。

完整参考文档：`{baseDir}/endpoints.md`

## 检查代理是否正在运行

```bash
curl -s "http://localhost:9009/get-data?command=ProtoOAVersionReq"
```

如果代理未运行，请执行以下命令启动它：  
`cd ~/ctrader-openapi-proxy && make run`

## 查找符号ID（请先执行此操作）

符号ID是由经纪商指定的，在下订单或获取数据之前请务必先查询相应的符号ID：

```bash
curl -s "http://localhost:9009/get-data?command=ProtoOASymbolsListReq"
```

该函数返回一个包含 `symbolId` 和 `symbolName` 的数组。请记录下您需要操作的金融工具的ID。

## 下市价单

```bash
curl -s -X POST http://localhost:9009/api/market-order \
  -H "Content-Type: application/json" \
  -d '{"symbolId": 158, "orderType": "MARKET", "tradeSide": "BUY", "volume": 1000}'
```

成交量单位说明：  
`1000` 表示 0.01 手；`10000` 表示 0.1 手；`100000` 表示 1 手。  
市价单可设置 `relativeStopLoss`（止损）和 `relativeTakeProfit`（止盈）参数（单位为点）。

## 下限价单或止损单

```bash
curl -s -X POST http://localhost:9009/api/market-order \
  -H "Content-Type: application/json" \
  -d '{"symbolId": 158, "orderType": "LIMIT", "tradeSide": "BUY", "volume": 1000, "price": 0.62500}'
```

`orderType` 可设置为 `MARKET`、`LIMIT` 或 `STOP`；`tradeSide` 可设置为 `BUY` 或 `SELL`。

## 获取OHLC K线数据

```bash
NOW_MS=$(python3 -c "import time; print(int(time.time()*1000))")
FROM_MS=$(python3 -c "import time; print(int(time.time()*1000) - 3600000)")
curl -s -X POST http://localhost:9009/api/trendbars \
  -H "Content-Type: application/json" \
  -d "{\"fromTimestamp\": $FROM_MS, \"toTimestamp\": $NOW_MS, \"period\": \"M5\", \"symbolId\": 158}"
```

可选的时间周期：`M1`、`M2`、`M3`、`M4`、`M5`、`M10`、`M15`、`M30`、`H1`、`H4`、`H12`、`D1`、`W1`、`MN1`。

## 获取实时报价（Tick数据）

```bash
curl -s -X POST http://localhost:9009/api/live-quote \
  -H "Content-Type: application/json" \
  -d '{"symbolId": 158, "quoteType": "BID", "timeDeltaInSeconds": 60}'
```

`quoteType` 可设置为 `BID` 或 `ASK`。

## 查看持仓和待处理订单

```bash
curl -s "http://localhost:9009/get-data?command=ProtoOAReconcileReq"
```

## 平仓

```bash
curl -s "http://localhost:9009/get-data?command=ClosePosition%20123456%201000"
# ClosePosition <positionId> <volumeInUnits>
```

## 取消待处理订单

```bash
curl -s "http://localhost:9009/get-data?command=CancelOrder%20789"
```

## 账户信息（余额、资产、杠杆率）

```bash
curl -s "http://localhost:9009/get-data?command=ProtoOATraderReq"
```

该工具使用本地HTTP代理（`localhost:9009`）来封装cTrader的OpenAPI接口，并将其暴露为REST API。调用该接口时无需传递用户名和密码，这些信息会从服务器的 `.env` 文件中读取。

完整端点参考文档：`{baseDir}/endpoints.md`

## Python使用示例：`{baseDir}/examples.md`

---

## 先决条件

在使用任何功能之前，必须确保代理服务已启动。如果不确定代理是否运行，请执行以下操作：  
```bash
curl -s "http://localhost:9009/get-data?command=ProtoOAVersionReq"
```  
如果返回JSON数据，说明代理已启动；否则请执行以下命令启动代理：  
```bash
cd ~/ctrader-openapi-proxy && make run
```

---

## 重要提示：符号ID由经纪商确定

**在下订单或获取K线/Tick数据之前，请务必先查询相应的符号ID。**  
不同经纪商以及模拟账户和真实账户之间的符号ID可能有所不同。

```bash
curl -s "http://localhost:9009/get-data?command=ProtoOASymbolsListReq"
```

响应结果中包含一个包含 `symbolId` 和 `symbolName` 的数组。请找到您需要操作的金融工具的ID并记录下来。

---

## API端点

### 获取OHLC K线数据
```
POST /api/trendbars
```  
```json
{
  "fromTimestamp": 1700000000000,
  "toTimestamp":   1700086400000,
  "period":        "M5",
  "symbolId":      158
}
```  
可选的时间周期：`M1`、`M2`、`M3`、`M4`、`M5`、`M10`、`M15`、`M30`、`H1`、`H4`、`H12`、`D1`、`W1`、`MN1`  

### 获取实时报价/Tick数据
```
POST /api/live-quote
```  
```json
{
  "symbolId":           158,
  "quoteType":          "BID",
  "timeDeltaInSeconds": 60
}
```  
`quoteType` 可设置为 `"BID"` 或 `"ASK"`。

### 下市价单/限价单/止损单
```
POST /api/market-order
```  
```json
{
  "symbolId":           158,
  "orderType":          "MARKET",
  "tradeSide":          "BUY",
  "volume":             1000,
  "comment":            "my trade",
  "relativeStopLoss":   200,
  "relativeTakeProfit": 350
}
```

`orderType` 的取值：`MARKET`、`LIMIT`、`STOP`  
`tradeSide` 的取值：`BUY`、`SELL`  

对于`LIMIT`和`STOP`订单，需要指定价格（单位为美元）。  
`relativeStopLoss`和`relativeTakeProfit`以点（pips）为单位，仅适用于市价单。  

**成交量单位（非手数）：**  
| `volume` | 手数 | 说明 |
|---|---|---|
| `1000` | 0.01 | 微量手（最小交易单位） |
| `10000` | 0.1 | 小额手 |
| `100000` | 1 | 标准手 |

### 查看持仓和待处理订单
```
GET /get-data?command=ProtoOAReconcileReq
```  
返回一个包含 `position[]` 和 `order[]` 的数组。每个持仓记录包含 `positionId`、`symbolId`、`tradeSide` 和 `volume` 等信息。

### 平仓
```
GET /get-data?command=ClosePosition <positionId> <volumeInUnits>
```  
示例：平仓编号为123456的持仓（交易量为1000单位，即0.01手）：  
```bash
curl -s "http://localhost:9009/get-data?command=ClosePosition%20123456%201000"
```

### 取消待处理订单
```
GET /get-data?command=CancelOrder <orderId>
```  
```bash
curl -s "http://localhost:9009/get-data?command=CancelOrder%20789"
```

### 设置当前账户（可选）  
账户信息会在程序启动时自动从 `.env` 文件中读取。只有在运行时需要切换账户时才需要调用此功能：  
```bash
curl -s -X POST http://localhost:9009/api/set-account
```  
要切换到其他账户，请通过JSON格式传递 `{"accountId": 12345678}`。

### 通用命令转发  
可以通过以下方式调用cTrader的任何API命令：  
```
GET /get-data?command=COMMAND_NAME arg1 arg2
```  
无需使用令牌，用户名和密码会从服务器的 `.env` 文件中读取。

支持的完整命令列表：`{baseDir}/endpoints.md`

---

## 工作流程：首次交易步骤  
1. 查询所需的符号ID：  
   ```bash
   curl -s "http://localhost:9009/get-data?command=ProtoOASymbolsListReq" | python3 -c "
   import sys, json
   data = json.load(sys.stdin)
   [print(s['symbolId'], s['symbolName']) for s in data.get('symbol', []) if 'EURUSD' in s['symbolName']]
   "
   ```  
2. 查看账户信息：  
   ```bash
   curl -s "http://localhost:9009/get-data?command=ProtoOATraderReq"
   ```  
3. 下市价买单：  
   ```bash
   curl -s -X POST http://localhost:9009/api/market-order \
     -H "Content-Type: application/json" \
     -d '{"symbolId": 1, "orderType": "MARKET", "tradeSide": "BUY", "volume": 1000}'
   ```  
4. 查看持仓情况：  
   ```bash
   curl -s "http://localhost:9009/get-data?command=ProtoOAReconcileReq"
   ```