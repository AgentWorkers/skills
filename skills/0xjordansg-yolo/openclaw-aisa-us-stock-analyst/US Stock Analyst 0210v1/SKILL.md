---
name: us-stock-analyst
description: "专业的美国股票分析服务，涵盖财务数据、新闻、市场情绪以及多模型人工智能分析。每份分析报告的价格为0.02至0.10美元。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# 美国股票分析师 📈

**由 AIsa 的统一 API 平台提供专业的股票分析服务。**

一个 API 密钥，即可获取完整的市场情报和 AI 驱动的洞察。

## 🔥 您能做什么？

### 投资研究
```
"Analyze NVDA: financial metrics, analyst estimates, insider trades, 
news sentiment, and AI-powered valuation"
```

### 投资组合监控
```
"Track my portfolio (AAPL, MSFT, GOOGL): daily updates on metrics, 
news, and sentiment changes"
```

### 盈利分析
```
"Full Tesla Q4 earnings analysis: results vs estimates, guidance, 
price reaction, analyst updates"
```

### 竞争对手分析
```
"Compare AMD vs NVDA: financials, growth, valuation, market sentiment"
```

### 筛选与发现
```
"Find tech stocks with P/E < 30, revenue growth > 20%, 
and positive insider activity"
```

## 快速入门
```bash
export AISA_API_KEY="your-key"
```

---

## 核心功能

### 📊 财务数据（MarketPulse API）

**实时财务指标**
```bash
curl "https://api.aisa.one/apis/v1/financial/financial-metrics/snapshot?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

- 市值、市盈率、收入、每股收益（EPS）、利润率、净资产收益率（ROE）、债务与股本比率等。

**历史股价**
```bash
# Daily prices for last 30 days
curl "https://api.aisa.one/apis/v1/financial/prices?ticker=AAPL&start_date=2025-01-01&end_date=2025-01-31&interval=day&interval_multiplier=1" \
  -H "Authorization: Bearer $AISA_API_KEY"

# 5-minute intraday data
curl "https://api.aisa.one/apis/v1/financial/prices?ticker=AAPL&start_date=2025-02-07&end_date=2025-02-07&interval=minute&interval_multiplier=5" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**财务报表**
```bash
# All statements (income, balance, cash flow)
curl "https://api.aisa.one/apis/v1/financial/financial_statements/all?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**分析师预测**
```bash
# EPS forecasts and ratings
curl "https://api.aisa.one/apis/v1/financial/analyst/eps?ticker=AAPL&period=annual" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**内幕交易**
```bash
# Track insider buy/sell activity
curl "https://api.aisa.one/apis/v1/financial/insider/trades?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**机构持股情况**
```bash
# See who owns the stock
curl "https://api.aisa.one/apis/v1/financial/institutional/ownership?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**美国证券交易委员会（SEC）文件**
```bash
# Access 10-K, 10-Q, 8-K filings
curl "https://api.aisa.one/apis/v1/financial/sec/filings?ticker=AAPL" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

### 📰 新闻与研究

**公司新闻**
```bash
curl "https://api.aisa.one/apis/v1/financial/news?ticker=AAPL&limit=10" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**网络搜索（新闻与文章）**
```bash
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/web?query=AAPL+stock+analysis&max_num_results=10" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

**学术研究**
```bash
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/scholar?query=semiconductor+industry+analysis&max_num_results=5" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

### 🐦 社交情绪分析

**Twitter 搜索**
```bash
curl "https://api.aisa.one/apis/v1/twitter/tweet/advanced_search?query=\$AAPL&queryType=Latest" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

### 📺 视频内容

**YouTube 搜索（财报电话会议、分析视频）**
```bash
curl "https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AAPL+earnings+call&gl=us&hl=en" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

---

### 🤖 AI 分析（多模型）

**大型语言模型（LLM）接口（兼容 OpenAI）**
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {
        "role": "system",
        "content": "You are a professional equity analyst."
      },
      {
        "role": "user",
        "content": "Analyze Apple stock investment prospects"
      }
    ],
    "temperature": 0.3,
    "max_tokens": 2000
  }'
```

**支持的模型：**
- GPT-4、GPT-4 Turbo（OpenAI）
- Claude 3 Opus、Sonnet、Haiku（Anthropic）
- Gemini 1.5 Pro、Ultra（Google）
- Qwen Max、Plus（Alibaba）
- DeepSeek V2（DeepSeek）
- Grok（xAI）

---

## Python 客户端
```bash
# Basic analysis
python3 {baseDir}/scripts/stock_analyst.py analyze --ticker AAPL

# Standard analysis with multiple models
python3 {baseDir}/scripts/stock_analyst.py analyze --ticker NVDA --depth standard --models gpt-4 claude-3-opus

# Deep analysis (all data sources)
python3 {baseDir}/scripts/stock_analyst.py analyze --ticker TSLA --depth deep

# Quick screening
python3 {baseDir}/scripts/stock_analyst.py analyze --ticker MSFT --depth quick

# Save report to file
python3 {baseDir}/scripts/stock_analyst.py analyze --ticker GOOGL --output report.json
```

---

## 分析深度选项

| 分析模式 | 所需时间 | 费用 | 数据来源 |
|------|------|------|--------------|
| **快速** | 约 10 秒 | $0.01-0.02 | 财务指标、新闻、Twitter、基础 AI 分析 |
| **标准** | 约 20 秒 | $0.02-0.05 | 包括分析师预测、内幕交易信息、YouTube 视频 |
| **深度** | 约 30 秒 | $0.05-0.10 | 包括财务报表、机构持股信息、SEC 文件、学术研究数据 |

---

## API 参考

| 类别 | 端点 | 方法 | 费用 |
|----------|----------|--------|------|
| **财务指标** | `/financial/financial-metrics/snapshot` | GET | $0.002 |
| **股价** | `/financial/prices` | GET | $0.001 |
| **新闻** | `/financial/news` | GET | $0.001 |
| **财务报表** | `/financial/financial_statements/*` | GET | $0.002 |
| **分析师预测** | `/financial/analyst/eps` | GET | $0.002 |
| **内幕交易** | `/financial/insider/trades` | GET | $0.001 |
| **机构持股** | `/financial/institutional/ownership` | GET | $0.001 |
| **SEC 文件** | `/financial/sec/filings` | GET | $0.001 |
| **网络搜索** | `/scholar/search/web` | POST | $0.001 |
| **学术搜索** | `/scholar/search/scholar` | POST | $0.002 |
| **Twitter** | `/twitter/tweet/advanced_search` | GET | $0.0004 |
| **YouTube** | `/youtube/search` | GET | $0.002 |
| **LLM** | `/v1/chat/completions` | POST | 基于令牌的费用 |

每个响应都会包含 `usage.cost` 和 `usage.credits_remaining` 信息。

---

## 示例输出
```json
{
  "ticker": "NVDA",
  "analysis_date": "2025-02-07T10:30:00Z",
  
  "investment_summary": "NVIDIA maintains dominant position in AI chip market with strong data center revenue growth. Recent Blackwell launch positions company for continued expansion...",
  
  "key_metrics": {
    "market_cap": 1780500000000,
    "pe_ratio": 68.5,
    "revenue": 60922000000,
    "revenue_growth": 1.26,
    "profit_margin": 0.489,
    "roe": 1.152
  },
  
  "sentiment_analysis": {
    "sentiment": "bullish",
    "confidence": "high",
    "key_themes": ["AI dominance", "Data center growth", "Blackwell launch"],
    "summary": "Overwhelmingly positive sentiment following Q4 earnings beat"
  },
  
  "valuation": {
    "assessment": "fairly_valued",
    "price_target_12m": 850.00,
    "reasoning": "Premium valuation justified by AI market leadership and strong growth trajectory"
  },
  
  "data_sources": {
    "Financial Metrics": "Available",
    "Stock News": 10,
    "Analyst Estimates": "Available",
    "Insider Trades": 15,
    "Twitter": "Available",
    "YouTube": 5
  }
}
```

---

## 价格

**分析费用：**
- 快速模式：每只股票 $0.01-0.02
- 标准模式：每只股票 $0.02-0.05
- 深度模式：每只股票 $0.05-0.10

**费用对比：**
- Bloomberg 终端：每月 $2,000
- FactSet：每月 $1,000
- 传统分析师报告：每份 $50-500
- **AIsa 股票分析师服务：每只股票 $0.02-0.10** ✨

**费用明细：**
```
Standard Analysis ($0.02-0.05):
├── Financial Metrics: $0.002
├── Stock Prices: $0.001
├── Company News: $0.001
├── Analyst Estimates: $0.002
├── Insider Trades: $0.001
├── Twitter: $0.0004
├── YouTube: $0.002
└── LLM Analysis: $0.01-0.04
```

---

## 使用场景

### 1. 投资研究
- 在投资前筛选和分析股票
```python
analyst.analyze_stock("NVDA", depth="deep")
```

### 2. 投资组合监控
- 每日更新您的持股情况
```python
for ticker in ["AAPL", "MSFT", "GOOGL"]:
    report = analyst.analyze_stock(ticker, depth="quick")
```

### 盈利季
- 全面的盈利分析
```python
analyst.analyze_stock("TSLA", depth="standard")
# Check estimates, actual results, guidance, reaction
```

### 内幕交易监控
- 监控内幕交易活动
```python
report = analyst.analyze_stock("META", depth="standard")
print(report['raw_data']['insider_trades'])
```

### 情绪分析
- 跟踪市场情绪
```python
report = analyst.analyze_stock("COIN", depth="standard")
print(report['sentiment_analysis'])
```

---

## 合规性

**免责声明（始终包含）：**
> 本分析仅用于提供信息参考，不应被视为个性化投资建议。在做出投资决策前，请自行进行研究并咨询持牌财务顾问。

**合规性说明：**
- 遵守美国证券交易委员会（SEC）规则 15c2-1（非投资建议）
- 符合 FINRA 相关规定（仅提供信息）
- 遵守 GDPR 数据隐私法规

---

## 开始使用

1. 在 [aisa.one](https://aisa.one) 注册
2. 获取您的 API 密钥
3. 充值（按使用量付费，最低金额 $5）
4. 设置环境变量：`export AISA_API_KEY="您的 API 密钥"`
5. 运行分析脚本：`python scripts/stock_analyst.py analyze --ticker AAPL`

---

## 完整 API 文档

- **API 参考**：https://aisa.mintlify.app/api-reference/introduction
- **完整文档**：https://aisa.mintlify.app/llms.txt
- **支持**：support@aisa.one
- **Discord 社区**：https://discord.gg/aisa

---

## 关于 AIsa

**AIsa** – 专为 AI 代理设计的统一 API 平台。

- 一个 API 密钥，按使用次数计费。
- 支持多种 AI 代理。

- 官网：https://aisa.one
- 文档：https://aisa.mintlify.app