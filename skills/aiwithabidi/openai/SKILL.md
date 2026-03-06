---
name: openai
description: "OpenAI API集成：通过OpenAI的REST API实现聊天功能、文本生成、图像生成、音频转录、文件管理以及AI助手的开发。支持使用DALL-E生成图像，利用Whisper进行音频转录，管理模型微调任务，并构建AI助手。该工具专为AI应用设计，仅依赖Python标准库，无需额外依赖任何第三方库。适用于AI文本生成、图像创作、语音转文本、模型微调以及AI助手的开发。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": ["OPENAI_API_KEY"]}, "primaryEnv": "OPENAI_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🧠 OpenAI

OpenAI API 提供了一系列功能，包括聊天补全、文本嵌入、图像生成、音频转录、文件管理、模型微调以及通过 OpenAI REST API 创建和管理 AI 助手等。

## 主要功能

- **聊天补全**：支持 GPT-4o、GPT-5 和 o1 模型的响应。
- **文本嵌入**：使用 text-embedding-3 技术进行语义搜索。
- **图像生成**：能够生成和编辑 DALL-E 3 图像。
- **音频转录**：支持将语音转换为文本（Whisper 技术）。
- **文本转语音**：提供多种语音选项的 TTS（文本转语音）功能。
- **文件管理**：允许上传和操作文件。
- **模型微调**：支持创建和管理模型微调任务。
- **AI 助手**：可以构建和管理 AI 助手。
- **内容审核**：提供内容审核功能。
- **模型信息**：列出可用的模型及其详细信息。

## 必需参数

| 参数 | 是否必需 | 说明 |
|--------|---------|-------|
| `OPENAI_API_KEY` | ✅ | 用于访问 OpenAI API 的密钥/令牌 |

## 快速入门

```bash
# Send chat completion
python3 {baseDir}/scripts/openai.py chat "Explain quantum computing in 3 sentences" --model gpt-4o
```

```bash
# Chat with system prompt
python3 {baseDir}/scripts/openai.py chat-system --system "You are a Python expert" "How do I use asyncio?"
```

```bash
# Generate embeddings
python3 {baseDir}/scripts/openai.py embed "The quick brown fox" --model text-embedding-3-small
```

```bash
# Generate an image
python3 {baseDir}/scripts/openai.py image "A sunset over mountains, oil painting style" --size 1024x1024
```



## 命令说明

### `chat`  
发送聊天请求，获取聊天结果。  
```bash
python3 {baseDir}/scripts/openai.py chat "Explain quantum computing in 3 sentences" --model gpt-4o
```

### `chat-system`  
与系统进行交互（使用系统提示）。  
```bash
python3 {baseDir}/scripts/openai.py chat-system --system "You are a Python expert" "How do I use asyncio?"
```

### `embed`  
生成文本嵌入（用于语义搜索）。  
```bash
python3 {baseDir}/scripts/openai.py embed "The quick brown fox" --model text-embedding-3-small
```

### `image`  
生成图像。  
```bash
python3 {baseDir}/scripts/openai.py image "A sunset over mountains, oil painting style" --size 1024x1024
```

### `transcribe`  
将音频文件转录为文本。  
```bash
python3 {baseDir}/scripts/openai.py transcribe recording.mp3
```

### `tts`  
将文本转换为语音（支持多种语音）。  
```bash
python3 {baseDir}/scripts/openai.py tts "Hello, welcome to our service" --voice alloy --output greeting.mp3
```

### `models`  
列出所有可用的模型。  
```bash
python3 {baseDir}/scripts/openai.py models
```

### `model-get`  
获取模型的详细信息。  
```bash
python3 {baseDir}/scripts/openai.py model-get gpt-4o
```

### `files`  
列出已上传的文件。  
```bash
python3 {baseDir}/scripts/openai.py files
```

### `file-upload`  
上传文件。  
```bash
python3 {baseDir}/scripts/openai.py file-upload data.jsonl --purpose fine-tune
```

### `fine-tune`  
创建模型微调任务。  
```bash
python3 {baseDir}/scripts/openai.py fine-tune '{"training_file":"file-abc123","model":"gpt-4o-mini"}'
```

### `fine-tune-list`  
列出所有的模型微调任务。  
```bash
python3 {baseDir}/scripts/openai.py fine-tune-list
```

### `moderate`  
检查内容是否符合审核标准。  
```bash
python3 {baseDir}/scripts/openai.py moderate "Some text to check"
```

### `usage`  
查看 API 的使用情况。  
```bash
python3 {baseDir}/scripts/openai.py usage --date 2026-02-01
```

### `assistants`  
列出所有的 AI 助手。  
```bash
python3 {baseDir}/scripts/openai.py assistants
```

## 输出格式

所有命令默认以 JSON 格式输出。若需以更易读的格式输出，可使用 `--human` 选项。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/openai.py chat --limit 5

# Human-readable
python3 {baseDir}/scripts/openai.py chat --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|------|------|
| `{baseDir}/scripts/openai.py` | 主要的命令行工具，用于执行所有 OpenAI 相关操作 |

## 数据政策

本技能 **从不将数据存储在本地**。所有请求都会直接发送到 OpenAI API，结果会返回到标准输出（stdout），数据会保存在 OpenAI 服务器上。

## 致谢  
本技能由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关内容可在 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi) 查看。  
本技能属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)