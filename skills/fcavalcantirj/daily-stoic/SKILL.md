---
name: daily-stoic
description: 每天发送来自瑞安·霍利迪（Ryan Holiday）所著《每日斯多葛哲学》（The Daily Stoic）中的斯多葛哲学名言。这些名言可用于通过电子邮件或 Telegram 设置每日智慧提醒，也可满足用户对特定日期的斯多葛哲学名言的需求。系统支持全年366天的内容，每条名言都包含标题、正文以及相关的思考内容。
---

# 每日斯多葛智慧

每天为您带来 Ryan Holiday 撰写的《The Daily Stoic》中的斯多葛哲学智慧。每篇文章都包含一个标题、开篇引语以及深刻的思考。

## 快速入门

```bash
# Get today's stoic message
python3 {baseDir}/scripts/get-stoic.py

# Get specific date (MM-DD format)
python3 {baseDir}/scripts/get-stoic.py 02-03

# Output formats
python3 {baseDir}/scripts/get-stoic.py --format text    # Plain text (default)
python3 {baseDir}/scripts/get-stoic.py --format json    # JSON
python3 {baseDir}/scripts/get-stoic.py --format html    # Email-ready HTML
python3 {baseDir}/scripts/get-stoic.py --format telegram # Telegram markdown
```

## 通过 Clawdbot 发送

### Telegram
```bash
# Use Clawdbot's message tool with telegram format
MESSAGE=$(python3 {baseDir}/scripts/get-stoic.py --format telegram)
# Then send via Clawdbot message action
```

### 电子邮件（通过 gog skill）
```bash
# Generate HTML email
HTML=$(python3 {baseDir}/scripts/get-stoic.py --format html)

# Send via gog gmail
gog gmail send --to recipient@email.com --subject "Daily Stoic - $(date +%B\ %d)" --body-html="$HTML"
```

## Cron 任务设置

安排每天早上 7 点自动发送：
```
0 7 * * * python3 /path/to/scripts/get-stoic.py --format telegram | send-to-telegram
```

或者使用 Clawdbot 的 Cron 任务来发送文本：
```
"Send today's Daily Stoic quote via Telegram and email to the configured recipients"
```

## 数据

- 共有 366 条内容（包括 2 月 29 日的条目）
- 每条内容包含：`date_label`（日期标签）、`title`（标题）、`quote`（引语）、`source`（来源）和 `reflection`（思考）
- 数据文件：`assets/stoic-daily.json`

## 示例输出

**2 月 3日 —— 你焦虑的根源**

“当我看到一个焦虑的人时，我会问自己：他们真正想要什么？”
— 伊壁鸠鲁，《论说集》，2.13.1

那位焦虑的父亲，担心着自己的孩子。他真正想要的是什么？一个永远安全的世界……

## 自定义

请编辑 `assets/email-template.html` 中的 HTML 模板，以匹配您的品牌形象。