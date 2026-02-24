---
name: 0xarchive
version: 1.1.0
description: 从 0xArchive 查询 Hyperliquid、Lighter.xyz 和 HIP-3 的历史加密货币市场数据。这些数据包括订单簿、交易记录、K线图、资金费率、未平仓合约数量以及数据质量信息。当用户询问有关 Hyperliquid、Lighter.xyz 或 HIP-3 的加密货币市场数据、订单簿、交易记录、资金费率或历史价格时，可以使用此功能。
allowed-tools: Bash
argument-hint: "query, e.g. 'BTC funding rate' or 'ETH 4h candles last week'"
metadata: {"openclaw":{"requires":{"env":["OXARCHIVE_API_KEY"]},"primaryEnv":"OXARCHIVE_API_KEY"}}
---
# 0xArchive API 技能

使用 `curl` 从 **0xArchive** 查询历史和实时的加密货币市场数据。支持三种交易所：**Hyperliquid**（Perps DEX）、**Lighter.xyz**（订单簿 DEX）和 **HIP-3**（Hyperliquid builder）。数据类型包括订单簿、交易记录、K线图、资金费率、未平仓合约数量（OI）、清算事件以及数据质量指标。

## 认证

所有 API 端点都需要 `x-api-key` 头部字段。该密钥从 `$OXARCHIVE_API_KEY` 变量中获取。

```bash
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" "https://api.0xarchive.io/v1/..."
```

## 交易所与货币命名规则

| 交易所 | 路径前缀 | 货币格式 | 示例 |
|----------|-------------|-------------|---------|
| Hyperliquid | `/v1/hyperliquid` | 大写形式 | `BTC`, `ETH`, `SOL` |
| HIP-3 | `/v1/hyperliquid/hip3` | 区分大小写，格式为 `prefix:NAME` | `km:US500`, `xyz:XYZ100` |
| Lighter | `/v1/lighter` | 大写形式 | `BTC`, `ETH` |

Hyperliquid 和 Lighter 会在服务器端将货币符号自动转换为大写形式；HIP-3 的货币名称则保持原样。

## 时间戳

所有时间戳均以 **Unix 毫秒** 为单位。可以使用以下 shell 常量进行转换：

```bash
NOW=$(( $(date +%s) * 1000 ))
HOUR_AGO=$(( NOW - 3600000 ))
DAY_AGO=$(( NOW - 86400000 ))
WEEK_AGO=$(( NOW - 604800000 ))
```

## 响应格式

所有响应数据的结构如下：

```json
{
  "success": true,
  "data": [ ... ],
  "meta": {
    "count": 100,
    "request_id": "uuid",
    "next_cursor": "1706000000000"   // 当存在更多数据页时显示
  }
}
```

## API 端点参考

### Hyperliquid (`/v1/hyperliquid`)

| 端点 | 参数 | 说明 |
|----------|--------|-------|
| `GET /instruments` | -- | 列出所有可交易的货币 |
| `GET /instruments/{symbol}` | -- | 单个货币的详细信息 |
| `GET /orderbook/{symbol}` | `timestamp`, `depth` | 最新数据或指定时间戳的数据 |
| `GET /orderbook/{symbol}/history` | `start`, `end`, `limit`, `cursor`, `depth` | 历史数据快照 |
| `GET /trades/{symbol}` | `start`, `end`, `limit`, `cursor` | 交易记录 |
| `GET /candles/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | K线图数据（OHLCV） |
| `GET /funding/{symbol}/current` | -- | 当前资金费率 |
| `GET /funding/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | 资金费率历史数据 |
| `GET /openinterest/{symbol}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | 未平仓合约历史数据 |
| `GET /liquidations/{symbol}` | `start`, `end`, `limit`, `cursor` | 清算事件 |
| `GET /liquidations/{symbol}/volume` | `start`, `end`, `limit`, `cursor`, `interval` | 清算量（美元） |
| `GET /liquidations/user/{address}` | `start`, `end`, `limit`, `cursor`, `coin` | 指定用户的清算记录 |
| `GET /freshness/{symbol}` | -- | 数据的新鲜度 |
| `GET /summary/{symbol}` | -- | 综合市场概览（价格、资金费率、未平仓合约数量、交易量） |
| `GET /prices/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | 价格历史数据 |

### HIP-3 (`/v1/hyperliquid/hip3`)

货币名称区分大小写（例如 `km:US500`）。该交易所没有提供清算相关的 API 端点。查询订单簿数据需要 Pro+ 订阅等级。

| 端点 | 参数 | 说明 |
|----------|--------|-------|
| `GET /instruments` | -- | 列出所有可交易的 HIP-3 货币 |
| `GET /instruments/{coin}` | -- | 单个货币的详细信息 |
| `GET /orderbook/{coin}` | `timestamp`, `depth` | 需要 Pro+ 订阅等级 |
| `GET /orderbook/{coin}/history` | `start`, `end`, `limit`, `cursor`, `depth` | 历史数据快照 |
| `GET /trades/{coin}` | `start`, `end`, `limit`, `cursor` | 交易记录 |
| `GET /trades/{coin}/recent` | `limit` | 最近的交易记录（无需指定时间范围） |
| `GET /candles/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | K线图数据（OHLCV） |
| `GET /funding/{coin}/current` | -- | 当前资金费率 |
| `GET /funding/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | 资金费率历史数据 |
| `GET /openinterest/{coin}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | 未平仓合约历史数据 |
| `GET /freshness/{coin}` | -- | 数据的新鲜度 |
| `GET /summary/{coin}` | -- | 综合市场概览（价格、资金费率） |
| `GET /prices/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | 价格历史数据 |

### Lighter (`/v1/lighter`)

数据类型与 Hyperliquid 相同，但 Lighter 不提供清算相关的 API 端点。订单簿历史数据的显示粒度可设置：

| 端点 | 参数 | 说明 |
|----------|--------|-------|
| `GET /instruments` | -- | 列出所有可交易的 Lighter 货币 |
| `GET /instruments/{symbol}` | -- | 单个货币的详细信息 |
| `GET /orderbook/{symbol}` | `timestamp`, `depth` | 最新数据或指定时间戳的数据 |
| `GET /orderbook/{symbol}/history` | `start`, `end`, `limit`, `cursor`, `granularity` | 数据显示粒度（默认为 `checkpoint`） |
| `GET /trades/{symbol}` | `start`, `end`, `limit`, `cursor` | 交易记录 |
| `GET /trades/{symbol}/recent` | `limit` | 最近的交易记录（无需指定时间范围） |
| `GET /candles/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | K线图数据（OHLCV） |
| `GET /funding/{symbol}/current` | -- | 当前资金费率 |
| `GET /funding/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | 资金费率历史数据 |
| `GET /openinterest/{symbol}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | 未平仓合约历史数据 |
| `GET /freshness/{symbol}` | -- | 数据的新鲜度 |
| `GET /summary/{symbol}` | -- | 综合市场概览（价格、资金费率） |
| `GET /prices/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | 价格历史数据 |

### 数据质量 (`/v1/data-quality`)

| 端点 | 参数 | 说明 |
|----------|--------|-------|
| `GET /status` | -- | 系统健康状态 |
| `GET /coverage` | -- | 所有交易所的数据覆盖情况 |
| `GET /coverage/{exchange}` | -- | 单个交易所的数据覆盖情况 |
| `GET /coverage/{exchange}/{symbol}` | `from`, `to` | 指定时间范围内的数据覆盖情况 |
| `GET /incidents` | `status`, `exchange`, `since`, `limit`, `offset` | 事件列表 |
| `GET /incidents/{id}` | -- | 单个事件详情 |
| `GET /latency` | -- | 数据传输延迟指标 |
| `GET /sla` | `year`, `month` | 服务水平协议（SLA）合规报告 |

## 常用参数

| 参数 | 类型 | 说明 |
|-------|------|-------------|
| `start` | int | 开始时间戳（Unix 毫秒），默认为 24 小时前 |
| `end` | int | 结束时间戳（Unix 毫秒），默认为当前时间 |
| `limit` | int | 最大记录数量，默认为 100 条，K线图数据最多 1000 条 |
| `cursor` | string | 分页游标（来自 `meta.next_cursor`） |
| `interval` | string | K线图的时间间隔（`1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`；OI/资金费率数据为 `5m`, `15m`, `30m`, `1h`, `4h`, `1d`；原始数据可省略） |
| `depth` | int | 订单簿的深度（每侧的价格层次数） |
| `granularity` | string | Lighter 订单簿的显示粒度（`checkpoint`, `30s`, `10s`, `1s`, `tick`）

## 默认值

如果用户未指定时间范围，系统将使用 **过去 24 小时** 的数据：

```bash
NOW=$(( $(date +%s) * 1000 ))
DAY_AGO=$(( NOW - 86400000 ))
```

对于 K线图数据，如果没有指定时间范围，系统会自动选择合适的范围（例如：4 小时 K线图使用过去 7 天的数据）。

## 分页

如果响应中包含 `meta.next_cursor`，则表示还有更多数据。可以通过添加 `&cursor=VALUE` 参数来获取下一页数据：

```bash
# 获取第一页数据
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/trades/BTC?start=$START&end=$END&limit=1000"

# 获取下一页数据（使用上一次响应中的 `next_cursor`）
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/trades/BTC?start=$START&end=$END&limit=1000&cursor=1706000000000_12345"
```

## 订阅等级限制

| 订阅等级 | 费用 | 支持的货币 | 订单簿深度 | Lighter 数据显示粒度 | 历史数据深度 | 数据请求速率限制 |
|------|-------|-------|-----------------|---------------------|------------------|------------|
| 免费 | $0 | 仅支持 BTC（HIP-3 仅支持 km:US500） | 20 个价格层次 | -- | 30 天 | 15 每秒请求次数（RPS） |
| 建议级 | $49/月 | 所有货币 | 50 个价格层次 | `checkpoint`, `30s`, `10s` | 1 年 | 50 每秒请求次数（RPS） |
| 专业级 | $199/月 | 所有货币 | 100 个价格层次 | `1s` | 全部历史数据 | 150 每秒请求次数（RPS） |
| 企业级 | 自定义 | 全部货币 | 全部数据深度 | `tick` | 全部历史数据 | 自定义 |

## 错误处理

| HTTP 状态码 | 含义 | 处理方式 |
|-------------|---------|--------|
| 400 | 请求错误/验证失败 | 检查参数（缺少开始/结束时间、时间间隔无效） |
| 401 | API 密钥缺失或无效 | 设置 `$OXARCHIVE_API_KEY` |
| 403 | 订阅等级限制 | 升级订阅等级（例如：免费等级无法查询非 BTC 货币） |
| 404 | 货币名称不存在 | 检查货币名称的拼写和交易所信息 |
| 429 | 数据请求频率受限 | 等待片刻后重试 |

错误响应会返回 `{ "code": 400, "error": "description" }`。

## 示例查询

```bash
# 列出 Hyperliquid 的所有货币
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/instruments" | jq '.data | length'

# 获取 BTC 的订单簿数据（前 10 个价格层次）
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/orderbook/BTC?depth=10" | jq '.data'

# 获取过去 1 小时的 ETH 交易记录
NOW=$(( $(date +%s) * 1000)); HOUR_AGO=$(( NOW - 3600000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/trades/ETH?start=$HOUR_AGO&end=$NOW&limit=100" | jq '.data'

# 获取过去一周的 SOL 4 小时 K线图数据
NOW=$(( $(date +%s) * 1000)); WEEK_AGO=$(( NOW - 604800000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/candles/SOL?start=$WEEK_AGO&end=$NOW&interval=4h" | jq '.data'

# 获取当前的 BTC 资金费率
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

# 获取过去 24 小时内 HIP-3 km:US500 的 K线图数据（1 小时间隔）
NOW=$(( $(date +%s) * 1000)); DAY_AGO=$(( NOW - 86400000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/hip3/candles/km:US500?start=$DAY_AGO&end=$NOW&interval=1h" | jq '.data'

# 获取 Lighter 的 BTC 订单簿数据（30 秒显示粒度，过去 1 小时的数据）
NOW=$(( $(date +%s) * 1000)); HOUR_AGO=$(( NOW - 3600000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/lighter/orderbook/BTC/history?start=$HOUR_AGO&end=$NOW&granularity=30s&limit=100" | jq '.data'

# 获取系统健康状态
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/status" | jq '.' |

# 获取当前月的 SLA 报告
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/sla" | jq '.' |

# 获取 BTC 的综合市场概览（价格、资金费率、未平仓合约数量、交易量）
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/summary/BTC" | jq '.data'

# 获取 BTC 数据的新鲜度
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/freshness/BTC" | jq '.data'

# 获取 BTC 的价格历史数据（Mark/Oracle/Mid 价格）
NOW=$(( $(date +%s) * 1000)); DAY_AGO=$(( NOW - 86400000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/prices/BTC?start=$DAY_AGO&end=$NOW&interval=1h" | jq '.data'

# 获取 BTC 的清算量（按 4 小时区间聚合）
NOW=$(( $(date +%s) * 1000)); WEEK_AGO=$(( NOW - 604800000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/liquidations/BTC/volume?start=$WEEK_AGO&end=$NOW&interval=4h" | jq '.data'

# 获取 Hyperliquid 的 BTC 数据覆盖情况
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/coverage/hyperliquid/BTC" | jq '.' |
```