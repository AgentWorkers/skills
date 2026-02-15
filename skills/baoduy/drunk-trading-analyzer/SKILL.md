---
name: trading-analyzer
description: 多源交易分析工具（`/drunk-trading-analyzer`）能够整合加密货币数据（来自TradingView）、股票数据（来自Alpha Vantage）以及市场情报（来自Yahoo Finance），生成统一的分析报告。这些报告包含价格走势、技术指标和情绪分析等内容。
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "os": ["darwin", "linux", "win32"],
        "mcp_servers":
          ["tradingview-mcp", "alphavantage", "yahoo-finance-server"],
        "description": "Uses MCP (Model Context Protocol) tools auto-discovered by mcporter for seamless integration with TradingView, Alpha Vantage, and Yahoo Finance APIs",
      },
  }
---

# **交易分析师技能**

该工具结合了加密货币和股票数据，并利用人工智能技术提供深入的市场分析。

## **快速入门**

### 分析加密货币

```bash
# List available TradingView tools
mcporter list tradingview-mcp

# Analyze a specific coin
mcporter call tradingview-mcp.coin_analysis symbol=BTCUSDT exchange=BINANCE timeframe=15m

# Find bullish coins
mcporter call tradingview-mcp.top_gainers exchange=BINANCE timeframe=4h limit=25

# Detect volume breakouts
mcporter call tradingview-mcp.volume_breakout_scanner exchange=KUCOIN timeframe=15m volume_multiplier=2.0
```

### 分析股票

```bash
# List available Alpha Vantage and Yahoo Finance tools
mcporter list alphavantage
mcporter list yahoo-finance-server

# Get company fundamentals
mcporter call alphavantage.get_ticker_info symbol=AAPL

# Fetch latest news
mcporter call yahoo-finance-server.get_ticker_news symbol=AAPL count=10

# Get stock price history
mcporter call alphavantage.get_price_history symbol=AAPL period=1y interval=1d

# Get earnings data
mcporter call alphavantage.ticker_earning symbol=AAPL period=quarterly
```

## **常见用例**

### 1. 快速加密货币分析

```bash
# 1. Get immediate technical overview
mcporter call tradingview-mcp.coin_analysis symbol=BTCUSDT

# 2. Identify breakout opportunities
mcporter call tradingview-mcp.smart_volume_scanner \
  exchange=BINANCE min_volume_ratio=2.0 min_price_change=2.0

# 3. Find bullish signals
mcporter call tradingview-mcp.top_gainers exchange=BINANCE timeframe=4h
```

### 2. 基本面股票研究

```bash
# 1. Get company metrics
mcporter call alphavantage.get_ticker_info symbol=TSLA

# 2. Get sentiment from latest news
mcporter call yahoo-finance-server.get_ticker_news symbol=TSLA count=5

# 3. Confirm trend with historical data
mcporter call alphavantage.get_price_history symbol=TSLA period=1y interval=1d
```

### 3. 市场筛选

使用加密货币筛选器来识别投资机会：

```bash
# Top performers
mcporter call tradingview-mcp.top_gainers exchange=BINANCE timeframe=1h limit=50

# Volume + momentum
mcporter call tradingview-mcp.smart_volume_scanner \
  exchange=KUCOIN min_volume_ratio=3.0 rsi_range=oversold

# Top stock sectors
mcporter call yahoo-finance-server.get_top_entities \
  entity_type=performing_companies sector=technology count=10
```

### 4. 综合报告

通过整合多个数据源进行全面的分析——可以使用脚本或代理调用来协调这些工具的使用。

## **MCP工具参考**

### **TradingView（加密货币分析）**

| 工具                        | 功能                                                  |
| -------------------------- | -------------------------------------------------------- |
| `coin_analysis`            | 对特定加密货币进行详细分析（指标、数据）                         |
| `smart_volume_scanner`     | 通过成交量、RSI和价格变化来筛选加密货币                     |
| `volume_breakout_scanner`  | 筛选出现成交量和价格突破的加密货币                     |
| `top_gainers`              | 表现最佳的加密货币（基于Bollinger Band过滤）                   |
| `top_losers`               | 表现最差的加密货币                             |
| `advanced_candle_pattern`  | 分析不同时间框架下的蜡烛图形态                         |
| `consecutive_candles_scan` | 筛选连续蜡烛图的变化趋势                         |

### **Alpha Vantage（股票数据）**

| 工具                | 功能                                   |
| ------------------- | ----------------------------------------- |
| `get_ticker_info`   | 获取公司基本信息、财务指标和治理结构                         |
| `get_price_history` | 获取历史价格数据以进行趋势分析                         |
| `ticker_earning`    | 获取公司的盈利数据和未来盈利预测                         |

### **Yahoo Finance（市场情报）**

| 工具               | 功能                             |
| ------------------ | ----------------------------------- |
| `get_ticker_news`  | 获取带有情感分析的最新新闻文章                         |
| `get-top-entities` | 按行业分类的顶级股票/ETF                         |

## **配置**

### **交易所选项（加密货币）**

- `BINANCE`（默认，流动性最高）  
- `KUCOIN`  
- `BYBIT`  

### **时间框架（加密货币）**

- `5m`, `15m`, `1h`, `4h`, `1D`（默认），`1W`, `1M`  

### **输出格式**

- `markdown`（默认）——格式化的报告  
- `json`——原始数据结构  

## **资产检测**

系统会自动将资产路由到正确的分析工具：

1. **加密货币**：以USDT、USDC、BTC、ETH、BNB或常见的加密货币对（如BTC、ETH、SOL、ADA）结尾的资产  
2. **股票**：以1-5个字母组成的股票代码（如AAPL、TSLA、MSFT）  
3. **备用方案**：首先尝试查找股票数据，如果找不到则转而使用加密货币数据  

## **示例报告**

### **加密货币报告结构**

```
# Trading Analysis: BTCUSDT

## Price Overview
Current: $45,200 (-2.3%) | 24h High: $46,100 | Low: $44,800
Volume: $28.5B | Change: -$1,050

## Technical Analysis (1D)
Trend: Bearish | RSI: 35 (Oversold) | MACD: Negative
Bollinger Bands: Below MA | Support: $44,200 | Resistance: $46,500

## Market Data
Exchange: BINANCE | Sentiment: Neutral-Bearish

## Recommendation
Signal: HOLD | Risk: Moderate
```

### **股票报告结构**

```
# Trading Analysis: AAPL

## Price Overview
Current: $278.12 (+0.80%) | Open: $277.12 | Volume: 50.4M
52-week High: $305.25 | Low: $201.50

## Company Fundamentals
P/E Ratio: 28.5 | Market Cap: $2.8T | Dividend: 0.92%
Revenue Growth: 2.3% | Profit Margin: 28.1%

## Latest News (5 articles)
1. "Apple announces AI features" - CNBC (2h ago) [Positive]
2. "Q1 earnings beat estimates" - Reuters (1d ago) [Positive]

## Recommendation
Outlook: BULLISH | Target: $295 | Risk: Low
```

## **错误处理**

- 如果MCP服务器不可用，系统会优雅地切换到备用方案  
- 如果某个数据源失败，系统会生成部分报告  
- 支持重复查询的缓存机制  
- 提供清晰的错误信息及重试建议  

## **性能说明**

- 在5分钟的时间窗口内缓存查询结果  
- 对于多数据源的报告，系统会并行获取数据  
- 每个资产的平均分析时间为2-5秒  

## **故障排除**

```bash
# Verify MCP servers running
echo "Check .vscode/mcp.json configuration"

# Debug API keys
echo "Ensure Alpha Vantage API key is set"

# Test connectivity
python3 -c "import requests; print(requests.__version__)"
```

## **扩展方式**

要添加新的数据源，请按照以下步骤操作：

1. 在`analyzers/`目录下创建新的分析工具  
2. 实现`analyze(symbol, options)`接口  
3. 在路由逻辑中注册新工具  
4. 更新工具参考列表  

## **许可证**

MIT许可证