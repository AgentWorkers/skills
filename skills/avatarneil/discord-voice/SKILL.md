---
name: discord-voice
description: 在 Discord 的语音频道中，使用 Claude AI 进行实时语音对话
metadata:
  clawdbot:
    config:
      requiredEnv:
        - DISCORD_TOKEN
        - OPENAI_API_KEY
      optionalEnv:
        - ELEVENLABS_API_KEY
        - DEEPGRAM_API_KEY
      systemDependencies:
        - ffmpeg
        - build-essential
      example: |
        {
          "plugins": {
            "entries": {
              "discord-voice": {
                "enabled": true,
                "config": {
                  "sttProvider": "whisper",
                  "ttsProvider": "openai",
                  "ttsVoice": "nova",
                  "vadSensitivity": "medium",
                  "streamingSTT": true,
                  "bargeIn": true,
                  "allowedUsers": []
                }
              }
            }
          }
        }
---

# Clawdbot的Discord语音插件

该插件支持在Discord语音频道中进行实时语音对话。用户可以加入语音频道，说话后，自己的语音会被Claude系统转录并处理，然后通过语音重新播放出来。

## 主要功能

- **加入/离开语音频道**：通过斜杠命令（slash commands）、命令行界面（CLI）或代理工具（agent tool）实现
- **语音活动检测（VAD）**：自动检测用户是否在说话
- **语音转文本（Speech-to-Text）**：使用OpenAI的Whisper API或Deepgram服务
- **流式语音转文本（Streaming STT）**：通过Deepgram的WebSocket接口实现实时转录（延迟约1秒）
- **集成到Clawdbot代理**：转录后的文本会通过Clawdbot代理进行处理
- **文本转语音（Text-to-Speech）**：使用OpenAI的TTS或ElevenLabs服务
- **音频播放**：处理后的文本会通过语音频道播放出来
- **插话支持**：当用户开始说话时，插件会立即停止播放
- **自动重连**：在连接断开时自动检测并尝试重新连接

## 所需条件

- 一个具有语音权限的Discord机器人（包括“Connect”、“Speak”和“Use Voice Activity”权限）
- STT（语音转文本）和TTS（文本转语音）服务所需的API密钥
- 系统依赖库：
  - `ffmpeg`（用于音频处理）
  - `@discordjs/opus`和`sodium-native`的本地构建工具

## 安装方法

### 1. 安装系统依赖库

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg build-essential python3

# Fedora/RHEL
sudo dnf install ffmpeg gcc-c++ make python3

# macOS
brew install ffmpeg
```

### 2. 通过ClawdHub安装

```bash
clawdhub install discord-voice
```

或手动安装：

```bash
cd ~/.clawdbot/extensions
git clone <repository-url> discord-voice
cd discord-voice
npm install
```

### 3. 在`clawdbot.json`中配置插件

```json5
{
  "plugins": {
    "entries": {
      "discord-voice": {
        "enabled": true,
        "config": {
          "sttProvider": "whisper",
          "ttsProvider": "openai",
          "ttsVoice": "nova",
          "vadSensitivity": "medium",
          "allowedUsers": [],  // Empty = allow all users
          "silenceThresholdMs": 1500,
          "maxRecordingMs": 30000,
          "openai": {
            "apiKey": "sk-..."  // Or use OPENAI_API_KEY env var
          }
        }
      }
    }
  }
}
```

### 4. 配置Discord机器人

确保您的Discord机器人具有以下权限：
- **Connect**：允许机器人加入语音频道
- **Speak**：允许机器人播放音频
- **Use Voice Activity**：允许机器人检测用户是否在说话

将这些权限添加到机器人的OAuth2 URL中，或在Discord开发者门户中进行配置。

## 配置参数

| 参数 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `enabled` | 布尔值 | `true` | 是否启用该插件 |
| `sttProvider` | 字符串 | `"whisper"` | 使用Whisper API |
| `streamingSTT` | 布尔值 | `true` | 启用流式语音转文本（仅支持Deepgram，延迟约1秒） |
| `ttsProvider` | 字符串 | `"openai"` | 使用OpenAI TTS |
| `ttsVoice` | 字符串 | `"nova"` | TTS服务的音频ID |
| `vadSensitivity` | 字符串 | `"medium"` | 语音检测的灵敏度（`low`、`medium`、`high`） |
| `bargeIn` | 布尔值 | `true` | 用户说话时立即停止播放 |
| `allowedUsers` | 字符串数组 | 允许加入的用户名单（空表示允许所有用户） |
| `silenceThresholdMs` | 数字 | `1500` | 检测静音的时长（毫秒） |
| `maxRecordingMs` | 数字 | 最大录音时长（毫秒） |
| `heartbeatIntervalMs` | 数字 | 连接健康检查间隔（毫秒） |
| `autoJoinChannel` | 字符串 | `undefined` | 启动时自动加入的频道ID |

## 服务提供商配置

#### OpenAI（Whisper + TTS）

```json5
{
  "openai": {
    "apiKey": "sk-...",
    "whisperModel": "whisper-1",
    "ttsModel": "tts-1"
  }
}
```

#### ElevenLabs（仅TTS）

```json5
{
  "elevenlabs": {
    "apiKey": "...",
    "voiceId": "21m00Tcm4TlvDq8ikWAM",  // Rachel
    "modelId": "eleven_multilingual_v2"
  }
}
```

#### Deepgram（仅STT）

```json5
{
  "deepgram": {
    "apiKey": "...",
    "model": "nova-2"
  }
}
```

## 使用方法

### 斜杠命令（Discord）

注册Discord机器人后，可以使用以下命令：
- `/voice join <channel>`：加入指定的语音频道
- `/voice leave`：离开当前语音频道
- `/voice status`：查看语音连接状态

### 命令行界面（CLI）命令

```bash
# Join a voice channel
clawdbot voice join <channelId>

# Leave voice
clawdbot voice leave --guild <guildId>

# Check status
clawdbot voice status
```

### 代理工具（Agent Tool）

代理工具可以使用`discord_voice`命令：
```
Join voice channel 1234567890
```

该工具支持以下操作：
- `join`：加入语音频道（需要提供频道ID）
- `leave`：离开语音频道
- `speak`：在语音频道中说话
- `status`：获取当前语音状态

## 工作原理

1. **加入频道**：机器人加入指定的语音频道。
2. **监听语音**：通过VAD检测用户是否开始/停止说话。
3. **录音**：用户说话时，音频会被缓冲。
4. **转录**：检测到静音时，音频会被发送到语音转文本服务。
5. **处理**：转录后的文本会被发送到Clawdbot代理。
6. **合成语音**：代理将文本转换为音频并通过TTS服务播放。
7. **播放**：处理后的音频会在语音频道中播放。

## 流式语音转文本（Deepgram）

当使用Deepgram作为语音转文本服务时，系统默认启用流式转录模式。该模式具有以下优势：
- **延迟约1秒**：端到端延迟更短。
- **实时反馈**：提供中间转录结果。
- **自动保持连接**：防止连接超时。
- **故障切换**：如果流式转录失败，系统会切换到批量转录模式。

### 插话支持

如果启用（默认设置），当用户开始说话时，机器人会立即停止播放，从而实现更自然的对话体验。

### 自动重连

插件具备自动连接监控功能：
- 每30秒进行一次连接健康检查。
- 连接断开时会自动尝试重新连接，最多尝试3次。
如果连接失败，系统会记录错误日志（参见```
[discord-voice] Disconnected from voice channel
[discord-voice] Reconnection attempt 1/3
[discord-voice] Reconnected successfully
```）。

## 语音检测灵敏度设置

- **low**：对轻微的声音也能检测到，但可能容易受到背景噪音干扰。
- **medium**：平衡性较好（推荐设置）。
- **high**：需要用户说话声音更大、更清晰。

## 常见问题及解决方法

- **“Discord客户端不可用”**：确保语音频道已配置且机器人已连接。
- **Opus/Sodium构建错误**：请安装相应的构建工具（参见```bash
npm install -g node-gyp
npm rebuild @discordjs/opus sodium-native
```）。
- **听不到音频**：
  1. 确保机器人具有播放音频的权限。
  2. 检查机器人是否被服务器静音。
  3. 验证TTS API密钥是否有效。
- **转录失败**：
  1. 确认TTS API密钥有效。
  2. 检查是否正在录制音频（查看日志）。
  3. 调整语音检测的灵敏度设置（参见```bash
DEBUG=discord-voice clawdbot gateway start
```）。

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `DISCORD_TOKEN` | Discord机器人令牌（必需） |
| `OPENAI_API_KEY` | OpenAI API密钥（用于Whisper和TTS） |
| `ELEVENLABS_API_KEY` | ElevenLabs API密钥 |
| `DEEPGRAM_API_KEY` | Deepgram API密钥 |

## 限制

- 每个公会最多只能使用一个语音频道。
- 最大录音时长为30秒（可配置）。
- 需要稳定的网络环境以支持实时音频传输。
- TTS输出可能存在轻微延迟。

## 许可证

本插件采用MIT许可证。