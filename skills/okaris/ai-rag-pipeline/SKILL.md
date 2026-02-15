---
name: ai-rag-pipeline
description: |
  Build RAG (Retrieval Augmented Generation) pipelines with web search and LLMs.
  Tools: Tavily Search, Exa Search, Exa Answer, Claude, GPT-4, Gemini via OpenRouter.
  Capabilities: research, fact-checking, grounded responses, knowledge retrieval.
  Use for: AI agents, research assistants, fact-checkers, knowledge bases.
  Triggers: rag, retrieval augmented generation, grounded ai, search and answer,
  research agent, fact checking, knowledge retrieval, ai research, search + llm,
  web grounded, perplexity alternative, ai with sources, citation, research pipeline
allowed-tools: Bash(infsh *)
---

# AI RAG 管道

您可以通过 [inference.sh](https://inference.sh) 命令行界面（CLI）来构建 RAG（Retrieval Augmented Generation，检索增强生成）管道。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Simple RAG: Search + LLM
SEARCH=$(infsh app run tavily/search-assistant --input '{"query": "latest AI developments 2024"}')
infsh app run openrouter/claude-sonnet-45 --input "{
  \"prompt\": \"Based on this research, summarize the key trends: $SEARCH\"
}"
```

## 什么是 RAG？

RAG 结合了以下三个步骤：
1. **检索**：从外部来源获取相关信息。
2. **增强**：将检索到的内容添加到问题提示中。
3. **生成**：大型语言模型（LLM）利用这些信息生成回答。

这种方式能够产生更准确、更及时且可验证的 AI 回答。

## RAG 管道模式

### 模式 1：简单搜索 + 回答

```
[User Query] -> [Web Search] -> [LLM with Context] -> [Answer]
```

### 模式 2：多源研究

```
[Query] -> [Multiple Searches] -> [Aggregate] -> [LLM Analysis] -> [Report]
```

### 模式 3：提取 + 处理

```
[URLs] -> [Content Extraction] -> [Chunking] -> [LLM Summary] -> [Output]
```

## 可用工具

### 搜索工具

| 工具 | 应用 ID | 适用场景 |
|------|--------|----------|
| Tavily Search | `tavily/search-assistant` | 基于 AI 的搜索工具，提供答案 |
| Exa Search | `exa/search` | 神经搜索，语义匹配 |
| Exa Answer | `exa/answer` | 直接提供事实性答案 |

### 提取工具

| 工具 | 应用 ID | 适用场景 |
|------|--------|----------|
| Tavily Extract | `tavily/extract` | 从 URL 中提取内容 |
| Exa Extract | `exa/extract` | 分析网页内容 |

### LLM 工具

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Claude Sonnet 4.5 | `openrouter/claude-sonnet-45` | 复杂数据分析 |
| Claude Haiku 4.5 | `openrouter/claude-haiku-45` | 快速处理 |
| GPT-4o | `openrouter/gpt-4o` | 通用型模型 |
| Gemini 2.5 Pro | `openrouter/gemini-25-pro` | 处理长篇文本 |

## 管道示例

### 基本 RAG 管道

```bash
# 1. Search for information
SEARCH_RESULT=$(infsh app run tavily/search-assistant --input '{
  "query": "What are the latest breakthroughs in quantum computing 2024?"
}')

# 2. Generate grounded response
infsh app run openrouter/claude-sonnet-45 --input "{
  \"prompt\": \"You are a research assistant. Based on the following search results, provide a comprehensive summary with citations.

Search Results:
$SEARCH_RESULT

Provide a well-structured summary with source citations.\"
}"
```

### 多源研究

```bash
# Search multiple sources
TAVILY=$(infsh app run tavily/search-assistant --input '{"query": "electric vehicle market trends 2024"}')
EXA=$(infsh app run exa/search --input '{"query": "EV market analysis latest reports"}')

# Combine and analyze
infsh app run openrouter/claude-sonnet-45 --input "{
  \"prompt\": \"Analyze these research results and identify common themes and contradictions.

Source 1 (Tavily):
$TAVILY

Source 2 (Exa):
$EXA

Provide a balanced analysis with sources.\"
}"
```

### URL 内容分析

```bash
# 1. Extract content from specific URLs
CONTENT=$(infsh app run tavily/extract --input '{
  "urls": [
    "https://example.com/research-paper",
    "https://example.com/industry-report"
  ]
}')

# 2. Analyze extracted content
infsh app run openrouter/claude-sonnet-45 --input "{
  \"prompt\": \"Analyze these documents and extract key insights:

$CONTENT

Provide:
1. Key findings
2. Data points
3. Recommendations\"
}"
```

### 事实核查管道

```bash
# Claim to verify
CLAIM="AI will replace 50% of jobs by 2030"

# 1. Search for evidence
EVIDENCE=$(infsh app run tavily/search-assistant --input "{
  \"query\": \"$CLAIM evidence studies research\"
}")

# 2. Verify claim
infsh app run openrouter/claude-sonnet-45 --input "{
  \"prompt\": \"Fact-check this claim: '$CLAIM'

Based on the following evidence:
$EVIDENCE

Provide:
1. Verdict (True/False/Partially True/Unverified)
2. Supporting evidence
3. Contradicting evidence
4. Sources\"
}"
```

### 研究报告生成器

```bash
TOPIC="Impact of generative AI on creative industries"

# 1. Initial research
OVERVIEW=$(infsh app run tavily/search-assistant --input "{\"query\": \"$TOPIC overview\"}")
STATISTICS=$(infsh app run exa/search --input "{\"query\": \"$TOPIC statistics data\"}")
OPINIONS=$(infsh app run tavily/search-assistant --input "{\"query\": \"$TOPIC expert opinions\"}")

# 2. Generate comprehensive report
infsh app run openrouter/claude-sonnet-45 --input "{
  \"prompt\": \"Generate a comprehensive research report on: $TOPIC

Research Data:
== Overview ==
$OVERVIEW

== Statistics ==
$STATISTICS

== Expert Opinions ==
$OPINIONS

Format as a professional report with:
- Executive Summary
- Key Findings
- Data Analysis
- Expert Perspectives
- Conclusion
- Sources\"
}"
```

### 带有来源的快速回答

```bash
# Use Exa Answer for direct factual questions
infsh app run exa/answer --input '{
  "question": "What is the current market cap of NVIDIA?"
}'
```

## 最佳实践

### 1. 查询优化

```bash
# Bad: Too vague
"AI news"

# Good: Specific and contextual
"latest developments in large language models January 2024"
```

### 2. 上下文管理

```bash
# Summarize long search results before sending to LLM
SEARCH=$(infsh app run tavily/search-assistant --input '{"query": "..."}')

# If too long, summarize first
SUMMARY=$(infsh app run openrouter/claude-haiku-45 --input "{
  \"prompt\": \"Summarize these search results in bullet points: $SEARCH\"
}")

# Then use summary for analysis
infsh app run openrouter/claude-sonnet-45 --input "{
  \"prompt\": \"Based on this research summary, provide insights: $SUMMARY\"
}"
```

### 3. 来源标注

始终要求 LLM 引用其使用的信息来源：

```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "... Always cite sources in [Source Name](URL) format."
}'
```

### 4. 迭代研究

```bash
# First pass: broad search
INITIAL=$(infsh app run tavily/search-assistant --input '{"query": "topic overview"}')

# Second pass: dive deeper based on findings
DEEP=$(infsh app run tavily/search-assistant --input '{"query": "specific aspect from initial search"}')
```

## 管道模板

### 代理研究工具

```bash
#!/bin/bash
# research.sh - Reusable research function

research() {
  local query="$1"

  # Search
  local results=$(infsh app run tavily/search-assistant --input "{\"query\": \"$query\"}")

  # Analyze
  infsh app run openrouter/claude-haiku-45 --input "{
    \"prompt\": \"Summarize: $results\"
  }"
}

research "your query here"
```

## 相关技能

```bash
# Web search tools
npx skills add inference-sh/agent-skills@web-search

# LLM models
npx skills add inference-sh/agent-skills@llm-models

# Content pipelines
npx skills add inference-sh/agent-skills@ai-content-pipeline

# Full platform skill
npx skills add inference-sh/agent-skills@inference-sh
```

查看所有工具：`infsh app list`

## 文档

- [将工具添加到代理中](https://inference.sh/docs/agents/adding-tools) - 代理工具集成指南
- [构建研究代理](https://inference.sh/blog/guides/research-agent) - 完整指南