---
name: crypto-tracker
description: 通过 CoinGecko API 追踪加密货币价格、设置警报以及搜索各种加密货币。
homepage: https://www.coingecko.com/api
metadata: {"clawdis":{"emoji":"📈","requires":{"bins":["uv"]}}}
---

# 加密货币追踪器

使用免费的 CoinGecko API（无需 API 密钥）来追踪加密货币价格、设置价格/百分比警报以及搜索加密货币。

## 快速命令

### 查看价格
```bash
# Single coin
uv run {baseDir}/scripts/crypto.py price bitcoin

# Multiple coins
uv run {baseDir}/scripts/crypto.py price bitcoin ethereum solana

# With more details (market cap, volume)
uv run {baseDir}/scripts/crypto.py price bitcoin --detailed
```

### 搜索加密货币
```bash
# Find coin ID by name/symbol
uv run {baseDir}/scripts/crypto.py search doge
uv run {baseDir}/scripts/crypto.py search cardano
```

### 管理警报
```bash
# Set price threshold alert
uv run {baseDir}/scripts/crypto.py alert <user_id> bitcoin above 100000
uv run {baseDir}/scripts/crypto.py alert <user_id> ethereum below 3000

# Set percentage change alert (24h)
uv run {baseDir}/scripts/crypto.py alert <user_id> bitcoin change 5    # ±5%
uv run {baseDir}/scripts/crypto.py alert <user_id> solana drop 10      # -10%
uv run {baseDir}/scripts/crypto.py alert <user_id> ethereum rise 15    # +15%

# List user's alerts
uv run {baseDir}/scripts/crypto.py alerts <user_id>

# Remove an alert
uv run {baseDir}/scripts/crypto.py alert-rm <alert_id>

# Check all alerts (for cron/heartbeat)
uv run {baseDir}/scripts/crypto.py check-alerts
```

## 加密货币别名

常见的货币别名会自动被识别：
- `btc` → 比特币
- `eth` → 以太坊
- `sol` → Solana
- `doge` → Dogecoin
- `ada` → Cardano
- `xrp` → Ripple
- `dot` → Polkadot
- `matic` → Polygon
- `link` → Chainlink
- `avax` → Avalanche-2
- `ltc` → Litecoin

## 警报类型

| 类型 | 例子 | 触发条件 |
|------|---------|---------------|
| `above` | `当比特币价格超过 100,000 美元时提醒用户` | 价格 >= $100,000 |
| `below` | `当以太坊价格低于 3,000 美元时提醒用户` | 价格 <= $3,000 |
| `change` | `当比特币价格变化超过 5% 时提醒用户` | 24 小时内的价格变化幅度 >= ±5% |
| `drop` | `当 Solana 价格下跌超过 10% 时提醒用户` | 24 小时内的价格变化幅度 <= -10% |
| `rise` | `当以太坊价格上涨超过 15% 时提醒用户` | 24 小时内的价格变化幅度 >= +15% |

## Cron 任务集成

可以定期（例如每 15 分钟）检查警报：
```bash
uv run {baseDir}/scripts/crypto.py check-alerts --json-output
```

系统会返回被触发的警报以及对应的用户 ID 以供通知。

## 数据存储

警报信息存储在 `{baseDir}/data/alerts.json` 文件中，包含：
- 每个用户的警报记录
- 重复通知之间的冷却时间（默认：1 小时）
- 最后一次触发警报的时间戳

## 注意事项

- CoinGecko 的免费 tier 每分钟允许约 10-30 次请求（无需 API 密钥）
- 支持超过 15,000 种加密货币
- 可使用 `--json-output` 标志生成机器可读的输出格式