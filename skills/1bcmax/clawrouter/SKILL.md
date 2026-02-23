---
name: clawrouter
description: 智能大语言模型（LLM）路由器——可节省高达67%的推理成本。该路由器会将每个请求自动路由到OpenAI、Anthropic、Google、DeepSeek和xAI提供的41个模型中性能最优秀、成本最低的模型进行处理。
homepage: https://github.com/BlockRunAI/ClawRouter
metadata: { "openclaw": { "emoji": "🦀", "requires": { "config": ["models.providers.blockrun"] } } }
---
# ClawRouter

这是一个智能的LLM（大型语言模型）路由器，通过将每个请求路由到能够处理该请求的最便宜的模型，从而节省了67%的推理成本。系统支持5家提供商提供的41个模型，所有这些模型都可通过同一个钱包进行使用。

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

- **简单请求**（占流量的40%）——事实查询、问候语、翻译 → Gemini Flash（费用：0.60美元/百万次请求，节省99%的成本）
- **中等复杂度请求**（占30%）——摘要生成、解释、数据提取 → DeepSeek Chat（费用：0.42美元/百万次请求，节省99%的成本）
- **复杂请求**（占20%）——代码生成、多步骤分析 → Claude Opus（费用：75美元/百万次请求，提供最佳质量的服务）
- **高级推理请求**（占10%）——证明、形式逻辑、多步骤数学运算 → o3（费用：8美元/百万次请求，节省89%的成本）

系统能够以不到1毫秒的时间处理大约80%的请求；只有那些含义模糊的查询才会被发送到LLM分类器进行处理（每次分类的费用约为0.00003美元）。

## 可用的模型

系统支持的模型包括：gpt-5.2、gpt-4o、gpt-4o-mini、o3、o1、claude-opus-4.6、claude-sonnet-4.6、claude-haiku-4.5、geminii-3.1-pro、geminii-2.5-pro、geminii-2.5-flash、geminii-2.5-flash-lite、deepseek-chat、deepseek-reasoner、grok-3、grok-3-mini。

## 示例输出

```
[ClawRouter] google/gemini-2.5-flash (SIMPLE, rules, confidence=0.92)
             Cost: $0.0025 | Baseline: $0.308 | Saved: 99.2%
```