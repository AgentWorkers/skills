---
name: yfinance
description: 访问 Yahoo Finance 数据——包括股票价格、历史行情、财务信息、期权信息、股息信息、新闻以及市场筛选工具。
---
# YFinance MCP 服务器

该服务器可访问雅虎财经（Yahoo Finance）的实时及历史金融数据，提供12种工具，涵盖股票价格、公司基本信息、分析师推荐、期权链、股息、市场动态和新闻等内容。

## 可用工具

### 股票数据（7种工具）

#### `tool_get_stock_price` — 当前价格及交易指标
```
tool_get_stock_price(symbol: "AAPL")
tool_get_stock_price(symbol: "BBCA.JK")
```
返回值：当前价格、价格变动百分比、开盘价、当日最高/最低价、成交量、52周价格范围、市值、市盈率、股息率、价格走势（▲/▼）。

#### `tool_get_stock_info` — 公司详情
```
tool_get_stock_info(symbol: "MSFT")
```
返回值：所属行业、公司全称、市值、市盈率、市净率、利润率、收入增长率、分析师目标价格、业务描述。

#### `tool_get_history` — 历史开盘价（OHLCV）数据
```
tool_get_history(symbol: "AAPL", period: "1mo", interval: "1d")
tool_get_history(symbol: "BBCA.JK", period: "1y", interval: "1wk")
tool_get_history(symbol: "BTC-USD", period: "5y", interval: "1mo")
```
- **时间周期**：`1天`、`5天`、`1个月`、`3个月`、`6个月`、`1年`、`2年`、`5年`、`10年`、`至今`
- **时间间隔**：`1分钟`、`2分钟`、`5分钟`、`15分钟`、`30分钟`、`60分钟`、`1小时`、`1天`、`5天`、`1周`、`1个月`、`3个月`

#### `tool_get_financials` — 财务报表
```
tool_get_financials(symbol: "AAPL", statement_type: "income", quarterly: false)
tool_get_financials(symbol: "MSFT", statement_type: "balance_sheet", quarterly: true)
tool_get_financials(symbol: "GOOG", statement_type: "all")
```
- **报表类型**：损益表（income）、资产负债表（balance_sheet）、现金流量表（cash_flow）、全部（all）

#### `tool_get_recommendations` — 分析师评级
```
tool_get_recommendations(symbol: "TSLA")
```
返回值：评级趋势（强烈买入、买入、持有、卖出、强烈卖出）、目标价格（最低、平均值、中位数、最高价）以及最近的评级调整。

#### `tool_get_options` — 期权链
```
tool_get_options(symbol: "AAPL")
tool_get_options(symbol: "TSLA", expiration: "2025-03-21")
```
返回值：看涨期权和看跌期权的相关信息（执行价格、最新价格、买入价、卖出价、成交量、未平仓合约量、隐含波动率），同时列出可交易的到期日。

#### `tool_get_dividends` — 股息历史
```
tool_get_dividends(symbol: "JNJ")
tool_get_dividends(symbol: "BBCA.JK")
```
返回值：当前股息率、除息日、股息支付率以及历史股息支付记录。

---

### 市场分析（3种工具）

#### `tool_compare_stocks` — 对比分析
```
tool_compare_stocks(symbols: "AAPL,MSFT,GOOG")
tool_compare_stocks(symbols: "BBCA.JK BBRI.JK BMRI.JK")
```
可同时对比最多10只股票的信息：价格、价格变动百分比、市值、市盈率、股息率、利润率、收入增长率、分析师评级。股票代码之间用逗号或空格分隔。

#### `tool_get_market_movers` — 行情热点股票
```
tool_get_market_movers(mover_type: "gainers")
tool_get_market_movers(mover_type: "losers")
tool_get_market_movers(mover_type: "most_active")
```

#### `tool_screen_stocks` — 股票筛选器
```
tool_screen_stocks(sector: "Technology", min_market_cap: 1000000000)
tool_screen_stocks(max_pe_ratio: 15, min_dividend_yield: 0.03)
tool_screen_stocks(sector: "Healthcare", exchange: "NMS")
```
所有筛选条件均可选择且可组合使用：
- **行业**：科技（Technology）、医疗保健（Healthcare）、金融服务（Financial Services）等
- **最低市值**：以美元为单位（例如：`1000000000` 表示10亿美元）
- **最高市盈率**：过去一段时间内的最高市盈率（例如：`25`）
- **最低股息率**：以小数表示（例如：`0.03` 表示3%）
- **交易所**：NMS（纳斯达克）、NYQ（纽约证券交易所）等

---

### 搜索与新闻（2种工具）

#### `tool_search_stocks` — 搜索股票
```
tool_search_stocks(query: "Apple", max_results: 5)
tool_search_stocks(query: "semiconductor ETF")
tool_search_stocks(query: "bank indonesia")
```
可通过股票名称、代码或关键词搜索股票、ETF、共同基金和指数。

#### `tool_get_news` — 最新新闻
```
tool_get_news(symbol: "AAPL", max_items: 5)
tool_get_news(symbol: "TSLA")
```
返回每条新闻的标题、发布者、链接、发布时间和缩略图。

---

## 支持的市场

该服务器支持 **雅虎财经支持的任何股票代码**：

| 市场 | 示例代码 |
|--------|----------|
| 美国股票 | AAPL, MSFT, GOOG, TSLA, AMZN |
| 印度尼西亚（IDX） | BBCA.JK, BBRI.JK, TLKM.JK, BMRI.JK |
| 日本（TSE） | 7203.T（丰田）、6758.T（索尼） |
| 英国（LSE） | SHEL.L, AZN.L, HSBA.L |
| 香港（HKEX） | 0700.HK（腾讯）、9988.HK（阿里巴巴） |
| ETF | SPY, QQQ, VTI, VOO, ARKK |
| 加密货币 | BTC-USD, ETH-USD, SOL-USD |
| 指数 | ^GSPC（标准普尔500指数）、^IXIC（纳斯达克指数）、^JKSE（印度尼西亚证券交易所指数） |
| 外汇 | USDIDR=X, EURUSD=X, GBPUSD=X |

## 常见使用场景

### 投资研究
1. 使用 `tool_search_stocks` 查找目标股票代码。
2. 使用 `tool_get_stock_info` 了解公司基本情况。
3. 使用 `tool_get_financials` 分析公司财务数据。
4. 使用 `tool_get_recommendations` 查看分析师评级。
5. 使用 `tool_get_history` 查看价格走势。

### 投资组合监控
1. 使用 `tool_compare_stocks` 对比持仓股票的表现。
2. 使用 `tool_get_stock_price` 查看股票当前价格。
3. 使用 `tool_get_news` 了解所持股票的最新动态。

### 市场探索
1. 使用 `tool_get_market_movers` 发现热门股票。
2. 使用 `tool_screen_stocks` 根据条件筛选股票。
3. 使用 `tool_get_stock_info` 深入研究潜在投资标的。

---

## 安装

### 快速安装（install.sh）

随附的 `install.sh` 脚本可自动完成所有安装步骤：
- 设置环境变量 `UV`
- 创建 Python 3.12 虚拟环境
- 安装所需软件包
- 配置 `mcporter` 并注册新技能 `yfinance-mcp-server`

安装过程包括：
1. 检查项目目录中是否存在 `pyproject.toml` 文件。
2. 如果未安装 `uv`，则进行安装。
3. 创建 Python 3.12 虚拟环境。
4. 安装 `yfinance-mcp-server` 及所有依赖库。
5. 确保所有12种工具都能正常使用。
6. 将 `yfinance` 添加到 `mcporter` 的配置文件中（系统会自动识别）。
7. 将 `SKILL.md` 文件复制到 `OpenClaw` 的技能目录中。

### 环境变量配置

可通过设置环境变量来自定义安装行为。

---

### 手动安装

（详细安装步骤请参考相关文档。）

### 验证安装结果

（安装完成后，可运行相关测试命令来验证所有功能是否正常运行。）

---