---
name: qwen3-audio
description: "专为苹果硅架构设计的高性能音频库，支持文本转语音（TTS）和语音转文本（STT）功能。"
version: "0.0.3"
---
# Qwen3-Audio

## 概述

Qwen3-Audio 是一个专为 Apple Silicon (M1/M2/M3/M4) 平台优化的高性能音频处理库，能够提供快速、高效的文本转语音（TTS）和语音转文本（STT）功能，同时支持多种模型、语言和音频格式。

## 前提条件

- Python 3.10 或更高版本
- 使用 Apple Silicon 架构的 Mac 电脑（M1/M2/M3/M4）

### 环境检查

在使用任何功能之前，请确保 `./references/env-check-list.md` 文件中的所有要求都已满足。

## 功能介绍

### 文本转语音（Text to Speech）
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav"
```

**返回值（JSON）：**
```json
{
  "audio_path": "/path_to_save.wav",
  "duration": 1.234,
  "sample_rate": 24000
}
```

### 语音克隆（Voice Cloning）
可以使用参考音频样本克隆任意语音。请提供音频文件（wav 格式）及其对应的文本：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav" --ref_audio "sample_audio.wav" --ref_text "This is what my voice sounds like."
```
```python
ref_audio: 参考音频文件
ref_text: 参考音频的文本内容
```

### 使用已创建的语音（Use Created Voice，快捷方式）
可以通过语音 ID 来使用使用 `voice create` 命令创建的语音：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav" --ref_voice "my-voice-id"
```
此命令会自动加载 `ref_audio` 和 `ref_text` 文件。

### CustomVoice（情感控制）
可以使用预定义的语音，并通过指令控制其情感或风格：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav" --speaker "Ryan" --language "English" --instruct "Very happy and excited."
```

### VoiceDesign（创建任意语音）
可以根据文本描述创建新的语音：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav" --language "English" --instruct "A cheerful young female voice with high pitch and energetic tone."
```

### 自动语音识别（Automatic Speech Recognition, STT）
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" stt --audio "/sample_audio.wav" --output "/path_to_save.txt" --output-format srt
```
测试音频文件：https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav
**输出格式：** "txt" | "ass" | "srt" | "all"
**返回值（JSON）：**
```json
{
  "text": "transcribed text content",
  "duration": 10.5,
  "sample_rate": 16000,
  "files": ["/path_to_save.txt", "/path_to_save.srt"]
}
```

### 语音管理
所有语音文件都存储在技能根目录下的 `voices/` 目录中。每个语音文件包含以下文件：
- `ref_audio.wav`：参考音频文件
- `ref_text.txt`：参考文本文件

#### 创建语音
可以创建一个可重复使用的语音配置文件，用于语音克隆：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" voice create --text "This is a sample voice reference text." --language "English"
```
**可选参数：** `--id "my-voice-id"` 用于指定自定义语音 ID。
**返回值（JSON）：**
```json
{
  "id": "abc12345",
  "ref_audio": "/path/to/skill/voices/abc12345/ref_audio.wav",
  "ref_text": "This is a sample voice reference text.",
  "duration": 3.456,
  "sample_rate": 24000
}
```

#### 列出所有语音
可以列出所有已创建的语音配置文件：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" voice list
```
**返回值（JSON）：**
```json
[
  {
    "id": "abc12345",
    "ref_audio": "/path/to/skill/voices/abc12345/ref_audio.wav",
    "ref_text": "This is a sample voice reference text.",
    "duration": 3.456,
    "sample_rate": 24000
  }
]
```

#### 使用已创建的语音
创建语音后，可以通过 `--ref_voice` 参数将其用于文本转语音功能：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "New text to speak" --output "/output.wav" --ref_voice "abc12345"
```

## 预定义的语音角色（CustomVoice）

对于 `Qwen3-TTS-12Hz-1.7B-0.6B-CustomVoice` 模型，支持的语音角色及其描述如下。建议使用每个角色的母语以获得最佳音质。每个角色仍能使用模型支持的所有语言进行语音输出。

| 角色 | 语音描述 | 母语 |
| --- | --- | --- |
| Vivian | 明亮、略带活力的年轻女性声音 | 中文 |
| Serena | 温暖、温柔的年轻女性声音 | 中文 |
| Uncle_Fu | 经验丰富的男性声音，音色低沉醇厚 | 中文 |
| Dylan | 青春的北京男性声音，音色清晰自然 | 中文（北京方言） |
| Eric | 活泼的成都男性声音，略带沙哑的音色 | 中文（四川方言） |
| Ryan | 动感有力的男性声音 | 英文 |
| Aiden | 阳光般的美国男性声音，中音部分清晰 | 英文 |
| Ono_Anna | 活泼的日本女性声音，音色轻快灵活 | 日文 |
| Sohee | 温暖的韩国女性声音，情感表达丰富 | 韩文 |

### 已发布的模型

| 模型 | 功能 | 支持的语言 | 指令控制 |
| --- | --- | --- | --- |
| Qwen3-TTS-12Hz-1.7B-VoiceDesign | 根据用户提供的描述进行语音设计 | 中文、英文、日文、韩文、德文、法文、俄文、葡萄牙文、西班牙文、意大利文 | ✅ |
| Qwen3-TTS-12Hz-1.7B-CustomVoice | 允许用户通过指令控制目标音色；支持 9 种高级音色组合（包括性别、年龄、语言和方言） | 中文、英文、日文、韩文、德文、法文、俄文、葡萄牙文、西班牙文、意大利文 | ✅ |
| Qwen3-TTS-12Hz-1.7B-Base | 基础模型，可以从用户提供的音频快速克隆语音（最长 3 秒）；可用于其他模型的微调 | 中文、英文、日文、韩文、德文、法文、俄文、葡萄牙文、西班牙文、意大利文 |  |