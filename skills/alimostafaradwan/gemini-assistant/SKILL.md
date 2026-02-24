---
name: gemini-assistant
description: 这是一个通用型AI助手，它使用Gemini API，支持语音和文本交互。当你需要一个智能AI助手来回答问题、进行对话或协助完成各种任务时，可以使用它。该助手基于谷歌的Gemini模型，具备音频和文本处理能力。
metadata:
  openclaw:
    emoji: "🤖"
---
# Gemini Assistant

这是一个由 Google 的 Gemini API 驱动的通用 AI 助手，支持文本和语音交互。

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

处理程序会返回一个 JSON 响应：

```json
{
  "message": "[[audio_as_voice]]\nMEDIA:/tmp/gemini_voice_xxx.ogg",
  "text": "Text response from Gemini"
}
```

## 配置

设置您的 Gemini API 密钥：

```bash
export GEMINI_API_KEY="your-api-key-here"
```

或者在技能目录下创建一个 `.env` 文件：

```
GEMINI_API_KEY=your-api-key-here
```

## 模型选项

默认模型是 `gemini-2.5-flash-native-audio-preview-12-2025`，支持音频功能。

要使用其他模型，请编辑 `handler.py` 文件：

```python
MODEL = "gemini-2.0-flash-exp"  # For text-only
```

## 系统要求

- `google-genai>=1.0.0`
- `numpy>=1.24.0`
- `soundfile>=0.12.0`
- `librosa>=0.10.0`（用于音频输入）
- FFmpeg（用于音频转换）

## 功能特点

- 🎙️ 语音输入/输出支持
- 💬 文本对话
- 🔧 可配置的系统指令
- ⚡ 使用 Gemini Flash 提供快速响应