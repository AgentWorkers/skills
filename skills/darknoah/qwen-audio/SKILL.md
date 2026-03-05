---
name: qwen-audio
description: "这是一个高性能的音频库，支持文本转语音（TTS）和语音转文本（STT）功能。"
version: "0.0.4"
---
# Qwen-Audio

## 概述

Qwen-Audio 是一个高性能的音频处理库，经过优化，能够提供快速、高效的文本转语音（TTS）和语音转文本（STT）功能，支持多种模型、语言和音频格式。

## 先决条件

- Python 3.10 或更高版本

### 环境检查

在使用任何功能之前，请确保 `./references/env-check-list.md` 中列出的所有项都已满足。

## 功能

### 语音管理

语音文件存储在技能根目录下的 `./voices/` 目录中。每个语音文件都有一个独立的文件夹，其中包含以下文件：
- `ref_audio.wav`：参考音频文件
- `ref_text.txt`：参考文本
- `ref_instruct.txt`：语音风格描述

#### 创建语音
可以使用 VoiceDesign 模型创建一个可重用的语音配置文件。必须使用 `--instruct` 参数来描述语音风格：
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" voice create --text "This is a sample voice reference text." --instruct "A warm, friendly female voice with a professional tone." --id "my-voice-id"
```
可选：`--id "my-voice-id"` 用于指定自定义语音 ID。

**返回值（JSON）：**
```json
{
  "id": "my-voice-id",
  "ref_audio": "/<qwen-audio-skill-path>/voices/my-voice-id/ref_audio.wav",
  "ref_text": "This is a sample voice reference text.",
  "instruct": "A warm, friendly female voice with a professional tone.",
  "duration": 3.456,
  "sample_rate": 24000,
  "success": true
}
```


#### 列出所有语音
列出所有已创建的语音配置文件：
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" voice list
```

**返回值（JSON）：**
```json
[
  {
    "id": "my-voice-id",
    "ref_audio": "/<qwen-audio-skill-path>/voices/my-voice-id/ref_audio.wav",
    "ref_text": "This is a sample voice reference text.",
    "instruct": "A warm, friendly female voice with a professional tone.",
    "duration": 3.456,
    "sample_rate": 24000
  }
]
```


### 文本转语音（TTS）

#### TTS 语音预检查（必选）
在进行任何 `tts` 生成操作之前，请先确认可用的语音：
1. 运行 `voice list` 命令查看当前可用的语音配置文件。
2. 如果返回的列表为空，请停止操作并询问用户希望创建哪种类型的语音。提供语音风格选项，例如：
   - 温暖友好的女性旁白
   - 深沉稳重的男性播报音
   - 年轻充满活力的中性音调
   - 平静专业的客服语音
   确认用户选择了所需的语音风格后，再运行 `voice create` 命令。
3. 如果返回的列表不为空，请显示可用的语音 ID，并询问用户选择哪个 ID 作为 `--ref_voice` 参数进行语音生成。
只有在完成确认步骤后，才能执行 `tts` 操作。

**返回值（JSON）：**
```json
{
  "audio_path": "/path/to/save.wav",
  "duration": 1.234,
  "sample_rate": 24000,
  "success": true
}
```


### 语音克隆
可以使用参考音频样本克隆任意语音。需要提供音频文件（.wav 格式）及其对应的文本文件：
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" tts --text "hello world" --output "/path/to/save.wav" --ref_audio "sample_audio.wav" --ref_text "This is what my voice sounds like."
```
ref_audio: 参考音频文件
ref_text: 参考音频的文本


#### 使用创建的语音
创建语音配置文件后，可以通过 `--ref_voice` 参数将其用于 TTS 生成。语音风格描述（instruct）会自动被应用：
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" tts --text "New text to speak" --output "/path/to/save.wav" --ref_voice "my-voice-id" --instruct "Very happy and excited."
```
可选：`--instruct` 参数用于控制语音的情感表达。

### 自动语音识别（STT）
```bash
uv run --project "/<qwen-audio-skill-path>" python "<qwen-audio-skill-path>/scripts/qwen-audio.py" stt --audio "/sample_audio.wav" --output "/path/to/save.txt" --output-format txt
```
测试音频文件：https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-ASR-Repo/asr_en.wav
支持的输出格式：`"txt" | "ass" | "srt" | "all"

**返回值（JSON）：**
```json
{
  "text": "transcribed text content",
  "duration": 10.5,
  "sample_rate": 16000,
  "files": ["/path/to/save.txt", "/path/to/save.srt"],
  "success": true
}
```