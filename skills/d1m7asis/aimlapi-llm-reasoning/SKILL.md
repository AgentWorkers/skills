---
name: aimlapi-llm-reasoning
description: 运行与 OpenAI 兼容的 AIMLAPI 大语言模型（LLM）以及相关的推理工作流程，包括聊天对话的自动完成、工具式提示生成以及结构化输出功能。当 Codex 需要设计提示语、调用 LLM 或通过 AIMLAPI 端点执行推理/分析任务时，可以使用该功能。
---

# AIMLAPI LLM + 推理

## 概述

使用可重用的脚本来调用 AIMLAPI 的聊天功能、传递模型特定的推理参数，并捕获结构化的输出结果。

## 快速入门

```bash
export AIMLAPI_API_KEY="sk-aimlapi-..."
python3 {baseDir}/scripts/run_chat.py --model aimlapi/openai/gpt-5-nano-2025-08-07 --user "Summarize this in 3 bullets."
```

## 任务

### 运行基本的聊天功能

```bash
python3 {baseDir}/scripts/run_chat.py \
  --model aimlapi/openai/gpt-5-nano-2025-08-07 \
  --system "You are a concise assistant." \
  --user "Draft a project kickoff checklist."
```

### 添加推理参数或特定于提供者的参数

使用 `--extra-json` 选项来传递诸如推理难度、响应格式或工具配置等参数，而无需修改脚本。

```bash
python3 {baseDir}/scripts/run_chat.py \
  --model aimlapi/openai/gpt-5-nano-2025-08-07 \
  --user "Plan a 5-step rollout for a new chatbot feature." \
  --extra-json '{"reasoning": {"effort": "medium"}, "temperature": 0.3}'
```

### 结构化的 JSON 输出

```bash
python3 {baseDir}/scripts/run_chat.py \
  --model aimlapi/openai/gpt-5-nano-2025-08-07 \
  --user "Return a JSON array of 3 project risks with mitigation." \
  --extra-json '{"response_format": {"type": "json_object"}}'
```

## 参考资料

- `references/aimlapi-llm.md`：数据字段说明及故障排除指南。