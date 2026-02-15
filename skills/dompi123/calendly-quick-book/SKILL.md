---
name: calendly-quick-book
description: 立即通过 Calendly 预订会议。当用户执行“book”、“schedule calendly”、“calendly book”或任何与预订会议相关的操作时，系统会自动触发该功能，而无需发送会议链接。
user-invocable: true
metadata: {"openclaw": {"always": true, "emoji": "📅", "requires": {"env": ["CALENDLY_API_TOKEN"]}}}
---

# Calendly 快速预约功能

通过自然语言即可预约 Calendly 会议，无需切换标签页或发送链接。

## 默认配置

| 设置 | 值 |
|---------|-------|
| Calendly 默认链接 | https://calendly.com/你的用户名 |
| Calendly 用户名 | 你的用户名 |

**注意：** 安装完成后，请将上述值替换为你的实际 Calendly 用户名。

## 命令

| 输入 | 动作 |
|-------|--------|
| `book [会议名称] [电子邮件] [时区] [时间]` | 预约会议 |
| `calendly book [会议名称] [电子邮件] [时区] [时间]` | 预约会议 |

## 输入字段

| 字段 | 是否必填 | 示例 |
|-------|----------|---------|
| 会议名称 | 是 | John Smith |
| 电子邮件 | 是 | john@acme.com |
| 时区 | 是 | EST, PST, UTC |
| 时间 | 是 | 明天下午 2 点 |

## 时区映射

| 输入 | IANA 格式 |  
|-------|-------------|
| EST/EDT | America/New_York |  
| CST/CDT | America/Chicago |  
| MST/MDT | America/Denver |  
| PST/PDT | America/Los_Angeles |  
| GMT/UTC | UTC |  

## API 工作流程

### 第一步：获取当前用户信息

```bash
curl -s "https://api.calendly.com/users/me" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"
```

### 第二步：获取可用的会议类型

```bash
curl -s "https://api.calendly.com/event_types?user={USER_URI}" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"
```

### 第三步：获取可用时间

```bash
curl -s "https://api.calendly.com/event_type_available_times?event_type={EVENT_TYPE_URI}&start_time={START_UTC}&end_time={END_UTC}" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN"
```

### 第四步：创建预约

```bash
curl -s -X POST "https://api.calendly.com/invitees" \
  -H "Authorization: Bearer $CALENDLY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "{EVENT_TYPE_URI}",
    "start_time": "{TIME_UTC}",
    "invitee": {
      "name": "{NAME}",
      "email": "{EMAIL}",
      "timezone": "{TIMEZONE_IANA}"
    }
  }'
```

## 响应格式

### 预约成功
```
✅ Meeting Booked!

📅 [Date]
⏰ [Time] [Timezone]
👤 [Name] ([Email])
📍 Calendar invite sent automatically
```

### 无法预约
```
⚠️ No availability at [time]

Nearest slots:
1. [Option 1]
2. [Option 2]
3. [Option 3]
```

### 错误信息

| 错误类型 | 响应内容 |
|-------|----------|
| 电子邮件无效 | 请确认电子邮件地址 |
| 令牌过期 | 请前往 Calendly 设置页面更新令牌 |
| 无可用会议类型 | 请在 Calendly 中创建新的会议类型 |