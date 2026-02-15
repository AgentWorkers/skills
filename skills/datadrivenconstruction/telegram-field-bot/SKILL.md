---
slug: "telegram-field-bot"
display_name: "Telegram Field Bot"
description: "为建筑领域的工人开发 Telegram 机器人。支持实时报告、照片上传、任务分配以及进度跟踪功能。通过与 n8n 的集成，实现自动化工作流程。"
---

# Telegram 田间作业辅助机器人

## 概述

田间工作人员需要简单的工具。Telegram 机器人能够提供即时通讯、图片分享以及任务管理功能，无需额外培训或下载任何应用程序。

> “适用于田间作业的 Telegram：实时任务分配和状态更新”——DDC 社区

## 为什么选择 Telegram？

| 功能 | 优势 |
|---------|---------|
| 无需培训 | 工作者已经在使用 Telegram |
| 支持离线工作 | 连接网络后消息会自动同步 |
| 支持上传图片/视频 | 便于进行可视化记录 |
| 支持群组聊天 | 便于团队协作 |
| 机器人自动化处理 | 实现工作流程自动化 |
| 免费使用 | 无需为每个用户购买许可 |

## 架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    TELEGRAM FIELD BOT                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Field Worker              Bot                    n8n            │
│  ────────────              ───                    ───            │
│                                                                  │
│  📱 Send photo    ───▶    🤖 Receive     ───▶   ⚙️ Process     │
│  📝 Text report           📋 Parse              📊 Store        │
│  📍 Location              🏷️ Classify           📧 Notify       │
│                           ✅ Confirm            📈 Dashboard     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 使用 n8n 快速入门

### 1. 创建 Telegram 机器人

```
1. Open Telegram, search @BotFather
2. Send /newbot
3. Name: "SiteReport Bot"
4. Username: "sitereport_company_bot"
5. Copy the API token
```

### 2. n8n 工作流程

```json
{
  "workflow": "Telegram Field Reporting",
  "nodes": [
    {
      "name": "Telegram Trigger",
      "type": "Telegram",
      "event": "message",
      "token": "YOUR_BOT_TOKEN"
    },
    {
      "name": "Parse Message",
      "type": "Code",
      "code": "Parse message type: text, photo, location"
    },
    {
      "name": "Route by Type",
      "type": "Switch",
      "rules": ["photo", "text", "location", "command"]
    },
    {
      "name": "Process Photo",
      "type": "OpenAI Vision",
      "prompt": "Describe this construction site photo. Identify: progress, issues, safety concerns."
    },
    {
      "name": "Save to Database",
      "type": "PostgreSQL",
      "operation": "insert"
    },
    {
      "name": "Confirm to User",
      "type": "Telegram",
      "action": "sendMessage",
      "text": "✅ Report received! ID: {{report_id}}"
    }
  ]
}
```

## 机器人命令

```python
# /start - Welcome and instructions
# /report - Start daily report
# /photo - Upload site photo
# /issue - Report issue
# /progress - Update progress
# /weather - Log weather conditions
# /safety - Safety observation
# /help - Show commands
```

## Python 机器人实现

```python
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio

# Bot token from BotFather
TOKEN = "YOUR_BOT_TOKEN"

# Keyboards
main_keyboard = ReplyKeyboardMarkup([
    ["📸 Photo Report", "📝 Text Report"],
    ["⚠️ Issue", "✅ Progress"],
    ["🌤️ Weather", "🦺 Safety"]
], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message"""
    await update.message.reply_text(
        "👷 Site Report Bot\n\n"
        "Use the buttons below to submit reports.\n"
        "All reports are automatically logged and processed.",
        reply_markup=main_keyboard
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process photo submissions"""
    photo = update.message.photo[-1]  # Highest resolution
    file = await photo.get_file()

    # Download photo
    photo_path = f"photos/{update.message.chat.id}_{photo.file_id}.jpg"
    await file.download_to_drive(photo_path)

    # Get caption (description)
    caption = update.message.caption or "No description"

    # Get location if available
    location = None
    if update.message.location:
        location = {
            "lat": update.message.location.latitude,
            "lon": update.message.location.longitude
        }

    # Save to database (via n8n webhook or direct)
    report = {
        "type": "photo",
        "user_id": update.message.from_user.id,
        "username": update.message.from_user.username,
        "photo_path": photo_path,
        "caption": caption,
        "location": location,
        "timestamp": update.message.date.isoformat()
    }

    # Send to n8n for processing
    # requests.post("https://n8n.company.com/webhook/photo-report", json=report)

    await update.message.reply_text(
        f"✅ Photo received!\n"
        f"📝 Description: {caption}\n"
        f"🕐 Time: {update.message.date.strftime('%H:%M')}\n\n"
        "Photo will be analyzed and added to daily report."
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process text reports"""
    text = update.message.text

    # Route based on button pressed
    if text == "📸 Photo Report":
        await update.message.reply_text("📸 Send a photo of the site with a description.")
    elif text == "📝 Text Report":
        await update.message.reply_text("📝 Type your progress report:")
    elif text == "⚠️ Issue":
        await update.message.reply_text(
            "⚠️ Describe the issue:\n"
            "- What is the problem?\n"
            "- Where is it located?\n"
            "- How urgent? (High/Medium/Low)"
        )
    elif text == "✅ Progress":
        await update.message.reply_text(
            "✅ Update progress:\n"
            "- What work was completed?\n"
            "- Percentage complete?\n"
            "- Any blockers?"
        )
    elif text == "🌤️ Weather":
        await update.message.reply_text(
            "🌤️ Weather conditions:\n"
            "- Temperature?\n"
            "- Conditions? (Clear/Rain/Snow/Wind)\n"
            "- Impact on work?"
        )
    elif text == "🦺 Safety":
        await update.message.reply_text(
            "🦺 Safety observation:\n"
            "- What did you observe?\n"
            "- Location?\n"
            "- Action taken?"
        )
    else:
        # Regular text report
        report = {
            "type": "text",
            "user_id": update.message.from_user.id,
            "username": update.message.from_user.username,
            "text": text,
            "timestamp": update.message.date.isoformat()
        }

        await update.message.reply_text("✅ Report logged!")

def main():
    """Start the bot"""
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
```

## 日报汇总

```python
def generate_daily_report(project_id: str, date: str) -> str:
    """Aggregate all Telegram reports into daily summary"""

    # Fetch all reports for the day
    reports = db.query("""
        SELECT * FROM telegram_reports
        WHERE project_id = ? AND DATE(timestamp) = ?
        ORDER BY timestamp
    """, [project_id, date])

    # Group by type
    photos = [r for r in reports if r['type'] == 'photo']
    issues = [r for r in reports if r['type'] == 'issue']
    progress = [r for r in reports if r['type'] == 'progress']

    # Generate summary with LLM
    summary = llm.summarize(f"""
        Daily reports for {date}:

        Photos submitted: {len(photos)}
        Issues reported: {len(issues)}
        Progress updates: {len(progress)}

        Details:
        {json.dumps(reports, indent=2)}

        Generate a concise daily report summary.
    """)

    return summary
```

## 群组聊天功能

```python
# Track messages in project groups
async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log important messages from project groups"""

    # Only log messages with keywords
    keywords = ["delay", "issue", "problem", "complete", "delivered", "inspection"]

    text = update.message.text.lower()
    if any(kw in text for kw in keywords):
        log_message({
            "group_id": update.message.chat.id,
            "group_name": update.message.chat.title,
            "user": update.message.from_user.username,
            "text": update.message.text,
            "timestamp": update.message.date.isoformat()
        })
```

## 需求

```bash
pip install python-telegram-bot requests
```

## 资源推荐

- python-telegram-bot: https://python-telegram-bot.org
- n8n Telegram 插件：https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-baseTelegram/
- BotFather：https://t.me/BotFather