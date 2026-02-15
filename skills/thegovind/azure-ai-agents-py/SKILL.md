---
name: azure-ai-agents-py
description: 使用 Azure AI Agents Python SDK (azure-ai-agents) 构建 AI 代理。该 SDK 适用于在 Azure AI Foundry 上托管代理时，涉及以下功能：文件搜索、代码解释、Bing Grounding、Azure AI Search、函数调用、OpenAPI、MCP 等工具的使用；线程和消息的管理；流式响应的实现；以及与向量存储的交互。这是一个低级别的 SDK——如需更高层次的抽象功能，请使用 agent-framework 技能。
package: azure-ai-agents
---

# Azure AI Agents Python SDK

使用 `azure-ai-agents` SDK 在 Azure AI Foundry 上构建代理。

## 安装

```bash
pip install azure-ai-agents azure-identity
# Or with azure-ai-projects for additional features
pip install azure-ai-projects azure-identity
```

## 环境变量

```bash
PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
```

## 认证

```python
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient

credential = DefaultAzureCredential()
client = AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=credential,
)
```

## 核心工作流程

代理的基本生命周期：**创建代理 → 创建线程 → 创建消息 → 启动运行 → 获取响应**

### 最小示例

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient

client = AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# 1. Create agent
agent = client.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are a helpful assistant.",
)

# 2. Create thread
thread = client.threads.create()

# 3. Add message
client.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hello!",
)

# 4. Create and process run
run = client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

# 5. Get response
if run.status == "completed":
    messages = client.messages.list(thread_id=thread.id)
    for msg in messages:
        if msg.role == "assistant":
            print(msg.content[0].text.value)

# Cleanup
client.delete_agent(agent.id)
```

## 工具概述

| 工具 | 类 | 用途 |
|------|-------|----------|
| 代码解释器 | `CodeInterpreterTool` | 执行 Python 代码、生成文件 |
| 文件搜索 | `FileSearchTool` | 对上传的文档进行检索 |
| Bing 地理信息查询 | `BingGroundingTool` | 进行网络搜索 |
| Azure AI 搜索 | `AzureAISearchTool` | 在索引中搜索 |
| 函数调用 | `FunctionTool` | 调用 Python 函数 |
| OpenAPI | `OpenApiTool` | 调用 REST API |
| MCP | `McpTool` | 模型上下文协议服务器 |

详细的使用模式请参阅 [references/tools.md](references/tools.md)。

## 添加工具

```python
from azure.ai.agents import CodeInterpreterTool, FileSearchTool

agent = client.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="tool-agent",
    instructions="You can execute code and search files.",
    tools=[CodeInterpreterTool()],
    tool_resources={"code_interpreter": {"file_ids": [file.id]}},
)
```

## 函数调用

```python
from azure.ai.agents import FunctionTool, ToolSet

def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 72F, sunny"

functions = FunctionTool(functions=[get_weather])
toolset = ToolSet()
toolset.add(functions)

agent = client.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="function-agent",
    instructions="Help with weather queries.",
    toolset=toolset,
)

# Process run - toolset auto-executes functions
run = client.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
    toolset=toolset,  # Pass toolset for auto-execution
)
```

## 流式处理

```python
from azure.ai.agents import AgentEventHandler

class MyHandler(AgentEventHandler):
    def on_message_delta(self, delta):
        if delta.text:
            print(delta.text.value, end="", flush=True)

    def on_error(self, data):
        print(f"Error: {data}")

with client.runs.stream(
    thread_id=thread.id,
    agent_id=agent.id,
    event_handler=MyHandler(),
) as stream:
    stream.until_done()
```

有关高级处理模式的详细信息，请参阅 [references/streaming.md](references/streaming.md)。

## 文件操作

### 上传文件

```python
file = client.files.upload_and_poll(
    file_path="data.csv",
    purpose="assistants",
)
```

### 创建向量存储

```python
vector_store = client.vector_stores.create_and_poll(
    file_ids=[file.id],
    name="my-store",
)

agent = client.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    tools=[FileSearchTool()],
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)
```

## 异步客户端

```python
from azure.ai.agents.aio import AgentsClient

async with AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
) as client:
    agent = await client.create_agent(...)
    # ... async operations
```

有关异步客户端使用的详细信息，请参阅 [references/async-patterns.md](references/async-patterns.md)。

## 响应格式

### JSON 模式

```python
agent = client.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    response_format={"type": "json_object"},
)
```

### JSON 架构

```python
agent = client.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "weather_response",
            "schema": {
                "type": "object",
                "properties": {
                    "temperature": {"type": "number"},
                    "conditions": {"type": "string"},
                },
                "required": ["temperature", "conditions"],
            },
        },
    },
)
```

## 线程管理

### 继续对话

```python
# Save thread_id for later
thread_id = thread.id

# Resume later
client.messages.create(
    thread_id=thread_id,
    role="user",
    content="Follow-up question",
)
run = client.runs.create_and_process(thread_id=thread_id, agent_id=agent.id)
```

### 列出消息

```python
messages = client.messages.list(thread_id=thread.id, order="asc")
for msg in messages:
    role = msg.role
    content = msg.content[0].text.value
    print(f"{role}: {content}")
```

## 最佳实践

1. 对于异步客户端，使用上下文管理器。
2. 使用完代理后及时清理资源：`client.delete_agent(agent.id)`
3. 对于简单场景使用 `create_and_process`，对于实时用户体验使用流式处理（streaming）。
4. 通过 `run` 方法传递工具集以自动执行函数。
5. 对于耗时较长的操作，使用 `*_and_poll` 方法进行轮询。

## 参考文件

- [references/tools.md](references/tools.md)：所有工具类型及其详细示例
- [references/streaming.md](references/streaming.md)：事件处理器和流式处理模式
- [references/async-patterns.md](references/async-patterns.md)：异步客户端的使用方法