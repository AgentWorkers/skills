---
name: yt_transcript
description: 使用 `yt-dlp` 从现有的 YouTube 视频字幕（无论是手动生成的还是自动生成的）中提取视频文字记录，支持可选的时间戳功能，并支持将结果缓存到本地的 SQLite 数据库中。此功能适用于用户需要获取 YouTube 视频的文字记录、字幕或字幕文件的情况，或者希望将 YouTube 链接转换为文本以便进行摘要生成或搜索的场景。
metadata: {"openclaw":{"requires":{"bins":["python3","yt-dlp"]},"os":["linux","darwin","win32"]}}
user-invocable: true
---

# YouTube 字幕提取工具（仅提供字幕内容）

该工具用于从现有的 YouTube 视频字幕中提取文本内容。

**主要功能：**
- 在有手动字幕的情况下，优先使用手动字幕。
- 当手动字幕不可用时，使用自动生成的字幕。
- 输出格式可选：
  - JSON 格式（默认）
  - 纯文本格式（使用 `--text` 选项）
- 将提取结果缓存到本地的 SQLite 数据库中，以提高执行速度。

**可靠性机制：**
- 如果 YouTube 禁止匿名访问（通过机器人检测），工具会自动使用 `cookies.txt` 文件来绕过这一限制。
- 如果 `yt-dlp` 无法为视频获取字幕，工具会尝试使用 YouTube 的字幕显示面板（与用户界面中的“显示字幕”功能使用相同的接口）来获取字幕。

## 使用方法**

脚本路径：
- `{baseDir}/scripts/yt_transcript.py`

常见用法：
- `python3 {baseDir}/scripts/yt_transcript.py <youtube_url_or_id>`
- `python3 {baseDir}/scripts/yt_transcript.py <url> --lang en`
- `python3 {baseDir}/scripts/yt_transcript.py <url> --text`
- `python3 {baseDir}/scripts/yt_transcript.py <url> --no-ts`

**Cookies（可选，但在 VPS 环境中通常需要）：**
- `python3 {baseDir}/scripts/yt_transcript.py <url> --cookies /path/to/youtube-cookies.txt`
- 或者通过环境变量设置：`YT_TRANSCRIPT_COOKIES=/path/to/youtube-cookies.txt`
- 如果 `{baseDir}/cache/youtube-cookies.txt` 文件存在，工具会自动使用该文件。

**发布注意事项：**  
Cookies 是可选的，因此并未被列为 `metadata.openclaw.requires.env` 的强制要求。即使不使用 Cookies，该工具也能正常运行。

**最佳实践：**  
将 Cookies 存储在工具文件夹之外（以防意外被包含在发布版本中），例如：`~/.config/yt-transcript/youtube-cookies.txt`，并通过 `--cookies` 或 `YT_TRANSCRIPT_COOKIES` 参数指定其路径。

## 脚本返回的数据格式**

### JSON 格式（默认）
返回一个 JSON 对象，包含以下字段：
- `video_id`：11 位的视频 ID
- `lang`：选择的语言
- `source`：字幕来源（`manual`、`auto` 或 `panel`）
- `segments`：一个包含 `{start, duration, text}` 的列表（如果使用 `--no-ts` 选项，则只返回文本）

### 纯文本格式（`--text` 选项）
返回以换行符分隔的文本字符串。默认情况下，时间戳会以 `[12.34s]` 的格式显示；使用 `--no-ts` 选项可忽略时间戳。

## 缓存机制**
默认缓存文件：`{baseDir}/cache/transcripts.sqlite`

缓存键包含以下信息：
- `video_id`
- `lang`
- `source`
- `include_timestamp`
- `format`

**Cookies 处理注意事项：**
- Cookies 必须采用 Netscape cookies.txt 格式。
- 将 Cookies 视为敏感信息，切勿将其存储或发布到 ClawHub。

**推荐的本地存储路径：**  
`{baseDir}/cache/youtube-cookies.txt`（权限设置为 600，确保文件私密性）

**安全与可靠性提示：**
- 仅接受 YouTube 视频的 URL 或 11 位的视频 ID 作为输入。
- 不要将从用户那里接收的任何参数传递给脚本。
- 如果 `yt-dlp` 未安装，建议用户安装该工具：
  - 使用 `pipx` 安装：`pipx install yt-dlp`
  - 确保 `yt-dlp` 在系统的 PATH 环境变量中可用。