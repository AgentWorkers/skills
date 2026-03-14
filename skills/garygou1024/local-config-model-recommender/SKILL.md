---
name: local-config-model-recommender
description: 根据任务需求，智能推荐最优的AI模型。动态读取用户的OpenCLAW配置，并提供基于上下文的模型建议。支持所有主流的国内外模型，包括OpenAI、Claude、Gemini、DeepSeek、Kimi、Zhipu GLM、Qwen和MiniMax。
---
# 模型推荐器

这是一个智能的模型选择助手，它能够动态分析您的 OpenCLAW 配置，并为您的具体任务推荐最合适的 AI 模型。

## 概述

该功能会读取您本地的 OpenCLAW 配置，以确定可用的模型，然后通过基于关键词的能力匹配来提供智能化的推荐建议。

## 支持的模型

### 全球模型提供商

| 提供商 | 模型        |
|---------|-----------|
| OpenAI   | gpt-5-pro, gpt-4o, gpt-4o-mini, o3, o1 |
| Anthropic Claude | claude-opus-4.6, claude-sonnet-4.6, claude-haiku-4.5 |
| Google Gemini | gemini-3.1-pro, gemini-3.1-flash, gemini-2.5-flash |
| Mistral   | mistral-large, mistral-small |
| xAI    | grok-4.20-beta, grok-4-fast |

### 国内（中国）模型提供商

| 提供商 | 模型        |
|---------|-----------|
| Alibaba Qwen | qwen3-max, qwen3-vl, qwen3.5-plus, qwen3-coder-plus |
| MiniMax  | minimax-m2.5, minimax-m2.1 |
| DeepSeek | deepseek-v3.2, deepseek-chat, deepseek-coder |
| Moonshot (Kimi) | kimi-k2.5, kimi-k2 |
| Zhipu GLM | glm-5, glm-4.7-flash, glm-4.6v |
| Baidu ERNIE | ernie-4.5-thinking, ernie-4.5-vl |
| ByteDance Seed | seed-2.0-lite, seed-2.0-mini |

## 能力匹配

该功能使用基于关键词的模式匹配来推断模型的能力：

| 关键词    | 能力        | 主要用途                |
|---------|------------------|----------------------|
| `vl`, `vision`, `image`, `4v`, `4o` | 视觉/多模态    | 图像分析、OCR、图表解读           |
| `code`, `coder`, `codex` | 代码生成    | 编程、调试、重构             |
| `o1`, `o3`, `o4`, `reasoning`, `thinking` | 高级推理    | 数学推理、复杂逻辑             |
| `max`, `pro`, `premium`, `large`, `opus` | 高端/顶级模型 | 高质量输出、复杂任务             |
| `mini`, `small`, `lite`, `flash`, `haiku`, `nano` | 轻量级模型    | 快速响应、简单任务、成本敏感           |

## 推荐逻辑

```
1. Parse ~/.openclaw/openclaw.json to extract configured models
2. Analyze user's task requirements
3. Match task to model capabilities via keyword detection
4. Return the best-matching model from available configuration
5. Fall back to default model if no specific match found
```

## 使用示例

**用户:** “我应该使用哪个模型进行编程？”
→ **推荐:** minimax-m2.5, deepseek-coder, qwen3-coder-plus

**用户:** “我需要分析一张图片”
→ **推荐:** qwen3-vl, glm-4.6v, gpt-4o, gemini-1.5-pro

**用户:** “对于复杂的推理任务”
→ **推荐:** o3, claude-opus-4.6, qwen3-max, gemini-3.1-pro

## 注意事项

- 自动适应您的具体配置
- 优先选择您系统中实际可用的模型
- 在找不到完全匹配的模型时，会优雅地回退
- 支持全球（OpenAI、Claude、Gemini）和国内（中国）的模型提供商