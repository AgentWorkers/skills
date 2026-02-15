---
name: llm-evaluator
version: 1.0.0
description: **通过 Langfuse 将 LLM 作为评估器使用**：该工具使用 GPT-5-nano 作为评估标准，对代码追踪（traces）的相关性、准确性、生成幻觉（hallucination）以及实用性（helpfulness）进行评分。支持单条代码追踪的评分、批量数据补充（backfill）以及测试模式。同时，该工具与 Langfuse 仪表板集成，以便于监控和观察评估结果。可执行的操作包括：评估代码追踪、评分质量检查、准确性验证、补充评分数据、测试评估器功能以及启动 LLM 评估流程。
license: MIT
compatibility:
  openclaw: ">=0.10"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["OPENROUTER_API_KEY", "LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY"]
---
# LLM Evaluator ⚖️

这是一个基于 Langfuse 的 LLM（大型语言模型）评估系统，使用 GPT-5-nano 对 AI 输出进行评分。

## 使用场景

- 评估搜索结果或 AI 回答的质量
- 评估日志记录的相关性、准确性和幻觉检测能力
- 批量评分最近未评分的日志记录
- 对代理输出进行质量保证

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

| 评估指标 | 测量内容 | 分数范围 |
|---------|------------|---------|
| 相关性 | 回答与查询的相关程度 | 0–1 |
| 准确性 | 事实的准确性 | 0–1 |
| 幻觉检测 | 检测到的虚假信息 | 0–1 |
| 有用性 | 整体的实用性 | 0–1 |

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)  
该工具是 OpenClaw 代理的 **AgxntSix Skill Suite** 的一部分。

📅 **需要帮助为您的企业设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)