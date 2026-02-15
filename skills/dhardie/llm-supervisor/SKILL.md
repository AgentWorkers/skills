---
name: llm-supervisor
description: 使用 Ollama 作为备用方案，实现优雅的速率限制处理机制。当达到速率限制时，系统会发出通知，并允许用户通过确认操作切换到本地模型来继续执行代码任务。
---

# LLM Supervisor 🔮

负责优雅地处理速率限制和模型切换问题。

## 行为规范

### 面对速率限制/过载错误

当遇到来自云服务提供商（如Anthropic、OpenAI）的速率限制或过载错误时：

1. **立即通知用户** — 不要默默失败或无限重试；
2. **提供本地模型作为替代方案** — 询问用户是否希望切换到Ollama；
3. **等待用户确认** — 对于代码生成任务，绝不自动切换模型。

### 需要用户确认

在使用本地模型进行代码生成之前，会询问用户：
> “当前云服务受到速率限制。是否切换到本地Ollama（`qwen2.5:7b`）？请回复‘yes’以确认。”

对于简单的查询（如聊天、摘要生成），如果用户之前已经同意过，可以无需确认即可直接切换。

## 命令

### `/llm status`  
报告当前状态：
- 正在使用的服务提供商（云/本地）；
- Ollama模型的可用性及具体模型；
- 最近的速率限制事件。

### `/llm switch local`  
手动将当前会话切换到Ollama模型。

### `/llm switch cloud`  
将当前会话切换回云服务提供商。

## 使用Ollama模型

```bash
# Check available models
ollama list

# Run a query
ollama run qwen2.5:7b "your prompt here"

# For longer prompts, use stdin
echo "your prompt" | ollama run qwen2.5:7b
```

## 安装的模型

可以使用`ollama list`命令查看已安装的模型。默认配置的模型为`qwen2.5:7b`。

## 状态跟踪

在会话期间，系统会在内存中记录以下状态：
- `currentProvider`：`cloud` 或 `local`；
- `lastRateLimitAt`：发生速率限制的时间戳（或为空）；
- `localConfirmedForCode`：一个布尔值，表示用户是否已确认使用本地模型进行代码生成。

会话开始时，系统会自动将状态重置为使用云服务提供商。