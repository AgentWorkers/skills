---
name: video-transcript-downloader
description: 从 YouTube 及任何其他支持 yt-dlp 的网站下载视频、音频、字幕以及格式规范的文字记录（即段落式转录文本）。当需要执行以下操作时，可以使用该工具：下载视频、保存音频片段、提取字幕、获取文字记录，或者用于排查 yt-dlp/ffmpeg 的故障以及处理相关格式和播放列表的问题。
---

# 视频字幕下载工具

`./scripts/vtd.js` 可以执行以下操作：
- 将字幕以纯文本段落的形式输出（可选添加时间戳）。
- 下载视频、音频或字幕文件。

**字幕处理方式：**
- 对于 YouTube 视频：优先使用 `youtube-transcript-plus` 工具获取字幕。
- 如果 `youtube-transcript-plus` 不可用，则通过 `yt-dlp` 下载字幕，并将其格式化为纯文本段落。

## 设置

```bash
cd ~/Projects/agent-scripts/skills/video-transcript-downloader && npm ci
```

## 字幕输出（默认格式：纯文本段落）

```bash
./scripts/vtd.js transcript --url 'https://…'
./scripts/vtd.js transcript --url 'https://…' --lang en
./scripts/vtd.js transcript --url 'https://…' --timestamps
./scripts/vtd.js transcript --url 'https://…' --keep-brackets
```

## 下载视频/音频/字幕文件

```bash
./scripts/vtd.js download --url 'https://…' --output-dir ~/Downloads
./scripts/vtd.js audio --url 'https://…' --output-dir ~/Downloads
./scripts/vtd.js subs --url 'https://…' --output-dir ~/Downloads --lang en
```

## 可用的文件格式（列表及选择方式）

以下是所有可用文件格式的列表（包括格式 ID、分辨率、容器格式、是否仅包含音频等信息）：

```bash
./scripts/vtd.js formats --url 'https://…'
```

**下载特定格式的文件：**

```bash
./scripts/vtd.js download --url 'https://…' --output-dir ~/Downloads -- --format 137+140
```

**优先选择 MP4 格式（尽可能避免重新编码）：**

```bash
./scripts/vtd.js download --url 'https://…' --output-dir ~/Downloads -- --remux-video mp4
```

## 注意事项：**
- 默认情况下，字幕输出为纯文本段落。仅在需要时使用 `--timestamps` 选项添加时间戳。
- 标有方括号的提示信息（如 `[Music]`）在默认输出中会被删除；如需保留这些信息，请使用 `--keep-brackets` 选项。
- 可在 `--` 后添加额外的 `yt-dlp` 命令参数，用于指定字幕、音频、字幕文件或视频文件的下载方式。

```bash
./scripts/vtd.js formats --url 'https://…' -- -v
```

## 故障排除（仅在需要时使用）**
- 如果 `yt-dlp` 或 `ffmpeg` 无法正常使用，请检查相关软件是否已安装并正确配置。

```bash
brew install yt-dlp ffmpeg
```

**验证工具是否正常工作：**

```bash
yt-dlp --version
ffmpeg -version | head -n 1
```