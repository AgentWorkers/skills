---
name: gmail-ai
description: AI-enhanced Gmail — smart email triage, priority scoring, AI-generated replies, thread summarization, and automated categorization. IMAP/SMTP with OpenRouter-powered intelligence. Use for inbox zero, email management, smart replies, and email automation.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, Gmail App Password
metadata: {"openclaw": {"emoji": "\ud83d\udce7", "requires": {"env": ["GMAIL_APP_PASSWORD"]}, "primaryEnv": "GMAIL_APP_PASSWORD", "homepage": "https://www.agxntsix.ai"}}
---

# 📧 Gmail AI  
专为 OpenClaw 代理设计的、基于人工智能的 Gmail 工具。该工具基于 gmail v1.0.6 版本开发，新增了人工智能邮件分类、优先级评分、智能回复以及邮件摘要功能。  

## 与标准 Gmail 的区别  
- **人工智能分类**：自动将邮件分为紧急、需处理、仅供参考或垃圾邮件三类。  
- **优先级评分**：根据发件人、主题和内容为邮件打分（0-100 分）。  
- **智能回复**：根据邮件内容生成合适的回复风格（专业/友好/简洁/正式）。  
- **邮件摘要**：为长篇邮件内容生成简短的总结。  
- **发送邮件**：支持通过 SMTP 协议发送邮件。  

## 必需配置项  
| 变量          | 是否必需 | 说明                          |  
|--------------|---------|--------------------------------|  
| `GMAIL_ADDRESS` | ✅       | 你的 Gmail 地址                      |  
| `GMAIL_APP_PASSWORD` | ✅       | Gmail 应用密码                      |  
| `OPENROUTER_API_KEY` | 可选      | 用于人工智能分类、回复和摘要功能            |  

## 快速入门  
```bash
# Fetch recent unread emails
python3 {baseDir}/scripts/gmail_ai.py inbox --unread --limit 10

# Fetch by label
python3 {baseDir}/scripts/gmail_ai.py inbox --label INBOX --limit 20

# Fetch from specific sender
python3 {baseDir}/scripts/gmail_ai.py inbox --from "boss@company.com"

# AI triage — categorize emails
python3 {baseDir}/scripts/gmail_ai.py triage --limit 20

# Priority scoring
python3 {baseDir}/scripts/gmail_ai.py priority --limit 20

# Summarize an email thread
python3 {baseDir}/scripts/gmail_ai.py summarize <message_id>

# Generate smart reply
python3 {baseDir}/scripts/gmail_ai.py reply <message_id> --tone professional
python3 {baseDir}/scripts/gmail_ai.py reply <message_id> --tone friendly
python3 {baseDir}/scripts/gmail_ai.py reply <message_id> --tone brief

# Send email
python3 {baseDir}/scripts/gmail_ai.py send --to "recipient@example.com" --subject "Hello" --body "Message body"

# Send with CC/BCC
python3 {baseDir}/scripts/gmail_ai.py send --to "a@b.com" --cc "c@d.com" --subject "Hello" --body "Message"
```  

## 常用命令  

### `inbox`  
通过 IMAP 协议从 Gmail 获取邮件：  
- `--unread`    | 只获取未读邮件                    |  
- `--label LABEL`   | 按 Gmail 标签或文件夹筛选（默认：收件箱）          |  
- `--from ADDRESS` | 按发件人筛选邮件                    |  
- `--limit N`    | 最多显示 N 条邮件                    |  
- `--since YYYY-MM-DD` | 显示自指定日期以来的邮件            |  

### `triage`  
基于人工智能的邮件分类功能（需要 `OPENROUTER_API_KEY`）：  
- 分类标准：🔴 紧急邮件、🟡 需处理邮件、⚪ 垃圾邮件/无关邮件  
- `--limit N`    | 分类处理的邮件数量                    |  

### `priority`  
根据发件人、主题紧急程度和内容为邮件评分（0-100 分）：  
- `--limit N`    | 评分的邮件数量                    |  
- 评分因素：发件人身份、主题关键词、是否提及你、截止日期等。  

### `summarize <message_id>`  
为指定邮件或邮件线程生成简短摘要。  

### `reply <message_id>`  
生成符合上下文的回复草稿：  
- `--tone professional|friendly|brief|formal` | 回复风格选择                    |  
- `--context TEXT` | 回复所需的额外背景信息                |  

### `send`  
通过 SMTP 协议发送邮件：  
- `--to ADDRESS` | 收件人地址                      |  
- `--subject TEXT` | 主题行                          |  
- `--body TEXT` | 邮件正文                        |  
- `--cc ADDRESS` | 抄送收件人地址                    |  
- `--bcc ADDRESS` | 密送收件人地址                    |  

## 安全提示  
- 该工具使用 Gmail 应用密码（而非 OAuth 认证），设置更简单，支持两步验证。  
- 注意：应用密码并非你的 Google 账户密码。  
- 获取方法：Google 账户 → 安全设置 → 两步验证 → 应用密码。  
- 确保已启用 Gmail 的 IMAP 功能。  

## 开发者信息  
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关内容可查看 [YouTube](https://youtube.com/@aiwithabidi) 和 [GitHub](https://github.com/aiwithabidi)。  
该工具属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。  

📅 **需要帮助配置 OpenClaw 以适应您的业务需求吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)