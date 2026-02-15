---
name: youtube-channels
description: 与 YouTube 频道交互：将频道名称解析为对应的频道 ID，浏览频道内的上传内容，获取最新视频，以及在频道内进行搜索。当用户询问某个特定频道的信息、想要查看该频道的最新上传内容，或者提出诸如“X 最近发布了什么？”、“TED 的最新视频是什么？”、“展示他们的频道内容”、“列出该频道的所有视频”或“浏览该频道的上传文件”等请求时，可以使用此功能。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"📡","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# YouTube频道工具

这些YouTube频道工具可通过 [TranscriptAPI.com](https://transcriptapi.com) 使用。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供100个信用点，无需使用信用卡）：

**步骤1 — 注册：** 向用户索取他们的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 系统会向用户的电子邮件地址发送一个一次性密码（OTP）。然后询问用户：“请查看您的电子邮件，找到6位数的验证码。”

**步骤2 — 验证：** 用户提供验证码后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API密钥会被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下面的“文件写入”部分。修改前会先备份现有文件。

**手动注册方式：** [transcriptapi.com/signup](https://transcriptapi.com/signup) → 选择“仪表盘” → “API密钥”。

## 文件写入

`verify` 和 `save-key` 命令会将API密钥保存到 `~/.openclaw/openclaw.json` 文件中（该文件会设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改前，现有文件会被备份到 `~/.openclaw/openclaw.json.bak`。

若要在终端或命令行（CLI）环境中使用该API密钥，请手动将其添加到您的Shell配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## API参考

完整的OpenAPI规范请参见 [transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json)——其中包含了最新的参数和数据结构信息。

所有频道相关的API端点都支持灵活的输入格式：`@handle`、频道URL或`UC...`频道ID。无需预先进行解析。

## GET /api/v2/youtube/channel/resolve — 免费

该API用于将 `@handle`、URL或`UC...` ID转换为规范的频道ID。

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数          | 是否必填 | 验证规则                                      |
| -------------- | -------- | ----------------------------------------- |
| `input`        | 是       | 必须为1-200个字符，格式为@handle、URL或UC... ID            |

**响应：**

```json
{ "channel_id": "UCsT0YIqwnpJCM-mx7-gSA4Q", "resolved_from": "@TED" }
```

如果输入的ID已经是`UC[a-zA-Z0-9_-]{22}`格式，系统会立即返回结果。

## GET /api/v2/youtube/channel/latest — 免费

该API可通过RSS获取该频道的最新15个视频及其详细统计信息。

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数          | 是否必填 | 验证规则                                      |
| -------------- | -------- | ----------------------------------------- |
| `channel`       | 是       | 必须为`@handle`、频道URL或`UC...` ID                   |

**响应：**

```json
{
  "channel": {
    "channelId": "UCsT0YIqwnpJCM-mx7-gSA4Q",
    "title": "TED",
    "author": "TED",
    "url": "https://www.youtube.com/channel/UCsT0YIqwnpJCM-mx7-gSA4Q",
    "published": "2006-04-17T00:00:00Z"
  },
  "results": [
    {
      "videoId": "abc123xyz00",
      "title": "Latest Video Title",
      "channelId": "UCsT0YIqwnpJCM-mx7-gSA4Q",
      "author": "TED",
      "published": "2026-01-30T16:00:00Z",
      "updated": "2026-01-31T02:00:00Z",
      "link": "https://www.youtube.com/watch?v=abc123xyz00",
      "description": "Full video description...",
      "thumbnail": { "url": "https://i1.ytimg.com/vi/.../hqdefault.jpg" },
      "viewCount": "2287630",
      "starRating": {
        "average": "4.92",
        "count": "15000",
        "min": "1",
        "max": "5"
      }
    }
  ],
  "result_count": 15
}
```

非常适合用于监控频道——免费提供视频观看次数和ISO时间戳等信息。

## GET /api/v2/youtube/channel/videos — 每页100条记录

该API用于分页显示该频道的所有上传视频。

```bash
# First page
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?channel=@NASA" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# Next pages
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?continuation=TOKEN" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数          | 是否必填 | 验证规则                                      |
| -------------- | ----------- | --------------------------------------------- |
| `channel`       | 是       | 必须为`@handle`、频道URL或`UC...` ID                   |
| `continuation` | 是       | 必须非空（用于获取后续页面）                         |

请同时提供`channel`或`continuation`中的一个参数，不可同时使用两个。

**响应：**

```json
{
  "results": [{
    "videoId": "abc123xyz00",
    "title": "Video Title",
    "channelId": "UCsT0YIqwnpJCM-mx7-gSA4Q",
    "channelTitle": "TED",
    "channelHandle": "@TED",
    "lengthText": "15:22",
    "viewCountText": "3.2M views",
    "thumbnails": [...],
    "index": "0"
  }],
  "playlist_info": {"title": "Uploads from TED", "numVideos": "5000", "ownerName": "TED"},
  "continuation_token": "4qmFsgKlARIYVVV1...",
  "has_more": true
}
```

持续调用`continuation`参数，直到系统返回`has_more: false`为止。

## GET /api/v2/youtube/channel/search — 需要1个信用点

该API用于在特定频道内进行搜索。

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/search\
?channel=@TED&q=climate+change&limit=30" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数          | 是否必填 | 验证规则                                      |
| -------------- | -------- | ----------------------------------------- |
| `channel`       | 是       | 必须为`@handle`、频道URL或`UC...` ID                   |
| `q`          | 是       | 必须为1-200个字符的搜索关键词                     |
| `limit`        | 否       | 最大为50条（默认值为30条）                         |

## 典型工作流程

```bash
# 1. Check latest uploads (free — pass @handle directly)
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# 2. Get transcript of recent video
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_ID&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

## 错误代码及处理方式

| 错误代码 | 处理方式                                      |
| -------- | -------------------------------------------------------------- |
| 400       | 参数组合无效（`channel`或`continuation`参数缺失）                |
| 402       | 未获得足够的信用点——请访问 [transcriptapi.com/billing](https://transcriptapi.com/billing) |
| 404       | 未找到对应的频道                                  |
| 408       | 超时——请稍后再试                               |
| 422       | 无效的频道标识符                                |

**免费 tier：** 提供100个信用点，每分钟最多300次请求。`resolve` 和 `latest` 等免费API接口虽然需要认证，但不消耗信用点。