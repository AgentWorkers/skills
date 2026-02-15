---
name: claude
description: Anthropic Claude集成：通过Anthropic API与Claude模型进行聊天。
metadata: {"clawdbot":{"emoji":"🧠","always":true,"requires":{"bins":["curl","jq"]},"primaryEnv":"ANTHROPIC_API_KEY"}}
---

# Claude 🧠

Anthropic Claude 的集成方案。

## 设置

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 功能

- 与 Claude 进行聊天（支持 Opus、Sonnet、Haiku 三种风格）
- 支持长文本对话（最大长度为 200,000 个令牌）
- 具备视觉理解能力
- 支持使用各种工具

## 使用示例

```
"Ask Claude: Analyze this code"
"Use Claude to summarize this document"
```

## API 参考

```bash
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":1024,"messages":[{"role":"user","content":"Hello"}]}'
```