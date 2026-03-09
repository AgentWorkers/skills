---
name: us-stock-radar
description: 这是一个用于美国股票的筛选工具，支持上市前分析、单只股票深度研究以及 watchlist（关注列表）的提醒功能。该工具利用公开市场数据来实现这些功能。适用于需要系统化美国股票筛选、对股票进行评级（A/B/C/D 级别）、提供适合初学者与高级用户的解释、以及进行基于事件的分析（包括时间戳标记的信息和明确的数据缺失情况）的用户。
---
# 美国股票雷达（US Stock Radar）

该工具支持三种模式来执行美国股票相关的分析工作流程：
- **筛选器模式（Screener）**：根据多因素信号评分对股票进行排序。
- **深度分析模式（Deep-Dive）**：结合基本面数据和技术指标对单只股票进行深入分析。
- **观察列表模式（Watchlist）**：监控自定义股票并生成警报提示。

请注意，这只是一个**仅用于读取数据的启发式市场分析工具**，并非完整的机构级研究终端。公开的免费API可能存在数据延迟、部分缺失或访问限制，请在使用时明确了解这些限制。

## 工作流程

1. 使用相应的模式运行 `scripts/us_stock_radar.py` 脚本。
2. 首先读取 JSON 格式的输出结果，并将其视为最权威的数据来源。
3. 在解释分析结果时，需明确说明存在的局限性、分析的可靠性以及数据缺口。
4. 避免做出确定性的预测，而是提供信号等级、触发原因以及关于数据不完整的警告。
5. 如果某些API无法正常使用，系统会以降级的功能继续运行，并明确显示分析可靠性的降低情况。

## 快速审核流程

若需快速查看分析结果，可以执行以下命令：
1. `python3 skills/us-stock-radar/scripts/us_stock-radar.py --sources`
2. `python3 skills/us-stock-radar/scripts/us_stock-radar.py --mode screener --json`
3. 确认该脚本仅执行公开的、基于HTTP的读取操作。
4. 检查在数据覆盖不完整的情况下，系统是否能够正确显示 `availability`（数据可用性）、`data_gaps`（数据缺口）以及 `degraded_mode`（功能降级状态）等信息。

## 命令说明

```bash
python3 skills/us-stock-radar/scripts/us_stock_radar.py --sources
python3 skills/us-stock-radar/scripts/us_stock_radar.py --version
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode screener --tickers "AAPL,MSFT,NVDA,AMZN,GOOGL"
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode deep-dive --ticker AAPL --audience pro
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode deep-dive --ticker TSLA --audience beginner --lang zh
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode watchlist --tickers "AAPL,NVDA,TSLA" --event-mode high-alert
python3 skills/us-stock-radar/scripts/us_stock_radar.py --mode screener --json
```

## 安全性与使用范围限制

- **仅限读取数据**：该工具仅用于查询公开的市场数据源。
- **无需认证**：无需使用用户名、密码、经纪账户或私有API。
- **禁止交易操作**：不允许下达订单或执行任何交易操作，也不会修改投资组合的状态。
- **禁止文件写入和消息发送**：在正常使用过程中，该工具不会写入任何文件或发送任何外部消息。
- **仅提供分析结果**：该工具仅用于生成分析报告，不提供投资建议。

## 输出格式规范

- **默认语言设置**：自动选择适合的语言（`auto`）。
- 如果命令行参数中包含中文，输出结果将使用中文；如果没有检测到中文，则使用英文。
- **JSON格式的输出**：输出结果与语言无关。
- 必须包含以下信息：
  - `as_of_utc`（数据更新时间）
  - `mode`（运行模式）
  - `event_mode`（事件类型）
  - `availability`（数据可用性）
  - `data_gaps`（数据缺口）
  - `degraded_mode`（功能降级状态）
  - `confidence`（分析可靠性）
  - `sources`（数据来源）
  - 分析过程中的注意事项或限制条件

- **针对不同用户的输出格式**：
  - **专业用户（Pro）**：简洁的分析摘要。
  - **初学者（Beginner）**：通俗易懂的解读内容。
- **事件类型**：
    - `normal`（普通模式）
    - `high-alert`（高警觉模式，采用更严格的判断标准）

## 评分标准（A/B/C/D）

信号评分综合考虑了以下因素：
- **估值范围（PE）**
- **相对强弱指数（RSI）**
- **成交量变化**
- **股价与50日均线（MA50）的关系**
- **收入增长率**
- **净资产收益率（ROE）的质量**

评分等级：
- **A**：评分 ≥ 5
- **B**：评分 = 4
- **C**：评分 = 2–3
- **D**：评分 ≤ 1

## 解释说明

- 评分结果仅作为参考依据，不代表价格预测。
- 如果某些基本面数据缺失，应降低分析的可靠性，而不是默认假设市场趋势为牛市或熊市。
- 公开的免费API可能存在数据延迟、部分数据缺失或因地区限制而无法访问。
- 预交易或计划中的分析操作应明确标注时间戳。

## 数据来源

- **Yahoo Finance 数据源**：
  - 股票报价 API：`/v7/finance/quote`
  - 股票图表 API：`/v8/finance/chart`
  - 股票报价摘要 API：`/v10/finance/quoteSummary`
- **Stooq 数据源**：提供每日股票报价和历史数据（CSV格式）。