---
name: tradingview-screener
description: 使用 TradingView 数据监控 6 个资产类别的市场行情。策略的构建依赖于 API 预过滤器以及 pandas 库计算出的交易信号（交易信号）。整个策略的配置通过 YAML 文件进行管理。
version: 1.1.0
---

# TradingView 筛选器

使用 TradingView 的市场数据筛选股票、加密货币、外汇、债券、期货和加密货币。无需任何身份验证。

## 设置（仅运行一次）

首次使用前，请运行安装脚本以创建虚拟环境（venv）并安装依赖项：
```bash
bash skills/tradingview-screener/install.sh
```
该脚本会在技能目录（skill）下创建一个 `.venv/` 目录，并安装所有所需的包。

## 执行

所有脚本均使用该技能自带的虚拟环境：
```bash
skills/tradingview-screener/.venv/bin/python3 skills/tradingview-screener/scripts/<script>.py [args]
```

**Windows:**
```bash
skills/tradingview-screener/.venv/Scripts/python.exe skills/tradingview-screener/scripts/<script>.py [args]
```

## 模式

| 模式 | 描述 | 脚本 |
|------|-------------|--------|
| **筛选** | 使用过滤器、列和排序进行一次性扫描 | `screen.py` |
| **信号** | 基于 YAML 的信号检测（预过滤器 + 计算信号） | `signal-engine.py` |

## 快速入门

### 筛选模式
```bash
skills/tradingview-screener/.venv/bin/python3 skills/tradingview-screener/scripts/screen.py \
  --asset-class stock --limit 20 \
  --filters '[{"field":"MARKET_CAPITALIZATION","op":">","value":1000000000}]' \
  --columns NAME,PRICE,CHANGE_PERCENT,VOLUME \
  --sort-by VOLUME --sort-order desc
```

### 信号模式
```bash
# List available signals
skills/tradingview-screener/.venv/bin/python3 skills/tradingview-screener/scripts/signal-engine.py --list

# Run a signal
skills/tradingview-screener/.venv/bin/python3 skills/tradingview-screener/scripts/signal-engine.py --signal golden-cross
```

## 资产类别

| 类别 | 筛选器 | 字段枚举 |
|-------|----------|------------|
| 股票 | StockScreener | StockField |
| 加密货币 | CryptoScreener | CryptoField |
| 外汇 | ForexScreener | ForexField |
| 债券 | BondScreener | BondField |
| 期货 | FuturesScreener | FuturesField |
| 加密货币 | CoinScreener | CoinField |

## 信号类型（计算型）

| 类型 | 描述 | 关键参数 |
|------|-------------|------------|
| 交叉信号 | 快速字段与慢速字段的交叉 | fast, slow, direction |
| 阈值信号 | 字段值超过预设阈值 | field, op, value |
| 表达式信号 | 在 DataFrame 上使用的 Pandas 表达式 | expr |
| 范围信号 | 字段值在指定范围内 | field, min, max |

## 过滤操作符

`>`, `>=`, `<`, `<=`, `==`, `!=`, `between` (value: [min, max]), `isin` (value: [...])

## 常见股票字段

`NAME`, `PRICE`, `CHANGE_PERCENT`, `VOLUME`, `MARKET_CAPITALIZATION`, `SECTOR`,
`SIMPLE_MOVING_AVERAGE_50`, `SIMPLE_MOVING_AVERAGE_200`, `RELATIVE_STRENGTH_INDEX_14`,
`MACD_LEVEL_12_26`, `AVERAGE_VOLUME_30_DAY`

可以使用 `StockField.search("keyword")` 在 Python 中查找更多字段（共 13,000 多个字段）。

## 预置信号

| 信号名称 | 文件路径 | 描述 |
|--------|------|-------------|
| 金叉信号 | `state/signals/golden-cross.yaml` | SMA50 上穿 SMA200（看涨信号） |
| 过度卖出反弹 | `state/signals/oversold-bounce.yaml` | RSI < 30 且价格上升 |
| 成交量突破 | `state/signals/volume-breakout.yaml` | 成交量超过平均值 2 倍且市场动能强劲 |

## 输出格式
```markdown
**Stock Screener** | 15 results | Sorted by VOLUME desc

| NAME | PRICE | CHANGE_PERCENT | VOLUME |
|------|-------|----------------|--------|
| AAPL | 185.50 | 2.3 | 80000000 |
...
```

## 时间周期

`1`, `5`, `15`, `30`, `60`, `120`, `240`, `1D`, `1W`, `1M`

通过传递 `--timeframe 60` 参数，可以应用每小时的时间间隔来计算技术指标。

## 参考资料

- [API 文档](references/tvscreener-api-guide.md) - 筛选器类型、过滤器、字段查询方法
- [信号处理指南](references/computed-signals-guide.md) - YAML 格式、信号类型配置
- [策略模板](references/strategy-templates.md) - 预置的筛选策略
- [字段预设](references/field-presets.md) - 各资产类别的常用字段组合