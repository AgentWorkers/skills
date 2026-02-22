---
metadata:
  name: BacktestBot
  description: Backtest trading strategies against historical market data with performance analytics and risk metrics
  version: 0.0.2
  tags: [finance, trading, backtesting, strategy, quantitative]
  openclaw:
    requires:
      env: [BACKTESTBOT_API_KEY]
    primaryEnv: BACKTESTBOT_API_KEY
---

# BacktestBot

使用历史市场数据对交易策略进行回测，并提供详细的性能分析。

## 功能介绍

BacktestBot 允许您使用历史数据来定义、测试和评估交易策略，具体包括：

- **策略定义**：用自然语言或结构化规则描述策略（入场/出场信号、头寸大小、止损策略）
- **历史数据模拟**：在多年的股票、期权、期货和加密货币的逐笔交易数据或日数据上运行策略
- **性能指标**：夏普比率（Sharpe Ratio）、最大回撤率（Max Drawdown）、胜率（Win Rate）、利润因子（Profit Factor）、复合年增长率（CAGR）以及交易级别的详细分析
- **风险分析**：风险价值（Value-at-Risk）、与基准指数的相关性、最糟糕情况下的回撤期以及尾部风险指标（Tail Risk Metrics）
- **策略比较**：并行测试多种策略变体，并根据经风险调整后的回报进行排名

## 使用方法

请您的代理执行策略回测并分析结果：

- “使用过去5年内RSI低于30的入场条件，对SPY指数执行均值回归策略的回测”
- “比较自2020年以来标准普尔500指数各板块的买入持有策略与动量轮换策略的表现”
- “如果我在AAPL的波段交易中使用2%的追踪止损，最大回撤率是多少？”
- “优化我的QQQ指数移动平均线交叉策略的回顾周期”

## 配置

请设置以下环境变量：

- `BACKTESTBOT_API_KEY`：BacktestBot的API密钥，用于验证历史OHLCV数据请求、策略模拟和性能指标的访问权限。
- `BACKTESTBOT_DATA_DIR`：（可选）本地缓存历史数据的目录，默认为`~/.backtestbot/data`。