---
name: azure-ai-projects-py
description: 使用 Azure AI Projects Python SDK (azure-ai-projects) 构建 AI 应用程序。该 SDK 适用于与 Foundry 项目客户端协作、使用 PromptAgentDefinition 创建版本化的代理、运行评估任务、管理连接/部署/数据集/索引，以及使用兼容 OpenAI 的客户端。这是一款高级别的 Foundry SDK；如需进行低级别的代理操作，请使用 azure-ai-agents-python SDK。
package: azure-ai-projects
---

# Azure AI 项目 Python SDK（Azure AI Foundry SDK）

使用 `azure-ai-projects` SDK 在 Azure AI Foundry 上构建 AI 应用程序。

## 安装

```bash
pip install azure-ai-projects azure-identity
```

## 环境变量

```bash
AZURE_AI_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
```

## 认证

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

credential = DefaultAzureCredential()
client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=credential,
)
```

## 客户端操作概述

| 操作        | 访问权限    | 目的                |
|-------------|-----------|-------------------|
| `client.agents`   | `.agents.*`    | 管理代理（创建、读取、更新、删除）、代理版本、线程、运行状态 |
| `client.connections` | `.connections.*` | 列出/获取项目连接信息       |
| `client.deployments` | `.deployments.*` | 管理模型部署           |
| `client.datasets` | `.datasets.*` | 管理数据集             |
| `client.indexes` | `.indexes.*` | 管理索引             |
| `client.evaluations` | `.evaluations.*` | 运行评估任务           |
| `client.red_teams` | `.red_teams.*` | 管理红队相关操作           |

## 两种客户端实现方式

### 1. AIProjectClient（Azure AI Foundry 的原生客户端）

```python
from azure.ai.projects import AIProjectClient

client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Use Foundry-native operations
agent = client.agents.create_agent(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are helpful.",
)
```

### 2. 兼容 OpenAI 的客户端

```python
# Get OpenAI-compatible client from project
openai_client = client.get_openai_client()

# Use standard OpenAI API
response = openai_client.chat.completions.create(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    messages=[{"role": "user", "content": "Hello!"}],
)
```

## 代理操作

### 创建代理（基础操作）

```python
agent = client.agents.create_agent(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are a helpful assistant.",
)
```

### 使用工具创建代理

```python
from azure.ai.agents import CodeInterpreterTool, FileSearchTool

agent = client.agents.create_agent(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    name="tool-agent",
    instructions="You can execute code and search files.",
    tools=[CodeInterpreterTool(), FileSearchTool()],
)
```

### 使用 `PromptAgentDefinition` 创建带版本控制的代理

```python
from azure.ai.projects.models import PromptAgentDefinition

# Create a versioned agent
agent_version = client.agents.create_version(
    agent_name="customer-support-agent",
    definition=PromptAgentDefinition(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        instructions="You are a customer support specialist.",
        tools=[],  # Add tools as needed
    ),
    version_label="v1.0",
)
```

有关代理的详细信息，请参阅 [references/agents.md](references/agents.md)。

## 工具概述

| 工具        | 类型        | 用途                |
|------------|------------|-------------------|
| 代码解释器    | `CodeInterpreterTool` | 执行 Python 代码、生成文件        |
| 文件搜索工具    | `FileSearchTool` | 对上传的文档进行检索          |
| Bing 搜索工具    | `BingGroundingTool` | 使用 Bing 进行网络搜索（需连接网络）     |
| Azure AI 搜索工具 | `AzureAISearchTool` | 在索引中搜索             |
| 函数调用工具    | `FunctionTool` | 调用 Python 函数           |
| OpenAPI 工具    | `OpenApiTool` | 调用 REST API            |
| MCP 工具      | `McpTool`     | 用于模型上下文协议的服务器       |
| 内存搜索工具    | `MemorySearchTool` | 搜索代理的内存存储           |
| SharePoint 工具    | `SharepointGroundingTool` | 在 SharePoint 中搜索           |

有关所有工具的详细信息，请参阅 [references/tools.md](references/tools.md)。

## 线程与消息流

```python
# 1. Create thread
thread = client.agents.threads.create()

# 2. Add message
client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="What's the weather like?",
)

# 3. Create and process run
run = client.agents.runs.create_and_process(
    thread_id=thread.id,
    agent_id=agent.id,
)

# 4. Get response
if run.status == "completed":
    messages = client.agents.messages.list(thread_id=thread.id)
    for msg in messages:
        if msg.role == "assistant":
            print(msg.content[0].text.value)
```

## 连接管理

```python
# List all connections
connections = client.connections.list()
for conn in connections:
    print(f"{conn.name}: {conn.connection_type}")

# Get specific connection
connection = client.connections.get(connection_name="my-search-connection")
```

有关连接管理的详细信息，请参阅 [references/connections.md](references/connections.md)。

## 部署管理

```python
# List available model deployments
deployments = client.deployments.list()
for deployment in deployments:
    print(f"{deployment.name}: {deployment.model}")
```

有关部署管理的详细信息，请参阅 [references/deployments.md](references/deployments.md)。

## 数据集与索引管理

```python
# List datasets
datasets = client.datasets.list()

# List indexes
indexes = client.indexes.list()
```

有关数据集和索引管理的详细信息，请参阅 [references/datasets-indexes.md](references/datasets-indexes.md)。

## 评估操作

```python
# Using OpenAI client for evals
openai_client = client.get_openai_client()

# Create evaluation with built-in evaluators
eval_run = openai_client.evals.runs.create(
    eval_id="my-eval",
    name="quality-check",
    data_source={
        "type": "custom",
        "item_references": [{"item_id": "test-1"}],
    },
    testing_criteria=[
        {"type": "fluency"},
        {"type": "task_adherence"},
    ],
)
```

有关评估操作的详细信息，请参阅 [references/evaluation.md](references/evaluation.md)。

## 异步客户端

```python
from azure.ai.projects.aio import AIProjectClient

async with AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
) as client:
    agent = await client.agents.create_agent(...)
    # ... async operations
```

有关异步客户端的使用方式，请参阅 [references/async-patterns.md](references/async-patterns.md)。

## 内存存储

```python
# Create memory store for agent
memory_store = client.agents.create_memory_store(
    name="conversation-memory",
)

# Attach to agent for persistent memory
agent = client.agents.create_agent(
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    name="memory-agent",
    tools=[MemorySearchTool()],
    tool_resources={"memory": {"store_ids": [memory_store.id]}},
)
```

## 最佳实践

1. 对于异步客户端，请使用上下文管理器：`async with AIProjectClient(...) as client:`
2. 使用完代理后，请及时删除它们：`client.agents.delete_agent(agent.id)`
3. 对于简单的运行任务，使用 `create_and_process` 方法；对于实时用户体验，使用流式处理（streaming）方法。
4. 在生产环境中部署时，建议使用带版本控制的代理。
5. 在集成外部服务（如 Azure AI 搜索、Bing 等）时，优先使用连接（connections）。

## SDK 对比

| 功能        | `azure-ai-projects` | `azure-ai-agents`       |
|------------|-------------------|-------------------|
| 级别        | 高层（针对整个 Azure AI Foundry）| 低层（针对代理管理）       |
| 客户端类型    | `AIProjectClient`     | `AgentsClient`        |
| 版本控制      | 支持版本控制          | 不支持版本控制         |
| 连接管理    | 支持连接管理        | 不支持连接管理         |
| 部署管理    | 支持模型部署        | 不支持模型部署         |
| 数据集/索引管理 | 支持数据集和索引管理     | 不支持数据集和索引管理     |
| 评估功能    | 通过 OpenAI 客户端进行评估   | 不支持独立评估功能       |
| 使用场景      | 适用于完整的 Azure AI Foundry 集成 | 适用于独立的代理应用程序     |

## 参考文件

- [references/agents.md](references/agents.md): 带有 `PromptAgentDefinition` 的代理操作
- [references/tools.md](references/tools.md): 所有代理工具及其使用示例
- [references/evaluation.md](references/evaluation.md): 评估操作及内置评估器
- [references/connections.md](references/connections.md): 连接管理相关内容
- [references/deployments.md](references/deployments.md): 部署管理相关内容
- [references/datasets-indexes.md](references/datasets-indexes.md): 数据集和索引管理相关内容
- [references/async-patterns.md](references/async-patterns.md): 异步客户端的使用方式