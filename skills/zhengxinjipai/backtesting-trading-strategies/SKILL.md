---
name: backtesting-trading-strategies
description: >
  使用历史数据对加密货币和传统交易策略进行回测。  
  该功能可计算性能指标（如夏普比率、索蒂诺比率、最大回撤率），生成资产价值曲线，并优化策略参数。  
  适用于用户想要测试交易策略、验证交易信号或比较不同交易方法的情况。  
  可通过以下指令触发该功能：  
  “backtest strategy”（回测策略）、  
  “test trading strategy”（测试交易策略）、  
  “historical performance”（历史表现）、  
  “simulate trades”（模拟交易）、  
  “optimize parameters”（优化参数）、  
  “validate signals”（验证交易信号）。
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(python:*)
version: 2.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
---
# 回测交易策略

## 概述

在投入真实资金之前，先使用历史数据验证交易策略的有效性。本工具提供了一个完整的回测框架，包含8种内置交易策略、全面的性能指标以及参数优化功能。

**主要特性：**
- 8种预构建的交易策略（简单移动平均线（SMA）、指数移动平均线（EMA）、相对强弱指数（RSI）、MACD、布林带（Bollinger Bands）、突破策略（Breakout）、均值回归策略（Mean Reversion）、动量策略（Momentum）  
- 全面的性能指标（夏普比率（Sharpe Ratio）、索蒂诺比率（Sortino Ratio）、卡尔马比率（Calmar Ratio）、风险价值（VaR）、最大回撤（max drawdown）  
- 参数网格搜索优化功能  
- 股票价格曲线可视化  
- 单笔交易分析功能  

## 先决条件

安装所需的依赖项：  
```bash
pip install pandas numpy yfinance matplotlib
```  

（高级功能可选：）  
```bash
pip install ta-lib scipy scikit-learn
```  

## 使用说明  

### 第1步：获取历史数据  

```bash
python {baseDir}/scripts/fetch_data.py --symbol BTC-USD --period 2y --interval 1d
```  

数据会被缓存到 `{baseDir}/data/{symbol}_{interval}.csv` 文件中，以便后续使用。  

### 第2步：运行回测  

- 使用默认参数进行基本回测：  
```bash
python {baseDir}/scripts/backtest.py --strategy sma_crossover --symbol BTC-USD --period 1y
```  

- 使用自定义参数进行高级回测：  
```bash
# Example: backtest with specific date range
python {baseDir}/scripts/backtest.py \
  --strategy rsi_reversal \
  --symbol ETH-USD \
  --period 1y \
  --capital 10000 \
  --params '{"period": 14, "overbought": 70, "oversold": 30}'
```  

### 第3步：分析结果  

结果会被保存到 `{baseDir}/reports/` 目录下，包括：  
- `*_summary.txt`：性能指标  
- `*_trades.csv`：交易记录  
- `*_equity.csv`：股票价格曲线数据  
- `*_chart.png`：股票价格曲线图表  

### 第4步：优化参数  

通过参数网格搜索找到最优参数：  
```bash
python {baseDir}/scripts/optimize.py \
  --strategy sma_crossover \
  --symbol BTC-USD \
  --period 1y \
  --param-grid '{"fast_period": [10, 20, 30], "slow_period": [50, 100, 200]}'
```  

## 输出结果  

### 性能指标  

| 指标          | 描述                          |
|----------------|---------------------------------------------|
| 总回报        | 整体百分比收益/亏损                      |
| 复合年增长率（CAGR）   | 年化复合增长率                      |
| 夏普比率        | 风险调整后的回报（目标值：>1.5）                  |
| 索蒂诺比率        | 下降风险调整后的回报                      |
| 卡尔马比率        | 回报除以最大回撤                      |

### 风险指标  

| 指标          | 描述                          |
|----------------|---------------------------------------------|
| 最大回撤        | 最大峰值到最低值的跌幅                    |
| VaR（95%）      | 95%置信水平下的风险价值                    |
| CVaR（95%）      | 超过VaR的预期损失                    |
| 波动率        | 年化标准差                        |

### 交易统计  

| 指标          | 描述                          |
|----------------|---------------------------------------------|
| 总交易次数      | 完整交易次数                        |
| 胜率          | 盈利交易的百分比                      |
| 盈利因子        | 总利润除以总损失                      |
| 期望收益        | 单笔交易的预期收益                      |

### 示例输出  

```
================================================================================
                    BACKTEST RESULTS: SMA CROSSOVER
                    BTC-USD | [start_date] to [end_date]
================================================================================
 PERFORMANCE                          | RISK
 Total Return:        +47.32%         | Max Drawdown:      -18.45%
 CAGR:                +47.32%         | VaR (95%):         -2.34%
 Sharpe Ratio:        1.87            | Volatility:        42.1%
 Sortino Ratio:       2.41            | Ulcer Index:       8.2
--------------------------------------------------------------------------------
 TRADE STATISTICS
 Total Trades:        24              | Profit Factor:     2.34
 Win Rate:            58.3%           | Expectancy:        $197.17
 Avg Win:             $892.45         | Max Consec. Losses: 3
================================================================================
```  

## 支持的交易策略  

| 策略            | 描述                                      | 关键参数                                      |
|----------------|-----------------------------------------|-----------------------------------------|
| `sma_crossover`     | 简单移动平均线交叉策略                | `fast_period`, `slow_period`                   |
| `ema_crossover`     | 指数移动平均线交叉策略                | `fast_period`, `slow_period`                   |
| `rsi_reversal`     | RSI超买/超卖策略                   | `period`, `overbought`, `oversold`                |
| `macd`         | MACD信号线交叉策略                | `fast`, `slow`, `signal`                   |
| `bollinger_bands`     | 布林带策略                        | `period`, `std_dev`                   |
| `breakout`       | 价格突破策略                    | `lookback`, `threshold`                   |
| `mean_reversion`    | 均值回归策略                    | `period`, `z_threshold`                   |
| `momentum`      | 动量策略                        | `period`, `threshold`                   |

## 配置  

创建 `{baseDir}/config/settings.yaml` 文件以配置回测参数：  
```yaml
data:
  provider: yfinance
  cache_dir: ./data

backtest:
  default_capital: 10000
  commission: 0.001     # 0.1% per trade
  slippage: 0.0005      # 0.05% slippage

risk:
  max_position_size: 0.95
  stop_loss: null       # Optional fixed stop loss
  take_profit: null     # Optional fixed take profit
```  

## 错误处理  

有关常见问题及解决方法，请参阅 `{baseDir}/references/errors.md`。  

## 使用示例  

详细的使用示例请参阅 `{baseDir}/references/examples.md`，包括：  
- 多资产比较  
- 前向分析（Walk-forward analysis）  
- 参数优化工作流程  

## 相关文件  

| 文件            | 用途                                      |
|----------------|-----------------------------------------|-----------------------------------------|
| `scripts/backtest.py`    | 主要回测引擎                      |
| `scripts/fetch_data.py`    | 历史数据获取工具                      |
| `scripts/strategies.py`    | 交易策略定义文件                      |
| `scripts/metrics.py`    | 性能指标计算工具                      |
| `scripts/optimize.py`    | 参数优化工具                      |

## 资源推荐  

- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance数据源  
- [TA-Lib](https://ta-lib.org/) - 技术分析库                      |
- [QuantStats](https://github.com/ranaroussi/quantstats) - 投资组合分析工具            |