---
name: extract-youtube-transcript
version: 2.1.0
description: 使用本地 Python 脚本从 YouTube 视频中提取纯文本字幕。适用于用户需要从 YouTube 视频 URL 中获取字幕、分析视频内容为文本，或从视频中提取字幕/旁白的情况。
---
# 提取 YouTube 视频的字幕

使用本技能文件夹中的 `extract_youtube_transcript.py` 命令从 YouTube 视频中提取纯文本字幕。

## 依赖项

```bash
pip show youtube-transcript-api &>/dev/null || pip install youtube-transcript-api
```

## 快速入门

```bash
python extract_youtube_transcript.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

支持的 URL 格式：`youtube.com/watch?v=`、`youtu.be/`、`/embed/`、`/live/`、`/shorts/`，或原始的 11 位字符组成的视频 ID。

## 常用用法

### 按优先顺序获取指定语言的字幕

```bash
python extract_youtube_transcript.py "URL" --lang zh-Hant en
```

按优先顺序传递所需的语言代码。如果未找到匹配的语言，则会自动使用其他可用的语言的字幕。

### 将字幕保存到文件

```bash
python extract_youtube_transcript.py "URL" --output transcript.txt
```

字幕内容会输出到标准输出（stdout），同时也会被保存到文件中。

### 先列出可用的语言代码

```bash
python extract_youtube_transcript.py "URL" --list-langs
```

在获取字幕之前，可以使用此方法查看哪些语言代码是可用的。

## 语言代码

| 代码 | 语言 |
|------|----------|
| `en` | 英语 |
| `zh-Hant` | 繁体中文 |
| `zh-Hans` | 简体中文 |
| `ja` | 日语 |
| `ko` | 韩语 |
| `es` | 西班牙语 |

## 错误处理

| 错误类型 | 原因 | 处理方法 |
|-------|-------|----------|
| `TranscriptsDisabled` | 视频所有者禁用了字幕功能 | 无法获取字幕 |
| `NoTranscriptFound` | 未找到所需的语言字幕 | 运行 `--list-langs` 命令，选择可用的语言代码 |
| `VideoUnavailable` | 视频被设置为私密或已被删除 | 请检查视频 URL 是否正确 |
| `AgeRestricted` | 视频受年龄限制 | 该功能不支持；无法解决 |
| `InvalidVideoId` | URL 或视频 ID 格式不正确 | 请检查 URL 的格式 |

## 工作流程

1. 首先尝试直接获取字幕。
2. 如果未找到字幕（`NoTranscriptFound`），运行 `--list-langs` 命令查看可用的语言代码，然后使用 `--lang <代码>` 重新获取字幕。
3. 使用 `--output` 选项将较长的字幕保存到文件中，以便后续处理。