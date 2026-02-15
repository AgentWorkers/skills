---
name: aimlapi-llm-reasoning
description: 通过聊天完成方式运行 AIMLAPI 的大型语言模型（LLM）和推理工作流程，支持重试机制、结构化输出以及明确的 User-Agent 标头。当 Codex 需要对 AIMLAPI 模型进行脚本化提示或推理调用时，可使用此方法。
env:
  - AIMLAPI_API_KEY
primaryEnv: AIMLAPI_API_KEY
---

# AIMLAPI LLM + 推理（AIMLAPI Large Language Model + Reasoning）

## 概述

使用 `run_chat.py` 调用 AIMLAPI 的聊天功能，该工具支持重试机制、可选的 API 密钥文件作为备用方案，并在每次请求中添加 `User-Agent` 标头。

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
  --user "Draft a project kickoff checklist." \
  --user-agent "openclaw-custom/1.0"
```

### 添加推理参数

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
  --extra-json '{"response_format": {"type": "json_object"}}' \
  --output ./out/risks.json
```

## 参考资料

- `references/aimlapi-llm.md`：包含请求数据（payload）及故障排除说明。
- `README.md`：以变更日志的形式总结了新增的指令和功能。