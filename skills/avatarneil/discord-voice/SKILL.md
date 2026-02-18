---
name: discord-voice
description: 在 Discord 的语音频道中，使用 Claude AI 进行实时语音对话
metadata:
  clawdbot:
    config:
      requiredConfig:
        - discord.token
      optionalEnv:
        - OPENAI_API_KEY
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
                  "sttProvider": "local-whisper",
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

该插件支持在Discord语音频道中进行实时语音对话。用户可以加入语音频道、发言，系统会自动将语音内容转录并经过处理后通过语音播放出来。

## 主要功能

- **加入/离开语音频道**：通过斜杠命令、命令行界面（CLI）或代理工具实现
- **语音活动检测（VAD）**：自动识别用户是否在说话
- **语音转文本（STT）**：支持OpenAI的Whisper API、Deepgram或本地语音转文本服务（离线模式）
- **流式语音转文本**：使用Deepgram的WebSocket接口实现实时转录（延迟约1秒）
- **集成到Clawdbot代理**：转录后的文本会通过Clawdbot代理进行处理
- **文本转语音（TTS）**：支持OpenAI、ElevenLabs或Kokoro的文本转语音服务（本地/离线模式）
- **音频播放**：将处理后的语音内容回放到频道中
- **插话功能**：用户开始说话时，插件会立即停止播放
- **自动重连**：在连接断开时自动检测并尝试重新连接

## 必备条件

- 一个具有语音权限的Discord机器人（包括“连接”、“发言”和“检测语音活动”权限）
- 需要语音转文本（STT）和文本转语音（TTS）服务的API密钥
- 系统依赖库：
  - `ffmpeg`（用于音频处理）
  - `@discordjs/opus`和`sodium-native`的编译工具

## 安装步骤

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

### 3. 在`clawdbot.json`文件中进行配置

```json5
{
  plugins: {
    entries: {
      "discord-voice": {
        enabled: true,
        config: {
          sttProvider: "local-whisper",
          ttsProvider: "openai",
          ttsVoice: "nova",
          vadSensitivity: "medium",
          allowedUsers: [], // Empty = allow all users
          silenceThresholdMs: 1500,
          maxRecordingMs: 30000,
          openai: {
            apiKey: "sk-...", // Or use OPENAI_API_KEY env var
          },
        },
      },
    },
  },
}
```

### 4. 配置Discord机器人

确保你的Discord机器人具有以下权限：
- **连接**：允许机器人加入语音频道
- **发言**：允许机器人播放音频
- **检测语音活动**：允许机器人检测用户是否在说话

将这些权限添加到机器人的OAuth2 URL中，或在Discord开发者门户中进行配置。

## 配置选项

| 选项                | 类型     | 默认值           | 说明                                         |
| --------------------- | -------- | ----------------- | ----------------------------------------------- |
| `enabled`             | 布尔值  | `true`            | 是否启用该插件                       |
| `sttProvider`         | 字符串   | `"local-whisper"` | `"whisper"`、"`deepgram"`或"`local-whisper"` |
| `streamingSTT`        | 布尔值  | `true`            | 是否使用流式语音转文本（仅限Deepgram，延迟约1秒）   |
| `ttsProvider`         | 字符串   | `"openai"`        | `"openai"`或"`elevenlabs"`                    |
| `ttsVoice`            | 字符串   | `"nova"`          | 用于文本转语音的服务ID                                |
| `vadSensitivity`      | 字符串   | `"medium"`        | `"low"`、"`medium"`或"`high"`                |
| `bargeIn`             | 布尔值  | `true`            | 用户开始说话时停止播放                   |
| `allowedUsers`        | 字符串数组 | `[]`              | 允许加入的用户名单（空表示允许所有用户）                  |
| `silenceThresholdMs`  | 数值   | `1500`            | 处理前的静默时间（毫秒）                  |
| `maxRecordingMs`      | 数值   | `30000`           | 最大录音时长（毫秒）                       |
| `heartbeatIntervalMs` | 数值   | `30000`           | 连接健康检查间隔                        |
| `autoJoinChannel`     | 字符串   | `undefined`       | 启动时自动加入的频道ID              |

### 服务提供商配置

#### OpenAI（Whisper + TTS）

```json5
{
  openai: {
    apiKey: "sk-...",
    whisperModel: "whisper-1",
    ttsModel: "tts-1",
  },
}
```

#### ElevenLabs（仅TTS）

```json5
{
  elevenlabs: {
    apiKey: "...",
    voiceId: "21m00Tcm4TlvDq8ikWAM", // Rachel
    modelId: "eleven_multilingual_v2",
  },
}
```

#### Deepgram（仅STT）

```json5
{
  deepgram: {
    apiKey: "...",
    model: "nova-2",
  },
}
```

## 使用方法

### 斜杠命令（Discord）

注册Discord机器人后，可以使用以下命令：
- `/discord_voice join <频道>` - 加入指定的语音频道
- `/discord_voice leave` - 离开当前语音频道
- `/discord_voice status` - 查看语音连接状态

### 命令行界面（CLI）命令

```bash
# Join a voice channel
clawdbot discord_voice join <channelId>

# Leave voice
clawdbot discord_voice leave --guild <guildId>

# Check status
clawdbot discord_voice status
```

### 代理工具

代理工具可以执行以下操作：
- `join` - 加入语音频道
- `leave` - 离开语音频道
- `speak` - 在语音频道中发言
- `status` - 获取当前语音状态

## 工作原理

1. **加入频道**：机器人自动加入指定的语音频道。
2. **监听语音**：通过VAD技术检测用户是否在说话。
3. **录音**：用户说话时，系统会缓冲音频。
4. **转录**：用户停止说话后，音频会被发送到语音转文本服务。
5. **处理**：转录后的文本会被发送给Clawdbot代理。
6. **合成语音**：代理会将文本转换为音频并通过TTS服务播放出来。
7. **回放**：最终的语音内容会在频道中播放。

## 流式语音转文本（Deepgram）

当使用Deepgram作为语音转文本服务时，系统会默认启用流式转录模式。该模式具有以下优势：
- **延迟缩短约1秒**
- **实时反馈**：提供转录过程中的中间结果
- **自动保持连接**：防止连接超时
- **故障时切换到批量转录**

要启用流式转文本功能，请按照说明操作。

## 插话功能

如果启用该功能（默认开启），机器人会在用户开始说话时立即停止播放。这样可以让对话更加自然。

## 自动重连

插件具有自动连接监控功能：
- 每30秒进行一次连接状态检查
- 连接断开时会尝试自动重连，最多尝试3次。
如果连接失败，系统会记录错误日志。

## 配置参数说明

- **VAD灵敏度**：
  - `low`：能检测到微弱的语音，但可能容易受到背景噪音干扰
  - `medium`：平衡性较好（推荐设置）
  - `high`：需要更清晰、较大的语音才能被检测到

## 常见问题解决方法

- **“Discord客户端不可用”**：确保语音频道已配置且机器人已连接。
- **编译错误**：安装`ffmpeg`及`@discordjs/opus`、`sodium-native`的编译工具。
- **听不到音频**：
  - 确认机器人具有必要的权限。
  - 检查机器人是否被服务器静音。
- **转录失败**：
  - 确认TTS API密钥有效。
- **调试日志**：启用调试日志可帮助排查问题。

## 环境变量

| 变量                | 说明                          |
| -------------------- | ------------------------------ |
| `DISCORD_TOKEN`      | Discord机器人令牌（必需）           |
| `OPENAI_API_KEY`     | OpenAI API密钥（用于Whisper和TTS）     |
| `ELEVENLABS_API_KEY` | ElevenLabs API密钥             |
| `DEEPGRAM_API_KEY`   | Deepgram API密钥                   |

## 限制

- 每个公会最多只能使用一个语音频道。
- 最大录音时长为30秒（可配置）。
- 需要稳定的网络环境以支持实时音频传输。
- TTS输出可能存在轻微延迟。

## 许可证

本插件遵循MIT许可证。