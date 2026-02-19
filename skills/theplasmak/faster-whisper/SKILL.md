---
name: faster-whisper
description: "使用 faster-whisper 实现本地语音转文本功能：其转录速度比 OpenAI Whisper 快 4 到 6 倍，同时保持相同的准确率；通过 GPU 加速，可实现近乎实时的转录效果（约 20 倍速）。支持 SRT/VTT/TTML/CSV 格式的字幕文件、说话者标注功能、URL/YouTube 视频输入、批量处理（并提供预计完成时间）、转录文本搜索、章节检测以及文件级别的语言信息识别。"
version: 1.5.0
author: ThePlasmak
homepage: https://github.com/ThePlasmak/faster-whisper
tags:
  [
    "audio",
    "transcription",
    "whisper",
    "speech-to-text",
    "ml",
    "cuda",
    "gpu",
    "subtitles",
    "diarization",
    "podcast",
    "chapters",
    "search",
    "csv",
    "ttml",
    "batch",
  ]
platforms: ["linux", "macos", "wsl2"]
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "requires":
          {
            "bins": ["python3"],
            "optionalBins": ["ffmpeg", "yt-dlp"],
            "optionalPaths": ["~/.cache/huggingface/token"],
          },
      },
  }
---
# 更快的Whisper

这是一个基于CTranslate2实现的本地语音转文本工具，它使用了OpenAI的Whisper模型，运行速度比原版快4到6倍，同时保持了相同的准确率。通过GPU加速，转录速度可达到接近实时的水平（10分钟的音频文件大约30秒内完成）。

## 使用场景

以下情况适合使用此工具：
- **转录音频/视频文件**：会议记录、采访、播客、讲座、YouTube视频
- **生成字幕**：SRT、VTT、ASS、LRC或TTML格式的字幕
- **识别说话者**：为音频文件添加说话者标签
- **从URL转录**：通过yt-dlp自动下载YouTube视频的音频
- **批量处理文件**：支持glob模式和目录路径
- **显示预计完成时间（ETA）**：自动显示每个文件的转录完成时间

## 重要规则
1. 保持翻译内容的自然流畅性，同时确保技术准确性。
2. 保留所有的代码示例、命令和URL。
3. 完整保留Markdown格式。
4. 在适当的情况下使用技术术语（如OpenClaw、ClawHub、API、CLI）。
5. 仅翻译代码块中的注释，如果这些注释具有解释性。
6. 保持与原始文档相同的结构和组织结构。
7. 不要添加或删除任何部分。
8. 如有需要，保留所有占位符（如```dot
digraph model_selection {
    rankdir=LR;
    node [shape=box, style=rounded];

    start [label="Start", shape=doublecircle];
    need_accuracy [label="Need maximum\naccuracy?", shape=diamond];
    multilingual [label="Multilingual\ncontent?", shape=diamond];
    resource_constrained [label="Resource\nconstraints?", shape=diamond];

    large_v3 [label="large-v3\nor\nlarge-v3-turbo", style="rounded,filled", fillcolor=lightblue];
    large_turbo [label="large-v3-turbo", style="rounded,filled", fillcolor=lightblue];
    distil_large [label="distil-large-v3.5\n(default)", style="rounded,filled", fillcolor=lightgreen];
    distil_medium [label="distil-medium.en", style="rounded,filled", fillcolor=lightyellow];
    distil_small [label="distil-small.en", style="rounded,filled", fillcolor=lightyellow];

    start -> need_accuracy;
    need_accuracy -> large_v3 [label="yes"];
    need_accuracy -> multilingual [label="no"];
    multilingual -> large_turbo [label="yes"];
    multilingual -> resource_constrained [label="no (English)"];
    resource_constrained -> distil_small [label="mobile/edge"];
    resource_constrained -> distil_medium [label="some limits"];
    resource_constrained -> distil_large [label="no"];
}
```）。