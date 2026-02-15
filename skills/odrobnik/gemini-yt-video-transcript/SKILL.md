---
name: gemini-yt-video-transcript
description: "使用 Google Gemini 为 YouTube URL 生成逐字转录文本（包含演讲者标签和段落分隔；不包含时间戳）。适用于用户请求转录 YouTube 视频或需要纯净的转录内容（不含时间标记）的情况。"
summary: "Generate a verbatim YouTube transcript via Google Gemini (speaker labels, no time codes)."
version: 1.0.4
homepage: https://github.com/odrobnik/gemini-yt-video-transcript-skill
metadata: {"openclaw":{"emoji":"📝","requires":{"env":["GEMINI_API_KEY"],"bins":["python3"]}}}
---

# Gemini YouTube 视频字幕生成工具

使用 **Google Gemini** 为 YouTube 视频生成 **逐字记录**。

**输出格式**：
- 第一行：YouTube 视频标题
- 接下来是字幕内容，格式如下：

```
Speaker: text
```

**使用要求**：
- 不需要添加时间戳
- 不允许添加额外的标题、列表或注释

## 使用方法

```bash
python3 {baseDir}/scripts/youtube_transcript.py "https://www.youtube.com/watch?v=..."
```

**选项**：
- `--out <路径>` 将字幕内容写入指定文件（默认情况下，文件会自动保存在工作区的 `out/` 文件夹中）。

## 交付方式**
在聊天过程中，可以将生成的字幕内容以文档或附件的形式发送给对方。