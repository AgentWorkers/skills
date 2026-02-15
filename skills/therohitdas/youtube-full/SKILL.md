---
name: youtube-full
description: **完整的 YouTube 工具包**——包含字幕、搜索、频道、播放列表以及元数据等功能，集于一身。适用于需要全面访问 YouTube 的场景，无论是进行搜索并获取字幕、浏览频道内容，还是操作播放列表，或是需要使用 YouTube 的全部数据接口。这款工具包专为自动化脚本（agents）设计，能够满足您的各种需求。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"🎯","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# YouTube 全功能工具包

通过 [TranscriptAPI.com](https://transcriptapi.com) 提供完整的 YouTube 功能工具包。所有功能都集成在一个技能中。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供 100 个信用点数，无需使用信用卡）：

**步骤 1 — 注册：** 请求用户的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 会向用户的电子邮件发送 OTP（一次性密码）。然后询问用户：“请查看您的电子邮件以获取 6 位数的验证码。”

**步骤 2 — 验证：** 用户提供 OTP 后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥会被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下面的 **文件写入** 部分。修改前会先备份现有文件。

**手动注册方式：** [transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改前会先将现有文件备份到 `~/.openclaw/openclaw.json.bak`。

若要在终端/命令行（CLI）中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## API 参考

完整的 OpenAPI 规范：[transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — 请参考此处获取最新的参数和数据结构。

## 获取视频字幕 — 需要 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数               | 是否必填 | 默认值 | 可选值                          |
| ------------------- | -------- | ------- | ------------------------------- |
| `video_url`         | 是      | —       | YouTube 视频 URL 或 11 位的视频 ID           |
| `format`            | 否       | `json`  | `json` 或 `text`                        |
| `include_timestamp` | 否       | `true`  | `true` 或 `false`                        |
| `send_metadata`     | 否       | `false` | `true` 或 `false`                        |

**响应格式（`format=json`）：**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [{ "text": "...", "start": 18.0, "duration": 3.5 }],
  "metadata": { "title": "...", "author_name": "...", "author_url": "..." }
}
```

## 搜索视频 — 需要 1 个信用点数

```bash
# Videos
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video&limit=20" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# Channels
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=channel&limit=10" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数               | 是否必填 | 默认值 | 验证规则                          |
| ------------------- | -------- | ------- | ------------------ |
| `q`     | 是      | —       | 1-200 个字符                         |
| `type`  | 否       | `video`  | `video` 或 `channel`                    |
| `limit` | 否       | `20`    | 每页返回 1-50 个结果                   |

## 查看频道信息

所有频道相关的 API 端点都支持使用 `channel` 参数，该参数可以是频道昵称（`@handle`）、频道 URL 或 `UC...` 形式的频道 ID。无需预先解析频道信息。

### 解析频道昵称 — 免费

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

响应格式：`{"channel_id": "UC...", "resolved_from": "@TED"}`

### 获取频道最新的 15 个视频 — 免费

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

响应中会包含视频的观看次数（`viewCount`）和发布的 ISO 时间戳（`published`）。

### 查看频道的所有视频 — 每页需要 1 个信用点数

```bash
# First page (100 videos)
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?channel=@NASA" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# Next pages
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?continuation=TOKEN" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

必须提供 `channel` 或 `continuation` 参数之一。响应中会包含 `continuation_token` 和 `has_more`（表示是否还有更多视频）。

### 在频道内搜索视频 — 需要 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/search\
?channel=@TED&q=QUERY&limit=30" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

## 查看播放列表 — 每页需要 1 个信用点数

接受 `playlist` 参数，该参数可以是 YouTube 播放列表的 URL 或播放列表 ID。

```bash
# First page
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?playlist=PL_ID" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"

# Next pages
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?continuation=TOKEN" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

有效的播放列表 ID 前缀包括：`PL`、`UU`、`LL`、`FL`、`OL`。响应中会包含 `playlist_info`、`results`、`continuation_token` 和 `has_more`。

## 信用点数费用

| API 端点        | 费用     |
| --------------- | -------- |
| transcript      | 1        |
| search          | 1        |
| channel/resolve | 免费                |
| channel/latest  | 免费                |
| channel/videos  | 每页 1 个信用点数           |
| channel/search  | 1        |
| playlist/videos | 每页 1 个信用点数           |

## 验证规则

| 参数                | 规则                                      |
| ---------------------- | ------------------------------------------------------- |
| `channel`            | 必须是频道昵称（`@handle`）、频道 URL 或 `UC...` 形式的 ID         |
| `playlist`           | 必须是 YouTube 播放列表的 URL 或 ID（以 `PL`、`UU`、`LL`、`FL`、`OL` 开头） |
| `q`                | 必须是 1-200 个字符的长度                         |
| `limit`              | 每次请求返回的结果数量限制为 1-50 个                 |

## 错误代码及说明

| 代码            | 错误原因            | 处理方式                                      |
| ---------------------- | -------------------------------------- |
| 401             | API 密钥无效             | 请检查 API 密钥是否正确                         |
| 402             | 信用点数不足             | 请访问 transcriptapi.com/billing 查看计费信息             |
| 404             | 资源未找到             | 视频不存在或没有字幕                         |
| 408             | 超时                 | 请等待 2 秒后重试                         |
| 422             | 参数格式错误             | 请检查输入参数的格式                         |
| 429             | 请求频率受限             | 请稍后重试                         |

## 常见工作流程

**研究流程：** 搜索视频 → 选择目标视频 → 获取视频字幕

```bash
# 1. Search
curl -s "https://transcriptapi.com/api/v2/youtube/search\
?q=machine+learning+explained&limit=5" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
# 2. Transcript
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_ID&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

**频道监控：** 获取频道最新视频（免费） → 获取这些视频的字幕

```bash
# 1. Latest uploads (free — pass @handle directly)
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
# 2. Transcript of latest
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_ID&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

免费 tier：每天 100 个信用点数，每分钟最多 300 次请求。高级会员（每月 5 美元）：每天 1,000 个信用点数。