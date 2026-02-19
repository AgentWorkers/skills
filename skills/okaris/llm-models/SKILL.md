---
name: llm-models
description: "通过 `inference.sh` CLI 和 `OpenRouter`，您可以访问 Claude、Gemini、Kimi、GLM 以及 100 多个大型语言模型（LLM）。支持的模型包括：Claude Opus 4.5、Claude Sonnet 4.5、Claude Haiku 4.5、Gemini 3 Pro、Kimi K2、GLM-4.6 和 Intellect 3。所有模型都通过同一个 API 进行访问，系统会自动进行故障转移（fallback）并优化使用成本。这些模型可用于以下场景：AI 辅助、代码生成、推理、聊天机器人、内容创作等。相关的触发命令包括：`claude api`、`openrouter`、`llm api`、`claude sonnet`、`claude opus`、`gemini api`、`kimi`、`language model`、`gpt alternative`、`anthropic api`、`ai model api`、`llm access`、`chat api`、`claude alternative` 和 `openai alternative`。"
allowed-tools: Bash(infsh *)
---
# 通过 OpenRouter 使用大语言模型（LLM）

您可以通过 [inference.sh](https://inference.sh) 命令行界面（CLI）访问 100 多种语言模型。

![通过 OpenRouter 使用大语言模型](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgvftjwhby36trvaj66bwzcf.jpeg)

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Call Claude Sonnet
infsh app run openrouter/claude-sonnet-45 --input '{"prompt": "Explain quantum computing"}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Claude Opus 4.5 | `openrouter/claude-opus-45` | 复杂推理、编程 |
| Claude Sonnet 4.5 | `openrouter/claude-sonnet-45` | 平衡的性能 |
| Claude Haiku 4.5 | `openrouter/claude-haiku-45` | 快速、高效 |
| Gemini 3 Pro | `openrouter/gemini-3-pro-preview` | Google 的最新模型 |
| Kimi K2 Thinking | `openrouter/kimi-k2-thinking` | 多步骤推理 |
| GLM-4.6 | `openrouter/glm-46` | 开源模型，适用于编程 |
| Intellect 3 | `openrouter/intellect-3` | 通用型模型 |
| 任意模型 | `openrouter/any-model` | 自动选择最佳模型 |

## 搜索 LLM 应用

```bash
infsh app list --search "openrouter"
infsh app list --search "claude"
```

## 示例

### Claude Opus（高质量模型）

```bash
infsh app run openrouter/claude-opus-45 --input '{
  "prompt": "Write a Python function to detect palindromes with comprehensive tests"
}'
```

### Claude Sonnet（性能均衡的模型）

```bash
infsh app run openrouter/claude-sonnet-45 --input '{
  "prompt": "Summarize the key concepts of machine learning"
}'
```

### Claude Haiku（快速且低成本的模型）

```bash
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Translate this to French: Hello, how are you?"
}'
```

### Kimi K2（用于多步骤推理的模型）

```bash
infsh app run openrouter/kimi-k2-thinking --input '{
  "prompt": "Plan a step-by-step approach to build a web scraper"
}'
```

### 任意模型（自动选择）

```bash
# Automatically picks the most cost-effective model
infsh app run openrouter/any-model --input '{
  "prompt": "What is the capital of France?"
}'
```

### 使用系统提示进行交互

```bash
infsh app sample openrouter/claude-sonnet-45 --save input.json

# Edit input.json:
# {
#   "system": "You are a helpful coding assistant",
#   "prompt": "How do I read a file in Python?"
# }

infsh app run openrouter/claude-sonnet-45 --input input.json
```

## 使用场景

- **编程**：生成、审查、调试代码
- **写作**：内容创作、摘要生成、翻译
- **分析**：数据解读、研究
- **智能助手**：构建基于 AI 的工作流程
- **聊天**：提供对话式交互界面

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# Web search (combine with LLMs for RAG)
npx skills add inference-sh/skills@web-search

# Image generation
npx skills add inference-sh/skills@ai-image-generation

# Video generation
npx skills add inference-sh/skills@ai-video-generation
```

- 浏览所有应用：`infsh app list`

## 文档资料

- [智能助手概述](https://inference.sh/docs/concepts/agents) - 如何构建 AI 助手
- [智能助手 SDK](https://inference.sh/docs/api/agent/overview) - 程序化控制智能助手
- [构建研究型智能助手](https://inference.sh/blog/guides/research-agent) - LLM 与搜索功能的集成指南