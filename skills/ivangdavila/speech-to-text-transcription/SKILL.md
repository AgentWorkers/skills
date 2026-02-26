---
name: Speech to Text Transcription
slug: speech-to-text-transcription
version: 1.0.0
homepage: https://clawic.com/skills/speech-to-text-transcription
description: 将音频和视频文件转录为文本，并支持说话人检测、时间戳添加以及格式转换功能。
metadata: {"clawdbot":{"emoji":"🎤","requires":{"bins":["ffmpeg"]},"os":["linux","darwin","win32"]}}
changelog: Initial release with multi-provider support and batch processing.
---
## 设置

首次使用时，请阅读 `setup.md` 文件，然后开始协助进行转录工作。

## 使用场景

当用户拥有需要转录的音频或视频文件时，该工具可发挥作用。该工具支持处理本地文件、URL、语音备忘录、播客、会议记录和讲座内容。

## 架构

转录相关的数据存储在 `~/speech-to-text-transcription/` 目录下。具体数据结构请参考 `memory-template.md` 文件。

```
~/speech-to-text-transcription/
├── memory.md        # Provider preferences, defaults
├── transcripts/     # Saved transcriptions
└── temp/            # Processing workspace
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 数据模板 | `memory-template.md` |

## 核心规则

### 1. 首先识别文件类型
在开始转录之前，需要确定输入文件的类型：
- **本地文件**：验证文件是否存在并检查文件格式；
- **URL**：将文件下载到临时目录后再进行处理；
- **会议录音**：通常需要识别发言者的声音；
- **语音备忘录**：通常只包含单一发言者的内容，文件长度较短。

### 2. 根据场景选择合适的转录服务
| 场景 | 最适合的服务 | 选择理由 |
|----------|---------------|-----|
| 快速的本地转录 | **Whisper (本地)** | 不需要 API 密钥，免费且私密 |
| 高精度转录 | **OpenAI Whisper API** | 转录质量最高 |
| 识别发言者声音 | **AssemblyAI** | 支持发言者声音的自动识别 |
| 实时/流式转录 | **Deepgram** | 延迟时间较短 |
| 长时间内容（超过 2 小时） | **分块处理** | 避免超时问题 |

### 3. 处理大文件
对于文件大小超过 25MB 或时长超过 2 小时的音频文件：
1. 使用 `ffmpeg` 将文件分割成多个部分；
2. 分别处理每个部分；
3. 将处理后的转录结果按照时间戳合并；
4. **切勿尝试一次性上传大文件**。

### 4. 保留上下文信息
转录完成后：
- 询问用户是否需要保存转录结果；
- 根据内容为文件命名；
- 可以帮助用户提取关键信息或生成摘要。

### 5. 输出格式
默认输出格式为纯文本。同时提供其他格式选项：
- `.txt`：纯文本格式，不含时间戳；
- `.srt` / `.vtt`：带时间戳的字幕文件；
- `.json`：包含单词级时间戳的结构化文本；
- `.md`：包含发言者标签的格式化文本。

## 常见问题

- **错误假设**：认为所有场景都适用同一转录服务（例如，Whisper 不支持发言者声音的识别）；
- **直接上传大文件**：可能导致超时或内存错误（建议先分割文件）；
- **忽视音频质量**：嘈杂的音频需要预处理（使用 `ffmpeg` 进行降噪）；
- **未检查语言设置**：虽然 Whisper 会自动识别语言，但在混合语言内容中可能会出错；
- **丢失发言者信息**：多发言者的音频文件若未进行发言者识别，则无法正确转录。

## 所需软件/工具

**必备**：`ffmpeg`（用于音频处理）。

**可选的 API 密钥（仅在使用云服务时）：**
- `OPENAI_API_KEY`：用于 OpenAI Whisper API；
- `ASSEMBLYAI_API_KEY`：用于 AssemblyAI（发言者声音识别）；
- `DEEPGRAM_API_KEY`：用于 Deepgram（实时转录）；
- 本地使用的 Whisper 不需要 API 密钥。

## 各转录服务的快速参考

### 本地 Whisper（无需 API 密钥）
```bash
# Install
pip install openai-whisper

# Basic transcription
whisper audio.mp3 --model base --output_format txt

# With timestamps
whisper audio.mp3 --model medium --output_format srt
```

模型选项：`tiny`（快速）→ `base` → `small` → `medium` → `large`（精度逐渐提高）

### OpenAI Whisper API
```bash
curl -X POST https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -F file="@audio.mp3" \
  -F model="whisper-1"
```

### AssemblyAI（发言者声音识别）
```bash
# Upload
curl -X POST https://api.assemblyai.com/v2/upload \
  -H "Authorization: $ASSEMBLYAI_API_KEY" \
  --data-binary @audio.mp3

# Transcribe with speakers
curl -X POST https://api.assemblyai.com/v2/transcript \
  -H "Authorization: $ASSEMBLYAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "URL", "speaker_labels": true}'
```

## 音频预处理

### 从视频中提取音频
```bash
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

### 降噪处理
```bash
ffmpeg -i noisy.wav -af "afftdn=nf=-25" clean.wav
```

### 分割长音频文件
```bash
# Split into 10-minute chunks
ffmpeg -i long.mp3 -f segment -segment_time 600 -c copy chunk_%03d.mp3
```

## 安全性与隐私

- **数据存储**：
  - 转录结果存储在 `~/speech-to-text-transcription/transcripts/` 目录下；
  - 本地使用的 Whisper 完全在设备上处理数据。

- **数据传输**：
  - 如果使用云服务，音频文件会被发送到指定的提供商（OpenAI、AssemblyAI、Deepgram）；
  - 转录结果会返回并保存在本地。

**注意事项**：
- **不会以明文形式存储 API 密钥**（使用环境变量进行管理）；
- **不会在未经用户确认的情况下自动上传文件**；
- **处理完成后不会将文件保存在外部服务器上**。

## 外部接口

| 接口地址 | 发送的数据 | 用途 |
|----------|-----------|---------|
| api.openai.com/v1/audio | 音频文件 | 使用 OpenAI Whisper API 进行转录 |
| api.assemblyai.com/v2 | 音频文件 | 使用 AssemblyAI 进行转录 |
| api.deepgram.com/v1 | 音频流 | 使用 Deepgram 进行转录 |

这些接口仅在用户明确选择云服务时才会被调用。本地使用的 Whisper 不会发送任何数据。

## 安全性考虑

使用云服务进行转录时，音频数据会传输到 OpenAI、AssemblyAI 或 Deepgram。只有在确信这些服务能够妥善处理您的音频数据时，才建议使用它们。对于敏感内容，建议优先使用本地的 Whisper 工具。

## 相关技能

如果用户需要，可以使用以下工具进行额外处理：
- `clawhub install <slug>`：安装相关工具（例如 `audio` 用于通用音频处理，`ffmpeg` 用于音频和视频转换，`podcast` 用于播客的创建和编辑）。

## 反馈建议

- 如果该工具对您有帮助，请点赞：`clawhub star speech-to-text-transcription`；
- 为了获取最新信息，请执行 `clawhub sync` 命令。