---
name: subtitles
description: 从 YouTube 视频中获取字幕，可用于翻译、语言学习或同步阅读。当用户需要字幕、外语文本或希望阅读视频内容时，可以使用该功能。支持多种语言，并提供带有时间戳的输出文件，以便用户能够同步阅读。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"🗨️","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# 字幕获取

通过 [TranscriptAPI.com](https://transcriptapi.com) 获取 YouTube 视频的字幕。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供 100 个信用点，无需信用卡）：

**步骤 1 — 注册：** 询问用户的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 系统会向用户的电子邮件发送 OTP（一次性密码）。询问用户：“请查看您的电子邮件以获取 6 位的验证码。”

**步骤 2 — 验证：** 用户提供 OTP 后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥会被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下面的 **文件写入** 部分。修改前会备份现有文件。

**手动注册方式：** [transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改前会备份现有文件到 `~/.openclaw/openclaw.json.bak`。

若要在终端/命令行（CLI）中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## 请求接口 `/api/v2/youtube/transcript`

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=false&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数                | 值                                      | 用途                                      |
| ------------------- | -------------------------------------- | -------------------------------------- |
| `video_url`          | YouTube 视频链接或视频 ID                         | 必填                                      |
| `format`            | `json` 或 `text`                              | `json` 用于获取带时间戳的字幕                   |
| `include_timestamp`     | `true` 或 `false`                              | `false` 用于获取纯文本（便于阅读/翻译）             |
| `send_metadata`     | `true` 或 `false`                              | 是否包含视频标题、频道和描述                        |

**用于语言学习**：选择纯文本（不包含时间戳）。

**用于翻译**：选择结构化的数据格式。

**响应格式：**

- **`format=json`**：包含视频的详细字幕信息（包括时间戳）。
- **`format=text`**：仅包含纯文本（不包含时间戳）。

**响应示例：**

（具体响应内容根据请求参数的不同而变化，此处省略。）

## 提示

- 许多视频支持多种语言的字幕。
- 使用 `format=json` 可以获取每行字幕的时间戳（适合同步阅读）。
- 使用 `include_timestamp=false` 可以获取纯文本，便于翻译软件使用。

## 错误代码及处理方式

| 错误代码 | 处理方式                                      |
| -------- | -------------------------------------- |
| 402    | 无足够的信用点 — 请联系 transcriptapi.com 客服            |
| 404    | 无法获取字幕                                   |
| 408    | 请求超时 — 请稍后重试（2 秒后再次尝试）                    |

每次请求消耗 1 个信用点。免费 tier 提供 100 个信用点，每分钟最多 300 次请求。