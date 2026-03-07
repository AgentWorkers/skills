---
name: agnost-ingestion
description: 在为Agnost AI分析系统实现数据导入功能时，请使用本文档。其中包含API参考资料、Python和TypeScript的SDK使用指南，以及用于跟踪AI对话、MCP服务器事件和用户交互的代码示例。
license: MIT
metadata:
  author: Agnost AI
  version: "1.0.0"
---
# Agnost 数据采集

本文档提供了将数据导入 Agnost AI 的全面指南，用于数据分析、监控和洞察。内容涵盖了用于跟踪 AI 交互的 Conversation SDK 以及用于模型上下文协议（Model Context Protocol, MCP）服务器分析的 MCP SDK。

> **官方文档：** [https://docs.agnost.ai](https://docs.agnost.ai)
> **API 端点：** `https://api.agnost.ai`
> **仪表板：** [https://app.agnost.ai](https://app.agnost.ai)

## 重要提示：如何应用本技能

在实施 Agnost 数据采集之前，请按照以下优先级顺序进行操作：

1. **确定使用场景**：是用于跟踪 AI 对话（如聊天机器人、代理）还是用于 MCP 服务器分析。
2. 查阅 `references/` 目录中的 SDK 参考资料，以获取详细的 API 信息。
3. 使用提供的代码示例作为起点。
4. 在解释实现细节时引用相关参考资料。

---

## 快速参考

### SDK 包

| 使用场景 | Python | TypeScript/Node.js | Go |
|----------|--------|-------------------|-----|
| **AI 对话跟踪** | `pip install agnost` | `npm install agnostai` | N/A |
| **MCP 服务器分析** | `pip install agnost-mcp` | `npm install agnost` | `go get github.com/agnostai/agnost-go` |

### API 端点

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/v1/capture-session` | POST | 创建新的对话/会话 |
| `/api/v1/capture-event` | POST | 记录会话中的事件 |

---

## Conversation SDK（推荐用于 AI 应用）

在构建需要跟踪用户交互、输入、输出和性能指标的 AI 应用、聊天机器人或代理时，请使用 Conversation SDK。

### Python 安装与设置

```python
# Installation
pip install agnost
# or
uv add agnost

# Basic Setup
import agnost

# Initialize with your org ID (from dashboard)
agnost.init("your-org-id")
```

### TypeScript/Node.js 安装与设置

```typescript
// Installation
npm install agnostai
// or
pnpm add agnostai

// Basic Setup
import * as agnost from "agnostai";

// Initialize with your org ID (from dashboard)
agnost.init("your-org-id");
```

---

## 核心方法

### 1. `init-org_id, config?)` - 初始化 SDK

**必须在任何跟踪方法之前调用。**

#### Python
```python
import agnost

# Basic initialization
agnost.init("your-org-id")

# With configuration
agnost.init(
    "your-org-id",
    endpoint="https://api.agnost.ai",  # Custom endpoint (optional)
    debug=True                          # Enable debug logging
)
```

#### TypeScript
```typescript
import * as agnost from "agnostai";

// Basic initialization
agnost.init("your-org-id");

// With configuration
agnost.init("your-org-id", {
  endpoint: "https://api.agnost.ai",  // Custom endpoint (optional)
  debug: true                          // Enable debug logging
});
```

---

### 2. `begin()` + `end()` - 跟踪交互（推荐）

使用 `begin()` 和 `end()` 方法可以自动计算延迟并使代码更简洁。

#### Python
```python
import agnost

agnost.init("your-org-id")

# Start tracking an interaction
interaction = agnost.begin(
    user_id="user_123",
    agent_name="weather-agent",
    input="What's the weather in NYC?",
    conversation_id="conv_456",  # Optional: group related events
    properties={"model": "gpt-4"}  # Optional: custom metadata
)

# ... Your AI processing happens here ...
response = call_your_ai_model(interaction.input)

# Complete the interaction (latency auto-calculated)
interaction.end(
    output=response,
    success=True  # Set False if the call failed
)
```

#### TypeScript
```typescript
import * as agnost from "agnostai";

agnost.init("your-org-id");

// Start tracking an interaction
const interaction = agnost.begin({
  userId: "user_123",
  agentName: "weather-agent",
  input: "What's the weather in NYC?",
  conversationId: "conv_456",  // Optional: group related events
  properties: { model: "gpt-4" }  // Optional: custom metadata
});

// ... Your AI processing happens here ...
const response = await callYourAIModel(interaction.input);

// Complete the interaction (latency auto-calculated)
interaction.end(response);  // or interaction.end(response, true) for success
```

---

### 3. `track()` - 一次性跟踪

当所有数据都一次性可用时（无需使用 `begin()` 和 `end()`）使用此方法。

#### Python
```python
import agnost

agnost.init("your-org-id")

agnost.track(
    user_id="user_123",
    input="What's the weather?",
    output="The weather is sunny with 72°F.",
    agent_name="weather-agent",
    conversation_id="conv_456",  # Optional
    success=True,
    latency=150,  # milliseconds
    properties={"model": "gpt-4", "tokens": 42}
)
```

---

### 4. `identify()` - 用户信息增强

将用户元数据与用户 ID 关联起来，以便进行更深入的分析。

#### Python
```python
import agnost

agnost.init("your-org-id")

agnost.identify("user_123", {
    "name": "John Doe",
    "email": "john@example.com",
    "plan": "premium",
    "company": "Acme Inc"
})
```

#### TypeScript
```typescript
import * as agnost from "agnostai";

agnost.init("your-org-id");

agnost.identify("user_123", {
  name: "John Doe",
  email: "john@example.com",
  plan: "premium",
  company: "Acme Inc"
});
```

---

### 5. `flush()` & `shutdown()` - 资源管理

#### Python
```python
import agnost

# Manually flush pending events
agnost.flush()

# Clean shutdown (flushes and closes connections)
agnost.shutdown()
```

#### TypeScript
```typescript
import * as agnost from "agnostai";

// Manually flush pending events
await agnost.flush();

// Clean shutdown (flushes and closes connections)
await agnost.shutdown();
```

---

## 交互对象方法

使用 `begin()` 之后，您将获得一个 `Interaction` 对象，该对象包含以下方法：

| 方法 | 描述 |
|--------|-------------|
| `set_input(text)` / `setInput(text)` | 设置/更新输入文本 |
| `set_property(key, value)` / `setProperty(key, value)` | 添加单个自定义属性 |
| `set_properties(dict)` / `setProperties(obj)` | 添加多个自定义属性 |
| `end(output, success?, latency?)` | 完成并发送事件 |

#### 示例：动态构建输入（Python）

```python
interaction = agnost.begin(
    user_id="user_123",
    agent_name="my-agent"
)

# Build input from multiple sources
interaction.set_input("Combined user query: " + user_input)
interaction.set_property("source", "chat-widget")
interaction.set_properties({"model": "gpt-4", "version": "v2"})

# Process and complete
response = process_query(interaction.input)
interaction.end(output=response)
```

---

## MCP 服务器分析

对于需要跟踪模型上下文协议（MCP）服务器的情况，请使用 MCP SDK。

### Python (FastMCP)

```python
from mcp.server.fastmcp import FastMCP
from agnost_mcp import track, config

# Create FastMCP server
mcp = FastMCP("my-mcp-server")

# Add your tools
@mcp.tool()
def my_tool(param: str) -> str:
    return f"Result: {param}"

# Enable tracking
track(mcp, "your-org-id", config(
    endpoint="https://api.agnost.ai",
    disable_input=False,   # Track input arguments
    disable_output=False   # Track output results
))

# Run server
mcp.run()
```

### TypeScript (MCP SDK)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { trackMCP } from "agnost";

// Create MCP server
const server = new Server({
  name: "my-mcp-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

// Enable tracking
trackMCP(server, "your-org-id", {
  endpoint: "https://api.agnost.ai",
  disableInput: false,
  disableOutput: false
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Go (mcp-go)

```go
package main

import (
    "github.com/agnostai/agnost-go/agnost"
    "github.com/mark3labs/mcp-go/server"
)

func main() {
    s := server.NewMCPServer("my-server", "1.0.0")

    // Add tools...

    // Enable tracking
    agnost.Track(s, "your-org-id", &agnost.Config{
        DisableInput:  false,
        DisableOutput: false,
        BatchSize:     10,
        LogLevel:      "info",
    })

    server.ServeStdio(s)
}
```

---

## 直接 HTTP API

在不需要 SDK 的情况下，可以直接使用这些 API。

### 创建会话

```bash
curl -X POST https://api.agnost.ai/api/v1/capture-session \
  -H "Content-Type: application/json" \
  -H "X-Org-Id: your-org-id" \
  -d '{
    "session_id": "unique-session-id",
    "client_config": "my-app",
    "connection_type": "http",
    "ip": "",
    "user_data": {
      "user_id": "user_123",
      "email": "user@example.com"
    },
    "tools": ["tool1", "tool2"]
  }'
```

### 捕获事件

```bash
curl -X POST https://api.agnost.ai/api/v1/capture-event \
  -H "Content-Type: application/json" \
  -H "X-Org-Id: your-org-id" \
  -d '{
    "session_id": "unique-session-id",
    "primitive_type": "tool",
    "primitive_name": "weather_lookup",
    "latency": 150,
    "success": true,
    "args": "{\"city\": \"NYC\"}",
    "result": "{\"temp\": 72}",
    "metadata": {
      "model": "gpt-4",
      "tokens": "42"
    }
  }'
```

---

## 数据结构

### 会话请求

```json
{
  "session_id": "string (UUID or custom ID)",
  "client_config": "string (app identifier)",
  "connection_type": "string (http/stdio/sse)",
  "ip": "string (optional)",
  "user_data": {
    "user_id": "string",
    "...": "any additional user fields"
  },
  "tools": ["array", "of", "tool", "names"]
}
```

### 事件请求

```json
{
  "session_id": "string (must match existing session)",
  "primitive_type": "string (tool/resource/prompt)",
  "primitive_name": "string (name of the primitive)",
  "latency": "integer (milliseconds)",
  "success": "boolean",
  "args": "string (JSON-encoded input)",
  "result": "string (JSON-encoded output)",
  "checkpoints": [
    {
      "name": "string",
      "timestamp": "integer (ms since start)",
      "metadata": {}
    }
  ],
  "metadata": {
    "key": "value pairs"
  }
}
```

---

## 配置选项

### Python Conversation SDK

```python
agnost.init(
    "your-org-id",
    endpoint="https://api.agnost.ai",  # API endpoint
    debug=False                         # Enable debug logging
)
```

### TypeScript Conversation SDK

```typescript
interface ConversationConfig {
  endpoint?: string;  // API endpoint (default: https://api.agnost.ai)
  debug?: boolean;    // Enable debug logging (default: false)
}

agnost.init("your-org-id", { endpoint: "...", debug: true });
```

### Python MCP SDK (FastMCP)

```python
from agnost_mcp import track, config

track(server, "your-org-id", config(
    endpoint="https://api.agnost.ai",
    disable_input=False,   # Don't track input arguments
    disable_output=False   # Don't track output results
))
```

### TypeScript MCP SDK

```typescript
import { trackMCP, createConfig } from "agnost";

const cfg = createConfig({
  endpoint: "https://api.agnost.ai",
  disableInput: false,
  disableOutput: false
});

trackMCP(server, "your-org-id", cfg);
```

### Go MCP SDK

```go
type Config struct {
    Endpoint         string        // default: "https://api.agnost.ai"
    DisableInput     bool          // default: false
    DisableOutput    bool          // default: false
    BatchSize        int           // default: 5
    MaxRetries       int           // default: 3
    RetryDelay       time.Duration // default: 1s
    RequestTimeout   time.Duration // default: 5s
    LogLevel         string        // "debug", "info", "warning", "error"
    Identify         IdentifyFunc  // optional user identification
}
```

---

## 最佳实践

### 1. 尽早初始化 SDK
```python
# At application startup
import agnost
agnost.init("your-org-id")
```

### 2. 使用 `begin()` 和 `end()` 以确保延迟测量的准确性
```python
# Automatically calculates processing time
interaction = agnost.begin(user_id="u1", agent_name="agent")
# ... processing ...
interaction.end(output=result)
```

### 3. 使用 `conversation_id` 将相关事件分组
```python
# All events for a single chat session
conversation_id = f"chat_{session_id}"
interaction = agnost.begin(
    user_id="u1",
    conversation_id=conversation_id,
    agent_name="chatbot"
)
```

### 4. 优雅地处理错误
```python
interaction = agnost.begin(user_id="u1", agent_name="agent")
try:
    result = process_request()
    interaction.end(output=result, success=True)
except Exception as e:
    interaction.end(output=str(e), success=False)
```

### 5. 清晰地关闭 SDK
```python
import atexit
import agnost

atexit.register(agnost.shutdown)
```

---

## 适用场景

本技能适用于以下情况：

- 需要实现 Agnost 的数据采集功能时
- 设置 AI 对话跟踪时
- 集成 MCP 服务器分析时
- 使用事件/会话捕获 API 时
- 对 SDK 初始化有疑问时
- 需要跟踪延迟时
- 需要对用户进行识别/信息增强时

---

## 其他资源

- **Python SDK 参考文档**：`references/python-sdk.md`
- **TypeScript SDK 参考文档**：`references/typescript-sdk.md`
- **API 参考文档**：`references/api-reference.md`
- **仪表板**：[https://app.agnost.ai](https://app.agnost.ai)
- **Discord 社区**：[https://discord.gg/agnost](https://discord.gg/agnost)