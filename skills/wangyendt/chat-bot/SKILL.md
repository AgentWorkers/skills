---
name: pywayne-llm-chat-bot
description: 使用与 OpenAI 兼容的 API 构建的 LLM（大型语言模型）聊天接口，支持流式传输和会话管理。该接口适用于与 `pywayne.llm.chat_bot` 模块配合使用，用于创建具有自定义配置的 LLM 聊天实例、管理多轮对话（包括对话历史记录）、处理流式响应，或通过 `ChatManager` 管理多个聊天会话。
---
# Pywayne LLM 聊天机器人

该模块提供了一个与 OpenAI API（包括 Ollama 等本地服务器）兼容的同步 LLM 聊天接口。

## 快速入门

```python
from pywayne.llm.chat_bot import LLMChat

# Create chat instance
chat = LLMChat(
    base_url="https://api.example.com/v1",
    api_key="your_api_key",
    model="deepseek-chat"
)

# Single-turn conversation (non-streaming)
response = chat.ask("Hello, LLM!", stream=False)
print(response)

# Streaming response
for token in chat.ask("Explain recursion", stream=True):
    print(token, end='', flush=True)
```

## 多轮对话

```python
# Use chat() for history tracking
for token in chat.chat("What is a class in Python?"):
    print(token, end='', flush=True)

# Continuation - remembers previous context
for token in chat.chat("How do I define a constructor?"):
    print(token, end='', flush=True)

# View history
for msg in chat.history:
    print(f"{msg['role']}: {msg['content']}")

# Clear history
chat.clear_history()
```

## 配置

### LLMConfig 类

```python
from pywayne.llm.chat_bot import LLMConfig

config = LLMConfig(
    base_url="https://api.example.com/v1",
    api_key="your_api_key",
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=8192,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    system_prompt="You are a helpful assistant"
)

chat = LLMChat(**config.to_dict())
```

### 动态系统提示更新

```python
chat.update_system_prompt("You are now a Python expert, provide code examples")
```

## 管理多个会话

```python
from pywayne.llm.chat_bot import ChatManager

manager = ChatManager(
    base_url="https://api.example.com/v1",
    api_key="your_api_key",
    model="deepseek-chat",
    timeout=300  # Session timeout in seconds
)

# Get or create chat instance (maintains per-session history)
chat1 = manager.get_chat("user1")
chat2 = manager.get_chat("user2")

# Sessions are independent
chat1.chat("Hello from user1")
chat2.chat("Hello from user2")

# Remove a session
manager.remove_chat("user1")
```

### 每个会话的自定义配置

```python
custom_config = LLMConfig(
    base_url=base_url,
    api_key=api_key,
    model="deepseek-chat",
    temperature=0.9,
    system_prompt="You are a creative writer"
)

chat3 = manager.get_chat("user3", config=custom_config)
```

## API 参考

### LLMChat

| 方法 | 描述 |
|--------|-------------|
| `ask(prompt, stream=False)` | 单轮对话（不保留对话历史记录） |
| `chat(prompt, stream=True)` | 多轮对话（保留对话历史记录） |
| `update_system.prompt(prompt)` | 更新系统提示 |
| `clear_history()` | 清除对话历史记录（保留系统提示） |
| `history` (属性) | 获取当前对话历史记录的副本 |

### ChatManager

| 方法 | 描述 |
|--------|-------------|
| `get_chat(chat_id, stream=True, config=None)` | 通过 ID 获取或创建聊天实例 |
| `remove_chat(chat_id)` | 删除聊天会话 |

## 参数

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------|
| `base_url` | 必需 | API 基础 URL（例如：`https://api.deepseek.com/v1`） |
| `api_key` | 必需 | API 认证密钥 |
| `model` | `"deepseek-chat"` | 模型名称 |
| `temperature` | `0.7` | 控制对话的随机性（0-2） |
| `max_tokens` | `2048`/`8192` | 最大输出字符数 |
| `top_p` | `1.0` | 核心采样率（0-1） |
| `frequency Penalty` | `0.0` | 减少重复内容（-2 到 2） |
| `presence Penalty` | `0.0` | 促进新话题的生成（-2 到 2） |
| `system_prompt` | `"你严谨的助手"` | 系统提示信息 |
| `timeout` | `inf` | 会话超时时间（仅适用于 ChatManager） |