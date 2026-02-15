---
name: avatar
description: 具有 Simli 视频渲染功能及 ElevenLabs TTS 技术的交互式 AI 阿凡达
emoji: "\U0001F9D1\u200D\U0001F4BB"
homepage: https://github.com/Johannes-Berggren/openclaw-avatar
metadata:
  clawdis:
    skillKey: avatar
    os: [macos, linux, windows]
    requires:
      bins: [node, npm]
      env: [SIMLI_API_KEY, ELEVENLABS_API_KEY]
    install:
      - npm install -g openclaw-avatar
    config:
      requiredEnv:
        - SIMLI_API_KEY
        - ELEVENLABS_API_KEY
      example: |
        SIMLI_API_KEY=your-simli-api-key
        ELEVENLABS_API_KEY=your-elevenlabs-api-key
    cliHelp: |
      openclaw-avatar - Interactive AI avatar frontend

      Usage: openclaw-avatar [options]

      Starts the avatar server at http://localhost:5173
      Requires SIMLI_API_KEY and ELEVENLABS_API_KEY environment variables.
---

# 虚拟形象技能

OpenClaw 的交互式 AI 虚拟形象功能，支持实时唇形同步视频和文本转语音功能。

## 特点

- **语音响应**：使用 ElevenLabs 的文本转语音（TTS）技术，提供简洁、自然的对话式回答。
- **视觉虚拟形象**：通过 Simli 技术生成逼真的唇形同步视频。
- **详细信息面板**：在语音回答旁边显示格式化的 Markdown 内容。
- **多语言支持**：支持多种语言的语音和文本转语音功能。
- **Slack/邮件**：可配置将回答内容转发至 Slack 私信或电子邮件。
- **Stream Deck**：可选的硬件控制设备，支持 Elgato Stream Deck。

## 设置步骤

1. 获取 API 密钥：
   - [Simli](https://simli.com) - 虚拟形象渲染服务
   - [ElevenLabs](https://elevenlabs.io) - 文本转语音服务

2. 设置环境变量：
   ```bash
   export SIMLI_API_KEY=your-key
   export ELEVENLABS_API_KEY=your-key
   ```

3. 启动虚拟形象服务：
   ```bash
   openclaw-avatar
   ```

4. 打开浏览器，访问 http://localhost:5173

## 回答格式

在回答虚拟形象的查询时，请使用以下格式：

```
<spoken>
A short conversational summary (1-3 sentences). NO markdown, NO formatting. Plain speech only.
</spoken>
<detail>
Full detailed response with markdown formatting (bullet points, headers, bold, etc).
</detail>
```

### 编写指南

1. **语音部分**：回答应简洁、自然，符合对话风格（这部分内容会被朗读出来）。
2. **详细信息部分**：提供包含格式化 Markdown 内容的详细解答。
3. 必须同时包含以上两个部分。

## 示例

用户：“我今天有哪些会议？”

```
<spoken>
You have three meetings today. Your first one is a team standup at 9 AM, then a product review at 2 PM, and finally a 1-on-1 with Sarah at 4 PM.
</spoken>
<detail>
## Today's Meetings

### 9:00 AM - Team Standup
- **Duration**: 15 minutes
- **Attendees**: Engineering team

### 2:00 PM - Product Review
- **Duration**: 1 hour
- **Attendees**: Product, Design, Engineering leads

### 4:00 PM - 1:1 with Sarah
- **Duration**: 30 minutes
- **Notes**: Follow up on project timeline
</detail>
```

## 会话密钥

虚拟形象的回答会使用以下会话密钥进行识别：`agent:main:avatar`