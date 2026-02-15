---
name: youtube-api
description: 无需担心官方API配额的限制，即可访问YouTube API的功能——包括获取视频字幕、搜索结果、频道信息、播放列表以及元数据，且完全不需要使用Google API密钥。适用于需要以编程方式获取YouTube数据、希望避免使用Google API配额的用户，或者那些搜索“youtube api”、“get video data”、“youtube without api key”或“no quota youtube”的用户。
homepage: https://transcriptapi.com
user-invocable: true
metadata: {"openclaw":{"emoji":"⚡","requires":{"env":["TRANSCRIPT_API_KEY"],"bins":["node"],"config":["~/.openclaw/openclaw.json"]},"primaryEnv":"TRANSCRIPT_API_KEY"}}
---

# YouTube API

可以通过 [TranscriptAPI.com](https://transcriptapi.com) 访问 YouTube 数据——无需使用 Google API 的配额。

## 设置

如果 `$TRANSCRIPT_API_KEY` 未设置，请帮助用户创建一个账户（免费提供 100 个信用额度，无需使用信用卡）：

**步骤 1 — 注册：** 询问用户的电子邮件地址。

```bash
node ./scripts/tapi-auth.js register --email USER_EMAIL
```

→ 会向用户的电子邮件发送 OTP（一次性密码）。然后询问用户：“请查看您的电子邮件以获取 6 位数的验证码。”

**步骤 2 — 验证：** 用户提供 OTP 后：

```bash
node ./scripts/tapi-auth.js verify --token TOKEN_FROM_STEP_1 --otp CODE
```

> API 密钥将被保存到 `~/.openclaw/openclaw.json` 文件中。具体操作请参阅下面的 **文件写入** 部分。修改文件之前会先备份原有文件。

手动注册方式：[transcriptapi.com/signup](https://transcriptapi.com/signup) → 仪表板 → API 密钥。

## 文件写入

`verify` 和 `save-key` 命令会将 API 密钥保存到 `~/.openclaw/openclaw.json` 文件中（同时设置 `skills.entries.transcriptapi.apiKey` 为该密钥，并将 `enabled` 设置为 `true`）。修改文件之前，原有文件会被备份到 `~/.openclaw/openclaw.json.bak`。

若要在终端/CLI 中使用该 API 密钥，请手动将其添加到您的 shell 配置文件中：
`export TRANSCRIPT_API_KEY=<your-key>`

## API 参考

完整的 OpenAPI 规范：[transcriptapi.com/openapi.json](https://transcriptapi.com/openapi.json) — 请查阅此处以获取最新的参数和数据结构信息。

## 端点参考

所有端点的地址为：`https://transcriptapi.com/api/v2/youtube/...`

- **频道相关端点** 接受以下参数：`channel` — 节目处理程序（`@handle`）、频道 URL 或 `UC...` ID。
- **播放列表相关端点** 接受以下参数：`playlist` — 播放列表 URL 或 ID。

| 端点                            | 方法      | 费用     |
| ----------------------------------- | -------- | -------- |
| `/transcript?video_url=ID`          | GET    | 1        |
| `/search?q=QUERY&type=video`        | GET    | 1        |
| `/channel/resolve?input=@handle`    | GET    | **免费**     |
| `/channel/latest?channel=@handle`   | GET    | **免费**     |
| `/channel/videos?channel=@handle`   | GET    | 1/页     |
| `/channel/search?channel=@handle&q=Q` | GET    | 1        |
| `/playlist/videos?playlist=PL_ID`   | GET    | 1/页     |

## 快速示例

- **搜索视频：**
  ```bash
curl -s "https://transcriptapi.com/api/v2/youtube/search\
?q=python+tutorial&type=video&limit=10" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

- **获取字幕：**
  ```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript\
?video_url=dQw4w9WgXcQ&format=text&include_timestamp=true&send_metadata=true" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

- **解析频道处理程序（免费）：**
  ```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/resolve?input=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

- **获取最新视频（免费）：**
  ```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/latest?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

- **浏览频道上传内容（分页显示）：**
  ```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?channel=@NASA" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
# Use continuation token from response for next pages
```

- **浏览播放列表（分页显示）：**
  ```bash
curl -s "https://transcriptapi.com/api/v2/youtube/playlist/videos?playlist=PL_PLAYLIST_ID" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

## 参数验证

| 参数            | 规则                                                         |
| ------------------------- | --------------------------------------------------------- |
| `channel`        | 节目处理程序（`@handle`）、频道 URL 或 `UC...` ID                           |
| `playlist`       | 播放列表 URL 或 ID（前缀为 `PL`/`UU`/`LL`/`FL`/`OL`）                         |
| `q`            | 需要搜索的文本（长度限制为 1-200 个字符）                                      |
| `limit`         | 每次请求的最大结果数量（1-50 个）                                      |
| `continuation`    | 用于分页请求的连续标识符（非空字符串）                             |

## 为什么选择 TranscriptAPI 而不是 Google 的 API？

|                | Google YouTube Data API         | TranscriptAPI              |
| ------------------------- | -------------------------- |
| 配额限制        | 每天 10,000 次请求（100 次搜索）                             | 基于信用额度，无每日上限          |
| 设置要求        | 需要 OAuth 认证、API 密钥及项目配置                        | 仅需一个 API 密钥                |
| 字幕功能        | 不提供字幕服务                                        | TranscriptAPI 提供核心字幕功能         |
| 价格            | 超量使用费用为每单位 0.0015 美元                              | 每 1000 个信用额度收费 5 美元          |

## 错误代码及说明

| 代码            | 错误含义                          | 处理方式                                      |
| ------------------------- | ----------------------------------------- | -------------------------------------------------------- |
| 401            | API 密钥无效                        | 请检查 API 密钥是否正确                          |
| 402            | 信用额度不足                        | 访问 [transcriptapi.com/billing](https://transcriptapi.com/billing) 查看计费信息     |
| 404            | 资源未找到                        | 请确认资源是否存在                         |
| 408            | 请求超时或可重试                      | 2 秒后尝试再次请求                         |
| 422            | 参数格式错误                        | 请检查输入参数的格式                         |
| 429            | 请求频率受限                        | 请稍后尝试或遵守请求间隔限制                         |

**免费 tier：** 提供 100 个信用额度，每分钟 300 次请求。  
**高级 tier（每月 5 美元）：** 提供 1,000 个信用额度。