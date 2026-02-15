---
name: zoho-email-integration
description: **Zoho Mail 完整集成：支持 OAuth2、REST API（速度提升 5-10 倍）、Clawdbot/email 命令、HTML 邮件、附件以及批量操作。**  
系统经过安全加固，有效防范路径遍历（path traversal）和命令注入（command injection）攻击。非常适合用于电子邮件自动化处理和工作流程管理。
homepage: https://github.com/briansmith80/clawdbot-zoho-email
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - ZOHO_EMAIL
        - ZOHO_PASSWORD
    primaryEnv: ZOHO_EMAIL
    tokenFile: "~/.clawdbot/zoho-mail-tokens.json"
---

# Zoho 邮件集成

**v2.2.6** - 完整支持 Zoho Mail 的集成，采用 OAuth2 认证和 REST API 后端（速度比 IMAP/SMTP 快 5-10 倍），并支持通过 `/email` 命令在 Telegram/Discord 中使用 Clawdbot。**安全性得到加强**，防止路径遍历和命令注入攻击。支持 HTML 邮件、附件、批量操作以及高级自动化工作流。

选择您的认证方式：OAuth2（推荐，更安全）或应用密码（设置简单）。

## 🔄 升级到最新版本

```bash
clawhub install zoho-email-integration --force
```

或者更新所有技能：
```bash
clawhub update
```

## 🔒 安全公告（v2.2.5+）

**紧急修复：** 移除了易受攻击的 JavaScript 命令处理程序。如果您使用了示例文件夹中的 `email-command.js`，请立即更新：

```bash
# Re-download the secure handler
clawhub install zoho-email-integration --force
cp ~/.openclaw/skills/zoho-email-integration/examples/clawdbot-extension/email-command.js /your/deployment/path/
```

旧版本使用了带有 shell 插值的 `execSync`，新版本则使用 `spawn` 并传递参数数组来防止命令注入。

## ✨ 功能

### 🔐 认证与性能
- **OAuth2 认证** - 基于令牌的安全认证，支持自动刷新
- **REST API 后端** - 操作速度比 IMAP/SMTP 快 5-10 倍
- **优雅的回退机制** - 如果 REST API 不可用，会自动切换到 IMAP
- **应用密码支持** - OAuth2 的简单替代方案

### 📧 邮件操作
- **📥 阅读邮件** - 从任意文件夹（收件箱、已发送邮件、草稿等）中读取邮件
- **🔍 智能搜索** - 通过主题、发件人或关键词进行搜索，速度快速
- **📊 监控收件箱** - 实时显示未读邮件数量以接收通知
- **📤 发送邮件** - 支持纯文本或 HTML 格式，支持抄送/密送
- **🎨 HTML 邮件** - 支持丰富的格式和专业模板
- **📎 附件** - 支持发送和下载文件附件

### ⚡ 批量操作
- **批量操作** - 高效地标记、删除或移动多封邮件
- **批量操作** - 一次搜索并处理数百封邮件
- **试运行模式** - 执行前预览操作以确保安全

### 🔒 安全性
- **无硬编码的凭据** - 仅使用 OAuth2 令牌或环境变量
- **自动令牌刷新** - 令牌自动更新
- **加密连接** - 所有操作均使用 SSL/TLS 协议

## 📦 安装

```bash
clawdhub install zoho-email
```

**要求：**
- Python 3.x
- `requests` 库（安装：`pip3 install requests`）
- Zoho Mail 账户

## ⚙️ 设置

### 1. 获取应用专用密码

**重要提示：** 请勿使用您的主 Zoho 密码！

1. 登录 Zoho Mail
2. 转到 **设置** → **安全** → **应用密码**
3. 为 “Clawdbot” 或 “IMAP/SMTP 访问” 生成一个新的应用密码
4. 复制密码（后续会用到）

### 2. 配置凭据

**选项 A：环境变量**

导出您的 Zoho 凭据：

```bash
export ZOHO_EMAIL="your-email@domain.com"
export ZOHO_PASSWORD="your-app-specific-password"
```

**选项 B：凭据文件**

创建 `~/.clawdbot/zoho-credentials.sh`：

```bash
#!/bin/bash
export ZOHO_EMAIL="your-email@domain.com"
export ZOHO_PASSWORD="your-app-specific-password"
```

使其可执行并确保安全：
```bash
chmod 600 ~/.clawdbot/zoho-credentials.sh
```

然后在运行前执行该文件：
```bash
source ~/.clawdbot/zoho-credentials.sh
```

### 3. 测试连接

```bash
python3 scripts/zoho-email.py unread
```

预期输出：
```json
{"unread_count": 5}
```

## 🚀 使用方法

所有命令都需要通过环境变量设置凭据。

### 常用命令

```bash
# Diagnose setup (recommended first step)
python3 scripts/zoho-email.py doctor

# Unread count (great for briefings)
python3 scripts/zoho-email.py unread

# Search inbox
python3 scripts/zoho-email.py search "invoice"

# Get a specific email (folder + id)
python3 scripts/zoho-email.py get INBOX <id>

# Send a simple email
python3 scripts/zoho-email.py send recipient@example.com "Subject" "Body text"

# Empty Spam (safe by default: DRY RUN)
python3 scripts/zoho-email.py empty-spam
# Execute for real
python3 scripts/zoho-email.py empty-spam --execute

# Empty Trash (safe by default: DRY RUN)
python3 scripts/zoho-email.py empty-trash
# Execute for real
python3 scripts/zoho-email.py empty-trash --execute
```

### 发送 HTML 邮件

发送格式丰富的 HTML 邮件，支持多部分/替代格式（HTML 和纯文本版本）：

**CLI 命令：**
```bash
# Send HTML from a file
python3 scripts/zoho-email.py send-html recipient@example.com "Newsletter" examples/templates/newsletter.html

# Send HTML from inline text
python3 scripts/zoho-email.py send-html recipient@example.com "Welcome" "<h1>Hello!</h1><p>Welcome to our service.</p>"

# Preview HTML email before sending
python3 scripts/zoho-email.py preview-html examples/templates/newsletter.html
```

**Python API：**
```python
from scripts.zoho_email import ZohoEmail

zoho = ZohoEmail()

# Method 1: Send HTML with auto-generated plain text fallback
zoho.send_html_email(
    to="recipient@example.com",
    subject="Newsletter",
    html_body="<h1>Hello!</h1><p>Welcome!</p>"
)

# Method 2: Send HTML with custom plain text version
zoho.send_email(
    to="recipient@example.com",
    subject="Newsletter",
    body="Plain text version of your email",
    html_body="<h1>Hello!</h1><p>HTML version of your email</p>"
)

# Load HTML from template file
with open('examples/templates/newsletter.html', 'r') as f:
    html_content = f.read()

zoho.send_html_email(
    to="recipient@example.com",
    subject="Monthly Newsletter",
    html_body=html_content
)
```

**特点：**
- ✅ 支持多部分/替代格式的邮件（HTML + 纯文本）
- ✅ 自动生成纯文本作为备用方案
- ✅ 可从文件或内联字符串加载 HTML
- ✅ 发送前支持预览模式
- ✅ 全面支持 CSS 样式
- ✅ 适用于所有邮件客户端

**模板：**
`examples/templates/` 目录中提供预建模板：
- `newsletter.html` - 专业新闻通讯布局
- `announcement.html` - 带有横幅的重要公告
- `welcome.html` - 新员工欢迎邮件
- `simple.html` - 基本 HTML 模板，便于快速定制

### 查看未读邮件数量

```bash
python3 scripts/zoho-email.py unread
```

非常适合用于晨间简报或通知系统。

### 查看收件箱

```bash
python3 scripts/zoho-email.py search "invoice"
```

返回最近 10 封符合条件的邮件，包括主题、发件人和邮件正文预览。

### 查看已发送邮件

```bash
python3 scripts/zoho-email.py search-sent "client name"
```

返回最近 5 封符合条件的已发送邮件。

### 获取特定邮件

```bash
python3 scripts/zoho-email.py get Inbox 4590
python3 scripts/zoho-email.py get Sent 1234
```

返回邮件的完整内容，包括正文。

### 发送邮件

```bash
python3 scripts/zoho-email.py send "client@example.com" "Subject" "Email body here"
```

### 带附件发送邮件

```bash
python3 scripts/zoho-email.py send "client@example.com" "Invoice" "Please find the invoice attached" --attach invoice.pdf --attach receipt.jpg
```

支持使用 `--attach` 标志添加多个附件。

### 列出邮件附件

```bash
python3 scripts/zoho-email.py list-attachments Inbox 4590
```

返回包含附件详细信息的 JSON 数据：

```json
[
  {
    "index": 0,
    "filename": "invoice.pdf",
    "content_type": "application/pdf",
    "size": 52341
  },
  {
    "index": 1,
    "filename": "receipt.jpg",
    "content_type": "image/jpeg",
    "size": 128973
  }
]
```

### 下载附件

```bash
# Download first attachment (index 0) with original filename
python3 scripts/zoho-email.py download-attachment Inbox 4590 0

# Download second attachment (index 1) with custom filename
python3 scripts/zoho-email.py download-attachment Inbox 4590 1 my-receipt.jpg
```

返回包含下载详细信息的 JSON 数据：

```json
{
  "filename": "invoice.pdf",
  "output_path": "invoice.pdf",
  "size": 52341,
  "content_type": "application/pdf"
}
```

## 🤖 Clawdbot 集成示例

### 晨间简报

检查未读邮件并生成报告：

```bash
UNREAD=$(python3 scripts/zoho-email.py unread | jq -r '.unread_count')
echo "📧 You have $UNREAD unread emails"
```

### 邮件监控

监控重要邮件：

```bash
RESULTS=$(python3 scripts/zoho-email.py search "Important Client")
COUNT=$(echo "$RESULTS" | jq '. | length')

if [ $COUNT -gt 0 ]; then
  echo "⚠️ New email from Important Client!"
fi
```

### 自动回复

搜索并回复邮件：

```bash
# Find latest invoice inquiry
EMAIL=$(python3 scripts/zoho-email.py search "invoice" | jq -r '.[0]')
FROM=$(echo "$EMAIL" | jq -r '.from')

# Send reply
python3 scripts/zoho-email.py send "$FROM" "Re: Invoice" "Thanks for your inquiry..."
```

### 附件处理

自动下载发票附件：

```bash
# Search for invoice emails
EMAILS=$(python3 scripts/zoho-email.py search "invoice")

# Get latest email ID
EMAIL_ID=$(echo "$EMAILS" | jq -r '.[0].id')

# List attachments
ATTACHMENTS=$(python3 scripts/zoho-email.py list-attachments Inbox "$EMAIL_ID")

# Download all PDF attachments
echo "$ATTACHMENTS" | jq -r '.[] | select(.content_type == "application/pdf") | .index' | while read INDEX; do
  python3 scripts/zoho-email.py download-attachment Inbox "$EMAIL_ID" "$INDEX" "invoice_${INDEX}.pdf"
  echo "Downloaded invoice_${INDEX}.pdf"
done
```

发送带有附件的报告：

```bash
# Generate report
python3 generate_report.py > report.txt

# Send with attachment
python3 scripts/zoho-email.py send "manager@example.com" "Weekly Report" "Please see attached report" --attach report.txt --attach chart.png
```

## 📖 Python API

导入该模块以进行程序化使用：

```python
from scripts.zoho_email import ZohoEmail

zoho = ZohoEmail()

# Search emails
results = zoho.search_emails(folder="INBOX", query='SUBJECT "invoice"', limit=10)

# Get specific email
email = zoho.get_email(folder="Sent", email_id="4590")

# Send plain text email
zoho.send_email(
    to="client@example.com",
    subject="Hello",
    body="Message text",
    cc="manager@example.com"  # optional
)

# Send HTML email (auto-generated plain text fallback)
zoho.send_html_email(
    to="client@example.com",
    subject="Newsletter",
    html_body="<h1>Welcome!</h1><p>Rich HTML content here</p>",
    text_body="Welcome! Plain text version here"  # optional, auto-generated if not provided
)

# Send multipart email (HTML + custom plain text)
zoho.send_email(
    to="client@example.com",
    subject="Update",
    body="Plain text version",
    html_body="<h1>HTML version</h1>",
    cc="manager@example.com"
)

# Send email with attachments
zoho.send_email_with_attachment(
    to="client@example.com",
    subject="Invoice",
    body="Please find the invoice attached",
    attachments=["invoice.pdf", "receipt.jpg"],
    cc="manager@example.com"  # optional
)

# List attachments
attachments = zoho.get_attachments(folder="INBOX", email_id="4590")
for att in attachments:
    print(f"{att['index']}: {att['filename']} ({att['size']} bytes)")

# Download attachment
result = zoho.download_attachment(
    folder="INBOX",
    email_id="4590",
    attachment_index=0,
    output_path="downloaded_file.pdf"  # optional, uses original filename if not provided
)

# Check unread count
count = zoho.get_unread_count()
```

## 📖 HTML 邮件示例

请查看 `examples/send-html-newsletter.py` 中的完整示例：

```bash
# Run the HTML email examples
python3 examples/send-html-newsletter.py
```

示例内容包括：
- 发送简单的内联 HTML 邮件
- 加载和发送 HTML 模板
- 自动生成纯文本作为备用方案
- 支持预览功能
- 全面支持 CSS 样式

**快速入门：**
```python
#!/usr/bin/env python3
from scripts.zoho_email import ZohoEmail

zoho = ZohoEmail()

# Load a template
with open('examples/templates/welcome.html', 'r') as f:
    html = f.read()

# Send to recipient
zoho.send_html_email(
    to="newuser@example.com",
    subject="🎉 Welcome to Our Platform!",
    html_body=html
)
```

## 📁 文件夹参考

常见的 Zoho Mail 文件夹：
- `INBOX` - 主收件箱
- `Sent` - 已发送邮件
- `Drafts` - 草稿邮件
- `Spam` - 垃圾邮件文件夹
- `Trash` - 已删除邮件
- 自定义文件夹（例如 `INBOX/ClientName`）

## 🔧 高级配置

（如果使用自托管的 Zoho Mail，可以）覆盖默认的 IMAP/SMTP 服务器配置：

```bash
export ZOHO_IMAP="imap.yourdomain.com"
export ZOHO_SMTP="smtp.yourdomain.com"
export ZOHO_IMAP_PORT="993"
export ZOHO_SMTP_PORT="465"
```

## ❓ 故障排除

### 认证失败

- 确保 Zoho Mail 设置中启用了 IMAP
- 使用 **应用专用密码**，而非主密码
- 验证凭据是否正确导出

### 连接超时

- 检查防火墙是否允许端口 993（IMAP）和 465（SMTP）
- 验证 Zoho Mail 服务器的状态
- 尝试使用其他网络（企业防火墙可能会阻止 IMAP）

### 搜索无结果

- IMAP 搜索不区分大小写
- 尝试使用更宽泛的关键词
- 确认文件夹名称正确（区分大小写）

### “ZOHO_EMAIL 和 ZOHO_PASSWORD 必须设置”

您忘记导出凭据了！请运行以下命令：

```bash
export ZOHO_EMAIL="your-email@domain.com"
export ZOHO_PASSWORD="your-app-password"
```

## 🛣️ 路线图

### ✅ 已完成的功能（v2.0.0）

- [x] **OAuth2 认证** - 基于令牌的安全认证，支持自动刷新
- [x] **Zoho Mail REST API** - 操作速度比 IMAP/SMTP 快 5-10 倍
- [x] **附件支持** - 支持下载和发送附件
- [x] **HTML 邮件编写** - 支持丰富的格式和模板
- [x] **批量操作** - 标记、删除或移动多封邮件
- [x] **批量操作** - 一次搜索并处理多封邮件

### 🔮 未来改进计划

- [ ] **邮件分组** - 将相关邮件归类在一起
- [ ] **标签管理** - 创建和管理 Zoho Mail 标签
- [ ] **草稿邮件管理** - 创建、编辑和发送草稿邮件
- [ ] **定时发送** - 安排邮件发送时间
- [ ] **邮件模板** - 可重用的邮件模板，支持变量
- [ ] **Webhook** - 新邮件到达时发送实时通知
- [ ] **高级搜索** - 按大小、是否包含附件、日期范围筛选邮件
- [ ] **Zoho 日历集成** - 从邮件创建事件
- [ ] **Zoho CRM 集成** - 同步联系人和活动

## 📝 注意事项

- **搜索限制：** 默认返回最近 5-10 封邮件（可通过代码配置）
- **正文截断：** 搜索结果仅显示前 500 个字符
- **编码：** 支持 UTF-8 和多种邮件编码格式
- **安全性：** 凭据不会离开您的系统，只会传输到 Zoho 服务器

## 🤝 贡献

发现漏洞或希望贡献代码？请在 GitHub 上提交问题或 Pull Request！

## 📄 许可证

MIT 许可证 - 可免费使用、修改和分发。

---

**创建日期：** 2026-01-29  
**状态：** 已准备好生产使用 ✅  
**所需环境：** Python 3.x。对于 REST API 模式：`pip install -r requirements.txt`（包含 `requests` 库）。

## 🔄 批量操作

**v1.1 新功能！** 使用批量命令高效处理多封邮件。

### 将多封邮件标记为已读

```bash
python3 scripts/zoho-email.py mark-read INBOX 1001 1002 1003
```

一次命令即可将多封邮件标记为已读。非常适合清除通知。

### 将多封邮件标记为未读

```bash
python3 scripts/zoho-email.py mark-unread INBOX 1004 1005
```

标记重要邮件以便稍后处理。

### 删除多封邮件

```bash
python3 scripts/zoho-email.py delete INBOX 2001 2002 2003
```

**安全提示：** 删除前会请求确认。邮件会被移动到垃圾邮件文件夹（而非永久删除）。

### 在文件夹间移动邮件

```bash
python3 scripts/zoho-email.py move INBOX "Archive/2024" 3001 3002 3003
```

通过将邮件移动到自定义文件夹来整理邮件。

### 带搜索功能的批量操作

对符合搜索条件的所有邮件执行操作：

```bash
# Dry run first - see what would be affected
python3 scripts/zoho-email.py bulk-action \
  --folder INBOX \
  --search 'SUBJECT "newsletter"' \
  --action mark-read \
  --dry-run

# Execute the action
python3 scripts/zoho-email.py bulk-action \
  --folder INBOX \
  --search 'SUBJECT "newsletter"' \
  --action mark-read
```

**可用操作：**
- `mark-read` - 将所有匹配的邮件标记为已读
- `mark-unread` - 将所有匹配的邮件标记为未读
- `delete` - 将所有匹配的邮件移动到垃圾邮件文件夹

**搜索示例：**
```bash
# By subject
--search 'SUBJECT "invoice"'

# By sender
--search 'FROM "sender@example.com"'

# Unread emails
--search 'UNSEEN'

# Combine criteria (AND)
--search '(SUBJECT "urgent" FROM "boss@company.com")'

# Date range
--search 'SINCE 01-Jan-2024'
```

### Python 中的批量操作

```python
from scripts.zoho_email import ZohoEmail

zoho = ZohoEmail()

# Mark multiple emails as read
result = zoho.mark_as_read(['1001', '1002', '1003'], folder="INBOX")
print(f"Success: {len(result['success'])}, Failed: {len(result['failed'])}")

# Delete multiple emails
result = zoho.delete_emails(['2001', '2002'], folder="INBOX")

# Move emails to another folder
result = zoho.move_emails(
    email_ids=['3001', '3002'],
    target_folder="Archive/2024",
    source_folder="INBOX"
)

# Bulk action with search
result = zoho.bulk_action(
    query='SUBJECT "newsletter"',
    action='mark-read',
    folder="INBOX",
    dry_run=True  # Preview first
)

print(f"Found {result['total_found']} emails")
print(f"Will process {result['to_process']} emails")

# Execute for real
result = zoho.bulk_action(
    query='SUBJECT "newsletter"',
    action='mark-read',
    folder="INBOX",
    dry_run=False
)
```

### 批量清理示例

自动清理旧新闻通讯：

```bash
# 1. Preview what will be deleted
python3 scripts/zoho-email.py bulk-action \
  --folder INBOX \
  --search 'SUBJECT "newsletter"' \
  --action delete \
  --dry-run

# 2. Review the preview output

# 3. Execute if satisfied
python3 scripts/zoho-email.py bulk-action \
  --folder INBOX \
  --search 'SUBJECT "newsletter"' \
  --action delete
```

请参阅 `examples/batch-cleanup.py` 以获取完整的自动化清理脚本。