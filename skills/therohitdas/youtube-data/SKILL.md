---
name: youtube-data
description: **访问 YouTube 视频数据：字幕、元数据、频道信息、搜索结果及播放列表**  
这是一个轻量级的替代方案，用于获取 YouTube 的视频数据，无需使用 Google 的 YouTube Data API，也没有使用量限制。当用户需要从 YouTube 视频、频道或播放列表中获取结构化数据时，无需进行 Google API 的配置、处理 OAuth 认证或担心每日使用量限制，即可使用该工具。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"📊","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# YouTube 数据

可以通过 [TranscriptAPI.com](https://transcriptapi.com) 访问 YouTube 数据，这是 Google YouTube Data API 的一个轻量级替代方案。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供 100 个信用点数，无需使用信用卡）：

**步骤 1 — 注册：** 向用户索取他们的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 会向用户的电子邮件发送 OTP（一次性密码）。然后询问用户：“请查看您的电子邮件以获取 6 位数的验证码。”

**步骤 2 — 验证：** 用户提供 OTP 后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥会被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下方的 **文件写入** 部分。修改文件之前会先备份现有文件。

**手动注册方式：** [transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（同时设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改文件之前，现有文件会被备份到 `~/.openclaw/openclaw.json.bak`。

若要在终端/命令行（CLI）环境中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## API 参考

完整的 OpenAPI 规范：[transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — 请查阅此处以获取最新的参数和数据结构信息。

## 视频数据（文字记录 + 元数据）—— 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=json&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

**响应：**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 }
  ],
  "metadata": {
    "title": "Rick Astley - Never Gonna Give You Up",
    "author_name": "Rick Astley",
    "author_url": "https://www.youtube.com/@RickAstley",
    "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
  }
}
```

## 数据搜索—— 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video&limit=20" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

**视频结果字段：** `videoId`、`title`、`channelId`、`channelTitle`、`channelHandle`、`channelVerified`、`lengthText`、`viewCountText`、`publishedTimeText`、`hasCaptions`、`thumbnails`

**频道结果字段**（`type=channel`）：`channelId`、`title`、`handle`、`url`、`description`、`subscriberCount`、`verified`、`rssUrl`、`thumbnails`

## 频道数据

频道相关接口接受以下参数：`channel`（可以是频道名称（@handle）、频道 URL 或 `UC...` ID。无需先进行解析。

**将频道名称解析为 ID（免费）：**

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

返回结果：`{"channel_id": "UCsT0YIqwnpJCM-mx7-gSA4Q", "resolved_from": "@TED"}`

**获取最近 15 个视频的详细信息（免费）：**

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

返回结果包括频道信息以及一个包含 `videoId`、`title`、`published`（ISO 格式）、`viewCount`（精确数值）、`description`、`thumbnail` 的数组 `results`。

**获取频道内的所有视频（分页显示，每页 100 个视频）：**

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?channel=@NASA" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

每页返回 100 个视频，并提供分页用的 `continuation_token`。

**在频道内进行搜索（1 个信用点数）：**

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/search\
?channel=@TED&q=QUERY&limit=30" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

## 播放列表数据——每页 1 个信用点数

接受参数 `playlist`（YouTube 播放列表的 URL 或 ID）。

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?playlist=PL_ID" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

返回结果包括视频列表 `results` 以及播放列表信息（`title`、`numVideos`、`ownerName`、`viewCount`）、`continuation_token`、`has_more`。

## 信用点数费用

| 接口          | 费用       | 返回的数据                        |
|---------------|------------|-------------------------------------------|
| transcript     | 1           | 完整的文字记录 + 元数据                   |
| search        | 1           | 视频/频道详细信息                     |
| channel/resolve   | **免费**       | 频道 ID 的解析服务                   |
| channel/latest   | **免费**       | 最新 15 个视频及详细信息                |
| channel/videos   | 每页 100 个视频    | 获取频道内的所有视频                   |
| channel/search   | 1           | 符合查询条件的视频                   |

## 错误代码及处理方式

| 代码           | 处理方式                         |
|---------------|-------------------------------------------|
| 402           | 信用点数不足 — 访问 [transcriptapi.com/billing]          |
| 404           | 未找到相关内容                     |
| 408           | 超时 — 请稍后再试                   |
| 422           | 参数格式不正确                     |

免费 tier：提供 100 个信用点数，每分钟允许 300 次请求。