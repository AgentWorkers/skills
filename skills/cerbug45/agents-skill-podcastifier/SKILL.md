---
name: podcastifier
description: 将收到的文本（电子邮件/新闻通讯）通过分块处理和 ffmpeg 拼接技术转换为简短的 TTS 播客。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["python3", "ffmpeg"] },
      "category": "media"
    }
  }
---
# podcastifier

将传入的文本（电子邮件/新闻通讯内容）转换为短音频播客，通过分块处理并使用 ffmpeg 进行合并。

## 主要功能
- 解析纯文本或 HTML 格式的输入内容，并提取文章中的要点（项目符号列表）。
- 为每个文本块生成对应的 TTS 文件（确保每个文件的长度符合字符限制要求），然后使用 ffmpeg 将这些 TTS 文件合并在一起。
- 输出包含引言和结尾的 MP3 文件。

## 使用方法
```bash
python podcastify.py --input newsletter.txt --voice "elevenlabs" --out briefing.mp3
```