---
name: tvscreener
description: 使用 deepentropy/tvscreener 查询 TradingView 的筛选器数据，涵盖香港股票、A股股票、A股交易型开放式指数基金（ETF）以及美国股票。该工具可用于股票查找、技术指标分析（如价格、涨跌幅度、相对强弱指数 RSI、移动平均收敛发散指标 MACD、成交量等），以及基于股票代码或自定义字段/条件的市场查询。
---

# tvscreener

首先，可以使用简单的脚本来进行市场查询；当需要更复杂的功能时，再使用 Python 的原生接口。

## 安装

```bash
python3 -m pip install -U tvscreener
```

确保你的 Python 版本大于或等于 3.10。

## 快速命令（在 tvscreener 的根目录下运行）

> 在你喜欢的 Python 环境中（venv、pyenv 或系统 Python）中使用 Python 3.10 或更高版本。

```bash
# Preset single-symbol output (recommended)
python3 scripts/query_symbol.py --symbol HKEX:700 --market HONGKONG

# Custom query (fields + filters)
bash scripts/run_query.sh \
  --market CHINA \
  --symbol SHSE:600519 \
  --fields 'NAME,PRICE,CHANGE_PERCENT,VOLUME,RELATIVE_STRENGTH_INDEX_14,MACD_LEVEL_12_26,MACD_SIGNAL_12_26,MACD_HIST,SIMPLE_MOVING_AVERAGE_20,SIMPLE_MOVING_AVERAGE_50,SIMPLE_MOVING_AVERAGE_200,EXPONENTIAL_MOVING_AVERAGE_20,EXPONENTIAL_MOVING_AVERAGE_50,EXPONENTIAL_MOVING_AVERAGE_200,BOLLINGER_UPPER_BAND_20,BOLLINGER_LOWER_BAND_20,STOCHASTIC_PERCENTK_14_3_3,STOCHASTIC_PERCENTD_14_3_3,AVERAGE_TRUE_RANGE_14,MOVING_AVERAGES_RATING' \
  --filter 'NAME=600519'

# Field discovery
python3 scripts/discover_fields.py --keyword macd --limit 20
```

### Shell 命令中的引号使用规则

- 将 `--fields` 和 `--filter` 参数用单引号括起来。
- 如果使用间隔时间格式（如 `FIELD|60`），必须加上引号，以避免被 Shell 解释为管道操作。

## 查询规则

- 推荐的核心技术指标：`PRICE`（价格）、`CHANGE_PERCENT`（百分比变化）、`VOLUME`（成交量）、`RELATIVE_STRENGTH_INDEX_14`（相对强弱指数）、`MACD_LEVEL_12_26`（MACD 指数）、`MACD SIGNAL_12_26`（MACD 信号）、`MACD_HIST`（MACD 历史数据）、`SIMPLE_MOVING_AVERAGE_20/50/200`（简单移动平均线）、`EXPONENTIAL_MOVING_AVERAGE_20/50/200`（指数移动平均线）、`BOLLINGER_UPPER_band_20`（布林带上限）、`BOLLINGER_lower_band_20`（布林带下限）、`STOCHASTIC_PERCENTK_14_3_3`（随机百分比K指标）、`STOCHASTIC_PERCENTD_14_3_3`（随机百分比D指标）、`AVERAGE TRUE RANGE_14`（平均真实范围）、`MOVING_AVERAGES_RATING`（移动平均线评级）。
- 间隔时间字段的格式：`FIELD|60` / `FIELD|240`（例如：`RELATIVE_STRENGTH_INDEX_14|60`）
  - **注意**：在某些 tvscreener 版本中，使用 `FieldWithInterval` 属性时，间隔时间字段可能会导致 `scripts/custom_query.py` 出错。
  - 解决方法：可以选择不使用间隔时间字段，或者使用 `scripts/query_symbol.py` 来获取稳定的单只股票技术数据。
- 过滤条件：`=`、`!=`、`>`、`<`、`>=`、`<=`

## 故障排除

- **错误：`ImportError: cannot import name 'Market' from 'tvscreener'**
  - 通常是由于 Python 环境配置不正确或安装了多个 Python 版本导致的。
  - 解决方法：确保所有命令和脚本都使用相同的 Python 版本（3.10 或更高），然后重新安装 tvscreener：
    - `python3 -m pip install -U tvscreener`
- **错误：`zsh: command not found: 60,...`**
  - 原因是未加引号的 `FIELD|60` 被 Shell 解释为管道操作。
  - 解决方法：将 `--fields` 参数用单引号括起来。

## 参考资料

- 工作流程和示例：`references/README_usage.md`
- API 详细信息：`references/api/screeners.md`、`references/api/fields.md`、`references/api/filters.md`、`references/api/enums.md`

如果脚本无法满足需求，请查阅参考资料，并直接使用 tvscreener 的原生 API 编写程序。

## 回归测试

```bash
bash scripts/test_markets.sh
```

测试对象包括腾讯（香港）、茅台（A股）、A股 ETF（510300）和百度（美国）。