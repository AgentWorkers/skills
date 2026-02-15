---
name: newsapi-search
version: 1.0.0
description: 通过 NewsAPI 搜索新闻文章，并支持按时间窗口、来源、域名和语言进行过滤。
---

# NewsAPI搜索  
⏹ 快速设置请访问：https://openclawcli.forum  

通过[NewsAPI](https://newsapi.org)搜索5,000多个新闻来源。支持全面搜索文章（/everything）和实时获取头条新闻（/top-headlines）。  

## 快速入门  

```bash
# Basic search
node scripts/search.js "technology" --days 7

# Filter by quality sources
node scripts/search.js "technology" --sources bbc-news,reuters,al-jazeera-english

# Exclude low-quality domains
node scripts/search.js "technology" --exclude tmz.com,radaronline.com

# Breaking headlines
node scripts/search.js "technology" --headlines --country us

# List available sources
node scripts/sources.js --country us --category general
```  

## 设置  

将API密钥添加到`~/.openclaw/.env`文件中：  
```
NEWSAPI_KEY=your_api_key
```  

从https://newsapi.org获取API密钥（免费 tier：每天100次请求）  

## 端点  

### 全面搜索（Everything Search）  

可搜索数百万篇文章。  

**时间范围：**  
```bash
node scripts/search.js "query" --hours 24
node scripts/search.js "query" --days 7        # default
node scripts/search.js "query" --weeks 2
node scripts/search.js "query" --months 1
node scripts/search.js "query" --from 2026-01-01 --to 2026-01-31
```  

**筛选条件：**  
```bash
node scripts/search.js "query" --sources bbc-news,cnn           # max 20
node scripts/search.js "query" --domains nytimes.com,bbc.co.uk
node scripts/search.js "query" --exclude gossip-site.com
node scripts/search.js "query" --lang en                       # or 'any'
```  

**搜索字段：**  
```bash
node scripts/search.js "query" --title-only                    # title only
node scripts/search.js "query" --in title,description          # specific fields
```  

**高级查询语法：**  
- `"exact phrase"` — 精确匹配  
- `+musthave` — 必需包含的词  
- `-exclude` — 需要排除的词  
- `word1 AND word2` — 两者都必须包含  
- `word1 OR word2` — 两者中任意一个都可以  
- `(word1 OR word2) AND word3` — 组合条件  

**分页与排序：**  
```bash
node scripts/search.js "query" --page 2 --limit 20
node scripts/search.js "query" --sort relevancy      # default
node scripts/search.js "query" --sort date           # newest first
node scripts/search.js "query" --sort popularity
```  

### 实时头条新闻（Top Headlines）  

按国家或类别获取实时新闻。  

**类别：** `business`（商业）、`entertainment`（娱乐）、`general`（综合）、`health`（健康）、`science`（科学）、`sports`（体育）、`technology`（科技）  

**注意：** 在头条新闻模式下，不能同时使用`--country`/`--category`和`--sources`选项。  

### 列出新闻来源（List Sources）  
```bash
node scripts/sources.js                    # all sources
node scripts/sources.js --country us       # filter by country
node scripts/sources.js --category business
node scripts/sources.js --lang en
node scripts/sources.js --json             # JSON output
```  

## 高级用法  

有关完整参数参考，请参阅[references/api-reference.md](references/api-reference.md)。  
有关常见的工作流程和搜索模式，请参阅[references/examples.md](references/examples.md)。  

## 程序化API（Programmatic API）  
```javascript
const { searchEverything, searchHeadlines, getSources } = require('./scripts/search.js');

const results = await searchEverything('climate change', {
  timeWindow: { type: 'days', value: 7 },
  sources: 'bbc-news,reuters',
  excludeDomains: 'tmz.com',
  limit: 20
});

const headlines = await searchHeadlines('business', {
  country: 'us',
  category: 'business'
});
```  

## 免费 tier限制：  
- 每天100次请求  
- 每次请求最多返回100条结果  
- 归档内容延迟1个月才可查看  

## 输出格式：**  
返回结构化的JSON数据：  
```json
{
  "query": "technology",
  "endpoint": "everything",
  "totalResults": 64,
  "returnedResults": 10,
  "page": 1,
  "results": [
    {
      "title": "...",
      "url": "...",
      "source": "BBC News",
      "publishedAt": "2026-02-05T14:30:00Z",
      "description": "...",
      "content": "..."
    }
  ]
}
```