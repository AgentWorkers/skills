---
name: transcriptapi
description: **Full Transcript API 工具包**  
该工具包可用于获取 YouTube 视频的字幕、搜索视频和频道、浏览频道上传的内容、获取最新视频以及浏览播放列表。适用于需要以编程方式处理 YouTube 内容的场景，例如获取字幕以用于总结或分析、查找特定视频或监控频道动态。  
该工具包会在以下 YouTube URL 下触发：  
`transcript`, `transcriptapi`, `video summary`, `what did they say`, `find videos about`, `search youtube`.
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"📺","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# TranscriptAPI

通过 [TranscriptAPI.com](https://transcriptapi.com) 可以获取完整的 YouTube 数据。支持获取字幕、搜索视频、频道信息以及播放列表功能，所有操作均通过同一个 API 密钥完成。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，需要帮助用户创建一个账户（免费提供 100 个信用点数，无需使用信用卡）：

**步骤 1 — 注册：** 询问用户的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 系统会向用户的电子邮件地址发送验证码（OTP）。随后请用户查看邮件并输入 6 位验证码。

**步骤 2 — 验证：** 用户输入验证码后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥会被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作细节请参见下面的 “文件写入” 部分。修改文件前会先备份现有文件。

**手动注册方式：** 访问 [transcriptapi.com/signup](https://transcriptapi.com/signup)，然后进入仪表盘（Dashboard）并选择 “API Keys”（API 密钥）。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（该文件会设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改文件前，系统会自动将现有文件备份到 `~/.openclaw/openclaw.json.bak`。

若需要在终端或命令行（CLI）环境中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## API 参考

完整的 OpenAPI 规范请参见 [transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json)，其中包含了最新的参数和数据结构信息。

## 认证

所有请求都需要在请求头中添加以下字段：
`-H "Authorization: Bearer $TRANSCRIPT_API_KEY"`

## 端点说明

- **频道相关端点：** 可接受 `channel` 参数，该参数可以是频道名称（@handle）、频道 URL 或者 YouTube 用户 ID（UC...）。无需预先解析频道信息。
- **播放列表相关端点：** 可接受 `playlist` 参数，该参数可以是播放列表的 URL 或 ID。

### GET /api/v2/youtube/transcript — 需要 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 是否必填 | 默认值 | 验证规则                                      |
| ------------------- | -------- | ------- | ------------------------------------------- |
| `video_url`         | 是      | —       | YouTube 视频的 URL 或 11 位的视频 ID             |
| `format`            | 否       | `json`    | 请求返回格式（`json` 或 `text`）                 |
| `include_timestamp` | 否       | `true`    | 是否包含时间戳                         |
| `send_metadata`     | 否       | `true`    | 是否发送元数据                         |

**响应格式（`format=json`）：**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "We're no strangers...", "start": 18.0, "duration": 3.5 }
  ],
  "metadata": { "title": "...", "author_name": "...", "author_url": "..." }
}
```

### GET /api/v2/youtube/search — 需要 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video&limit=20" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 是否必填 | 默认值 | 验证规则                                      |
| ------------------- | -------- | ------- | ------------------------------------------- |
| `q`     | 是      | —       | 搜索关键词（1-200 个字符）                     |
| `type`  | 否       | `video`    | 请求类型（`video` 或 `channel`）                |
| `limit` | 否       | `20`     | 每页返回的视频数量（1-50 个）                   |

**响应格式（`type=video`）：**

```json
{
  "results": [
    {
      "type": "video",
      "videoId": "dQw4w9WgXcQ",
      "title": "Rick Astley - Never Gonna Give You Up",
      "channelId": "UCuAXFkgsw1L7xaCfnd5JJOw",
      "channelTitle": "Rick Astley",
      "channelHandle": "@RickAstley",
      "channelVerified": true,
      "lengthText": "3:33",
      "viewCountText": "1.5B views",
      "publishedTimeText": "14 years ago",
      "hasCaptions": true,
      "thumbnails": [{ "url": "...", "width": 120, "height": 90 }]
    }
  ],
  "result_count": 20
}
```

**响应格式（`type=channel`）：**

```json
{
  "results": [
    {
      "type": "channel",
      "channelId": "UCuAXFkgsw1L7xaCfnd5JJOw",
      "title": "Rick Astley",
      "handle": "@RickAstley",
      "subscriberCount": "4.2M subscribers",
      "verified": true,
      "rssUrl": "https://www.youtube.com/feeds/videos.xml?channel_id=UC..."
    }
  ],
  "result_count": 5
}
```

### GET /api/v2/youtube/channel/resolve — 免费（0 个信用点数）

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 是否必填 | 验证规则                                      |
| ------------------- | -------- | --------------------------------------- |
| `input` | 是      | 1-200 个字符（频道名称、URL 或 YouTube 用户 ID）           |

**响应内容：**

```json
{ "channel_id": "UCsT0YIqwnpJCM-mx7-gSA4Q", "resolved_from": "@TED" }
```

如果输入的参数已经是有效的 YouTube 用户 ID（格式为 `UC[a-zA-Z0-9_-]{22}`），系统会立即返回结果，无需进行额外查询。

### GET /api/v2/youtube/channel/videos — 需要 1 个信用点数（每页返回部分结果）

```bash
# First page (100 videos)
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?channel=@NASA" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# Next pages
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?continuation=TOKEN" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 是否必填 | 验证规则                                      |
| ------------------- | -------- | --------------------------------------------- |
| `channel`      | 是      | 频道名称（@handle）、频道 URL 或 YouTube 用户 ID           |
| `continuation` | 是      | 用于分页的字符串（用于获取后续页面）                 |

必须指定 `channel` 或 `continuation` 中的一个参数。

**响应内容：**

```json
{
  "results": [{
    "videoId": "abc123xyz00",
    "title": "Latest Video",
    "channelId": "UCsT0YIqwnpJCM-mx7-gSA4Q",
    "channelTitle": "TED",
    "channelHandle": "@TED",
    "lengthText": "15:22",
    "viewCountText": "3.2M views",
    "thumbnails": [...],
    "index": "0"
  }],
  "playlist_info": {"title": "Uploads from TED", "numVideos": "5000"},
  "continuation_token": "4qmFsgKlARIYVVV1...",
  "has_more": true
}
```

### GET /api/v2/youtube/channel/latest — 免费（0 个信用点数）

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 是否必填 | 验证规则                                      |
| ------------------- | -------- | ----------------------------------------- |
| `channel`      | 是      | 频道名称（@handle）、频道 URL 或 YouTube 用户 ID           |

**响应内容：** 通过 RSS 提供该频道最近 15 个视频的列表，包括观看次数和 ISO 时间戳。

**响应格式：**

```json
{
  "channel": {
    "channelId": "...",
    "title": "TED",
    "author": "TED",
    "url": "..."
  },
  "results": [
    {
      "videoId": "abc123xyz00",
      "title": "Latest Video",
      "published": "2026-01-30T16:00:00Z",
      "viewCount": "2287630",
      "description": "Full description...",
      "thumbnail": { "url": "...", "width": "480", "height": "360" }
    }
  ],
  "result_count": 15
}
```

### GET /api/v2/youtube/channel/search — 需要 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/search\
?channel=@TED&q=climate+change&limit=30" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 是否必填 | 验证规则                                      |
| ------------------- | -------- | ----------------------------------------- |
| `channel`      | 是      | 频道名称（@handle）、频道 URL 或 YouTube 用户 ID           |
| `q`       | 是      | 搜索关键词（1-200 个字符）                     |
| `limit`   | 否       | 每页返回的视频数量（默认为 30 个）                   |

### GET /api/v2/youtube/playlist/videos — 需要 1 个信用点数（每页返回部分结果）

```bash
# First page
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?playlist=PL_PLAYLIST_ID" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# Next pages
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?continuation=TOKEN" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 是否必填 | 验证规则                                      |
| ------------------- | -------- | --------------------------------------------- |
| `playlist`     | 是      | 播放列表的 URL 或 ID（前缀为 `PL`/`UU`/`LL`/`FL`/`OL`）         |
| `continuation` | 是      | 用于分页的字符串（用于获取后续页面）                 |

## 信用点数费用

| 端点                | 费用（信用点数） |
| ------------------- | -------- |
| transcript      | 1            |
| search          | 1            |
| channel/resolve | 免费                          |
| channel/search | 1            |
| channel/videos | 1（每页）        |
| channel/latest | 免费                          |
| playlist/videos | 1（每页）        |

## 错误代码及处理方式

| 错误代码 | 错误原因 | 处理建议                                      |
| -------- | ---------------- | --------------------------------------------------- |
| 401     | API 密钥无效     | 请检查 API 密钥并重新设置                         |
| 402     | 信用点数不足     | 请在 [transcriptapi.com/billing](https://transcriptapi.com/billing) 充值       |
| 404     | 未找到相关内容     | 视频/频道/播放列表不存在或没有字幕                   |
| 408     | 超时/可重试     | 2 秒后尝试再次请求                             |
| 422     | 参数格式错误     | 请检查输入参数的格式                         |
| 429     | 请求频率限制     | 请稍后再试                         |

## 使用提示：

- 当用户提供 YouTube 视频 URL 时，可获取该视频的字幕并总结关键内容。
- 可使用 `channel/latest`（免费）功能来查看新上传的视频，无需先获取字幕；直接使用频道名称（@handle）即可。
- 研究用途：先搜索视频，再获取字幕。
- 免费 tier：提供 100 个信用点数，每分钟最多请求 300 次；高级 tier（每月 5 美元）提供 1,000 个信用点数，每分钟最多请求 300 次。