---
name: LLM Evaluator
version: 1.0.0
description: 集成 Langfuse 的 LLM 作为裁判（LLM-as-a-Judge）评估系统
author: aiwithabidi
---
# LLM Evaluator ⚖️

这是一个基于Langfuse的LLM（Large Language Model）评估系统，用于评估AI模型的输出。该系统从相关性、准确性、虚假信息生成能力以及实用性四个方面对AI模型的表现进行评分，并能够补充历史数据以完善评分结果。在评分过程中，系统使用了GPT-5-nano模型以实现高效、低成本的评估。

## 使用方法

```bash
# Test with sample cases
python3 scripts/evaluator.py test

# Score a specific Langfuse trace
python3 scripts/evaluator.py score <trace_id>

# Score with a single evaluator
python3 scripts/evaluator.py score <trace_id> --evaluators relevance

# Backfill scores on recent unscored traces
python3 scripts/evaluator.py backfill --limit 20
```

### 评估指标

- **相关性**（0-1）：模型的回答与查询内容的关联程度如何？
- **准确性**（0-1）：模型的回答是否在事实上是正确的？
- **虚假信息生成能力**（0-1）：模型的回答中是否包含虚构的信息？
- **实用性**（0-1）：模型的回答对用户有多大的帮助？

## 系统要求

- `OPENROUTER_API_KEY` 环境变量（用于GPT-5-nano模型的调用）
- `LANGFUSE_PUBLIC_KEY` 和 `LANGFUSE_SECRET_KEY` 环境变量
- `LANGFUSE_HOST`：您的Langfuse实例URL
- Python 3.10及以上版本
- `langfuse` 和 `requests` 库

## 开发者信息

该系统由 **AgxntSix** 开发，AgxntSix是由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 创建的AI运维工具。  
🌐 [agxntsix.ai](https://www.agxntsix.ai) | 属于OpenClaw代理工具包中的 **AgxntSix Skill Suite** 产品系列。