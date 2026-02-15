---
name: eachlabs-voice-audio
description: 使用EachLabs AI模型实现文本转语音（Text-to-Speech, TTS）、语音转文本（Speech-to-Text, STT）、语音转换（Voice Conversion, VC）以及音频处理功能。支持 ElevenLabs 的 TTS 服务，以及带有时间戳记录的 Whisper 转录功能（Whisper transcription with diarization）。当用户需要文本转语音、语音转文本或语音转换服务时，可以使用该工具。
metadata:
  author: eachlabs
  version: "1.0"
---

# EachLabs 语音与音频服务

通过 EachLabs 的 Predictions API，提供文本转语音（TTS）、语音转文本（STT）、语音转换以及音频处理功能。

## 认证

```
Header: X-API-Key: <your-api-key>
```

请设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取该密钥。

## 可用模型

### 文本转语音（Text-to-Speech）

| 模型            | Slug           | 适用场景                |
|-----------------|-----------------|----------------------|
| ElevenLabs TTS       | `elevenlabs-text-to-speech` | 高质量的文本转语音服务       |
| ElevenLabs TTS with Timestamps | `elevenlabs-text-to-speech-with-timestamp` | 带时间戳的文本转语音服务       |
| ElevenLabs Text to Dialogue | `elevenlabs-text-to-dialogue` | 多语音角色的对话生成服务       |
| ElevenLabs Sound Effects | `elevenlabs-sound-effects` | 音效生成服务             |
| ElevenLabs Voice Design v2    | `elevenlabs-voice-design-v2` | 个性化语音设计服务         |
| Kling V1 TTS       | `kling-v1-tts`         | Kling 提供的文本转语音服务       |
| Kokoro 82M         | `kokoro-82m`         | 轻量级的文本转语音服务         |
| Play AI Dialog      | `play-ai-text-to-speech-dialog` | 用于对话场景的文本转语音服务     |
| Stable Audio 2.5       | `stable-audio-2-5-text-to-audio` | 文本转音频服务           |

### 语音转文本（Speech-to-Text）

| 模型            | Slug           | 适用场景                |
|-----------------|-----------------|----------------------|
| ElevenLabs Scribe v2     | `elevenlabs-speech-to-text-scribe-v2` | 高质量的语音转文本服务         |
| ElevenLabs STT        | `elevenlabs-speech-to-text` | 标准的语音转文本服务         |
| Wizper with Timestamp    | `wizper-with-timestamp` | 带时间戳的语音转文本服务         |
| Wizper           | `wizper`           | 基础的语音转文本服务         |
| Whisper          | `whisper`           | 开源的语音转文本服务         |
| Whisper Diarization | `whisper-diarization` | 语音识别及转录服务         |
| Incredibly Fast Whisper | `incredibly-fast-whisper` | 高速的语音转文本服务         |

### 语音转换与克隆（Voice Conversion & Cloning）

| 模型            | Slug           | 适用场景                |
|-----------------|-----------------|----------------------|
| RVC v2           | `rvc-v2`           | 语音转换服务             |
| Train RVC         | `train-rvc`         | 自定义语音模型的训练服务         |
| ElevenLabs Voice Clone    | `elevenlabs-voice-clone` | 语音克隆服务             |
| ElevenLabs Voice Changer | `elevenlabs-voice-changer` | 语音变换服务             |
| ElevenLabs Voice Design v3    | `elevenlabs-voice-design-v3` | 高级语音设计服务           |
| ElevenLabs Dubbing     | `elevenlabs-dubbing`     | 视频配音服务             |
| Chatterbox S2S       | `chatterbox-speech-to-speech` | 语音对语音的转换服务         |
| Open Voice        | `openvoice`         | 开源的语音克隆服务         |
| XTTS v2           | `xtts-v2`           | 多语言语音克隆服务           |
| Stable Audio 2.5 Inpaint   | `stable-audio-2-5-inpaint` | 音频修复服务             |
| Stable Audio 2.5 A2A     | `stable-audio-2-5-audio-to-audio` | 音频转换服务             |
| Audio Trimmer       | `audio-trimmer-with-fade` | 带淡入效果的音频剪辑服务         |

### 音频处理工具（Audio Utilities）

| 模型            | Slug           | 适用场景                |
|-----------------|-----------------|----------------------|
| FFmpeg Merge Audio Video | `ffmpeg-api-merge-audio-video` | 音频与视频的合并服务         |
| Toolkit Video Convert | `toolkit`         | 视频/音频转换工具包           |

## 预测流程

1. **检查模型**：`GET https://api.eachlabs.ai/v1/model?slug=<slug>` — 确认模型存在，并获取包含完整输入参数的 `request_schema`。在创建预测请求前务必执行此操作，以确保输入正确。
2. **发送请求**：`POST https://api.eachlabs.ai/v1/prediction`，传入模型 slug、版本 `"0.0.1"` 以及符合 schema 的输入数据。
3. **查询结果**：`GET https://api.eachlabs.ai/v1/prediction/{id}`，直到状态变为 `"success"` 或 `"failed"`。
4. **提取输出**：从响应中提取预测结果。

## 示例

### 使用 ElevenLabs 进行文本转语音

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "elevenlabs-text-to-speech",
    "version": "0.0.1",
    "input": {
      "text": "Welcome to our product demo. Today we will walk through the key features.",
      "voice_id": "EXAVITQu4vr4xnSDxMaL",
      "model_id": "eleven_v3",
      "stability": 0.5,
      "similarity_boost": 0.7
    }
  }'
```

### 使用 ElevenLabs Scribe 进行语音转文本

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "elevenlabs-speech-to-text-scribe-v2",
    "version": "0.0.1",
    "input": {
      "media_url": "https://example.com/recording.mp3",
      "diarize": true,
      "timestamps_granularity": "word"
    }
  }'
```

### 使用 Wizper（Whisper）进行语音转文本

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "wizper-with-timestamp",
    "version": "0.0.1",
    "input": {
      "audio_url": "https://example.com/audio.mp3",
      "language": "en",
      "task": "transcribe",
      "chunk_level": "segment"
    }
  }'
```

### 使用 Whisper 进行语音识别（Speaker Diarization）

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "whisper-diarization",
    "version": "0.0.1",
    "input": {
      "file_url": "https://example.com/meeting.mp3",
      "num_speakers": 3,
      "language": "en",
      "group_segments": true
    }
  }'
```

### 使用 RVC v2 进行语音转换

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "rvc-v2",
    "version": "0.0.1",
    "input": {
      "input_audio": "https://example.com/vocals.wav",
      "rvc_model": "CUSTOM",
      "custom_rvc_model_download_url": "https://example.com/my-voice-model.zip",
      "pitch_change": 0,
      "output_format": "wav"
    }
  }'
```

### 将音频与视频合并

```bash
curl -X POST https://api.eachlabs.ai/v1/prediction \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "model": "ffmpeg-api-merge-audio-video",
    "version": "0.0.1",
    "input": {
      "video_url": "https://example.com/video.mp4",
      "audio_url": "https://example.com/narration.mp3",
      "start_offset": 0
    }
  }'
```

## ElevenLabs 语音 ID

`elevenlabs-text-to-speech` 模型支持以下语音 ID。请传递相应的原始 ID 字符串：

| 语音 ID          | 说明                        |
|-----------------|---------------------------|
| `EXAVITQu4vr4xnSDxMaL`   | 默认语音                         |
| `9BWtsMINqrJLrRacOk9x`   |                           |
| `CwhRBWXzGAHq8TQ4Fs17`   |                           |
| `FGY2WhTYpPnrIDTdsKH5`   |                           |
| `JBFqnCBsd6RMkjVDRZzb`   |                           |
| `N2lVS1w4EtoT3dr4eOWO`   |                           |
| `TX3LPaxmHKxFdv7VOQHJ`   |                           |
| `XB0fDUnXU5powFXDhCwa`   |                           |
| `onwK4e9ZLuTAKqWW03F9`   |                           |
| `pFZP5JQG7iQjIQuC4Bku`   |                           |

## 参数参考

有关每个模型的详细参数信息，请参阅 [references/MODELS.md](references/MODELS.md)。