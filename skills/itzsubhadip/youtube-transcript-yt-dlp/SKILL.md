---
name: yt_transcript
description: 使用 `yt-dlp` 从现有的 YouTube 视频字幕（手动生成或自动生成的）中提取文本记录，支持可选的时间戳功能，并使用本地的 SQLite 数据库进行缓存。适用于用户请求 YouTube 视频的文字记录、字幕或 subtitle，或者希望将 YouTube 链接转换为文本以便进行摘要生成或搜索的情况。
metadata: {"openclaw":{"requires":{"bins":["python3","yt-dlp"]},"os":["linux","darwin","win32"]}}
user-invocable: true
---

# YouTube 字幕提取工具（仅提供字幕）

该工具用于从现有的 YouTube 视频字幕中提取文本内容。

**主要功能：**
- 在有手动字幕的情况下，优先使用手动字幕。
- 当手动字幕不可用时，会使用自动生成的字幕。
- 输出格式有两种：
  - JSON 格式（默认）
  - 纯文本格式（使用 `--text` 选项）
- 为提高效率，会将提取结果缓存到本地的 SQLite 数据库中。

**可靠性机制：**
- 如果 YouTube 取消了对匿名访问的权限（通过机器人检测），则会提示用户提供 `cookies.txt` 文件。
- 如果 `yt-dlp` 无法为某个视频获取字幕，脚本会尝试以下备用方法：
  1) 如果可以访问，会使用 YouTube 的字幕面板功能（通过 `youtubei get_transcript` 获取字幕）。

**隐私声明：**
- 该工具仅直接与 YouTube 进行交互（通过 `yt-dlp` 和字幕面板功能），不会将视频 ID/URL 发送给第三方字幕服务提供商。

**关于 Cookie 的说明：**
- Cookie 被视为敏感信息。
- 脚本支持 `--cookies` 或 `YT_TRANSCRIPT_COOKIES` 参数来设置 Cookie，但不会自动从脚本目录中加载 Cookie。
- Cookie 会被存储在 `~/.config/yt-transcript/` 目录下。

**路径安全规则：**
- `--cookies` 和 `--cache` 参数的路径必须指向受信任的目录。
- 允许的 Cookie 存储路径：`~/.config/yt-transcript/`
- 允许的缓存文件存储路径：`{baseDir}/cache/` 和 `~/.config/yt-transcript/`

## 使用方法：**
- 脚本路径：`{baseDir}/scripts/yt_transcript.py`
- 常见用法：
  - `python3 {baseDir}/scripts/yt_transcript.py <youtube_url_or_id>`
  - `python3 {baseDir}/scripts/yt_transcript.py <url> --lang en`
  - `python3 {baseDir}/scripts/yt_transcript.py <url> --text`
  - `python3 {baseDir}/scripts/yt_transcript.py <url> --no-ts`
- 设置 Cookie（在 VPS 环境中通常需要）：
  - `python3 {baseDir}/scripts/yt_transcript.py <url> --cookies /path/to/youtube-cookies.txt`
  - 或者通过环境变量设置：`YT_TRANSCRIPT_COOKIES=/path/to/youtube-cookies.txt`

**关于发布的注意事项：**
- Cookie 是可选的，因此脚本的元数据中并未强制要求设置 `YT_TRANSCRIPT_COOKIES`。只有在需要身份验证访问时才需要设置该参数。
- 建议将 Cookie 存储在脚本文件夹之外（以防意外发布），例如：`~/.config/yt-transcript/youtube-cookies.txt`，并通过 `--cookies` 或 `YT_TRANSCRIPT_COOKIES` 参数指定其路径。

## 脚本返回的内容：**

### JSON 格式（默认）
- 返回一个 JSON 对象，包含以下字段：
  - `video_id`：11 位的视频 ID
  - `lang`：选择的语言
  - `source`：字幕来源（`manual`、`auto` 或 `panel`）
  - `segments`：一个包含 `{start, duration, text}` 的列表（如果使用 `--no-ts` 选项，则只返回文本）

### 纯文本格式（`--text`）
- 返回以换行符分隔的文本字符串。
- 默认情况下，时间戳会以 `[12.34s]` 的格式显示。
- 使用 `--no-ts` 选项可以仅输出纯文本。

## 缓存机制：
- 默认缓存文件：`{baseDir}/cache/transcripts.sqlite`
- 缓存键包含以下字段：
  - `video_id`
  - `lang`
  - `source`
  - `include_timestamp`
  - `format`

**关于 Cookie 的重要说明：**
- Cookie 必须遵循 Netscape cookies.txt 的格式。
- Cookie 被视为敏感信息，切勿将其存储或发布到 ClawHub。

**推荐的本地 Cookie 存储路径（Git 发布时会被忽略）：**
- `/{baseDir}/cache/youtube-cookies.txt`（权限设置为 600）

**其他注意事项（安全与可靠性）：**
- 仅接受 YouTube 视频的 URL 或 11 位的视频 ID 作为输入。
- 不会将用户提供的任何参数传递给外部工具。
- 如果 `yt-dlp` 未安装，建议用户安装它：
  - 使用 `pipx` 安装 `yt-dlp`：
    - `pipx install yt-dlp`
  - 确保 `yt-dlp` 已添加到系统的 PATH 环境变量中。