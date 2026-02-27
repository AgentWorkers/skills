---
name: transistor-fm
description: 通过 Transistor.fm 的 API 管理播客。该 API 可用于创建、发布、更新或删除播客剧集，上传音频文件，列出节目/剧集信息，查看分析数据，以及管理私人播客订阅者。适用于任何与 Transistor.fm 播客管理相关的操作。
---
# Transistor.fm 播客管理

通过 Transistor.fm 的 REST API 管理托管在其平台上的播客。

## 先决条件

- Transistor.fm API 密钥（可在“仪表板”→“账户”中获取）
- 将该密钥存储为环境变量 `TRANSISTOR_API_KEY`，或从密钥管理工具中获取

## 快速参考

所有请求均使用基础 URL `https://api.transistor.fm/v1`，并添加 `x-api-key: <key>` 头部字段。
请求速率限制：每 10 秒内最多发送 10 个请求。

有关完整端点详情、参数和响应格式，请参阅 [references/api.md](references/api.md)。

## 核心工作流程

### 列出播客及剧集

```bash
# Get all shows
curl -s "$BASE/shows" -H "x-api-key: $KEY"

# Get episodes for a show
curl -s "$BASE/episodes?show_id=SHOW_ID" -H "x-api-key: $KEY"
```

### 上传音频并创建剧集

分为三个步骤：

```bash
# 1. Get authorized upload URL
UPLOAD=$(curl -s "$BASE/episodes/authorize_upload?filename=episode.mp3" -H "x-api-key: $KEY")
# Extract upload_url and audio_url from response

# 2. Upload the audio file
curl -X PUT -H "Content-Type: audio/mpeg" -T /path/to/episode.mp3 "$UPLOAD_URL"

# 3. Create episode with the audio_url
curl -s "$BASE/episodes" -X POST -H "x-api-key: $KEY" \
  -d "episode[show_id]=SHOW_ID" \
  -d "episode[title]=My Episode" \
  -d "episode[summary]=Short description" \
  -d "episode[audio_url]=$AUDIO_URL"
```

创建的剧集默认为“草稿”状态，需单独进行发布。

### 发布剧集

```bash
# Publish now
curl -s "$BASE/episodes/EPISODE_ID/publish" -X PATCH -H "x-api-key: $KEY" \
  -d "episode[status]=published"

# Schedule for future
curl -s "$BASE/episodes/EPISODE_ID/publish" -X PATCH -H "x-api-key: $KEY" \
  -d "episode[status]=scheduled" \
  -d "episode[published_at]=2026-03-01 09:00:00"
```

### 查看分析数据

```bash
# Show-level (last 14 days default)
curl -s "$BASE/analytics/SHOW_ID" -H "x-api-key: $KEY"

# Episode-level
curl -s "$BASE/analytics/episodes/EPISODE_ID" -H "x-api-key: $KEY"

# Custom date range (dd-mm-yyyy)
curl -s "$BASE/analytics/SHOW_ID?start_date=01-01-2026&end_date=31-01-2026" -H "x-api-key: $KEY"
```

## 提示

- 所有剧集创建时均为草稿状态，发布是一个单独的操作，以便在正式发布前进行审核。
- 使用 `episode[increment_number]=true` 可自动分配剧集编号。
- `episode[description]` 支持 HTML 格式；`episode[summary]` 为纯文本。
- 音频上传链接的有效期为 600 秒，请在授权后立即上传。
- 通过使用精简的字段集（`fields[episode][]=title&fields[episode][]=status`）来减少响应数据量。