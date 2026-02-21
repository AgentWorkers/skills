---
name: 0xarchive
version: 1.0.0
description: 从 0xArchive 查询 Hyperliquid、Lighter.xyz 和 HIP-3 的历史加密货币市场数据。这些数据包括订单簿、交易记录、K线图、资金费率、未平仓合约数量以及数据质量信息。当用户询问有关 Hyperliquid、Lighter.xyz 或 HIP-3 的加密货币市场数据、订单簿、交易记录、资金费率或历史价格时，可以使用此功能。
allowed-tools: Bash
argument-hint: "query, e.g. 'BTC funding rate' or 'ETH 4h candles last week'"
metadata: {"openclaw":{"requires":{"env":["OXARCHIVE_API_KEY"]},"primaryEnv":"OXARCHIVE_API_KEY"}}
---
# 0xArchive API 技能

使用 `curl` 从 **0xArchive** 查询历史和实时的加密货币市场数据。支持三种交易所：**Hyperliquid**（perps DEX）、**Lighter.xyz**（订单簿 DEX）和 **HIP-3**（Hyperliquid builder perps）。数据类型包括订单簿、交易记录、K线图、资金费率、未平仓合约数量以及数据质量指标。

## 认证

所有接口都需要 `x-api-key` 头部字段。该密钥可以从 `$OXARCHIVE_API_KEY` 变量中获取。

```bash
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" "https://api.0xarchive.io/v1/..."
```

## 交易所与币种命名

| 交易所 | 路径前缀 | 币种格式 | 示例 |
|----------|-------------|-------------|---------|
| Hyperliquid | `/v1/hyperliquid` | 大写形式 | `BTC`, `ETH`, `SOL` |
| HIP-3 | `/v1/hyperliquid/hip3` | 区分大小写，格式为 `prefix:NAME` | `km:US500`, `xyz:XYZ100` |
| Lighter | `/v1/lighter` | 大写形式 | `BTC`, `ETH` |

Hyperliquid 和 Lighter 会在服务器端将币种名称自动转换为大写形式；HIP-3 的币种名称则原样传递。

## 时间戳

所有时间戳均为 **Unix 毫秒**。可以使用以下 shell 命令获取当前时间：

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
|----------|--------|-------|
| `GET /instruments` | -- | 列出所有币种 |
| `GET /instruments/{symbol}` | -- | 单个币种的详细信息 |
| `GET /orderbook/{symbol}` | `timestamp`, `depth` | 最新数据或指定时间点的订单簿 |
| `GET /orderbook/{symbol}/history` | `start`, `end`, `limit`, `cursor`, `depth` | 历史数据快照 |
| `GET /trades/{symbol}` | `start`, `end`, `limit`, `cursor` | 交易历史记录 |
| `GET /candles/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | OHLCV K线图 |
| `GET /funding/{symbol}/current` | -- | 当前资金费率 |
| `GET /funding/{symbol}` | `start`, `end`, `limit`, `cursor` | 资金费率历史记录 |
| `GET /openinterest/{symbol}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{symbol}` | `start`, `end`, `limit`, `cursor` | 未平仓合约历史记录 |
| `GET /liquidations/{symbol}` | `start`, `end`, `limit`, `cursor` | 清仓事件 |
| `GET /liquidations/user/{address}` | `start`, `end`, `limit`, `cursor`, `coin` | 指定用户的清仓记录 |

### HIP-3 (`/v1/hyperliquid/hip3`)

币种名称区分大小写（例如 `km:US500`）。该接口不提供清仓相关功能，且需要 Pro+ 订阅层级才能使用订单簿功能。

| 接口 | 参数 | 说明 |
|----------|--------|-------|
| `GET /instruments` | -- | 列出所有 HIP-3 币种 |
| `GET /instruments/{coin}` | -- | 单个币种 |
| `GET /orderbook/{coin}` | `timestamp`, `depth` | 需要 Pro+ 订阅层级 |
| `GET /orderbook/{coin}/history` | `start`, `end`, `limit`, `cursor`, `depth` | 需要 Pro+ 订阅层级 |
| `GET /trades/{coin}` | `start`, `end`, `limit`, `cursor` | 交易历史记录 |
| `GET /trades/{coin}/recent` | `limit` | 最近的交易记录（无需指定时间范围） |
| `GET /candles/{coin}` | `start`, `end`, `limit`, `cursor`, `interval` | OHLCV K线图 |
| `GET /funding/{coin}/current` | -- | 当前资金费率 |
| `GET /funding/{coin}` | `start`, `end`, `limit`, `cursor` | 资金费率历史记录 |
| `GET /openinterest/{coin}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{coin}` | `start`, `end`, `limit`, `cursor` | 未平仓合约历史记录 |

### Lighter (`/v1/lighter`)

数据类型与 Hyperliquid 相同（不提供清仓功能），但增加了订单簿历史记录的详细程度以及最近交易记录的功能。

| 接口 | 参数 | 说明 |
|----------|--------|-------|
| `GET /instruments` | -- | 列出所有 Lighter 币种 |
| `GET /instruments/{symbol}` | -- | 单个币种的详细信息 |
| `GET /orderbook/{symbol}` | `timestamp`, `depth` | 最新数据或指定时间点的订单簿 |
| `GET /orderbook/{symbol}/history` | `start`, `end`, `limit`, `cursor`, `depth`, `granularity` | 默认粒度为 `checkpoint` |
| `GET /trades/{symbol}` | `start`, `end`, `limit`, `cursor` | 交易历史记录 |
| `GET /trades/{symbol}/recent` | `limit` | 最近的交易记录（无需指定时间范围） |
| `GET /candles/{symbol}` | `start`, `end`, `limit`, `cursor`, `interval` | OHLCV K线图 |
| `GET /funding/{symbol}/current` | -- | 当前资金费率 |
| `GET /funding/{symbol}` | `start`, `end`, `limit`, `cursor` | 资金费率历史记录 |
| `GET /openinterest/{symbol}/current` | -- | 当前未平仓合约数量 |
| `GET /openinterest/{symbol}` | `start`, `end`, `limit`, `cursor` | 未平仓合约历史记录 |

### 数据质量 (`/v1/data-quality`)

| 接口 | 参数 | 说明 |
|----------|--------|-------|
| `GET /status` | -- | 系统健康状态 |
| `GET /coverage` | -- | 所有交易所的覆盖情况概览 |
| `GET /coverage/{exchange}` | -- | 单个交易所的覆盖情况 |
| `GET /coverage/{exchange}/{symbol}` | `from`, `to` | 指定时间范围内的币种覆盖情况 |
| `GET /incidents` | `status`, `exchange`, `since`, `limit`, `offset` | 事件列表 |
| `GET /incidents/{id}` | -- | 单个事件详情 |
| `GET /latency` | -- | 数据传输延迟指标 |
| `GET /sla` | `year`, `month` | 服务水平协议（SLA）合规报告 |

## 常用参数

| 参数 | 类型 | 说明 |
|-------|------|-------------|
| `start` | int | 开始时间戳（Unix 毫秒），历史数据接口必需 |
| `end` | int | 结束时间戳（Unix 毫秒），历史数据接口必需 |
| `limit` | int | 最大记录数，默认为 100，K线图最高为 1000 |
| `cursor` | string | 分页游标（来自 `meta.next_cursor`） |
| `interval` | string | K线图间隔：`1m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`, `1w`，默认为 `1h` |
| `depth` | int | 订单簿深度（每侧的价格层次数） |

## 智能默认值

如果用户未指定时间范围，系统将使用 **过去 24 小时** 的数据：

```bash
NOW=$(( $(date +%s) * 1000 ))
DAY_AGO=$(( NOW - 86400000 ))
```

对于 K线图，如果没有指定时间范围，系统会自动选择合适的范围（例如：4 小时的 K线图使用过去 7 天的数据）。

## 分页

如果响应中包含 `meta.next_cursor`，则表示还有更多数据。可以通过添加 `&cursor=VALUE` 参数来获取下一页数据：

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
|------|-------|-----------------|-----------------|-------------------|------------|
| 免费 | $0 | 仅支持 BTC（HIP-3 仅支持 km:US500） | 20 个价格层次 | -- | 30 天 | 15 每秒请求次数（RPS） |
| 建议级 | $49/月 | 所有币种 | 50 个价格层次 | `checkpoint` 粒度，30 秒间隔，10 秒间隔 | 1 年 | 50 每秒请求次数（RPS） |
| 专业级 | $199/月 | 所有币种 | 100 个价格层次 | `1 秒` 粒度 | 全部历史数据 | 150 每秒请求次数（RPS） |
| 企业级 | $499/月 | 所有币种 | 全部价格层次 | `tick` 粒度 | 全部历史数据 | 可自定义 |

## 错误处理

| HTTP 状态码 | 含义 | 处理方式 |
|-------------|---------|--------|
| 400 | 请求错误/验证失败 | 检查参数（缺少开始/结束时间戳或时间间隔无效） |
| 401 | API 密钥缺失或无效 | 设置 `$OXARCHIVE_API_KEY` |
| 403 | 订阅层级限制 | 升级订阅层级（例如：免费层级无法查询非 BTC 币种） |
| 404 | 未找到对应的币种 | 检查币种名称和交易所名称 |
| 429 | 数据请求速率受限 | 请稍后再试 |

错误响应会返回 `{ "success": false, "error": "描述" }`。

## 示例查询

```bash
# 列出 Hyperliquid 的所有币种
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/instruments" | jq '.data | length'

# 获取 BTC 的订单簿（前 10 个价格层次）
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

# 获取当前的 BTC 资金费率
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/funding/BTC/current" | jq '.data'

# 获取 HIP-3 km:US500 的过去 24 小时 K线图（1 小时间隔）
NOW=$(( $(date +%s) * 1000)); DAY_AGO=$(( NOW - 86400000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/hyperliquid/hip3/candles/km:US500?start=$DAY_AGO&end=$NOW&interval=1h" | jq '.data'

# 获取 Lighter 的 BTC 订单簿历史记录（30 秒粒度，过去 1 小时）
NOW=$(( $(date +%s) * 1000)); HOUR_AGO=$(( NOW - 3600000 ))
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/lighter/orderbook/BTC/history?start=$HOUR_AGO&end=$NOW&granularity=30s&limit=100" | jq '.data'

# 获取系统健康状态
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/status" | jq.'

# 获取当前月份的 SLA 报告
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/sla" | jq.'

# 获取 Hyperliquid BTC 的数据覆盖情况
curl -s -H "x-api-key: $OXARCHIVE_API_KEY" \
  "https://api.0xarchive.io/v1/data-quality/coverage/hyperliquid/BTC" | jq.'
```