---
name: sarvam
description: 使用 Sarvam AI 进行印度语言的文本转语音（TTS）、语音转文本（STT）、翻译以及聊天功能。
---
# Sarvam AI技能

该技能提供了对Sarvam AI系列印度语言模型的访问权限。

## 使用方法

### 文本转语音（TTS）

将文本转换为多种印度语言的语音输出。

```bash
python skills/sarvam/scripts/sarvam_cli.py tts "Namaste, kaise hain aap?" --lang hi-IN --speaker meera --output hello.wav
```

**参数：**
- `text`：需要转换成语音的文本。
- `--lang`：语言代码（例如，`hi-IN`表示印地语，`bn-IN`表示孟加拉语等）。
- `--speaker`：语音合成器的名称（例如，`meera`、`pavithra`、`arvind`）。
- `--output`：输出文件的路径（默认：`output.wav`）。

### 语音转文本（STT）

将音频文件转换为文本。

```bash
python skills/sarvam/scripts/sarvam_cli.py stt path/to/audio.wav --model saaras:v3
```

**参数：**
- `file`：音频文件的路径（格式：wav、mp3）。
- `--model`：要使用的模型（默认：`saaras:v3`）。
- `--mode`：语音转文本的模式：
  - `transcribe`：将音频转录为文本。
  - `translate`：将文本翻译成英语。
  - `verbatim`：逐字转录音频内容。
  - `codemix`：混合多种语言的文本和语音。

### 翻译

在印度语言和英语之间进行文本翻译。

```bash
python skills/sarvam/scripts/sarvam_cli.py translate "Hello, how are you?" --source en-IN --target hi-IN
```

**参数：**
- `text`：需要翻译的文本。
- `--source`：源语言代码。
- `--target`：目标语言代码。

### 聊天

与Sarvam的LLM（sarvam-2g）进行交互。

```bash
python skills/sarvam/scripts/sarvam_cli.py chat "What is the capital of India?"
```

**参数：**
- `message`：用户发送的消息。
- `--model`：要使用的模型（默认：`sarvam-2g`）。
- `--system`：可选的系统提示语。

## 设置

1. **环境变量：**
   确保您的API密钥已设置在`.env`文件中（此工作区已配置完成）：
    ```bash
    SARVAM_API_KEY="sk_..."
    ```

2. **虚拟环境：**
   该技能使用位于`skills/sarvam/.venv`的本地虚拟环境。
   所需的依赖库（`requests`）已预先安装在该虚拟环境中。

## 使用方法

使用虚拟环境中的Python命令来执行相应功能：

### 文本转语音（TTS）

```bash
skills/sarvam/.venv/bin/python skills/sarvam/scripts/sarvam_cli.py tts "Namaste, kaise hain aap?" --lang hi-IN --speaker meera --output hello.wav
```

### 语音转文本（STT）

```bash
skills/sarvam/.venv/bin/python skills/sarvam/scripts/sarvam_cli.py stt path/to/audio.wav --model saaras:v3
```

### 翻译

```bash
skills/sarvam/.venv/bin/python skills/sarvam/scripts/sarvam_cli.py translate "Hello, how are you?" --source en-IN --target hi-IN
```

### 聊天

```bash
skills/sarvam/.venv/bin/python skills/sarvam/scripts/sarvam_cli.py chat "What is the capital of India?"
```