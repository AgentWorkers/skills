---
name: cn-llm
description: "**China LLM Gateway**  
——一个统一的中国大型语言模型（LLM）接口，支持 Qwen、DeepSeek、GLM、Baichuan 等模型。兼容 OpenAI，只需一个 API 密钥即可使用所有模型。"
homepage: https://openclaw.ai
metadata: {"openclaw":{"emoji":"🐉","requires":{"bins":["curl","python3"],"env":["AISA_API_KEY"]},"primaryEnv":"AISA_API_KEY"}}
---

# OpenClaw CN-LLM 🐉  
**中国大语言模型统一入口。由AIsa提供支持。**  

只需一个API密钥，即可访问所有中国的大语言模型。支持OpenAI接口。  
Qwen、DeepSeek、GLM、Baichuan、Moonshot等模型，均可通过统一的API进行访问。  

## 🔥 您可以做什么  

### 智能聊天  
```
"Use Qwen to answer Chinese questions, use DeepSeek for coding"
```  

### 深度推理  
```
"Use DeepSeek-R1 for complex reasoning tasks"
```  

### 代码生成  
```
"Use DeepSeek-Coder to generate Python code with explanations"
```  

### 长文本处理  
```
"Use Qwen-Long for ultra-long document summarization"
```  

### 模型比较  
```
"Compare response quality between Qwen-Max and DeepSeek-V3"
```  

## 支持的模型  

### Qwen（阿里巴巴）  

| 模型 | 输入价格（百万令牌） | 输出价格（百万令牌） | 特点 |
|-----|---------|---------|------|  
| qwen3-max | $1.37/M | $5.48/M | 最强大的通用模型 |
| qwen3-max-2026-01-23 | $1.37/M | $5.48/M | 最新版本 |
| qwen3-coder-plus | $2.86/M | $28.60/M | 强化的代码生成功能 |
| qwen3-coder-flash | $0.72/M | $3.60/M | 快速代码生成 |
| qwen3-coder-480b-a35b-instruct | $2.15/M | $8.60/M | 480B大型模型 |
| qwen3-vl-plus | $0.43/M | $4.30/M | 视觉语言模型 |
| qwen3-vl-flash | $0.86/M | $0.86/M | 快速视觉模型 |
| qwen3-omni-flash | $4.00/M | $16.00/M | 多模态模型 |
| qwen-vl-max | $0.23/M | $0.57/M | 视觉语言模型 |
| qwen-plus-2025-12-01 | $1.26/M | $12.60/M | 升级版本 |
| qwen-mt-flash | $0.168/M | $0.514/M | 快速机器翻译 |
| qwen-mt-lite | $0.13/M | $0.39/M | 简易机器翻译 |

### DeepSeek  

| 模型 | 输入价格（百万令牌） | 输出价格（百万令牌） | 特点 |
|-----|---------|---------|------|  
| deepseek-r1 | $2.00/M | $8.00/M | 推理模型，支持工具使用 |
| deepseek-v3 | $1.00/M | $4.00/M | 通用聊天模型，参数量671B |
| deepseek-v3-0324 | $1.20/M | $4.80/M | V3稳定版本 |
| deepseek-v3.1 | $4.00/M | $12.00/M | 最新Terminus版本 |

> **注意**：价格以百万令牌（M）为单位。模型可用性可能会发生变化，请访问[marketplace.aisa.one/pricing](https://marketplace.aisa.one/pricing)获取最新列表。  

## 快速入门  
```bash
export AISA_API_KEY="your-key"
```  

## API端点  
```
POST https://api.aisa.one/v1/chat/completions
```  

### 兼容OpenAI的接口  
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-max",
    "messages": [
      {"role": "system", "content": "You are a professional Chinese assistant."},
      {"role": "user", "content": "Please explain what a large language model is?"}
    ],
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```  

#### Qwen示例  
```bash
# DeepSeek-V3 general chat (671B parameters)
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v3",
    "messages": [{"role": "user", "content": "Write a quicksort algorithm in Python"}],
    "temperature": 0.3
  }'

# DeepSeek-R1 deep reasoning (supports Tools)
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-r1",
    "messages": [{"role": "user", "content": "A farmer needs to cross a river with a wolf, a sheep, and a cabbage. The boat can only carry the farmer and one item at a time. If the farmer is not present, the wolf will eat the sheep, and the sheep will eat the cabbage. How can the farmer safely cross?"}]
  }'

# DeepSeek-V3.1 Terminus latest version
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v3.1",
    "messages": [{"role": "user", "content": "Implement an LRU cache with get and put operations"}]
  }'
```  

#### DeepSeek示例  
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-coder-plus",
    "messages": [{"role": "user", "content": "Implement a thread-safe Map in Go"}]
  }'
```  

#### Qwen3代码生成示例  
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "qwen-max",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "A large language model (LLM) is a deep learning-based..."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 30,
    "completion_tokens": 150,
    "total_tokens": 180,
    "cost": 0.001
  }
}
```  

#### 参数参考  
| 参数 | 类型 | 是否必填 | 说明 |
|-----|------|-----|------|  
| `model` | string | 是 | 模型标识符 |
| `messages` | array | 是 | 消息列表 |
| `temperature` | number | 否 | 随机性（0-2，默认1） |
| `max_tokens` | integer | 否 | 生成的最大令牌数 |
| `stream` | boolean | 否 | 流式输出（默认为false） |
| `top_p` | number | 否 | 核心采样参数（0-1） |

#### 响应格式  
```bash
curl -X POST "https://api.aisa.one/v1/chat/completions" \
  -H "Authorization: Bearer $AISA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-plus",
    "messages": [{"role": "user", "content": "Tell a Chinese folk story"}],
    "stream": true
  }'
```  

### 流式输出  
```
data: {"id":"chatcmpl-xxx","choices":[{"delta":{"content":"Once"}}]}
data: {"id":"chatcmpl-xxx","choices":[{"delta":{"content":" upon"}}]}
...
data: [DONE]
```  
返回服务器发送的事件（SSE）格式：  

```bash
# Qwen chat
python3 {baseDir}/scripts/cn_llm_client.py chat --model qwen3-max --message "Hello, please introduce yourself"

# Qwen3 code generation
python3 {baseDir}/scripts/cn_llm_client.py chat --model qwen3-coder-plus --message "Write a binary search algorithm"

# DeepSeek-R1 reasoning
python3 {baseDir}/scripts/cn_llm_client.py chat --model deepseek-r1 --message "Which is larger, 9.9 or 9.11? Please reason in detail"

# DeepSeek-V3 chat
python3 {baseDir}/scripts/cn_llm_client.py chat --model deepseek-v3 --message "Tell a story" --stream

# With system prompt
python3 {baseDir}/scripts/cn_llm_client.py chat --model qwen3-max --system "You are a classical poetry expert" --message "Write a poem about plum blossoms"

# Model comparison
python3 {baseDir}/scripts/cn_llm_client.py compare --models "qwen3-max,deepseek-v3" --message "What is quantum computing?"

# List supported models
python3 {baseDir}/scripts/cn_llm_client.py models
```  

## Python客户端  
```python
from cn_llm_client import CNLLMClient

client = CNLLMClient()  # Uses AISA_API_KEY environment variable

# Qwen chat
response = client.chat(
    model="qwen3-max",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response["choices"][0]["message"]["content"])

# Qwen3 code generation
response = client.chat(
    model="qwen3-coder-plus",
    messages=[
        {"role": "system", "content": "You are a professional programmer."},
        {"role": "user", "content": "Implement a singleton pattern in Python"}
    ],
    temperature=0.3
)

# Streaming output
for chunk in client.chat_stream(
    model="deepseek-v3",
    messages=[{"role": "user", "content": "Tell a story about an idiom"}]
):
    print(chunk, end="", flush=True)

# Model comparison
results = client.compare_models(
    models=["qwen3-max", "deepseek-v3", "deepseek-r1"],
    message="Explain what machine learning is"
)
for model, result in results.items():
    print(f"{model}: {result['response'][:100]}...")
```  

## CLI使用  
```python
# Copywriting
response = client.chat(
    model="qwen3-max",
    messages=[
        {"role": "system", "content": "You are a professional copywriter."},
        {"role": "user", "content": "Write a product introduction for a smart watch"}
    ]
)
```  

## Python SDK使用  
```python
# Code generation and explanation
response = client.chat(
    model="qwen3-coder-plus",
    messages=[{"role": "user", "content": "Implement a thread-safe Map in Go"}]
)
```  

## 使用场景  

### 1. 中文内容生成  
```python
# Mathematical reasoning
response = client.chat(
    model="deepseek-r1",
    messages=[{"role": "user", "content": "Prove: For any positive integer n, n³-n is divisible by 6"}]
)
```  

### 2. 代码开发  
```python
# Image understanding
response = client.chat(
    model="qwen3-vl-plus",
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "Describe the content of this image"},
            {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]}
    ]
)
```  

### 3. 复杂推理  
```python
MODEL_MAP = {
    "chat": "qwen3-max",           # General chat
    "code": "qwen3-coder-plus",    # Code generation
    "reasoning": "deepseek-r1",    # Complex reasoning
    "vision": "qwen3-vl-plus",     # Visual understanding
    "fast": "qwen3-coder-flash",   # Fast response
    "translate": "qwen-mt-flash"   # Machine translation
}

def route_by_task(task_type: str, message: str) -> str:
    model = MODEL_MAP.get(task_type, "qwen3-max")
    return client.chat(model=model, messages=[{"role": "user", "content": message}])
```  

### 4. 视觉理解  
```json
{
  "error": {
    "code": "model_not_found",
    "message": "Model 'xxx' is not available"
  }
}
```  

### 5. 模型路由策略  
___CODE_BLOCK_21___  

## 错误处理  
错误会以JSON格式返回，其中包含`error`字段：  
___CODE_BLOCK_22___  
常见错误代码：  
- `401` - API密钥无效或缺失  
- `402` - 账户余额不足  
- `404` - 模型未找到  
- `429` - 超过请求频率限制  
- `500` - 服务器错误  

## 价格  
| 模型 | 输入价格（百万令牌） | 输出价格（百万令牌） |
|-----|-----------|-----------|  
| qwen3-max | $1.37 | $5.48 |
| qwen3-coder-plus | $2.86 | $28.60 |
| qwen3-coder-flash | $0.72 | $3.60 |
| qwen3-vl-plus | $0.43 | $4.30 |
| deepseek-v3 | $1.00 | $4.00 |
| deepseek-r1 | $2.00 | $8.00 |
| deepseek-v3.1 | $4.00 | $12.00 |

> 价格单位：每百万令牌（$）。每个响应包含`usage.cost`和`usage.credits_remaining`信息。  

## 开始使用  
1. 在[aisa.one](https://aisa.one)注册  
2. 获取API密钥  
3. 充值（按需付费）  
4. 设置环境变量：`export AISA_API_KEY="your-key"`  

## 完整API参考  
请参阅[API参考](https://aisa.mintlify.app/api-reference/introduction)以获取完整的端点文档。