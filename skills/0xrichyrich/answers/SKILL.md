---
name: answers
description: "**用途：**  
用于通过兼容 OpenAI 的 `/chat/completions` 功能生成基于人工智能的答案。提供两种模式：  
1. **单次搜索**（快速响应）；  
2. **深度研究**（`enable_research=true`，进行详尽的多轮搜索）。  
支持数据流式传输或阻塞式处理方式，并支持引用相关资料。"
---
# Answers — 基于AI的问答服务

> **需要API密钥**：请在 [https://api.search.brave.com](https://api.search.brave.com) 获取API密钥。

> **计划**：该功能包含在“Answers”计划中。详情请参阅 [https://api-dashboard.search.brave.com/app/subscriptions/subscribe](https://api-dashboard.search.brave.com/app/subscriptions/subscribe)。

## 使用场景

| 使用场景 | 所需技能 | 原因 |
|--|--|--|
| 快速提供事实性答案（原始上下文） | `llm-context` | 通过单次搜索，返回给您的LLM（大型语言模型）的原始上下文 |
| 带有引用的快速AI答案 | **`answers`**（单次搜索） | 提供实时流式输出及引用信息 |
| 详细的多源深度研究 | **`answers`**（研究模式） | 进行多次搜索并合成带有引用的答案 |

**此端点`/res/v1/chat/completions`**支持两种模式：**
- **单次搜索**（默认）：通过单次搜索快速获得基于AI的答案，支持`enable_citations`选项。
- **研究模式**（`enable_research=true`）：进行多次迭代深度搜索，提供进度信息及合成后的引用答案。

## 快速入门（cURL示例）

### 单次搜索（阻塞式响应）
```bash
curl -X POST "https://api.search.brave.com/res/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -d '{
    "messages": [{"role": "user", "content": "How does the James Webb Space Telescope work?"}],
    "model": "brave",
    "stream": false
  }'
```

### 带有引用的流式响应（单次搜索）
```bash
curl -X POST "https://api.search.brave.com/res/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -d '{
    "messages": [{"role": "user", "content": "What are recent breakthroughs in fusion energy?"}],
    "model": "brave",
    "stream": true,
    "enable_citations": true
  }'
```

### 研究模式
```bash
curl -X POST "https://api.search.brave.com/res/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-Subscription-Token: ${BRAVE_SEARCH_API_KEY}" \
  -d '{
    "messages": [{"role": "user", "content": "Compare quantum computing approaches"}],
    "model": "brave",
    "stream": true,
    "enable_research": true,
    "research_maximum_number_of_iterations": 3,
    "research_maximum_number_of_seconds": 120
  }'
```

## 端点信息

```http
POST https://api.search.brave.com/res/v1/chat/completions
```

**身份验证**：需要在请求头中添加 `X-Subscription-Token: <API_KEY>`（或 `Authorization: Bearer <API_KEY>`）

**SDK兼容性**：可通过 `base_url="https://api.search.brave.com/res/v1"` 与OpenAI SDK集成。

## 两种模式的区别

| 特性 | 单次搜索（默认） | 研究模式（`enable_research=true`） |
|--|--|--|
| 速度 | 快速 | 较慢 |
| 搜索范围 | 单个查询 | 多次迭代查询 |
| 流式输出 | 可选（`stream=true/false`） | **必需**（`stream=true`） |
| 引用信息 | `enable_citations=true`（仅流式响应时提供） | 内置在 `<answer>` 标签中 |
| 进度信息 | 无 | 有（通过 `<progress>` 标签提供） |
| 响应类型 | 阻塞式响应 | 流式响应 |

## 参数说明

### 标准参数

| 参数 | 类型 | 是否必需 | 默认值 | 说明 |
| `messages` | 数组 | 是 | - | 单条用户输入的消息（必须为1条） |
| `model` | 字符串 | 是 | - | 使用 `"brave"` 模型 |
| `stream` | 布尔值 | 否 | true | 启用SSE流式输出 |
| `country` | 字符串 | 否 | "US" | 搜索国家（2位国家代码或 `ALL`） |
| `language` | 字符串 | 否 | "en" | 响应语言 |
| `safesearch` | 字符串 | 否 | "moderate" | 搜索安全级别（`off`, `moderate`, `strict`） |
| `max_completion_tokens` | 整数 | 否 | null | 答案的最大字符数限制 |
| `enable_citations` | 布尔值 | 否 | false | 是否包含内联引用标签（仅限流式响应） |
| `web_search_options` | 对象 | 否 | null | OpenAI兼容的搜索选项：`search_context_size`（`low`, `medium`, `high`） |

### 研究模式参数

| 参数 | 类型 | 是否必需 | 默认值 | 说明 |
| `enable_research` | 布尔值 | 否 | `false` | 启用研究模式 |
| `research_allow_thinking` | 布尔值 | 否 | `true` | 允许扩展思考过程 |
| `research_maximum_number_of_tokens_per_query` | 整数 | 否 | `8192` | 每次查询的最大字符数 |
| `research_maximum_number_of_queries` | 整数 | 否 | `20` | 最大查询次数（1-50次） |
| `research_maximum_number_of_iterations` | 整数 | 否 | 最大迭代次数（1-5次） |
| `research_maximum_number_of_seconds` | 整数 | 否 | 最大搜索时间（1-300秒） |
| `research_maximum_number_of_results_per_query` | 整数 | 否 | 每次查询的最大结果数（1-60个） |

### 注意事项

- **重要限制**：
  - `enable_research=true` 必须同时设置 `stream=true`，否则会返回阻塞式响应。
  - `enable_research=true` 与 `enable_citations=true` 不兼容，因为研究模式不支持引用功能。
  - `enable_citations=true` 也需要 `stream=true`，否则会返回阻塞式响应。

## OpenAI SDK使用示例

### 单次搜索（阻塞式响应）
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.search.brave.com/res/v1",
    api_key="your-brave-api-key",
)

response = client.chat.completions.create(
    model="brave",
    messages=[{"role": "user", "content": "How does the James Webb Space Telescope work?"}],
    stream=False,
)
print(response.choices[0].message.content)
```

### 带有引用的流式响应（单次搜索）
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.search.brave.com/res/v1",
    api_key="your-brave-api-key",
)

stream = client.chat.completions.create(
    model="brave",
    messages=[{"role": "user", "content": "What are the current trends in renewable energy?"}],
    stream=True,
    extra_body={"enable_citations": True}
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### 研究模式
```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://api.search.brave.com/res/v1",
    api_key="your-brave-api-key",
)

stream = await client.chat.completions.create(
    model="brave",
    messages=[{"role": "user", "content": "Compare quantum computing approaches"}],
    stream=True,
    extra_body={
        "enable_research": True,
        "research_maximum_number_of_iterations": 3,
        "research_maximum_number_of_seconds": 120
    }
)

async for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## 响应格式

### 阻塞式响应（`stream=false`，仅单次搜索）

符合OpenAI标准的JSON响应：
```json
{
  "id": "chatcmpl-...",
  "object": "chat.completion",
  "choices": [{"message": {"role": "assistant", "content": "The James Webb Space Telescope works by..."}, "index": 0, "finish_reason": "stop"}],
  "usage": {"prompt_tokens": 10, "completion_tokens": 50, "total_tokens": 60}
}
```

### 流式响应

采用SSE格式的响应，包含OpenAI兼容的数据块：
```text
data: {"id":"chatcmpl-...","object":"chat.completion.chunk","choices":[{"delta":{"content":"Based on"},"index":0}]}

data: {"id":"chatcmpl-...","object":"chat.completion.chunk","choices":[{"delta":{"content":" recent research"},"index":0}]}

data: [DONE]
```

### 不同模式下的流式响应标签

#### 单次搜索（`enable_citations=true`）

| 标签 | 用途 |
|--|--|
| `<citation>` | 内联引用链接 |
| `<usage>` | JSON格式的成本/计费信息 |

#### 研究模式

| 标签 | 用途 | 是否保留？ |
|--|--|--|
| `<queries>` | 生成的搜索查询 | 调试用 |
| `<analyzing>` | 分析的URL数量 | 调试用 |
| `<thinking>` | URL选择逻辑 | 调试用 |
| `<progress>` | 进度信息：耗时、迭代次数、查询次数、分析的URL数量、使用的字符数 | 监控用 |
| `<blindspots>` | 识别出的知识空白 | 是 |
| `<answer>` | 最终合成答案（仅输出最终答案，中间草稿会被丢弃） | 是 |
| `<usage>` | JSON格式的成本/计费信息（包含在流式响应的末尾） | 是 |

### `<usage>` 标签格式

`<usage>` 标签包含格式化的成本和字符数数据：
```text
<usage>{"X-Request-Requests":1,"X-Request-Queries":8,"X-Request-Tokens-In":15000,"X-Request-Tokens-Out":2000,"X-Request-Requests-Cost":0.005,"X-Request-Queries-Cost":0.032,"X-Request-Tokens-In-Cost":0.075,"X-Request-Tokens-Out-Cost":0.01,"X-Request-Total-Cost":0.122}</usage>
```

## 应用场景

- **聊天界面集成**：可以直接使用OpenAI SDK替换原有功能，设置 `base_url="https://api.search.brave.com/res/v1"`。
- **深度研究/综合主题研究**：对于需要多源信息整合的复杂问题（例如“比较核聚变的不同方法”），使用研究模式（`enable_research=true`）。
- **OpenAI SDK集成**：使用相同的SDK和流式响应格式，只需更改 `base_url` 和 `api_key` 即可。支持同步和异步客户端。
- **带引用的答案**：在单次搜索模式下启用 `enable_citations=true` 以显示内联引用；或使用研究模式，答案中会自动包含引用信息。

## 其他注意事项

- **超时设置**：单次搜索的客户端超时时间至少设置为30秒，研究模式的超时时间设置为300秒（5分钟）。
- **单条消息**：`messages` 数组必须包含 exactly 1 条用户输入的消息。
- **成本监控**：通过解析流式响应中的 `<usage>` 标签来跟踪使用成本。