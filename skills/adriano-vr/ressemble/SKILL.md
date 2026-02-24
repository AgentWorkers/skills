---
name: ressemble
displayName: Ressemble - Adriano
version: 1.0.0
description: 使用 Resemble AI 的 HTTP API 进行文本转语音（Text-to-Speech）和语音转文本（Speech-to-Text）的集成。
author: Adriano Vargas
tags: [tts, stt, audio, ai, voice]
---
# Resemble – 文本与语音AI集成

该技能将OpenClaw与Resemble AI的HTTP API集成在一起，实现了以下功能：

- 🎙 语音转文本（音频转录）
- 🔊 文本转语音（语音合成）

它通过直接的HTTP请求与Resemble AI的生产端点进行交互，并支持异步转录请求的轮询。

---

## 功能

### resemble-tts
根据文本输入生成高质量的语音音频。

支持：
- 自定义`voice_uuid`
- MP3输出格式
- 以Base64格式返回音频文件

### resemble-stt
使用Resemble AI将音频文件转录为文本。

支持：
- 分块上传音频文件
- 自动轮询直至转录完成
- 返回清晰的转录文本

---

## 需求

您需要定义以下环境变量：

```bash
export RESEMBLE_API_KEY="your_api_key_here"
```