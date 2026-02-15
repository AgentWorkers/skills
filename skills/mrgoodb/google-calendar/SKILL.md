---
name: google-calendar
description: 管理 Google 日历事件：创建、列出、更新和删除事件。适用于需要查看日程安排、安排会议或自动化日历管理的场景。使用前需完成 OAuth2 设置。
---

# Google 日历 API

通过 Google 日历 API 管理日历事件。

## 设置（OAuth2）

1. 创建项目：https://console.cloud.google.com
2. 启用日历 API：APIs & Services → Enable APIs → Google 日历 API
3. 创建 OAuth 凭据：APIs & Services → Credentials → Create OAuth 客户端 ID
4. 下载 JSON 文件，并将其保存为 `~/.config/google/credentials.json`
5. 使用 OAuth2 流程获取刷新令牌（详见下方）

## 快速认证（使用 gcalcli）

使用 gcalcli 的最简单设置方法：
```bash
pip install gcalcli
gcalcli init  # Opens browser for OAuth
```

或者使用 gcloud：
```bash
gcloud auth application-default login --scopes=https://www.googleapis.com/auth/calendar
```

## API 基础知识

```bash
ACCESS_TOKEN=$(gcloud auth application-default print-access-token)

curl -s "https://www.googleapis.com/calendar/v3/users/me/calendarList" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[] | {id, summary}'
```

## 列出日历

```bash
curl -s "https://www.googleapis.com/calendar/v3/users/me/calendarList" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[] | {id, summary}'
```

主日历 ID 通常为你的电子邮件地址或 `primary`。

## 列出事件

```bash
CALENDAR_ID="primary"
TIME_MIN=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
TIME_MAX=$(date -u -d "+7 days" +"%Y-%m-%dT%H:%M:%SZ")

curl -s "https://www.googleapis.com/calendar/v3/calendars/${CALENDAR_ID}/events?timeMin=${TIME_MIN}&timeMax=${TIME_MAX}&singleEvents=true&orderBy=startTime" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[] | {summary, start: .start.dateTime, end: .end.dateTime}'
```

## 获取今日事件

```bash
TODAY=$(date -u +"%Y-%m-%dT00:00:00Z")
TOMORROW=$(date -u -d "+1 day" +"%Y-%m-%dT00:00:00Z")

curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin=${TODAY}&timeMax=${TOMORROW}&singleEvents=true&orderBy=startTime" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[] | {summary, start: .start.dateTime}'
```

## 创建事件

```bash
curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Meeting Title",
    "description": "Meeting description",
    "start": {
      "dateTime": "2024-01-15T10:00:00",
      "timeZone": "Europe/Paris"
    },
    "end": {
      "dateTime": "2024-01-15T11:00:00",
      "timeZone": "Europe/Paris"
    }
  }' | jq '{id, summary, htmlLink}'
```

## 创建包含参与者的事件

```bash
curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events?sendUpdates=all" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Team Meeting",
    "start": {"dateTime": "2024-01-15T14:00:00", "timeZone": "Europe/Paris"},
    "end": {"dateTime": "2024-01-15T15:00:00", "timeZone": "Europe/Paris"},
    "attendees": [
      {"email": "person1@example.com"},
      {"email": "person2@example.com"}
    ],
    "conferenceData": {
      "createRequest": {"requestId": "meet-'$(date +%s)'"}
    }
  }' | jq
```

添加 `sendUpdates=all` 以发送电子邮件邀请。

## 创建全天事件

```bash
curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Holiday",
    "start": {"date": "2024-01-15"},
    "end": {"date": "2024-01-16"}
  }'
```

对于全天事件，请使用 `date`（而非 `dateTime`）。

## 更新事件

```bash
EVENT_ID="event_id_here"

curl -s -X PATCH "https://www.googleapis.com/calendar/v3/calendars/primary/events/${EVENT_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Updated Title",
    "description": "Updated description"
  }'
```

## 删除事件

```bash
curl -s -X DELETE "https://www.googleapis.com/calendar/v3/calendars/primary/events/${EVENT_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

## 添加 Google Meet

```bash
curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events?conferenceDataVersion=1" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Video Call",
    "start": {"dateTime": "2024-01-15T10:00:00", "timeZone": "Europe/Paris"},
    "end": {"dateTime": "2024-01-15T11:00:00", "timeZone": "Europe/Paris"},
    "conferenceData": {
      "createRequest": {
        "requestId": "'$(uuidgen)'",
        "conferenceSolutionKey": {"type": "hangoutsMeet"}
      }
    }
  }' | jq '.conferenceData.entryPoints[0].uri'
```

## 查询空闲/忙碌状态

```bash
curl -s -X POST "https://www.googleapis.com/calendar/v3/freeBusy" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "timeMin": "2024-01-15T00:00:00Z",
    "timeMax": "2024-01-15T23:59:59Z",
    "items": [{"id": "primary"}]
  }' | jq '.calendars.primary.busy'
```

## 快速添加事件（通过自然语言）

```bash
curl -s -X POST "https://www.googleapis.com/calendar/v3/calendars/primary/events/quickAdd?text=Lunch%20with%20John%20tomorrow%20at%20noon" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq
```

## 速率限制

- 每天 1,000,000 次请求（默认值）
- 每用户每 100 秒 100 次请求