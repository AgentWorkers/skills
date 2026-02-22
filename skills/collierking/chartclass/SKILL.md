---
metadata:
  name: ChartClass
  description: Technical analysis and chart pattern recognition for equities, options, and crypto markets
  version: 0.0.2
  tags: [finance, trading, technical-analysis, charting, patterns]
  openclaw:
    requires:
      env: [CHARTCLASS_API_KEY]
    primaryEnv: CHARTCLASS_API_KEY
---

# ChartClass

用于金融市场的技术分析和图表形态识别工具。

## 功能概述

ChartClass 提供基于人工智能的技术分析功能，适用于股票、期权和加密货币，包括：

- **形态识别**：能够识别头肩顶/底、双顶/底、旗形、楔形、杯形等图表形态
- **指标分析**：支持移动平均线、相对强弱指数（RSI）、MACD、布林带、成交量分析以及自定义指标组合
- **支撑/阻力位检测**：自动从历史价格走势中提取关键价格水平
- **趋势分析**：判断当前趋势的方向、强度及潜在的反转信号
- **多时间框架分析**：支持日线、周线和日内线图表，并具备时间框架的叠加分析功能

## 使用方法

您可以要求您的代理执行以下操作来分析图表和技术设置：

- “分析特斯拉股票（TSLA）的日线图表，找出当前的图表形态”
- “SPY 的关键支撑和阻力位是多少？”
- “筛选出那些在 200 日移动平均线上方形成牛市旗形图案的股票”
- “显示 NVDA 股票 4 小时图表中的 RSI 发散情况”

## 配置要求

为了访问市场数据，请设置以下环境变量：

- `CHARTCLASS_API_KEY`：ChartClass 的 API 密钥，用于验证对 OHLCV 价格数据、技术指标值及形态识别结果的请求
- `CHARTCLASS_DEFAULT_TIMEFRAME`：（可选）默认的图表时间框架，可选值包括 `1m`、`5m`、`15m`、`1h`、`4h`、`daily`、`weekly`。默认值为 `daily`