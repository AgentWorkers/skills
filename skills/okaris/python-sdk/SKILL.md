---
name: python-sdk
description: |
  Python SDK for inference.sh - run AI apps, build agents, and integrate with 150+ models.
  Package: inferencesh (pip install inferencesh). Supports sync/async, streaming, file uploads.
  Build agents with template or ad-hoc patterns, tool builder API, skills, and human approval.
  Use for: Python integration, AI apps, agent development, RAG pipelines, automation.
  Triggers: python sdk, inferencesh, pip install, python api, python client, async inference,
  python agent, tool builder python, programmatic ai, python integration, sdk python
allowed-tools: Bash(pip install inferencesh), Bash(python *)
---

# Python SDK

使用 [inference.sh](https://inference.sh) Python SDK 构建 AI 应用程序。

## 快速入门

```bash
pip install inferencesh
```

```python
from inferencesh import inference

client = inference(api_key="inf_your_key")

# Run an AI app
result = client.run({
    "app": "infsh/flux-schnell",
    "input": {"prompt": "A sunset over mountains"}
})
print(result["output"])
```

## 安装

```bash
# Standard installation
pip install inferencesh

# With async support
pip install inferencesh[async]
```

**系统要求：** Python 3.8 或更高版本

## 认证

```python
import os
from inferencesh import inference

# Direct API key
client = inference(api_key="inf_your_key")

# From environment variable (recommended)
client = inference(api_key=os.environ["INFERENCE_API_KEY"])
```

获取您的 API 密钥：设置 → API 密钥 → 创建 API 密钥

## 运行应用程序

### 基本执行

```python
result = client.run({
    "app": "infsh/flux-schnell",
    "input": {"prompt": "A cat astronaut"}
})

print(result["status"])  # "completed"
print(result["output"])  # Output data
```

### 一次性执行（无需管理会话）

```python
task = client.run({
    "app": "google/veo-3-1-fast",
    "input": {"prompt": "Drone flying over mountains"}
}, wait=False)

print(f"Task ID: {task['id']}")
# Check later with client.get_task(task['id'])
```

### 流式处理（实时进度更新）

```python
for update in client.run({
    "app": "google/veo-3-1-fast",
    "input": {"prompt": "Ocean waves at sunset"}
}, stream=True):
    print(f"Status: {update['status']}")
    if update.get("logs"):
        print(update["logs"][-1])
```

### 运行参数

| 参数 | 类型 | 说明 |
|-----------|------|-------------|
| `app` | 字符串 | 应用程序 ID（格式：namespace/name@version） |
| `input` | 字典 | 符合应用程序结构的输入数据 |
| `setup` | 字典 | 隐藏的配置信息 |
| `infra` | 字符串 | 执行环境：`cloud` 或 `private` |
| `session` | 字符串 | 用于保持会话状态的会话 ID |
| `session_timeout` | 整数 | 会话空闲超时时间（1-3600 秒） |

## 文件处理

### 自动上传

```python
result = client.run({
    "app": "image-processor",
    "input": {
        "image": "/path/to/image.png"  # Auto-uploaded
    }
})
```

### 手动上传

```python
from inferencesh import UploadFileOptions

# Basic upload
file = client.upload_file("/path/to/image.png")

# With options
file = client.upload_file(
    "/path/to/image.png",
    UploadFileOptions(
        filename="custom_name.png",
        content_type="image/png",
        public=True
    )
)

result = client.run({
    "app": "image-processor",
    "input": {"image": file["uri"]}
})
```

## 会话（保持状态）

在多次调用之间维持应用程序的状态：

```python
# Start new session
result = client.run({
    "app": "my-app",
    "input": {"action": "init"},
    "session": "new",
    "session_timeout": 300  # 5 minutes
})
session_id = result["session_id"]

# Continue in same session
result = client.run({
    "app": "my-app",
    "input": {"action": "process"},
    "session": session_id
})
```

## 代理 SDK

### 模板代理

使用工作区中预构建的代理：

```python
agent = client.agent("my-team/support-agent@latest")

# Send message
response = agent.send_message("Hello!")
print(response.text)

# Multi-turn conversation
response = agent.send_message("Tell me more")

# Reset conversation
agent.reset()

# Get chat history
chat = agent.get_chat()
```

### 自定义代理

通过编程方式创建自定义代理：

```python
from inferencesh import tool, string, number, app_tool

# Define tools
calculator = (
    tool("calculate")
    .describe("Perform a calculation")
    .param("expression", string("Math expression"))
    .build()
)

image_gen = (
    app_tool("generate_image", "infsh/flux-schnell@latest")
    .describe("Generate an image")
    .param("prompt", string("Image description"))
    .build()
)

# Create agent
agent = client.agent({
    "core_app": {"ref": "infsh/claude-sonnet-4@latest"},
    "system_prompt": "You are a helpful assistant.",
    "tools": [calculator, image_gen],
    "temperature": 0.7,
    "max_tokens": 4096
})

response = agent.send_message("What is 25 * 4?")
```

### 可用的核心应用程序

| 模型 | 应用程序参考 |
|-------|---------------|
| Claude Sonnet 4 | `infsh/claude-sonnet-4@latest` |
| Claude 3.5 Haiku | `infsh/claude-haiku-35@latest` |
| GPT-4o | `infsh/gpt-4o@latest` |
| GPT-4o Mini | `infsh/gpt-4o-mini@latest` |

## 工具构建器 API

### 参数类型

```python
from inferencesh import (
    string, number, integer, boolean,
    enum_of, array, obj, optional
)

name = string("User's name")
age = integer("Age in years")
score = number("Score 0-1")
active = boolean("Is active")
priority = enum_of(["low", "medium", "high"], "Priority")
tags = array(string("Tag"), "List of tags")
address = obj({
    "street": string("Street"),
    "city": string("City"),
    "zip": optional(string("ZIP"))
}, "Address")
```

### 客户端工具（在您的代码中运行）

```python
greet = (
    tool("greet")
    .display("Greet User")
    .describe("Greets a user by name")
    .param("name", string("Name to greet"))
    .require_approval()
    .build()
)
```

### 应用程序工具（调用 AI 应用程序）

```python
generate = (
    app_tool("generate_image", "infsh/flux-schnell@latest")
    .describe("Generate an image from text")
    .param("prompt", string("Image description"))
    .setup({"model": "schnell"})
    .input({"steps": 20})
    .require_approval()
    .build()
)
```

### 代理工具（委托给子代理）

```python
from inferencesh import agent_tool

researcher = (
    agent_tool("research", "my-org/researcher@v1")
    .describe("Research a topic")
    .param("topic", string("Topic to research"))
    .build()
)
```

### Webhook 工具（调用外部 API）

```python
from inferencesh import webhook_tool

notify = (
    webhook_tool("slack", "https://hooks.slack.com/...")
    .describe("Send Slack notification")
    .secret("SLACK_SECRET")
    .param("channel", string("Channel"))
    .param("message", string("Message"))
    .build()
)
```

### 内部工具（内置功能）

```python
from inferencesh import internal_tools

config = (
    internal_tools()
    .plan()
    .memory()
    .web_search(True)
    .code_execution(True)
    .image_generation({
        "enabled": True,
        "app_ref": "infsh/flux@latest"
    })
    .build()
)

agent = client.agent({
    "core_app": {"ref": "infsh/claude-sonnet-4@latest"},
    "internal_tools": config
})
```

## 代理响应的流式传输

```python
def handle_message(msg):
    if msg.get("content"):
        print(msg["content"], end="", flush=True)

def handle_tool(call):
    print(f"\n[Tool: {call.name}]")
    result = execute_tool(call.name, call.args)
    agent.submit_tool_result(call.id, result)

response = agent.send_message(
    "Explain quantum computing",
    on_message=handle_message,
    on_tool_call=handle_tool
)
```

## 文件附件

```python
# From file path
with open("image.png", "rb") as f:
    response = agent.send_message(
        "What's in this image?",
        files=[f.read()]
    )

# From base64
response = agent.send_message(
    "Analyze this",
    files=["data:image/png;base64,iVBORw0KGgo..."]
)
```

## 技能（可复用的上下文数据）

```python
agent = client.agent({
    "core_app": {"ref": "infsh/claude-sonnet-4@latest"},
    "skills": [
        {
            "name": "code-review",
            "description": "Code review guidelines",
            "content": "# Code Review\n\n1. Check security\n2. Check performance..."
        },
        {
            "name": "api-docs",
            "description": "API documentation",
            "url": "https://example.com/skills/api-docs.md"
        }
    ]
})
```

## 异步支持

```python
from inferencesh import async_inference
import asyncio

async def main():
    client = async_inference(api_key="inf_...")

    # Async app execution
    result = await client.run({
        "app": "infsh/flux-schnell",
        "input": {"prompt": "A galaxy"}
    })

    # Async agent
    agent = client.agent("my-org/assistant@latest")
    response = await agent.send_message("Hello!")

    # Async streaming
    async for msg in agent.stream_messages():
        print(msg)

asyncio.run(main())
```

## 错误处理

```python
from inferencesh import RequirementsNotMetException

try:
    result = client.run({"app": "my-app", "input": {...}})
except RequirementsNotMetException as e:
    print(f"Missing requirements:")
    for err in e.errors:
        print(f"  - {err['type']}: {err['key']}")
except RuntimeError as e:
    print(f"Error: {e}")
```

## 人工审批工作流程

```python
def handle_tool(call):
    if call.requires_approval:
        # Show to user, get confirmation
        approved = prompt_user(f"Allow {call.name}?")
        if approved:
            result = execute_tool(call.name, call.args)
            agent.submit_tool_result(call.id, result)
        else:
            agent.submit_tool_result(call.id, {"error": "Denied by user"})

response = agent.send_message(
    "Delete all temp files",
    on_tool_call=handle_tool
)
```

## 参考文件

- [代理模式](references/agent-patterns.md) - 多代理、RAG（问答系统）和人工干预模式
- [工具构建器](references/tool-builder.md) - 完整的工具构建器 API 参考
- [流式处理](references/streaming.md) - 实时进度更新和 SSE（Server-Side Eventing）处理
- [文件处理](references/files.md) - 文件上传、下载和管理
- [会话管理](references/sessions.md) - 保持会话状态的处理方式
- [异步处理模式](references/async-patterns.md) - 并行处理和 async/await 的使用

## 相关技能

```bash
# JavaScript SDK
npx skills add inference-sh/agent-skills@javascript-sdk

# Full platform skill (all 150+ apps via CLI)
npx skills add inference-sh/agent-skills@inference-sh

# LLM models
npx skills add inference-sh/agent-skills@llm-models

# Image generation
npx skills add inference-sh/agent-skills@ai-image-generation
```

## 文档资料

- [Python SDK 参考文档](https://inference.sh/docs/api/sdk-python) - 完整的 API 文档
- [代理 SDK 概述](https://inference.sh/docs/api/agent-sdk) - 代理程序的构建方法
- [工具构建器参考](https://inference.sh/docs/api/agent-tools) - 工具的创建方法
- [认证机制](https://inference.sh/docs/api/authentication) - API 密钥的设置方法
- [流式处理](https://inference.sh/docs/api/sdk/streaming) - 实时更新功能
- [文件上传](https://inference.sh/docs/api/sdk/files) - 文件处理相关说明