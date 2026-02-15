---
name: ollama-local
description: 管理和使用本地的 Ollama 模型。支持模型管理（列出、下载、删除）、聊天交互、文本生成（补全功能）以及与本地大型语言模型（LLM）的集成使用。内容包括 OpenClaw 子代理的集成方法及模型选择指南。
---

# Ollama Local

您可以使用本地的Ollama模型进行推理、生成嵌入数据以及使用相关工具。

## 配置

设置您的Ollama服务器地址（默认为 `http://localhost:11434`）：

```bash
export OLLAMA_HOST="http://localhost:11434"
# Or for remote server:
export OLLAMA_HOST="http://192.168.1.100:11434"
```

## 快速参考

```bash
# List models
python3 scripts/ollama.py list

# Pull a model
python3 scripts/ollama.py pull llama3.1:8b

# Remove a model
python3 scripts/ollama.py rm modelname

# Show model details
python3 scripts/ollama.py show qwen3:4b

# Chat with a model
python3 scripts/ollama.py chat qwen3:4b "What is the capital of France?"

# Chat with system prompt
python3 scripts/ollama.py chat llama3.1:8b "Review this code" -s "You are a code reviewer"

# Generate completion (non-chat)
python3 scripts/ollama.py generate qwen3:4b "Once upon a time"

# Get embeddings
python3 scripts/ollama.py embed bge-m3 "Text to embed"
```

## 模型选择

请参阅 [references/models.md](references/models.md) 以获取完整的模型列表和选择指南。

**推荐模型：**
- 快速回答：`qwen3:4b`
- 编程：`qwen2.5-coder:7b`
- 通用：`llama3.1:8b`
- 推理：`deepseek-r1:8b`

## 工具使用

部分本地模型支持函数调用。请使用 `ollama_tools.py`：

```bash
# Single request with tools
python3 scripts/ollama_tools.py single qwen2.5-coder:7b "What's the weather in Amsterdam?"

# Full tool loop (model calls tools, gets results, responds)
python3 scripts/ollama_tools.py loop qwen3:4b "Search for Python tutorials and summarize"

# Show available example tools
python3 scripts/ollama_tools.py tools
```

**支持工具的模型：** qwen2.5-coder, qwen3, llama3.1, mistral

## OpenClaw子代理

使用 `sessions_spawn` 创建本地模型的子代理：

```python
# Example: spawn a coding agent
sessions_spawn(
    task="Review this Python code for bugs",
    model="ollama/qwen2.5-coder:7b",
    label="code-review"
)
```

模型路径格式：`ollama/<model-name>`

### 并行代理（思维库模式）

为协作任务创建多个本地代理：

```python
agents = [
    {"label": "architect", "model": "ollama/gemma3:12b", "task": "Design the system architecture"},
    {"label": "coder", "model": "ollama/qwen2.5-coder:7b", "task": "Implement the core logic"},
    {"label": "reviewer", "model": "ollama/llama3.1:8b", "task": "Review for bugs and improvements"},
]

for a in agents:
    sessions_spawn(task=a["task"], model=a["model"], label=a["label"])
```

## 直接API

如需进行自定义集成，请直接使用Ollama API：

```bash
# Chat
curl $OLLAMA_HOST/api/chat -d '{
  "model": "qwen3:4b",
  "messages": [{"role": "user", "content": "Hello"}],
  "stream": false
}'

# Generate
curl $OLLAMA_HOST/api/generate -d '{
  "model": "qwen3:4b",
  "prompt": "Why is the sky blue?",
  "stream": false
}'

# List models
curl $OLLAMA_HOST/api/tags

# Pull model
curl $OLLAMA_HOST/api/pull -d '{"name": "phi3:mini"}'
```

## 故障排除

**连接失败？**
- 检查Ollama是否正在运行：`ollama serve`
- 确认 `OLLAMA_HOST` 的地址是否正确
- 对于远程服务器，请确保防火墙允许端口11434的访问

**模型无法加载？**
- 检查显存（VRAM）：大型模型可能需要CPU卸载部分计算任务
- 先尝试使用较小的模型

**响应缓慢？**
- 模型可能正在使用CPU进行计算
- 尝试使用较低精度的量化格式（例如，使用 `:7b` 而不是 `:30b`）

**OpenClaw子代理是否回退到默认模型？**
- 确保OpenClaw配置中存在 `ollama:default` 的认证配置文件
- 检查模型路径格式：`ollama/modelname:tag`