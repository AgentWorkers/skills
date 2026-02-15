---
name: Events
description: 构建一个个人事件管理系统，用于跟踪音乐会、会议、聚会以及各种其他活动。
metadata: {"clawdbot":{"emoji":"📅","os":["linux","darwin","win32"]}}
---

## 核心功能
- 当用户提到某个活动时，主动提出帮忙跟踪该活动。
- 当用户计划举办活动时，协助组织相关细节。
- 当用户询问即将发生的活动时，及时提供相关信息。
- 创建 `~/events/` 作为活动管理的工作空间。

## 文件结构
```
~/events/
├── upcoming/
│   ├── concerts/
│   ├── conferences/
│   ├── social/
│   └── appointments/
├── hosting/
├── past/
├── annual/
│   └── recurring.md
└── calendar.md
```

## 活动记录
```markdown
# radiohead-may.md
## Event
Radiohead — MSG

## Date & Time
May 15, 2024, 8:00 PM

## Venue
Madison Square Garden, NYC

## Tickets
Section 112, Row 8
Confirmation: TM-789456

## Logistics
Doors 7pm, meeting Jake at 6:30
No large bags allowed
```

## 主办活动
```markdown
# hosting/birthday-2024/
├── overview.md    # date, venue, status checklist
├── guests.md      # confirmed, pending, declined
└── details.md     # food, drinks, music, setup
```

**访客跟踪**
```markdown
## Confirmed (12)
- Sarah + 1
- Jake

## Pending (5)
- Tom — following up

## Declined (2)
- Amy — out of town
```

## 年度重复性活动
```markdown
# recurring.md
## Birthdays
- Mom: March 22
- Dad: July 8

## Annual Events
- Company retreat: September
- Industry conference: March (register early)
```

## 快速日历视图
```markdown
# calendar.md
## March 2024
- 5: Jake's birthday party
- 12-14: SXSW Austin
- 22: Mom's birthday
```

## 多日活动
```markdown
# sxsw-2024/
├── overview.md    # dates, location, registration, travel
└── schedule.md    # day-by-day sessions and plans
```

## 需要记录的信息：
- 日期、时间、地点
- 门票/确认号码
- 后勤信息（停车、入场方式、着装要求）
- 与谁一起参加活动
- 在主办活动时记录参与者的回复情况（是否参加）

## 需要展示的信息：
- “下周有音乐会，入场时间为晚上7点”
- “妈妈5天后生日”
- “报名截止日期是明天”
- “周六已有15人确认参加”

## 逐步改进计划：
- 首先：添加即将举行的活动。
- 接着：添加年度重要事件（如生日、节假日）的记录。
- 然后：跟踪过去的事件以供回顾。
- 最后：建立活动主办的 checklist（检查清单）。

## 不应做的事情：
- 忘记确认号码。
- 迟误报名截止日期。
- 在主办活动时忘记记录参与者的回复情况。
- 忽略后勤细节。