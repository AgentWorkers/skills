---
name: donotify
description: 您可以使用 DoNotify 功能立即发送语音通话提醒，或安排未来的通话。
version: 1.0.1
homepage: https://donotifys.com/openclaw
permissions:
  - network:outbound
requires:
  env:
    - DONOTIFY_API_TOKEN
    - DONOTIFY_URL
metadata: {"openclaw":{"requires":{"env":["DONOTIFY_API_TOKEN","DONOTIFY_URL"]},"primaryEnv":"DONOTIFY_API_TOKEN"}}
---
# DoNotify Skill

您可以通过 DoNotify API 发送即时的语音提醒或安排未来的通话。

## 认证

所有请求都需要满足以下条件：
- 请求头：`Authorization: Bearer $DONOTIFY_API_TOKEN`
- 请求头：`Accept: application/json`
- 基本 URL：`$DONOTIFY_URL`（默认值：`https://donotifys.com`）

## 端点

### 检查使用情况

检查用户的套餐、剩余通知数量以及电话号码的状态。

```
GET $DONOTIFY_URL/api/usage
```

响应：
```json
{
  "plan": "starter",
  "notification_limit": 30,
  "used_this_month": 5,
  "remaining": 25,
  "phone_number_set": true
}
```

在拨打电话之前，请确保 `phone_number_set` 为 `true` 且 `remaining` 大于 0。如果电话号码未设置，请告知用户在 DoNotify 配置文件中设置它。

### 立即通话

立即拨打用户的电话。

```
POST $DONOTIFY_URL/api/call-now
Content-Type: application/json

{
  "title": "Pick up groceries",
  "description": "Milk, eggs, bread from Trader Joe's"
}
```

参数：
- `title`（必填，字符串，最长 255 个字符）——通话的内容。这部分内容会通过语音播放给用户听。
- `description`（可选，字符串，最长 1000 个字符）——在通话中补充说明的额外信息。

成功响应：
```json
{
  "success": true,
  "reminder_id": 42,
  "call_uuid": "abc-123",
  "status": "completed"
}
```

错误响应（422：未设置电话号码；500：通话失败）：
```json
{
  "success": false,
  "reminder_id": 42,
  "error": "Phone number not configured. Update your profile first.",
  "status": "failed"
}
```

### 安排提醒

安排在未来某个时间进行语音通话。

```
POST $DONOTIFY_URL/api/reminders
Content-Type: application/json

{
  "title": "Team standup",
  "call_at": "2025-06-15T14:45:00Z",
  "description": "Prepare sprint update",
  "event_time": "2025-06-15T15:00:00Z"
}
```

参数：
- `title`（必填，字符串，最长 255 个字符）——通话中的提醒主题。
- `call_at`（必填，ISO 8601 格式的日期时间，必须是未来的时间）——通话的具体时间。
- `description`（可选，字符串，最长 1000 个字符）——额外的详细信息。
- `event_time`（可选，ISO 8601 格式的日期时间）——实际事件发生的时间（如果与通话时间不同）。

成功响应（201）：
```json
{
  "success": true,
  "reminder": {
    "id": 43,
    "title": "Team standup",
    "description": "Prepare sprint update",
    "call_at": "2025-06-15T14:45:00+00:00",
    "event_time": "2025-06-15T15:00:00+00:00",
    "status": "pending"
  }
}
```

## 行为准则

- 当用户说“现在就给我打电话关于 X”或“马上提醒我关于 X”时，使用 **Call Now** 端点。
- 当用户说“在 [时间] 提醒我关于 X”或“在 [时间] 打电话给我关于 X”时，使用 **Schedule Reminder** 端点。请将用户提供的自然语言时间转换为 ISO 8601 格式。
- 当用户询问“我还剩下多少条提醒”或“查看我的使用情况”时，使用 **Usage** 端点。
- 如果不确定用户是否有剩余的通知，请先检查使用情况。
- 如果 `phone_number_set` 为 `false`，请告知用户在拨打电话前先在 DoNotify 配置页面中设置电话号码。
- 请确保提醒主题简洁明了——这些主题会在通话过程中被大声读出。