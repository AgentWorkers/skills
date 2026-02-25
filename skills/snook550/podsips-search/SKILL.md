---
name: podsips-search
description: 通过 PodSips API 搜索播客文本并检索剧集数据。当用户请求“搜索播客”、“查找播客片段”、“获取文本记录”、“查询剧集信息”或需要用于研究、总结或引用的播客内容时，可以使用此功能。需要设置 PODSIPS_API_KEY 环境变量。
version: 1.2.0
author: PodSips
homepage: https://developer.podsips.com
metadata: { "clawdbot": { "requires": { "env": ["PODSIPS_API_KEY"], "bins": ["curl", "jq"] }, "primaryEnv": "PODSIPS_API_KEY" } }
---
# PodSips 播客搜索 API

该 API 支持通过语义搜索在索引的播客文本中查找内容，检索完整文本，获取剧集和系列元数据，以及请求添加新的播客。

## 重要说明

- 所有请求都需要 `PODSIPS_API_KEY` 环境变量。请将其设置为 `Authorization: Bearer $PODSIPS_API_KEY`。
- 基本 URL：`https://api.podsips.com/public/v1`
- 所有响应均为 JSON 格式。
- 每次请求都会扣除相应的信用点数。大多数接口的请求成本为 1 个信用点数，完整文本的请求成本为 5 个信用点数，而播客添加请求是免费的。
- 如果用户没有 PodSips API 密钥，请按照下面的 **获取 API 密钥** 部分中的步骤进行设置。

## 获取 API 密钥

在使用任何接口之前，用户需要一个 PodSips API 密钥。如果 `PODSIPS_API_KEY` 未设置，请按照以下步骤操作：

1. 访问 **https://developer.podsips.com**
2. 点击 **使用 Google 登录** 以创建账户（这是唯一的登录方式）。
3. 登录后，系统会提示用户注册开发账户（如果尚未注册的话）。完成注册表单。
4. 进入仪表板后，导航到 **API 密钥** 部分。
5. 点击 **生成 API 密钥**。密钥仅显示一次，请将其复制下来。
6. 将密钥设置为环境变量，以便该技能能够使用它：
   ```bash
   export PODSIPS_API_KEY="ps_live_..."
   ```

每个新账户默认处于 **免费 tier**，每月拥有 100 个信用点数。如果用户需要更多信用点数，可以在 https://developer.podsips.com 的仪表板上升级计划。

## 先决条件

在发送任何请求之前，请确保 API 密钥已设置：
```bash
test -n "$PODSIPS_API_KEY" && echo "API key is set" || echo "ERROR: Set PODSIPS_API_KEY first. See the 'Getting an API Key' section above."
```

## 使用说明

### 1. 搜索播客文本

使用语义搜索找到与查询匹配的相关播客片段。这是主要的接口。

**参数：**
- `q`（必填）— 搜索查询文本
- `top_k`（可选，默认值 10）— 返回的结果数量
- `series_id`（可选）— 按特定播客系列的 UUID 过滤
- `episode_id`（可选）— 按特定剧集的 UUID 过滤
- `speakers`（可选）— 按演讲者名称过滤

**响应格式：**
```json
{
  "groups": [
    {
      "episode": {
        "uuid": "episode-uuid",
        "name": "Episode Title",
        "description": "Episode description...",
        "date_published": "2025-01-15T00:00:00Z",
        "podcast_uuid": "series-uuid",
        "speakers": ["Host Name", "Guest Name"]
      },
      "podcast": {
        "uuid": "series-uuid",
        "name": "Series Title",
        "description": "Series description..."
      },
      "chunks": [
        {
          "uuid": "chunk-uuid",
          "text": "The transcript text of the matching segment...",
          "start_time": 120.5,
          "end_time": 185.3,
          "duration": 64.8,
          "episode_uuid": "episode-uuid",
          "podcast_uuid": "series-uuid",
          "speakers": ["Speaker Name"],
          "timestamped_podcast_link": "podsips://episode-uuid?t=120",
          "episode_image_url": "https://...",
          "podcast_image_url": "https://..."
        }
      ]
    }
  ],
  "chunks": [
    {
      "uuid": "chunk-uuid",
      "text": "...",
      "start_time": 120.5,
      "end_time": 185.3,
      "duration": 64.8,
      "episode_uuid": "episode-uuid",
      "podcast_uuid": "series-uuid",
      "speakers": ["Speaker Name"],
      "timestamped_podcast_link": "podsips://episode-uuid?t=120",
      "episode_image_url": "https://...",
      "podcast_image_url": "https://..."
    }
  ],
  "meta": {
    "total_chunks": 3,
    "episodes_represented": 3,
    "query": "artificial intelligence ethics"
  }
}
```

结果以两种格式返回：`groups` 格式按剧集组织（每个组包含一个 `episode` 对象、一个 `podcast` 对象以及匹配的 `chunks`），而顶级的 `chunks` 数组则是所有匹配片段的扁平列表。`meta` 对象提供了关于结果的摘要信息。

每个片段包含文本、时间戳（`start_time`、`end_time`、`duration`）、演讲者名称和图片 URL。可以使用 `start_time` 和 `end_time` 来引用特定时间点。

**文本中的演讲者标签：** `chunks` 的 `text` 字段可能包含原始的演讲者标签，例如 `<<SPEAKER_00>>`、`<<SPEAKER_01>>` 或 `<<UNKNOWN>>`。在显示给用户之前，请将这些标签替换为实际的演讲者名称，或者将其删除。

**`timestamped_podcast_link`：** 这是一个 `podsips://` 深链接，用于在 PodSips 应用中打开指定剧集和时间点的页面。如果用户没有使用 PodSips 应用，可以忽略此字段，直接使用 `start_time` 来引用时间点。

**费用：** 每次请求 1 个信用点数。

### 2. 搜索播客系列

通过名称或描述搜索播客系列。当用户询问某个特定播客是否存在时，可以使用此接口进行查询。

**参数：**
- `q`（必填）— 搜索查询文本（搜索系列名称和描述）
- `genre`（可选）— 按类型过滤（不区分大小写）
- `limit`（可选，默认值 20，最大值 100）— 返回的结果数量
- `offset`（可选，默认值 0）— 分页偏移量

**响应格式：**
```json
[
  {
    "id": "uuid",
    "name": "Y Combinator Startup Podcast",
    "description": "We help founders make something people want...",
    "image_url": "https://...",
    "genre": "technology",
    "episode_count": 56
  }
]
```

如果没有找到匹配的系列，将返回一个空数组。

**费用：** 每次请求 1 个信用点数。

### 3. 列出所有可用的播客系列

可以浏览数据库中的所有播客系列，并支持可选的类型过滤和分页。

**参数：**
- `genre`（可选）— 按类型过滤
- `limit`（可选）— 结果数量
- `offset`（可选）— 分页偏移量

**响应格式：**
```json
[
  {
    "id": "uuid",
    "name": "Podcast Name",
    "description": "Description of the podcast",
    "image_url": "https://...",
    "genre": "Technology",
    "episode_count": 42
  }
]
```

**费用：** 每次请求 1 个信用点数。

### 4. 获取系列详情及剧集信息

检索特定系列及其所有可用剧集的信息。

**参数：**
- `series_id` — 使用系列列表或搜索结果中的 UUID

**响应格式：**
```bash
curl -s -H "Authorization: Bearer $PODSIPS_API_KEY" \
  "https://api.podsips.com/public/v1/series/{series_id}" | jq .
```

仅包含具有完整文本的剧集。

**费用：** 每次请求 1 个信用点数。

### 5. 获取剧集详情

检索特定剧集的元数据和演讲者信息。

**响应格式：**
```bash
curl -s -H "Authorization: Bearer $PODSIPS_API_KEY" \
  "https://api.podsips.com/public/v1/episodes/{episode_id}" | jq .
```

**费用：** 每次请求 1 个信用点数。

### 6. 获取时间戳周围的文本片段

检索剧集中特定时间点周围的文本片段。这有助于扩展搜索结果的上下文。

**参数：**
- `position`（必填）— 时间戳（以秒为单位）
- `pre_seconds`（可选，默认值 60）— 位置之前的上下文时间（以秒为单位）
- `post_seconds`（可选，默认值 15）— 位置之后的上下文时间（以秒为单位）

**响应格式：**
```json
{
  "episode_id": "uuid",
  "position": 120.0,
  "pre_context_seconds": 60,
  "post_context_seconds": 15,
  "pre_context": [
    {"speaker": "Dr. Jane Smith", "text": "What they said before...", "start": 62.1, "end": 68.5}
  ],
  "post_context": [
    {"speaker": "John Doe", "text": "What they said after...", "start": 120.5, "end": 134.2}
  ]
}
```

**费用：** 每次请求 1 个信用点数。

### 7. 获取完整剧集文本

检索剧集的完整文本。所有片段按时间顺序返回。

**响应格式：**
```bash
curl -s -H "Authorization: Bearer $PODSIPS_API_KEY" \
  "https://api.podsips.com/public/v1/episodes/{episode_id}/transcript" | jq .
```

**费用：** 每次请求 5 个信用点数（由于数据量较大，费用较高）。

### 8. 请求添加缺失的播客

如果用户所需的播客不在数据库中，可以提交添加请求。此操作是免费的，不消耗信用点数。

**参数：**
- `podcast_name`（必填）— 要添加的播客名称
- `rss_url`（可选）— 如果已知，提供 RSS 源链接

**响应：** 返回请求 ID 和状态。处理通常需要 24-48 小时。

**费用：** 免费（0 个信用点数）。

### 9. 检查播客请求状态

检查之前提交的播客请求是否已处理。

**响应格式：**
```bash
curl -s -H "Authorization: Bearer $PODSIPS_API_KEY" \
  "https://api.podsips.com/public/v1/podcast-requests/{request_id}" | jq .
```

**状态值：** `pending`、`processing`、`complete`、`rejected`。当状态为 `complete` 时，`resulting_series_id` 包含新系列的 UUID。

**费用：** 免费（0 个信用点数）。

## 推荐的工作流程

当用户请求从播客中查找信息时，请按照以下步骤操作：

1. **首先进行搜索。** 使用搜索接口和用户的查询进行搜索。如果结果相关，展示包含剧集名称、演讲者名称和时间戳的文本片段。
2. **如有需要，扩展上下文。** 如果搜索结果有趣，但用户希望获取更多关于该时间点的上下文信息，可以使用上下文接口，并将搜索结果中的 `start_time` 作为 `position` 参数。
3. **在适当的情况下获取完整文本。** 如果用户需要完整文本或分析整个剧集，可以使用文本片段接口。请注意，此操作费用为 5 个信用点数。
4. **处理缺失的播客。** 如果搜索没有结果，且用户询问某个特定播客：
   a. 使用 `GET /series/search?q=...` 检查该播客是否存在于数据库中。
   b. 如果找到，使用系列 UUID 通过 `series_id` 过滤文本搜索结果。
   c. 如果未找到，使用 `POST /podcast-requests` 提交添加请求。
   d. 告诉用户：“该播客目前尚不在 PodSips 数据库中。我已经提交了添加请求。处理通常需要 24-48 小时。此请求不消耗信用点数。”
   e. 如果用户之后再次询问，请使用 `GET /podcast-requests/{id}` 检查请求状态。
5. **引用来源。** 在展示播客文本片段时，请包含剧集名称、系列名称、演讲者名称和时间戳，以便用户可以验证或收听原始音频。

## 错误处理

- **HTTP 401 — API 密钥无效或缺失。** 请确认 `PODSIPS_API_KEY` 已设置且有效。用户可能需要在 https://developer.podsips.com 生成新的密钥。
- **HTTP 402 — 信用点数不足。** 开发者账户的当前计费周期内的信用点数已用完。用户需要升级计划或等待下一个计费周期。
- **HTTP 429 — 超过请求速率限制。** 当前时间窗口内的请求次数过多。请稍后重试。不同订阅等级的请求速率限制可能不同。
- **HTTP 404 — 资源未找到。** 系列、剧集或播客请求 ID 不存在。

## 信用点数统计

| 接口 | 信用点数 |
|----------|---------|
| 搜索 | 1 |
| 系列搜索 | 1 |
| 列出系列 | 1 |
| 系列详情 | 1 |
| 剧集详情 | 1 |
| 文本片段上下文 | 1 |
| 完整文本 | 5 |
| 提交播客请求 | 0 |
| 检查请求状态 | 0 |