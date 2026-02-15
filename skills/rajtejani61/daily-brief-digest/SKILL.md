---
name: daily-digest
description: 生成每日简报，内容包括紧急邮件（himalaya）、即将到来的日历事件（gog）以及相关新闻。当用户请求晨间总结、每日简报或当天工作进展更新时，可使用此功能。
---

# 每日摘要

此技能提供了一种结构化的方式，帮助您快速了解当天的工作内容。它依赖于本地配置的工具（使用 `himalaya` 处理电子邮件，使用 `gog` 管理日历），并且不会在技能本身中存储任何个人凭据。

## 工作流程

1. **电子邮件分类**：使用 `himalaya --output json envelope list --page-size 20` 获取最近的电子邮件，识别需要立即处理的紧急事项。
2. **日历与任务同步**：使用 `gog calendar events [calendarId] --from [today_start] --to [today_end]` 获取当天的日程安排。如有需要，还可以通过 `gog tasks/contacts` 或特定的列表命令查看到期任务。
3. **新闻检索**：使用 `web_fetch` 或 `browser` 获取当天的前三到五条新闻。
4. **日志生成与展示**：使用 `scripts/digest.js` 将这些信息整合成一份格式化的 HTML 报告。**重要提示：该脚本会自动将此报告保存为永久性的 Markdown 文件，路径为 `.openclaw/cron/DailyDigest_logs/[date].md`，以供日后查阅。**
5. **通知用户**：通过 `message` 工具向用户的活跃频道发送简短通知，并告知详细日志可查看于 `.openclaw/cron/DailyDigest_logs/[date].md`。

## 数据来源

- **电子邮件**：`himalaya` 命令行工具。
- **日历**：`gog` 命令行工具。
- **新闻**：网络搜索或可信的 RSS 源。
- **日志**：保存在本地目录 `~/.openclaw/cron/DailyDigest_logs/` 中。

## 示例输出

**📅 每日简报 - 2026-02-12**

**📧 最新邮件**
- **Google**：安全警报（04:10）
- **The Replit Team**：释放 Replit Agent 的全部潜力（2月11日）

**🗓️ 日程安排**
- 上午 10:30：锻炼（肩部）
- 下午 02:00：项目评审

**📰 新闻**
- [头条新闻 1]
- [头条新闻 2]