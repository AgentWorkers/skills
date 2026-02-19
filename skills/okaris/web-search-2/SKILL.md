---
name: web-search
description: "使用 `inference.sh` CLI 通过 Tavily 和 Exa 进行网页搜索和内容提取。相关应用程序包括：Tavily Search、Tavily Extract、Exa Search、Exa Answer、Exa Extract。主要功能包括：基于人工智能的搜索、内容提取、直接提供答案以及辅助研究工作。应用场景包括：学术研究、信息检索管道（RAG – Retrieval, Aggregation, and Generation）、事实核查、内容聚合以及自动化任务处理。触发条件包括：执行网页搜索、调用 Tavily 或 Exa 的相关 API、执行内容提取操作等。"
allowed-tools: Bash(infsh *)
---
# 网页搜索与内容提取

您可以通过 [inference.sh](https://inference.sh) 命令行工具在网页上搜索并提取内容。

![网页搜索与内容提取](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgndqjxd780zm2j3rmada6y8.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Search the web
infsh app run tavily/search-assistant --input '{"query": "latest AI developments 2024"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用的应用程序

### Tavily

| 应用程序 | 应用程序 ID | 说明 |
|-----|--------|-------------|
| Search Assistant | `tavily/search-assistant` | 基于 AI 的搜索工具，可提供答案 |
| Extract | `tavily/extract` | 从 URL 中提取内容 |

### Exa

| 应用程序 | 应用程序 ID | 说明 |
|-----|--------|-------------|
| Search | `exa/search` | 智能网页搜索工具 |
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
- **检索增强生成 (RAG)**：利用 AI 改进信息检索效果
- **事实核查**：通过来源验证信息
- **内容聚合**：从多个来源收集数据
- **智能助手**：构建具备研究能力的人工智能助手

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# LLM models (combine with search for RAG)
npx skills add inference-sh/skills@llm-models

# Image generation
npx skills add inference-sh/skills@ai-image-generation
```

查看所有应用程序：`infsh app list`

## 文档资料

- [为智能助手添加工具](https://inference.sh/docs/agents/adding-tools) - 为智能助手配备搜索功能
- [构建研究型智能助手](https://inference.sh/blog/guides/research-agent) - 大语言模型与搜索功能的集成指南
- [工具集成指南](https://inference.sh/blog/tools/integration-tax) - 了解预构建工具的重要性