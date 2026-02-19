---
name: sarvam
description: 使用 Sarvam AI 进行印度语言的文本转语音（TTS）、语音转文本（STT）、翻译以及聊天功能。
metadata: {"clawdbot":{"emoji":"🧘","requires":{"env":["SARVAM_API_KEY"],"bins":["skills/sarvam/.venv/Scripts/python.exe"]},"primaryEnv":"SARVAM_API_KEY","installNotes":"Requires SARVAM_API_KEY. Local script execution may require explicit pathing (e.g., .\\skills\\sarvam\\.venv\\Scripts\\python.exe) due to current shell environment."}}
---
# Sarvam AI 技能

该技能提供了对 Sarvam AI 提供的多种印度语言模型的访问权限。

## 使用方法

### 文本转语音（TTS）

将文本转换为多种印度语言的语音输出。

**参数：**
- `text`：需要转换成语音的文本。
- `--lang`：语言代码（例如，`hi-IN` 表示印地语，`bn-IN` 表示孟加拉语等）。
- `--speaker`：语音合成器的名称（例如，`meera`、`pavithra`、`arvind`）。
- `--output`：输出文件的路径（默认为 `output.wav`）。

### 语音转文本（STT）

将音频文件转换为文本。

**参数：**
- `file`：音频文件的路径（格式为 wav 或 mp3）。
- `--model`：使用的模型（默认为 `saaras:v3`）。
- `--mode`：转换模式：
  - `transcribe`：将音频转录为文本。
  - `translate`：将文本翻译成英语。
  - `verbatim`：逐字转录音频内容。
  - `codemix`：混合多种语言的文本。

### 翻译

在印度语言与英语之间进行文本翻译。

**参数：**
- `text`：需要翻译的文本。
- `--source`：源语言代码。
- `--target`：目标语言代码。

### 聊天

与 Sarvam 的大型语言模型（sarvam-2g）进行交互。

**参数：**
- `message`：用户发送的消息。
- `--model`：使用的模型（默认为 `sarvam-2g`）。
- `--system`：可选的系统提示信息。

## 设置

1. **环境变量：**
   确保您的 API 密钥已配置在 `.env` 文件中（此工作区已配置完成）：
   ```bash
    SARVAM_API_KEY="sk_..."
    ```

2. **虚拟环境：**
   该技能使用位于 `skills/sarvam/.venv` 的本地虚拟环境。
   所需的依赖库（`requests`）已预先安装在该虚拟环境中。

## 使用方法

使用虚拟环境中的 Python 命令来执行相应功能：

### 文本转语音（TTS）

### 语音转文本（STT）

### 翻译

### 聊天