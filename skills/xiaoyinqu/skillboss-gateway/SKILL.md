---
name: skillboss-gateway
tagline: "One API for 100+ AI models - Claude, GPT, Gemini, more"
description: "使用一个 API 密钥即可访问 100 多个 AI 模型。兼容 OpenAI，支持自动故障转移、统一计费，无需创建供应商账户。"
version: "1.0.0"
author: "SkillBoss"
homepage: "https://skillboss.co"
support: "support@skillboss.co"
license: "MIT"
category: "ai-gateway"
tags:
  - ai-gateway
  - multi-model
  - openai-compatible
  - unified-api
  - failover
pricing: "pay-as-you-go"
metadata:
  openclaw:
    requires:
      env:
        - SKILLBOSS_API_KEY
    primaryEnv: SKILLBOSS_API_KEY
    installHint: "Get API key at https://skillboss.co/console"
---
# SkillBoss 统一 AI 门户

**一个 API 密钥，支持 100 多个模型，无需注册任何供应商账户。**

## 为什么使用这个门户？

| 问题 | SkillBoss 的解决方案 |
|---------|-------------------|
| 需要多个 API 密钥 | 使用一个密钥即可访问所有模型 |
| 多个账单 | 支持统一计费 |
| 遇到速率限制 | 自动切换到备用模型 |
| 被供应商锁定 | 通过一个参数即可切换模型 |

## 支持的模型

### 聊天/推理
- **Claude**: 4.5 Opus, 4.5 Sonnet, 3.7 Sonnet, Haiku
- **GPT**: GPT-5, GPT-4.1, o4-mini, o3-mini
- **Gemini**: 2.5 Pro, 2.5 Flash
- **DeepSeek**: R1, V3
- **Llama**: 3.1 405B, 70B
- **Mistral**: Large
- **Cohere**: Command R+

### 图像生成
- DALL-E 3, Flux Schnell/Dev, Minimax

### 视频生成
- Veo 3.1, Minimax Video-01

### 音频
- Whisper (文本转语音), ElevenLabs (文本转语音), Minimax TTS

### 数据与工具
- Perplexity Search, Firecrawl, Reducto 等

## 使用方法

```bash
# Just change the model parameter
curl https://api.heybossai.com/v1/chat/completions \
  -H "Authorization: Bearer $SKILLBOSS_API_KEY" \
  -d '{
    "model": "claude-4-5-sonnet",  # or gpt-5, gemini-2.5-pro, etc.
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## 兼容 OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-skillboss-key",
    base_url="https://api.heybossai.com/v1"
)

# Use any model
response = client.chat.completions.create(
    model="claude-4-5-sonnet",  # or any other model
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## 主要特性

- **自动切换** - 如果 Claude 无法使用，会自动切换到 GPT
- **实时响应** - 提供实时响应
- **函数调用** - 支持调用各种工具
- **图像处理** - 支持使用图像作为输入
- **缓存** - 在可能的情况下缓存提示内容

## 定价

按照供应商的定价标准收费，不加任何额外费用。

立即开始使用：https://skillboss.co/console