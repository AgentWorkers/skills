---
name: strands
version: 2.0.0
description: 使用 AWS Strands SDK 构建并运行基于 Python 的 AI 代理。当您需要创建自主代理、多代理工作流程、自定义工具或与 MCP 服务器集成时，可以使用该 SDK。它支持 Ollama（本地）、Anthropic、OpenAI、Bedrock 等模型提供商，可用于代理的搭建、工具的开发以及代理任务的程序化运行。
homepage: https://github.com/strands-agents/sdk-python
metadata:
  openclaw:
    emoji: 🧬
    requires:
      bins: [python3]
      packages: [strands-agents]
---

# Strands Agents SDK

使用 [Strands SDK](https://github.com/strands-agents/sdk-python)（基于 Apache-2.0 协议，由 AWS 提供）在 Python 中构建 AI 代理。

验证版本：`strands-agents==1.23.0`，`strands-agents-tools==0.2.19`

## 先决条件

```bash
# Install SDK + tools (via pipx for isolation — recommended)
pipx install strands-agents-builder  # includes strands-agents + strands-agents-tools + CLI

# Or install directly
pip install strands-agents strands-agents-tools
```

## 核心概念：默认使用 Bedrock

当 `Agent()` 方法没有 `model=` 参数时，会默认使用 **Amazon Bedrock** — 具体来说是 `us.anthropic.claude-sonnet-4-20250514-v1:0`（位于 `us-west-2` 区域）。这需要 AWS 凭据。如果要使用其他提供商，请显式指定 `model=` 参数。

默认模型常量：`strands.models BEDrock.DEFAULT_BEDROCK_MODEL_ID`

## 快速入门 — 本地代理（Ollama）

```python
from strands import Agent
from strands.models.ollama import OllamaModel

# host is a required positional argument
model = OllamaModel("http://localhost:11434", model_id="qwen3:latest")
agent = Agent(model=model)
result = agent("What is the capital of France?")
print(result)
```

**注意：** 并非所有开源模型都支持调用外部工具。部分模型在处理过程中会失去调用外部工具的功能。建议先使用默认模型（如 qwen3、llama3.x、mistral）进行测试。

## 快速入门 — Bedrock（默认提供商）

```python
from strands import Agent

# No model specified → BedrockModel (Claude Sonnet 4, us-west-2)
# Requires AWS credentials (~/.aws/credentials or env vars)
agent = Agent()
result = agent("Explain quantum computing")

# Explicit Bedrock model:
from strands.models import BedrockModel
model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0")
agent = Agent(model=model)
```

## 快速入门 — Anthropic（直接使用 API）

```python
from strands import Agent
from strands.models.anthropic import AnthropicModel

# max_tokens is Required[int] — must be provided
model = AnthropicModel(model_id="claude-sonnet-4-20250514", max_tokens=4096)
agent = Agent(model=model)
result = agent("Explain quantum computing")
```

需要设置 `ANTHROPIC_API_KEY` 环境变量。

## 快速入门 — OpenAI

```python
from strands import Agent
from strands.models.openai import OpenAIModel

model = OpenAIModel(model_id="gpt-4.1")
agent = Agent(model=model)
```

需要设置 `OPENAI_API_KEY` 环境变量。

## 创建自定义工具

使用 `@tool` 装饰器。该装饰器会自动生成工具的类型提示和文档字符串：

```python
from strands import Agent, tool

@tool
def read_file(path: str) -> str:
    """Read contents of a file at the given path.

    Args:
        path: Filesystem path to read.
    """
    with open(path) as f:
        return f.read()

@tool
def write_file(path: str, content: str) -> str:
    """Write content to a file.

    Args:
        path: Filesystem path to write.
        content: Text content to write.
    """
    with open(path, 'w') as f:
        f.write(content)
    return f"Wrote {len(content)} bytes to {path}"

agent = Agent(model=model, tools=[read_file, write_file])
agent("Read /tmp/test.txt and summarize it")
```

### ToolContext

工具可以通过 `ToolContext` 访问代理的状态：

```python
from strands import tool
from strands.types.tools import ToolContext

@tool
def stateful_tool(query: str, tool_context: ToolContext) -> str:
    """A tool that accesses agent state.

    Args:
        query: Input query.
    """
    # Access shared agent state
    count = tool_context.state.get("call_count", 0) + 1
    tool_context.state["call_count"] = count
    return f"Call #{count}: {query}"
```

## 内置工具（共 46 个）

`strands-agents-tools` 提供了多种预构建的工具：

```python
from strands_tools import calculator, file_read, file_write, shell, http_request
agent = Agent(model=model, tools=[calculator, file_read, shell])
```

完整工具列表：`calculator`、`file_read`、`file_write`、`shell`、`http_request`、`editor`、`image_reader`、`python_repl`、`current_time`、`think`、`stop`、`sleep`、`environment`、`retrieve`、`search_video`、`chat_video`、`speak`、`generate_image`、`generate_image_stability`、`diagram`、`journal`、`memory`、`agent_core_memory`、`elasticsearch_memory`、`mongodb_memory`、`mem0_memory`、`rss`、`cron`、`batch`、`workflow`、`use_agent`、`use_llm`、`use_aws`、`use_computer`、`load_tool`、`handoff_to_user`、`slack`、`swarm`、`graph`、`a2a_client`、`mcp_client`、`exa`、`tavily`、`bright_data`、`nova_reels`。

**热重载功能**：`Agent LOAD_tools_from_directory=True` 会监控 `./tools/` 目录下的文件变化，并自动重新加载工具。

## MCP 集成

可以连接到任何 Model Context Protocol 服务器。`MCPClient` 实现了 `ToolProvider` 接口，可以直接将其添加到工具列表中：

```python
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# MCPClient takes a callable that returns the transport
mcp = MCPClient(lambda: stdio_client(StdioServerParameters(
    command="uvx",
    args=["some-mcp-server@latest"]
)))

# Use as context manager — MCPClient is a ToolProvider
with mcp:
    agent = Agent(model=model, tools=[mcp])
    agent("Use the MCP tools to do something")
```

**SSE 传输**：
```python
from mcp.client.sse import sse_client
mcp = MCPClient(lambda: sse_client("http://localhost:8080/sse"))
```

## 多代理模式

### 代理作为工具

内部代理可以作为外部代理的工具使用：

```python
researcher = Agent(model=model, system_prompt="You are a research assistant.")
writer = Agent(model=model, system_prompt="You are a writer.")

orchestrator = Agent(
    model=model,
    tools=[researcher, writer],
    system_prompt="You coordinate research and writing tasks."
)
orchestrator("Research quantum computing and write a blog post")
```

### Swarm 模式

自组织的代理团队，具有共享的上下文和自动的任务交接机制：

```python
from strands.multiagent.swarm import Swarm

# Agents need name + description for handoff identification
researcher = Agent(
    model=model,
    name="researcher",
    description="Finds and summarizes information"
)
writer = Agent(
    model=model,
    name="writer",
    description="Creates polished content"
)

swarm = Swarm(
    nodes=[researcher, writer],
    entry_point=researcher,    # optional — defaults to first agent
    max_handoffs=20,           # default
    max_iterations=20,         # default
    execution_timeout=900.0,   # 15 min default
    node_timeout=300.0         # 5 min per node default
)
result = swarm("Research AI agents, then hand off to writer for a blog post")
```

Swarm 会自动插入 `handoff_to_agent` 工具。代理可以通过调用该工具来交接任务。支持中断/恢复、会话持久化以及重复性任务交接的功能。

### Graph 模式（有向无环图）

通过 `GraphBuilder` 实现基于依赖关系的确定性执行：

```python
from strands.multiagent.graph import GraphBuilder

builder = GraphBuilder()
research_node = builder.add_node(researcher, node_id="research")
writing_node = builder.add_node(writer, node_id="writing")
builder.add_edge("research", "writing")
builder.set_entry_point("research")

# Optional: conditional edges
# builder.add_edge("research", "writing",
#     condition=lambda state: "complete" in str(state.completed_nodes))

graph = builder.build()
result = graph("Write a blog post about AI agents")
```

支持循环（反馈循环），可以通过 `builder.reset_on_revisit(True)` 来设置重试机制，同时支持执行超时和嵌套图结构。

### A2A 协议（代理间通信）

可以将 Strands 代理作为 A2A 兼容的服务器来使用，以实现代理间的通信：

```python
from strands.multiagent.a2a import A2AServer

server = A2AServer(
    agent=my_agent,
    host="127.0.0.1",
    port=9000,
    version="0.0.1"
)
server.start()  # runs uvicorn
```

可以使用 `strands-agents-tools` 中的 `a2a_client` 工具连接到其他 A2A 代理。A2A 协议支持标准的跨进程/跨网络代理通信。

## 会话持久化

可以在代理运行期间持久化对话内容：

```python
from strands.session.file_session_manager import FileSessionManager

session = FileSessionManager(session_file_path="./sessions/my_session.json")
agent = Agent(model=model, session_manager=session)

# Also available:
from strands.session.s3_session_manager import S3SessionManager
session = S3SessionManager(bucket_name="my-bucket", session_id="session-1")
```

Swarm 和 Graph 都支持会话管理器，用于保存多代理的状态。

## 双向流式通信（实验性）

支持实时语音/文本对话，并保留音频流：

```python
from strands.experimental.bidi.agent import BidiAgent
from strands.experimental.bidi.models.nova_sonic import NovaSonicModel

# Supports: NovaSonicModel, GeminiLiveModel, OpenAIRealtimeModel
model = NovaSonicModel(region="us-east-1")
agent = BidiAgent(model=model, tools=[my_tool])
```

支持中断检测、并发工具执行以及连续的音频传输。此功能仍处于实验阶段，API 可能会发生变化。

## 系统提示

**Strands** 还支持使用 `list[SystemContentBlock]` 来生成结构化的系统提示，并支持缓存控制。

## 可观测性

支持原生 OpenTelemetry 追踪功能：

```python
agent = Agent(
    model=model,
    trace_attributes={"project": "my-agent", "environment": "dev"}
)
```

所有的工具调用、模型调用、任务交接以及生命周期事件都可以被追踪记录。

## Bedrock 特有功能

- **安全机制**：`BedrockModel` 配置中的 `guardrail_id` 和 `guardrail_version` 可用于内容过滤和 PII（个人身份信息）检测，以及输入/输出内容的编辑。
- **缓存机制**：系统提示和工具定义会被缓存以优化性能。
- **流式传输**：默认启用，可以通过 `streaming=False` 来禁用。
- **区域设置**：默认使用 `us-west-2` 区域，可以通过 `region_name` 参数或 `AWS_REGION` 环境变量进行更改。
- **跨区域推理**：以 `us.` 开头的模型 ID 会使用跨区域推理功能。

## 构建新代理

```bash
python3 {baseDir}/scripts/create-agent.py my-agent --provider ollama --model qwen3:latest
python3 {baseDir}/scripts/create-agent.py my-agent --provider anthropic
python3 {baseDir}/scripts/create-agent.py my-agent --provider bedrock
python3 {baseDir}/scripts/create-agent.py my-agent --provider openai --model gpt-4.1
```

会创建一个包含工具、配置文件和入口点的可运行代理目录。

## 运行代理

```bash
python3 {baseDir}/scripts/run-agent.py path/to/agent.py "Your prompt here"
python3 {baseDir}/scripts/run-agent.py path/to/agent.py --interactive
```

## 模型提供商参考（共 11 种）

| 提供商 | 类型 | 初始化方法 | 备注 |
|----------|-------|------|-------|
| Bedrock | `BedrockModel` | `BedrockModel(model_id=...)` | 默认提供商，会立即加载 |
| Ollama | `OllamaModel` | `OllamaModel("http://host:11434", model_id=...)` | `host` 参数是可选的 |
| Anthropic | `AnthropicModel` | `AnthropicModel(model_id=..., max_tokens=4096)` | `max_tokens` 参数是必需的 |
| OpenAI | `OpenAIModel` | `OpenAIModel(model_id=...)` | 需要 `OPENAI_API_KEY` |
| Gemini | `GeminiModel` | `GeminiModel(model_id=...)` | `api_key` 参数需要在客户端参数中提供 |
| Mistral | `MistralModel` | `MistralModel(model_id=...)` | 需要 Mistral API 密钥 |
| LiteLLM | `LiteLLMModel` | `LiteLLMModel(model_id=...)` | 适用于 Cohere、Groq 等模型 |
| LlamaAPI | `LlamaAPIModel` | `LlamaAPIModel(model_id=...)` | Meta Llama API |
| llama.cpp | `LlamaCppModel` | `LlamaCppModel(...)` | 适用于本地服务器，兼容 OpenAI |
| SageMaker | `SageMakerAIModel` | `SageMakerAIModel(...)` | 需要自定义 AWS 端点 |
| Writer | `WriterModel` | `WriterModel(model_id=...)` | 适用于 Writer 平台 |

所有非 Bedrock 类型的提供商都是 **按需加载** 的 — 只有在引用时才会导入相应的依赖项。

导入方式：`from strands.models.<provider> import <Class>`（或者使用 `from strands.models import <Class>` 来实现按需加载）。

## 提示

- 如果 `Agent()` 方法没有 `model=` 参数，则需要 AWS 凭据（默认使用 Bedrock）。
- `AnthropicModel` 需要 `max_tokens` 参数；省略该参数会导致运行时错误。
- `OllamaModel` 中的 `host` 参数是可选的，格式为 `OllamaModel("http://...", model_id="..."`。
- 部分被删除的 Ollama 模型可能无法调用外部工具，建议使用默认模型。
- Swarm 代理需要 `name=` 和 `description=` 参数来进行任务交接。
- `Agent LOAD_tools_from_directory=True` 会监控 `./tools/` 目录下的文件变化，并自动重新加载工具。
- 可以使用 `agent.tool.my_tool()` 直接调用工具，无需通过 LLM 代理进行转发。
- `MCPClient` 是一个 `ToolProvider`，可以直接在工具列表 `tools=[mcp]` 中使用；在使用 `Agent` 时无需手动调用 `list_tools_sync()`。
- 会话管理器适用于 Agent、Swarm 和 Graph 模式。
- 请确保使用的是最新版本的 `strands-agents` SDK，因为 API 可能会在后续版本中发生变化。