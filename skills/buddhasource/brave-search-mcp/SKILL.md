---
name: brave-search-mcp
description: Brave Search 的官方 MCP（Media Center Platform）服务器，支持网页搜索、图片搜索、新闻搜索、视频搜索以及本地兴趣点（POI）搜索功能。该搜索 API 以隐私保护为核心设计，并配备了人工智能驱动的摘要生成功能。它将 AI 功能与全面的搜索能力相结合，且不依赖 Google 的数据追踪服务。用户可以通过该平台进行网页浏览、资料研究、事实核查以及内容发现等操作。无论是需要在网上搜索信息、查找最新数据、研究特定主题、验证事实，还是查找图片/视频，或是定位企业/地点，Brave Search 都能提供强大的支持。
---

# Brave Search MCP 服务器

> **以隐私为先的 AI 搜索工具**

Brave 官方提供的 MCP 服务器，集成了 [Brave Search API](https://brave.com/search/api/)。该服务器提供全面的搜索功能，包括网页、图片、视频、新闻以及本地兴趣点的搜索，并支持 AI 驱动的摘要生成。

## 为什么选择 Brave Search？

### 🔒 以隐私为核心
Brave Search 不会跟踪用户行为、不生成用户画像，也不会监控用户的搜索历史记录。与 Google 不同，Brave Search 不会收集用户的个人信息或行为数据。

### 🤖 兼容 AI 的功能
- **AI 驱动的摘要生成**：利用 AI 为搜索结果生成简洁的摘要。
- **结构化的数据**：为相关应用提供易于处理的数据格式。
- **丰富的搜索结果上下文**：提供更详细的背景信息。

### 🌐 全面的搜索范围
- **网页搜索**：通用的互联网搜索服务。
- **图片搜索**：发现视觉内容。
- **视频搜索**：来自多个平台的视频资源。
- **新闻搜索**：实时新闻和新闻报道。
- **本地兴趣点**：查找用户所在位置附近的商家、餐厅和服务。

## 安装

```bash
# Official Brave Search MCP Server
npm install -g @brave/brave-search-mcp-server

# Or via GitHub
git clone https://github.com/brave/brave-search-mcp-server
cd brave-search-mcp-server
npm install
npm run build
```

## 配置

将以下配置添加到您的 MCP 客户端配置文件中：

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@brave/brave-search-mcp-server"],
      "env": {
        "BRAVE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### 获取 API 密钥

1. 访问 https://brave.com/search/api/
2. 注册 Brave Search API 账户。
3. 免费套餐：每月 2,000 次查询。
4. 高流量套餐可供选择。

## 可用的工具

### 1. 网页搜索 (`brave_web_search`)

通用互联网搜索工具。

**代理使用方式：**
```
"Search for recent developments in quantum computing"
"Find tutorials on React hooks"
"What are the best practices for Docker security?"
```

**参数：**
- `query`（必填）：搜索关键词。
- `count`（可选）：结果数量（默认 10 个，最多 20 个）。
- `offset`（可选）：分页偏移量。

### 2. 本地搜索 (`brave_local_search`)

查找用户所在位置附近的商家、餐厅和服务。

**代理使用方式：**
```
"Find coffee shops near San Francisco"
"Pizza restaurants in Brooklyn"
"Gas stations near Times Square"
```

**参数：**
- `query`（必填）：搜索内容。
- `location`（可选）：城市、地址或坐标。

### 3. 图片搜索 (`brave_image_search`)

用于发现视觉内容。

**代理使用方式：**
```
"Find images of the Golden Gate Bridge"
"Product photography for smartphones"
"Infographics about climate change"
```

### 4. 视频搜索 (`brave_video_search`)

搜索来自 YouTube、Vimeo 等平台的视频内容。

**代理使用方式：**
```
"Tutorial videos on machine learning"
"Keynotes from recent tech conferences"
"Documentary about space exploration"
```

### 5. 新闻搜索 (`brave_news_search`)

提供实时新闻和新闻报道。

**代理使用方式：**
```
"Latest news about AI regulation"
"Recent developments in renewable energy"
"Tech industry news this week"
```

### 6. 摘要生成器 (`brave_web_search` with summarizer`)

为搜索结果生成 AI 驱动的摘要。

**代理使用方式：**
```
"Summarize current state of quantum computing research"
"Give me a summary of recent climate policy changes"
```

## 代理的应用场景

### 研究助手
```
Agent: "What are the latest findings on CRISPR gene editing?"
Brave Search: Returns recent articles, papers, news with summary
```

### 事实核查
```
Agent: "Is it true that coffee improves cognitive function?"
Brave Search: Provides sources, studies, verification
```

### 本地信息探索
```
Agent: "Find highly-rated sushi restaurants in Seattle"
Brave Search: Returns businesses with ratings, addresses, hours
```

### 内容发现
```
Agent: "Find video tutorials on Kubernetes deployment"
Brave Search: Returns relevant videos from multiple platforms
```

### 新闻监控
```
Agent: "What's happening with Tesla this week?"
Brave Search: Recent news articles, announcements, coverage
```

## 代理工作流程示例

```
Human: "I'm planning a trip to Tokyo. Help me prepare."

Agent:
1. brave_web_search("Tokyo travel guide 2026")
2. brave_web_search("Tokyo weather forecast")
3. brave_local_search("best ramen restaurants Tokyo")
4. brave_image_search("Tokyo metro map")
5. brave_news_search("Tokyo events 2026")

Agent: "Here's your Tokyo trip prep:
- Weather: [from search results]
- Top ramen spots: [from local search]
- Metro map: [image links]
- Current events: [from news search]"
```

## 与 Google Search 的对比

| 功能 | Brave Search | Google Search |
|---------|--------------|---------------|
| **隐私保护** | ✅ 无数据追踪 | ❌ 大规模数据追踪 |
| **AI 摘要** | ✅ 内置功能 | ⚠️ 功能有限 |
| **API 使用成本** | ✅ 免费（每月 2,000 次查询） | ❌ 费用较高 |
| **搜索速度** | ✅ 快速 | ✅ 快速 |
| **搜索范围** | ✅ 独立索引 | ✅ 全面覆盖 |
| **对代理的友好程度** | ✅ 提供结构化数据 | ⚠️ 数据格式有限 |

## 使用限制

**免费套餐：**
- 每月 2,000 次查询。
- 每秒 1 次查询请求。
- 支持网页、图片、视频和新闻搜索。

**高级套餐：**
- 提供更高的搜索量。
- 提供专属技术支持。
- 详情请参阅：https://brave.com/search/api/

## 隐私保障

Brave 宣称：
> “Brave Search 不会收集个人数据、不生成用户画像，也不会追踪用户的搜索记录。您的搜索请求是匿名的。”

## 相关资源

- **官方 MCP 服务器**：https://github.com/brave/brave-search-mcp-server
- **API 文档**：https://brave.com/search/api/
- **API 密钥注册**：https://brave.com/search/api/
- **Brave Search 官网**：https://search.brave.com

## 高级配置选项

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "node",
      "args": ["/path/to/brave-search-mcp-server/build/index.js"],
      "env": {
        "BRAVE_API_KEY": "YOUR_API_KEY",
        "DEFAULT_COUNT": "15",
        "ENABLE_SUMMARIZER": "true"
      }
    }
  }
}
```

---

**这款搜索工具是每个代理程序都需要的选择**：以隐私为核心，兼容 AI 技术，覆盖范围广泛。只需安装一次，即可永久使用。