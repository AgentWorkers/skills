---
name: morning-briefing
description: 使用本地的 `briefing` CLI 生成每日晨间简报（包括天气、日历、新闻和提醒）。在数据收集过程中不使用任何 API 令牌。适用于用户请求晨间简报、每日总结、日程概览或希望自动接收每日简报的情况。
metadata: { "openclaw": { "emoji": "🌅", "os": ["darwin"], "requires": { "bins": ["briefing"] }, "install": [{ "id": "node", "kind": "node", "package": "@openclaw-tools/morning-briefing", "bins": ["briefing"], "label": "Install morning-briefing (npm)" }] } }
---

# 早晨简报

可以生成每日本地简报，且无需支付任何 API 许可费。

## 快速入门
- `briefing`：生成完整简报
- `briefing weather`：仅显示天气信息
- `briefing calendar`：显示日历事件
- `briefing news`：显示 RSS 新闻标题
- `briefing reminders`：显示到期提醒

## 输出格式
- `briefing --format default`：以易读的格式输出
- `briefing --format compact`：以简短的一行格式输出
- `briefing --format json`：以机器可读的 JSON 格式输出

## 配置
配置文件：`~/.config/morning-briefing/config.json`
配置初始化：`briefing config init`
自定义位置：`briefing --location "New York"`
日历预览：`briefing calendar --days 3`

## 安排任务
Cron 任务：`openclaw cron add --name "morning-briefing" --schedule "0 7 * * *" --prompt "运行 `briefing` 并将输出结果发送给我。`
Heartbeat 任务：在 HEARTBEAT.md 中添加以下内容：“在 07:00-08:00 之间运行 `briefing` 并将输出结果发送”

## macOS 权限设置
日历/提醒功能：系统设置 → 隐私与安全 → 允许使用终端

## 许可证
激活服务：`briefing activate <license-key>`
查看服务状态：`briefing status`