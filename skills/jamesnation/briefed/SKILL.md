---
name: briefed
description: 设置并运行一个名为 Briefed 的个人 AI 通讯智能系统。该系统每天从 Gmail 中获取通讯内容，使用 Claude Haiku 工具提取文章摘要，并提供一个功能完善的本地网页阅读器应用，支持投票、笔记记录以及兴趣跟踪功能。当用户需要设置通讯阅读器、每日摘要功能或通讯内容汇总工具时，可以选用 Briefed 与 OpenClaw 结合使用。
---
# 概述

这是一个每日新闻简报的自动化处理流程，包括从Gmail获取邮件、使用Haiku工具进行内容摘要处理，以及通过Web应用程序向用户发送通知。

## 架构

```
[Gmail]
   ↓  pre-fetch.py (fetches, filters, extracts compact metadata)
[newsletter-inbox.json]
   ↓  Haiku cron agent (reads compact JSON, writes AI summaries)
[newsletter-today.json]
   ↓  fetch-bodies.py (adds full HTML email bodies)
[newsletter-today.json + bodies]
   ↓  Express web reader (default port 3001)
[Notification ping → user opens reader]
```

**为什么要分离数据获取和摘要处理？** 直接使用Gmail的API获取原始JSON数据会导致Haiku的显示界面超载。Python负责数据清洗和整理工作，而Haiku则负责内容的理解和呈现。

## 先决条件

- 已安装并配置`gog`（gogcli）工具，并使用Gmail的只读OAuth权限进行身份验证。
- 确保Node.js版本不低于18（用于Web应用程序的运行）。
- 确保`claude-haiku-4-5`模型被添加到OpenClaw的允许使用模型列表中。
- 在OpenClaw中配置好通知渠道（例如Telegram、Discord等）。

## 设置步骤

### 1. 安装Gmail OAuth认证

```bash
# Install gogcli if not present
brew install gogcli   # or: npm install -g gogcli

# Authenticate (needs GCP OAuth client JSON — download from Google Cloud Console)
gog auth login --account YOUR@EMAIL.COM --credentials ~/client_secret_*.json
```

### 2. 部署Web应用程序

```bash
# Copy the reader to the workspace
cp -r assets/reader/ ~/.openclaw/workspace/briefed/
cd ~/.openclaw/workspace/briefed
npm install
```

### 3. 设置Gmail账户

请设置`NEWSLETTER_ACCOUNT`环境变量，或直接在两个脚本中修改`ACCOUNT`的值：

```bash
# scripts/pre-fetch.py  — line ~14
# scripts/fetch-bodies.py — line ~12
ACCOUNT = os.environ.get('NEWSLETTER_ACCOUNT', 'your@gmail.com')
```

最简单的方法是在LaunchAgent的plist文件中设置该账户信息（详见步骤5）。

### 4. 配置阅读兴趣

创建`~/.openclaw/workspace/newsletter-interests.json`文件（或在首次运行时自动生成）：

```json
{
  "version": 1,
  "topics": { "ai": 0.9, "startups": 0.8, "design": 0.75 },
  "signals": [],
  "sources": {}
}
```

### 5. 启动阅读器（macOS下使用LaunchAgent实现自动启动）

```bash
# Quick test
node ~/.openclaw/workspace/briefed/server.js

# Persistent — create ~/Library/LaunchAgents/ai.openclaw.briefed.plist
```

LaunchAgent的plist文件模板如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>ai.openclaw.briefed</string>
  <key>ProgramArguments</key><array>
    <string>/usr/local/bin/node</string>
    <string>/Users/YOUR_USER/.openclaw/workspace/briefed/server.js</string>
  </array>
  <key>EnvironmentVariables</key><dict>
    <key>NEWSLETTER_ACCOUNT</key><string>YOUR@EMAIL.COM</string>
  </dict>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>WorkingDirectory</key><string>/Users/YOUR_USER/.openclaw/workspace/briefed</string>
  <key>StandardOutPath</key><string>/tmp/briefed.log</string>
  <key>StandardErrorPath</key><string>/tmp/briefed.log</string>
</dict></plist>
```

```bash
launchctl load ~/Library/LaunchAgents/ai.openclaw.briefed.plist
```

### 6. 创建每日定时任务

使用OpenClaw的cron工具来安排定时任务（请填写相应的参数）：

```
Run my daily newsletter digest. Follow these steps exactly:

## Step 1 — Pre-fetch emails
Run: NEWSLETTER_ACCOUNT=YOUR@EMAIL.COM python3 ~/.openclaw/workspace/briefed/scripts/pre-fetch.py

## Step 2 — Read the compact inbox
Read: ~/.openclaw/workspace/newsletter-inbox.json

## Step 3 — Write newsletter-today.json with AI summaries
For each newsletter, write to ~/.openclaw/workspace/newsletter-today.json.
Use the snippet field to write real summaries — do NOT just repeat the subject line.
Score by interest: (adjust topics and weights to match your interests)
  ai/ml=0.9, startups=0.85, design=0.8, finance=0.75, general=0.6

Schema per story:
{ "id", "rank", "source", "subject", "headline", "summary", "bullets": [], "threadId", "gmailUrl", "score", "body": "" }

## Step 4 — Fetch HTML bodies
Run: NEWSLETTER_ACCOUNT=YOUR@EMAIL.COM python3 ~/.openclaw/workspace/briefed/scripts/fetch-bodies.py

## Step 5 — Send notification
Send (via your configured channel):
"📬 Today's digest is ready — <N> stories waiting.\n→ http://YOUR_HOST:3001"

## Step 6 — Final reply
📬 *Briefed — [DD Mon YYYY]* · <N> stories
*<rank>. <Source>* — <Headline>
<One sentence summary>
(repeat for all stories)
_Open the reader → http://YOUR_HOST:3001_
```

定时任务安排：每天早上7点执行，使用的模型为`anthropic/claude-haiku-4-5`，通知方式设置为`announce`。

## 数据文件

所有数据文件都存储在`~/.openclaw/workspace/`目录下：

| 文件名 | 用途 |
|------|---------|
| `newsletter-inbox.json` | 预先获取的电子邮件元数据（临时存储） |
| `newsletter-today.json` | 当天的新闻内容及摘要（包含HTML格式的正文） |
| `newsletter-interests.json` | 用户的阅读兴趣偏好及投票/阅读状态 |
| `newsletter-notes.json` | 用户对每篇新闻的备注 |
| `reading-list.md` | 用户已阅读或标记为收藏的新闻列表 |

## Web应用程序接口

| 端点 | 方法 | 用途 |
|----------|--------|---------|
| `/api/today` | GET | 获取所有新闻内容（去除HTML格式） |
| `/api/story/:id` | GET | 获取指定新闻的完整HTML内容 |
| `/api/vote` | POST | 发送投票信息（格式：`{ storyId, vote: "up" | "down" | "open" }`） |
| `/api/save` | POST | 将新闻添加到用户阅读列表（`reading-list.md`） |
| `/api/note` | POST | 为新闻添加备注（`{ storyId, note }`） |
| `/api/notes` | GET | 查看所有用户的备注 |

## 过滤交易类邮件

`scripts/pre-fetch.py`文件中的`SKIP_subject_PATTERNS`和`SKIP_SENDERS`列表可用于过滤交易类邮件：
- `SKIP_subject_PATTERNS`：用于识别交易类邮件的主题字符串。
- `SKIP_SENDERS`：始终被标记为交易类邮件的发送者名称（如银行、商店等）。

如果发现有交易类邮件被遗漏，请根据实际情况调整这些列表。

## 品牌设计

默认情况下，该阅读器会显示“Briefed”字样，并使用蓝色的“B”标志作为标识。如需自定义界面，请编辑`public/index.html`和`public'icon.svg`文件。