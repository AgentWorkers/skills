---
name: elevenlabs-ai
description: OpenClaw技能适用于ElevenLabs的APIs，支持以下功能：文本转语音（text-to-speech）、语音转文本（speech-to-text）、实时语音转文本（realtime speech-to-text）、语音合成（voices/models）以及对话工作流程（dialogue workflows）。
---

# ElevenLabs API 技能（高级）

## 目的  
提供一份面向生产环境的指南，指导如何通过直接 HTTPS（无需 SDK）使用 ElevenLabs 的 API，同时涵盖身份验证、安全性和工作流程等方面的内容。

## 适用场景  
- 需要文本转语音（TTS）或语音转文本（STT）功能。  
- 希望实现低延迟的实时语音转文本功能。  
- 偏好使用可预测输出结果的直接 HTTP 调用方式。  

## 不适用场景  
- 需要完整的 SDK 集成及辅助工具。  
- 需要超出简单音频输入/输出功能的复杂对话系统。  

## 快速入门指南  
- 请参阅 `references/elevenlabs-authentication.md` 以获取 API 密钥和一次性令牌。  
- 请参阅 `references/elevenlabs-text-to-speech.md` 了解 TTS 端点及数据格式要求。  
- 请参阅 `references/elevenlabs-speech-to-speech.md` 了解语音转换的相关信息。  
- 请参阅 `references/elevenlabs-speech-to-text-realtime.md` 了解实时语音转文本（WebSocket）功能。  
- 请参阅 `references/elevenlabs-text-to-dialogue.md` 了解多语音对话系统的实现方法。  
- 请参阅 `references/elevenlabs-voices-models.md` 了解语音 ID 及模型选择方式。  
- 请参阅 `references/elevenlabs-safety-and-privacy.md` 了解数据安全与隐私保护规则。  

## 必需输入  
- API 密钥（xi-api-key）或根据需求使用的一次性令牌。  
- 目标使用场景所需的语音 ID 和模型 ID。  
- 输出格式（音频编码格式、采样率、比特率）。  

## 预期输出  
- 明确的工作流程方案、端点使用清单以及操作规范。  

## 操作注意事项  
- 严格限制音频输出的接收方。  
- 在服务器端缓存语音 ID 和模型 ID。  
- 保持数据包大小较小，并在请求被限制时采用重试机制。  

## 安全注意事项  
- 绝不要记录 API 密钥或令牌信息。  
- 客户端访问应使用一次性令牌。