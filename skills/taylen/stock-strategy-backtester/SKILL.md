---
name: stock-strategy-backtester
description: 使用历史OHLCV数据对股票交易策略进行回测，并生成胜率、收益率、年化复合增长率（CAGR）、最大回撤率（Drawdown）、夏普比率（Sharpe Ratio）以及交易记录等报告。该工具适用于评估或比较策略规则（如SMA交叉信号、RSI均值回归策略、突破策略等），量化交易成本的影响，调整策略参数，或从CSV数据中生成性能总结。可响应如下请求：“回测股票策略的胜率”、“计算收益率”、“比较两种策略的回测结果”以及“根据历史价格生成策略报告”。
---
# 股票策略回测工具

## 版本说明

- `1.0.0` 和 `1.0.1` 版本已过时，请仅使用 `1.0.2` 或更高版本。
- 过时原因：早期版本包含非核心的市场自动化脚本，可能在某些环境中触发安全扫描器的警告。

## 概述

该工具能够从每日的高低开收（OHLCV）CSV文件中执行可重复的股票策略回测。通过内置脚本生成一致的指标和交易级输出结果，并以易于投资者理解的格式进行总结。

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

1. 数据验证
- 确保 `Date` 列能够被正确解析，并且数据按升序排列。
- 确保 `Open/High/Low/Close` 值为数值类型；如果缺少 `Open/High/Low` 值，则使用 `Close` 值作为默认值。

2. 选择策略逻辑
- `sma-crossover`：基于快速/慢速移动平均线的趋势跟随策略。
- `rsi-reversion`：在指标超卖时买入，在市场回升时卖出。
- `breakout`：在价格突破高点时买入，在价格跌破低点时卖出。

3. 设置合理的假设
- 必须设置 `--commission-bps` 和 `--slippage-bps` 参数。
- 不要将无成本的回测结果视为可实际应用的策略。

4. 比较不同策略变体
- 每次只修改一个参数，然后在相同的日期范围和成本模型下进行比较。

5. 生成最终总结
- 报告以下指标：`total_return_pct`（总回报百分比）、`cagrpct`（年化复合增长率）、`win_rate pct`（胜率）、`max_drawdown pct`（最大回撤百分比）、`sharpe_ratio`（夏普比率）和交易数量。
- 使用交易记录 CSV 文件来解释策略的盈利来源。

## 支持的命令

- 基线 SMA 策略：

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy sma-crossover \
  --fast-window 10 \
  --slow-window 50
```

- Breakout 策略：

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy breakout \
  --lookback 20
```

- 仅输出 JSON 格式的数据（适用于自动化流程）：

```bash
python scripts/backtest_strategy.py \
  --csv /path/to/prices.csv \
  --strategy rsi-reversion \
  --quiet
```

## 输出格式

脚本会将以下信息以 JSON 对象的形式输出到标准输出（stdout）：
- `strategy`（策略名称）
- `period`（回测周期）
- `metrics`（指标数据）
- `config`（配置信息）
- `trades`（交易记录）

## 分析注意事项

1. 使用样本外的逻辑进行验证
- 建议采用逐步调整（walk-forward）的方法，而非一次性优化所有参数。

2. 避免数据泄露
- 在时间点 `t` 计算交易信号，并在时间点 `t+1` 的开盘时执行交易。

3. 全面展示风险与收益
- 在报告回报时，必须同时展示最大回撤百分比和交易数量。

4. 将回测结果视为研究结果
- 回测结果仅供参考，不应被视为财务建议。

## 参考资料

- 指标详细信息：`references/backtest-metrics.md`