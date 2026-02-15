---
name: llm
description: 多提供商大语言模型（LLM）集成：为 OpenAI、Anthropic、Google 以及本地模型提供统一的接口。
metadata: {"clawdbot":{"emoji":"🔮","always":true,"requires":{"bins":["curl","jq"]}}}
---

# 大语言模型（LLM） 🔮

支持多提供者的大型语言模型集成。

## 支持的提供者

- OpenAI（GPT-4、GPT-4o）
- Anthropic（Claude）
- Google（Gemini）
- 本地模型（Ollama、LM Studio）

## 主要功能

- 统一的聊天界面
- 模型比较
- 词元计数
- 成本估算
- 流式响应

## 使用示例

```
"Compare GPT-4 vs Claude on this task"
"Use local Llama model"
"Estimate tokens for this prompt"
```