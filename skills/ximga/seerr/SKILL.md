---
name: seerr
description: 通过 Seerr 实例搜索电影和电视剧，并请求下载它们。当用户请求下载、查找或排队某部电影或电视剧时，可以使用此功能。需要运行中的 Seerr 实例，并且已配置 Sonarr/Radarr。
env:
  - SEERR_URL
  - SEERR_API_KEY
---
# Seerr 媒体请求

通过 Seerr 的 API 搜索和请求电影/电视剧。Seerr 会自动将电影请求路由到 Radarr，将电视剧请求路由到 Sonarr。

## 设置

该代理需要两个环境变量。请将它们存储在您的 OpenClaw 环境或 `.env` 文件中：

- `SEERR_URL` — Seerr 实例的基 URL（例如，如果在本地运行则为 `http://localhost:5055`，或在远程服务器上则为 `http://<server-ip>:5055`）
- `SEERR_API_KEY` — 来自 Seerr 的 API 密钥（可在“设置”→“常规”中找到）

**重要提示：** 在 API 调用中始终使用 `$SEERR_URL`（而不是硬编码的 `localhost`），以确保无论 Seerr 部署在何处都能正常工作。

## API 参考

所有请求都需要包含以下头部信息：`X-Api-Key: <SEERR_API_KEY>`

### 搜索

```bash
curl -s -H "X-Api-Key: $SEERR_API_KEY" \
  "$SEERR_URL/api/v1/search?query=PERCENT_ENCODED_QUERY&page=1&language=en"
```

结果数组。每个结果的键字段包括：
- `mediaType` — `movie`（电影）、`tv`（电视剧）或 `person`（人物）
- `id` — TMDB ID（用于请求）
- `title`（电影）/ `name`（电视剧）
- `releaseDate` / `firstAirDate`（上映日期/首播日期）
- `overview`（剧情简介）
- `mediaInfo.status` — `1`（未知）、`2`（待处理）、`3`（正在处理中）、`4`（部分可用）、`5`（已可用）。如果从未请求过，则该字段为空。

仅过滤出 `mediaType` 为 `movie` 或 `tv` 的结果。

### 请求电影

```bash
curl -s -X POST -H "X-Api-Key: $SEERR_API_KEY" -H "Content-Type: application/json" \
  "$SEERR_URL/api/v1/request" \
  -d '{"mediaType":"movie","mediaId":TMDB_ID}'
```

### 请求电视剧

**所有季数：**
```bash
curl -s -X POST -H "X-Api-Key: $SEERR_API_KEY" -H "Content-Type: application/json" \
  "$SEERR_URL/api/v1/request" \
  -d '{"mediaType":"tv","mediaId":TMDB_ID,"seasons":"all"}'
```

**特定季数：**
```bash
curl -s -X POST -H "X-Api-Key: $SEERR_API_KEY" -H "Content-Type: application/json" \
  "$SEERR_URL/api/v1/request" \
  -d '{"mediaType":"tv","mediaId":TMDB_ID,"seasons":[1,3]}'
```

### 检查状态

```bash
# Movie
curl -s -H "X-Api-Key: $SEERR_API_KEY" "$SEERR_URL/api/v1/movie/TMDB_ID"

# TV
curl -s -H "X-Api-Key: $SEERR_API_KEY" "$SEERR_URL/api/v1/tv/TMDB_ID"
```

## 工作流程

1. 搜索所需标题。
2. 过滤出电影或电视剧的结果，并显示前 1–3 个匹配项（包括标题、年份和评分以及剧情简介）。
3. 检查资源是否已可用：
   - 如果 `mediaInfo.status` 为 5（已可用），则通知用户并跳过请求。
   - 如果资源未可用（状态为 1–4 或信息缺失），则通过 API 自动请求资源。
4. 请求后，确认资源是否已加入队列。
5. 对于电视剧，询问用户是否需要所有季数或特定季数（除非用户已明确指定）。
6. 响应中必须包含 Seerr 的 URL 链接。

## Discord 集成

在 Discord 中回复时，发送纯文本消息，并使用内联链接和可选的海报图片。请勿使用交互式组件——OpenClaw 尚不支持这些功能。

### Discord 消息格式

```json
{
  "action": "send",
  "channel": "discord",
  "to": "channel:<CHANNEL_ID>",
  "message": "<title> (<year>) — ⭐ <rating>\n<genre>\n\n<overview snippet...>\n\n<status emoji> <status text>\n\n🔗 [View in Seerr]($SEERR_URL/<mediaType>/<tmdbId>)",
  "media": "<poster image URL>"
}
```

### 关键要点：

- 使用 Markdown 格式发送纯文本：加粗标题，用表情符号表示状态。
- 使用 `media` 字段附加来自 TMDB 的海报图片（例如：`https://image.tmdb.org/t/p/w500/<posterPath>`）。
- 使用内联链接提供 Seerr 的 URL：`[$SEERR_URL/<mediaType>/<tmdbId>]`。
- 使用表情符号表示状态：✅ 已可用、⏳ 待处理/正在处理中、🔄 部分可用。
- 显示结果后，检查资源是否已可用：
  - 如果资源未可用（`mediaInfo.status` 不等于 5），则通过 API 自动请求资源。
  - 然后回复确认已进行请求。
- 响应中必须包含 Seerr 的链接，以便用户可以在 UI 中查看资源。