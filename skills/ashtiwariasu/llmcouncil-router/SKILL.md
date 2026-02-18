---
name: llmcouncil-router
description: 根据 LLM Council 的同行评审排名结果，将任何提示（prompt）路由到性能最佳的 large language model（LLM）。
homepage: https://llmcouncil.ai
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["LLMCOUNCIL_API_KEY"]},"emoji":"🧠"}}
---
# LLM Council Router

该工具会将用户输入的任何提示（prompt）路由到性能最佳的Large Language Model（LLM）模型。该API会根据数千次经过同行评审的评估结果，为特定查询找到表现最佳的模型，然后您可以直接调用该模型。

## 基本URL

```
https://clawbot.llmcouncil.ai
```

## 认证

在使用LLM Council API时，请在请求头中添加`X-API-Key`字段，该字段包含您的API密钥。

```
X-API-Key: clwb_YOUR_KEY_HERE
```

您可以在[llmcouncil.ai/developers](https://llmcouncil.ai/developers)获取免费的API密钥。

## 端点：POST /v1/route

该端点用于查找针对特定查询表现最佳的模型。

### 请求参数

```json
{
  "query": "Explain quantum entanglement simply",
  "k": 20
}
```

| 参数名 | 类型 | 是否必填 | 说明 |
|---------|--------|---------|-------------------|
| `query`   | string  | 是      | 需要路由的提示或问题             |
| `k`     | integer | 否      | 考虑的过去评估次数（默认值：20）         |

### 响应参数

```json
{
  "query": "Explain quantum entanglement simply",
  "nearest_councils": 20,
  "model": "anthropic/claude-sonnet-4",
  "relevance": 0.8234,
  "confidence": 0.65,
  "model_rankings": [
    { "rank": 1, "model": "anthropic/claude-sonnet-4", "nearby_wins": 13, "nearby_appearances": 20 },
    { "rank": 2, "model": "openai/gpt-4.1", "nearby_wins": 5, "nearby_appearances": 18 }
  ]
}
```

| 参数名 | 类型 | 说明                |
|---------|--------|-------------------|
| `model`    | string  | 推荐的最佳模型ID（与OpenRouter目录匹配）     |
| `relevance` | float   | 评估结果与查询的匹配程度（0–1）     | 大于0.75表示匹配度高             |
| `confidence` | float   | 最佳模型相较于其他模型的优势程度（0–1） | 数值越高，优势越明显             |
| `nearest_councils` | integer | 使用的相关过去评估次数           |
| `model_rankings` | array  | 所有模型在匹配评估中的排名列表       |

## 使用方法

当用户请求您为某项任务寻找最佳模型，或者您需要决定使用哪个LLM模型时，请按照以下步骤操作：

1. 使用用户的查询内容调用路由API：

```bash
curl -X POST https://clawbot.llmcouncil.ai/v1/route \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $LLMCOUNCIL_API_KEY" \
  -d '{"query": "USER_QUERY_HERE"}'
```

2. 阅读响应结果——`model`字段中存储的就是针对该查询类型表现最佳的模型ID。

3. 通过OpenRouter进一步处理该模型ID——模型ID可以直接与OpenRouter目录进行匹配，无需额外映射：

```python
import requests, os

# Step 1: Get the best model from LLM Council
route = requests.post(
    "https://clawbot.llmcouncil.ai/v1/route",
    headers={"X-API-Key": os.environ["LLMCOUNCIL_API_KEY"]},
    json={"query": "Write a Python web scraper"},
).json()

best_model = route["model"]       # e.g. "anthropic/claude-sonnet-4"
confidence = route["confidence"]   # e.g. 0.85

# Step 2: Call that model via OpenRouter
answer = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
    json={
        "model": best_model,
        "messages": [{"role": "user", "content": "Write a Python web scraper"}],
    },
).json()

print(answer["choices"][0]["message"]["content"])
```

## 速率限制

| 等级 | 每日请求量 | 限制说明           |
|------|------------|-------------------|
| 免费账户 | 100次请求/天    | 必须遵守                 |
| 专业账户 | 10,000次请求/天    | 无额外限制                 |

## 使用场景

- 用户询问“哪个模型最适合处理某项任务？”
- 您需要为特定任务类型选择最佳模型
- 您希望基于数据驱动的方式选择模型，而非凭直觉判断
- 您希望将模型路由功能与OpenRouter结合使用，以实现自动选择最佳模型