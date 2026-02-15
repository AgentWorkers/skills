---
name: transcript
description: 从任何YouTube视频中获取文字记录——可用于总结、研究、翻译、引用或内容分析。当用户分享视频链接，或者询问“他们说了什么”、“获取视频的文字记录”、“将这个视频转录成文字”或希望分析视频中的语音内容时，都可以使用该功能。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"📝","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# 文本转录

通过 [TranscriptAPI.com](https://transcriptapi.com) 获取视频字幕。

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

> API 密钥将保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参见下面的 **文件写入** 部分。修改前会备份现有文件。

**手动注册方式：** [transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改前会将现有文件备份到 `~/.openclaw/openclaw.json.bak`。

若要在代理程序之外的终端/命令行（CLI）中使用该 API 密钥，请手动将其添加到 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## 请求接口 `/api/v2/youtube/transcript`

```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=VIDEO_URL&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

| 参数               | 是否必填 | 默认值 | 可选值                          |
| ------------------- | -------- | ------- | ------------------------------- |
| `video_url`         | 是      | —       | YouTube 视频链接或 11 位的视频 ID             |
| `format`            | 否       | `json`  | `json` 或 `text`                     |
| `include_timestamp` | 否       | `true`  | `true` 或 `false`                     |
| `send_metadata`     | 否       | `false` | `true` 或 `false`                     |

支持的输入格式：完整的 YouTube 链接（`youtube.com/watch?v=ID`）、简短链接（`youtu.be/ID`）、YouTube 短视频链接（`youtube.com/shorts/ID`）或仅包含视频 ID 的字符串。

**默认设置：** 除非用户另有指定，否则始终使用 `format=text&include_timestamp=true&send_metadata=true`。

**响应格式：**  
- **`format=json`**  
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": [
    { "text": "We're no strangers to love", "start": 18.0, "duration": 3.5 },
    { "text": "You know the rules and so do I", "start": 21.5, "duration": 2.8 }
  ],
  "metadata": {
    "title": "Rick Astley - Never Gonna Give You Up",
    "author_name": "Rick Astley",
    "author_url": "https://www.youtube.com/@RickAstley",
    "thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"
  }
}
```

- **`format=text`**  
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "transcript": "[00:00:18] We're no strangers to love\n[00:00:21] You know the rules...",
  "metadata": {...}
}
```

## 错误代码及处理方式

| 错误代码 | 错误原因 | 处理方式                          |
| -------- | ------------- | ----------------------------------- |
| 401     | API 密钥无效 | 请检查密钥或重新设置 API 密钥                |
| 402     | 信用点不足 | 请访问 transcriptapi.com/billing 进行充值          |
| 404     | 无法获取字幕   | 视频可能未启用字幕功能                   |
| 408     | 超时     | 2 秒后重试                        |
| 429     | 请求次数过多 | 请稍后重试                        |

## 使用建议：

- 对于较长的视频，可以先总结关键内容，根据用户需求提供完整字幕。
- 当需要精确的时间戳来引用视频中的特定片段时，使用 `format=json`。
- 若需要用于翻译或分析的纯文本，可将 `include_timestamp` 设置为 `false`。
- 每次成功请求消耗 1 个信用点。错误请求不会消耗信用点。
- 免费套餐提供 100 个信用点，每分钟最多 300 次请求。