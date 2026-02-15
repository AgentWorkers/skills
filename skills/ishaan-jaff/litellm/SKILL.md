---
name: litellm
description: 通过 LiteLLM 的统一 API，您可以调用 100 多个大型语言模型（LLM）提供商的服务。当您需要使用与当前模型不同的模型时（例如，在使用 Claude 的同时调用 GPT-4 进行代码审查），或者需要比较多个模型的输出结果，又或者需要为简单任务选择成本更低的模型，或者访问您的运行时环境不原生支持的模型时，都可以使用此功能。
---

# LiteLLM - 多模型大语言模型（LLM）调用

当您需要调用超出自己主要模型范围的其他大语言模型（LLM）时，可以使用 LiteLLM。

## 使用场景

- **模型比较**：从多个模型获取输出并进行对比
- **特定任务处理**：使用针对特定任务优化的模型（如代码生成或文本创作）
- **成本优化**：将简单查询路由到成本更低的模型
- **备用模型**：访问运行时未支持的模型

## 快速入门

```python
import litellm

# Call any model with unified API
response = litellm.completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain this code"}]
)
print(response.choices[0].message.content)
```

## 常见用法

### 比较多个模型

```python
import litellm

prompt = [{"role": "user", "content": "What's the best approach to X?"}]

models = ["gpt-4o", "claude-sonnet-4-20250514", "gemini/gemini-1.5-pro"]
for model in models:
    resp = litellm.completion(model=model, messages=prompt)
    print(f"{model}: {resp.choices[0].message.content[:200]}...")
```

### 按任务类型路由请求

```python
import litellm

def smart_call(task_type: str, prompt: str) -> str:
    model_map = {
        "code": "gpt-4o",           # Strong at code
        "writing": "claude-sonnet-4-20250514",  # Strong at prose
        "simple": "gpt-4o-mini",    # Cheap for simple tasks
        "reasoning": "o1-preview",  # Deep reasoning
    }
    model = model_map.get(task_type, "gpt-4o")
    resp = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content
```

### 推荐使用 LiteLLM 代理

如果可用，建议使用 LiteLLM 代理来实现缓存、速率限制和性能监控功能：

```python
import litellm

litellm.api_base = "https://your-litellm-proxy.com"
litellm.api_key = "sk-your-key"

response = litellm.completion(
    model="gpt-4o",  # Proxy routes to configured provider
    messages=[{"role": "user", "content": "Hello"}]
)
```

## 环境配置

确保已安装 `litellm` 并配置好 API 密钥：

```bash
pip install litellm

# Set provider keys (or configure in proxy)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-..."
```

## 模型参考

常见模型标识符：
- **OpenAI**：`gpt-4o`, `gpt-4o-mini`, `o1-preview`, `o1-mini`
- **Anthropic**：`claude-sonnet-4-20250514`, `claude-opus-4-20250514`
- **Google**：`gemini/gemini-1.5-pro`, `gemini/gemini-1.5-flash`
- **Mistral**：`mistral/mistral-large-latest`

完整模型列表：https://docs.litellm.ai/docs/providers