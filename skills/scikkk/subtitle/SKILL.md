---
name: senseaudio-subtitle-generator
description: 从视频音频中生成具有精确时间戳的同步字幕（SRT/VTT/ASS格式）。适用于用户需要字幕、说明文字或带有时间标注的视频转录内容的情况。
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
      bins:
        - ffmpeg
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
    install:
      - kind: uv
        package: requests
      - kind: uv
        package: pydub
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---
# SenseAudio 字幕生成器

为视频生成准确、同步的字幕，支持正确的时间戳、格式以及多语言功能。

## 该技能的功能

- 从视频文件中提取音频
- 带有精确时间戳的音频转录
- 生成字幕文件（SRT、VTT、ASS）
- 支持多种语言和翻译
- 以正确的换行和时序格式化字幕

## 先决条件

安装所需的 Python 包：

```bash
pip install requests pydub
```

注意：您还需要安装 `ffmpeg` 以提取视频音频：
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

## 实现指南

### 第一步：从视频中提取音频

```python
from pydub import AudioSegment
import subprocess

def extract_audio_from_video(video_file, output_audio="temp_audio.wav"):
    # Use ffmpeg to extract audio
    cmd = [
        "ffmpeg", "-i", video_file,
        "-vn",  # No video
        "-acodec", "pcm_s16le",  # PCM format
        "-ar", "16000",  # 16kHz sample rate
        "-ac", "1",  # Mono
        output_audio
    ]
    subprocess.run(cmd, check=True)
    return output_audio
```

### 第二步：进行逐词级时间戳的转录

```python
import os
import requests

API_KEY = os.environ["SENSEAUDIO_API_KEY"]

def transcribe_for_subtitles(audio_file, language="zh"):
    url = "https://api.senseaudio.cn/v1/audio/transcriptions"

    headers = {"Authorization": f"Bearer {API_KEY}"}
    files = {"file": open(audio_file, "rb")}
    data = {
        "model": "sense-asr-pro",
        "language": language,
        "response_format": "verbose_json",
        "timestamp_granularities[]": ["word", "segment"],
        "enable_punctuation": "true"
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json()
```

### 第三步：生成字幕片段

```python
def create_subtitle_segments(transcript_data, max_chars_per_line=42, max_duration=7):
    words = transcript_data.get("words", [])
    segments = []

    current_segment = {
        "start": 0,
        "end": 0,
        "text": ""
    }

    for word in words:
        word_text = word["word"]
        word_start = word["start"]
        word_end = word["end"]

        # Check if adding this word exceeds limits
        potential_text = current_segment["text"] + " " + word_text if current_segment["text"] else word_text

        if (len(potential_text) > max_chars_per_line or
            (current_segment["start"] > 0 and word_end - current_segment["start"] > max_duration)):
            # Save current segment
            if current_segment["text"]:
                segments.append(current_segment.copy())

            # Start new segment
            current_segment = {
                "start": word_start,
                "end": word_end,
                "text": word_text
            }
        else:
            # Add word to current segment
            if not current_segment["text"]:
                current_segment["start"] = word_start
            current_segment["end"] = word_end
            current_segment["text"] = potential_text

    # Add last segment
    if current_segment["text"]:
        segments.append(current_segment)

    return segments
```

### 第四步：格式化为 SRT 格式

```python
def format_srt(segments):
    srt_content = ""

    for i, segment in enumerate(segments, 1):
        start_time = format_timestamp_srt(segment["start"])
        end_time = format_timestamp_srt(segment["end"])

        srt_content += f"{i}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{segment['text']}\n\n"

    return srt_content

def format_timestamp_srt(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
```

### 第五步：格式化为 VTT 格式

```python
def format_vtt(segments):
    vtt_content = "WEBVTT\n\n"

    for segment in segments:
        start_time = format_timestamp_vtt(segment["start"])
        end_time = format_timestamp_vtt(segment["end"])

        vtt_content += f"{start_time} --> {end_time}\n"
        vtt_content += f"{segment['text']}\n\n"

    return vtt_content

def format_timestamp_vtt(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
```

## 高级功能

### 多语言字幕

生成多种语言的字幕：

```python
def generate_multilingual_subtitles(video_file, languages=["zh", "en"]):
    audio_file = extract_audio_from_video(video_file)
    subtitles = {}

    for lang in languages:
        # Transcribe in original language
        transcript = transcribe_for_subtitles(audio_file, language=lang)

        # If translating, use target_language parameter
        if lang != languages[0]:
            transcript = transcribe_for_subtitles(
                audio_file,
                language=languages[0],
                target_language=lang
            )

        segments = create_subtitle_segments(transcript)
        subtitles[lang] = format_srt(segments)

    return subtitles
```

### 字幕样式（ASS 格式）

```python
def format_ass(segments, style="Default"):
    ass_header = """[Script Info]
Title: Generated Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    ass_content = ass_header

    for segment in segments:
        start = format_timestamp_ass(segment["start"])
        end = format_timestamp_ass(segment["end"])
        text = segment["text"]

        ass_content += f"Dialogue: 0,{start},{end},{style},,0,0,0,,{text}\n"

    return ass_content

def format_timestamp_ass(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:01d}:{minutes:02d}:{secs:05.2f}"
```

### 字幕优化

```python
def optimize_subtitles(segments):
    optimized = []

    for segment in segments:
        text = segment["text"]

        # Split long lines
        if len(text) > 42:
            words = text.split()
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            text = f"{line1}\n{line2}"

        # Ensure minimum display time (1 second)
        duration = segment["end"] - segment["start"]
        if duration < 1.0:
            segment["end"] = segment["start"] + 1.0

        segment["text"] = text
        optimized.append(segment)

    return optimized
```

### 将字幕嵌入视频

```python
def burn_subtitles(video_file, subtitle_file, output_file):
    cmd = [
        "ffmpeg", "-i", video_file,
        "-vf", f"subtitles={subtitle_file}",
        "-c:a", "copy",
        output_file
    ]
    subprocess.run(cmd, check=True)
```

## 输出格式

- SRT 字幕文件
- VTT 字幕文件（适用于网页）
- 带有样式的 ASS 字幕文件
- 包含时间戳数据的 JSON 文件
- 嵌入字幕的视频（可选）

## 优化建议

- 使用高质量音频以获得更好的转录效果
- 根据视频大小调整每行的最大字符数
- 审查并编辑时间戳以确保完美的同步
- 在最终确定之前使用视频播放器测试字幕
- 考虑字幕的阅读速度（建议每秒 15-20 个字符）

## 示例用法

**用户请求**：“为这个视频生成英文字幕”

**技能执行步骤**：
1. 从视频中提取音频
2. 进行逐词级时间戳的转录
3. 生成具有正确时间戳的字幕片段
4. 将字幕格式化为 SRT 文件
5. （可选）生成适用于网页的 VTT 文件
6. 提供可供下载的字幕文件

## 参考资料

API 文档：https://senseaudio.cn/docs/speech_recognition