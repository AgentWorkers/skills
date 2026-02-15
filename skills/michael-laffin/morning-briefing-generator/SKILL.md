# 早晨简报生成器

**版本：** 1.0  
**价格：** 15美元  
**类别：** 生产力工具  
**预计收入：** 每月300-1,000美元  

---

## 功能介绍  

该工具可生成个性化的早晨简报，内容包括：  
- 用户所在位置的天气预报  
- 当天的日历事件  
- 明天的日历预览  
- 过去12小时内收到的紧急邮件  
- 用户感兴趣领域的热门话题  
- 健康数据（如已连接设备）  
- 新闻摘要  
- 来自任务管理器的每日待办事项  

每天早晨可节省30分钟以上的时间。  

---

## 使用场景  

- **高管**：无需查看多个应用程序，即可快速了解当天的工作安排。  
- **销售人员**：掌握当天的会议和跟进事项。  
- **自由职业者**：追踪客户电话和截止日期。  
- **内容创作者**：了解热门话题以确定创作方向。  
- **任何人**：希望拥有高效早晨习惯的人。  

---

## 使用方法  

### 基本简报  
```
Generate my morning briefing for [CITY]
```  

### 详细简报  
```
Create my morning briefing including:
- Weather for San Francisco
- My Google Calendar events for today and tomorrow
- Urgent emails from the last 12 hours
- Top 5 trending topics in AI and tech
- My high-priority Asana tasks
```  

### 自动化每日简报（通过Cron任务）  
```
Create a cron job that runs every weekday at 7am.
Generate my morning briefing and send it via Telegram.
```  

---

## 配置方法  

将相关配置添加到 `TOOLS.md` 或 `HEARTBEAT.md` 文件中：  
```markdown
## Morning Briefing Preferences

- Location: San Francisco, CA
- Calendar: work@company.com, personal@gmail.com
- Interests: AI, tech, startups, cryptocurrency
- Task Manager: Asana (workspace: "My Company")
- Email Accounts: work@company.com, personal@gmail.com
- Delivery: Telegram at 7am weekdays
- Additional: Include Oura Ring sleep score if below 70%
```  

---

## 示例输出  

```
🌅 Morning Briefing - Monday, Feb 13, 2026

📍 San Francisco, CA
☀️ Partly Cloudy, 58°F → 67°F
☔ 10% chance of rain

📅 TODAY'S SCHEDULE
• 9:00 AM - Team standup (30 min)
• 11:00 AM - Client call: Acme Corp (1 hr)
• 2:00 PM - Product review (45 min)
• 4:30 PM - 1:1 with Sarah (30 min)

📅 TOMORROW PREVIEW
• 10:00 AM - Investor update call
• 3:00 PM - Design review

📧 URGENT EMAILS (2)
• From: boss@company.com - "Q1 targets due Friday"
• From: client@acme.com - "Can we reschedule?"

🔥 TRENDING IN AI/TECH
• OpenAI announces GPT-5
• Apple Vision Pro sales exceed expectations
• New Claude model released
• AI regulation updates in EU
• Startup funding trends

✅ PRIORITY TASKS
• [ ] Finalize Q1 presentation
• [ ] Review contractor invoices
• [ ] Send proposal to Acme Corp

😴 SLEEP SCORE: 72/100
Feeling rested. Good day for deep work.

---
Briefing generated at 7:00 AM PST
```  

---

## 集成选项  

### 天气数据  
- 内置天气信息（无需API密钥）  
- 或指定：`使用OpenWeatherMap并输入我的API密钥`  

### 日历  
- Google日历（OAuth）  
- Apple日历  
- Outlook  
- 任何iCal数据源  

### 邮件  
- Gmail（OAuth）  
- 支持多个邮箱账户  

### 任务管理器  
- Asana  
- Todoist  
- Notion  
- Linear  
- GitHub Issues  

### 通知方式  
- Telegram（推荐）  
- WhatsApp  
- Slack  
- 电子邮件  

---

## 高级功能  

- **智能优先级排序**  
```
Include only calendar events tagged "important" or "client-facing"
```  

- **自定义时间范围**  
```
Show me calendar events for the next 3 days, not just today/tomorrow
```  

- **过滤新闻**  
```
Only show trending topics related to: SaaS, B2B, enterprise software
```  

- **条件逻辑**  
```
If my Oura readiness score is below 70, suggest rescheduling intense meetings
```  

- **团队简报**  
```
Generate a team briefing with everyone's meetings and shared tasks
```  

---

## 示例提示  

### 高管专用提示  
```
Generate my executive morning briefing:
- Weather for New York
- Today's meetings (board, investors, leadership)
- Urgent emails from executives only
- Market summary for my watchlist: AAPL, MSFT, GOOGL
- Top business news
```  

### 销售人员专用提示  
```
Create my sales morning briefing:
- Client meetings today
- Follow-ups due
- New leads from overnight
- Industry news in my vertical
```  

### 内容创作者专用提示  
```
Generate my creator morning briefing:
- Today's content schedule
- Trending topics in my niche
- New comments/DMs to respond to
- Platform algorithm updates
```  

---

## 常见问题解答  

- **日历事件未显示**：  
  - 检查日历权限设置。  
  - 确认`TOOLS.md`文件中的日历ID是否正确。  
  - 测试命令：`Show me my calendar for today`。  

- **天气信息显示错误位置**：  
  - 更新`TOOLS.md`文件中的位置信息。  
  - 或在提示中指定具体城市：`Weather for [具体城市]`。  

- **无法接收Telegram消息**：  
  - 确认`.env`文件中的机器人令牌是否有效。  
  - 测试命令：`Send me a test message via Telegram`。  

- **邮件无法加载**：  
  - 重新认证邮箱账户。  
  - 检查OAuth令牌是否过期。  

---

## 价格与价值  

- **费用：** 15美元（一次性支付）。  
- **节省时间：** 每天节省30分钟以上。  
- **价值计算：** 每小时100美元，每天节省50美元，每月节省1,500美元。  
- **投资回报率（ROI）：** 首月即可超过10,000%。  

---

## 安装步骤  

1. 从ClawHub平台安装该工具。  
2. 在`TOOLS.md`文件中配置个人偏好设置。  
3. 设置Cron任务以实现自动化。  
- 或手动触发简报：`Generate my morning briefing`。  

---

## 技术支持  

- ClawHub社区Discord频道  
- 邮箱：[support email]  
- 文档：docs.openclaw.ai  

---

**开发者：** Vernox  
**所属产品系列：** 生产力工具套件