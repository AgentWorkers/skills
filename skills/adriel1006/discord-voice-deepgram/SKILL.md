---
name: deepgram-discord-voice
description: 在 Discord 中，通过 Deepgram 的流式语音转文本（STT, Speech-to-Text）技术和低延迟的语音合成（TTS, Text-to-Speech）功能来实现语音通道的对话。
metadata:
  clawdbot:
    config:
      requiredEnv:
        - DISCORD_TOKEN
        - DEEPGRAM_API_KEY
      optionalEnv: []
      example: |
        {
          "plugins": {
            "entries": {
              "deepgram-discord-voice": {
                "enabled": true,
                "config": {
                  "streamingSTT": true,
                  "streamingTTS": true,
                  "ttsVoice": "aura-2-thalia-en",
                  "vadSensitivity": "medium",
                  "bargeIn": true,

                  "primaryUser": "atechy",
                  "allowVoiceSwitch": true,
                  "wakeWord": "openclaw",

                  "deepgram": {
                    "sttModel": "nova-2",
                    "language": "en-US"
                  }
                }
              }
            }
          }
        }
---

# Deepgram Discord语音插件（适用于OpenClaw/Clawdbot）

该插件允许您**仅通过Discord语音频道**与您的智能助手进行交流。

**通信流程（低延迟）：**
- Discord语音音频 → **Deepgram的实时语音转文本（STT）**（通过WebSocket传输）
- 转换后的文本 → 智能助手
- 智能助手的回复 → **Deepgram的文本转语音（TTS）**（通过HTTP以Ogg/Opus格式传输）
- 处理后的音频再次播放回Discord语音频道

## 所需条件：
- 一个Discord机器人令牌（`DISCORD_TOKEN`）
- 一个Deepgram API密钥（`DEEPGRAM_API_KEY`）
- 您的Discord机器人需要具备以下权限：
  - **连接（Connect）**
  - **发言（Speak）**
  - **使用语音功能（Use Voice Activity）**

## 安装方法：
### 方法A：通过ClawHub安装
1. 在OpenClaw/Clawdbot的控制面板中，进入**Skills/Plugins**（技能/插件）。
2. 添加并安装`deepgram-discord-voice`插件。
3. 设置所需的环境变量。

### 方法B：手动安装
1. 将该插件文件夹复制到您的`extensions/plugins`目录中。
2. 运行以下命令：
```bash
npm install
```

3. 重启OpenClaw/Clawdbot。

## 配置选项：
### 核心配置参数：
- `primaryUser`（推荐）：默认情况下，机器人会监听哪个用户的声音。
  - 最佳选择：您的**Discord用户ID**（数字格式）。
  - 如果在频道内唯一，也可以使用用户名或显示名称（例如`atechy`）。
- `allowVoiceSwitch`：如果设置为`true`，则主用户可以切换允许语音通信的对象。
- `wakeWord`：语音控制命令的前缀。默认值为`openclaw`。
- `deepgram.sttModel`：默认使用`nova-2`模型。
- `deepgram.language`：可选的BCP-47语言标签（例如`en-US`、`es`、`es-EC`）。
- `ttsVoice`：Deepgram的语音合成模型（例如`aura-2-thalia-en`）。

### 配置示例：
```json5
{
  "plugins": {
    "entries": {
      "deepgram-discord-voice": {
        "enabled": true,
        "config": {
          "streamingSTT": true,
          "streamingTTS": true,

          "primaryUser": "atechy",
          "allowVoiceSwitch": true,
          "wakeWord": "openclaw",

          "ttsVoice": "aura-2-thalia-en",
          "vadSensitivity": "medium",
          "bargeIn": true,

          "deepgram": {
            "sttModel": "nova-2",
            "language": "en-US"
          }
        }
      }
    }
  }
}
```

## 使用方法：
### 加入语音频道
- 使用插件工具或特定的Discord命令加入频道：
  - 加入：`action=join`，后跟频道ID。
- 离开：`action=leave`。

### 语音交流
- 机器人连接后，您可以直接通过语音与智能助手交流。

### 安全设置（默认）：
- 当设置了`primaryUser`后，插件只会监听该用户的声音，除非您允许其他用户使用语音功能。

### 允许其他用户使用语音功能：
- 作为主用户，您可以执行以下命令：
  - `openclaw allow <用户名>`：允许指定用户使用语音功能。
  - `openclaw listen to <用户名>`：切换监听对象为指定用户。

### 重新设置监听用户：
- `openclaw only me`：仅允许主用户使用语音功能。
- `openclaw reset`：重置所有设置。

### 通过工具进行语音控制：
- `allow_speaker`：允许指定用户使用语音功能（支持用户ID、@提及或用户名）。
- `only_me`：仅允许主用户使用语音功能。
- `status`：查看当前的语音监听状态。

## 注意事项：
- 通过`streamingSTT=true`和`streamingTTS=true`可实现最低延迟的通信效果。
- Deepgram的文本转语音功能通过HTTP以Ogg/Opus格式传输，因此Discord可以立即播放处理后的音频。