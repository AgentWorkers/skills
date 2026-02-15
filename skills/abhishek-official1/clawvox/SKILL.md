---
name: clawvox
description: **ClawVox – ElevenLabs 为 OpenClaw 开发的语音工作室**  
ClawVox 提供了丰富的功能，包括生成语音、转录音频、克隆声音、创建音效等。它是 ElevenLabs 专为 OpenClaw 平台开发的一款专业语音处理工具。
homepage: https://elevenlabs.io/developers
metadata:
  {
    "openclaw": {
      "emoji": "🎙️",
      "skillKey": "clawvox",
      "requires": {
        "bins": ["curl", "jq"],
        "env": ["ELEVENLABS_API_KEY"]
      },
      "primaryEnv": "ELEVENLABS_API_KEY"
    }
  }
---

# ClawVox

使用由 ElevenLabs 提供支持的 ClawVox，将您的 OpenClaw 助手转变为一个专业的语音制作工具。

## 快速参考

| 功能 | 命令 | 说明 |
|--------|---------|-------------|
| 朗读文本 | `{baseDir}/scripts/speak.sh '文本'` | 将文本转换为语音 |
| 语音转文本 | `{baseDir}/scripts/transcribe.sh audio.mp3` | 将语音转换为文本 |
| 克隆语音 | `{baseDir}/scripts/clone.sh --name "语音名称" sample.mp3` | 克隆语音 |
| 生成音效 | `{baseDir}/scripts/sfx.sh "雷暴"` | 生成音效 |
| 查看可用语音 | `{baseDir}/scripts/voices.sh list` | 查看可用的语音 |
| 配音 | `{baseDir}/scripts/dub.sh --target es audio.mp3` | 为音频添加配音 |
| 去除背景噪音 | `{baseDir}/scripts/isolate.sh audio.mp3` | 去除音频背景噪音 |

## 设置

1. 从 [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys) 获取您的 API 密钥。
2. 在 `~/.openclaw/openclaw.json` 中进行配置：

```json5
{
  skills: {
    entries: {
      "clawvox": {
        apiKey: "YOUR_ELEVENLABS_API_KEY",
        config: {
          defaultVoice: "Rachel",
          defaultModel: "eleven_turbo_v2_5",
          outputDir: "~/.openclaw/audio"
        }
      }
    }
  }
}
```

或者通过设置环境变量来配置：

```bash
export ELEVENLABS_API_KEY="your_api_key_here"
```

## 语音生成（TTS）

### 基本文本转语音
```bash
# Quick speak with default voice (Rachel)
{baseDir}/scripts/speak.sh 'Hello, I am your personal AI assistant.'

# Specify voice by name
{baseDir}/scripts/speak.sh --voice Adam 'Hello from Adam'

# Save to file
{baseDir}/scripts/speak.sh --out ~/audio/greeting.mp3 'Welcome to the show'

# Use specific model
{baseDir}/scripts/speak.sh --model eleven_multilingual_v2 'Bonjour'

# Adjust voice settings
{baseDir}/scripts/speak.sh --stability 0.5 --similarity 0.8 'Expressive speech'

# Adjust speed
{baseDir}/scripts/speak.sh --speed 1.2 'Faster speech'

# Use multilingual model for other languages
{baseDir}/scripts/speak.sh --model eleven_multilingual_v2 --voice Rachel 'Hola, que tal'
{baseDir}/scripts/speak.sh --model eleven_multilingual_v2 --voice Adam 'Guten Tag'
```

### 语音模型

| 模型 | 延迟时间 | 支持的语言 | 适用场景 |
|-------|---------|-----------|----------|
| `eleven_flash_v2_5` | 约 75 毫秒 | 32 种语言 | 实时流式播放 |
| `eleven_turbo_v2_5` | 约 250 毫秒 | 32 种语言 | 平衡音质和速度 |
| `eleven_multilingual_v2` | 约 500 毫秒 | 29 种语言 | 适合长篇内容，最高音质 |

### 可用语音

预设语音：Rachel、Adam、Antoni、Bella、Domi、Elli、Josh、Sam、Callum、Charlie、George、Liam、Matilda、Alice、Bill、Brian、Chris、Daniel、Eric、Jessica、Laura、Lily、River、Roger、Sarah、Will

### 长篇内容处理
```bash
# Generate audio from text file
{baseDir}/scripts/speak.sh --input chapter.txt --voice "George" --out audiobook.mp3
```

## 语音转文本（转录）

### 基本转录功能
```bash
# Transcribe audio file
{baseDir}/scripts/transcribe.sh recording.mp3

# Save to file
{baseDir}/scripts/transcribe.sh --out transcript.txt audio.mp3

# Transcribe with language hint
{baseDir}/scripts/transcribe.sh --language es spanish_audio.mp3

# Include timestamps
{baseDir}/scripts/transcribe.sh --timestamps podcast.mp3
```

### 支持的文件格式
- MP3、MP4、MPEG、MPGA、M4A、WAV、WebM
- 文件大小上限：100MB

## 语音克隆

### 即时语音克隆
```bash
# Clone from single sample (minimum 30 seconds recommended)
{baseDir}/scripts/clone.sh --name MyVoice recording.mp3

# Clone with description
{baseDir}/scripts/clone.sh --name BusinessVoice \
  --description 'Professional male voice' \
  sample.mp3

# Clone with labels
{baseDir}/scripts/clone.sh --name MyVoice \
  --labels '{"gender":"male","age":"adult"}' \
  sample.mp3

# Remove background noise during cloning
{baseDir}/scripts/clone.sh --name CleanVoice \
  --remove-bg-noise \
  sample.mp3

# Test cloned voice
{baseDir}/scripts/speak.sh --voice MyVoice 'Testing my cloned voice'
```

## 语音库管理
```bash
# List all available voices
{baseDir}/scripts/voices.sh list

# Get voice details
{baseDir}/scripts/voices.sh info --name Rachel
{baseDir}/scripts/voices.sh info --id 21m00Tcm4TlvDq8ikWAM

# Search voices (filter output with grep)
{baseDir}/scripts/voices.sh list | grep -i "female"

# Filter by category
{baseDir}/scripts/voices.sh list --category premade
{baseDir}/scripts/voices.sh list --category cloned

# Download voice preview
{baseDir}/scripts/voices.sh preview --name Rachel -o preview.mp3

# Delete custom voice
{baseDir}/scripts/voices.sh delete --id "voice_id"
```

## 音效制作
```bash
# Generate sound effect
{baseDir}/scripts/sfx.sh 'Heavy rain on a tin roof'

# With duration
{baseDir}/scripts/sfx.sh --duration 5 'Forest ambiance with birds'

# With prompt influence (higher = more accurate)
{baseDir}/scripts/sfx.sh --influence 0.8 'Sci-fi laser gun firing'

# Save to file
{baseDir}/scripts/sfx.sh --out effects/thunder.mp3 'Rolling thunder'
```

**注意：** 语音片段时长范围为 0.5 至 22 秒（四舍五入到最接近的 0.5 秒）

## 去除背景噪音

```bash
# Remove background noise and isolate voice
{baseDir}/scripts/isolate.sh noisy_recording.mp3

# Save to specific file
{baseDir}/scripts/isolate.sh --out clean_voice.mp3 meeting_recording.mp3

# Don't tag audio events
{baseDir}/scripts/isolate.sh --no-audio-events recording.mp3
```

**要求：**
- 语音片段时长至少为 4.6 秒
- 支持的文件格式：MP3、WAV、M4A、OGG、FLAC

## 配音（多语言翻译）

```bash
# Dub audio to Spanish
{baseDir}/scripts/dub.sh --target es audio.mp3

# Dub with source language specified
{baseDir}/scripts/dub.sh --source en --target ja video.mp4

# Check dubbing status
{baseDir}/scripts/dub.sh --status --id "dubbing_id"

# Download dubbed audio
{baseDir}/scripts/dub.sh --download --id "dubbing_id" --out dubbed.mp3
```

**支持的语言：** en、es、fr、de、it、pt、pl、hi、ar、zh、ja、ko、nl、ru、tr、vi、sv、da、fi、cs、el、he、id、ms、no、ro、uk、hu、th

## API 使用示例

所有脚本内部都使用 curl 进行 API 请求：

```bash
# Direct TTS API call
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "model_id": "eleven_turbo_v2_5"}' \
  --output speech.mp3
```

## 错误处理

所有脚本都会提供有用的错误信息：
- **401**: 认证失败 - 请检查您的 API 密钥。
- **403**: 权限被拒绝 - 您的 API 密钥可能没有相应的权限。
- **429**: 超过使用频率限制 - 请稍后再试。
- **500/502/503**: ElevenLabs API 出现问题 - 请稍后再试。

## 测试

运行测试套件以验证所有功能是否正常：

```bash
{baseDir}/test.sh YOUR_API_KEY
```

或者通过设置环境变量来执行测试：

```bash
export ELEVENLABS_API_KEY="your_key"
{baseDir}/test.sh
```

## 故障排除

### 常见问题

1. **“exec host not allowed (requested gateway)”**
   - 该功能需要在沙箱环境中运行命令。
   - 配置 OpenClaw 以使用沙箱模式：`tools.exec.host: "sandbox"`
   - 或者在 OpenClaw 配置中启用沙箱模式。
   - 或者为 gateway 主机配置执行权限（请参阅 OpenClaw 文档）。

2. **包含引号或感叹号的文本导致解析错误**
   - 使用单引号而不是双引号：`'Hello world'` 而不是 `"Hello world!"`
   - 在使用双引号时避免在文本中使用感叹号（`!`）。
   - 对于复杂的文本，使用 `--input` 选项并指定文件路径。

3. **“ELEVENLABS_API_KEY 未设置”**
   - 确保 `ELEVENLABS_API_KEY` 已设置并在 `openclaw.json` 中配置。
   - 检查 API 密钥长度是否至少为 20 个字符。

4. **需要jq 但未安装**
   - 安装 jq：`apt-get install jq`（Linux）或 `brew install jq`（macOS）。

5. **超出使用频率限制**
   - 请在 elevenlabs.io/app/usage 查看您的使用计划配额。
   - 免费套餐：每月约 10,000 个字符。

6. **找不到所需语音**
   - 使用 `{baseDir}/scripts/voices.sh list` 查看可用的语音。
   - 确认语音 ID 是否正确。

7. **配音失败**
   - 确保源音频清晰可听。
   - 检查支持的语言代码是否正确。

8. **文件过大**
   - 转录文件大小上限：100MB。
   - 配音文件大小上限：500MB。
   - 语音克隆文件大小上限：每个文件 50MB。

### 调试模式
```bash
# Enable verbose output
DEBUG=1 {baseDir}/scripts/speak.sh 'test'

# Show API request details
DEBUG=1 {baseDir}/scripts/transcribe.sh audio.mp3
```

## 价格说明

ElevenLabs API 的价格大致如下：
- **Flash v2.5**：约 0.06 美元/分钟
- **Turbo v2.5**：约 0.06 美元/分钟
- **Multilingual v2**：约 0.12 美元/分钟
- **语音克隆**：包含在套餐内。
- **音效生成**：约 0.02 美元/次
- **文本转语音（Scribe v1）**：约 0.02 美元/分钟

免费套餐：每月约 10,000 个字符。

## 链接

- [ElevenLabs 控制台](https://elevenlabs.io/app)
- [API 文档](https://elevenlabs.io/docs)
- [语音库](https://elevenlabs.io/voice-library)
- [价格信息](https://elevenlabs.io/pricing)