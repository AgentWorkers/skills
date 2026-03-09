---
name: willow-inference-server
description: 本地自动语音识别（ASR）和文本转语音（TTS）推理服务器。当用户需要将音频转换为文本（ASR）或将文本转换为语音（TTS）时可以使用该服务。该服务依赖于正在运行的Willow推理服务器实例。支持使用Whisper进行自动语音识别，并提供自定义的TTS语音选项。
metadata: {}
---
# Willow 推理服务器技能

本地自动语音识别（ASR，语音转文本）和文本转语音（TTS）推理服务器。

## 设置

### 1. 启动 Willow 推理服务器
```bash
git clone https://github.com/toverainc/willow-inference-server.git
cd willow-inference-server
./utils.sh install
./utils.sh gen-cert your-hostname
./utils.sh run
```

服务器运行地址：`https://your-hostname:19000`

### 2. 配置环境
设置服务器 URL：
```bash
export WILLOW_BASE_URL="https://your-hostname:19000"
```

或者按请求进行配置（详见下文）。

## ASR（语音转文本）

### 转录音频文件
```bash
curl -X POST "${WILLOW_BASE_URL}/asr" \
  -F "audio_file=@/path/to/audio.m4a" \
  -F "language=auto"
```

### 参数
| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| audio_file | 需要转录的音频文件 | 必填 |
| language | 语言代码（en, zh 等）或 "auto" | 自动选择 |
| model | Whisper 模型（tiny, base, medium, large-v2） | 由服务器配置决定 |
| task | 转录或翻译 | 转录 |

### 支持的格式
- MP3, WAV, M4A, OGG, FLAC, WebM

### 示例：使用 curl 进行转录
```bash
# Basic transcription
curl -X POST "${WILLOW_BASE_URL}/asr" \
  -F "audio_file=@recording.m4a" \
  -F "language=zh"

# With specific model
curl -X POST "${WILLOW_BASE_URL}/asr" \
  -F "audio_file=@meeting.mp3" \
  -F "language=en" \
  -F "model=base"
```

## TTS（文本转语音）

### 将文本转换为语音
```bash
curl -X POST "${WILLOW_BASE_URL}/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "voice": "af_sarah"}'
```

### 参数
| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| text | 需要转换为语音的文本 | 必填 |
| voice | 语音ID（详见下文） | 默认语音 |
| speed | 语音速度（0.5-2.0） | 1.0 |
| volume | 音量（0.0-1.0） | 1.0 |

### 可用的语音
常见语音（格式：`gender_voicename`）：
- `af_sarah` - Sarah（女性）
- `af_bella` - Bella（女性）
- `am_michael` - Michael（男性）
- `am_alex` - Alex（男性）

完整语音列表请查看服务器文档： `${WILLOW_BASE_URL}/api/docs`

### 示例：使用 curl 进行文本转语音
```bash
# Basic TTS
curl -X POST "${WILLOW_BASE_URL}/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，这是测试"}' \
  -o output.wav

# With custom voice
curl -X POST "${WILLOW_BASE_URL}/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello!", "voice": "am_michael", "speed": 1.2}' \
  -o hello.mp3
```

## 环境变量

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| WILLOW_BASE_URL | 服务器 URL | https://localhost:19000 |

## 工作流程示例

### 1. 录音并转录
```bash
# Record audio (macOS)
rec test.wav

# Transcribe
curl -X POST "${WILLOW_BASE_URL}/asr" \
  -F "audio_file=@test.wav" \
  -F "language=auto"
```

### 2. 文本转语音
```bash
# Convert text to speech
curl -X POST "${WILLOW_BASE_URL}/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "今天的任务是学习新技能"}' \
  -o speech.wav
```

### 批量转录
```bash
for f in *.m4a; do
  curl -X POST "${WILLOW_BASE_URL}/asr" \
    -F "audio_file=@$f" \
    -F "language=auto" \
    -o "${f%.m4a}.txt"
done
```

## API 文档
完整的 API 文档请访问： `${WILLOW_BASE_URL}/api/docs`

## 注意事项
- 所有接口均支持 HTTPS（如配置为 HTTP 也可使用）
- 音频文件在服务器端进行本地处理
- ASR 的处理延迟取决于所选模型和硬件配置
- TTS 的语音效果可通过自定义语音录音来调整