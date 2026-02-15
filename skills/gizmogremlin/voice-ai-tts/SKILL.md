---
name: voice-ai-tts
description: >
  High-quality voice synthesis with 9 personas, 11 languages, streaming, and voice cloning using Voice.ai API.
---

# Voice.ai 语音合成服务

## ✨ 主要功能

- **9种语音角色**：专为不同使用场景精心挑选的语音
- **11种语言**：支持多语言合成，采用多语言模型
- **流式输出模式**：在生成音频的同时实时输出
- **语音克隆**：能够根据音频样本克隆新的语音
- **语音定制**：可通过 `temperature` 和 `top_p` 参数调整语音特性
- **与OpenClaw集成**：兼容OpenClaw内置的语音合成（TTS）功能

## 🎙️ 可用语音

| 语音名称 | 性别 | 适用场景                |
|---------|--------|-------------------------|
| ellie   | 女性    | 视频博客、社交内容               |
| oliver  | 男性    | 解说、教程                   |
| lilith  | 女性    | 轻柔的语音（适合ASMR、舒缓内容）         |
| smooth  | 男性    | 沉稳的语音（适合纪录片、有声书）           |
| corpse  | 男性    | 独特的语音风格（适合游戏、娱乐内容）       |
| skadi   | 女性    | 动漫风格的语音                |
| zhongli | 男性    | 沉稳的语音（适合游戏、戏剧性内容）         |
| flora   | 女性    | 愉快的语音（适合儿童内容、轻松的氛围）       |
| chief   | 男性    | 英雄主义风格的语音（适合游戏、动作场景）       |

## 🌍 支持的语言

- 英语（en）
- 西班牙语（es）
- 法语（fr）
- 德语（de）
- 意大利语（it）
- 葡萄牙语（pt）
- 波兰语（pl）
- 俄语（ru）
- 荷兰语（nl）
- 瑞典语（sv）
- 加泰罗尼亚语（ca）

## 🎨 语音定制

可通过以下参数自定义语音输出效果：

- **temperature**（0-2）：数值越高，语音表达越丰富；数值越低，语音越连贯
- **top_p**（0-1）：控制语音生成的随机性

## 📡 流式输出模式

支持实时流式输出音频（适用于较长的文本）

```bash
# Stream audio as it generates
node scripts/tts.js --text "This is a long story..." --voice ellie --stream

# Streaming with custom output
node scripts/tts.js --text "Chapter one..." --voice oliver --stream --output chapter1.mp3
```

## 🔗 与OpenClaw的集成

Voice.ai的语音合成功能可与OpenClaw的内置TTS（Text-to-Speech）模块无缝集成。

## 💬 在聊天中触发语音合成

您可以在聊天应用中通过特定指令触发语音合成功能。

## 💻 命令行接口（CLI）使用方法

Voice.ai提供命令行接口（CLI）以支持自动化操作。

## 🔗 相关链接

- [Voice.ai官方文档](https://voice.ai/docs)
- [API参考文档](https://voice.ai/docs/api-reference/text-to-speech/generate-speech)

---

由 [Nick Gill](https://github.com/gizmoGremlin) 用爱心制作。