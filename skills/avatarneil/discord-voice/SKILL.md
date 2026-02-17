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
# Clawdbot 的 Discord 语音插件

该插件支持在 Discord 的语音频道中进行实时语音对话。您可以通过加入语音频道、说话，让您的发言被 Claude 处理后重新播放出来。

## 主要功能

- **加入/离开语音频道**：通过斜杠命令、命令行界面（CLI）或代理工具实现
- **语音活动检测（VAD）**：自动检测用户是否在说话
- **语音转文本（STT）**：支持使用 OpenAI 的 Whisper API、Deepgram 或本地语音转文本服务（离线模式）
- **流式语音转文本（Streaming STT）**：通过 Deepgram 的 WebSocket 功能实现实时转录（延迟约 1 秒）
- **集成到 Clawdbot 代理**：转录后的文本会通过 Clawdbot 代理进行处理
- **文本转语音（TTS）**：支持使用 OpenAI、ElevenLabs 或 Kokoro 的文本转语音服务（本地/离线模式）
- **音频播放**：处理后的语音会回放到语音频道中
- **插话支持**：当用户开始说话时，插件会立即停止播放
- **自动重连**：在连接断开时自动检测并尝试重新连接

## 所需条件

- 拥有语音权限的 Discord 机器人（包括 “Connect”、“Speak” 和 “Use Voice Activity” 权限）
- 需要 STT 和 TTS 服务提供商的 API 密钥
- 系统依赖库：
  - `ffmpeg`（用于音频处理）
  - `@discordjs/opus` 和 `sodium-native` 的构建工具

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

### 2. 通过 ClawdHub 安装

```bash
clawdhub install discord-voice
```

或者手动安装：

```bash
cd ~/.clawdbot/extensions
git clone <repository-url> discord-voice
cd discord-voice
npm install
```

### 3. 在 `clawdbot.json` 中配置插件

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

### 4. 配置 Discord 机器人

确保您的 Discord 机器人具有以下权限：
- **Connect**：允许加入语音频道
- **Speak**：允许播放音频
- **Use Voice Activity**：允许检测用户是否在说话

将这些权限添加到机器人的 OAuth2 URL 中，或在 Discord 开发者门户中进行配置。

## 配置参数

| 参数                | 类型       | 默认值         | 说明                                      |
| --------------------- | ---------- | -------------- | ------------------------------------------------------ |
| `enabled`             | boolean    | `true`         | 是否启用该插件                               |
| `sttProvider`         | string     | `"local-whisper"`    | 可选值：`"whisper"`、`"deepgram"` 或 `"local-whisper"`           |
| `streamingSTT`        | boolean    | `true`         | 是否使用流式语音转文本（仅限 Deepgram，延迟约 1 秒）                |
| `ttsProvider`         | string     | `"openai"`       | 可选值：`"openai"` 或 `"elevenlabs"`                     |
| `ttsVoice`            | string     | `"nova"`        | 用于文本转语音的音频 ID                           |
| `vadSensitivity`      | string     | `"medium"`       | 可选值：`"low"`、`"medium"` 或 `"high"`                    |
| `bargeIn`             | boolean    | `true`         | 用户开始说话时立即停止播放                         |
| `allowedUsers`        | string[]     | 可选值：允许访问的用户名列表（空表示允许所有用户）             |
| `silenceThresholdMs`      | number     | `1500`        | 静默后开始处理的延迟时间（毫秒）                         |
| `maxRecordingMs`      | number     | `30000`       | 最大录音时长（毫秒）                             |
| `heartbeatIntervalMs`     | number     | `30000`       | 连接状态检查间隔时间（毫秒）                         |
| `autoJoinChannel`     | string     | `undefined`     | 启动时自动加入的频道 ID                           |

### 服务提供商配置

#### OpenAI（结合 Whisper 和 TTS）

```json5
{
  openai: {
    apiKey: "sk-...",
    whisperModel: "whisper-1",
    ttsModel: "tts-1",
  },
}
```

#### ElevenLabs（仅支持 TTS）

```json5
{
  elevenlabs: {
    apiKey: "...",
    voiceId: "21m00Tcm4TlvDq8ikWAM", // Rachel
    modelId: "eleven_multilingual_v2",
  },
}
```

#### Deepgram（仅支持 STT）

```json5
{
  deepgram: {
    apiKey: "...",
    model: "nova-2",
  },
}
```

## 使用方法

### Discord 斜杠命令

注册 Discord 账号后，可以使用以下命令：
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

### 代理工具

您可以使用 `discord_voice` 工具来管理插件：
- `join`：加入语音频道（需要提供频道 ID）
- `leave`：离开语音频道
- `speak`：在语音频道中说话
- `status`：获取当前的语音状态

## 工作原理

1. **加入频道**：机器人自动加入指定的语音频道。
2. **监听语音**：通过 VAD 检测用户是否开始/停止说话。
3. **录音**：在用户说话期间，音频会被缓冲。
4. **转录**：当用户停止说话后，音频会被发送到语音转文本服务。
5. **处理结果**：转录后的文本会被发送给 Clawdbot 代理。
6. **合成语音**：代理会将文本转换为音频并通过 TTS 服务播放出来。
7. **回放**：处理后的音频会在语音频道中播放。

### 流式语音转文本（Deepgram）

当使用 Deepgram 作为语音转文本服务时，系统会默认启用流式转录模式。该模式具有以下优势：
- **延迟约 1 秒**：端到端延迟更短
- **实时反馈**：提供中间转录结果
- **自动保持连接**：防止连接超时
- **故障切换**：如果流式转录失败，系统会切换到批量转录模式

### 插话支持

如果启用该功能（默认开启），当用户开始说话时，机器人会立即停止播放。这有助于实现更自然的对话体验。

### 自动重连

插件具备自动连接监控功能：
- 每 30 秒进行一次连接状态检查。
- 连接断开后，系统会尝试自动重连，最多尝试 3 次。
如果重连失败，系统会记录相关日志（参见 **代码块 11**）。

## 配置选项说明

- **VAD 敏感性**：
  - `low`：能捕捉到微弱的声音，但可能容易受到背景噪音干扰。
  - `medium`：平衡性较好（推荐设置）。
  - `high`：需要用户声音更响亮、更清晰。

## 常见问题解决方法

- **“Discord 客户端不可用”**：确保语音功能已启用，并检查机器人是否已连接到 Discord 频道。
- **构建错误**：请安装 `ffmpeg` 及 `@discordjs/opus`、`sodium-native` 的构建工具。
- **听不到音频**：
  - 确认机器人具有播放音频的权限。
  - 检查机器人是否被服务器静音。
  - 验证 TTS API 密钥是否有效。
- **转录失败**：
  - 确认 TTS API 密钥有效。
  - 检查是否正在录音（查看调试日志）。
- **启用调试日志**：通过设置环境变量 `DISCORD_TOKEN`、`OPENAI_API_KEY`、`ELEVENLABS_API_KEY` 和 `DEEPGRAM_API_KEY` 来启用调试日志。

## 环境变量

| 变量                | 说明                                      |
| ----------------------------- | ------------------------------------------------------ |
| `DISCORD_TOKEN`      | Discord 机器人令牌（必需）                         |
| `OPENAI_API_KEY`     | OpenAI API 密钥（用于 Whisper 和 TTS 服务）                 |
| `ELEVENLABS_API_KEY`     | ElevenLabs API 密钥                             |
| `DEEPGRAM_API_KEY`   | Deepgram API 密钥                                   |

## 限制事项

- 每个公会最多只能使用一个语音频道。
- 最大录音时长为 30 秒（可配置）。
- 实时音频传输需要稳定的网络环境。
- TTS 服务的输出可能存在轻微延迟。

## 许可证

本插件采用 MIT 许可协议。