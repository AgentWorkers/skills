---
name: youtube-search
description: 在 YouTube 上搜索视频和频道，可以在特定频道内进行搜索，然后获取这些视频的文字记录（字幕）。当用户请求“查找关于 X 的视频”、“在 YouTube 上搜索”、“查找某个频道”、“了解哪些频道制作相关视频”或希望发现某个主题的 YouTube 内容时，可以使用此功能。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"🔍","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# YouTube 搜索

通过 [TranscriptAPI.com](https://transcriptapi.com) 在 YouTube 上进行搜索并获取视频字幕。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供 100 个信用点，无需使用信用卡）：

**步骤 1 — 注册：** 询问用户的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 会向用户的电子邮件发送验证码。询问用户：“请查看您的电子邮件以获取 6 位数的验证码。”_

**步骤 2 — 验证：** 用户提供验证码后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥将保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下面的 **文件写入** 部分。修改前会备份现有文件。

手动注册方式：[transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改前会将现有文件备份到 `~/.openclaw/openclaw.json.bak`。

若要在终端/命令行（CLI）中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## API 参考

完整的 OpenAPI 规范：[transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — 请查阅此处以获取最新的参数和数据结构。

## GET /api/v2/youtube/search — 需要 1 个信用点

在 YouTube 上全局搜索视频或频道。

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video&limit=20" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数    | 是否必填 | 默认值 | 验证规则                          |
| ------- | -------- | ------- | ----------------------------------- |
| `q`     | 是      | —       | 1-200 个字符（去除多余字符）                 |
| `type`  | 否       | `video`   | `video` 或 `channel`                    |
| `limit` | 否       | `20`     | 1-50                               |

**视频搜索结果：**

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

**频道搜索结果**（`type=channel`）：

```json
{
  "results": [{
    "type": "channel",
    "channelId": "UCuAXFkgsw1L7xaCfnd5JJOw",
    "title": "Rick Astley",
    "handle": "@RickAstley",
    "url": "https://www.youtube.com/@RickAstley",
    "description": "Official channel...",
    "subscriberCount": "4.2M subscribers",
    "verified": true,
    "rssUrl": "https://www.youtube.com/feeds/videos.xml?channel_id=UC...",
    "thumbnails": [...]
  }],
  "result_count": 5
}
```

## GET /api/v2/youtube/channel/search — 需要 1 个信用点

在特定频道内搜索视频。支持使用 `channel` 参数，该参数可以是频道昵称（`@handle`）、频道 URL 或频道 ID（`UC...`）。

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/search\
?channel=@TED&q=climate+change&limit=30" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数    | 是否必填 | 验证规则                          |
| --------- | -------- | ----------------------------------------- |
| `channel` | 是      | `@handle`、频道 URL 或频道 ID                 |
| `q`     | 是      | 1-200 个字符                         |
| `limit`   | 否       | 1-50 （默认值为 30）                        |

最多返回约 30 个结果（受 YouTube 限制）。返回结果的结构与全局搜索相同。

## GET /api/v2/youtube/channel/resolve — 免费

将频道昵称（`@handle`）转换为频道 ID：

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

## 工作流程：搜索 → 获取字幕

```bash
# 1. Search for videos
curl -s "https://transcriptapi.com/api/v2/youtube/search\
?q=python+web+scraping&type=video&limit=5" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# 2. Get transcript from result
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_ID&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

## 错误代码及处理方式

| 错误代码 | 处理方式                               |
| ---- | -------------------------------------- |
| 402    | 信用点不足 — 访问 [transcriptapi.com/billing](http://transcriptapi.com/billing) |
| 404    | 未找到相关内容                          |
| 408    | 超时 — 请稍后再试                     |
| 422    | 无效的频道标识符                         |

免费 tier：提供 100 个信用点，每分钟最多 300 次请求。