---
name: torrentclaw
description: 通过 TorrentClaw 搜索和下载种子文件。当用户需要查找、搜索或下载电影、电视剧或种子文件时，可以使用该工具。它能识别系统自带的种子客户端（如 Transmission、aria2），并直接提供磁链文件；同时也可以让用户复制磁链链接或下载 .torrent 文件。支持按类型（电影/电视剧）、类型、年份、画质（480p-2160p）、评分、语言以及季数/集数（如 S01E05、1x05）进行过滤。该工具支持 API 验证（需使用 API 密钥），并具备分层速率限制功能；采用人工智能技术进行内容匹配，并对画质进行评分（0-100 分）。查询结果会包含电影/电视剧的封面图片、评分信息，以及带有磁链链接和画质评分的种子文件。
license: MIT
metadata: {"version": "0.1.13", "repository": "https://github.com/torrentclaw/torrentclaw-skill", "homepage": "https://torrentclaw.com", "openclaw": {"emoji": "🎬", "os": ["darwin", "linux", "win32"], "requires": {"bins": ["curl", "bash", "jq"], "env": ["TORRENTCLAW_API_KEY"]}, "primaryEnv": "TORRENTCLAW_API_KEY"}, "tags": ["torrent", "movies", "tv-shows", "download", "media", "entertainment", "magnet", "transmission", "aria2", "search", "4k", "hdr"]}
---

# TorrentClaw

通过整合TMDB元数据，从多个种子源中搜索电影和电视剧。能够检测到本地的种子客户端并自动开始下载。

## 基础URL

```
https://torrentclaw.com
```

## 工作流程

当用户请求查找或下载种子文件时，请按照以下步骤操作：

### 第1步：检测种子客户端

运行检测脚本，查看用户系统中可用的种子客户端：

```bash
bash "$(dirname "$0")/scripts/detect-client.sh"
```

脚本会输出包含检测到的客户端和操作系统信息的JSON格式结果。请记住该结果，以备后续步骤使用。

### 第2步：搜索内容

调用TorrentClaw API。查询时务必添加`x-search-source: skill`头部信息，以便进行数据分析：

```bash
curl -s -H "x-search-source: skill" "https://torrentclaw.com/api/v1/search?q=QUERY&sort=seeders&limit=5"
```

**有用的过滤条件**（作为查询参数使用）：
- `type=movie` 或 `type=show`（搜索电影或电视剧）
- `quality=1080p`（也可使用：720p, 2160p, 480p）
- `genre=Action`（完整列表请参见参考文档/api-reference.md）
- `year_min=2020&year_max=2025`（指定搜索年份范围）
- `min_rating=7`（最低评分）
- `lang=es`（语言代码，例如ISO 639中的西班牙语）
- `audio=atmos`（音频格式，也可使用：aac, flac, opus）
- `hdr=dolby_vision`（视频格式，也可使用：hdr10, hdr10plus, hlg）
- `season=1`（按电视剧季数过滤）
- `episode=5`（按剧集编号过滤）
- `locale=es`（获取西班牙语字幕，也可使用：fr, de, pt, it, ja, ko, zh, ru, ar）
- `sort=seeders`（按种子数量排序；也可按相关性、年份、评分或添加时间排序）

### 第3步：展示结果

以清晰的表格格式展示搜索结果。每个内容条目应包含：
- 标题、年份、内容类型
- IMDb评分（或备用选项：TMDB评分）
- 每个种子文件的详细信息：质量、编码格式、文件大小（以人类可读的方式显示）、种子数量

示例格式如下：
```
1. Inception (2010) - Movie - IMDb: 8.8
   a) 1080p BluRay x265 - 2.1 GB - 847 seeders
   b) 2160p WEB-DL x265 HDR - 8.3 GB - 234 seeders
   c) 720p BluRay x264 - 1.0 GB - 156 seeders
```

询问用户想要下载哪个种子文件。

### 第4步：处理下载

根据第1步的检测结果：
- **如果检测到种子客户端**：
  提供直接添加磁力链接的选项：
  ```bash
bash "$(dirname "$0")/scripts/add-torrent.sh" "MAGNET_URL"
```

  或者指定使用特定的客户端和下载目录：
  ```bash
bash "$(dirname "$0")/scripts/add-torrent.sh" "MAGNET_URL" --client transmission --download-dir ~/Downloads
```

- **如果没有检测到种子客户端**：
  提供以下选项：
  1. **复制磁力链接**：将API响应中的完整`magnetUrl`提供给用户以便复制。
  2. **下载.torrent文件**：使用`curl -o "filename.torrent" "https://torrentclaw.com/api/v1/torrent/INFO_HASH"`命令下载。
  3. **安装客户端**：运行安装指南脚本：
  ```bash
bash "$(dirname "$0")/scripts/install-guide.sh" transmission
```

推荐使用**Transmission**（适用于Linux/macOS，轻量级守护进程，具有简单的命令行界面）或**aria2**（支持多种协议，无需安装守护进程）作为下载工具。

## API端点

### 搜索 — `GET /api/v1/search`

主要搜索端点。必填参数：`q`（查询字符串）。
- **过滤条件**：`type`（电影/电视剧）、`genre`、`year_min`、`year_max`、`min_rating`（0-10）、`quality`（480p/720p/1080p/2160p）、`lang`（语言代码）、`audio`（音频格式）、`hdr`（视频格式）。
- **排序方式**：`sort` = 相关性 | 种子数量 | 年份 | 评分 | 添加时间。
- **分页**：`page`（1-1000）、`limit`（1-50，默认20）。
- **响应格式**：`{ total, page, pageSize, results: [{ id, imdbId, tmdbId, contentType, title, year, overview, posterUrl, backdropUrl, genres, ratingImdb, ratingTmdb, contentUrl, hasTorrents, maxSeeders, torrents: [{ infoHash, magnetUrl, torrentUrl, quality, codec, sourceType, sizeBytes, seeders, leechers, source, qualityScore, scrapedAt, uploadedAt, languages, audioCodec, hdrType, releaseGroup, isProper, isRepack, isRemastered, season, episode }] }`。
- **新增字段**：
  - `hasTorrents`（布尔值）：内容是否关联有种子文件。
  - `maxSeeders`（数字）：该内容的最大种子数量。
  - `scrapedAt`（字符串）：最后一次抓取种子/下载者信息的ISO时间戳。

### 自动完成输入 — `GET /api/v1/autocomplete`

快速输入建议功能。参数：`q`（至少输入2个字符）。最多返回8个建议结果。

### 热门内容 — `GET /api/v1/popular`

根据种子数量排序的热门内容。参数：`limit`（1-24，默认12）、`page`。

### 最新内容 — `GET /api/v1/recent`

最近添加的内容。参数：`limit`（1-24，默认12）、`page`。

### 下载种子文件 — `GET /api/v1/torrent/{infoHash}`

通过40个字符的十六进制信息哈希值下载.torrent文件。返回的文件类型为`application/x-bittorrent`。

### 统计数据 — `GET /api/v1/stats`

内容/种子文件的统计信息及最近的数据摄入记录。无需参数。

### 演员信息 — `GET /api/v1/content/{id}/credits`

显示电影的导演和前10名演员的姓名。

**参数**：`id`（必填，来自搜索结果的唯一内容ID）。
- **响应格式**：`{ contentId, director: "name", cast: [{ name, character, profileUrl }] }`。
- **用途**：当用户询问“这部电影有哪些演员？”或需要查看搜索结果的详细信息时使用。

### 记录用户操作 — `POST /api/v1/track`

记录用户的操作行为，用于生成内容的热门排名。用户选择种子文件后调用此接口。

**请求体（JSON格式）**：
```json
{"infoHash": "40-char hex", "action": "magnet|torrent_download|copy"}
```

**响应**：`{"ok": true}`

### 搜索分析 — `GET /api/v1/search-analytics`

按时间段统计搜索量、热门查询和无结果查询的数量。**需要使用专业级别的API密钥**。
- **参数**：`days`（1-90，默认7天）、`limit`（1-100，默认20）。
- **响应格式**：`{ period, summary, topQueries, zeroResultQueries, dailyVolume }`。

## 季节和剧集搜索

TorrentClaw支持多种格式的剧集过滤：
- `S01E05`（标准格式）
- `1x05`（另一种格式）
- `1x05-1x08`（剧集范围）
- `Season 1 Episode 5`（自然语言格式）

**使用方法**：
- **在查询文本中直接使用**（系统会自动解析）：
  ```bash
curl "https://torrentclaw.com/api/v1/search?q=breaking+bad+S05E14"
```

- **使用明确的参数**：
  ```bash
curl "https://torrentclaw.com/api/v1/search?q=breaking+bad&season=5&episode=14"
```

API会自动识别查询中的剧集模式并相应地过滤结果。

## API认证

TorrentClaw支持可选的API密钥认证，以提升请求速率限制。

**请求速率限制等级**：
| 等级 | 每分钟请求次数 | 每天请求次数 | 是否需要认证 |
|------|--------------|--------------|----------------|
| 匿名用户 | 30 | 无限制 | 不需要认证 |
| 免费用户 | 120 | 1,000次 | 需要API密钥 |
| 专业用户 | 1,000 | 10,000次 | 需要API密钥 |
| 内部用户 | 无限制 | 无限制 | 需要API密钥 |

**使用API密钥的方法**：
```bash
# Via header (recommended)
curl -H "Authorization: Bearer tc_live_xxxxx" \
  "https://torrentclaw.com/api/v1/search?q=dune"

# Via query parameter
curl "https://torrentclaw.com/api/v1/search?q=dune&api_key=tc_live_xxxxx"
```

**响应中的速率限制相关头部信息**：
- `X-RateLimit-Tier`：当前使用的等级（匿名/免费/专业/内部）
- `X-RateLimit-Remaining`：当前时间段内剩余的请求次数

**获取API密钥**：
请通过https://torrentclaw.com/contact或https://torrentclaw.com/api/v1/contact联系我们。

## MCP服务器集成

对于使用**Claude Desktop**、**Cursor**或**Windsurf**的用户，TorrentClaw还提供了MCP（Model Context Protocol）服务器版本：

```bash
npx @torrentclaw/mcp
```

**MCP与Skill的区别**：
- **Skill（本文件）**：适用于OpenClaw、Claude Code、Cline、Roo Code等工具，提供自然语言接口。
- **MCP服务器**：适用于Claude Desktop、Cursor、Windsurf等工具，提供结构化接口。
- **两者**都使用相同的TorrentClaw API后端。

更多关于MCP的安装和使用信息，请访问https://torrentclaw.com/mcp。

## 常见使用技巧

- **查找最高质量的种子文件**：使用`sort=seeders`并按`qualityScore`排序。
- **查找4K内容**：使用`quality=2160p`过滤条件。
- **浏览西班牙语种子文件**：使用`lang=es`过滤条件。
- **搜索特定剧集**：```bash
curl "https://torrentclaw.com/api/v1/search?q=entrevias+S01E05&locale=es"
```
- **使用API密钥提升请求速率限制**：```bash
curl -H "Authorization: Bearer tc_live_xxxxx" \
  "https://torrentclaw.com/api/v1/search?q=dune&quality=2160p"
```
- **查找热门科幻电影**：```bash
curl "https://torrentclaw.com/api/v1/search?genre=Science%20Fiction&type=movie&sort=seeders"
```
- **查找支持Dolby Vision/HDR的视频内容**：```bash
curl "https://torrentclaw.com/api/v1/search?q=dune&hdr=dolby_vision&quality=2160p"
```
- **查找电影的演员信息**：```bash
curl "https://torrentclaw.com/api/v1/content/42/credits"
```
- **用户选择种子文件后的后续操作**：```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"infoHash":"aaf1e71c...","action":"magnet"}' \
  "https://torrentclaw.com/api/v1/track"
```

## 故障排除**

- **脚本无法执行**：在`scripts`目录中运行`chmod +x scripts/*.sh`命令。
- **虽然安装了Transmission但无法使用**：确保`transmission-remote`在系统路径（PATH）中。某些系统中该软件的包名为`transmission-cli`。
- **aria2启动后立即退出**：尝试使用`--download-dir`参数或`--daemon`模式。
- **未检测到种子客户端**：运行`bash scripts/install-guide.sh transmission`以获取适用于您的操作系统的安装说明（Linux、macOS、Windows/WSL）。
- **API密钥无法使用**：
  - 确认密钥格式是否为`tc_live_`后跟32个十六进制字符。
  - 检查`Authorization: Bearer <key>`头部信息是否正确。
  - 确保密钥未过期（如有需要，请联系技术支持）。
- **检查响应中的`X-RateLimit-Tier`头部信息以确认当前使用的等级**。

**速率限制说明**：
- 匿名用户：每分钟30次请求。
- 免费用户：每分钟120次请求，每天1000次（需要API密钥）。
- 专业用户：每分钟1000次请求，每天10,000次（需要API密钥）。
- 如果遇到429错误，请稍后再试或使用API密钥。

**Windows用户注意事项**：相关脚本需要在Bash环境下运行。建议使用Windows Subsystem for Linux（WSL）或Git Bash。

## 链接**

- **官方网站**：https://torrentclaw.com
- **GitHub仓库**：https://github.com/torrentclaw/torrentclaw-skill
- **OpenAPI规范**：https://torrentclaw.com/api/openapi.json
- **Swagger文档**：https://torrentclaw.com/api/docs
- **MCP服务器**：https://torrentclaw.com/mcp
- **配置文件（llms.txt）**：https://torrentclaw.com/llms.txt