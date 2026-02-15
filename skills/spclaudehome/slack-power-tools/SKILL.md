---
name: slack-power-tools
description: 高级 Slack 自动化功能，超越了基本的消息传递功能。适用于需要管理频道（创建、归档、邀请用户）、安排消息发送、上传文件、搜索工作空间内容、管理用户组、设置用户状态/“请勿打扰”模式（DND）、获取分析数据，或自动化 Slack 工作流程的场景。涵盖频道操作、用户管理、定时消息发送、文件上传、搜索功能以及工作空间数据分析等方面。
---

# Slack 功能扩展工具

通过 Slack Web API 实现高级自动化操作。需要具备具有适当权限范围的 Slack Bot Token。

## 先决条件

```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
```

所需的 OAuth 权限范围取决于所使用的功能（请参阅各相关章节）。

## 频道管理

**权限范围：`channels:manage`, `channels:read`, `groups:write`, `groups:read`

### 列出所有频道
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel,private_channel&limit=200" | jq '.channels[] | {id, name, num_members, is_archived}'
```

### 创建频道
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "new-channel", "is_private": false}' \
  "https://slack.com/api/conversations.create" | jq '.'
```

### 将频道归档
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C123456"}' \
  "https://slack.com/api/conversations.archive"
```

### 设置频道主题/用途
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C123456", "topic": "Project X Discussion"}' \
  "https://slack.com/api/conversations.setTopic"

curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C123456", "purpose": "All things Project X"}' \
  "https://slack.com/api/conversations.setPurpose"
```

### 邀请用户加入频道
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C123456", "users": "U111,U222,U333"}' \
  "https://slack.com/api/conversations.invite"
```

### 将用户踢出频道
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C123456", "user": "U111"}' \
  "https://slack.com/api/conversations.kick"
```

## 计划发送消息

**权限范围：`chat:write`

### 计划发送消息
```bash
# post_at is Unix timestamp
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C123456",
    "text": "Reminder: Team standup in 15 minutes!",
    "post_at": 1735689600
  }' \
  "https://slack.com/api/chat.scheduleMessage" | jq '.'
```

### 查看已计划的消息
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/chat.scheduledMessages.list" | jq '.scheduled_messages[]'
```

### 删除已计划的消息
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel": "C123456", "scheduled_message_id": "Q123456"}' \
  "https://slack.com/api/chat.deleteScheduledMessage"
```

## 文件管理

**权限范围：`files:write`, `files:read`

### 上传文件
```bash
# Get upload URL
UPLOAD=$(curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/files.getUploadURLExternal?filename=report.pdf&length=$(stat -f%z report.pdf)")

UPLOAD_URL=$(echo $UPLOAD | jq -r '.upload_url')
FILE_ID=$(echo $UPLOAD | jq -r '.file_id')

# Upload file content
curl -s -X POST "$UPLOAD_URL" -F "file=@report.pdf"

# Complete upload and share to channel
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"files\": [{\"id\": \"$FILE_ID\"}], \"channel_id\": \"C123456\"}" \
  "https://slack.com/api/files.completeUploadExternal"
```

### 列出文件
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/files.list?channel=C123456&count=20" | jq '.files[] | {id, name, filetype, size, created}'
```

### 删除文件
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file": "F123456"}' \
  "https://slack.com/api/files.delete"
```

## 用户管理

**权限范围：`users:read`, `users.profile:write`

### 列出所有用户
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/users.list?limit=200" | jq '.members[] | select(.deleted==false) | {id, name, real_name, is_admin}'
```

### 获取用户信息
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/users.info?user=U123456" | jq '.user'
```

### 设置用户状态（适用于机器人/自身）
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "status_text": "In a meeting",
      "status_emoji": ":calendar:",
      "status_expiration": 1735693200
    }
  }' \
  "https://slack.com/api/users.profile.set"
```

## 用户组

**权限范围：`usergroups:write`, `usergroups:read`

### 列出用户组
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/usergroups.list?include_users=true" | jq '.usergroups[] | {id, handle, name, user_count}'
```

### 创建用户组
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Backend Team", "handle": "backend-team"}' \
  "https://slack.com/api/usergroups.create"
```

### 更新用户组成员
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"usergroup": "S123456", "users": "U111,U222,U333"}' \
  "https://slack.com/api/usergroups.users.update"
```

## 搜索

**权限范围：`search:read`

### 搜索消息
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/search.messages?query=project%20deadline&sort=timestamp&count=20" | jq '.messages.matches[] | {channel: .channel.name, user, text, ts}'
```

### 搜索文件
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/search.files?query=report%20Q4&count=20" | jq '.files.matches[] | {name, filetype, user}'
```

## 设置“请勿打扰”状态

**权限范围：`dnd:write`, `dnd:read`

### 设置“请勿打扰”状态
```bash
# Snooze for 60 minutes
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/dnd.setSnooze?num_minutes=60"
```

### 结束“请勿打扰”状态
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/dnd.endSnooze"
```

### 检查“请勿打扰”状态
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/dnd.info?user=U123456" | jq '.'
```

## 提醒功能

**权限范围：`reminders:write`, `reminders:read`

### 创建提醒
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Review PR #42",
    "time": "in 2 hours",
    "user": "U123456"
  }' \
  "https://slack.com/api/reminders.add"
```

### 查看提醒列表
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/reminders.list" | jq '.reminders[]'
```

## 分析与统计

### 频道消息数量（过去 7 天）
```bash
# Get channel history and count
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.history?channel=C123456&oldest=$(($(date +%s) - 604800))&limit=1000" | jq '.messages | length'
```

### 频道中最活跃的用户
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.history?channel=C123456&limit=1000" | jq '[.messages[].user] | group_by(.) | map({user: .[0], count: length}) | sort_by(-.count) | .[0:10]'
```

### 工作区统计信息
```bash
# Count total users
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/users.list" | jq '[.members[] | select(.deleted==false and .is_bot==false)] | length'

# Count channels
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&exclude_archived=true" | jq '.channels | length'
```

## 收藏夹

**权限范围：`bookmarks:write`, `bookmarks:read`

### 将频道添加到收藏夹
```bash
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "C123456",
    "title": "Project Wiki",
    "type": "link",
    "link": "https://wiki.company.com/project"
  }' \
  "https://slack.com/api/bookmarks.add"
```

### 查看收藏夹列表
```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/bookmarks.list?channel_id=C123456" | jq '.bookmarks[]'
```

## 常用工作流程

### 每日站会提醒（安排在上午 9 点）
```bash
# Calculate next 9 AM timestamp
NINE_AM=$(date -v+1d -v9H -v0M -v0S +%s)
curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"channel\": \"C123456\", \"text\": \"🌅 Good morning team! Time for standup.\nWhat did you do yesterday?\nWhat will you do today?\nAny blockers?\", \"post_at\": $NINE_AM}" \
  "https://slack.com/api/chat.scheduleMessage"
```

### 批量邀请用户加入新项目频道
```bash
# Create channel, set topic, invite team
CHANNEL=$(curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "project-phoenix"}' \
  "https://slack.com/api/conversations.create" | jq -r '.channel.id')

curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"channel\": \"$CHANNEL\", \"topic\": \"🔥 Project Phoenix - Q1 2026\"}" \
  "https://slack.com/api/conversations.setTopic"

curl -s -X POST -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"channel\": \"$CHANNEL\", \"users\": \"U111,U222,U333,U444\"}" \
  "https://slack.com/api/conversations.invite"
```

### 每周频道清理报告
```bash
echo "# Slack Cleanup Report"
echo "Generated: $(date)"
echo ""
echo "## Inactive Channels (no messages in 30 days)"
# List channels, check last message date
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&exclude_archived=true&limit=500" | \
  jq -r '.channels[] | "\(.id) \(.name)"' | while read id name; do
    last_msg=$(curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
      "https://slack.com/api/conversations.history?channel=$id&limit=1" | jq -r '.messages[0].ts // "0"')
    if [ $(echo "$last_msg < $(date -v-30d +%s)" | bc) -eq 1 ]; then
      echo "- #$name (last activity: $(date -r ${last_msg%.*} +%Y-%m-%d 2>/dev/null || echo 'never'))"
    fi
done
```

## 错误处理

所有 Slack API 响应都会包含 `ok: true/false`。错误信息如下：
```bash
response=$(curl -s ...)
if [ "$(echo $response | jq -r '.ok')" != "true" ]; then
  echo "Error: $(echo $response | jq -r '.error')"
fi
```

常见错误：
- `channel_not_found` - 频道 ID 无效
- `not_in_channel` - 机器人未进入该频道
- `missing_scope` - 需要额外的 OAuth 权限范围
- `ratelimited` - 请求次数过多，请查看 `Retry-After` 头部信息