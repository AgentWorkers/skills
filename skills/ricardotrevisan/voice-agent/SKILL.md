---
name: voice-agent
display-name: AI Voice Agent Backend
version: 1.1.0
description: 使用 AI Voice Agent API 的代理程序的本地语音输入/输出功能。
author: trevisanricardo
homepage: https://github.com/ricardotrevisan/ai-conversational-skill
user-invocable: true
disable-model-invocation: false
---

# 语音代理（Voice Agent）

该技能允许您通过本地的语音代理 API 与用户进行语音交流（即用户说话，您也通过语音回应用户）。该技能仅适用于客户端，不会启动任何容器或服务。它使用 **local Whisper** 进行语音转文本（Speech-to-Text）的转录，以及 **AWS Polly** 进行文本转语音（Text-to-Speech）的生成。

## 先决条件
需要一个正在运行的后端 API，地址为 `http://localhost:8000`。后端服务的设置说明请参考以下文件：
- `README.md`
- `walkthrough.md`
- `DOCKER_README.md`

## 行为规范
- **优先使用音频响应**：当用户通过音频文件进行交流时，您的主要响应方式应为音频文件。
- **静默传输**：在发送音频响应时，**不要**附加任何文字说明（例如 “我已发送了音频文件”），只需直接传输音频文件即可。
- **工作流程**：
    1. 用户发送音频文件。
    2. 使用 `transcribe` 命令对音频文件进行转录。
    3. 您思考并准备响应内容。
    4. 使用 `synthesize` 命令生成音频文件。
    5. 将生成的音频文件发送给用户。
    6. 完成响应后，**不要**添加任何文字说明。
- **错误处理**：如果语音代理 API 出现故障或连接问题，请不要尝试通过该技能进行服务管理。请用户根据仓库中的文档来启动或修复后端服务。

## 工具

### 转录音频文件（Transcribe File）
要使用 **local Whisper** 的语音转文本功能转录音频文件，请运行客户端脚本并使用 `transcribe` 命令。

```bash
python3 {baseDir}/scripts/client.py transcribe "/path/to/audio/file.ogg"
```

### 生成音频文件（Synthesize to File）
要使用 **AWS Polly** 的文本转语音功能将文本转换为音频文件并保存到本地，请运行客户端脚本并使用 `synthesize` 命令。

```bash
python3 {baseDir}/scripts/client.py synthesize "Text to speak" --output "/path/to/output.mp3"
```

### 健康检查（Health Check）
要检查语音代理 API 是否正在运行且状态正常，请执行相应的检查操作。

```bash
python3 {baseDir}/scripts/client.py health
```