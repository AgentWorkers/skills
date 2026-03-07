---
name: audio-handler
description: Read, analyze, convert, and process audio files (MP3, WAV, FLAC, AAC, M4A, OGG, OPUS, WMA). Use when working with audio: extracting metadata, converting formats, trimming, merging, adjusting volume, or transcribing. Triggers on mentions of audio files, file paths with audio extensions, or requests to process/convert audio.
---

# 音频处理工具

用于分析、转换和处理音频文件。

## 支持的音频格式

| 格式 | 扩展名 | 读取 | 转换 | 元数据 |
|--------|------------|------|---------|----------|
| MP3 | .mp3 | ✅ | ✅ | ✅ |
| WAV | .wav | ✅ | ✅ | ✅ |
| FLAC | .flac | ✅ | ✅ | ✅ |
| AAC/M4A | .m4a, .aac | ✅ | ✅ | ✅ |
| OGG | .ogg | ✅ | ✅ | ✅ |
| Opus | .opus | ✅ | ✅ | ✅ |
| WMA | .wma | ✅ | ✅ | ✅ |
| AIFF | .aiff, .aif | ✅ | ✅ | ✅ |

## 快速命令

### 获取音频元数据（使用 ffprobe）

```bash
# Get all metadata
ffprobe -v quiet -print_format json -show_format -show_streams audio.mp3

# Get duration only
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 audio.mp3

# Get bitrate
ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 audio.mp3

# Get sample rate and channels
ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate,channels -of default=noprint_wrappers=1 audio.mp3

# Human-readable info
ffprobe -hide_banner audio.mp3
```

### 转换音频格式（使用 ffmpeg）

```bash
# Convert to MP3 (good quality)
ffmpeg -i input.wav -codec:a libmp3lame -qscale:a 2 output.mp3

# Convert to MP3 (specific bitrate)
ffmpeg -i input.wav -codec:a libmp3lame -b:a 192k output.mp3

# Convert to WAV (uncompressed)
ffmpeg -i input.mp3 output.wav

# Convert to FLAC (lossless)
ffmpeg -i input.wav output.flac

# Convert to M4A/AAC
ffmpeg -i input.wav -codec:a aac -b:a 256k output.m4a

# Convert to OGG Vorbis
ffmpeg -i input.wav -codec:a libvorbis -qscale:a 5 output.ogg

# Convert to Opus (best for speech)
ffmpeg -i input.wav -codec:a libopus -b:a 64k output.opus
```

### 剪裁音频文件

```bash
# Trim audio (from 30s to 90s)
ffmpeg -i input.mp3 -ss 30 -to 90 -c copy output.mp3

# Trim from start to duration
ffmpeg -i input.mp3 -t 60 -c copy output.mp3  # First 60 seconds

# Trim with re-encode (more accurate)
ffmpeg -i input.mp3 -ss 30 -to 90 output.mp3
```

### 调整音量和播放速度

```bash
# Adjust volume (2x louder)
ffmpeg -i input.mp3 -af "volume=2" output.mp3

# Reduce volume (half)
ffmpeg -i input.mp3 -af "volume=0.5" output.mp3

# Normalize audio
ffmpeg -i input.mp3 -af "loudnorm" output.mp3

# Speed up (1.5x)
ffmpeg -i input.mp3 -af "atempo=1.5" output.mp3

# Slow down (0.75x)
ffmpeg -i input.mp3 -af "atempo=0.75" output.mp3
```

### 合并音频文件

```bash
# Concatenate audio files
ffmpeg -i "concat:part1.mp3|part2.mp3|part3.mp3" -acodec copy output.mp3

# Merge with file list
echo "file 'part1.mp3'" > list.txt
echo "file 'part2.mp3'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp3

# Mix two audio tracks
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex amix=inputs=2:duration=longest output.mp3
```

### 从视频中提取音频

```bash
# Extract audio track
ffmpeg -i video.mp4 -vn -acodec copy audio.aac

# Extract and convert
ffmpeg -i video.mp4 -vn -acodec libmp3lame -b:a 192k audio.mp3
```

### 在 macOS 上播放音频

```bash
# Play audio file
afplay audio.mp3

# Play with volume (0.0 to 1.0)
afplay -v 0.5 audio.mp3

# Play in background
afplay audio.mp3 &

# Stop playback
killall afplay
```

### 将文本转换为语音（在 macOS 上）

```bash
# Speak text
say "Hello, this is a test"

# Save to file
say -o output.aiff "This will be saved as audio"

# List voices
say -v ?

# Use specific voice
say -v "Samantha" "Hello, I am Samantha"

# Convert to MP3
say -o temp.aiff "Text to convert" && ffmpeg -i temp.aiff output.mp3 && rm temp.aiff
```

## 脚本

### audio_info.sh

用于获取音频的详细元数据。

```bash
~/Dropbox/jarvis/skills/audio-handler/scripts/audio_info.sh <audio_file>
```

### convert_audio.sh

用于在多种音频格式之间进行转换，并支持质量设置。

```bash
~/Dropbox/jarvis/skills/audio-handler/scripts/convert_audio.sh <input> <output> [quality]
```

### trim_audio.sh

用于根据指定的开始/结束时间裁剪音频文件。

```bash
~/Dropbox/jarvis/skills/audio-handler/scripts/trim_audio.sh <input> <output> <start> <end>
```

### normalize_audio.sh

用于统一音频文件的音量水平。

```bash
~/Dropbox/jarvis/skills/audio-handler/scripts/normalize_audio.sh <input> <output>
```

## 质量优化建议

| 使用场景 | 最佳格式 | 相关设置 |
|----------|--------|----------|
| 音乐存档 | FLAC | `-codec:a flac` |
| 便携式音乐播放 | MP3 | `-codec:a libmp3lame -qscale:a 2` |
| 播客/语音内容 | Opus | `-codec:a libopus -b:a 64k` |
| 语音备忘录 | M4A | `-codec:a aac -b:a 128k` |
| 未压缩音频 | WAV | `-codec:a pcm_s16le` |

## 注意事项：

- `ffmpeg` 支持几乎所有的音频格式。
- 使用 `-c copy` 模式可以快速转换音频文件，但可能无法精确地裁剪音频片段。
- 如果需要精确裁剪音频片段，建议使用重新编码（`-af`）模式，但转换时间会较长。
- Opus 格式在低比特率下非常适合用于语音传输。
- 可以使用 `loudnorm` 滤镜来确保所有音频文件的音量一致。