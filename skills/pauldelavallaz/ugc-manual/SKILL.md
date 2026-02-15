---
name: ugc-manual
description: |
  Generate lip-sync video from image + user's own audio recording.
  
  ✅ USE WHEN:
  - User provides their OWN audio file (voice recording)
  - Want to sync image to specific audio/voice
  - User recorded the script themselves
  - Need exact audio timing preserved
  
  ❌ DON'T USE WHEN:
  - User provides text script (not audio) → use veed-ugc
  - Need AI to generate the voice → use veed-ugc
  - Don't have audio file yet → use veed-ugc with script
  
  INPUT: Image + audio file (user's recording)
  OUTPUT: MP4 video with lip-sync to provided audio
  
  KEY DIFFERENCE: veed-ugc = script → AI voice → video
                  ugc-manual = user audio → video (no voice generation)
---

# UGC-Manual

使用 ComfyDeploy 的 UGC-Manual 工作流程，可以通过将图片与自定义音频文件结合来生成对口型视频。

## 概述

UGC-Manual 需要：
1. 一张包含清晰面部特征的图片（人物或角色）
2. 一个音频文件（用户录制的语音）

最终生成的视频中，图片中的人物会随着音频进行对口型表演。

## API 详情

**端点：** `https://api.comfydeploy.com/api/run/deployment/queue`
**部署 ID：** `075ce7d3-81a6-4e3e-ab0e-7a25edf601b5`

## 必需输入参数

| 输入参数 | 描述 | 格式 |
|---------|------------------|---------|
| `image` | 包含清晰面部特征的图片 | JPG、PNG |
| `input_audio` | 用于对口型的音频文件 | MP3、WAV、OGG |

## 使用方法

```bash
uv run ~/.clawdbot/skills/ugc-manual/scripts/generate.py \
  --image "path/to/image.jpg" \
  --audio "path/to/audio.mp3" \
  --output "output-video.mp4"
```

### 使用 URL 的示例：

```bash
uv run ~/.clawdbot/skills/ugc-manual/scripts/generate.py \
  --image "https://example.com/image.jpg" \
  --audio "https://example.com/audio.mp3" \
  --output "result.mp4"
```

## 工作流程集成

### 典型使用场景

1. **自定义语音录制**：用户通过 Telegram/WhatsApp 录制自己的语音。
2. **预生成的 TTS**：从外部服务（如 ElevenLabs）生成的音频。
3. **音乐/声音同步**：将人物的口型动作与任何音频同步。

### 示例工作流程：

```bash
# 1. Convert Telegram voice message to MP3 (if needed)
ffmpeg -i voice.ogg -acodec libmp3lame -q:a 2 voice.mp3

# 2. Generate lip-sync video
uv run ugc-manual... --image face.jpg --audio voice.mp3 --output video.mp4
```

## 与 VEED-UGC 的区别

| 特性 | UGC-Manual | VEED-UGC |
|---------|------------|----------|
| 音频来源 | 用户提供 | 由系统自动生成 |
| 脚本 | 无 | 自动生成 |
| 语音 | 用户录制的语音 | ElevenLabs 提供的 TTS 服务 |
| 使用场景 | 需要自定义音频 | 适用于自动化内容生成 |

## 注意事项

- 图片中的面部必须清晰可见（正面或 3/4 视角）。
- 音频质量会影响最终视频的质量。
- 处理时间：根据音频长度大约为 2-5 分钟。
- **音频自动转换**：系统会自动将所有音频格式（MP3、OGG、M4A 等）转换为 WAV PCM 16 位单声道 48kHz 格式，然后再发送到 FabricLipsync。
- 系统需要安装 `ffmpeg` 工具。