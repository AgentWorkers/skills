---
name: llm-evaluator
description: 使用 Langfuse 的 LLM-as-a-Judge 评估系统：该系统用于评估 AI 输出在相关性、准确性、生成虚假内容（hallucination）以及实用性（helpfulness）方面的表现。系统会利用历史数据来补充评分（backfill scoring）。在评估 AI 质量、构建评估模型或监控输出准确性时，可优先选择使用 GPT-5-nano 进行高效、低成本的评估。
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, Langfuse instance, OpenRouter API key
metadata: {"openclaw": {"emoji": "\u2696\ufe0f", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# LLM Evaluator ⚖️

这是一个基于 Langfuse 的 LLM（Large Language Model）评估系统，使用 GPT-5-nano 对 AI 输出进行评分。

## 使用场景

- 评估搜索结果或 AI 回答的质量
- 评估日志记录的相关性、准确性和虚假信息检测能力
- 批量评分最近未评分的日志记录
- 对代理输出进行质量检查

## 使用方法

```bash
# Test with sample cases
python3 {baseDir}/scripts/evaluator.py test

# Score a specific Langfuse trace
python3 {baseDir}/scripts/evaluator.py score <trace_id>

# Score with specific evaluator only
python3 {baseDir}/scripts/evaluator.py score <trace_id> --evaluators relevance

# Backfill scores on recent unscored traces
python3 {baseDir}/scripts/evaluator.py backfill --limit 20
```

## 评估指标

| 评估指标 | 测量内容 | 分值范围 |
|---------|-----------|---------|
| 相关性 | 回答与查询内容的相关程度 | 0–1 |
| 准确性 | 信息的真实性 | 0–1 |
| 虚假信息检测 | 是否包含虚构内容 | 0–1 |
| 有用性 | 回答的总体实用性 | 0–1 |

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube 频道](https://youtube.com/@aiwithabidi) | [GitHub 仓库](https://github.com/aiwithabidi)  
该工具是 OpenClaw 代理的 **AgxntSix Skill Suite** 的组成部分。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)