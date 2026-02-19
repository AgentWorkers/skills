# ElevenLabs CLI

> **非官方 CLI**：这是一个由社区独立开发的 CLI 客户端，并非 ElevenLabs 官方发布。

这是一个用于 ElevenLabs AI 音频平台的全面命令行接口，实现了 100% 的 SDK 覆盖率。该 CLI 提供了 80 多种工具，涵盖了 ElevenLabs 的所有功能。

## 安装

```bash
# Homebrew (macOS/Linux)
brew install hongkongkiwi/tap/elevenlabs-cli

# Cargo
cargo install elevenlabs-cli --features mcp

# Scoop (Windows)
scoop bucket add elevenlabs-cli https://github.com/hongkongkiwi/scoop-elevenlabs-cli
scoop install elevenlabs-cli

# Docker
docker pull ghcr.io/hongkongkiwi/elevenlabs-cli:latest

# Snap (Linux)
sudo snap install elevenlabs-cli
```

## 使用场景

当用户需要执行以下操作时，可以使用此 CLI：
- 将文本转换为语音（文本转语音）
- 将语音转换为文本（语音转文本）
- 克隆语音或管理语音设置
- 根据文本描述生成音效
- 更改音频文件中的语音
- 去除背景噪音（音频隔离）
- 创建配音内容（视频/音频翻译）
- 管理 ElevenLabs 的资源（语音、代理、项目等）
- 为 ElevenLabs 设置 MCP 服务器以供 AI 助手使用

## 先决条件

- ElevenLabs API 密钥（通过 `ELEVENLABS_API_KEY` 环境变量或配置文件设置）
- 请从以下链接获取 API 密钥：https://elevenlabs.io/app/settings/api-keys

## 配置

```bash
# Set API key via environment variable
export ELEVENLABS_API_KEY="your-api-key"

# Or configure via CLI (stores in ~/.config/elevenlabs-cli/config.toml)
elevenlabs config set api_key your-api-key

# Set defaults
elevenlabs config set default_voice Brian
elevenlabs config set default_model eleven_multilingual_v2
```

## 常用命令

### 文本转语音

```bash
# Basic TTS
elevenlabs tts "Hello, world!"

# With options
elevenlabs tts "Hello" --voice Rachel --model eleven_v3 --output speech.mp3

# Stream to file
elevenlabs tts "Long text here" --output audio.mp3

# List available voices
elevenlabs voice list

# List models
elevenlabs model list
```

### 语音转文本

```bash
# Transcribe audio
elevenlabs stt audio.mp3

# With speaker diarization
elevenlabs stt audio.mp3 --diarize

# Output as SRT subtitles
elevenlabs stt audio.mp3 --format srt --output subtitles.srt
```

### 语音管理

```bash
# List voices
elevenlabs voice list

# Get voice details
elevenlabs voice get <voice-id>

# Clone a voice
elevenlabs voice clone --name "My Voice" --samples sample1.mp3,sample2.mp3

# Delete a voice
elevenlabs voice delete <voice-id>
```

### 音效生成

```bash
# Generate sound effect
elevenlabs sfx "door creaking slowly in a haunted house" --duration 5 --output sfx.mp3
```

### 噪音去除（音频隔离）

```bash
# Remove background noise
elevenlabs isolate noisy_audio.mp3 --output clean_audio.mp3
```

### 语音转换器

```bash
# Transform voice in audio file
elevenlabs voice-change input.mp3 --voice Rachel --output output.mp3
```

### 配音

```bash
# Create dubbing project
elevenlabs dubbing create video.mp4 --source-lang en --target-lang es

# Check status
elevenlabs dubbing status <dubbing-id>

# Download result
elevenlabs dubbing download <dubbing-id> --output dubbed.mp4
```

## MCP 服务器模式

该 CLI 可以作为 MCP 服务器运行，为 Claude、Cursor 等 AI 助手提供 ElevenLabs 的所有功能。

### 启动 MCP 服务器

```bash
# Run as stdio MCP server
elevenlabs mcp

# Enable only specific tools
elevenlabs mcp --enable-tools tts,stt,voice

# Disable specific tools
elevenlabs mcp --disable-tools agents,phone

# Disable administrative operations (safer for AI assistants)
elevenlabs mcp --disable-admin

# Disable only destructive operations (deletes)
elevenlabs mcp --disable-destructive

# Read-only mode
elevenlabs mcp --read-only
```

### 为 AI 客户端配置 MCP

将以下配置添加到您的 MCP 客户端中（例如 Claude Desktop、Cursor）：

```json
{
  "mcpServers": {
    "elevenlabs": {
      "command": "elevenlabs",
      "args": ["mcp"],
      "env": {
        "ELEVENLABS_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 可用的 MCP 工具（80 多种）

| 类别 | 工具 |
|----------|-------|
| **文本转语音/音频** | `text_to_speech`, `speech_to_text`, `generate_sfx`, `audio_isolation`, `voice_changer` |
| **语音** | `list_voices`, `get_voice`, `delete_voice`, `clone_voice`, `edit_voice_settings`, `create_voice_design` |
| **配音** | `create_dubbing`, `get_dubbing_status`, `delete_dubbing` |
| **历史记录** | `list_history`, `get_history_item`, `delete_history_item`, `download_history` |
| **代理** | `listAgents`, `create_agent`, `get_agent`, `update_agent`, `delete_agent` |
| **对话** | `converse_chat`, `list_conversations`, `get_conversation`, `delete_conversation` |
| **知识库/问答系统** | `list_knowledge`, `add_knowledge`, `delete_knowledge`, `create_rag`, `rebuild_rag` |
| **项目** | `list_projects`, `get_project`, `delete_project`, `convert_project` |
| **音乐** | `generate_music`, `list_music`, `get_music`, `download_music` |
| **电话** | `list_phones`, `import_phone`, `update_phone`, `delete_phone` |
| **Webhook** | `list_webhooks`, `create_webhook`, `delete_webhook` |
| **用户/使用情况** | `get_user_info`, `get_user_subscription`, `get_usage` |
| **模型** | `list_models`, `get_model_rates` |
| **发音** | `list_pronunciations`, `add_pronunciation`, `add_pronunciation_rules` |
| **工作空间** | `workspace_info`, `list_workspace_members`, `list_workspace_api_keys` |

## 输出格式

```bash
# JSON output
elevenlabs voice list --json

# Table output (default)
elevenlabs voice list

# Quiet mode (only essential output)
elevenlabs tts "Hello" -q
```

## 帮助文档

```bash
# General help
elevenlabs --help

# Command help
elevenlabs tts --help
elevenlabs voice --help
elevenlabs mcp --help
```

## 链接

- **GitHub**: https://github.com/hongkongkiwi/elevenlabs-cli
- **Crates.io**: https://crates.io/crates/elevenlabs-cli
- **问题反馈**: https://github.com/hongkongkiwi/elevenlabs-cli/issues
- **ElevenLabs API 文档**: https://elevenlabs.io/docs/api-reference

## 标签

elevenlabs, tts, text-to-speech, stt, speech-to-text, audio, voice, voice-cloning, voice-synthesis, mcp, ai, cli