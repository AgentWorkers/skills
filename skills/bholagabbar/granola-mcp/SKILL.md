---
name: granola
description: 通过 MCP (mcporter) 访问 Granola AI 的会议记录。可以查询会议信息、按日期范围筛选会议记录、查看详细内容以及获取会议的逐字记录。当用户询问会议记录、讨论内容、行动项、决策等会议相关事宜时，可以使用该工具。此外，该工具还能在认证失败导致调用失败时处理 OAuth 令牌的刷新问题。
metadata:
  openclaw:
    requires:
      bins: [mcporter, bash, curl, python3]
    config:
      - path: config/granola_oauth.json
        description: "OAuth credentials: client_id, refresh_token, access_token, token_endpoint (from Granola MCP auth flow)"
      - path: config/mcporter.json
        description: "MCP server config with bearer token header for Granola API"
---
# Granola MCP

会议记录可通过 `mcporter call granola.<tool>` 进行查询。

## 工具

```
granola.query_granola_meetings  query=<string> [document_ids=<uuid[]>]
granola.list_meetings           [time_range=this_week|last_week|last_30_days|custom] [custom_start=<ISO>] [custom_end=<ISO>]
granola.get_meetings            meeting_ids=<uuid[]>  (max 10)
granola.get_meeting_transcript  meeting_id=<uuid>
```

## 使用模式

1. 对于开放式问题（例如：“我们讨论了X的哪些内容？”），使用 `query_granola_meetings`。
2. 要列出指定时间范围内的会议，请使用 `list_meetings`。
3. 要获取特定会议的详细信息，请使用 `get_meetings` 并传入 `list_meetings` 的结果中的会议ID。
4. 要获取会议的完整文本或逐字记录，请使用 `get_meeting_transcript`。

对于自然语言问题，建议使用 `query_granola_meetings`，因为它比 `list_meetings` 后再使用 `get` 更简洁。响应中会包含引用链接（例如 `[[0]](url)`），请在回复中保留这些链接，以便用户可以点击查看原始会议记录。

## 设置

1. 完成在 `https://mcp-auth.granola.ai/oauth2/authorize` 的Granola OAuth认证流程。
2. 将认证凭据保存到 `config/granola.oauth.json` 文件中，其中包含以下键：`client_id`、`refresh_token`、`access_token`、`token_endpoint`。
3. 在 `config/mcporter.json` 中配置Granola MCP服务器的相关信息，并设置 `Authorization: Bearer <token>` 头部。
4. （可选）设置定时任务（cron job）定期运行 `scripts/refresh_token.sh` 脚本，因为OAuth令牌大约每6小时会过期一次。

## 认证与令牌刷新

**如果调用失败并出现401/认证错误：**

```bash
bash {baseDir}/scripts/refresh_token.sh
```

脚本会读取 `config/granola.oauth.json` 文件，向令牌端点（`https://mcp-auth.granola.ai/oauth2/token`）发送请求，并用新的访问令牌更新 `config/granola.oauth.json` 和 `config/mcporter.json` 文件。

然后尝试重新调用该接口。如果刷新令牌仍然失败，用户需要通过上述OAuth认证流程重新进行认证。

## 配置文件

- `config/granola.oauth.json` — OAuth认证凭据（`client_id`、`refresh_token`、`access_token`、`token_endpoint`）。**包含机密信息；请勿提交到代码仓库。**
- `config/mcporter.json` — 包含MCP服务器配置信息及`Bearer`令牌头部。**包含机密信息；请勿提交到代码仓库。**