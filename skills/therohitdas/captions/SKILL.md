---
name: captions
description: 从 YouTube 视频中提取字幕和隐藏字幕（closed captions）。当用户需要字幕、隐藏字幕（CC）、辅助文本（accessibility text），或者想要阅读视频中的内容时，可以使用此功能。该工具支持时间戳和多种语言。非常适合聋人或听力障碍者使用，也可用于内容审核、引用和翻译等场景。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"💬","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# 字幕提取

通过 [TranscriptAPI.com](https://transcriptapi.com) 从 YouTube 视频中提取字幕。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供 100 个信用点，无需使用信用卡）：

**步骤 1 — 注册：** 询问用户的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 会向用户的电子邮件发送 OTP（一次性密码）。询问用户：“请查看您的电子邮件以获取 6 位数的验证码。”

**步骤 2 — 验证：** 用户提供 OTP 后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥将保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下面的 **文件写入** 部分。修改前会先备份现有文件。

**手动注册方式：** [transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改前会先将现有文件备份到 `~/.openclaw/openclaw.json.bak`。

若要在终端/CLI 中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## 请求接口 `/api/v2/youtube/transcript`

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=json&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 是否必填 | 默认值 | 可选值                          |
|-------------------|--------|-------|-----------------------------------|
| `video_url`         | 是      | —       | YouTube 视频链接或视频 ID                   |
| `format`            | 否       | `json`   | `json`（结构化格式），`text`（纯文本格式）           |
| `include_timestamp` | 否       | `true`   | `true`（包含时间戳），`false`（不包含时间戳）         |
| `send_metadata`     | 否       | `false`   | `true`（发送元数据），`false`（不发送元数据）         |

**响应格式（`format=json`）—— 最适合辅助工具和时间分析：**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 },
    { "text": "You know the rules and so do I", "start": 21.5, "duration": 2.8 }
  ],
  "metadata": { "title": "...", "author_name": "...", "thumbnail_url": "..." }
}
```

- `start`：字幕开始的时间（以秒为单位）
- `duration`：字幕显示的时长

**响应格式（`format=text`）—— 便于阅读：**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": "[00:00:18] We're no strangers to love\n[00:00:21] You know the rules..."
}
```

## 提示

- 使用 `format=json` 可获得同步的字幕（适用于辅助工具和时间分析）。
- 使用 `format=text` 且 `include_timestamp=false` 可获得更简洁的文本格式。
- 大多数视频都支持自动生成的字幕；手动添加的字幕质量更高。

## 错误代码及处理方式

| 错误代码 | 错误原因 | 处理方法                          |
|---------|---------|--------------------------------------------|
| 402     | 无足够的信用点 | 访问 [transcriptapi.com/billing](https://transcriptapi.com/billing) 获取更多信用点 |
| 404     | 视频未启用字幕功能 | 确保视频已启用字幕功能                   |
| 408     | 超时     | 2 秒后重试                         |

每次请求消耗 1 个信用点。免费 tier 提供 100 个信用点，每分钟最多 300 次请求。