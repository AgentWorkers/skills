---
name: clawrouter
description: 智能大型语言模型（LLM）路由器——可节省78%的推理成本。该路由器会将每个请求路由到来自OpenAI、Anthropic、Google、DeepSeek和xAI等平台的30多个模型中成本最低且性能最佳的模型进行处理。
homepage: https://github.com/BlockRunAI/ClawRouter
metadata: { "openclaw": { "emoji": "🦀", "requires": { "config": ["models.providers.blockrun"] } } }
---

# ClawRouter

这是一个智能的大型语言模型（LLM）路由器，通过将每个请求路由到能够处理该请求的最便宜的模型，从而节省了78%的推理成本。系统支持来自5个提供商的30多个模型，所有这些模型都可通过同一个钱包进行使用。

## 安装

```bash
openclaw plugins install @blockrun/clawrouter
```

## 设置

```bash
# Enable smart routing (auto-picks cheapest model per request)
openclaw models set blockrun/auto

# Or pin a specific model
openclaw models set openai/gpt-4o
```

## 路由机制

ClawRouter将每个请求分为四个层级：

- **简单请求**（占流量的40%）——事实查询、问候语、翻译 → Gemini Flash（0.60美元/请求，节省99%的成本）
- **中等复杂度请求**（占30%）——摘要生成、解释、数据提取 → DeepSeek Chat（0.42美元/请求，节省99%的成本）
- **复杂请求**（占20%）——代码生成、多步骤分析 → Claude Opus（75美元/请求，提供最佳质量的服务）
- **高级推理请求**（占10%）——证明、形式逻辑、多步骤数学计算 → o3（8美元/请求，节省89%的成本）

系统能够以不到1毫秒的时间处理大约80%的请求；只有那些含义模糊的查询才会被发送到大型语言模型进行分类（每次分类的成本约为0.00003美元）。

## 可用的模型

系统提供了30多个模型，包括：gpt-5.2、gpt-4o、gpt-4o-mini、o3、o4-mini、claude-opus-4.5、claude-sonnet-4、claude-haiku-4.5、gemini-2.5-pro、gemini-2.5-flash、deepseek-chat、deepseek-reasoner、grok-3、grok-3-mini等。

## 示例输出

```
[ClawRouter] google/gemini-2.5-flash (SIMPLE, rules, confidence=0.92)
             Cost: $0.0025 | Baseline: $0.308 | Saved: 99.2%
```