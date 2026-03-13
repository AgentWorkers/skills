---
name: stock-sentiment
description: "**美国股票研究的情绪分析与财务数据**  
本工具提供多引擎人工智能情绪分析（包括Grok、DeepSeek、GPT-5），以及2000多只股票的财报电话记录、社交媒体情绪数据、新闻洞察、FRED宏观经济指标和OHLCV价格等信息。适用于股票研究、情绪监测、文件分析或市场数据探索等场景。"
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

[![文档](https://img.shields.io/badge/Docs-Deep%20Dive-blue?logo=bookstack)](https://alphafactoryx.com/skills/stock-sentiment)

提供股票情绪分析及美国股票研究工具。通过26个MCP工具，可以查询多引擎生成的AI情绪评分、美国证券交易委员会（SEC）的文件、分析师评级、财报文本、社交媒体情绪数据、宏观经济指标以及2000多只股票的价格信息。

## 参考资料

- `references/tools.md` — 全部工具的详细参考信息，包括参数和功能描述
- `references/workflows.md` — 逐步指导的研究工作流程（股票分析、情绪分析、宏观经济分析、深度搜索）

## 快速入门

无需任何令牌或注册。免费 tier 每个IP每天可发送20次请求。

**研究某只股票：**
```
mcp__alphafactoryx__analyst_overview(symbol="AAPL")
mcp__alphafactoryx__filing_latest(symbol="AAPL", form_type="10-K")
mcp__alphafactoryx__news_articles(symbol="AAPL")
mcp__alphafactoryx__kline(symbol="AAPL")
```

**在档案中搜索：**
```
mcp__alphafactoryx__filing_search(query="revenue guidance", symbol="AAPL")
mcp__alphafactoryx__analyst_search(query="AI chips")
mcp__alphafactoryx__analyst_transcript_search(query="margin expansion")
```

**查看股票情绪：**
```
mcp__alphafactoryx__news_articles(symbol="AAPL")
mcp__alphafactoryx__market_news_articles(symbol="AAPL")
mcp__alphafactoryx__social(symbol="AAPL")
```

**获取宏观经济数据：**
```
mcp__alphafactoryx__fred_macro()
```

## 工具分类

| 分类 | 工具 | 主要功能 |
|------|-------|-----------------|
| 文件 | 5 | 10-K、10-Q、8-K报表以及Form 4文件；全文搜索 |
| 分析师 | 10 | 文章、新闻、财报文本、分析师评级、财务数据、评论 |
| 新闻 | 2 | 带有Grok、DeepSeek和GPT-5情感分析功能的新闻文章 |
| 市场新闻 | 2 | 带有每只股票AI情感分析的新闻 |
| 社交媒体 | 3 | 根据互动次数排序的推文、筛选后的帖子、高互动量的话题 |
| FRED宏观经济数据 | 2 | 25个宏观经济指标（利率、CPI、GDP、VIX、收益率曲线） |
| 开盘价、最高价、最低价、成交量、收盘价 | 2 | 每只股票的日/小时/1分钟价格走势 |

## 认证

**免费 tier（无需设置）**：每天20次请求，每秒1次请求。只需连接即可使用。

**付费 tier：** 在您的环境变量中设置 `ALPHAFACTORYX_MCP_TOKEN`：

| Tier | 每日请求量 | 费率 | 价格 |
|------|-------|------|-------|
| 免费 | 20 | 1次/秒 | $0 |
| 入门级 | 200 | 2次/秒 | $29/月 |
| 专业级 | 2,000 | 5次/秒 | $99/月 |
| 企业级 | 10,000 | 10次/秒 | 从$299/月起 |

详情请访问 [alphafactoryx.com/pricing](https://alphafactoryx.com/pricing)。

## 最佳实践

- **交叉引用数据来源** — 结合EDGAR、SA、新闻、情绪数据和价格数据进行分析
- **使用搜索工具** — 通过关键词在档案中查找所需内容
- **使用 `offset` 分页** — 大多数工具支持使用 `offset` 对结果进行分页
- **文件内容可能被截断** — 使用搜索工具查找长文件中的特定部分
- **使用 `since` 筛选最新数据** — 对文章、财报文本和新闻进行日期过滤

## 错误处理

| 错误类型 | 处理方法 |
|-------|--------|
| “无可用数据” / “未找到文件” | 检查股票代码的拼写；尝试使用 `analyst_overview` 验证数据覆盖范围 |
| 认证错误 | 检查环境变量 `ALPHAFACTORYX_MCP_TOKEN` 是否设置正确 |
| 请求速率限制（429） | 等待片刻后重试；考虑升级服务等级 |
| 文本被截断 | 使用搜索工具查找所需内容 |
| 网络超时 | 确保可以访问 https://mcp.alphafactoryx.com/mcp |

## 数据覆盖范围

- 约2,000只美国股票（包括股票和ETF）
- 文件数据：10-K、10-Q、8-K报表以及Form 4文件（全文）
- 分析师数据：文章、财报电话会议记录、评级、财务数据、股息信息、分析师预测
- 新闻数据：带有Grok、DeepSeek和GPT-5情感分析功能的新闻文章
- 市场新闻：带有每只股票AI情感分析的新闻文章
- 社交媒体数据：约50只股票的推文互动数据（非全部2000只股票）
- FRED宏观经济数据：25个宏观经济指标（联邦基金利率、CPI、GDP、失业率、VIX、收益率曲线等）
- 开盘价、最高价、最低价、成交量、收盘价数据：约2000只股票及6种期货合约（ES、NQ、YM、RTY、GC、CL）的日/小时/1分钟价格走势