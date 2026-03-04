---
name: qwen3-audio
description: "专为 Apple Silicon 设计的高性能音频库，支持文本转语音（TTS）和语音转文本（STT）功能。"
version: "0.0.3"
---
# Qwen3-Audio

## 概述

Qwen3-Audio 是一个专为 Apple Silicon (M1/M2/M3/M4) 平台优化的高性能音频处理库，提供了快速、高效的文本转语音（TTS）和语音转文本（STT）功能，支持多种模型、语言和音频格式。

## 先决条件

- Python 3.10 或更高版本
- Apple Silicon Mac (M1/M2/M3/M4)

### 环境检查

在使用任何功能之前，请确保 `./references/env-check-list.md` 中的所有项目都已完成。

## 功能

### 文本转语音 (Text to Speech)
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav"
```

**返回值 (JSON):**
```json
{
  "audio_path": "/path_to_save.wav",
  "duration": 1.234,
  "sample_rate": 24000
}
```

### 语音克隆 (Voice Cloning)
可以使用参考音频样本克隆任何语音。提供 wav 文件及其文本记录：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav" --ref_audio "sample_audio.wav" --ref_text "This is what my voice sounds like."
```
ref_audio: 参考音频文件
ref_text: 参考音频的文本记录

### 使用已创建的语音 (Use Created Voice, 快捷方式)
通过 ID 使用 `voice create` 命令创建的语音：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav" --ref_voice "my-voice-id"
```
此操作会自动加载 `ref_audio` 和 `ref_text`。

### CustomVoice (情绪控制)
使用预定义的语音，并可设置情绪/风格：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav" --speaker "Ryan" --language "English" --instruct "Very happy and excited."
```

### VoiceDesign (创建任意语音)
根据文本描述创建任意语音：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "hello world" --output "/path_to_save.wav" --language "English" --instruct "A cheerful young female voice with high pitch and energetic tone."
```

### 自动语音识别 (Automatic Speech Recognition, STT)
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" stt --audio "/sample_audio.wav" --output "/path_to_save.txt" --output-format srt
```
测试音频：https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav
输出格式：`"txt" | "ass" | "srt" | "all"
**返回值 (JSON):**
```json
{
  "text": "transcribed text content",
  "duration": 10.5,
  "sample_rate": 16000,
  "files": ["/path_to_save.txt", "/path_to_save.srt"]
}
```

### 语音管理

语音文件存储在技能根目录下的 `voices/` 目录中。每个语音文件包含以下文件：
- `ref_audio.wav` - 参考音频文件
- `ref_text.txt` - 参考文本记录
- `ref_instruct.txt` - 语音风格描述

#### 创建语音
使用 VoiceDesign 模型创建可重用的语音配置文件。必须使用 `--instruct` 参数来描述语音风格：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" voice create --text "This is a sample voice reference text." --instruct "A warm, friendly female voice with a professional tone." --language "English"
```
可选：`--id "my-voice-id"` 用于指定自定义语音 ID。
**返回值 (JSON):**
```json
{
  "id": "abc12345",
  "ref_audio": "/path/to/skill/voices/abc12345/ref_audio.wav",
  "ref_text": "This is a sample voice reference text.",
  "instruct": "A warm, friendly female voice with a professional tone.",
  "duration": 3.456,
  "sample_rate": 24000
}
```

#### 列出所有语音
列出所有创建的语音配置文件：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" voice list
```

**返回值 (JSON):**
```json
[
  {
    "id": "abc12345",
    "ref_audio": "/path/to/skill/voices/abc12345/ref_audio.wav",
    "ref_text": "This is a sample voice reference text.",
    "instruct": "A warm, friendly female voice with a professional tone.",
    "duration": 3.456,
    "sample_rate": 24000
  }
]
```

#### 使用已创建的语音
创建语音后，可以使用 `--ref_voice` 参数将其用于文本转语音功能。语音风格描述会自动被加载：
```bash
uv run --python ".venv/bin/python" "./scripts/mlx-audio.py" tts --text "New text to speak" --output "/output.wav" --ref_voice "abc12345"
```

## 预定义的扬声器 (CustomVoice)

对于 `Qwen3-TTS-12Hz-1.7B-0.6B-CustomVoice` 模型，支持的扬声器及其描述如下。我们建议使用每个扬声器的原生语言以获得最佳音质。每个扬声器仍可以播放该模型支持的所有语言。

| 扬声器 | 语音描述 | 原生语言 |
| --- | --- | --- |
| Vivian | 明亮、略带活力的年轻女性声音 | 中文 |
| Serena | 温暖、温柔的年轻女性声音 | 中文 |
| Uncle_Fu | 经验丰富的男性声音，音色低沉醇厚 | 中文 |
| Dylan | 青春的北京男性声音，音色清晰自然 | 中文（北京方言） |
| Eric | 活泼的成都男性声音，带有轻微的沙哑感 | 中文（四川方言） |
| Ryan | 动感的男性声音，具有强烈的节奏感 | 英文 |
| Aiden | 阳光般的美国男性声音，中音区清晰 | 英文 |
| Ono_Anna | 活泼的日本女性声音，音色轻快灵活 | 日文 |
| Sohee | 温暖的韩国女性声音，情感表达丰富 | 韩文 |

### 已发布的模型

| 模型 | 特点 | 语言支持 | 语音指令控制 |
|---|---|---|---|
| Qwen3-TTS-12Hz-1.7B-VoiceDesign | 根据用户提供的描述进行语音设计 | 中文、英文、日文、韩文、德文、法文、俄文、葡萄牙文、西班牙文、意大利文 | ✅ |
| Qwen3-TTS-12Hz-1.7B-CustomVoice | 通过用户指令控制目标音色；支持 9 种高级音色，涵盖性别、年龄、语言和方言的组合 | 中文、英文、日文、韩文、德文、法文、俄文、葡萄牙文、西班牙文、意大利文 | ✅ |
| Qwen3-TTS-12Hz-1.7B-Base | 基础模型，能够从用户音频输入快速克隆语音（3 秒内）；可用于其他模型的微调 | 中文、英文、日文、韩文、德文、法文、俄文、葡萄牙文、西班牙文、意大利文 |  |