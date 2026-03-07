---
name: video-bgm
description: 分析视频的情绪，并为其添加由 AI 生成的背景音乐（BGM）。可选地，可以加快或减慢视频播放速度。该工具使用 Gemini 进行视频分析，同时利用 fal.ai Lyria2 生成音乐。当用户输入 “add bgm”（添加背景音乐）、”add music to video”（为视频添加音乐）或任何类似指令时，该功能会自动启动。
metadata: {"openclaw": {"emoji": "🎵", "os": ["darwin", "linux"]}}
---
# 视频背景音乐功能

该功能通过人工智能分析视频的内容和氛围，生成与之匹配的背景音乐，并将其混入视频中。

---

## 工作流程

```
Input Video → Gemini Analysis → Lyria2 BGM → FFmpeg Mix → Output
                (mood/style)     (generate)    (speed + volume + fade)
```

## 所需依赖项

- **Python**: `python3`（或激活项目中的虚拟环境）
- **Gemini API**: `GOOGLE_GENAI_API_KEY`（用于视频内容分析）
- **fal.ai**: `FAL_API_KEY`（用于音乐生成）
- **FFmpeg**: 需要系统自带的工具

## 设置

```bash
# Install required packages
pip install google-generativeai httpx

# Set API keys via environment variables
export GOOGLE_GENAI_API_KEY="your_google_api_key"
export FAL_API_KEY="your_fal_api_key"
```

## 使用方法

```
/video-bgm <path-to-video>
/video-bgm <path-to-video> --speed 1.1
/video-bgm <path-to-video> --speed 1.1 --volume 5
/video-bgm <path-to-video> --style "lo-fi chill"
```

## 参数说明

| 参数 | 默认值 | 说明 |
|-----|---------|-------------|
| `path` | （必填） | 输入视频文件的路径 |
| `--speed` | `1.0` | 速度倍率（例如：1.1 表示速度加快 10%） |
| `--volume` | `5.0` | 背景音乐的音量倍率（Lyria2 的输出音量较低） |
| `--fade-in` | `1.5` | 进场淡入时间（以秒为单位） |
| `--fade-out` | `3.0` | 出场淡出时间（以秒为单位） |
| `--style` | （自动） | 覆盖音乐风格（跳过 Gemini 的分析） |

## 详细步骤

### 第一步：使用 Gemini 分析视频

将视频上传到 Gemini 2.0 并获取详细的氛围分析结果。

```python
import google.generativeai as genai
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_GENAI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
```

使用以下提示进行分析（该提示具有针对性，而非通用提示）：

```
Watch this video very carefully. You are a music supervisor for commercials.

Tell me:
1. What BRAND POSITIONING does this video convey? (luxury? affordable? aspirational?)
2. What is the EMOTIONAL JOURNEY of the viewer? Be specific at each moment.
3. What REAL commercial music references would fit? Name specific ad styles
   (Four Seasons resort? Apple reveal? Volvo? Pottery Barn? Nike?)
4. What is the ENERGY LEVEL? Contemplative/still or forward momentum?
5. What tempo, instruments, and production style would ACTUALLY work?
   Be honest - classical piano is often too stuffy. Consider modern alternatives.

Then provide a SINGLE music generation prompt (2-3 sentences) that captures
the ideal BGM. Focus on: instruments, tempo BPM, mood adjectives, production style.
Format: MUSIC_PROMPT: <your prompt here>
```

### 第二步：提取音乐生成指令

从 Gemini 的响应中提取 `MUSIC_PROMPT:` 这一行，该内容将作为 Lyria2 的生成指令。

在 Lyria2 的生成指令中，务必添加以下限制条件：
```
No vocals, no drums, no percussion hits, no sound effects.
```

### 第三步：使用 fal.ai 和 Lyria2 生成背景音乐

```python
import httpx
import os

FAL_API_KEY = os.environ.get("FAL_API_KEY")

resp = httpx.post(
    "https://fal.run/fal-ai/lyria2",
    headers={
        "Authorization": f"Key {FAL_API_KEY}",
        "Content-Type": "application/json",
    },
    json={"prompt": music_prompt},
    timeout=120.0,
)
audio_url = resp.json()["audio"]["url"]
```

Lyria2 会生成约 32 秒的音频文件，输出格式为 WAV 格式（48kHz 立体声）。

### 第四步：使用 FFmpeg 调整音频速度并合并背景音乐

```bash
# Step 4a: Speed up video (if requested) and strip any existing audio
ffmpeg -y -i INPUT.mp4 \
  -filter:v "setpts=PTS/{speed}" \
  -an \
  -c:v libx264 -preset medium -crf 18 \
  OUTPUT_speedup.mp4

# Step 4b: Get sped-up duration
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 OUTPUT_speedup.mp4)

# Step 4c: Mix BGM with volume boost, fade in/out, trim to video length
ffmpeg -y \
  -i OUTPUT_speedup.mp4 \
  -i bgm.wav \
  -filter_complex "[1:a]volume={volume},atrim=0:{duration},afade=t=in:st=0:d={fade_in},afade=t=out:st={duration-fade_out}:d={fade_out}[a]" \
  -map 0:v -map "[a]" \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  OUTPUT_final.mp4
```

### 第五步：查看最终结果

打开处理后的视频供用户审阅，同时单独打开背景音乐文件以便用户单独评估音乐质量。

## 重要提示

- **Lyria2 的输出音量较低**——请务必使用音量倍率（默认值为 5.0） |
- **不要过度细化 Lyria2 的生成指令**——过于详细的指令可能导致混乱的结果。建议仅指定乐器、节奏、氛围和风格作为参考 |
- **让 Gemini 负责音乐风格的推荐**——它的推荐效果通常比通用的“轻松钢琴”等默认选项更好 |
- **处理前务必先去除视频中的现有音频**（使用 `-an` 参数）——某些视频中可能包含不需要的音频轨道 |
- **古典钢琴风格通常不合适**——对于奢华或现代简约风格的视频，使用现代乐器（如 Rhodes、吉他、大提琴）会更为合适 |

## 输出文件

所有处理后的文件都会保存在输入视频的同一目录下：
```
input_video.mp4          → original
input_video_speedup.mp4  → sped up, no audio
input_video_bgm.wav      → generated BGM
input_video_final.mp4    → final output with BGM
```

## 示例

```bash
# Basic: analyze and add BGM
/video-bgm ~/Desktop/product_video.mp4

# Speed up 10% and add BGM
/video-bgm ~/Desktop/product_video.mp4 --speed 1.1

# Override style (skip Gemini analysis)
/video-bgm ~/Desktop/ad.mp4 --style "upbeat modern pop, synth pads, 100 BPM"

# Adjust volume
/video-bgm ~/Desktop/quiet_video.mp4 --volume 8
```