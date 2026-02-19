---
name: geepers-llm
description: 向 dr.eamer.dev 的 LLM API 发送请求，以完成聊天对话、进行视觉分析、生成图像、实现文本转语音以及视频生成等功能。这些功能支持 12 家不同的模型提供商。当您需要调用外部 LLM 端点或希望比较不同提供商的响应时，可以使用该 API。
---
# Dreamer LLM

您可以通过一个统一的 API（`https://api.dr.eamer.dev`）访问 12 家大型语言模型（LLM）提供商。

## 认证

将您的 API 密钥设置为一个环境变量，或在每次请求时传递该密钥：

```bash
export DREAMER_API_KEY=your_key_here
```

获取 API 密钥：发送电子邮件至 luke@lukesteuber.com，或访问 https://dr.eamer.dev

## 端点（Endpoints）

### 聊天完成（Chat Completion）
```
POST https://api.dr.eamer.dev/v1/llm/chat
Headers: X-API-Key: $DREAMER_API_KEY
Body:
{
  "model": "claude-sonnet-4-5-20250929",
  "messages": [{"role": "user", "content": "Hello"}],
  "provider": "anthropic"
}
```

### 可用的提供商（Available Providers）
`anthropic`, `openai`, `xai`, `mistral`, `cohere`, `gemini`, `perplexity`, `groq`, `huggingface`, `ollama`

### 模型列表（List Models）
```
GET https://api.dr.eamer.dev/v1/llm/models
```

### 视觉处理（图像分析，Vision: Image Analysis）
```
POST https://api.dr.eamer.dev/v1/llm/vision
Body: { "model": "claude-sonnet-4-5-20250929", "image_url": "...", "prompt": "Describe this image" }
```

### 图像生成（Image Generation）
```
POST https://api.dr.eamer.dev/v1/llm/image
Body: { "prompt": "A sunset over the ocean", "provider": "openai" }
```

### 文本转语音（Text-to-Speech）
```
POST https://api.dr.eamer.dev/v1/llm/tts
Body: { "text": "Hello world", "voice": "alloy" }
```

## 适用场景（When to Use）
- 比较多个 LLM 提供商的响应结果
- 访问那些您没有直接 API 密钥的提供商
- 构建需要使用多个 LLM 提供商的应用程序

## 不适用场景（When Not to Use）
- 您已经拥有所需提供商的直接 API 密钥
- 您需要实时流式响应（请使用相应的提供商 API）