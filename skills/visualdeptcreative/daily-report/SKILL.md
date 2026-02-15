# SKILL.md - 日报

## 目的
跟踪进度、报告各项指标、管理内存使用情况。

## 使用的模型
**本地模型（ollama）** – 简单的数据聚合功能，免费使用。

## 早晨报告（西班牙时间上午9:30发送）

```
🤖 SKYNET MORNING BRIEFING - {{date}}

📊 PIPELINE
├─ Total leads: X
├─ Ready for outreach: X
├─ In sequence: X
├─ Awaiting reply: X

📬 OVERNIGHT
├─ Leads found: X
├─ Emails drafted: X
├─ Cost: $X.XX

🎯 TODAY'S PRIORITIES
1. [Based on pipeline status]
2. [Based on day of week]
3. [Based on targets]

💰 BUDGET
├─ Spent today: $X.XX
├─ Daily remaining: $X.XX
├─ Monthly remaining: $X.XX
```

## 日终报告（西班牙时间晚上9:00发送）

```
🤖 SKYNET EOD - {{date}}

📈 TODAY'S NUMBERS
├─ Leads sourced: X / 40 target
├─ DMs drafted: X / 25 target
├─ Emails drafted: X / 30 target
├─ Notion updated: ✓

💰 COST REPORT
├─ Today: $X.XX
├─ This week: $X.XX
├─ Budget remaining: $X.XX

🔥 HOT LEADS
[List any Priority A leads found]

⚠️ ISSUES
[List any blockers or errors]

📋 TOMORROW
[Next day priorities]

💾 Saved to memory/{{date}}.md
```

## 周报（每周日晚上8:00发送）

```
🤖 SKYNET WEEKLY - Week of {{date}}

📊 TOTALS
├─ Leads sourced: X
├─ Outreach sent: X (DMs + Emails)
├─ Replies: X
├─ Qualified: X
├─ Closes: X

💰 COSTS
├─ This week: $X.XX
├─ Avg per lead: $X.XX
├─ Avg per qualified: $X.XX

📈 CONVERSION
├─ Source → Qualified: X%
├─ Outreach → Reply: X%
├─ Reply → Meeting: X%

🎯 VS TARGETS
├─ Revenue: $X / $5,000 goal
├─ Days remaining: X
├─ Needed per day: $X
```

## 内存文件格式
将报告文件保存为 `memory/YYYY-MM-DD.md` 格式：

```markdown
# {{date}} - Daily Log

## Metrics
- Leads sourced: X
- DMs drafted: X
- Emails drafted: X
- Cost: $X.XX

## Leads Found (Summary)
- Priority A: X
- Priority B: X
- Skipped: X

## Issues
[Any problems encountered]

## Notes
[Context for future sessions]

## Tomorrow
- [ ] Task 1
- [ ] Task 2
```

## 警报机制（立即发送）
在以下情况下立即通过 Telegram 发送警报：
- 检测到任何回复
- 预算使用量达到75%
- 发生 API 错误或达到请求速率限制
- 运行任务完成（跨夜执行）
- 任务被阻塞或需要用户输入