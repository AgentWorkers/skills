---
name: dappier
description: 启用快速、免费的实时网络搜索功能，并访问来自可信媒体品牌的优质数据——包括新闻、金融市场、体育、娱乐、天气等信息。使用 Dappier 构建强大的 AI 代理程序。
homepage: https://dappier.com
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["node"],"env":["DAPPIER_API_KEY"]},"primaryEnv":"DAPPIER_API_KEY"}}
---
# Dappier

Dappier 提供快速、免费的实时网络搜索功能，并可访问来自知名媒体品牌的优质数据，涵盖新闻、金融市场、体育、娱乐、天气等领域。您还可以利用 Dappier 构建强大的 AI 应用程序。

## 工具

### 1. 实时搜索

支持实时网络搜索，可获取最新的新闻、股票信息、黄金价格、英国股市行情、全球市场动态、财经新闻、天气信息、旅行资讯等。

```bash
node {baseDir}/scripts/realtime-search.mjs "query"
```

**示例：**

```bash
node {baseDir}/scripts/realtime-search.mjs "latest news today"
node {baseDir}/scripts/realtime-search.mjs "weather in New York today"
node {baseDir}/scripts/realtime-search.mjs "best travel deals this week"
node {baseDir}/scripts/realtime-search.mjs "gold price today"
```

### 2. 股票市场数据

仅当用户查询需要实时财经新闻、股票价格或交易数据时使用此功能。查询时必须包含股票代码（例如：AAPL、TSLA、MSFT、GOOGL），才能获取实时股票价格、财经新闻或市场数据。

```bash
node {baseDir}/scripts/stock-market.mjs "query with ticker symbol"
```

**示例：**

```bash
node {baseDir}/scripts/stock-market.mjs "AAPL stock price today"
node {baseDir}/scripts/stock-market.mjs "TSLA latest financial news"
node {baseDir}/scripts/stock-market.mjs "MSFT earnings report"
node {baseDir}/scripts/stock-market.mjs "GOOGL revenue growth"
node {baseDir}/scripts/stock-market.mjs "AMZN market cap"
```

### 3. 体育新闻

提供基于 AI 的体育新闻推荐服务，可获取来自 Sportsnaut、Forever Blueshirts、Minnesota Sports Fan、LAFB Network、Bounding Into Sports 和 Ringside Intel 等知名体育媒体的实时新闻、更新内容及个性化内容。

```bash
node {baseDir}/scripts/sports-news.mjs "query"
node {baseDir}/scripts/sports-news.mjs "query" --top_k 5
node {baseDir}/scripts/sports-news.mjs "query" --algorithm trending
```

**选项：**
- `--top_k <数量>`：显示结果的数量（默认值：9）
- `--algorithm <类型>`：搜索算法（默认值：`most_recent`、`semantic`、`most_recent_semantic` 或 `trending`）

**示例：**

```bash
node {baseDir}/scripts/sports-news.mjs "NFL playoff results"
node {baseDir}/scripts/sports-news.mjs "NBA trade rumors" --algorithm trending
node {baseDir}/scripts/sports-news.mjs "MLB scores today" --top_k 5
node {baseDir}/scripts/sports-news.mjs "Premier League standings"
node {baseDir}/scripts/sports-news.mjs "UFC fight results this week" --algorithm most_recent
```

### 4. Benzinga 财经新闻

可访问 Benzinga.com 的实时财经新闻。

**选项：**
- `--top_k <数量>`：显示结果的数量（默认值：9）
- `--algorithm <类型>`：搜索算法（默认值：`most_recent`、`semantic`、`most_recent_semantic` 或 `trending`）

**示例：**

```bash
node {baseDir}/scripts/benzinga-news.mjs "latest market news"
node {baseDir}/scripts/benzinga-news.mjs "NVDA news" --algorithm most_recent
node {baseDir}/scripts/benzinga-news.mjs "AAPL earnings" --top_k 5
node {baseDir}/scripts/benzinga-news.mjs "inflation report markets" --algorithm trending
```

### 5. 生活方式新闻

提供基于 AI 的生活方式新闻推荐服务，可获取来自 The Mix、Snipdaily、Nerdable 和 Familyproof 等主流生活方式媒体的最新资讯、分析内容。

**选项：**
- `--top_k <数量>`：显示结果的数量（默认值：9）
- `--algorithm <类型>`：搜索算法（默认值：`most_recent`、`semantic`、`most_recent_semantic` 或 `trending`）

**示例：**

```bash
node {baseDir}/scripts/lifestyle-news.mjs "query"
node {baseDir}/scripts/lifestyle-news.mjs "query" --top_k 5
node {baseDir}/scripts/lifestyle-news.mjs "query" --algorithm trending
```

### 6. 研究论文搜索

支持实时研究论文搜索，可即时获取超过 240 万篇开放获取的学术文章，涵盖物理学、数学、计算机科学、定量生物学、定量金融、统计学、电气工程与系统科学以及经济学等领域。

**示例：**

```bash
node {baseDir}/scripts/research-papers.mjs "transformer architecture original paper"
node {baseDir}/scripts/research-papers.mjs "recent arXiv papers on diffusion models"
node {baseDir}/scripts/research-papers.mjs "graph neural networks survey 2024"
```

### 7. Stellar AI（屋顶分析与太阳能建议）

只需提供住宅地址，即可获取专业的屋顶分析及太阳能板安装建议。该服务利用数字卫星图像（DSM）和太阳能辐射数据来精确估算能源需求。

**示例：**

```bash
node {baseDir}/scripts/stellar-ai.mjs "residential home address"
```

## 注意事项：
- 需要从 [https://platform.dappier.com/profile/api-keys](https://platform.dappier.com/profile/api-keys) 获取 `DAPPIER_API_KEY`。
- Dappier 提供来自知名媒体品牌的实时数据。
- 对于一般查询（如新闻、天气、旅行等），请使用 **实时搜索** 功能。
- 如需进行金融相关查询，请使用 **股票市场数据** 功能（需提供股票代码）。
- 对于体育相关查询，请使用 **体育新闻** 功能（返回包含标题、作者、来源和摘要的文章）。
- 对于财经新闻查询，请使用 **Benzinga 财经新闻** 功能（返回包含标题、来源和摘要的 Benzinga 文章）。
- 对于生活方式相关查询，请使用 **生活方式新闻** 功能（返回包含标题、来源和摘要的文章）。
- 对于学术研究查询，请使用 **研究论文搜索** 功能（返回基于开放获取论文的 AI 生成结果）。
- 如需了解特定住宅地址的太阳能安装可行性，请使用 **Stellar AI** 功能。