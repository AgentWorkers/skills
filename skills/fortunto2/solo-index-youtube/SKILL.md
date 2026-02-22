---
name: solo-index-youtube
description: 为YouTube频道中的视频及其字幕创建索引，以便进行语义搜索。当用户输入“index YouTube”、“add YouTube channel”、“update video index”或“index transcripts”时，该功能会自动启动。该功能支持与solograph MCP（如果可用）集成使用，或者通过yt-dlp独立运行。
license: MIT
metadata:
  author: fortunto2
  version: "2.0.0"
  openclaw:
    emoji: "🎞️"
allowed-tools: Bash, Read, Glob, Grep, Write, AskUserQuestion, mcp__solograph__source_search, mcp__solograph__source_list, mcp__solograph__source_tags, mcp__solograph__source_related
argument-hint: "[channel handles or 'all']"
---
# /index-youtube

将YouTube视频的字幕索引到一个可搜索的知识库中。根据可用的工具，支持两种模式。

## 先决条件

请确保已经安装了 `yt-dlp`：

```bash
which yt-dlp || echo "MISSING: install yt-dlp (brew install yt-dlp / pip install yt-dlp / pipx install yt-dlp)"
```

## 参数

解析 `$ARGUMENTS`，以获取频道ID或“all”：
- 如果为空或为“all”：索引所有频道（从配置文件中获取或询问用户）。
- 如果包含一个或多个频道ID：仅索引这些频道（例如：`GregIsenberg ycombinator`）。
- 可选参数：`-n <limit>`（每个频道的最大视频数量，默认为10），`--dry-run`（仅进行解析）。

## 模式检测

检查可用的模式：

### 模式1：使用 solograph MCP（推荐）

如果 MCP 工具 `source_search`、`source_list`、`source_tags` 都可用，则使用 solograph 进行索引和搜索。

**安装（如果尚未安装）：**
```bash
# Install solograph
pip install solograph
# or
uvx solograph
```

**通过 solograph CLI 进行索引：**
```bash
# Single channel
solograph-cli index-youtube -c GregIsenberg -n 10

# Multiple channels
solograph-cli index-youtube -c GregIsenberg -c ycombinator -n 10

# All channels (from channels.yaml in solograph config)
solograph-cli index-youtube -n 10

# Dry run (parse only, no DB writes)
solograph-cli index-youtube --dry-run
```

如果 `solograph-cli` 不在 PATH 环境变量中，请尝试：
```bash
uvx solograph-cli index-youtube -c <handle> -n 10
```

**通过 MCP 进行验证：**
- `source_list` — 检查 YouTube 源是否被列出。
- `source_search("startup idea", source="youtube")` — 测试语义搜索功能。
- `source_tags` — 查看从字幕中自动检测到的主题。
- `source_related(video_id)` — 根据标签查找相关视频。

### 模式2：不使用 MCP（独立备用方案）

如果 solograph MCP 工具不可用，则直接使用 `yt-dlp` 下载字幕并进行分析。

**步骤1：下载视频列表**
```bash
# Get recent video URLs from a channel
yt-dlp --flat-playlist --print url "https://www.youtube.com/@GregIsenberg/videos" | head -n 10
```

**步骤2：下载字幕**
```bash
# Download auto-generated subtitles (no video download)
yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt \
  -o "docs/youtube/%(channel)s/%(title)s.%(ext)s" \
  "<video-url>"
```

**步骤3：将 VTT 格式的字幕转换为可读文本**
```bash
# Strip VTT formatting (timestamps, positioning)
sed '/^$/d; /^[0-9]/d; /^NOTE/d; /^WEBVTT/d; /-->/d' docs/youtube/channel/video.vtt | \
  awk '!seen[$0]++' > docs/youtube/channel/video.txt
```

**步骤4：创建索引**

使用 `Read` 工具读取每个字幕文件，提取以下信息：
- 视频标题（从文件名或 `yt-dlp` 元数据中获取）
- 关键主题和见解
- 可操作的要点
- 重要片段的时间戳（如果视频有章节标记）

将索引信息写入 `docs/youtube/index.md` 文件中：

```markdown
# YouTube Knowledge Index

## Channel: {channel_name}

### {video_title}
- **URL:** {url}
- **Key topics:** {topic1}, {topic2}
- **Insights:** {summary}
- **Actionable:** {takeaway}
```

**步骤5：搜索索引内容**

将字幕文件保存为文本文件后，使用 `Grep` 进行搜索：
```bash
# Search across all transcripts
grep -ri "startup idea" docs/youtube/
```

## 输出结果

向用户报告以下信息：
1. 索引的视频数量
2. 下载的字幕数量（以及未下载的字幕数量）
3. 具有章节标记的视频数量
4. 索引文件的位置
5. 搜索索引内容的方法（使用 MCP 工具或 `Grep` 命令）

## 常见问题

### “缺少 yt-dlp”
**原因：** 未安装 `yt-dlp`。
**解决方法：** 在 macOS 上运行 `brew install yt-dlp`，在 Linux 或 Windows 上运行 `pip install yt-dlp` 或 `pipx install yt-dlp`。

### 视频被跳过（没有字幕）
**原因：** 视频没有自动生成的字幕或手动添加的字幕。
**解决方法：** 这是正常现象——有些视频确实没有字幕，因此无法被索引。

### YouTube 的请求限制
**原因：** 在短时间内发送了过多请求。
**解决方法：** 减少 `-n` 参数的值，或在 `yt-dlp` 命令中添加 `--sleep-interval 2` 选项来设置延迟，或者使用 `--cookies-from-browser chrome` 选项进行身份验证访问。

### 未找到 solograph-cli
**原因：** 未安装 solograph 或 solograph 未添加到 PATH 环境变量中。
**解决方法：** 使用 `pip install solograph` 或 `uvx solograph` 进行安装。然后运行 `which solograph-cli` 命令确认是否已安装成功。