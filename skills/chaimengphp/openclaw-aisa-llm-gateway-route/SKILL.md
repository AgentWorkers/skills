---
name: llm-router
description: "统一大语言模型（Unified LLM）网关：一个API，支持70多个AI模型。只需使用一个API密钥，即可访问GPT、Claude、Gemini、Grok等众多AI模型。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw LLM Router 🧠

**专为自主代理设计的统一LLM网关，由AIsa提供支持。**

只需一个API密钥，即可使用70多种模型，且兼容OpenAI。

用一个API密钥替代原有的100多个API密钥，通过统一的、兼容OpenAI的接口访问GPT-4、Claude-3、Gemini、Grok等模型。

## 🔥 您能做什么？

### 多模型聊天
```
"Chat with GPT-4 for reasoning, switch to Claude for creative writing"
```

### 模型比较
```
"Compare responses from GPT-4, Claude, and Gemini for the same question"
```

### 视觉分析
```
"Analyze this image with GPT-4o - what objects are in it?"
```

### 成本优化
```
"Route simple queries to fast/cheap models, complex queries to GPT-4"
```

### 回退策略
```
"If GPT-4 fails, automatically try Claude, then Gemini"
```

## 为什么选择LLM Router？

| 特性 | LLM Router | 直接API |
|---------|------------|-------------|
| API密钥 | 1个 | 10多个 |
| SDK兼容性 | OpenAI SDK | 多个SDK |
| 计费方式 | 统一计费 | 按服务提供商计费 |
| 模型切换 | 通过字符串配置 | 需重新编写代码 |
| 回退机制 | 内置 | 需自行实现 |
| 成本追踪 | 统一追踪 | 分散式追踪 |

## 支持的模型家族

| 模型家族 | 开发者 | 示例模型 |
|--------|-----------|----------------|
| GPT | OpenAI | gpt-5.2, gpt-5, gpt-5-mini, gpt-4.1, gpt-4.1-mini, gpt-4o, gpt-4o-mini |
| Claude | Anthropic | claude-sonnet-4-5, claude-opus-4-1, claude-opus-4, claude-sonnet-4, claude-haiku-4-5 |
| Gemini | Google | gemini-2.5-pro, gemini-2.5-flash, gemini-2.5-flash-lite, gemini-3-pro-preview |
| Grok | xAI | grok-4, grok-3 |
| Llama | Meta | llama-3.1-405b, llama-3.1-70b, llama-3.1-8b |
| Mistral | Mistral AI | mistral-large, mistral-medium, mixtral-8x7b |

> **注意**：模型可用性可能有所变化。请访问[marketplace.aisa.one/pricing](https://marketplace.aisa.one/pricing)查看当前可用模型及价格列表。

## 快速入门

```bash
export AISA_API_KEY="your-key"
```

## API端点

### 兼容OpenAI的聊天功能

```
POST https://api.aisa.one/v1/chat/completions
```

#### 请求
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

#### 参数

| 参数 | 类型 | 是否必填 | 说明 |
|-----------|------|----------|-------------|
| `model` | 字符串 | 是 | 模型标识符（例如：`gpt-4.1`, `claude-sonnet-4-5`） |
| `messages` | 数组 | 是 | 对话消息 |
| `temperature` | 数字 | 否 | 随机性（0-2，默认值：1） |
| `max_tokens` | 整数 | 否 | 最大响应字符数 |
| `stream` | 布尔值 | 否 | 是否启用流式响应（默认值：false） |
| `top_p` | 数字 | 否 | 核心采样率（0-1） |
| `frequency_penalty` | 数字 | 否 | 频率惩罚（-2至2） |
| `presence Penalty` | 数字 | 否 | 出现惩罚（-2至2） |
| `stop` | 字符串/数组 | 否 | 停止序列 |

#### 消息格式
```json
{
  "role": "user|assistant|system",
  "content": "message text or array for multimodal"
}
```

#### 响应
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "gpt-4.1",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Quantum computing uses..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 200,
    "total_tokens": 250,
    "cost": 0.0025
  }
}
```

### 流式响应

流式响应会返回服务器发送的事件（SSE格式）：
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4-5",
    "messages": [{"role": "user", "content": "Write a poem about AI."}],
    "stream": true
  }'
```

### 视觉/图像分析

通过传递图像URL或Base64数据来分析图像：
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "What is in this image?"},
          {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
      }
    ]
  }'
```

### 函数调用

启用工具/函数以获取结构化输出：
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4.1",
    "messages": [{"role": "user", "content": "What is the weather in Tokyo?"}],
    "functions": [
      {
        "name": "get_weather",
        "description": "Get current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {"type": "string", "description": "City name"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
          },
          "required": ["location"]
        }
      }
    ],
    "function_call": "auto"
  }'
```

### Google Gemini格式

对于Gemini模型，您也可以使用其原生格式：
```
POST https://api.aisa.one/v1/models/gemini-2.5-flash:generateContent
```

```bash
curl -X POST "https://api.aisa.one/v1/models/gemini-2.5-flash:generateContent" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [{"text": "Explain machine learning."}]
      }
    ],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 1000
    }
  }'
```

## Python客户端

### 安装

无需安装，仅使用标准库。

### 命令行接口（CLI）使用方法
```bash
# Basic completion
python3 {baseDir}/scripts/llm_router_client.py chat --model gpt-4.1 --message "Hello, world!"

# With system prompt
python3 {baseDir}/scripts/llm_router_client.py chat --model claude-sonnet-4-5 --system "You are a poet" --message "Write about the moon"

# Streaming
python3 {baseDir}/scripts/llm_router_client.py chat --model gpt-4o --message "Tell me a story" --stream

# Multi-turn conversation
python3 {baseDir}/scripts/llm_router_client.py chat --model gpt-4.1 --messages '[{"role":"user","content":"Hi"},{"role":"assistant","content":"Hello!"},{"role":"user","content":"How are you?"}]'

# Vision analysis
python3 {baseDir}/scripts/llm_router_client.py vision --model gpt-4o --image "https://example.com/image.jpg" --prompt "Describe this image"

# List supported models
python3 {baseDir}/scripts/llm_router_client.py models

# Compare models
python3 {baseDir}/scripts/llm_router_client.py compare --models "gpt-4.1,claude-sonnet-4-5,gemini-2.5-flash" --message "What is 2+2?"
```

### Python SDK使用方法
```python
from llm_router_client import LLMRouterClient

client = LLMRouterClient()  # Uses AISA_API_KEY env var

# Simple chat
response = client.chat(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response["choices"][0]["message"]["content"])

# With options
response = client.chat(
    model="claude-3-sonnet",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain relativity."}
    ],
    temperature=0.7,
    max_tokens=500
)

# Streaming
for chunk in client.chat_stream(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a story."}]
):
    print(chunk, end="", flush=True)

# Vision
response = client.vision(
    model="gpt-4o",
    image_url="https://example.com/image.jpg",
    prompt="What's in this image?"
)

# Compare models
results = client.compare_models(
    models=["gpt-4.1", "claude-sonnet-4-5", "gemini-2.5-flash"],
    message="Explain quantum computing"
)
for model, result in results.items():
    print(f"{model}: {result['response'][:100]}...")
```

## 使用场景

### 1. 成本优化路由

对于简单任务，使用成本更低的模型：
```python
def smart_route(message: str) -> str:
    # Simple queries -> fast/cheap model
    if len(message) < 50:
        model = "gpt-3.5-turbo"
    # Complex reasoning -> powerful model
    else:
        model = "gpt-4.1"
    
    return client.chat(model=model, messages=[{"role": "user", "content": message}])
```

### 2. 回退策略

在发生故障时自动切换到备用模型：
```python
def chat_with_fallback(message: str) -> str:
    models = ["gpt-4.1", "claude-sonnet-4-5", "gemini-2.5-flash"]
    
    for model in models:
        try:
            return client.chat(model=model, messages=[{"role": "user", "content": message}])
        except Exception:
            continue
    
    raise Exception("All models failed")
```

### 3. 模型A/B测试

比较不同模型的输出：
```python
results = client.compare_models(
    models=["gpt-4.1", "claude-opus-4-1"],
    message="Analyze this quarterly report..."
)

# Log for analysis
for model, result in results.items():
    log_response(model=model, latency=result["latency"], cost=result["cost"])
```

### 4. 选择最适合任务的模型

为每个任务选择最佳模型：
```python
MODEL_MAP = {
    "code": "gpt-4.1",
    "creative": "claude-opus-4-1",
    "fast": "gemini-2.5-flash",
    "vision": "gpt-4o",
    "reasoning": "o1",
    "open_source": "llama-3.1-70b"
}

def route_by_task(task_type: str, message: str) -> str:
    model = MODEL_MAP.get(task_type, "gpt-4.1")
    return client.chat(model=model, messages=[{"role": "user", "content": message}])
```

## 错误处理

错误会以JSON格式返回，其中包含`error`字段：

```json
{
  "error": {
    "code": "model_not_found",
    "message": "Model 'xyz' is not available"
  }
}
```

常见错误代码：
- `401` - API密钥无效或缺失
- `402` - 信用不足
- `404` - 模型未找到
- `429` - 超过使用频率限制
- `500` - 服务器错误

## 最佳实践

1. **使用流式响应**以提升用户体验
2. **设置`max_tokens`以控制成本
3. **实现回退机制**以确保系统可靠性
4. **缓存响应**以减少重复请求
5. **通过响应元数据监控使用情况**
6. **根据任务选择合适的模型**——不要对简单任务使用GPT-4

## OpenAI SDK兼容性

只需更改基础URL和API密钥即可：
```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["AISA_API_KEY"],
    base_url="https://api.aisa.one/v1"
)

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

## 价格

费用按模型计费，具体价格请查看[marketplace.aisa.one/pricing](https://marketplace.aisa.one/pricing)。

| 模型家族 | 大约费用 |
|--------------|------------------|
| GPT-4.1 / GPT-4o | 约0.01美元/1000个token |
| Claude-3-Sonnet | 约0.01美元/1000个token |
| Gemini-2.5-Flash | 约0.001美元/1000个token |
| Grok-2 | 约0.01美元/1000个token |
| Llama-3.1-70b | 约0.002美元/1000个token |
| Mistral-Large | 约0.008美元/1000个token |

每个响应都会包含`usage.cost`和`usage.credits_remaining`字段。

## 开始使用

1. 在[aisa.one](https://aisa.one)注册
2. 从控制面板获取API密钥
3. 购买信用（按需付费）
4. 设置环境变量：`export AISA_API_KEY="your-key"`

## 完整API参考

请参阅[API参考](https://aisa.mintlify.app/api-reference/introduction)以获取完整的端点文档。