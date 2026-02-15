---
name: Daily Briefing
description: 创建一个包含优先事项、日程安排及重要更新的晨间简报。
---

# 每日简报

我们创建了一份简洁的晨间简报，让用户能够在开始新的一天时清楚地了解当天的重点事项。

## 触发条件

当用户说出以下话语时，系统会触发简报：  
“给我做个简报”  
“晨间简报”  
“今天有什么安排？”  
“开始我的一天”  

或者，如果配置了心跳（heartbeat）或定时任务（cron），系统会自动执行简报。

## 简报模板  
```
☀️ DAILY BRIEFING — [Day, Month Date, Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 TODAY'S SCHEDULE
• [Time] — [Event] ([Location/Link])
• [Time] — [Event] ([Location/Link])
• [No meetings today — deep work day!]

🎯 TOP 3 PRIORITIES
1. [Most important thing]
2. [Second priority]
3. [Third priority]

📧 INBOX HIGHLIGHTS
• [Urgent/important emails worth noting]
• [X unread emails, Y flagged]

📰 RELEVANT NEWS
• [Industry news or updates that matter]

⚡ FOLLOW-UPS DUE
• [Person] — [Action] (was due [date])
• [Person] — [Action] (due today)

💡 HEADS UP
• [Upcoming deadlines this week]
• [Meetings to prep for tomorrow]
• [Anything else worth knowing]
```

## 优先级框架  

使用以下矩阵对任务进行排序：  

|  | 紧急   | 不紧急   |
|---|--------|------------|
| **重要** | 首先处理 — 日历冲突、客户紧急事务、当天的截止日期 | 计划安排 — 战略性工作、关系建立 |
| **不重要** | 委派他人处理/快速完成 — 管理任务、常规回复 | 跳过 — 浪费时间的事务、低价值会议 |

## 数据来源  

从以下可用信息中提取内容：  
- **日历** — 当天的事件以及明天的早间事件  
- **电子邮件** — 未读邮件数量、标记为紧急的邮件、重要发件人  
- **客户关系管理（CRM）** — 到期的跟进事项（如果启用了CRM管理功能）  
- **任务/笔记** — 任何已记录的待办事项或项目笔记  
- **新闻** — 通过网络搜索获取的行业相关头条新闻  
- **天气** — 如有必要，提供快速天气预报  

## 规则  

- 保持简报内容易于阅读：整个简报的阅读时间应控制在60秒以内。  
- 严格区分任务的优先级，只列出真正重要的事项。  
- 如果日历为空，应如实说明（这也很重要——说明今天需要集中精力工作）。  
- 如果无法访问电子邮件，跳过相关部分，不要假装可以访问。  
- 以有用的信息结束简报，例如对明天的提醒或本周的总结。  
- 根据一天中的不同时间调整简报的语气：早晨的简报应充满活力，晚间的总结则应更具反思性。  
- 如果用户跨时区工作，需在简报中注明时区信息。  

## 晚间总结（可选）  

如果在一天结束时用户询问：“今天过得怎么样？”或“请提供一天总结”，系统可以提供相应的晚间总结。  
```
🌙 END OF DAY — [Date]
━━━━━━━━━━━━━━━━━━━━

✅ COMPLETED
• [What got done]

🔄 CARRIED OVER
• [What didn't get done — moves to tomorrow]

📝 NOTES
• [Key decisions, insights, things to remember]

📅 TOMORROW PREVIEW
• [First meeting/deadline]
```