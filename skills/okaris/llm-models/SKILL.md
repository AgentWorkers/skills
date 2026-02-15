---
name: llm-models
description: |
  Access Claude, Gemini, Kimi, GLM and 100+ LLMs via inference.sh CLI using OpenRouter.
  Models: Claude Opus 4.5, Claude Sonnet 4.5, Claude Haiku 4.5, Gemini 3 Pro, Kimi K2, GLM-4.6, Intellect 3.
  One API for all models with automatic fallback and cost optimization.
  Use for: AI assistants, code generation, reasoning, agents, chat, content generation.
  Triggers: claude api, openrouter, llm api, claude sonnet, claude opus, gemini api, kimi,
  language model, gpt alternative, anthropic api, ai model api, llm access, chat api,
  claude alternative, openai alternative
allowed-tools: Bash(infsh *)
---

# 通过 OpenRouter 访问 LLM 模型

您可以通过 [inference.sh](https://inference.sh) 命令行界面（CLI）访问 100 多种语言模型。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Call Claude Sonnet
infsh app run openrouter/claude-sonnet-45 --input '{"prompt": "Explain quantum computing"}'
```

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Claude Opus 4.5 | `openrouter/claude-opus-45` | 复杂推理、编程 |
| Claude Sonnet 4.5 | `openrouter/claude-sonnet-45` | 平衡的性能 |
| Claude Haiku 4.5 | `openrouter/claude-haiku-45` | 快速、经济实惠 |
| Gemini 3 Pro | `openrouter/gemini-3-pro-preview` | Google 的最新模型 |
| Kimi K2 Thinking | `openrouter/kimi-k2-thinking` | 多步推理 |
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

### Claude Haiku（快速且经济实惠的模型）

```bash
infsh app run openrouter/claude-haiku-45 --input '{
  "prompt": "Translate this to French: Hello, how are you?"
}'
```

### Kimi K2（具有推理能力的模型）

```bash
infsh app run openrouter/kimi-k2-thinking --input '{
  "prompt": "Plan a step-by-step approach to build a web scraper"
}'
```

### 任意模型（自动选择模型）

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
- **写作**：创作内容、撰写摘要、进行翻译
- **分析**：数据解读、科学研究
- **智能代理**：构建基于 AI 的工作流程
- **聊天**：实现对话式交互界面

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/agent-skills@inference-sh

# Web search (combine with LLMs for RAG)
npx skills add inference-sh/agent-skills@web-search

# Image generation
npx skills add inference-sh/agent-skills@ai-image-generation

# Video generation
npx skills add inference-sh/agent-skills@ai-video-generation
```

浏览所有应用：`infsh app list`

## 文档资料

- [智能代理概述](https://inference.sh/docs/concepts/agents) - 构建 AI 代理
- [代理 SDK](https://inference.sh/docs/api/agent/overview) - 程序化代理控制
- [构建研究代理](https://inference.sh/blog/guides/research-agent) - LLM 与搜索功能的集成指南