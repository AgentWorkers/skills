---
name: web-search
description: |
  Web search and content extraction with Tavily and Exa via inference.sh CLI.
  Apps: Tavily Search, Tavily Extract, Exa Search, Exa Answer, Exa Extract.
  Capabilities: AI-powered search, content extraction, direct answers, research.
  Use for: research, RAG pipelines, fact-checking, content aggregation, agents.
  Triggers: web search, tavily, exa, search api, content extraction, research,
  internet search, ai search, search assistant, web scraping, rag, perplexity alternative
allowed-tools: Bash(infsh *)
---

# 网页搜索与内容提取

您可以使用 [inference.sh](https://inference.sh) 命令行工具在网页上搜索并提取内容。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Search the web
infsh app run tavily/search-assistant --input '{"query": "latest AI developments 2024"}'
```

## 可用的应用程序

### Tavily

| 应用程序 | 应用程序 ID | 说明 |
|-----|--------|-------------|
| Search Assistant | `tavily/search-assistant` | 基于 AI 的搜索工具，可提供答案 |
| Extract | `tavily/extract` | 从 URL 中提取内容 |

### Exa

| 应用程序 | 应用程序 ID | 说明 |
|-----|--------|-------------|
| Search | `exa/search` | 智能网页搜索工具，支持 AI 功能 |
| Answer | `exa/answer` | 提供直接的事实性答案 |
| Extract | `exa/extract` | 从网页中提取并分析内容 |

## 示例

### Tavily Search

```bash
infsh app run tavily/search-assistant --input '{
  "query": "What are the best practices for building AI agents?"
}'
```

返回带有来源和图片的 AI 生成答案。

### Tavily Extract

```bash
infsh app run tavily/extract --input '{
  "urls": ["https://example.com/article1", "https://example.com/article2"]
}'
```

从多个 URL 中提取纯文本和图片。

### Exa Search

```bash
infsh app run exa/search --input '{
  "query": "machine learning frameworks comparison"
}'
```

返回高度相关的链接及其上下文信息。

### Exa Answer

```bash
infsh app run exa/answer --input '{
  "question": "What is the population of Tokyo?"
}'
```

提供直接的事实性答案。

### Exa Extract

```bash
infsh app run exa/extract --input '{
  "url": "https://example.com/research-paper"
}'
```

从网页中提取并分析内容。

## 工作流程：研究 + 大语言模型 (LLM)

```bash
# 1. Search for information
infsh app run tavily/search-assistant --input '{
  "query": "latest developments in quantum computing"
}' > search_results.json

# 2. Analyze with Claude
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Based on this research, summarize the key trends: <search-results>"
}'
```

## 工作流程：内容提取 + 摘要

```bash
# 1. Extract content from URL
infsh app run tavily/extract --input '{
  "urls": ["https://example.com/long-article"]
}' > content.json

# 2. Summarize with LLM
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Summarize this article in 3 bullet points: <content>"
}'
```

## 使用场景

- **研究**：收集任何主题的信息
- **检索增强生成 (RAG)**：结合检索结果进行内容生成
- **事实核查**：通过来源验证信息
- **内容聚合**：从多个来源收集数据
- **智能助手**：构建具备研究能力的人工智能助手

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# LLM models (combine with search for RAG)
npx skills add inference-sh/agent-skills@llm-models

# Image generation
npx skills add inference-sh/agent-skills@ai-image-generation
```

查看所有应用程序：`infsh app list`

## 文档资料

- [将工具添加到智能助手中](https://inference.sh/docs/agents/adding-tools) - 为智能助手配备搜索功能
- [构建研究型智能助手](https://inference.sh/blog/guides/research-agent) - 大语言模型与搜索功能的集成指南
- [工具集成指南](https://inference.sh/blog/tools/integration-tax) - 为什么使用预构建的工具很重要