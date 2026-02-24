---
name: gemini-reader
description: 使用 Gemini API 来理解本地的非文本文件（PDF、视频、音频）。当用户请求阅读、总结或分析 PDF 文档、视频文件（mp4/mov/webm）或音频文件（mp3/wav/m4a/ogg）（包括音频转录功能）时，可以使用该 API。**不适用于图片**——因为主要模型已经具备图像处理能力，建议直接使用该模型进行图片理解。
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "env": ["GEMINI_API_KEY"], "pip": ["google-genai"] },
      },
  }
---
# Gemini Reader

通过 Gemini API（Python SDK `google-genai`）分析本地的 PDF、视频和音频文件。

## 前提条件

- 已安装 `google-genai` Python 包（使用 `pip install google-genai`）。
- 已设置 `GEMINI_API_KEY` 环境变量。
- 支持的文件类型：PDF、视频（mp4/webm/mov/avi/mkv）、音频（mp3/wav/m4a/ogg）。

## 使用方法

```bash
python3 scripts/gemini_read.py <file> "<prompt>" [--model MODEL] [--output PATH]
```

### 示例

```bash
# Summarize a PDF
python3 scripts/gemini_read.py paper.pdf "用中文总结这篇论文的主要内容"

# Analyze a video
python3 scripts/gemini_read.py lecture.mp4 "列出这个视频的关键要点"

# Transcribe audio
python3 scripts/gemini_read.py recording.m4a "转录这段音频的内容"

# Save output to file
python3 scripts/gemini_read.py report.pdf "提取所有数据表格" --output tables.txt
```

### 模型选择

| 别名 | 完整名称 | 适用场景 |
|-------|-----------|----------|
| `3-flash`（默认） | gemini-3-flash-preview | 快速、性能较低，适合日常使用 |
| `2.5-flash` | gemini-2.5-flash | 稳定性能，平衡性好 |
| `2.5-pro` | gemini-2.5-pro | 深度分析，适合处理长文档 |
| `3-pro` | gemini-3-pro-preview | 高级推理能力 |
| `3.1-pro` | gemini-3.1-pro-preview | 最新的专业功能 |

使用别名和 `-m` 参数进行调用：`gemini_read.py file.pdf "prompt" -m 2.5-pro`

## 注意事项

- 所有文件均通过文件上传 API 进行处理（上传 → 生成结果 → 清理），无论文件大小如何，流程都是一致的。
- 对于远程节点（例如 Mac）上的文件，需先使用 Tailscale 或 scp 将文件传输到虚拟机。
- 脚本会自动根据文件扩展名检测文件的 MIME 类型。
- API 调用是直接的，没有沙箱限制，也没有 CLI 的额外开销。
- 需要设置 `GEMINI_API_KEY` 环境变量或配置 `google-genai` 的认证信息。