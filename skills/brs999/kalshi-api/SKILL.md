---
name: kalshi-api
description: 这是一个仅限读取的 Kalshi API 技能，用于市场发现、流动性检查以及市场验证。它可以用于扫描和评估 Kalshi 交易机会。如果您需要执行开仓/平仓操作，建议将其与独立的纸笔交易（paper-trading）技能配合使用。
homepage: https://docs.kalshi.com
user-invocable: true
disable-model-invocation: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["node"] }
      }
  }
---
# Kalshi API（仅限读取）

此技能仅用于Kalshi的行情分析和市场验证。

## 规则

- 使用OpenAPI的读取接口来进行市场数据查询和验证。
- 该技能不支持下单、修改订单或取消订单的功能。
- 该技能不包含用于执行纸质账本操作的脚本。

## 主要命令

- 查看交易所状态：
  ```bash
node {baseDir}/scripts/kalshi-api.mjs status --pretty
```

- 进行广泛的市场扫描：
  ```bash
node {baseDir}/scripts/kalshi-api.mjs markets --status open --limit 1000 --pretty
node {baseDir}/scripts/kalshi-api.mjs events --limit 100 --pretty
node {baseDir}/scripts/kalshi-api.mjs series --limit 400 --pretty
```

- 进行针对性的市场验证：
  ```bash
node {baseDir}/scripts/kalshi-api.mjs market --ticker <TICKER> --pretty
node {baseDir}/scripts/kalshi-api.mjs trades --ticker <TICKER> --limit 200 --pretty
node {baseDir}/scripts/kalshi-api.mjs orderbook --ticker <TICKER> --pretty
```

## 可选集成：需要“纸质账本”技能

如果您需要执行纸质交易（开仓/平仓）的操作，请安装并使用专门的“纸质交易”技能，该技能提供相应的执行脚本。
此Kalshi技能可以为此技能提供候选交易数据或市场分析结果。

```bash
node --experimental-strip-types skills/paper-trading/scripts/paper_trading.ts status --account kalshi --format json --pretty
```

## 环境配置

（可选，默认使用Kalshi生产环境API配置）：
```bash
export KALSHI_BASE_URL="https://api.elections.kalshi.com/trade-api/v2"
```

## 测试

运行Kalshi API的读取测试：
```bash
node --test {baseDir}/tests/kalshi-api.test.mjs
```