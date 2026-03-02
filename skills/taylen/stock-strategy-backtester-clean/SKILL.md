---
name: stock-strategy-backtester-clean
description: 在历史的高低开低收（OHLCV）数据上回测股票交易策略，并生成报告，内容包括胜率、收益率、年复合增长率（CAGR）、最大回撤率、夏普比率（Sharpe ratio）以及交易记录。该工具适用于评估或比较不同的交易策略（如移动平均线交叉（SMA crossover）、相对强弱指数均值回归（RSI mean reversion）、突破交易规则（breakout），量化交易成本的影响，以及从CSV数据中生成策略性能摘要。用户可以通过请求如“回测股票策略的胜率”、“计算收益率”、“比较两种策略的回测结果”或“根据历史价格生成策略报告”来使用该工具。
---
# Stock Strategy Backtester (Clean Version)

## 版本说明

- 如果您的环境设置为 `stock-strategy-backtester-clean`，请使用此版本名称。

## 概述

该工具能够从每日的高低开收价（OHLCV）CSV文件中运行可重复的股票策略回测。它使用内置脚本生成一致的指标和交易级输出结果，并以易于投资者理解的格式进行总结。

## 快速入门

1. 准备一个至少包含 `Date` 和 `Close` 列的 CSV 文件。
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
  --slippage-bps 2
```

## 工作流程

1. **数据验证**
   - 确保 `Date` 列可以被正确解析，并且数据按升序排列。
   - 确保 `Open/High/Low/Close` 列的值均为数字；如果缺少某个值，则使用 `Close` 的值作为替代。

2. **选择策略逻辑**
   - `sma-crossover`：基于快速/慢速移动平均线的趋势跟踪策略。
   - `rsi-reversion`：在指标超卖时买入，在市场动能恢复时卖出。
   - `breakout`：在价格突破高点时买入，在价格跌破低点时卖出。

3. **设置合理的假设**
   - 必须设置 `--commission-bps` 和 `--slippage-bps` 参数。
   - 不要将无成本的回测结果视为可实际应用的策略。

4. **比较不同策略**
   - 每次只修改一个参数，然后在相同的日期范围和成本模型下进行比较。

5. **生成最终报告**
   - 报告以下指标：`total_return_pct`（总回报率）、`cagr_pct`（年化复合增长率）、`win_rate pct`（胜率）、`max_drawdown pct`（最大回撤率）、`sharpe_ratio`（夏普比率）和交易次数。
   - 使用交易记录 CSV 文件来解释策略的盈利来源。

## 支持的命令

- **基线 SMA 策略：**
   ```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy sma-crossover \
  --fast-window 10 \
  --slow-window 50
```

- **Breakout 策略：**
   ```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy breakout \
  --lookback 20
```

- **仅输出 JSON 格式（适用于自动化流程）：**
   ```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy rsi-reversion \
  --quiet
```

## 输出格式

- 脚本会将结果以 JSON 对象的形式输出到标准输出（stdout），内容包括：
   - `strategy`（策略名称）
   - `period`（回测周期）
   - `metrics`（各项指标）
   - `config`（配置参数）
   - `trades`（交易记录）

## 分析注意事项

1. **使用样本外数据**
   - 建议使用滚动验证（walk-forward validation）而非一次性调整策略参数。

2. **避免数据泄露**
   - 在第 `t` 标准差处计算交易信号，并在第 `t+1` 标准差的开盘时执行交易。

3. **全面展示风险与收益**
   - 在报告收益时必须同时展示最大回撤率和交易次数。

4. **将结果视为研究结果**
   - 回测结果仅用于分析参考，不应被视为财务建议。

## 参考资料

- 指标详细信息：`references/backtest-metrics.md`