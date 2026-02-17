---
name: gemini-video-analyzer
description: >
  使用 Google Gemini API 进行原生视频分析。您可以上传视频文件并进行分析，包括：描述视频中的场景、提取文本和用户界面元素、回答与视频内容相关的问题、转录语音、识别视频中的物体和动作。适用场景包括：  
  (1) 用户发送视频文件并要求对其进行分析；  
  (2) 需要对视频进行总结或描述；  
  (3) 从屏幕录制中提取文本、用户界面元素或相关信息；  
  (4) 回答关于视频内容的问题；  
  (5) 比较多个视频；  
  (6) 分析教程、演示文稿或操作指南。
homepage: https://www.agxntsix.ai
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python3", "curl"], "env": ["GOOGLE_AI_API_KEY"] },
        "primaryEnv": "GOOGLE_AI_API_KEY",
      },
  }
---
# Gemini 视频分析器

使用 Google Gemini 的多模态 API 进行视频分析，无需提取帧数据——Gemini 以每秒 1 帧的速度处理视频，同时保留完整的动作、音频和视觉信息。

## 快速入门

```bash
# Analyze a video with default prompt (full description)
GOOGLE_AI_API_KEY=$GOOGLE_AI_API_KEY python3 {baseDir}/scripts/analyze.py /path/to/video.mp4

# Ask a specific question
GOOGLE_AI_API_KEY=$GOOGLE_AI_API_KEY python3 {baseDir}/scripts/analyze.py /path/to/video.mp4 "What text is visible on screen?"

# Manage uploaded files
GOOGLE_AI_API_KEY=$GOOGLE_AI_API_KEY python3 {baseDir}/scripts/manage_files.py list
GOOGLE_AI_API_KEY=$GOOGLE_AI_API_KEY python3 {baseDir}/scripts/manage_files.py cleanup
```

## 支持的格式

MP4、AVI、MOV、MKV、WebM、FLV、MPEG、MPG、WMV、3GP——每个文件最大支持 2GB。

## 工作原理

1. 视频被上传到 Google 的 Files API（临时存储，48 小时后自动删除）。
2. Gemini 以每秒 1 帧的速度处理视频，理解其中的动作、过渡效果和音频内容。
3. 模型根据您的指令生成分析结果。
4. 与传统的帧提取方法相比，这种方法能更准确地理解视频中的时间顺序和内容。

## 使用场景

| 任务 | 示例指令 |
|------|---------------|
| 一般描述 | *(默认情况下无需提供指令)* |
| 提取 UI/文本信息 | `"视频中显示了哪些文本和 UI 元素？"` |
| 教程总结 | `"总结这个教程中的步骤"` |
| 视频中的错误报告 | `"描述这段屏幕录像中出现了什么问题"` |
| 会议记录 | `"总结讨论的重点内容"` |
| 内容对比 | "上传两个视频，比较它们之间的差异" |

## 配置

在您的环境变量或 `.env` 文件中设置 `GOOGLE.AI_API_KEY`。您可以在 [aistudio.google.com](https://aistudio.google.com/apikey) 获取免费的 API 密钥。

默认模型：`gemini-2.5-flash`（速度快、成本低、视觉识别能力出色）。如需进行复杂分析，可使用 `--model gemini-2.5-pro` 替换默认模型。

## API 参考

有关文件上传限制、处理细节和高级选项，请参阅 [references/gemini-files-api.md](references/gemini-files-api.md)。