---
name: video-transcript
description: 从视频内容中提取完整的文字记录，用于分析、总结、笔记记录或研究。当用户需要视频内容的书面版本时，或者请求“将此视频转录为文本”、“从该视频中获取文本”、“将视频转换为文本”，或者分享视频链接以进行内容提取时，可以使用此功能。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"🎬","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# 视频字幕提取

通过 [TranscriptAPI.com](https://transcriptapi.com) 从视频中提取字幕。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供 100 个信用点，无需使用信用卡）：

**步骤 1 — 注册：** 请求用户的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 会向用户的电子邮件发送 OTP（一次性密码）。询问用户：“请查看您的电子邮件以获取 6 位数的验证码。”

**步骤 2 — 验证：** 用户提供 OTP 后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥会被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下面的 **文件写入** 部分。修改前会备份现有文件。

手动注册方式：[transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改前会将现有文件备份到 `~/.openclaw/openclaw.json.bak`。

若要在终端/命令行（CLI）中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## GET /api/v2/youtube/transcript

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数               | 是否必填 | 默认值 | 可选值                                      |
| ------------------- | -------- | ------- | -------------------------------------- |
| `video_url`         | 是      | —       | YouTube 视频链接或 11 位的视频 ID                |
| `format`            | 否       | `json`  | `json`（结构化格式），`text`（纯文本格式）             |
| `include_timestamp` | 否       | `true`  | `true` 或 `false`                            |
| `send_metadata`     | 否       | `false` | `true` 或 `false`                            |

支持的 URL 格式：
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/shorts/VIDEO_ID`
- 简单的视频 ID 格式：`dQw4w9WgXcQ`

**响应**（当 `format` 为 `text` 且 `send_metadata` 为 `true` 时）：

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": "[00:00:18] We're no strangers to love\n[00:00:21] You know the rules...",
  "metadata": {
    "title": "Rick Astley - Never Gonna Give You Up",
    "author_name": "Rick Astley",
    "author_url": "https://www.youtube.com/@RickAstley",
    "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
  }
}
```

**响应**（当 `format` 为 `json` 时）：

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 },
    { "text": "You know the rules and so do I", "start": 21.5, "duration": 2.8 }
  ]
}
```

## 提示

- 首先将长字幕内容总结为要点，根据需求提供完整文本。
- 当需要精确的时间戳来引用特定时刻时，使用 `format=json`。
- 使用 `send_metadata=true` 可获取视频标题和频道信息以提供上下文。
- 该功能也支持 YouTube Shorts 视频。

## 错误信息

| 错误代码 | 错误原因 | 处理方式                                      |
| -------- | ------------- | ----------------------------------- |
| 401   | API 密钥无效 | 请检查密钥或重新设置 API 密钥                        |
| 402   | 信用点不足 | 请访问 transcriptapi.com/billing 购买更多信用点             |
| 404   | 无法获取字幕   | 视频可能未启用字幕功能                         |
| 408   | 超时      | 2 秒后重试                                    |

每次成功请求消耗 1 个信用点。免费账户限使用 100 个信用点，每分钟最多 300 次请求。