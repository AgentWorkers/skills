---
name: kalshi-trading
description: 这是一个仅限读取的 Kalshi OpenAPI 技能，用于市场发现、流动性检测以及市场验证。该技能可用于扫描和评估 Kalshi 项目（投资机会）。如果您需要执行买入/卖出操作，建议将其与独立的纸面交易（paper-trading）技能结合使用。
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["node"] }
      }
  }
---
# Kalshi Trading (OpenAPI，仅限读取)

请仅将此技能用于Kalshi的市场调研和数据验证。

## 规则

- 使用OpenAPI的读取端点来进行市场数据的发现和验证。
- 该技能不支持下单、修改或取消订单。
- 该技能不包含用于执行交易操作的脚本（如纸质账本操作脚本）。

## 主要命令

- 获取交易所状态：
  ```bash
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs status --pretty
```

- 进行广泛的市场扫描：
  ```bash
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs markets --status open --limit 1000 --pretty
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs events --limit 100 --pretty
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs series --limit 400 --pretty
```

- 进行针对性的市场验证：
  ```bash
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs market --ticker <TICKER> --pretty
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs trades --ticker <TICKER> --limit 200 --pretty
node skills/kalshi-trading/scripts/kalshi_openapi_reader.mjs orderbook --ticker <TICKER> --pretty
```

## 可选集成：需要“纸质账本”技能

如果您需要实现交易执行的流程（包括开仓/平仓操作），请安装并使用专门的“纸质交易”技能，该技能会提供相应的执行脚本。
此Kalshi技能可以为您提供候选交易对象或市场相关的数据，供您进一步使用。
  ```bash
node --experimental-strip-types skills/paper-trading/scripts/paper_trading.ts status --account kalshi --format json --pretty
```

## 环境配置

（可选，默认使用Kalshi的生产环境API配置）：
```bash
export KALSHI_BASE_URL="https://api.elections.kalshi.com/trade-api/v2"
```

## 测试

运行Kalshi读取功能的测试用例：
```bash
node --test skills/kalshi-trading/tests/kalshi_openapi_reader.test.mjs
```