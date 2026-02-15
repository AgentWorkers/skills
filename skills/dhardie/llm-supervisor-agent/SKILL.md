# LLM Supervisor

当遇到速率限制时，该工具会自动在云端的 Ollama 模型和本地的 Ollama 模型之间切换。

## 主要功能

- 检测来自 Anthropic/OpenAI 的速率限制/过载错误
- 自动切换到本地的 Ollama 模型作为备用方案
- 在生成本地代码之前需要用户明确确认
- 支持手动执行以下命令：

### 可用命令

- `/llm status`  
- `/llm switch cloud`  
- `/llm switch local`  

## 默认的本地模型

- `qwen2.5:7b`  

## 安全性注意事项

在生成本地代码之前，用户需要输入以下确认指令：

`CONFIRM LOCAL CODE`