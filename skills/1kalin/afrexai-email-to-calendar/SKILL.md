---
name: afrexai-email-to-calendar
version: 1.0.0
description: >
  Extract calendar events, deadlines, action items, and follow-ups from emails.
  Works with any calendar provider (Google, Outlook, Apple, Notion, etc.).
  No external dependencies — pure agent intelligence.
  Use when the user forwards an email, asks to check inbox for events,
  or wants to extract structured scheduling data from any text.
---

# 邮件到日历提取引擎

将电子邮件转换为结构化的日历事件，确保不会错过任何截止日期。

## 快速入门

当您收到电子邮件（无论是转发的、粘贴的还是来自收件箱的）时，请按照以下步骤操作：

1. **解析** — 使用以下框架提取所有与时间相关的信息。
2. **分类** — 根据类型和置信度对每个信息进行评分。
3. **展示** — 以结构化的方式展示结果，并提供可选的标记选项。
4. **创建** — 使用用户的日历工具创建已确认的事件。
5. **跟进** — 跟踪截止日期并发送提醒。

---

## 1. 提取框架

### 需要关注的类别

在每封电子邮件中查找以下所有类别的信息：

| 类别 | 识别信号 | 优先级 |
|----------|---------|----------|
| **固定事件** | “在……时间开会”、“请……联系我”、“……日期的活动” | 🔴 高优先级 |
| **截止日期** | “必须在……之前完成”、“请在……之前提交”、“请在……之前回复”、“截止日期为……” | 🔴 高优先级 |
| **非固定事件** | “下周的某个时间”、“我们尽快见面吧”、“计划于三月……” | 🟡 中等优先级 |
| **重复事件** | “每周一”、“每月一次”、“定期会议” | 🟡 中等优先级 |
| **待办事项** | “请查看”、“你能发送……吗”、“需要跟进” | 🟡 中等优先级 |
| **旅行/物流信息** | 航班号、酒店确认信息、入住/退房时间、登机口信息 | 🔴 高优先级 |
| **隐含的截止日期** | 如果活动日期是2月20日，则机票的截止日期可能在1-2周前 | 🟡 中等优先级 |

### 提取模板

对于找到的每个信息，使用以下模板进行提取：

```yaml
- title: "Descriptive name (max 80 chars)"
  type: event | deadline | action_item | travel | recurring
  date: "YYYY-MM-DD"
  day_of_week: "Monday"  # Always include for verification
  time_start: "14:00"    # 24h format, default 09:00 if unclear
  time_end: "15:00"      # Default: start + 1h for meetings, all-day for deadlines
  timezone: "America/New_York"  # Extract from email headers or content
  is_all_day: false
  is_multi_day: false     # If true, include end_date
  end_date: null
  recurrence: null        # "weekly" | "biweekly" | "monthly" | "MWF" | custom RRULE
  location: null          # Physical address or video link
  url: null               # Registration link, event page, or action URL
  attendees: []           # Names/emails mentioned
  confidence: high | medium | low
  source_quote: "exact text from email that indicates this event"
  notes: "any context the user should know"
  deadline_action: null   # "RSVP" | "register" | "buy tickets" | "submit"
  deadline_url: null      # Direct link to take action
  reminder_minutes: 30    # Suggested reminder (15 for calls, 60 for travel, 1440 for deadlines)
```

### 置信度评分

| 置信度 | 评分标准 |
|------------|----------|
| **高** | 明确的日期和时间以及具体的活动类型。例如：“2月15日下午2点的会议” |
| **中** | 有日期但没有时间，或者有时间但日期不准确。例如：“下周二下午” |
| **低** | 描述模糊。例如：“我们应该尽快见面” |

### 智能默认值

- **会议时间未提供** → 设定为09:00-10:00（置信度：中等）
- **截止日期未提供** → 设定为23:59（当天结束）
- **未指定时区** → 使用用户的默认时区（请注意这只是一个假设）
- **“上午”** → 设定为09:00，**“下午”** → 设定为14:00，**“晚上”** → 设定为18:00，**“当天结束”** → 设定为17:00
- **“下周”** → 设定为下周一（置信度：中等）
- **多日事件** → 将`is_multi_day`设置为`true`，并包含开始和结束日期

---

## 2. 邮件分类

在提取信息之前，先对邮件进行分类：

| 邮件类型 | 处理方式 |
|------------|---------------|
| **日历通知**（来自calendar-notification@google.com、Outlook等） | 跳过——这些是对已有事件的回复 |
| **新闻通讯/营销邮件** | 仅提取包含相关活动日期的内容 |
| **个人/工作邮件** | 全部提取信息 |
| **旅行确认邮件** | 提取所有旅行相关信息：航班、酒店、租车、入住信息 |
| **会议邀请**（ICS附件或结构化邀请） | 直接提取，置信度较高 |
| **主题邮件/回复邮件** | 仅提取新的事件，不处理引用文本中的事件 |
| **转发邮件** | 处理转发的内容，并注明原始发送者 |

### 忽略的邮件类型

- 自动化的日历回复（如“已接受”、“已拒绝”、“待定”）
- 取消订阅确认邮件
- 阅读回执邮件
- 自动回复邮件/邮件作者不在办公
- 垃圾邮件/促销邮件（除非用户明确转发）

---

## 3. 展示格式

始终以以下格式展示提取的信息：

```
📧 From: [sender] | Subject: [subject] | Date: [received date]

Found [N] calendar items:

1. 🔴 **Team Standup** — Mon Feb 17, 9:00-9:30 AM EST
   📍 Zoom (link in email) | 👥 Alice, Bob, Charlie
   🔁 Recurring: Every weekday
   ✅ Confidence: High

2. 🔴 **Project Deadline: Q1 Report** — Fri Feb 28, EOD
   ⚠️ ACTION REQUIRED: Submit report
   🔗 [Submission portal](url)
   ⏰ Suggested reminder: 3 days before
   ✅ Confidence: High

3. 🟡 **Team Lunch** — "sometime next week"
   📍 TBD
   ⚠️ Confidence: Medium — date needs confirmation

---
Reply with numbers to create (e.g. "1, 2"), "all", or "none".
Type "edit 3" to modify before creating.
```

### 展示规则

1. **始终显示星期几** — 人类通常通过星期几来验证日期。
2. **当有多个事件时**，按日期分组展示。
3. **标记冲突** — 如果新事件与日历中的现有事件冲突。
4. **用⚠️标记截止日期** 并显示剩余天数。
5. **对于置信度较低的信息**，显示来源信息。
6. **未经用户确认，切勿自动创建事件**。

---

## 4. 日历创建

用户确认后，使用他们的日历工具创建事件：

### Google日历（通过`gog`或API）
```bash
gog calendar create \
  --title "Event Title" \
  --start "2026-02-17T09:00:00-05:00" \
  --end "2026-02-17T10:00:00-05:00" \
  --description "Extracted from email: [subject]" \
  --location "Zoom link or address"
```

### Apple日历（通过`osascript`）
```bash
osascript -e 'tell application "Calendar"
  tell calendar "Work"
    make new event with properties {summary:"Event Title", start date:date "Monday, February 17, 2026 at 9:00:00 AM", end date:date "Monday, February 17, 2026 at 10:00:00 AM", description:"Extracted from email", location:"Zoom"}
  end tell
end tell'
```

### Notion或其他工具
- 将数据格式化为结构化格式，并使用相应的API。
- 或者将结果输出为用户可以导入的.ics文件。

### ICS文件导出（通用格式）
```
BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTART:20260217T090000
DTEND:20260217T100000
SUMMARY:Event Title
DESCRIPTION:Extracted from email
LOCATION:Zoom link
END:VEVENT
END:VCALENDAR
```

---

## 5. 重复检测

在创建任何事件之前，请检查是否存在重复项：

1. **在日历中搜索** 在相同日期且标题相似的事件（允许一定程度的模糊匹配）。
2. **查看跟踪文件** — 记录已创建的事件：

```json
// memory/email-calendar-log.json
{
  "created_events": [
    {
      "email_id": "msg-123",
      "email_subject": "Team Offsite",
      "event_title": "Team Offsite",
      "event_date": "2026-02-17",
      "calendar_event_id": "cal-456",
      "created_at": "2026-02-13T10:00:00Z"
    }
  ]
}
```

**如果发现重复项**：向用户询问：“这个事件与[现有事件]相似。是跳过、更新还是创建新的事件？”

---

## 6. 截止日期与提醒功能

### 需要检测的截止日期模式

| 模式 | 例子 | 处理方式 |
|---------|---------|--------|
| 回复截止日期 | “请在2月10日前回复” | 在3天前创建提醒 |
| 注册截止日期 | “请在3月1日前注册” | 在1周前创建提醒 |
| 早鸟优惠截止日期 | “早鸟优惠截止日期为2月15日” | 在2天前创建提醒 |
| 票票销售截止日期 | “票票销售截止日期为……” | 创建提醒并添加日历事件 |
| 提交截止日期 | “请在……之前提交提案” | 在3天前创建提醒 |
| 到期日期 | “优惠有效期至……” | 在1天前创建提醒 |

### 提醒策略

- **超过30天**：在1周前提醒
- **7-30天**：在3天前提醒
- **少于7天**：在1天前提醒
- **包含URL的截止日期**：在提醒中包含相关链接
- 创建单独的日历事件，提醒内容为：“⚠️ 截止日期：[事件名称]，请在……之前完成”

---

## 7. 旅行相关邮件的处理

旅行确认邮件需要特殊处理：

### 提取以下所有信息：
- ✈️ **航班**：航空公司、航班号、出发/到达时间、机场、登机口、确认编号
- 🏨 **酒店**：酒店名称、地址、入住/退房时间、确认编号
- 🚗 **租车**：租车公司、接送时间、地点、确认编号
- 📋 **交通接送**：班车时间、火车预订信息

### 创建相应的日历事件：
- **航班出发**：在事件描述中包含登机口、航班号等信息
- **航班到达**：对于转机航班也需包含这些信息
- **酒店入住**：包含酒店地址和确认编号
- **酒店退房**：包含退房提醒
- **租车接送**：包含接送地点的详细信息

### 旅行相关的提醒：
- 航班：国内航班提前3小时提醒，国际航班提前4小时提醒
- 酒店退房：在出发当天早上提醒
- 在事件描述中包含所有确认信息

---

## 8. 批量处理

在扫描收件箱中的事件时，请执行以下操作：

1. **获取未读邮件**（或过去N天内的邮件）
2. **过滤无关信息** — 应用上述忽略规则
3. **从每封邮件中提取信息** — 运行提取框架
4. **消除重复项** — 处理多个邮件中提到的相同事件
5. **按日期排序** — 先显示最近的事件
6. **以分组的形式展示结果**：

```
📬 Inbox Scan: 47 unread → 12 with calendar items → 18 events found

THIS WEEK (Feb 13-19):
1. 🔴 Sprint Review — Thu Feb 13, 3:00 PM
2. 🔴 1:1 with Manager — Fri Feb 14, 10:00 AM
...

NEXT WEEK (Feb 20-26):
5. 🟡 Team Lunch — date TBD (mentioned in 2 emails)
...

DEADLINES:
⚠️ Q1 Report — Due Feb 28 (15 days) → [Submit here](url)
⚠️ Conference RSVP — Due Feb 20 (7 days) → [RSVP](url)
```

---

## 9. 特殊情况处理

| 情况 | 处理方式 |
|-----------|---------------|
| **一封邮件中包含多个时区** | 按邮件中指定的时区提取每个事件，并转换为用户的时区显示 |
| **时间未确定**（如“待定”或“TBA”） | 创建全天事件，并标记为待跟进 |
- **已取消的事件** | 检查日历中是否已有该事件——建议删除 |
- **重新安排的会议** | 找到原始会议信息后，建议更新（而非创建新事件） |
- **有特殊安排的重复事件**：在描述中注明具体的例外日期 |
- **日期不明确**（如“02/03”是指2月3日还是3月2日？） | 根据邮件的地区设置判断日期格式（MM/DD或DD/MM），如不确定则询问用户 |
- **引用或转发的邮件中的事件**：仅处理用户明确转发的邮件 |
- **附件为.ics文件**：直接解析ICS文件（置信度最高的来源）
- **“保存日期”类型的邮件**：创建临时事件，并标记为待处理状态 |
- **包含多个会议的会议**：将所有会议环节作为单独的事件提取，并使用相同的描述

---

## 10. 用户偏好记录

跟踪用户在不同会话中的偏好设置：

```yaml
# memory/email-calendar-prefs.yaml
default_timezone: "America/New_York"
default_calendar: "Work"
default_reminder_minutes: 30
auto_create_patterns:
  - "standup"
  - "1:1"
ignore_patterns:
  - "newsletter"
  - "marketing"
preferred_format: "12h"  # or "24h"
travel_reminder_hours: 3
```

当用户更正信息或明确表达偏好时，及时更新用户的偏好设置。