---
name: yt
description: 这是一个快速的 YouTube 工具：可以获取视频的字幕、搜索视频内容，以及获取某个频道的最新视频。当有人分享 YouTube 链接、询问某个视频的相关信息，或者提到 “yt”、“youtube”、“看看这个视频”、“这个视频是关于什么的”、“查找相关视频” 或 “获取某个频道的最新视频” 时，都可以使用这个工具。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"▶️","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# yt

通过 [TranscriptAPI.com](https://transcriptapi.com) 快速查询 YouTube 内容。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，需帮助用户创建一个账户（免费提供 100 个信用点数，无需使用信用卡）：

**步骤 1 — 注册：** 向用户索取他们的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 系统会向用户的电子邮件地址发送 OTP（一次性密码）。询问用户：“请查看您的电子邮件以获取 6 位数的验证码。”

**步骤 2 — 验证：** 用户提供 OTP 后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥会被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下面的 “文件写入” 部分。修改文件前会先备份现有文件。

**手动注册方式：** [transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（同时设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改文件前，现有文件会被备份到 `~/.openclaw/openclaw.json.bak`。

若要在终端/命令行（CLI）环境中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## API 参考

完整的 OpenAPI 规范：[transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — 请查阅此处以获取最新的参数和数据结构信息。

## 获取字幕 — 需要 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

## 搜索 YouTube 内容 — 需要 1 个信用点数

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=QUERY&type=video&limit=10" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数        | 默认值    | 可选值                |
|------------|---------|----------------------|
| `q`         |         | 1-200 个字符（必填）           |
| `type`       | `video`    | `video` 或 `channel`         |
| `limit`      | `20`     | 每次查询返回的视频数量（1-50 个）     |

## 获取某个频道的最新视频信息 — 免费

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

该功能可返回某个频道的最新 15 个视频的观看次数和发布日期。支持使用 `@handle`、频道 URL 或 `UC...` 标识符进行查询。

## 将用户名转换为频道 ID — 免费

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

该功能可将用户名 `@handle` 转换为对应的频道 ID（`UC...` 格式）。

## 错误代码及处理方式

| 错误代码 | 处理方式                          |
|---------|------------------------------------|
| 402      | 信用点数不足 — 请查看 transcriptapi.com/billing          |
| 404      | 未找到相关内容或字幕                    |
| 408      | 请求超时 — 请稍后再试                    |

免费 tier：提供 100 个信用点数。搜索和获取字幕功能各需 1 个信用点数。获取频道最新视频信息和转换用户名为频道 ID 的功能是免费的。