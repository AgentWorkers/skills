---
name: seerr
description: 通过 Seerr 实例搜索电影和电视节目，并请求下载它们。当用户请求下载、查找、请求或排队某部电影或电视节目时，可以使用此功能。需要运行中的 Seerr 实例，并且已配置 Sonarr/Radarr。
env:
  - SEERR_URL
  - SEERR_API_KEY
---
# Seerr 媒体请求

通过 Seerr 的 API 搜索和请求电影/电视剧。Seerr 会自动将电影请求路由到 Radarr，将电视剧请求路由到 Sonarr。

## 设置

该代理需要两个环境变量。请将它们存储在 OpenClaw 的环境变量或 `.env` 文件中：

- `SEERR_URL` — Seerr 实例的基 URL（例如，如果在本地运行，则为 `http://localhost:5055`；如果是远程服务器，则为 `http://<server-ip>:5055`）
- `SEERR_API_KEY` — 来自 Seerr 的 API 密钥（可在 “设置” → “通用” 中找到）

**重要提示：** 在 API 调用中始终使用 `$SEERR_URL`（而不是硬编码的 `localhost`），以确保无论 Seerr 位于何处都能正常工作。

## API 参考

所有请求都需要包含 `X-Api-Key: <SEERR_API_KEY>` 头部字段。

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
- `overview`（简介）
- `mediaInfo.status` — `1`（未知）、`2`（待处理）、`3`（正在处理中）、`4`（部分可用）、`5`（已可用）。如果从未请求过，则该字段为空。

仅过滤出 `mediaType` 为 `movie` 或 `tv` 的结果。

### 请求电影

```bash
curl -s -X POST -H "X-Api-Key: $SEERR_API_KEY" -H "Content-Type: application/json" \
  "$SEERR_URL/api/v1/request" \
  -d '{"mediaType":"movie","mediaId":TMDB_ID}'
```

### 请求电视剧

- 所有季数：
```bash
curl -s -X POST -H "X-Api-Key: $SEERR_API_KEY" -H "Content-Type: application/json" \
  "$SEERR_URL/api/v1/request" \
  -d '{"mediaType":"tv","mediaId":TMDB_ID,"seasons":"all"}'
```

- 特定季数：
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

1. 搜索所需电影或电视剧的标题。
2. 将结果过滤为电影或电视剧类型。
3. 对于每个结果，发送一条单独的 Discord 消息，内容包括：
   - 通过 `media` 字段显示海报图片
   - 标题、年份、评分、类型
   - 简要介绍
   - 表示状态的 emoji 和文本
   - Seerr 的链接
4. 检查资源是否可用：
   - 如果 `mediaInfo.status` 为 `5`（已可用），则仅显示状态信息。
   - 否则，通过 API 发起请求并确认资源是否可用。
5. 将每个结果作为单独的消息发送（不要将多个结果合并成一条消息）。

## Discord 集成

在 Discord 中回复时，发送纯文本消息，并包含内联链接（可选的海报图片）。请勿使用交互式组件，因为 OpenClaw 目前还不支持这些功能。

### Discord 消息格式

将每个搜索结果作为单独的消息发送。使用 `media` 字段嵌入海报图片（TMDB 图片链接格式：`https://image.tmdb.org/t/p/w500/<posterPath>`）。

### 关键点

- 每个搜索结果都应作为**单独的消息**发送。
- 使用 `media` 字段来嵌入海报图片（TMDB 图片链接格式）。
- 使用相应的 emoji 表示资源状态：✅ 已可用、⏳ 待处理中、🔄 正在处理/部分可用。
- 如果资源不可用，自动发起请求，并在获取结果后更新消息或发送确认信息。