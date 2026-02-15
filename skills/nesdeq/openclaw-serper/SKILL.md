---
name: openclaw-serper
description: >
  Searches Google and extracts full page content from every result via trafilatura.
  Returns clean readable text, not just snippets.
  Use when the user needs web search, research, current events, news, factual lookups,
  product comparisons, technical documentation, or any question requiring up-to-date
  information from the internet.
license: MIT
compatibility: Requires Python 3, trafilatura (pip install trafilatura), and network access.
allowed-tools: Bash(python3:*)
metadata:
  author: nesdeq
  version: "3.1.1"
  tags: "search, web-search, serper, google, content-extraction"
---

# Serper

通过 Serper API 进行谷歌搜索。该 API 不仅会获取搜索结果，还会读取实际的网页内容，并利用 trafilatura 工具提取完整的文本信息（而不仅仅是网页片段）。因此，用户能够获得整篇文章的完整文本。

## 使用限制

该技能本身已经能够获取并提取网页的完整内容。请勿对 Serper 返回的 URL 使用 WebFetch、web_fetch、WebSearch 等工具或其他任何用于获取或浏览网页的工具。所需的所有信息都已包含在搜索结果中，无需再次进行额外的数据请求。

## 查询技巧

只需构建一个恰当的搜索查询即可。通常情况下，一个查询就足以满足需求。每次调用该技能都会返回多个包含完整页面内容的搜索结果——通过一个查询即可获得广泛的信息覆盖。无需通过多次搜索来“深入探索”某个主题，一个选择得当的查询（并使用正确的搜索模式）就足够了。

**最多允许两次调用**：  
- 如果用户的请求确实涉及两个不同的主题（例如“比较 X 与 Y”，此时需要分别进行两次搜索）；  
- 或者一次使用 `default` 模式，另一次使用 `current` 模式来获取不同方面的信息。  

**禁止以下操作：**  
- 用不同的表述重新执行相同的查询以“获取更多结果”；  
- 通过连续多次搜索来“深入挖掘”内容（因为网页本身已经包含了丰富的信息）；  
- 先执行一次搜索找到所需内容，然后再进行另一次搜索（因为应该直接阅读已获取到的内容）。

## 两种搜索模式

Serper 提供两种搜索模式，请根据查询内容选择合适的模式：  

### `default` — 通用搜索（所有时间范围内的结果）  
- 搜索所有时间范围内的谷歌网页内容，返回 **5 个结果**，每个结果都包含完整的页面文本。  
- 适用于：一般性问题、研究、操作指南、长期有效的内容、产品信息、技术文档、对比分析、教程等不随时间变化的主题。  

### `current` — 新闻和最新信息  
- 搜索过去一周内的谷歌网页内容（3 个结果）以及谷歌新闻（3 个结果），每个结果都包含完整的页面文本。  
- 适用于：新闻、时事、最新动态、公告等时效性强的内容。  

## 模式选择指南  

| 查询关键词 | 使用模式 |  
|-------------|---------|  
| “X 是如何工作的？”、“X 是什么？”、“解释 X” | `default` |  
| 产品研究、对比分析、教程 | `default` |  
| 技术文档、指南 | `default` |  
| 历史性主题、长期有效的内容 | `default` |  
| “新闻”、“最新”、“本周”、“最近” | `current` |  
| “发生了什么”、“突发新闻”、“公告”、“发布” | `current` |  
| 时事、政治、体育比分、股票价格 | `current` |  

## 地区设置  

**默认设置为全球范围**（无国家筛选，返回英文结果）。但以下情况下必须设置地区参数：**  
- 用户的消息使用非英文语言；  
- 构建的搜索查询使用非英文语言；  
- 用户提到了特定的国家、城市或地区；  
- 用户要求获取特定地区的本地信息（如价格、新闻、商店等）。  

**如果用户使用德语输入查询，必须设置 `--gl de --hl de`。**  
（无例外情况。）  

| 情况 | 需要设置的参数 |  
|---------|---------|  
| 使用英文查询且无特定国家目标 | 不需要设置这些参数 |  
| 使用德语查询或用户使用德语输入 | `--gl de --hl de` |  
| 使用法语查询或用户使用法语输入 | `--gl fr --hl fr` |  
| 使用其他非英文语言或针对特定国家/地区 | `--gl XX --hl XX`（ISO 国家代码） |  

**经验法则：**  
如果查询字符串中包含非英文单词，务必设置 `--gl` 和 `--hl` 以匹配相应的语言。  

## 调用方式  

```bash
python3 scripts/search.py -q "QUERY" [--mode MODE] [--gl COUNTRY] [--hl LANG]
```  

### 示例  

```bash
# English, general research
python3 scripts/search.py -q "how does HTTPS work"

# English, time-sensitive
python3 scripts/search.py -q "OpenAI latest announcements" --mode current

# German query — set locale + current mode for news/prices
python3 scripts/search.py -q "aktuelle Preise iPhone" --mode current --gl de --hl de

# German news
python3 scripts/search.py -q "Nachrichten aus Berlin" --mode current --gl de --hl de

# French product research
python3 scripts/search.py -q "meilleur smartphone 2026" --gl fr --hl fr
```  

## 输出格式  

脚本会返回一个 JSON 数组。其中第一个元素是元数据，其余元素为包含完整提取内容的搜索结果：  

```json
[{"query": "...", "mode": "default", "locale": {"gl": "world", "hl": "en"}, "results": [{"title": "...", "url": "...", "source": "web"}]}
,{"title": "Page Title", "url": "https://example.com", "source": "web", "content": "Full extracted page text..."}
,{"title": "News Article", "url": "https://news.com", "source": "news", "date": "2 hours ago", "content": "Full article text..."}
]
```  

| 字段 | 描述 |  
|--------|---------|  
| `title` | 页面标题 |  
| `url` | 来源 URL |  
| `source` | `"web"`、`"news"` 或 `"knowledge_graph"` |  
| `content` | 完整提取的页面文本（如果提取失败则返回网页片段） |  
| `date` | 只有在新闻结果中提供（网页结果可能不提供） |  

## 命令行接口（CLI）参考  

| 参数 | 描述 |  
|--------|---------|  
| `-q, --query` | 搜索查询（必填） |  
| `-m, --mode` | `default`（所有时间范围内的结果，5 个）或 `current`（过去一周内的结果及新闻，各 3 个） |  
| `--gl` | 国家代码（如 `de`、`us`、`fr`、`at`、`ch`）；默认值：`world` |  
| `--hl` | 语言代码（如 `en`、`de`、`fr`）；默认值：`en` |  

## 特殊情况处理：**  
- 如果 trafilatura 无法从页面中提取内容，结果将回退为网页片段。  
- 有些网站会阻止爬虫访问，此时只能获取网页片段。  
- 如果没有返回任何结果，脚本会输出 `{"error": "未找到结果", "query": "..."}`。  
- Serper API 密钥存储在技能目录下的 `.env` 文件中；如果该文件缺失，脚本会提供设置说明并退出。