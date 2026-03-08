---
name: stock-sentiment
description: "**美国股票研究的情绪分析与财务数据**  
本工具提供多引擎人工智能情绪分析（包括Grok、DeepSeek、GPT-5），以及来自美国证券交易委员会（SEC）的EDGAR文件、Seeking Alpha评级、财报电话会议记录、社交媒体情绪数据、新闻分析、FRED宏观经济指标和2000多只股票的OHLCV价格等信息。适用于股票研究、情绪监测、SEC文件分析或市场数据探索等场景。"
argument-hint: "[symbol]"
allowed-tools: mcp__alphafactoryx__*
metadata:
  openclaw:
    requires:
      env:
        - name: ALPHAFACTORYX_MCP_TOKEN
          description: "API token for paid tier access (starter/pro/enterprise). Not required for free tier (20 req/day)."
          required: false
      bins: []
    emoji: "📊"
    homepage: "https://alphafactoryx.com"
    mcp:
      server: alphafactoryx
      type: streamable-http
      url: "https://mcp.alphafactoryx.com/mcp"
      headers:
        Authorization: "Bearer $ALPHAFACTORYX_MCP_TOKEN"
---
# 股票情绪分析与财务数据

提供股票情绪分析及美国股票研究工具。通过27个MCP工具，您可以查询多引擎AI情绪评分、SEC文件、分析师评级、财报文本、社交媒体情绪、宏观经济指标以及2000多只股票的价格数据。

## 参考资料

- `references/tools.md` — 全部工具的参考信息，包括参数和描述
- `references/workflows.md` — 逐步的研究工作流程（股票分析、情绪分析、宏观经济分析、深度搜索）

## 快速入门

无需任何token或注册。免费 tier：每个IP每天20次请求。

**查看数据覆盖范围：**
```
mcp__alphafactoryx__get_archive_stats()
```

**研究某只股票：**
```
mcp__alphafactoryx__sa_overview(symbol="AAPL")
mcp__alphafactoryx__edgar_latest(symbol="AAPL", form_type="10-K")
mcp__alphafactoryx__stocknews_articles(symbol="AAPL")
mcp__alphafactoryx__kline(symbol="AAPL")
```

**在档案中搜索：**
```
mcp__alphafactoryx__edgar_search(query="revenue guidance", symbol="AAPL")
mcp__alphafactoryx__sa_search(query="AI chips")
mcp__alphafactoryx__sa_transcript_search(query="margin expansion")
```

**查看股票情绪：**
```
mcp__alphafactoryx__stocknews_articles(symbol="AAPL")
mcp__alphafactoryx__polygon_news_articles(symbol="AAPL")
mcp__alphafactoryx__x_sentiment(symbol="AAPL")
```

**获取宏观经济数据：**
```
mcp__alphafactoryx__fred_macro()
```

## 工具分类

| 分类 | 工具 | 主要功能 |
|----------|-------|-----------------|
| 通用工具 | 1 | 档案统计与数据覆盖 |
| SEC EDGAR | 5 | 10-K、10-Q、8-K文件及Form 4文件；全文搜索 |
| Seeking Alpha | 10 | 文章、新闻、财报文本、评级、财务数据、评论 |
| Stock News | 2 | 带有Grok、DeepSeek和GPT-5情感分析的新闻文章 |
| Polygon News | 2 | 带有每只股票AI情感分析的新闻文章 |
| X/Twitter | 3 | 根据互动量筛选的推文 |
| FRED Macro | 2 | 25个宏观经济指标（利率、CPI、GDP、VIX、收益率曲线） |
| OHLCV | 2 | 每日/每小时/每分钟的价格数据 |

## 认证

**免费 tier（无需设置）**：每天20次请求，每秒1次请求。直接连接即可使用。

**付费 tier：** 在您的环境变量中设置 `ALPHAFACTORYX_MCP_TOKEN`：

| Tier | 每日请求量 | 费率 | 价格 |
|------|-------|------|-------|
| 免费 | 20 | 1次/秒 | $0 |
| 初级 | 200 | 2次/秒 | $29/月 |
| 专业 | 2,000 | 5次/秒 | $99/月 |
| 企业级 | 10,000 | 10次/秒 | 从$299/月起 |

详情请访问 [alphafactoryx.com/pricing](https://alphafactoryx.com/pricing)。

## 最佳实践

- **先使用 `get_archive_stats` 检查数据覆盖范围**  
- **交叉引用来源** — 结合EDGAR、Seeking Alpha、新闻、情绪分析和价格数据  
- **使用搜索工具** — 通过关键词在档案中查找内容  
- **使用 `offset` 分页** — 大多数工具支持分页功能  
- **文件内容可能被截断** — 使用搜索工具查找文件中的特定部分  
- **使用 `since` 筛选最新数据** — 对文章、财报文本和新闻进行日期过滤  

## 错误处理

| 错误 | 处理方法 |
|-------|--------|
| “无数据可用” / “未找到文件” | 检查股票代码拼写；使用 `get_archive_stats` 检查数据覆盖范围 |
| 认证错误 | 检查 `ALPHAFACTORYX_MCP_TOKEN` 环境变量 |
| 请求限制（429） | 等待片刻后重试；考虑升级 tier |
| 文本被截断 | 使用搜索工具查找特定部分 |
| 网络超时 | 确认 https://mcp.alphafactoryx.com/mcp 是否可访问 |

## 数据覆盖范围

- 约2,000只美国股票（包括股票和ETF）
- SEC EDGAR：10-K、10-Q、8-K文件及Form 4文件（全文）
- Seeking Alpha：文章、财报电话会议记录、评级、财务数据、股息信息  
- Stock News：带有Grok、DeepSeek和GPT-5情感分析的新闻文章  
- Polygon News：带有每只股票AI情感分析的新闻文章  
- X/Twitter：约50只股票的推文（非全部2000只股票）  
- FRED：25个宏观经济指标（联邦基金利率、CPI、GDP、失业率、VIX、收益率曲线等）  
- OHLCV：约2000只股票及6种期货（ES、NQ、YM、RTY、GC、CL）的每日/每小时/每分钟价格数据