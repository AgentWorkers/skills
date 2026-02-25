---
name: stock-strategy-backtester
description: 在历史上的OHLCV数据上回测股票交易策略，并报告胜率、回报率（CAGR）、最大回撤率（drawdown）、夏普比率（Sharpe ratio）以及交易记录。该功能可用于评估或比较策略规则（如SMA交叉、RSI均值回归、突破信号等），量化交易成本的影响，调整策略参数，或从CSV数据中生成性能总结。适用于以下请求：“回测股票策略的胜率”、“计算收益率”、“比较两种策略的回测结果”以及“根据历史价格生成策略报告”。
---
# 股票策略回测工具

## 概述

该工具能够从每日的高低开收价（OHLCV）CSV文件中运行可重复的、仅用于长期投资的股票策略回测。通过集成脚本生成一致的指标和交易级输出结果，并以投资者易于理解的格式进行汇总。

## 快速入门

1. 准备一个至少包含`Date`和`Close`列的CSV文件。
2. 运行基线回测：

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy sma-crossover \
  --fast-window 20 \
  --slow-window 60
```

3. 导出回测结果以供审查：

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy rsi-reversion \
  --rsi-period 14 \
  --rsi-entry 30 \
  --rsi-exit 55 \
  --commission-bps 5 \
  --slippage-bps 2 \
  --output-json /path/to/result.json \
  --output-trades /path/to/trades.csv
```

## 工作流程

1. **数据验证**
   - 确保`Date`列可以被解析，并且数据按升序排序。
   - 确保`Open/High/Low/Close`列中的数据为数值类型；如果缺少`Open/High/Low`值，则使用`Close`值作为替代。

2. **选择策略逻辑**
   - `sma-crossover`：基于快速/慢速移动平均线的趋势跟随策略。
   - `rsi-reversion`：在指标超卖时买入，在市场恢复动能时卖出。
   - `breakout`：在价格突破高点时买入，在价格跌破低点时卖出。

3. **设定合理的假设**
   - 必须设置`--commission-bps`和`--slippage-bps`参数。
   - 不要将无交易成本的回测结果视为可实际应用的策略。

4. **比较不同策略变体**
   - 每次只修改一个参数，然后在相同的日期范围和成本模型下进行比较。

5. **生成最终报告**
   - 报告以下指标：`total_return_pct`（总回报率）、`cagrpct`（年化复合增长率）、`win_rate pct`（胜率）、`max_drawdown pct`（最大回撤率）、`sharpe_ratio`（夏普比率）和`profit_factor`（收益因子）以及交易数量。
   - 使用交易记录CSV文件来解释策略的盈利来源。

## 支持的命令

- **基线SMA策略：**

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy sma-crossover \
  --fast-window 10 \
  --slow-window 50
```

- **突破策略：**

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy breakout \
  --lookback 20
```

- **仅输出JSON格式（适用于自动化流程）：**

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy rsi-reversion \
  --quiet
```

## 输出格式

脚本会将以下信息以JSON对象的形式输出到标准输出（stdout）：
- `strategy`（策略类型）
- `period`（回测周期）
- `metrics`（各项指标）
- `config`（配置参数）
- `trades`（交易记录）

**可选输出格式：**
- `--output-json`：完整的结果JSON文件
- `--output-trades`：按交易记录生成的CSV文件

## 分析注意事项

1. **使用样本外数据验证策略逻辑**
   - 建议使用“向前预测”的方法进行验证，而非一次性调整参数。

2. **避免数据泄漏**
   - 在时间点`t`计算交易信号后，应在时间点`t+1`的开市时执行交易。

3. **全面展示风险与收益**
   - 在报告回报时，必须同时展示最大回撤率和交易数量。

4. **将回测结果视为研究结果**
   - 回测结果仅供参考，不应被视为财务建议。

## 参考资料

- 指标详细信息：`references/backtest-metrics.md`