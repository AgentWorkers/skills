---
name: microsoft-teams
description: 通过 Microsoft Teams API 发送消息、管理频道以及自动化工作流程；在频道中发布内容、创建会议并管理团队成员资格。
metadata: {"clawdbot":{"emoji":"👥","requires":{"env":["TEAMS_WEBHOOK_URL"]}}}
---

# Microsoft Teams

用于团队协作和消息传递。

## Webhook（最简单的方式——无需身份验证）

```bash
# Post to channel via incoming webhook
curl -X POST "$TEAMS_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from automation!"}'
```

## 通过 Webhook 使用自适应卡片（Adaptive Cards）

```bash
curl -X POST "$TEAMS_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "message",
    "attachments": [{
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "body": [{"type": "TextBlock", "text": "Alert!", "weight": "bolder"}],
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.2"
      }
    }]
  }'
```

## Graph API（全权限访问）

需要使用 Azure AD 注册应用程序，并获得 Microsoft Graph 的相关权限。

```bash
export TEAMS_ACCESS_TOKEN="xxxxxxxxxx"

# List joined teams
curl "https://graph.microsoft.com/v1.0/me/joinedTeams" \
  -H "Authorization: Bearer $TEAMS_ACCESS_TOKEN"

# List channels
curl "https://graph.microsoft.com/v1.0/teams/{team-id}/channels" \
  -H "Authorization: Bearer $TEAMS_ACCESS_TOKEN"

# Send message to channel
curl -X POST "https://graph.microsoft.com/v1.0/teams/{team-id}/channels/{channel-id}/messages" \
  -H "Authorization: Bearer $TEAMS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"body": {"content": "Hello Teams!"}}'

# Create online meeting
curl -X POST "https://graph.microsoft.com/v1.0/me/onlineMeetings" \
  -H "Authorization: Bearer $TEAMS_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startDateTime": "2024-01-30T10:00:00Z", "endDateTime": "2024-01-30T11:00:00Z", "subject": "Quick Sync"}'
```

## 链接：
- 管理员：https://admin.teams.microsoft.com
- 文档：https://docs.microsoft.com/en-us/graph/api/resources/teams-api-overview