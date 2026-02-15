---
name: video-ad-analyzer
version: 1.0.0
description: 使用 Gemini Vision AI 从视频广告中提取并分析内容。该工具支持帧提取、OCR 文本检测、音频转录以及基于 AI 的场景分析功能。适用于分析视频创意内容、提取文本信息或生成逐场景的描述。
---

# 视频广告分析工具

该工具利用 Google Gemini Vision 技术实现基于人工智能的视频内容提取功能。

## 该工具的功能

- **帧提取**：通过场景变化检测进行智能采样
- **OCR 文本检测**：使用 EasyOCR 工具提取视频中的文字信息
- **音频转录**：利用 Google Cloud Speech 将音频转换为文本
- **AI 场景分析**：利用 Gemini Vision 对每个场景进行描述
- **原生视频分析**：支持对较大视频文件进行直接分析
- **缩略图生成**：从视频的第一帧自动生成缩略图

## 设置

### 1. 环境变量

```bash
# Required for Gemini Vision
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Required for audio transcription
# (same service account needs Speech-to-Text API enabled)
```

### 2. 依赖项

```bash
pip install opencv-python pillow easyocr ffmpeg-python google-cloud-speech vertexai google-api-python-client
```

系统上还需要安装 `ffmpeg` 和 `ffprobe`。

## 使用方法

### 基本视频分析

```python
from scripts.video_extractor import VideoExtractor
from scripts.models import ExtractedVideoContent
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize Vertex AI
vertexai.init(project="your-project-id", location="us-central1")
gemini_model = GenerativeModel("gemini-1.5-flash")

# Create extractor
extractor = VideoExtractor(gemini_model=gemini_model)

# Analyze video
result = extractor.extract_content("/path/to/video.mp4")

print(f"Duration: {result.duration}s")
print(f"Scenes: {len(result.scene_timeline)}")
print(f"Text overlays: {len(result.text_timeline)}")
print(f"Transcript: {result.transcript[:200]}...")
```

### 仅提取帧

```python
frames, timestamps, text_timeline, scene_timeline, thumbnail = extractor.extract_smart_frames(
    "/path/to/video.mp4",
    scene_interval=2,    # Check for scene changes every 2s
    text_interval=0.5    # Check for text every 0.5s
)
```

### 分析图片

```python
# Works with images too
result = extractor.extract_content("/path/to/image.jpg")
print(result.scene_timeline[0]['description'])
```

## 输出结构

```python
ExtractedVideoContent(
    video_path="/path/to/video.mp4",
    duration=30.5,
    transcript="Here's what we found...",
    text_timeline=[
        {"at": 0.0, "text": ["Download Now"]},
        {"at": 5.5, "text": ["50% Off Today"]}
    ],
    scene_timeline=[
        {"timestamp": 0.0, "description": "Woman using phone app..."},
        {"timestamp": 2.0, "description": "Product showcase with features..."}
    ],
    thumbnail_url="/static/thumbnails/video_thumb.jpg",
    extraction_complete=True
)
```

## 主要功能

| 功能 | 描述 |
|---------|-------------|
| 场景检测 | 基于直方图的场景变化检测（阈值=65） |
| OCR 精确度 | 分层阈值设置（0.5 表示高精度，0.3 表示低精度） |
| AI 校对 | 利用 Gemini Vision 修复 OCR 识别错误 |
| 源代码整合 | 智能合并 OCR 和视觉分析得到的文本 |
| 原生视频分析 | 支持对小于 20MB 的视频文件进行直接分析 |

## 提示语

通过编辑 `prompts/` 文件夹中的提示语来自定义 AI 的行为：

- `scene_analysis.md`：用于帧分析的提示语
- `scene_reconciliation.md`：用于场景信息补充的提示语

## 常见问题解答

- “这个视频广告中出现了哪些文字？”
- “请描述这个视频中的每个场景。”
- “旁白说了什么？”
- “请从这个广告中提取呼吁行动的文字。”