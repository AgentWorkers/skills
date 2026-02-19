---
name: anthropic
description: "Anthropic Claude API集成：通过Anthropic Messages API实现聊天对话的自动完成、视频流处理、图像分析、工具调用以及批量处理功能。可以利用Claude Opus、Sonnet和Haiku模型生成文本，处理图像数据，调用各种工具，并管理对话流程。该集成专为AI代理设计，仅依赖Python标准库，无任何外部依赖项。适用于AI文本生成、多模态数据分析、工具辅助的AI应用以及Claude模型的交互操作。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔮", "requires": {"env": ["ANTHROPIC_API_KEY"]}, "primaryEnv": "ANTHROPIC_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🔮 Anthropic

Anthropic 提供了与 Claude API 的集成功能，支持聊天对话、实时响应流、图像分析、工具使用以及批量处理等功能，这些功能均通过 Anthropic Messages API 实现。

## 主要特性

- **Messages API**：支持 Claude Opus、Sonnet、Haiku 等诗歌创作模式的文本生成。
- **实时响应流**：能够以流式方式接收 Claude 的实时响应。
- **图像分析**：具备图像识别和处理能力。
- **工具使用**：允许用户调用特定工具并获取结构化的输出结果。
- **系统提示**：可以自定义系统发出的提示信息。
- **多轮对话**：支持上下文管理，确保对话的连贯性。
- **批量处理 API**：支持批量发送请求和处理结果。
- **请求预统计**：在发送请求前可预估所需使用的 API 令牌数量。
- **扩展思维模式**：提供更复杂的推理能力。
- **模型列表**：可查看可用的模型及其功能。

## 使用要求

| 变量 | 必需条件 | 说明 |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ | 用于访问 Anthropic API 的 API 密钥/令牌 |

## 快速入门

```bash
# Send a message to Claude
python3 {baseDir}/scripts/anthropic.py chat "What is the meaning of life?" --model claude-sonnet-4-20250514
```

```bash
# Chat with system prompt
python3 {baseDir}/scripts/anthropic.py chat-system --system "You are a financial analyst" "Analyze AAPL stock"
```

```bash
# Analyze an image
python3 {baseDir}/scripts/anthropic.py chat-image --image photo.jpg 'What do you see in this image?'
```

```bash
# Stream a response
python3 {baseDir}/scripts/anthropic.py stream "Write a short story about a robot" --model claude-sonnet-4-20250514
```



## 命令说明

### `chat`  
向 Claude 发送消息。  
```bash
python3 {baseDir}/scripts/anthropic.py chat "What is the meaning of life?" --model claude-sonnet-4-20250514
```

### `chat-system`  
与系统提示进行对话。  
```bash
python3 {baseDir}/scripts/anthropic.py chat-system --system "You are a financial analyst" "Analyze AAPL stock"
```

### `chat-image`  
分析指定的图像。  
```bash
python3 {baseDir}/scripts/anthropic.py chat-image --image photo.jpg 'What do you see in this image?'
```

### `stream`  
以流式方式接收 Claude 的响应。  
```bash
python3 {baseDir}/scripts/anthropic.py stream "Write a short story about a robot" --model claude-sonnet-4-20250514
```

### `batch-create`  
创建一个批量处理请求。  
```bash
python3 {baseDir}/scripts/anthropic.py batch-create requests.jsonl
```

### `batch-list`  
列出所有待处理的批量任务。  
```bash
python3 {baseDir}/scripts/anthropic.py batch-list
```

### `batch-get`  
获取批量任务的执行状态。  
```bash
python3 {baseDir}/scripts/anthropic.py batch-get batch_abc123
```

### `batch-results`  
获取批量处理的结果。  
```bash
python3 {baseDir}/scripts/anthropic.py batch-results batch_abc123
```

### `count-tokens`  
统计消息中包含的 API 令牌数量。  
```bash
python3 {baseDir}/scripts/anthropic.py count-tokens "How many tokens is this message?"
```

### `models`  
查看可用的模型列表。  
```bash
python3 {baseDir}/scripts/anthropic.py models
```

### `tools`  
通过聊天界面使用相关工具。  
```bash
python3 {baseDir}/scripts/anthropic.py tools --tools '[{"name":"get_weather","description":"Get weather","input_schema":{"type":"object","properties":{"location":{"type":"string"}}}}]' "What is the weather in NYC?"
```

### `thinking`  
启用扩展思维模式（需要额外配置）。  
```bash
python3 {baseDir}/scripts/anthropic.py thinking "Solve this math problem step by step: what is 123 * 456?" --budget 10000
```

## 输出格式

所有命令默认以 JSON 格式输出。若需以更易读的格式查看结果，可使用 `--human` 参数。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/anthropic.py chat --limit 5

# Human-readable
python3 {baseDir}/scripts/anthropic.py chat --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |  
|--------|-------------|  
| `{baseDir}/scripts/anthropic.py` | 主要的命令行工具，用于执行所有与 Anthropic 相关的操作。 |

## 数据政策

本技能 **绝不** 在本地存储任何数据。所有请求都会直接发送到 Anthropic API，处理结果会直接输出到标准输出（stdout）。您的数据将保存在 Anthropic 的服务器上。

## 致谢  
本技能由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关内容也发布在 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi) 上。  
本技能属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的业务配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)