---
name: 0xarchive
version: 1.3.0
description: 从 0xArchive 中查询 Hyperliquid、Lighter.xyz 和 HIP-3 的历史加密货币市场数据。这些数据包括订单簿、交易记录、K线图、资金费率、未平仓合约数量以及数据质量信息。当用户询问有关 Hyperliquid、Lighter.xyz 或 HIP-3 的加密货币市场数据、订单簿、交易记录、资金费率或历史价格时，可以使用此功能。
allowed-tools: Bash
argument-hint: "query, e.g. 'BTC funding rate' or 'ETH 4h candles last week'"
metadata: {"openclaw":{"requires":{"env":["OXARCHIVE_API_KEY"]},"primaryEnv":"OXARCHIVE_API_KEY"}}
---
# 0xArchive API 技能

使用 `curl` 从 **0xArchive** 查询历史和实时的加密货币市场数据。支持三种交易所：**Hyperliquid**（Perps DEX）、**Lighter.xyz**（订单簿 DEX）和 **HIP-3**（Hyperliquid builder Perps）。数据类型包括订单簿、交易记录、K线图、资金费率、未平仓合约数量（OI）以及数据质量指标。

## 认证

所有接口都需要 `x-api-key` 头部字段。该密钥可以从 `$OXARCHIVE_API_KEY` 变量中获取。

```bash
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" "https://api.0xarchive.io/v1/..."
```

## 交易所与币种命名

| 交易所 | 路径前缀 | 币种格式 | 示例 |
|--------|---------|-------------|---------|
| Hyperliquid | /v1/hyperliquid | 大写形式 | `BTC`, `ETH`, `SOL` |
| HIP-3 | /v1/hyperliquid/hip3 | 区分大小写，格式为 `prefix:NAME` | `km:US500`, `xyz:XYZ100` |
| Lighter | /v1/lighter | 大写形式 | `BTC`, `ETH` |

Hyperliquid 和 Lighter 会在服务器端将币种名称自动转换为大写。HIP-3 的币种名称则按原样传递。

## 时间戳

所有时间戳均为 **Unix 毫秒**。可以使用以下 Shell 脚本辅助函数进行转换：

```bash
NOW=$(( $(date +%s) * 1000 ))
HOUR_AGO=$(( NOW - 3600000 ))
DAY_AGO=$(( NOW - 86400000 ))
WEEK_AGO=$(( NOW - 604800000 ))
```

## 响应格式

所有响应都遵循以下结构：

```json
{
  "success": true,
  "data": [ ... ],
  "meta": {
    "count": 100,
    "request_id": "uuid",
    "next_cursor": "1706000000000"   // 当存在更多页面时显示
  }
}
```

## 接口参考

### Hyperliquid (`/v1/hyperliquid`)

| 接口 | 参数 | 说明 |
|--------|--------|-------|
| `GET /instruments` | -- | 列出所有币种 |
| `GET /instruments/{symbol}` | -- | 单个币种详情 |
| `GET /orderbook/{symbol}` | `timestamp`, `depth` | 最新数据或指定时间戳的数据 |
| `GET /orderbook/{symbol}/history` | `start`, `end`, `limit`, `cursor`, `depth` | 历史数据快照 |
| `GET /trades/{symbol}` | `start`, `end`, `limit`, `cursor` | 交易记录 |
| `GET /candles/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | OHLCV K线图 |
| `GET /funding/{symbol}/current` | -- | 当前资金费率 |
| `GET /funding/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | 资金费率历史数据 |
| `GET /openinterest/{symbol}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | OI 历史数据 |
| `GET /liquidations/{symbol}` | `start`, `end`, `limit`, `cursor` | 清仓事件 |
| `GET /liquidations/{symbol}/volume` | `start`, `end`, `limit`, `cursor`, `interval` | 清仓量（美元） |
| `GET /liquidations/user/{address}` | `start`, `end`, `limit`, `cursor`, `coin` | 某用户的清仓记录 |
| `GET /freshness/{symbol}` | -- | 各数据类型的数据更新频率 |
| `GET /summary/{symbol}` | -- | 综合市场概览（价格、资金费率、OI、成交量、清仓量） |
| `GET /prices/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | Mark/Oracle/中间价历史数据 |

### HIP-3 (`/v1/hyperliquid/hip3`)

币种名称区分大小写（例如：`km:US500`）。该接口不提供清仓相关功能，且需要 Pro+ 订阅层级才能访问订单簿数据。

| 接口 | 参数 | 说明 |
|--------|--------|-------|
| `GET /instruments` | -- | 列出 HIP-3 的所有币种 |
| `GET /instruments/{coin}` | -- | 单个币种详情 |
| `GET /orderbook/{coin}` | `timestamp`, `depth` | 需要 Pro+ 订阅层级 |
| `GET /orderbook/{coin}/history` | `start`, `end`, `limit`, `cursor`, `depth` | 需要 Pro+ 订阅层级 |
| `GET /trades/{coin}` | `start`, `end`, `limit`, `cursor` | 交易记录 |
| `GET /trades/{coin}/recent` | `limit` | 最新交易记录（无需指定时间范围） |
| `GET /candles/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | OHLCV K线图 |
| `GET /funding/{coin}/current` | -- | 当前资金费率 |
| `GET /funding/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | 资金费率历史数据 |
| `GET /openinterest/{coin}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | OI 历史数据 |
| `GET /freshness/{coin}` | -- | 各数据类型的数据更新频率 |
| `GET /summary/{coin}` | -- | 综合市场概览（价格、资金费率、OI） |
| `GET /prices/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | Mark/Oracle/中间价历史数据 |

### Lighter (`/v1/lighter`)

数据类型与 Hyperliquid 相同，但无清仓相关功能。订单簿历史数据提供更高的粒度选项（`granularity`）。

| 接口 | 参数 | 说明 |
|--------|--------|-------|
| `GET /instruments` | -- | 列出 Lighter 的所有币种 |
| `GET /instruments/{symbol}` | -- | 单个币种详情 |
| `GET /orderbook/{symbol}` | `timestamp`, `depth` | 最新数据或指定时间戳的数据 |
| `GET /orderbook/{symbol}/history` | `start`, `end`, `limit`, `cursor`, `granularity` | 默认粒度为 `checkpoint` |
| `GET /trades/{symbol}` | `start`, `end`, `limit`, `cursor` | 交易记录 |
| `GET /trades/{symbol}/recent` | `limit` | 最新交易记录（无需指定时间范围） |
| `GET /candles/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | OHLCV K线图 |
| `GET /funding/{symbol}/current` | -- | 当前资金费率 |
| `GET /funding/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | 资金费率历史数据 |
| `GET /openinterest/{symbol}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | OI 历史数据 |
| `GET /freshness/{symbol}` | -- | 各数据类型的数据更新频率 |
| `GET /summary/{symbol}` | -- | 综合市场概览（价格、资金费率、OI） |
| `GET /prices/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | Mark/Oracle 价格历史数据 |

### 数据质量 (`/v1/data-quality`)

| 接口 | 参数 | 说明 |
|--------|--------|-------|
| `GET /status` | -- | 系统健康状态 |
| `GET /coverage` | -- | 所有交易所的覆盖情况 |
| `GET /coverage/{exchange}` | -- | 单个交易所的覆盖情况 |
| `GET /coverage/{exchange}/{symbol}` | `from`, `to` | 指定币种的覆盖范围及缺失数据 |
| `GET /incidents` | `status`, `exchange`, `since`, `limit`, `offset` | 事件列表 |
| `GET /incidents/{id}` | -- | 单个事件详情 |
| `GET /latency` | -- | 数据传输延迟指标 |
| `GET /sla` | `year`, `month` | SLA 合规性报告 |

### Web3 认证 (`/v1`)

可以使用以太坊钱包（SIWE）程序化获取 API 密钥。这些接口无需 API 密钥。

| 接口 | 参数 | 说明 |
|--------|--------|-------|
| `POST /auth/web3/challenge` | `address`（钱包地址） | 返回用于签名的 SIWE 消息 |
| `POST /web3/signup` | `message`, `signature` | 返回免费层级的 API 密钥 |
| `POST /web3/keys` | `message`, `signature` | 列出钱包的所有密钥 |
| `POST /web3/keys/revoke` | `message`, `signature`, `key_id` | 注销密钥 |
| `POST /web3/subscribe` | `tier`（`build` 或 `pro`）、`payment-signature` 头部字段 | x402 标准的 USDC 订阅服务 |

**免费层级流程：**  
调用 `/auth/web3/challenge` 并提供钱包地址 → 使用 `personal_sign`（EIP-191）签名返回的消息 → 将签名和消息一起发送到 `/web3/signup` 获取 API 密钥。

**付费层级流程（x402 标准）：**  
1. 发送 `POST /web3/subscribe` 并指定 `tier="build"` → 服务器返回包含 `payment.amount`（微 USDC）、`payment.pay_to`（钱包地址）和 `payment.network` 的响应。  
2. 使用 EIP-712 的 `TransferWithAuthorization` 消息进行转账：  
   - 示例消息：  
     ```json
     {
       "domain": "USD Coin",
       "version": "2",
       "chainId": 8453,
       "verifyingContract": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
       "type": "TransferWithAuthorization",
       "address_from": "<wallet>",
       "address_to": "<pay_to>",
       "value": "<amount>",
       "validAfter": "0",
       "validBefore": "<now+3600>",
       "nonce": "<32 random bytes>"
     }
     ```
   ```
3. 将 JSON 数据进行 Base64 编码，然后再次发送 `POST /web3/subscribe` 并添加 `payment-signature` 头部字段以获取 API 密钥。

**重要提示：**  
所有 `authorization` 参数（`value`, `validAfter`, `validBefore`）必须为字符串格式。具体实现可参考 `scripts/web3.subscribe.py` 文件。

## 常用参数

| 参数 | 类型 | 说明 |
|-------|------|-------------|
| `start` | int | 开始时间戳（Unix 毫秒），默认为 24 小时前 |
| `end` | int | 结束时间戳（Unix 毫秒），默认为当前时间 |
| `limit` | int | 最大记录数量，默认为 100 条（K线图为 1000 条） |
| `cursor` | string | 分页游标，来自 `meta.next_cursor` |
| `interval` | string | K线图间隔：`1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`；OI/资金费率数据为 `5m`, `15m`, `30m`, `1h`, `4h`, `1d`；原始数据可忽略 |
| `depth` | int | 订单簿深度（每侧的价格层次数） |
| `granularity` | string | Lighter 订单簿的显示粒度：`checkpoint`（默认）、`30s`, `10s`, `1s`, `tick` |

## 默认值

如果用户未指定时间范围，系统将使用 **过去 24 小时** 的数据：

```bash
NOW=$(( $(date +%s) * 1000 ))
DAY_AGO=$(( NOW - 86400000 ))
```

对于 K线图，如果没有指定时间范围，系统会自动选择合适的范围（例如：4 小时的 K线图显示过去 7 天的数据）。

## 分页

如果响应中包含 `meta.next_cursor`，则表示还有更多数据可用。可以通过添加 `&cursor=VALUE` 参数来获取下一页：

```bash
# 第一页
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/trades/BTC?start=$START&end=$END&limit=1000"

# 下一页（使用上一次响应的 `next_cursor`）
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/trades/BTC?start=$START&end=$END&limit=1000&cursor=1706000000000_12345"
```

## 订阅层级限制

| 订阅层级 | 费用 | 支持的币种 | 订单簿深度 | Lighter 数据粒度 | 历史数据深度 | 数据请求速率限制 |
|--------|-------|-----------------|-----------------|------------------|------------|
| 免费 | $0 | 仅支持 BTC（HIP-3 仅支持 km:US500） | 20 层 | -- | 30 天 | 15 每秒请求 |
| Build | $49/月 | 所有币种 | 50 层 | `checkpoint`, 30s, 10s | 1 年 | 50 每秒请求 |
| Pro | $199/月 | 所有币种 | 100 层 | `1 秒` | 全部历史数据 | 150 每秒请求 |
| Enterprise | 自定义 | 全部数据 | 全部深度 | `1 秒` | 全部历史数据 | 自定义 |

## 错误处理

| HTTP 状态码 | 含义 | 处理方式 |
|---------|---------|--------|
| 400 | 请求错误/验证失败 | 检查参数（缺少开始/结束时间或间隔设置无效） |
| 401 | API 密钥缺失或无效 | 设置 `$OXARCHIVE_API_KEY` |
| 403 | 订阅层级限制 | 升级订阅计划（例如：免费层级不允许查询非 BTC 币种） |
| 404 | 未找到指定的币种 | 检查币种名称和交易所名称 |
| 429 | 数据请求受限 | 请稍后再试 |

错误响应会返回 `{ "code": 400, "error": "description" }`。

## 示例查询

```bash
# 列出 Hyperliquid 的所有币种
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/instruments" | jq '.data | length'

# 获取 BTC 的订单簿数据（前 10 层）
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/orderbook/BTC?depth=10" | jq '.data'

# 获取过去 1 小时的 ETH 交易记录
NOW=$(( $(date +%s) * 1000)); HOUR_AGO=$(( NOW - 3600000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/trades/ETH?start=$HOUR_AGO&end=$NOW&limit=100" | jq '.data'

# 获取过去一周的 SOL 4 小时 K线图
NOW=$(( $(date +%s) * 1000)); WEEK_AGO=$(( NOW - 604800000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/candles/SOL?start=$WEEK_AGO&end=$NOW&interval=4h" | jq '.data'

# 获取 BTC 的当前资金费率
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/funding/BTC/current" | jq '.data'

# 获取过去一周的 BTC 未平仓合约数量（按 1 小时间隔聚合）
NOW=$(( $(date +%s) * 1000)); WEEK_AGO=$(( NOW - 604800000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/openinterest/BTC?start=$WEEK_AGO&end=$NOW&interval=1h" | jq '.data'

# 获取过去 30 天的 ETH 资金费率（按 4 小时间隔聚合）
NOW=$(( $(date +%s) * 1000)); MONTH_AGO=$(( NOW - 2592000000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/funding/ETH?start=$MONTH_AGO&end=$NOW&interval=4h" | jq '.data'

# 获取过去 24 小时的 HIP-3 km:US500 K线图（1 小时间隔）
NOW=$(( $(date +%s) * 1000)); DAY_AGO=$(( NOW - 86400000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/hip3/candles/km:US500?start=$DAY_AGO&end=$NOW&interval=1h" | jq '.data'

# 获取 Lighter 的 BTC 订单簿历史数据（30 秒粒度，过去 1 小时）
NOW=$(( $(date +%s) * 1000)); HOUR_AGO=$(( NOW - 3600000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/lighter/orderbook/BTC/history?start=$HOUR_AGO&end=$NOW&granularity=30s&limit=100" | jq '.data'

# 获取系统健康状态
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/status" | jq '.'

# 获取当前月份的 SLA 报告
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/sla" | jq '.'

# 获取 BTC 的综合市场信息（价格、资金费率、OI、成交量、清仓量）
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/summary/BTC" | jq '.data'

# 获取 BTC 数据的更新频率
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/freshness/BTC" | jq '.data'

# 获取 BTC 的价格历史数据（Mark/Oracle 价格，按 1 小时间隔聚合）
NOW=$(( $(date +%s) * 1000)); DAY_AGO=$(( NOW - 86400000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/prices/BTC?start=$DAY_AGO&end=$NOW&interval=1h" | jq '.data'

# 获取 BTC 的清仓量（按 4 小时区间聚合）
NOW=$(( $(date +%s) * 1000)); WEEK_AGO=$(( NOW - 604800000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/liquidations/BTC/volume?start=$WEEK_AGO&end=$NOW&interval=4h" | jq '.data'

# 获取 Hyperliquid 中 BTC 的数据覆盖情况
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/coverage/hyperliquid/BTC" | jq '.'
```