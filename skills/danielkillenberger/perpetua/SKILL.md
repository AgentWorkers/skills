---
name: perpetua
description: "**OAuth代理**：通过`Perpetua.sh`托管的API，使用单一API密钥调用外部API（如Oura、Google Calendar等）。适用于获取Oura数据、Google Calendar事件或管理OAuth连接。"
version: "1.0.0"
read_when:
  - User asks about Oura Ring data (sleep, readiness, activity, workouts, HRV)
  - User asks about Google Calendar events or schedule
  - User wants to add or manage OAuth provider connections
  - Perpetua proxy setup or troubleshooting
  - User asks what's on their calendar or how they slept
triggers:
  - oura
  - sleep score
  - readiness score
  - hrv
  - perpetua
  - oauth proxy
  - calendar
  - google calendar
metadata:
  {
    "openclaw":
      {
        "emoji": "🔑",
        "kind": "service",
        "notes": "Primary endpoint is hosted Perpetua.sh API at https://www.perpetua.sh/api."
      }
  }
---
# Perpetua Skill（托管版）

## 概述

使用 **Perpetua.sh 托管 API** 作为默认访问路径：

- 基本 URL：`https://www.perpetua.sh`
- API 路由：`/api/*`
- 认证方式：`Authorization: Bearer $PERPETUA_API_KEY`

通过以下方式加载秘钥：

```bash
op run --env-file="$HOME/.openclaw/secrets.env" -- <command>
```

## 凭据

通过环境变量（来自 1Password、CI、`.env` 文件或密钥管理工具）设置 API 密钥：

```bash
export PERPETUA_API_KEY="<your-key>"
```

## 核心接口（托管版）

```bash
# Connection status summary
curl -s "https://www.perpetua.sh/api/status" \
  -H "Authorization: Bearer $PERPETUA_API_KEY"

# Active connections
curl -s "https://www.perpetua.sh/api/connections" \
  -H "Authorization: Bearer $PERPETUA_API_KEY"

# Providers
curl -s "https://www.perpetua.sh/api/providers" \
  -H "Authorization: Bearer $PERPETUA_API_KEY"
```

## 代理调用模式

```bash
GET https://www.perpetua.sh/api/proxy/:provider/:path
Authorization: Bearer $PERPETUA_API_KEY
```

可选参数：`?account=default` 用于明确指定账户。

### Oura 示例

> 除非有特殊需求，否则避免使用大型接口（如 `daily_activity`、`sleep`）。

```bash
# Daily sleep
curl -s "https://www.perpetua.sh/api/proxy/oura/v2/usercollection/daily_sleep?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&account=default" \
  -H "Authorization: Bearer $PERPETUA_API_KEY" | jq .

# Daily readiness
curl -s "https://www.perpetua.sh/api/proxy/oura/v2/usercollection/daily_readiness?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&account=default" \
  -H "Authorization: Bearer $PERPETUA_API_KEY" | jq .

# Workout
curl -s "https://www.perpetua.sh/api/proxy/oura/v2/usercollection/workout?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&account=default" \
  -H "Authorization: Bearer $PERPETUA_API_KEY" | jq .
```

### Google 日历示例

```bash
# Upcoming primary calendar events
curl -s "https://www.perpetua.sh/api/proxy/gcal/calendars/primary/events?account=default&maxResults=10&orderBy=startTime&singleEvents=true&timeMin=$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  -H "Authorization: Bearer $PERPETUA_API_KEY" | jq '[.items[] | {summary, start}]'

# Calendar list
curl -s "https://www.perpetua.sh/api/proxy/gcal/users/me/calendarList?account=default" \
  -H "Authorization: Bearer $PERPETUA_API_KEY" | jq .
```

## 连接管理（托管版）

```bash
# Start OAuth flow for provider
curl -s -X POST "https://www.perpetua.sh/api/auth/connect/:provider/start" \
  -H "Authorization: Bearer $PERPETUA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"account":"default"}' | jq .authUrl
```

## 故障排除

- `401`：API 密钥错误或已过期
- `403/404`：连接丢失或提供的服务/账户信息错误
- `5xx`：托管服务出现故障；请重试或联系 Daniel

## 本地开发环境说明

本地开发环境使用 `http://localhost:3001`。该工作空间的默认操作路径为托管版的 Perpetua.sh。