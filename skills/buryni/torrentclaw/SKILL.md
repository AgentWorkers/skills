---
name: torrentclaw
description: 通过 TorrentClaw 搜索和下载种子文件。当用户需要查找、搜索或下载电影、电视剧或种子文件时，可以使用该工具。它可以检测到本地使用的种子客户端（如 Transmission、aria2），并直接提供磁链（magnet link）；或者允许用户复制磁链或下载 .torrent 文件。支持按类型（电影/电视剧）、类型、年份、画质（480p-2160p）、评分、语言以及季数/集数（例如 S01E05、1x05）进行过滤。该工具支持 API 密钥认证，并具有分层的速率限制机制；采用 AI 技术进行精确匹配，并提供画质评分（0-100 分）。查询结果会包含电影/电视剧的封面图片、评分信息，以及带有磁链和画质评分的种子文件。
license: MIT
metadata: {"version": "0.1.17", "repository": "https://github.com/torrentclaw/torrentclaw-skill", "homepage": "https://torrentclaw.com", "openclaw": {"emoji": "🎬", "os": ["darwin", "linux", "win32"], "requires": {"bins": ["curl", "bash", "jq"], "env": ["TORRENTCLAW_API_KEY"]}, "primaryEnv": "TORRENTCLAW_API_KEY"}, "tags": ["torrent", "movies", "tv-shows", "download", "media", "entertainment", "magnet", "transmission", "aria2", "search", "4k", "hdr"]}
---
# TorrentClaw

通过整合TMDB元数据，从多个种子源中搜索电影和电视节目，并自动检测并下载本地可用的种子客户端。

## 基本URL

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

该脚本会输出包含检测到的客户端和操作系统信息的JSON数据。请记住这些信息，以用于第4步。

### 第2步：搜索内容

调用TorrentClaw API。务必在请求头中添加`x-search-source: skill`以进行数据分析。API密钥是**可选的**——匿名使用允许每分钟30次请求，这足以满足日常搜索需求。只有当设置了`$TORRENTCLAW_API_KEY`时，才需要添加`Authorization`请求头。

**重要提示：**对于用户提供的值，务必使用`--data-urlencode`参数进行编码，以防止shell注入攻击。切勿直接将用户输入插入URL字符串中。

```bash
curl -s -G -H "x-search-source: skill" \
  --data-urlencode "q=QUERY" \
  -d "sort=seeders" -d "limit=5" \
  "https://torrentclaw.com/api/v1/search"
```

如果用户配置了API密钥以获得更高的请求限制：

```bash
curl -s -G -H "x-search-source: skill" -H "Authorization: Bearer $TORRENTCLAW_API_KEY" \
  --data-urlencode "q=QUERY" \
  -d "sort=seeders" -d "limit=5" \
  "https://torrentclaw.com/api/v1/search"
```

**有用的过滤条件**（作为查询参数使用）：
- `type=movie` 或 `type=show`（搜索电影或电视节目）
- `quality=1080p`（也可使用：720p, 2160p, 480p）
- `genre=Action`（完整列表请参见参考文档/api-reference.md）
- `year_min=2020&year_max=2025`（指定搜索年份范围）
- `min_rating=7`（设置最低评分）
- `lang=es`（ISO 639语言代码）
- `audio=atmos`（也可使用：aac, flac, opus）
- `hdr=dolby_vision`（也可使用：hdr10, hdr10plus, hlg）
- `season=1`（按季筛选电视节目）
- `episode=5`（按剧集编号筛选）
- `locale=es`（获取西班牙语字幕）
- `sort=seeders`（按种子数量排序）

### 第3步：展示结果

以清晰的表格格式展示搜索结果。每个内容条目应包含：
- 标题、年份、内容类型
- IMDb评分（或备用选项：TMDB评分）
- 每个种子的详细信息：质量、编码格式、文件大小

示例格式：
```
1. Inception (2010) - Movie - IMDb: 8.8
   a) 1080p BluRay x265 - 2.1 GB - 847 seeders
   b) 2160p WEB-DL x265 HDR - 8.3 GB - 234 seeders
   c) 720p BluRay x264 - 1.0 GB - 156 seeders
```

询问用户他们想要下载哪个种子文件。

### 第4步：处理下载

根据第1步的检测结果：

**如果检测到种子客户端：**
- 直接提供磁力链接供用户下载：

```bash
bash "$(dirname "$0")/scripts/add-torrent.sh" "MAGNET_URL"
```

或者指定特定的客户端和下载目录：

```bash
bash "$(dirname "$0")/scripts/add-torrent.sh" "MAGNET_URL" --client transmission --download-dir ~/Downloads
```

**如果没有检测到种子客户端：**
- 提供以下选项：
  1. **复制磁力链接**：将API响应中的完整`magnetUrl`提供给用户。
  2. **下载torrent文件**：使用`curl -o "filename.torrent" "https://torrentclaw.com/api/v1/torrent/INFO_HASH"`命令下载。
  3. **安装客户端**：运行安装指南脚本：

```bash
bash "$(dirname "$0")/scripts/install-guide.sh" transmission
```

推荐使用**Transmission**（适用于Linux/macOS，轻量级守护进程，命令行界面简单）或**aria2**（支持多种协议，无需安装守护进程）作为下载工具。

## API接口

### 搜索 — `GET /api/v1/search`

主要搜索接口。必填参数：`q`（查询字符串）。

**过滤条件：**
- `type`（电影/电视节目类型）
- `genre`（类型）
- `year_min`（最低搜索年份）
- `year_max`（最高搜索年份）
- `min_rating`（最低评分）
- `quality`（画质）
- `lang`（语言代码）
- `audio`（音频格式）
- `hdr`（视频格式）

**排序方式：**
- `sort`：按种子数量 | 年份 | 评分 | 添加时间

**分页：**
- `page`（页码，1-1000）
- `limit`（每页显示数量，默认20条）

**响应格式：**
```json
{
  "total":总数,
  "page":当前页码,
  "pageSize":每页显示数量,
  "results": [
    {
      "id":内容ID,
      "imdbId":IMDbID,
      "tmdbId":TMDBID,
      "contentType":内容类型,
      "title":标题,
      "year":年份,
      "overview":内容简介,
      "posterUrl":海报链接,
      "genres":类型,
      "ratingImdb":IMDb评分,
      "ratingTmdb":TMDB评分,
      "contentUrl":内容链接,
      "hasTorrents":是否包含种子文件,
      "maxSeeders":该内容的最大种子数量,
      "torrents": [
        {
          "infoHash":种子文件的唯一哈希值,
          "magnetUrl":磁力链接,
          "torrentUrl":下载链接,
          "quality":画质,
          "codec":编码格式,
          "sourceType":来源类型,
          "sizeBytes":文件大小（字节）,
          "seeders":种子数量,
          "leechers":下载者数量,
          "source":来源信息,
          "qualityScore":质量评分,
          "scrapedAt":最后一次抓取时间（ISO时间戳，用于获取实时种子/下载者数量）,
          "uploadedAt":上传时间,
          "languages":支持的语言,
          "audioCodec":音频编码格式,
          "hdrType":视频格式,
          "releaseGroup":版本信息,
          "isProper":是否为官方版本,
          "isRepack":是否为重新打包版本,
          "isRemastered":是否为修复版,
          "season":季数,
          "episode":剧集编号
        }
      ]
    }
  ]
}
```

**新增字段：**
- `hasTorrents`：该内容是否包含种子文件。
- `maxSeeders`：该内容所有种子文件中的最大种子数量。
- `scrapedAt`：最后一次抓取数据的ISO时间戳（用于获取实时种子/下载者数量）。

### 自动补全 — `GET /api/v1/autocomplete`

快速输入查询词。参数：`q`（至少输入2个字符）。返回最多8个搜索建议。

### 热门内容 — `GET /api/v1/popular`

根据种子数量排序的热门内容。参数：`limit`（每页显示数量，默认12条），`page`（页码）。

### 最新内容 — `GET /api/v1/recent`

最近添加的内容。参数：`limit`（每页显示数量，默认12条），`page`（页码）。

### 下载种子文件 — `GET /api/v1/torrent/{infoHash}`

通过40个字符的哈希值下载种子文件。返回的文件格式为`application/x-bittorrent`。

### 统计数据 — `GET /api/v1/stats`

提供内容/种子文件的统计信息和最近的数据摄入记录。无需参数。

### 作者信息 — `GET /api/v1/content/{id}/credits`

显示电影的导演和前10名演员的信息。

**参数：**`id`（内容ID，必填）。

**响应格式：**
```json
{
  "contentId":内容ID,
  "director":导演名称,
  "cast": [
    {
      "name":演员名称,
      "character":角色名称,
      "profileUrl":演员个人资料链接
    }
  ]
}
```

**使用说明：**当用户询问“这部电影有哪些演员？”或需要查看搜索结果的详细信息时，可以使用此接口。

### 记录用户操作 — `POST /api/v1/track`

记录用户的操作行为，用于生成内容的热度排名。在用户选择种子文件后调用此接口。

**请求体（JSON格式）：**
```json
{"infoHash": "40-char hex", "action": "magnet|torrent_download|copy"}
```

**响应：**`{"ok": true}`

### 搜索分析 — `GET /api/v1/search-analytics`

按时间段统计搜索量、热门查询和无结果查询的数量。**需要使用专业级API密钥。**

**参数：**`days`（查询时间段，1-90天，默认7天），`limit`（查询数量，默认20条）。

**响应格式：**
```json
{
  "period":时间段,
  "summary":搜索统计信息,
  "topQueries":热门查询列表,
  "zeroResultQueries":无结果查询列表,
  "dailyVolume":每日搜索量
}
```

## 季节和剧集搜索

TorrentClaw支持多种格式的剧集筛选：

**支持的格式：**
- `S01E05`（标准格式）
- `1x05`（另一种格式）
- `1x05-1x08`（剧集范围）
- `Season 1 Episode 5`（自然语言格式）

**使用方法：**
- **在查询文本中直接输入**：系统会自动解析格式。
- **使用明确参数**：也可以通过指定参数进行筛选。

## API认证

TorrentClaw默认支持匿名访问（每分钟30次请求）。只有在使用高请求限制（如自动化脚本）时，才需要API密钥。

**请求限制等级：**

| 等级 | 每分钟请求次数 | 每天请求次数 | 是否需要认证 |
|------|--------------|--------------|----------------|
| 匿名 | 30 | 无限制 | 不需要认证 |
| 免费 | 120 | 1,000 | 需要API密钥 |
| 专业级 | 1,000 | 10,000 | 需要API密钥 |
| 内部使用 | 无限制 | 无限制 | 需要API密钥 |

**使用API密钥：**

请通过`Authorization`请求头设置环境变量`$TORRENTCLAW_API_KEY`。避免将密钥作为查询参数传递，以防被记录在服务器访问日志或HTTP请求头中。

```bash
curl -s -G -H "Authorization: Bearer $TORRENTCLAW_API_KEY" \
  --data-urlencode "q=dune" \
  "https://torrentclaw.com/api/v1/search"
```

**响应中的请求限制相关头部：**
- `X-RateLimit-Tier`：当前使用的等级（匿名/免费/专业级/内部使用）
- `X-RateLimit-Remaining`：当前时间段内剩余的请求次数

**获取API密钥：**

请访问[https://torrentclaw.com/contact](https://torrentclaw.com/contact)或[https://torrentclaw.com/api/v1/contact)获取API密钥。

## MCP服务器集成

对于使用**Claude Desktop**、**Cursor**或**Windsurf**的用户，TorrentClaw还提供了MCP（Model Context Protocol）服务器接口：

```bash
npx @torrentclaw/mcp
```

**MCP与Skill的区别：**
- **Skill（本文件）**：适用于OpenClaw、Claude Code、Cline、Roo Code等工具，提供自然语言界面。
- **MCP服务器**：适用于Claude Desktop、Cursor、Windsurf等工具，提供结构化接口。
- **两者**都使用相同的TorrentClaw API后端。

更多关于MCP的安装和使用信息，请访问[https://torrentclaw.com/mcp](https://torrentclaw.com/mcp)。

## 常用操作示例

- **查找画质最佳的种子文件**：使用`sort=seeders`并按`qualityScore`排序。
- **查找4K画质内容**：使用`quality=2160p`进行筛选。
- **浏览西班牙语种子文件**：使用`lang=es`进行筛选。
- **搜索特定剧集**：使用相应的参数进行筛选。

**使用API密钥以获得更高请求限制：**
```bash
curl -s -G -H "Authorization: Bearer $TORRENTCLAW_API_KEY" \
  --data-urlencode "q=dune" \
  -d "quality=2160p" \
  "https://torrentclaw.com/api/v1/search"
```

**查找热门科幻电影：**
```bash
curl -s -G --data-urlencode "genre=Science Fiction" \
  -d "type=movie" -d "sort=seeders" \
  "https://torrentclaw.com/api/v1/search"
```

**查找支持Dolby Vision或HDR格式的内容：**
```bash
curl -s -G --data-urlencode "q=dune" \
  -d "hdr=dolby_vision" -d "quality=2160p" \
  "https://torrentclaw.com/api/v1/search"
```

**查找支持Atmos音频格式的种子文件：**
```bash
curl -s -G --data-urlencode "q=oppenheimer" \
  -d "audio=atmos" \
  "https://torrentclaw.com/api/v1/search"
```

**获取电影演员信息：**
```bash
curl "https://torrentclaw.com/api/v1/content/42/credits"
```

**用户选择种子文件后的后续操作：**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"infoHash":"aaf1e71c...","action":"magnet"}' \
  "https://torrentclaw.com/api/v1/track"
```

## 故障排除**

- **脚本无法执行**：在`scripts`目录中运行`chmod +x scripts/*.sh`命令以赋予脚本执行权限。
- **虽然安装了Transmission但无法使用**：确保`transmission-remote`在系统路径中。在某些系统中，该软件包可能名为`transmission-cli`。
- **aria2启动后立即退出**：尝试使用`--download-dir`参数或`--daemon`模式运行`aria2`。
- **未检测到种子客户端**：运行`bash scripts/install-guide.sh transmission`以获取适用于您的操作系统的安装指南（Linux、macOS、Windows/WSL）。
- **API密钥无法使用**：
  - 确认密钥格式是否正确（格式为`tc_live_`后跟32个十六进制字符）。
  - 检查`Authorization: Bearer <key>`请求头是否正确。
  - 确保密钥未过期（如有需要，请联系技术支持）。
- **检查响应中的`X-RateLimit-Tier`头部以确认当前使用的等级**。

**请求限制说明：**
- **匿名用户**：每分钟30次请求。
- **免费用户**：每分钟120次请求，每天1,000次请求（需要API密钥）。
- **专业级用户**：每分钟1,000次请求，每天10,000次请求（需要API密钥）。
- 如果遇到429错误，请稍后重试或使用API密钥。

**Windows用户注意事项：**部分脚本需要bash环境。请使用Windows Subsystem for Linux（WSL）或Git Bash。

## 链接**

- **官方网站**：https://torrentclaw.com
- **GitHub仓库**：https://github.com/torrentclaw/torrentclaw-skill
- **OpenAPI规范**：https://torrentclaw.com/api/openapi.json
- **Swagger文档**：https://torrentclaw.com/api/docs
- **MCP服务器**：https://torrentclaw.com/mcp
- **配置文件（llms.txt）**：https://torrentclaw.com/llms.txt