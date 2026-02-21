---
name: solo-index-youtube
description: 将YouTube频道中的视频及其字幕索引到FalkorDB源图中，以便进行语义搜索。当用户输入“index YouTube”、“add YouTube channel”、“update video index”或“index transcripts”时，系统会执行此操作。该功能需要yt-dlp工具和SearXNG隧道处于激活状态。
license: MIT
metadata:
  author: fortunto2
  version: "1.1.0"
  openclaw:
    emoji: "🎞️"
allowed-tools: Bash, Read, Glob, Grep, AskUserQuestion
argument-hint: "[channel handles or 'all']"
---
# /index-youtube

通过 solograph CLI 将 YouTube 视频的字幕文件索引到 FalkorDB 数据库中。

## 先决条件

确保 yt-dlp 和 SearXNG 已经安装：

```bash
which yt-dlp || echo "MISSING: brew install yt-dlp"
curl -sf http://localhost:8013/health && echo "searxng_ok" || echo "MISSING: make search-tunnel (in solopreneur)"
```

如果 SearXNG 无法使用，请告知用户先在 solopreneur 中运行 `make search-tunnel` 命令。

## 参数

解析 `$ARGUMENTS` 参数，确定要索引的频道：
- 如果参数为空或为 "all"：则索引 `channels.yaml` 文件中的所有频道。
- 如果参数包含一个或多个频道名称（例如 "GregIsenberg ycombinator"）：则仅索引这些频道。

## 执行方式

运行 solograph CLI 命令：

```bash
# Single channel
TAVILY_API_URL=http://localhost:8013 uv run --project ~/startups/shared/solograph solograph-cli index-youtube -c GregIsenberg -n 10

# Multiple channels
TAVILY_API_URL=http://localhost:8013 uv run --project ~/startups/shared/solograph solograph-cli index-youtube -c GregIsenberg -c ycombinator -n 10

# All channels (from channels.yaml)
TAVILY_API_URL=http://localhost:8013 uv run --project ~/startups/shared/solograph solograph-cli index-youtube -n 10

# Dry run (parse only, no DB writes)
TAVILY_API_URL=http://localhost:8013 uv run --project ~/startups/shared/solograph solograph-cli index-youtube --dry-run
```

或者通过 solopreneur 的 Makefile 进行执行：

```bash
cd ~/startups/solopreneur && make index-youtube CHANNELS=GregIsenberg LIMIT=10
```

## 验证结果

索引完成后，需要验证以下信息：

```bash
# Check source list for youtube entry
TAVILY_API_URL=http://localhost:8013 uv run --project ~/startups/shared/solograph solograph-cli source-list

# Search indexed content
TAVILY_API_URL=http://localhost:8013 uv run --project ~/startups/shared/solograph solograph-cli source-search "startup idea" --source youtube
```

## 输出结果

向用户报告以下信息：
1. 被索引的视频数量。
2. 生成的源数据块数量。
3. 具有章节标记的视频数量。
4. 被跳过的视频数量（可能是已经索引过或没有字幕的视频）。

## 常见问题

### 错误提示：“MISSING: brew install yt-dlp”
**原因：** yt-dlp 未安装。
**解决方法：** 在 macOS 上运行 `brew install yt-dlp`，在 Linux 或 Windows 上运行 `pip install yt-dlp`。

### SearXNG 检查失败
**原因：** SSH 隧道未建立。
**解决方法：** 先在 solopreneur 中运行 `make search-tunnel` 命令。如果使用直接 URL 模式（`-u`），则不需要 SearXNG。

### 视频被跳过（没有字幕）
**原因：** 视频没有自动生成的字幕或手动添加的字幕。
**解决方法：** 这是正常现象，因为有些视频确实没有字幕。请检查 `~/.solo/sources/youtube/vtt/` 目录中是否有缓存的 VTT 文件。