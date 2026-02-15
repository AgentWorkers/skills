---
name: openclaw-search
description: "智能代理搜索功能：通过统一API实现多源数据检索，并提供置信度评分。支持从网络、学术资源以及Tavily平台获取信息。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw 搜索 🔍

**专为自主代理设计的智能搜索工具，由 AIsa 提供支持。**

**仅需一个 API 密钥，即可实现多源信息检索，并获得带有置信度评分的搜索结果。**

> 受 [AIsa Verity](https://github.com/AIsa-team/verity) 的启发——这是一个具备置信度评分功能的下一代搜索代理。

## 🔥 您可以使用 OpenClaw 进行哪些操作？

### 研究助手
```
"Search for the latest papers on transformer architectures from 2024-2025"
```

### 市场研究
```
"Find all web articles about AI startup funding in Q4 2025"
```

### 竞争分析
```
"Search for reviews and comparisons of RAG frameworks"
```

### 新闻聚合
```
"Get the latest news about quantum computing breakthroughs"
```

### 深度研究
```
"Smart search combining web and academic sources on 'autonomous agents'"
```

## 快速入门
```bash
export AISA_API_KEY="your-key"
```

---

## 🏗️ 架构：多阶段协调机制

OpenClaw 搜索采用 **两阶段检索策略** 来提供全面的结果：

### 第一阶段：发现（并行检索）

同时查询 4 个不同的搜索源：
- **Scholar**：深度学术检索
- **Web**：结构化网页搜索
- **Smart**：智能混合模式搜索
- **Tavily**：外部验证数据

### 第二阶段：推理（元分析）

使用 **AIsa Explain** 对搜索结果进行元分析，生成：
- 置信度评分（0-100 分）
- 来源一致性分析
- 综合性答案

```
┌─────────────────────────────────────────────────────────────┐
│                      User Query                              │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌─────────┐     ┌─────────┐     ┌─────────┐
        │ Scholar │     │   Web   │     │  Smart  │
        └─────────┘     └─────────┘     └─────────┘
              │               │               │
              └───────────────┼───────────────┘
                              ▼
                    ┌─────────────────┐
                    │  AIsa Explain   │
                    │ (Meta-Analysis) │
                    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Confidence Score│
                    │  + Synthesis    │
                    └─────────────────┘
```

---

## 核心功能

### 网页搜索
```bash
# Basic web search
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/web?query=AI+frameworks&max_num_results=10" \
  -H "Authorization: Bearer $AISA_API_KEY"

# Full text search (with page content)
curl -X POST "https://api.aisa.one/apis/v1/search/full?query=latest+AI+news&max_num_results=10" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 学术/科研搜索
```bash
# Search academic papers
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/scholar?query=transformer+models&max_num_results=10" \
  -H "Authorization: Bearer $AISA_API_KEY"

# With year filter
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/scholar?query=LLM&max_num_results=10&as_ylo=2024&as_yhi=2025" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### 智能搜索（网页 + 学术结合）
```bash
# Intelligent hybrid search
curl -X POST "https://api.aisa.one/apis/v1/scholar/search/smart?query=machine+learning+optimization&max_num_results=10" \
  -H "Authorization: Bearer $AISA_API_KEY"
```

### Tavily 集成（高级功能）
```bash
# Tavily search
curl -X POST "https://api.aisa.one/apis/v1/tavily/search" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"latest AI developments"}'

# Extract content from URLs
curl -X POST "https://api.aisa.one/apis/v1/tavily/extract" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"urls":["https://example.com/article"]}'

# Crawl web pages
curl -X POST "https://api.aisa.one/apis/v1/tavily/crawl" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","max_depth":2}'

# Site map
curl -X POST "https://api.aisa.one/apis/v1/tavily/map" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

### 解释搜索结果（元分析）
```bash
# Generate explanations with confidence scoring
curl -X POST "https://api.aisa.one/apis/v1/scholar/explain" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"results":[...],"language":"en","format":"summary"}'
```

---

## 📊 置信度评分引擎

与传统的 RAG（检索、聚合、解释）系统不同，OpenClaw 搜索会评估信息来源的可信度和一致性：

### 评分标准

| 因素        | 权重    | 描述                          |
|-------------|--------|--------------------------------------------|
| **来源质量**     | 40%    | 学术来源 > 智能/网页来源 > 外部来源                |
| **一致性分析**    | 35%    | 跨来源的一致性检查                    |
| **时效性**     | 15%    | 更新较新的来源会被赋予更高权重                 |
| **相关性**     | 10%    | 查询内容与搜索结果的语义匹配度                    |

### 评分解读

| 评分        | 置信度水平 | 含义                          |
|------------|---------|--------------------------------------------|
| 90-100       | 非常高   | 学术和网页来源之间存在高度一致                |
| 70-89       | 高      | 来源之间有较好的一致性，来源可靠                |
| 50-69       | 中等      | 来源信息混合，需要独立验证                 |
| 30-49       | 低      | 来源之间存在矛盾，使用时需谨慎                 |
| 0-29       | 非常低   | 数据不足或相互矛盾                     |

---

## Python 客户端
```bash
# Web search
python3 {baseDir}/scripts/search_client.py web --query "latest AI news" --count 10

# Academic search
python3 {baseDir}/scripts/search_client.py scholar --query "transformer architecture" --count 10
python3 {baseDir}/scripts/search_client.py scholar --query "LLM" --year-from 2024 --year-to 2025

# Smart search (web + academic)
python3 {baseDir}/scripts/search_client.py smart --query "autonomous agents" --count 10

# Full text search
python3 {baseDir}/scripts/search_client.py full --query "AI startup funding"

# Tavily operations
python3 {baseDir}/scripts/search_client.py tavily-search --query "AI developments"
python3 {baseDir}/scripts/search_client.py tavily-extract --urls "https://example.com/article"

# Multi-source search with confidence scoring
python3 {baseDir}/scripts/search_client.py verity --query "Is quantum computing ready for enterprise?"
```

---

## API 端点参考

| 端点        | 方法      | 描述                          |
|-------------|---------|--------------------------------------------|
| /scholar/search/web | POST     | 结构化网页搜索                     |
| /scholar/search/scholar | POST     | 学术论文搜索                     |
| /scholar/search/smart | POST     | 智能混合模式搜索                     |
| /scholar/explain | POST     | 生成搜索结果解释                     |
| /search/full    | POST     | 全文搜索（包含内容）                    |
| /search/smart   | POST     | 智能网页搜索                     |
| /tavily/search  | POST     | 集成 Tavily 搜索功能                 |
| /tavily/extract   | POST     | 从 URL 中提取内容                     |
| /tavily/crawl   | POST     | 爬取网页                         |
| /tavily/map    | POST     | 生成站点地图                     |

---

## 搜索参数

| 参数        | 类型      | 描述                          |
|-------------|---------|--------------------------------------------|
| query       | string    | 搜索查询（必填）                      |
| max_num_results | integer | 最大搜索结果数量（1-100，默认为 10）             |
| as_ylo       | integer | 年份下限（仅适用于学术搜索）                |
| as_yhi       | integer | 年份上限（仅适用于学术搜索）                |

---

## 🚀 构建自己的置信度评分搜索代理

想要自己构建一个具备置信度评分功能的搜索代理吗？以下是实现步骤：

### 1. 并行检索
```python
import asyncio

async def discover(query):
    """Phase 1: Parallel retrieval from multiple sources."""
    tasks = [
        search_scholar(query),
        search_web(query),
        search_smart(query),
        search_tavily(query)
    ]
    results = await asyncio.gather(*tasks)
    return {
        "scholar": results[0],
        "web": results[1],
        "smart": results[2],
        "tavily": results[3]
    }
```

### 2. 置信度评分
```python
def score_confidence(results):
    """Calculate deterministic confidence score."""
    score = 0
    
    # Source quality (40%)
    if results["scholar"]:
        score += 40 * len(results["scholar"]) / 10
    
    # Agreement analysis (35%)
    claims = extract_claims(results)
    agreement = analyze_agreement(claims)
    score += 35 * agreement
    
    # Recency (15%)
    recency = calculate_recency(results)
    score += 15 * recency
    
    # Relevance (10%)
    relevance = calculate_relevance(results, query)
    score += 10 * relevance
    
    return min(100, score)
```

### 结果合成
```python
async def synthesize(query, results, score):
    """Generate final answer with citations."""
    explanation = await explain_results(results)
    return {
        "answer": explanation["summary"],
        "confidence": score,
        "sources": explanation["citations"],
        "claims": explanation["claims"]
    }
```

有关完整实现方式，请参考 [AIsa Verity](https://github.com/AIsa-team/verity)。

---

## 价格信息

| API        | 费用        |
|------------|------------|
| 网页搜索     | 约 0.001 美元/次                |
| 学术搜索     | 约 0.002 美元/次                |
| 智能搜索     | 约 0.002 美元/次                |
| Tavily 搜索   | 约 0.002 美元/次                |
| 结果解释     | 约 0.003 美元/次                |

每个搜索结果都会包含 `usage.cost` 和 `usage.credits_remaining` 字段。

---

## 开始使用

1. 在 [aisa.one](https://aisa.one) 注册账号
2. 获取您的 API 密钥
3. 购买信用额度（按需付费）
4. 设置环境变量：`export AISA_API_KEY="your-key"`

## 完整 API 参考

请访问 [API 参考文档](https://aisa.mintlify.app/api-reference/introduction) 以获取完整的端点说明。

## 资源链接

- [AIsa Verity](https://github.com/AIsa-team/verity) - 具有置信度评分功能的搜索代理参考实现
- [AIsa 文档](https://aisa.mintlify.app) - 完整的 API 文档