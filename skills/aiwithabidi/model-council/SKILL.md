---
name: model-council
description: Multi-model consensus system — send a query to 3+ different LLMs via OpenRouter simultaneously, then a judge model evaluates all responses and produces a winner, reasoning, and synthesized best answer. Like having a board of AI advisors. Use for important decisions, code review, research verification.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, OpenRouter API key
metadata: {"openclaw": {"emoji": "\ud83c\udfdb\ufe0f", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# Model Council 🏛️

**通过多个AI模型获取关于任何问题的共识。**

您可以通过OpenRouter同时将查询发送给3个或更多的大型语言模型（LLM）。一个“评判模型”会评估所有响应，并选出最佳答案，同时提供理由和综合分析。

## 使用场景

- **重要决策** — 不要仅依赖一个模型的意见
- **代码审查** — 从多个角度评估架构选择
- **研究验证** — 在不同模型之间交叉核对事实
- **创意工作** — 比较不同的写作风格并选择最佳方案
- **调试** — 当某个模型遇到问题时，其他模型可能能发现问题的根源

## 工作原理

```
Your Question
    ├──→ Claude Sonnet 4    ──→ Response A
    ├──→ GPT-4o             ──→ Response B
    └──→ Gemini 2.0 Flash   ──→ Response C
                                    │
                              Judge (Opus) evaluates all
                                    │
                              ├── Winner + Reasoning
                              ├── Synthesized Best Answer
                              └── Cost Breakdown
```

## 快速入门

```bash
# Basic usage
python3 {baseDir}/scripts/model_council.py "What's the best database for a real-time analytics dashboard?"

# Custom models
python3 {baseDir}/scripts/model_council.py --models "anthropic/claude-sonnet-4,openai/gpt-4o,google/gemini-2.5-pro" "Your question"

# Custom judge
python3 {baseDir}/scripts/model_council.py --judge "openai/gpt-4o" "Your question"

# JSON output
python3 {baseDir}/scripts/model_council.py --json "Your question"

# Set max tokens per response
python3 {baseDir}/scripts/model_council.py --max-tokens 2000 "Your question"
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `--models` | claude-sonnet-4, gpt-4o, gemini-2.0-flash | 用逗号分隔的模型列表 |
| `--judge` | anthropic/claude-opus-4-6 | 评判模型 |
| `--max-tokens` | 1024 | 每个模型的最大令牌数 |
| `--json` | false | 以JSON格式输出结果 |
| `--timeout` | 60 | 每个模型的超时时间（秒） |

## 环境要求

需要设置`OPENROUTER_API_KEY`环境变量。

## 输出示例

```
═══ MODEL COUNCIL RESULTS ═══

Question: What's the best way to handle auth in a microservices architecture?

── Council Member Responses ──

🤖 anthropic/claude-sonnet-4 ($0.0043)
Use a centralized auth service with JWT tokens...

🤖 openai/gpt-4o ($0.0038)
Implement OAuth 2.0 with an API gateway...

🤖 google/gemini-2.0-flash-001 ($0.0012)
Consider using service mesh with mTLS...

── Judge Verdict (anthropic/claude-opus-4-6, $0.0125) ──

🏆 Winner: anthropic/claude-sonnet-4
Reasoning: Most comprehensive and practical approach...

📝 Synthesized Answer:
The best approach combines elements from all three...

💰 Total Cost: $0.0218
```

## 致谢

由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai)开发 |
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)提供支持 |
该工具是OpenClaw代理的**AgxntSix Skill Suite**的一部分。

📅 **需要帮助为您的业务设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)