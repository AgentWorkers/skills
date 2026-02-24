---
name: stock-strategy-backtester
description: 使用历史的高低开低收（OHLCV）数据对股票交易策略进行回测，并生成胜率、回报率、年复合增长率（CAGR）、最大回撤率、夏普比率（Sharpe Ratio）以及交易记录等报告。该工具适用于评估或比较不同的交易策略（如简单移动平均线交叉（SMA crossover）、相对强弱指数均值回归（RSI mean reversion）、突破交易（breakout）等策略规则；量化交易成本对策略表现的影响；调整策略参数；以及从CSV数据中生成策略性能总结。可用来执行诸如“回测股票策略的胜率”、“计算收益率”、“比较两种策略的回测结果”或“根据历史价格生成策略报告”等操作。
---
# 股票策略回测工具

## 概述

该工具能够从每日的高低开收价（OHLCV）CSV文件中运行可重复的股票策略回测。通过内置脚本生成统一的指标和交易细节数据，并以易于投资者理解的格式进行总结。

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
   - 确保`Date`列可以被正确解析，并且数据按升序排列。
   - 确保`Open/High/Low/Close`列中的数据为数值类型；如果缺少`Open/High/Low`值，则使用`Close`值作为替代。

2. **选择策略逻辑**
   - `sma-crossover`：基于快速移动平均线和慢速移动平均线的趋势跟踪策略。
   - `rsi-reversion`：在股票超卖时买入，并在价格回升时卖出。
   - `breakout`：在股价突破高点时买入，在股价跌破低点时卖出。

3. **设定合理的假设**
   - 必须设置`--commission-bps`（佣金率）和`--slippage-bps`（滑点率）参数。
   - 不要将无实际交易成本的回测结果视为可实际应用的策略。

4. **比较不同策略变体**
   - 每次只修改一个策略参数，然后在相同的日期范围和成本模型下进行比较。

5. **生成最终报告**
   - 报告以下指标：`total_return_pct`（总回报率）、`cagr_pct`（年化复合增长率）、`win_rate pct`（胜率）、`max_drawdown pct`（最大回撤率）、`sharpe_ratio`（夏普比率）和`profit_factor`（收益因子）以及交易数量。
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

- **仅输出JSON格式（用于自动化流程）：**

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy rsi-reversion \
  --quiet
```

- **发布到OpenClaw市场**（需要`clawhub`命令行工具和网络连接）：

```bash
bash scripts/publish_openclaw.sh 1.0.0 \
  "Initial release: stock strategy backtesting with win-rate and return analytics."
```

- **在遇到速率限制时重试发布：**

```bash
bash scripts/publish_with_retry.sh 1.0.1 \
  "Add A/B marketplace copy variants and Chinese listing text for conversion optimization."
```

- **查询扫描/列表状态：**

```bash
bash scripts/check_openclaw_status.sh stock-strategy-backtester 12 30
```

## 输出格式

脚本会将结果以JSON对象的形式输出到标准输出（stdout），包含以下内容：
- `strategy`（策略类型）
- `period`（回测周期）
- `metrics`（各项指标）
- `config`（配置信息）
- `trades`（交易记录）

**可选输出格式：**
- `--output-json`：完整的JSON结果
- `--output-trades`：逐笔交易的CSV文件

## 分析注意事项

1. **使用样本外数据**：优先使用样本外数据（out-of-sample data）进行验证，而非仅通过一次调整来优化策略。
2. **避免数据泄露**：在时间点`t`计算交易信号后，应在时间点`t+1`的开盘时执行交易。
3. **全面展示风险与收益**：在报告回报时，必须同时展示最大回撤率和交易数量。
4. **将结果视为研究结果**：回测结果仅用于参考，不应被视为财务建议。

## 参考资料

- **指标详细信息**：`references/backtest-metrics.md`
- **上市前检查清单**：`references/market-launch-checklist.md`
- **上市申请模板**：`references/listing-copy.md`
- **A/B类上市申请模板**：`references/listing-copy-ab.md`