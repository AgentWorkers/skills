---
name: youtube-playlist
description: **功能概述：**  
浏览 YouTube 播放列表并获取视频字幕。当用户分享播放列表链接、询问播放列表中的内容、请求列出播放列表中的视频，或希望处理播放列表中的视频并获取其字幕时，可使用该功能。  

**使用场景：**  
- 用户分享播放列表链接时  
- 用户询问播放列表中包含哪些视频时  
- 用户需要浏览播放列表内容时  
- 用户希望处理播放列表中的视频并获取其字幕时  

**技术实现细节：**  
该功能通过解析用户提供的播放列表链接，从 YouTube 获取播放列表中的所有视频信息，并自动下载这些视频的字幕文件。具体实现包括：  
1. 解析播放列表的 URL 结构，提取视频列表中的每个视频的详细信息（如视频标题、时长等）  
2. 使用 YouTube 提供的 API 下载每个视频的字幕文件  
3. 将下载到的字幕文件保存到用户指定的目录中  
4. 提供用户友好的界面，方便用户查看和操作这些视频及字幕  

**注意事项：**  
- 该功能依赖于 YouTube 的 API，因此可能需要用户授权才能正常使用  
- 对于某些特殊类型的播放列表（如受版权保护的视频），可能无法获取字幕  
- 字幕文件的格式可能因视频类型而异（如 SRT、VTT 等），系统会自动选择合适的格式进行保存
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"📋","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# YouTube 播放列表

您可以通过 [TranscriptAPI.com](https://transcriptapi.com) 浏览播放列表并获取视频字幕。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供 100 个信用点，无需信用卡）：

**步骤 1 — 注册：** 询问用户的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 系统会向用户的电子邮件发送验证码（OTP）。请用户查看邮件并输入 6 位验证码。

**步骤 2 — 验证：** 用户提供验证码后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥会被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下方的 **文件写入** 部分。修改前会先备份现有文件。

**手动注册方式：** [transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改前会先备份现有文件（备份文件名为 `~/.openclaw/openclaw.json.bak`）。

若要在终端或命令行（CLI）中使用该 API 密钥，请手动将其添加到您的 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## API 参考

完整的 OpenAPI 规范请参见：[transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — 请查阅最新的参数和数据结构。

## GET /api/v2/youtube/playlist/videos — 每页 1 个视频（需 1 个信用点）

该接口用于分页获取 YouTube 播放列表中的视频列表（每页显示 100 个视频）。支持使用播放列表的 URL 或播放列表 ID 作为参数：

```bash
# First page
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?playlist=PL_PLAYLIST_ID" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# Next pages
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?continuation=TOKEN" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数          | 是否必填    | 验证规则                                           |
| -------------- | ----------- | ---------------------------------------------------- |
| `playlist`     | 是         | 必须是 YouTube 播放列表的 URL 或 ID （前缀为 `PL`/`UU`/`LL`/`FL`/`OL`） |
| `continuation` | 是         | 非空字符串                                           |

请仅提供 `playlist` 或 `continuation` 中的一个参数，切勿同时提供两个。

**支持的播放列表 ID 前缀：**

- `PL` — 用户创建的播放列表
- `UU` — 频道上传的播放列表
- `LL` — 用户喜欢的视频
- `FL` — 用户收藏的视频
- `OL` — 其他系统生成的播放列表

**响应内容：**

```json
{
  "results": [
    {
      "videoId": "abc123xyz00",
      "title": "Playlist Video Title",
      "channelId": "UCuAXFkgsw1L7xaCfnd5JJOw",
      "channelTitle": "Channel Name",
      "channelHandle": "@handle",
      "lengthText": "10:05",
      "viewCountText": "1.5M views",
      "thumbnails": [{ "url": "...", "width": 120, "height": 90 }],
      "index": "0"
    }
  ],
  "playlist_info": {
    "title": "Best Science Talks",
    "numVideos": "47",
    "description": "Top science presentations",
    "ownerName": "TED",
    "viewCount": "5000000"
  },
  "continuation_token": "4qmFsgKlARIYVVV1...",
  "has_more": true
}
```

**分页流程：**

1. 第一次请求：`?playlist=PLxxx` — 返回前 100 个视频以及分页令牌（`continuation_token`）
2. 下一次请求：`?continuation=TOKEN` — 返回接下来的 100 个视频以及新的分页令牌
3. 重复上述步骤，直到 `has_more: false` 或 `continuation_token: null` 为止

## 工作流程：播放列表 → 视频字幕

```bash
# 1. List playlist videos
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?playlist=PL_PLAYLIST_ID" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# 2. Get transcript from a video in the playlist
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_ID&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

## 从 URL 中提取播放列表 ID

以 `https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf` 为例，该播放列表的 ID 为 `PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf`。您也可以直接将完整的 URL 作为 `playlist` 参数传递。

## 错误代码及说明

| 错误代码 | 错误原因                | 处理方式                                           |
| -------- | ---------------------- | ------------------------------------------------ |
| 400     | 两个参数均未提供           | 请确保提供 `playlist` 或 `continuation` 中的一个参数             |
| 402     | 信用点不足               | 访问 [transcriptapi.com/billing](https://transcriptapi.com/billing) 获取更多信息       |
| 404     | 播放列表未找到             | 请确认播放列表是否为公开播放列表                         |
| 408     | 超时                   | 请稍后再试                                      |
| 422     | 播放列表格式无效             | 请提供有效的播放列表 URL 或 ID                         |

每页获取视频需要 1 个信用点。免费账户限使用 100 个信用点，每分钟最多请求 300 次。