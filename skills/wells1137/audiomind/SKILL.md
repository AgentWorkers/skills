---
name: AudioMind
version: 2.0.0
author: "@wells1137"
emoji: "🧠"
tags:
  - audio
  - tts
  - music
  - sfx
  - voice-clone
  - elevenlabs
  - fal
description: 这款终极AI音频生成工具能够智能地将请求路由到ElevenLabs和fal.ai提供的18种以上模型，以实现文本转语音（TTS）、音乐生成、音效制作以及语音克隆等功能。无需任何配置，只需简单发起请求即可使用。
---
## 描述

**AudioMind** 是一项功能齐全、无需额外配置的音频生成技能，能够满足您的所有音频需求。它能够智能地将您的自然语言请求路由到来自 **ElevenLabs** 和 **fal.ai** 等领先提供商的 18 个专业音频模型库中。

只需安装此技能，您的智能助手即可立即具备以下功能：

- **文本转语音（TTS）**：支持 9 种不同的模型，适用于多种语言、风格和延迟要求。
- **音乐生成**：能够创作免版税的器乐曲目，涵盖多种音乐风格。
- **音效（SFX）生成**：根据文本描述生成各种音效。
- **语音克隆**：从音频样本中克隆声音以生成新的语音内容。

该技能由一个后端代理服务提供支持，该服务负责安全地管理 API 密钥和使用情况，为用户带来无缝、即插即用的使用体验。

## 工作原理

1. **安装**：用户安装 `audiomind` 技能。
2. **请求**：用户提出音频相关的自然语言请求（例如：“*生成一段火车经过的声音效果*”）。
3. **智能路由**：AudioMind 分析请求内容，并从内部模型库中选择最适合的模型来处理该请求。
4. **代理调用**：该技能将结构化请求发送到 AudioMind 代理服务。
5. **API 执行**：代理服务使用正确的参数调用相应的底层 API（ElevenLabs 或 fal.ai）。
6. **结果返回**：生成的音频结果会被返回给用户。

## 使用方法

该技能支持通过自然语言进行操作。系统会自动使用 **智能路由** 逻辑来选择最合适的模型；您也可以直接指定所需的模型。

**推荐使用方式：** **智能路由**  
（具体实现代码见 **```
# TTS
"Narrate this: Hello, world!"

# Music
"Compose a 30-second upbeat lo-fi hip hop track."

# SFX
"I need the sound of a thunderstorm."

# Voice Clone
"Clone the voice from this audio file and say: Welcome to the future."
```**）

**高级用法：** **直接选择模型**  
（具体实现代码见 **```json
{
  "action": "tts",
  "text": "This is a test.",
  "model": "minimax-tts-hd"
}
```**）

## 模型库（v2.0.0）

AudioMind v2.0 可智能地将请求路由到以下模型：

| 类型            | 模型 ID                    | 提供商     | 描述                                                                                          |
|----------------|-------------------------|-----------|--------------------------------------------------------------------------------------------|
| **TTS**          | `elevenlabs-tts-v3`         | ElevenLabs   | 表现力最强，支持多语言                          |
|                | `elevenlabs-tts-v2`         | ElevenLabs   | 稳定性高，支持 29 种语言                         |
|                | `elevenlabs-tts-turbo`      | ElevenLabs   | 极低延迟，支持 32 种语言                         |
|                | `minimax-tts-hd`            | fal.ai      | 高质量音效，支持多语言                          |
|                | `minimax-tts-2.6-hd`        | fal.ai      | MiniMax Speech-2.6 高清版本                         |
|                | `minimax-tts-2.8-hd`        | fal.ai      | 最新的 MiniMax TTS 版本                         |
|                | `minimax-tts-2.8-turbo`     | fal.ai      | 快速响应，低延迟版本                         |
|                | `chatterbox-tts`            | fal.ai      | 具有情感识别的 TTS 功能                         |
|                | `playai-dialog`             | fal.ai      | 支持多角色对话生成                         |
| **语音克隆**       | `dia-voice-clone`           | fal.ai      | 从音频样本中克隆声音                           |
| **音乐生成**       | `elevenlabs-music`          | ElevenLabs   | 基于作曲计划的音乐生成                         |
|                | `beatoven-music`            | fal.ai      | 免版税的器乐曲目，涵盖多种风格                   |
|                | `cassetteai-music`          | fal.ai      | 快速音乐生成工具                         |
| **音效生成**       | `elevenlabs-sfx`            | ElevenLabs   | 根据文本生成音效                           |
|                | `beatoven-sfx`              | fal.ai      | 专业级别的音效效果                         |
|                | `mirelo-video-to-audio`     | fal.ai      | 为视频生成同步音频                         |
|                | `mirelo-video-to-video`     | fal.ai      | 为视频添加音轨                         |

## 商业使用

该技能提供免费使用额度（100 次生成请求）。如需无限使用权限，请访问我们的 Gumroad 页面（达到免费使用限制后我们会提供链接）进行升级至 AudioMind Pro。

激活 Pro 版本后，请将 `AUDIOMIND_PRO_KEY` 环境变量设置为购买后收到的密钥。