---
name: gpt
description: OpenAI GPT集成：通过OpenAI API实现聊天功能、图像生成、嵌入模型以及模型的微调。
metadata: {"clawdbot":{"emoji":"🤖","always":true,"requires":{"bins":["curl","jq"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# GPT 🤖

OpenAI GPT 的集成方案。

## 设置

```bash
export OPENAI_API_KEY="sk-..."
```

## 功能

- 聊天自动补全（GPT-4、GPT-4o）
- 图像生成（DALL-E）
- 文本嵌入
- 模型微调
- 辅助工具 API

## 使用示例

```
"Ask GPT: Explain quantum computing"
"Generate image of a sunset"
"Create embeddings for this text"
```

## API 参考

```bash
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"Hello"}]}'
```