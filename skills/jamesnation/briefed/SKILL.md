---
name: briefed
description: 设置并运行一个名为 Briefed 的个人 AI 通讯智能系统。该系统每天从 Gmail 中获取通讯内容，利用 Claude Haiku 工具提取文章摘要，并通过一个精美的本地网页阅读器应用程序提供阅读体验，支持投票、做笔记以及跟踪用户兴趣。当用户需要设置通讯阅读器、每日摘要功能或基于 OpenClaw 的通讯内容汇总工具时，可以使用该系统。
metadata:
  openclaw:
    requires:
      env:
        - BRIEFED_GMAIL_CLIENT_SECRET
      optionalEnv:
        - BRIEFED_GMAIL_TOKEN_FILE
        - NEWSLETTER_ACCOUNT
      files:
        - ~/.openclaw/workspace/newsletter-inbox.json
        - ~/.openclaw/workspace/newsletter-today.json
        - ~/.openclaw/workspace/newsletter-interests.json
        - ~/.openclaw/workspace/newsletter-notes.json
        - ~/.openclaw/workspace/reading-list.md
---
# Briefed

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

**为什么要分离数据获取和摘要处理？** 直接使用Gmail的API获取原始JSON数据会导致Haiku无法正确处理这些数据。Python负责数据的整理和清洗，而Haiku则负责生成简洁的摘要。

## 安全性与权限

- 对Gmail的访问权限仅为**只读**（使用`gmail.readonly`）。
- OAuth令牌存储在本地文件`~/.openclaw/workspace/briefed-gmail-token.json`（或`BRIEFED_GMAIL_TOKEN_FILE`）中。
- 该流程仅允许读写以下工作区文件：
  - `newsletter-inbox.json`
  - `newsletter-today.json`
  - `newsletter-interests.json`
  - `newsletter-notes.json`
  - `reading-list.md`
- 通知内容仅发送到配置好的模型提供者和用户选择的通知渠道，不会发送到其他外部端点。

## 先决条件

- Python 3.9或更高版本
- 需要安装用于Gmail API的Python库：`google-api-python-client`、`google-auth`、`google-auth-oauthlib`
- 一个Google OAuth桌面客户端生成的JSON文件（用于Gmail的只读认证）
- Node.js版本≥18（用于Web应用程序）
- OpenClaw模型列表中包含`claude-haiku-4-5`
- 在OpenClaw中配置好通知渠道（例如Telegram、Discord等）

## 设置步骤

### 1. 安装Python依赖库

```bash
cd ~/.openclaw/workspace/briefed
python3 -m pip install -r scripts/requirements.txt
```

### 2. 配置Gmail OAuth认证

创建一个Google Cloud OAuth桌面应用并下载相应的客户端JSON文件，然后进行配置：

```bash
export BRIEFED_GMAIL_CLIENT_SECRET=~/client_secret.json
```

首次运行脚本时，Briefed会启动浏览器中的OAuth认证流程，并将生成的令牌存储在本地：

```bash
~/.openclaw/workspace/briefed-gmail-token.json
```

### 3. 部署Web应用程序

```bash
# Copy the reader to the workspace
cp -r assets/reader/ ~/.openclaw/workspace/briefed/
cd ~/.openclaw/workspace/briefed
npm install
```

### 4. 配置Gmail令牌路径（可选）

默认设置适用于大多数用户：
- 令牌文件：`~/.openclaw/workspace/briefed-gmail-token.json`
- 客户端密钥：`~/client_secret.json`

如有需要，可以通过环境变量进行修改：

```bash
export BRIEFED_GMAIL_CLIENT_SECRET=~/path/to/client_secret.json
export BRIEFED_GMAIL_TOKEN_FILE=~/.openclaw/workspace/briefed-gmail-token.json
```

### 5. 配置用户兴趣偏好

创建文件`~/.openclaw/workspace/newsletter-interests.json`（或在首次运行时自动生成）：

```json
{
  "version": 1,
  "topics": { "ai": 0.9, "startups": 0.8, "design": 0.75 },
  "signals": [],
  "sources": {}
}
```

### 6. 启动阅读器应用程序

如果不需要持久化数据，可以手动运行该应用程序；LaunchAgent是一个可选的自动化启动工具。

```bash
# Quick test
node ~/.openclaw/workspace/briefed/server.js

# Persistent — create ~/Library/LaunchAgents/ai.openclaw.briefed.plist
```

LaunchAgent的plist配置文件模板：

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
    <key>BRIEFED_GMAIL_CLIENT_SECRET</key><string>/Users/YOUR_USER/client_secret.json</string>
    <key>BRIEFED_GMAIL_TOKEN_FILE</key><string>/Users/YOUR_USER/.openclaw/workspace/briefed-gmail-token.json</string>
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

### 7. 创建每日定时任务

使用OpenClaw的cron工具设置定时任务（请填写相应的占位符）：

```
Run my daily newsletter digest. Follow these steps exactly:

## Step 1 — Pre-fetch emails
Run: python3 ~/.openclaw/workspace/briefed/scripts/pre-fetch.py

## Step 2 — Read the compact inbox
Read: ~/.openclaw/workspace/newsletter-inbox.json

## Step 3 — Write newsletter-today.json with AI summaries
For each newsletter, write to **only** this file: ~/.openclaw/workspace/newsletter-today.json.
Do not modify any other files in this step.
Use the snippet field to write real summaries — do NOT just repeat the subject line.
Score by interest: (adjust topics and weights to match your interests)
  ai/ml=0.9, startups=0.85, design=0.8, finance=0.75, general=0.6

Schema per story:
{ "id", "rank", "source", "subject", "headline", "summary", "bullets": [], "threadId", "gmailUrl", "score", "body": "" }

## Step 4 — Fetch HTML bodies
Run: python3 ~/.openclaw/workspace/briefed/scripts/fetch-bodies.py

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

在启用定时任务之前，需要手动运行一次以完成浏览器中的OAuth认证流程：

```bash
python3 ~/.openclaw/workspace/briefed/scripts/pre-fetch.py
```

定时任务安排：每天早上7点（`0 7 * * *`），使用的模型为`anthropic/claude-haiku-4-5`，通知方式设置为`announce`。

## 数据文件

所有数据文件都存储在`~/.openclaw/workspace/`目录下：

| 文件名 | 用途 |
|------|---------|
| `newsletter-inbox.json` | 预先获取的电子邮件元数据（临时存储） |
| `newsletter-today.json` | 当天的新闻故事及其摘要（包含HTML内容） |
| `newsletter-interests.json` | 用户的兴趣偏好和投票/阅读状态 |
| `newsletter-notes.json` | 用户对每篇新闻故事的评论 |
| `reading-list.md` | 用户保存或标记的新闻故事列表 |

## Web应用程序 API

| 端点 | 方法 | 用途 |
|----------|--------|---------|
| `/api/today` | GET | 获取所有新闻故事（去除HTML内容） |
| `/api/story/:id` | GET | 获取单篇新闻故事的完整HTML内容 |
| `/api/vote` | POST | 发送投票信息（格式：`{ storyId, vote: "up" | "down" | "open" }`） |
| `/api/save` | POST | 将新闻故事添加到阅读列表（`reading-list.md`） |
| `/api/note` | POST | 为新闻故事添加评论（`{ storyId, note }`） |
| `/api/notes` | GET | 查看所有评论 |

## 过滤交易类邮件

`scripts/pre-fetch.py`文件中包含两个可配置的列表：
- `SKIP_subject_PATTERNS`：用于标记交易类邮件的主题字符串模式 |
- `SKIP_SENDERS`：始终被视为交易类邮件的发件人名称（例如银行、商店等）

如果发现有交易类邮件被遗漏，可以调整这些配置。

## 品牌设计

默认情况下，阅读器会显示“Briefed”字样，并使用蓝色的“B”标志。如需自定义外观，请编辑`public/index.html`和`public'icon.svg`文件。