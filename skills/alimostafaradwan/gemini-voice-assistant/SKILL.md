---
name: gemini-voice-assistant
description: 基于 Gemini Live API 的语音交互 AI 助手：您可以与 AI 对话并接收语音形式的回复。当您希望与由 Google 的 Gemini 模型驱动的 AI 助手进行自然的语音交流时，可以使用该功能。
metadata:
  openclaw:
    emoji: "🎙️"
---
# Gemini 语音助手

这是一个基于 Google 的 Gemini Live API 开发的语音交互式 AI 助手。你可以与它进行对话，它会用自然的声音回应你。

## 使用方法

### 文本模式

```bash
cd ~/.openclaw/agents/kashif/skills/gemini-assistant && python3 handler.py "Your question or message"
```

### 语音模式

```bash
cd ~/.openclaw/agents/kashif/skills/gemini-assistant && python3 handler.py --audio /path/to/audio.ogg "optional context"
```

## 响应格式

处理程序会返回一个 JSON 格式的响应：

```json
{
  "message": "[[audio_as_voice]]\nMEDIA:/tmp/gemini_voice_xxx.ogg",
  "text": "Text response from Gemini"
}
```

## 配置

设置你的 Gemini API 密钥：

```bash
export GEMINI_API_KEY="your-api-key-here"
```

或者可以在技能（skill）目录下创建一个 `.env` 文件来存储 API 密钥：

```
GEMINI_API_KEY=your-api-key-here
```

## 模型选项

默认使用的模型是 `gemini-2.5-flash-native-audio-preview-12-2025`，以支持音频功能。

如果你想使用其他模型，请编辑 `handler.py` 文件：

```python
MODEL = "gemini-2.0-flash-exp"  # For text-only
```

## 系统要求

- `google-genai` 版本需大于或等于 1.0.0
- `numpy` 版本需大于或等于 1.24.0
- `soundfile` 版本需大于或等于 0.12.0
- `librosa` 版本需大于或等于 0.10.0（用于音频输入）
- FFmpeg（用于音频转换）

## 功能特点

- 🎙️ 支持语音输入/输出
- 💬 可以进行文本对话
- 🔧 可配置系统指令
- ⚡ 使用 Gemini Flash 技术实现快速响应