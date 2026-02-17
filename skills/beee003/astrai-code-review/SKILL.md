---
name: astrai-code-review
description: 基于人工智能的代码审查系统，结合智能模型路由技术——与始终使用最昂贵的模型相比，可节省40%以上的成本。
version: 1.0.0
homepage: https://github.com/beee003/astrai-openclaw
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      env: ["ASTRAI_API_KEY"]
    primaryEnv: "ASTRAI_API_KEY"
    files: ["plugin.py", "config.example.toml"]
tags: [code-review, inference, routing, cost-optimization, pr-review, diff, quality]
---
# Astrai 代码审查

Astrai 是一款基于人工智能的代码审查工具，具备智能的模型选择功能。复杂的逻辑问题会由强大的模型处理，而格式和风格问题则会由效率较高的模型处理。使用 Astrai 可以节省 40% 以上的成本，同时不会牺牲代码质量。

## 功能概述

- **智能的模型选择**：Astrai 会根据代码差异的复杂程度自动选择最合适的模型进行处理。例如，复杂的并发问题会由 Opus 模型处理，而简单的格式问题则由 Haiku 模型处理。您只需为实际需要的智能服务付费。
- **结构化的审查结果**：每条审查结果都会包含问题的详细信息（文件路径、行号、严重程度、问题描述以及具体的改进建议）。
- **多种审查模式**：
  - **标准模式**：仅检测代码错误和逻辑问题。
  - **严格模式**：除了检测错误和逻辑问题外，还会检查代码格式和最佳实践是否符合规范。
  - **安全模式**：重点检测安全漏洞（如 SQL 注入、跨站脚本攻击、身份验证漏洞等）。
- **自定义模型选择**：您可以使用自己的 API 密钥（BYOK, Bring Your Own Keys）来指定使用哪个模型。Astrai 会使用您的密钥调用相应的模型，并直接向模型提供商支付费用。
- **成本透明**：每条审查结果的报告中都会显示实际费用以及相比使用最昂贵模型的节省金额。
- **本地模式**：如果您仅设置 `ASTRAI_API_KEY` 而不提供其他模型密钥，Astrai 会使用自己托管的模型进行代码审查，依然提供智能的路由选择和低成本的审查服务。

## 设置方法

1. 在 [as-trai.com](https://as-trai.com) 免费获取 API 密钥。
2. 在您的环境配置或技能设置中添加 `ASTRAI_API_KEY`。
3. （可选）添加用于自定义模型选择的提供商 API 密钥（如 `ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 等）。
4. 对任何代码差异或 Pull Request（PR）执行 `/review` 命令即可启动代码审查。

## 使用示例

### 基本代码差异审查：
Astrai 会返回当前代码差异中发现的问题的详细信息，包括问题的严重程度和改进建议。

### 严格模式的代码审查（适用于 Pull Request）：
Astrai 不仅能检测代码错误，还能检查代码格式、命名规范以及是否存在最佳实践的缺失。

### 安全审计：
Astrai 会重点检测 SQL 注入、跨站脚本攻击、身份验证漏洞、硬编码的敏感信息以及不安全的序列化等问题。

## 环境变量

| 变量 | 是否必填 | 说明 | 默认值 |
| --- | --- | --- | --- |
| `ASTRAI_API_KEY` | 是 | 从 as-trai.com 获取的 API 密钥 | -- |
| `ANTHROPIC_API_KEY` | 否 | 用于自定义模型选择的 Anthropic API 密钥 | -- |
| `OPENAI_API_KEY` | 否 | 用于自定义模型选择的 OpenAI API 密钥 | -- |
| `GOOGLE_API_KEY` | 否 | 用于自定义模型选择的 Google API 密钥 | -- |
| `DEEPSEEK_API_KEY` | 否 | 用于自定义模型选择的 DeepSeek API 密钥 | -- |
| `MISTRAL_API_KEY` | 否 | 用于自定义模型选择的 Mistral API 密钥 | -- |
| `GROQ_API_KEY` | 否 | 用于自定义模型选择的 Groq API 密钥 | -- |
| `TOGETHER_API_KEY` | 否 | 用于自定义模型选择的 Together API 密钥 | -- |
| `FIREWORKS_API_KEY` | 否 | 用于自定义模型选择的 Fireworks API 密钥 | -- |
| `COHERE_API_KEY` | 否 | 用于自定义模型选择的 Cohere API 密钥 | -- |
| `PERPLEXITY_API_KEY` | 否 | 用于自定义模型选择的 Perplexity API 密钥 | -- |
| `REVIEW_STRICTNESS` | 否 | 可设置为 standard、strict 或 security | standard |

## 外部接口

| 接口 | 功能 | 发送的数据 |
| --- | --- | --- |
| `https://as-trai.com/v1/chat/completions` | 通过智能路由进行代码审查 | 代码差异内容、文件上下文及审查指令 |

## 安全与隐私

- 所有请求均通过 API 请求头中的 API 密钥进行身份验证。
- 代码差异数据会被发送到 Astrai 的路由 API，然后由该 API 转发给选定的模型提供商。
- 在自定义模型模式下，提供商的 API 密钥会通过加密的 `X-Astrai-Provider-Keys` 头部字段发送，且不会被 Astrai 存储。
- 请求完成后，Astrai 会立即删除所有相关的代码差异数据、代码内容及审查结果。
- 源代码代码库公开可见：[github.com/beee003/astrai-openclaw](https://github.com/beee003/astrai-openclaw)

## 模型调用机制

该工具会将代码差异数据发送到 Astrai 的路由 API，Astrai 会根据代码的复杂程度选择合适的模型进行处理：
- **高复杂度问题**（如并发问题、安全漏洞、架构问题）：会使用 Claude Opus、GPT-4o 或 Gemini Pro 模型。
- **中等复杂度问题**（如逻辑错误、遗漏的边界情况）：会使用 Claude Sonnet、GPT-4o-mini 或 Gemini Flash 模型。
- **低复杂度问题**（如格式问题、拼写错误、命名不规范）：会使用 Claude Haiku、GPT-4o-mini 或 Gemini Flash 模型。

您的输入内容会由第三方大型语言模型（LLM）提供商根据路由策略进行处理。在自定义模型模式下，所有调用均使用您提供的 API 密钥进行。

## 定价

价格与 Astrai 平台的定价相同：

- **免费版**：每天 1,000 次请求，支持智能模型选择和所有审查模式。
- **专业版**（每月 49 美元）：无限请求次数、优先路由服务及分析仪表盘。
- **企业版**（每月 199 美元）：团队级仪表盘、合规性报告及 SLA 保障。