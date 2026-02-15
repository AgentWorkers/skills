---
name: youtube
version: 1.0.4
description: |
  YouTube transcript extractor, video downloader, comment reader for AI agents. Extract transcripts FREE (zero API quota), search with filters, batch video details, download videos/audio. The most comprehensive YouTube skill — we analyzed 15+ tools and built the one that does everything.
homepage: https://github.com/openclaw/openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "📺",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
            {
              "id": "ytdlp-brew",
              "kind": "brew",
              "formula": "yt-dlp",
              "bins": ["yt-dlp"],
              "label": "Install yt-dlp for downloads (optional)",
            },
          ],
      },
  }
---

# YouTube Research Pro

**专为AI代理设计的最全面的YouTube功能集。**

我们分析了15款以上的YouTube MCP工具，发现每款工具都有其擅长的方面，但没有一款工具能同时满足所有需求。因此，我们开发出了这款我们梦寐以求的工具。

## 为什么选择这款工具？

| 其他工具的功能 | 我们的功能 |
|----------------|------------|
| 提取视频字幕或搜索或下载 | **三者合一** |
| 使用API获取字幕会消耗大量配额 | **免费提供字幕**（无需任何API配额） |
| 一次仅处理一个视频 | **支持批量操作**（最多处理50个视频） |
| 基本搜索功能 | **具有过滤功能**（可按日期、时长、顺序搜索） |
| 仅提供文本输出 | **支持JSON格式导出**，便于后续处理 |

### 最核心功能：免费提供字幕

大多数工具都通过YouTube Data API来获取字幕，但每次请求会消耗100个API配额。每日配额限制为10,000个，因此每天最多只能获取约100条字幕。

**我们使用`youtube-transcript-api`**——直接从YouTube的前端接口获取字幕，**完全不需要API配额**，可以无限量获取字幕。

## 快速参考

| 命令 | 配额需求 | 功能说明 |
|---------|-------|--------------|
| `transcript VIDEO` | **免费** | 获取视频字幕 |
| `transcript-list VIDEO` | **免费** | 显示可用的语言版本 |
| `download VIDEO` | **免费** | 下载视频（使用yt-dlp工具） |
| `download-audio VIDEO` | **免费** | 仅下载音频文件 |
| `search QUERY` | 100个配额 | 搜索视频 |
| `video ID [ID...]` | 1次请求 | 获取视频详情（支持批量操作） |
| `comments VIDEO` | 1个配额 | 获取视频评论及回复 |
| `channel [ID]` | 1-3个配额 | 获取频道统计信息 |

## 设置（只需一次操作）

```bash
# 1. Get credentials from Google Cloud Console
#    - Create OAuth 2.0 Client ID (Desktop app)
#    - Download JSON

# 2. Save credentials
mkdir -p ~/.config/youtube-skill
mv ~/Downloads/client_secret*.json ~/.config/youtube-skill/credentials.json

# 3. Authenticate
uv run {baseDir}/scripts/youtube.py auth
```

## 免费提供字幕！

```bash
# Plain text transcript
uv run {baseDir}/scripts/youtube.py transcript VIDEO_ID

# With timestamps
uv run {baseDir}/scripts/youtube.py transcript VIDEO_ID --timestamps

# Specific language (falls back to available)
uv run {baseDir}/scripts/youtube.py transcript VIDEO_ID -l es

# List what's available
uv run {baseDir}/scripts/youtube.py transcript-list VIDEO_ID

# JSON output
uv run {baseDir}/scripts/youtube.py transcript VIDEO_ID --json
```

**该工具也支持通过URL直接调用相关功能：**

```bash
uv run {baseDir}/scripts/youtube.py transcript "https://youtube.com/watch?v=dQw4w9WgXcQ"
```

## 搜索功能

```bash
# Basic search
uv run {baseDir}/scripts/youtube.py search "AI news 2026"

# With filters
uv run {baseDir}/scripts/youtube.py search "tutorial" -l 20 --order date
uv run {baseDir}/scripts/youtube.py search "lecture" --duration long
uv run {baseDir}/scripts/youtube.py search "news" --published-after 2026-01-01T00:00:00Z
```

## 视频详情（支持批量处理）

```bash
# Single video
uv run {baseDir}/scripts/youtube.py video dQw4w9WgXcQ

# Multiple videos at once (up to 50)
uv run {baseDir}/scripts/youtube.py video id1 id2 id3 id4 id5

# JSON output for processing
uv run {baseDir}/scripts/youtube.py video id1 id2 --json
```

## 视频评论

```bash
# Top comments
uv run {baseDir}/scripts/youtube.py comments VIDEO_ID

# With replies
uv run {baseDir}/scripts/youtube.py comments VIDEO_ID --replies

# Recent comments
uv run {baseDir}/scripts/youtube.py comments VIDEO_ID --order time -l 50
```

## 下载功能（需要yt-dlp工具）

```bash
# Video (best quality)
uv run {baseDir}/scripts/youtube.py download VIDEO_ID

# Specific resolution
uv run {baseDir}/scripts/youtube.py download VIDEO_ID -r 720p

# With subtitles
uv run {baseDir}/scripts/youtube.py download VIDEO_ID -s en

# Audio only (MP3)
uv run {baseDir}/scripts/youtube.py download-audio VIDEO_ID

# Audio as M4A
uv run {baseDir}/scripts/youtube.py download-audio VIDEO_ID -f m4a
```

## 用户数据相关操作

```bash
uv run {baseDir}/scripts/youtube.py subscriptions
uv run {baseDir}/scripts/youtube.py playlists
uv run {baseDir}/scripts/youtube.py playlist-items PLAYLIST_ID
uv run {baseDir}/scripts/youtube.py liked
uv run {baseDir}/scripts/youtube.py channel
```

## 命令别名

| 完整命令 | 别名 |
|------|-------|
| `transcript` | `tr` |
| `search` | `s` |
| `video` | `v` |
| `comments` | `c` |
| `download` | `dl` |
| `download-audio` | `dla` |

## 使用场景

- **研究**：获取视频字幕后使用大型语言模型进行分析，提取有用信息。
- **学习**：批量下载播放列表中的视频字幕，制作学习笔记。
- **监控**：搜索近期发布的视频，提取字幕以追踪趋势。
- **播客**：下载音频文件以便离线收听。
- **分析**：获取频道统计信息，对比不同频道的表现。

## 多账号支持

```bash
uv run {baseDir}/scripts/youtube.py -a work subscriptions
uv run {baseDir}/scripts/youtube.py -a personal liked
```

## 我们为何开发这款工具？

我们对比了市场上的多种工具：
- **kimtaeyoon83/mcp-server-youtube-transcript**（463个赞）：字幕质量很高，但不支持搜索功能。
- **kevinwatt/yt-dlp-mcp**（211个赞）：下载功能强大，但不提供字幕。
- **dannySubsense/youtube-mcp-server**（9个赞）：功能较为齐全，但字幕需要付费API。
- **kirbah/mcp-youtube**（9个赞）：支持批量操作，但不提供免费字幕。

**目前市场上还没有一款工具能够同时提供免费字幕、搜索功能、下载功能以及批量处理功能。**

现在，这款工具实现了这一切。

---

## 致谢

本工具由**Oscar Serra**在**Claude**（Anthropic团队）的帮助下开发完成。

*我们分析了15款以上的YouTube相关工具，最终打造出了这款功能齐全的工具。*