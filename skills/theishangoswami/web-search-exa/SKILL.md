---
name: web-search-exa
description: "神经网络驱动的网页搜索、内容提取、公司及人物信息查询、代码查找，以及通过 Exa MCP 服务器进行的深度数据分析。适用于以下场景：  
(1) 基于语义理解的网页搜索（而不仅仅是关键词搜索）；  
(2) 查找研究论文、新闻、推文、公司或个人信息；  
(3) 从 URL 中提取干净、可用的内容；  
(4) 找到与已知 URL 在语义上相似的网页；  
(5) 获取代码示例及相关文档；  
(6) 进行复杂的多步骤研究并生成报告；  
(7) 快速获取带有引用信息的综合答案。  
**不适用场景**：  
- 本地文件操作；  
- 非网页相关的任务；  
- 任何不涉及网页搜索或内容检索的场景。"
---
# Exa — 神经网络搜索与研究工具

Exa 是一款基于神经网络的搜索引擎。与传统的关键词搜索不同，它能够理解用户的需求和页面的含义——用户只需描述所需页面的内容，Exa 就能找到它。它返回的内容经过清洗处理，可以直接用于大型语言模型（LLM），无需进行任何数据抓取操作。

**MCP 服务器：** `https://mcp.exa.ai/mcp`  
**免费 tier：** 提供丰富的速率限制；基本功能无需 API 密钥  
**API 密钥：** [dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys) — 可解锁更多功能及所有工具  
**文档：** [exa.ai/docs](https://exa.ai/docs)  
**GitHub：** [github.com/exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server)

## 设置

将 MCP 服务器添加到您的代理配置中：

```bash
# OpenClaw
openclaw mcp add exa --url "https://mcp.exa.ai/mcp"
```

或在任何 MCP 配置 JSON 文件中添加如下内容：
```json
{
  "mcpServers": {
    "exa": {
      "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```

若要解锁所有工具并解除速率限制，请添加您的 API 密钥：
```
https://mcp.exa.ai/mcp?exaApiKey=YOUR_EXA_KEY
```

若要启用特定的可选工具，请根据需要配置相关参数：
```
https://mcp.exa.ai/mcp?exaApiKey=YOUR_KEY&tools=web_search_exa,web_search_advanced_exa,people_search_exa,crawling_exa,company_research_exa,get_code_context_exa,deep_researcher_start,deep_researcher_check,deep_search_exa
```

---

## 工具参考

### 默认工具（无需 API 密钥即可使用）

| 工具 | 功能 |
|------|-------------|
| `web_search_exa` | 通用网页搜索——返回内容清晰、速度较快 |
| `get_code_context_exa` | 从 GitHub、Stack Overflow 和官方文档中检索代码示例及使用说明 |
| `company_research_exa` | 提供公司概况、新闻、融资信息和竞争对手信息 |

### 可选工具（需通过 `tools` 参数启用，部分工具需要 API 密钥）

| 工具 | 功能 |
|------|-------------|
| `web_search_advanced_exa` | 全功能搜索：支持域名过滤、日期范围设置、类别选择及内容提取模式 |
| `crawling_exa` | 从指定 URL 中提取完整页面内容——支持处理 JavaScript、PDF 文件及复杂页面布局 |
| `people_search_exa` | 查找 LinkedIn 用户资料、职业背景及专家信息 |
| `deep_researcher_start` | 启动异步多步骤研究任务并生成详细报告 |
| `deep_researcher_check` | 查询研究任务的进度或获取结果 |
| `deep_search_exa` | 单次调用即可进行深度搜索，返回带有引用信息的综合答案（需 API 密钥） |

---

## web_search_exa

快速通用搜索工具。用户只需用自然语言描述所需内容即可。

**参数：**
- `query` (字符串，必填) — 描述要查找的页面内容 |
- `numResults` (整数) — 返回结果数量，默认为 10 |
- `type` — `auto`（最佳质量）、`fast`（较低延迟）、`deep`（多步骤推理） |
- `livecrawl` — `fallback`（默认值）或 `preferred`（始终获取最新内容） |
- `contextMaxCharacters` (整数) — 限制返回内容的长度 |

```
web_search_exa {
  "query": "blog posts about using vector databases for recommendation systems",
  "numResults": 8
}
```

```
web_search_exa {
  "query": "latest OpenAI announcements March 2026",
  "numResults": 5,
  "type": "fast"
}
```

---

## web_search_advanced_exa

高级搜索工具。具备 `web_search_exa` 的所有功能，同时支持域名过滤、日期过滤、类别选择及内容提取模式。

**额外参数：**

| 参数 | 类型 | 功能 |
|-----------|------|-------------|
| `includeDomains` | 字符串数组 | 仅返回指定域名的结果（最多 1200 个） |
| `excludeDomains` | 字符串数组 | 阻止来自指定域名的结果 |
| `category` | 字符串 | 目标内容类型（详见下表） |
| `startPublishedDate` | 字符串 | 结果的发布日期（ISO 格式） |
| `endPublishedDate` | 字符串 | 结果的发布日期（ISO 格式） |
| `maxAgeHours` | 整数 | 内容更新频率：`0` 表示始终获取最新内容；`-1` 表示仅使用缓存；`24` 表示仅缓存 24 小时内的内容 |
| `contents.highlights` | 对象 | 与查询相关的摘录内容；通过设置 `maxCharacters` 来控制摘录长度 |
| `contents.text` | 对象 | 完整页面内容（以 Markdown 格式返回）；通过设置 `maxCharacters` 来控制内容长度 |
| `contents.summary` | 对象 | 由大型语言模型生成的摘要；支持使用 `query` 或 JSON `schema` 进行结构化提取 |

**类别：**

| 类别 | 适用场景 |
|----------|---------|
| `company` | 公司页面、LinkedIn 公司资料 |
| `people` | LinkedIn 用户资料、个人简介 |
| `research_paper` | arXiv 存储库中的学术论文 |
| `news` | 最新新闻 |
| `tweet` | X/Twitter 上的帖子 |
| `personal_site` | 博客、个人网站 |
| `financial_report` | 证券交易委员会（SEC）文件、财务报告 |

### 示例

**检索学术论文：**
```
web_search_advanced_exa {
  "query": "transformer architecture improvements for long-context windows",
  "category": "research paper",
  "numResults": 15,
  "contents": { "highlights": { "maxCharacters": 3000 } }
}
```

**构建公司列表并提取结构化数据：**
```
web_search_advanced_exa {
  "query": "Series A B2B SaaS companies in climate tech founded after 2022",
  "category": "company",
  "numResults": 25,
  "contents": {
    "summary": {
      "query": "company name, what they do, funding stage, location",
      "schema": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "description": { "type": "string" },
          "funding": { "type": "string" },
          "location": { "type": "string" }
        }
      }
    }
  }
}
```

**查找具有特定资料的候选人：**
```
web_search_advanced_exa {
  "query": "machine learning engineers at fintech startups in NYC with experience in fraud detection",
  "category": "people",
  "numResults": 20,
  "contents": { "highlights": { "maxCharacters": 2000 } }
}
```

**查找与已知 URL 相似的页面：**
直接使用该 URL 作为查询参数，Exa 会找到语义上相似的页面：
```
web_search_advanced_exa {
  "query": "https://linkedin.com/in/some-candidate-profile",
  "numResults": 15,
  "contents": { "highlights": { "maxCharacters": 2000 } }
}
```

**控制更新频率的最新新闻：**
```
web_search_advanced_exa {
  "query": "AI regulation policy updates",
  "category": "news",
  "maxAgeHours": 72,
  "numResults": 10,
  "contents": { "highlights": { "maxCharacters": 4000 } }
}
```

**限定搜索范围：**
```
web_search_advanced_exa {
  "query": "authentication best practices",
  "includeDomains": ["owasp.org", "auth0.com", "docs.github.com"],
  "numResults": 10,
  "contents": { "text": { "maxCharacters": 5000 } }
}
```

---

## company_research_exa

一次查询即可获取公司信息，包括业务概况、最新新闻、融资情况以及竞争对手信息。

```
company_research_exa { "query": "Stripe payments company overview and recent news" }
```

```
company_research_exa { "query": "what does Anduril Industries do and who are their competitors" }
```

---

## people_search_exa

根据职位、公司、位置或专长查找专业人士。返回 LinkedIn 用户资料和简介。

```
people_search_exa { "query": "VP of Engineering at healthcare startups in San Francisco" }
```

```
people_search_exa { "query": "AI researchers specializing in multimodal models" }
```

---

## get_code_context_exa

从 GitHub 仓库、Stack Overflow 和官方文档中检索代码示例及 API 使用方式。

```
get_code_context_exa { "query": "how to implement rate limiting in Express.js with Redis" }
```

```
get_code_context_exa { "query": "Python asyncio connection pooling example with aiohttp" }
```

---

## crawling_exa

从指定 URL 中提取清晰的内容。支持处理 JavaScript 渲染的页面、PDF 文件及复杂页面布局。返回内容以 Markdown 格式呈现。

**适用场景：** 当您已经拥有目标 URL 且需要阅读页面内容时。

---

## deep_researcher_start + deep_researcher_check

异步执行长时间运行的研究任务。Exa 的研究引擎会进行搜索、读取数据并生成详细报告。

**启动研究任务：**
```
deep_researcher_start {
  "query": "competitive landscape of AI code generation tools in 2026 — key players, pricing, technical approaches, market share"
}
```

**查询任务状态：** 使用开始时的响应中的 `researchId` 进行查询：
```
deep_researcher_check { "researchId": "abc123..." }
```

持续调用 `deep_researcher_check` 直到任务状态变为 `completed`。最终响应将包含完整报告。

---

## deep_search_exa

单次调用即可进行深度搜索，从多个角度扩展查询结果，读取数据并返回带有引用信息的综合答案（需 API 密钥）。

**支持结构化输出：** 通过 `outputSchema` 参数进行配置：
```
deep_search_exa {
  "query": "top 10 aerospace companies by revenue",
  "type": "deep",
  "outputSchema": {
    "type": "object",
    "required": ["companies"],
    "properties": {
      "companies": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "revenue": { "type": "string" },
            "hq": { "type": "string" }
          }
        }
      }
    }
  }
}
```

---

## 查询技巧

Exa 是基于神经网络的搜索引擎，它根据内容的含义进行匹配，而非关键词。请像向同事描述理想页面一样编写查询语句。

**示例：**
- 正确的查询方式：`search for blog posts about using embeddings for product recommendations at scale`  
- 错误的查询方式：`search for embeddings product recommendations`  
- 推荐使用方式：`search for a fintech company called Stripe located in San Francisco`  
- 注意：避免使用过于模糊的查询词（如 `Stripe`）  

**使用建议：**
- 如果知道内容类型，请使用 `category` 参数进行精确搜索。  
- 为获得更全面的搜索结果，可以并行执行多个查询并去除重复结果。  
- 在自动化工作流程中，建议使用 `highlights` 而不是 `text`，这样可以节省大量计算资源。  

## 计算效率

| 内容提取方式 | 适用场景 |
|-------------|------------|
| `highlights` | 适用于自动化工作流程、事实性查询及多步骤处理流程——计算效率最高 |
| `text` | 适用于深度分析或需要完整页面上下文的情况 |
| `summary` | 适用于快速概览或需要结构化提取的情况（支持 JSON 格式） |

**设置 `maxCharacters` 可以控制输出内容的长度。**

## 根据需求选择合适的工具

| 需要完成的任务 | 使用的工具 |
|-------------|-----|
| 快速网页查询 | `web_search_exa` |
| 学术论文搜索 | `web_search_advanced_exa` + `category: "research paper"` |
| 公司信息、竞争分析 | `company_research_exa` 或 `web_search_advanced_exa` + `category: "company"` |
| 查找人员、候选人或专家 | `people_search_exa` 或 `web_search_advanced_exa` + `category: "people"` |
| 代码示例、API 文档 | `get_code_context_exa` |
| 阅读特定页面 | `crawling_exa` |
| 查找与已知 URL 相似的页面 | `web_search_advanced_exa` 并使用该 URL 作为查询参数 |
| 最新新闻/推文 | `deep_search_exa` + `category: "news"` 或 `category: "tweet"` + `maxAgeHours` |
| 详细研究报告 | `deep_researcher_start` → `deep_researcher_check` |
| 带有引用的快速答案 | `deep_search_exa` |

---

**更多信息：**  
文档：[exa.ai/docs](https://exa.ai/docs)  
**控制面板：** [dashboard.exa.ai](https://dashboard.exa.ai)  
**支持：** support@exa.ai