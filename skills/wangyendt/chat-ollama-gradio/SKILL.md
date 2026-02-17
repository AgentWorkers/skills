---
name: pywayne-llm-chat-ollama-gradio
description: 基于Gradio的Ollama聊天界面，支持多会话管理。当使用`pywayne.llm.chat_ollama_gradio`模块时，该界面可用于创建一个基于Web的聊天用户界面，该界面能够连接到Ollama模型，支持多个聊天会话、模型选择以及实时响应输出。该界面还与`ChatManager`集成，以实现会话管理功能。
---
# Pywayne Chat Ollama Gradio

该模块提供了一个基于Gradio的Web聊天界面，用于与Ollama模型进行交互，并支持多会话功能。

## 快速入门

```python
from pywayne.llm.chat_ollama_gradio import OllamaChatGradio

# Create and launch chat interface
app = OllamaChatGradio(
    base_url="http://localhost:11434/v1",
    server_port=7870
)
app.launch()
```

## 配置

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `base_url` | `"http://localhost:11434/v1"` | Ollama API的基URL |
| `server_name` | `"0.0.0.0"` | 服务器主机名 |
| `server_port` | `7870` | 服务器端口 |
| `root_path` | `""` | 反向代理的根路径 |
| `api_key` | `"ollama"` | API密钥（用于与Ollama兼容） |

## 模型发现

通过运行`ollama list`命令自动发现可用的Ollama模型：

- 排除名称中包含“embed”的模型；
- 如果未找到模型，则默认使用`qwen2.5:0.5b`模型。

## 会话管理

### 创建新会话

```python
# UI method: Click "新建会话" button
new_chat_id, new_history, new_choices = app.create_new_chat()
```

### 切换会话

```python
# UI method: Select from "历史会话" radio list
history = app.switch_chat(selected_chat_id)
```

## API参考

### OllamaChatGradio

| 方法 | 说明 |
|---------|-------------|
| `get_ollama_models()` | 获取可用的Ollama模型列表 |
| `init_chat_manager()` | 初始化ChatManager实例 |
| `create_new_chat()` | 创建新聊天会话，返回（chat_id, history, radio_update） |
| `switch_chat(chat_id)` | 切换到指定的聊天会话 |
| `format_history(history)` | 格式化聊天历史记录以供显示 |
| `chat(message, history, model_name)` | 处理聊天消息并实现实时流式响应 |
| `create_demo()` | 创建Gradio界面 |
| `launch()` | 启动Gradio服务器 |

## 用户界面组件

| 组件 | 说明 |
|-----------|-------------|
| `chatbot` | 主聊天显示区域 |
| `msg` | 消息输入框 |
| `modelDropdown` | 模型选择下拉菜单 |
| `chat_id_text` | 当前会话ID（只读） |
| `new_chat_btn` | 创建新会话的按钮 |
| `chat_history_list` | 用于切换会话的列表控件 |

## 所需依赖

- `gradio`：Web UI框架
- `pywayne.llm.chat_bot`：用于管理聊天会话和配置LLM的库
- `ollama` CLI：必须已安装并可用

## 注意事项

- 该模块使用ChatManager来实现多会话支持；
- 流式响应可实时更新用户界面；
- 会话历史记录存储在内存中（不持久化）；
- 启动应用程序前必须确保Ollama服务正在运行。