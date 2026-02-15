---
name: agent-framework-azure-ai-py
description: 使用 Microsoft Agent Framework Python SDK（agent-framework-azure-ai）构建 Azure AI Foundry 代理。该 SDK 适用于创建使用 AzureAIAgentsProvider 的持久化代理，这些代理可以执行托管工具（如代码解释器、文件搜索、网络搜索）的功能，集成 MCP 服务器，管理对话线程，以及实现流式响应。文档涵盖了相关功能工具、结构化输出以及多工具代理的实现方法。
package: agent-framework-azure-ai
---

# Azure 托管代理（Agent Framework）

使用 Microsoft Agent Framework Python SDK 在 Azure AI Foundry 上构建持久化代理。

## 架构

```
User Query → AzureAIAgentsProvider → Azure AI Agent Service (Persistent)
                    ↓
              Agent.run() / Agent.run_stream()
                    ↓
              Tools: Functions | Hosted (Code/Search/Web) | MCP
                    ↓
              AgentThread (conversation persistence)
```

## 安装

```bash
# Full framework (recommended)
pip install agent-framework --pre

# Or Azure-specific package only
pip install agent-framework-azure-ai --pre
```

## 环境变量

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://<project>.services.ai.azure.com/api/projects/<project-id>"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o-mini"
export BING_CONNECTION_ID="your-bing-connection-id"  # For web search
```

## 认证

```python
from azure.identity.aio import AzureCliCredential, DefaultAzureCredential

# Development
credential = AzureCliCredential()

# Production
credential = DefaultAzureCredential()
```

## 核心工作流程

### 基本代理（Basic Agent）

```python
import asyncio
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="MyAgent",
            instructions="You are a helpful assistant.",
        )
        
        result = await agent.run("Hello!")
        print(result.text)

asyncio.run(main())
```

### 带有功能工具的代理（Agent with Function Tools）

```python
from typing import Annotated
from pydantic import Field
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

def get_weather(
    location: Annotated[str, Field(description="City name to get weather for")],
) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}: 72°F, sunny"

def get_current_time() -> str:
    """Get the current UTC time."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="WeatherAgent",
            instructions="You help with weather and time queries.",
            tools=[get_weather, get_current_time],  # Pass functions directly
        )
        
        result = await agent.run("What's the weather in Seattle?")
        print(result.text)
```

### 带有托管工具的代理（Agent with Hosted Tools）

```python
from agent_framework import (
    HostedCodeInterpreterTool,
    HostedFileSearchTool,
    HostedWebSearchTool,
)
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="MultiToolAgent",
            instructions="You can execute code, search files, and search the web.",
            tools=[
                HostedCodeInterpreterTool(),
                HostedWebSearchTool(name="Bing"),
            ],
        )
        
        result = await agent.run("Calculate the factorial of 20 in Python")
        print(result.text)
```

### 流式响应（Streaming Responses）

```python
async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="StreamingAgent",
            instructions="You are a helpful assistant.",
        )
        
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream("Tell me a short story"):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()
```

### 对话线程（Conversation Threads）

```python
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="ChatAgent",
            instructions="You are a helpful assistant.",
            tools=[get_weather],
        )
        
        # Create thread for conversation persistence
        thread = agent.get_new_thread()
        
        # First turn
        result1 = await agent.run("What's the weather in Seattle?", thread=thread)
        print(f"Agent: {result1.text}")
        
        # Second turn - context is maintained
        result2 = await agent.run("What about Portland?", thread=thread)
        print(f"Agent: {result2.text}")
        
        # Save thread ID for later resumption
        print(f"Conversation ID: {thread.conversation_id}")
```

### 结构化输出（Structured Outputs）

```python
from pydantic import BaseModel, ConfigDict
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential

class WeatherResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    location: str
    temperature: float
    unit: str
    conditions: str

async def main():
    async with (
        AzureCliCredential() as credential,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="StructuredAgent",
            instructions="Provide weather information in structured format.",
            response_format=WeatherResponse,
        )
        
        result = await agent.run("Weather in Seattle?")
        weather = WeatherResponse.model_validate_json(result.text)
        print(f"{weather.location}: {weather.temperature}°{weather.unit}")
```

## 提供者方法（Provider Methods）

| 方法                | 描述                                      |
|-------------------|-------------------------------------------|
| `create_agent()`       | 在 Azure AI 服务上创建新代理                   |
| `get_agent(agent_id)`     | 通过 ID 获取现有代理                         |
| `as_agent(sdk_agent)`     | 将 SDK 代理对象封装（无需 HTTP 调用）                   |

## 托管工具快速参考（Hosted Tools Quick Reference）

| 工具                | 导入方式                                      | 用途                                      |
|-------------------|-------------------------------------------|-------------------------------------------|
| `HostedCodeInterpreterTool` | `from agent_framework import HostedCodeInterpreterTool` | 执行 Python 代码                         |
| `HostedFileSearchTool` | `from agent_framework import HostedFileSearchTool` | 搜索向量存储                         |
| `HostedWebSearchTool` | `from agent_framework import HostedWebSearchTool` | 使用 Bing 进行网页搜索                         |
| `HostedMCPTool` | `from agent_framework import HostedMCPTool` | 由服务管理的 MCP 工具                         |
| `MCPStreamableHTTPTool` | `from agent_framework import MCPStreamableHTTPTool` | 由客户端管理的 MCP 工具                         |

## 完整示例（Complete Example）

```python
import asyncio
from typing import Annotated
from pydantic import BaseModel, Field
from agent_framework import (
    HostedCodeInterpreterTool,
    HostedWebSearchTool,
    MCPStreamableHTTPTool,
)
from agent_framework.azure import AzureAIAgentsProvider
from azure.identity.aio import AzureCliCredential


def get_weather(
    location: Annotated[str, Field(description="City name")],
) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 72°F, sunny"


class AnalysisResult(BaseModel):
    summary: str
    key_findings: list[str]
    confidence: float


async def main():
    async with (
        AzureCliCredential() as credential,
        MCPStreamableHTTPTool(
            name="Docs MCP",
            url="https://learn.microsoft.com/api/mcp",
        ) as mcp_tool,
        AzureAIAgentsProvider(credential=credential) as provider,
    ):
        agent = await provider.create_agent(
            name="ResearchAssistant",
            instructions="You are a research assistant with multiple capabilities.",
            tools=[
                get_weather,
                HostedCodeInterpreterTool(),
                HostedWebSearchTool(name="Bing"),
                mcp_tool,
            ],
        )
        
        thread = agent.get_new_thread()
        
        # Non-streaming
        result = await agent.run(
            "Search for Python best practices and summarize",
            thread=thread,
        )
        print(f"Response: {result.text}")
        
        # Streaming
        print("\nStreaming: ", end="")
        async for chunk in agent.run_stream("Continue with examples", thread=thread):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()
        
        # Structured output
        result = await agent.run(
            "Analyze findings",
            thread=thread,
            response_format=AnalysisResult,
        )
        analysis = AnalysisResult.model_validate_json(result.text)
        print(f"\nConfidence: {analysis.confidence}")


if __name__ == "__main__":
    asyncio.run(main())
```

## 规范（Conventions）

- 始终使用异步上下文管理器：`async with provider:`  
- 直接将函数传递给 `tools=` 参数（会自动转换为 AIFunction 类型）  
- 使用 `Annotated[type, Field(description=...)]` 标记函数参数  
- 使用 `get_new_thread()` 进行多轮对话管理  
- 对于服务管理的 MCP，优先使用 `HostedMCPTool`；对于客户端管理的 MCP，优先使用 `MCPStreamableHTTPTool`  

## 参考文件（Reference Files）

- [references/tools.md](references/tools.md)：托管工具的详细使用模式  
- [references/mcp.md](references/mcp.md)：MCP 集成（托管 + 本地）  
- [references/threads.md](references/threads.md)：线程与对话管理  
- [references/advanced.md](references/advanced.md)：OpenAPI、引用格式、结构化输出