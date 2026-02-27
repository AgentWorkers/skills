---
name: trakt-readonly
description: 这是一个只读的 Trakt.tv 技能（skill），用于通过 Trakt API 检查用户当前正在观看的内容、最近的剧集历史记录、已观看的剧集列表、用户信息以及播放进度（需要 OAuth 认证）。当用户询问自己的 Trakt 活动、观看状态或最近观看的剧集时，可以使用此技能。该技能需要用户的 Trakt 客户端 ID（Client ID）和用户名。
metadata: {"openclaw":{"requires":{"env":["TRAKT_CLIENT_ID","TRAKT_USERNAME"],"bins":["curl","jq"]},"primaryEnv":"TRAKT_CLIENT_ID","emoji":"📺"}}
---
# Trakt (OpenClaw) — 仅限读取

使用此技能通过 API 查询 Trakt.tv 的用户数据（仅限读取）。默认设置为 **仅限读取**；除非用户明确要求支持 OAuth，否则不要实现写入操作。

## 必需条件

- 环境变量：
  - `TRAKT_CLIENT_ID`（Trakt API 客户端 ID）
  - `TRAKT_USERNAME`（Trakt 用户名或用户别名）
  - `TRAKT_ACCESS_TOKEN`（OAuth 承载令牌，用于播放）
  - `TRAKT_CLIENT_SECRET`（用于设备令牌交换）
- 必需的二进制文件：`curl`、`jq`

## 命令（脚本）

使用 `{baseDir}/scripts/trakt-api.sh`。

- `watching` — 当前正在观看的电影/剧集
- `recent [limit]` — 最近观看的剧集记录（默认 10 条，最多 100 条）
- `watched-shows` — 最近观看的剧集列表
- `profile` — 用户个人资料
- `stats` — 用户统计信息
- `playback <type> <start_at> <end_at>` — 播放进度（需要 OAuth）

示例：

```
TRAKT_CLIENT_ID=xxx TRAKT_USERNAME=user {baseDir}/scripts/trakt-api.sh watching
TRAKT_CLIENT_ID=xxx TRAKT_USERNAME=user {baseDir}/scripts/trakt-api.sh recent 5
TRAKT_CLIENT_ID=xxx TRAKT_ACCESS_TOKEN=yyy {baseDir}/scripts/trakt-api.sh playback movies 2016-06-01T00:00:00.000Z 2016-07-01T23:59:59.000Z
TRAKT_CLIENT_ID=xxx {baseDir}/scripts/trakt-api.sh device-code
TRAKT_CLIENT_ID=xxx TRAKT_CLIENT_SECRET=zzz {baseDir}/scripts/trakt-api.sh device-token <device_code>
```

## 安全规范

- 绝不要记录或泄露 API 密钥或访问令牌。
- 仅调用 `https://api.trakt.tv`。
- 仅使用仅限读取的 API 端点；播放功能需要 OAuth 令牌的读取权限。
- 设备的 OAuth 流程也仅限读取；不要请求写入权限。
- 确保 `recent` 参数的值是数字，并且在 1 到 100 之间。
- 优雅地处理空响应或 404 错误（需要显示用户个人资料）。

## 参考资料

- 请参阅 `references/trakt-api.md` 以获取 API 端点、请求头和身份验证的相关信息。