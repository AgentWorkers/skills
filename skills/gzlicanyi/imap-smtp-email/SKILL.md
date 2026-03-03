---
name: imap-smtp-email
description: 通过 IMAP/SMTP 协议读取和发送电子邮件。可以查看新邮件/未读邮件、获取邮件内容、搜索邮箱、将邮件标记为已读/未读，以及发送带有附件的电子邮件。支持与所有 IMAP/SMTP 服务器配合使用，包括 Gmail、Outlook、163.com、vip.163.com、126.com、vip.126.com、188.com 和 vip.188.com。
metadata:
  openclaw:
    emoji: "📧"
    requires:
      env:
        - IMAP_HOST
        - IMAP_USER
        - IMAP_PASS
        - SMTP_HOST
        - SMTP_USER
        - SMTP_PASS
      bins:
        - node
        - npm
    primaryEnv: SMTP_PASS
---
# IMAP/SMTP 邮件工具

通过 IMAP 协议读取、搜索和管理电子邮件；通过 SMTP 发送电子邮件。支持 Gmail、Outlook、163.com、vip.163.com、126.com、vip.126.com、188.com、vip.188.com 以及任何标准的 IMAP/SMTP 服务器。

## 配置

在 `skill` 文件夹中创建 `.env` 文件，或设置环境变量：

```bash
# IMAP Configuration (receiving email)
IMAP_HOST=imap.gmail.com          # Server hostname
IMAP_PORT=993                     # Server port
IMAP_USER=your@email.com
IMAP_PASS=your_password
IMAP_TLS=true                     # Use TLS/SSL connection
IMAP_REJECT_UNAUTHORIZED=true     # Set to false for self-signed certs
IMAP_MAILBOX=INBOX                # Default mailbox

# SMTP Configuration (sending email)
SMTP_HOST=smtp.gmail.com          # SMTP server hostname
SMTP_PORT=587                     # SMTP port (587 for STARTTLS, 465 for SSL)
SMTP_SECURE=false                 # true for SSL (465), false for STARTTLS (587)
SMTP_USER=your@gmail.com          # Your email address
SMTP_PASS=your_password           # Your password or app password
SMTP_FROM=your@gmail.com          # Default sender email (optional)
SMTP_REJECT_UNAUTHORIZED=true     # Set to false for self-signed certs
```

## 常见邮件服务器

| 提供商 | IMAP 主机 | IMAP 端口 | SMTP 主机 | SMTP 端口 |
|----------|-----------|-----------|-----------|-----------|
| 163.com | imap.163.com | 993 | smtp.163.com | 465 |
| vip.163.com | imap.vip.163.com | 993 | smtp.vip.163.com | 465 |
| 126.com | imap.126.com | 993 | smtp.126.com | 465 |
| vip.126.com | imap.vip.126.com | 993 | smtp.vip.126.com | 465 |
| 188.com | imap.188.com | 993 | smtp.188.com | 465 |
| vip.188.com | imap.vip.188.com | 993 | smtp.vip.188.com | 465 |
| yeah.net | imap.yeah.net | 993 | smtp.yeah.net | 465 |
| Gmail | imap.gmail.com | 993 | smtp.gmail.com | 587 |
| Outlook | outlook.office365.com | 993 | smtp.office365.com | 587 |
| QQ Mail | imap.qq.com | 993 | smtp.qq.com | 587 |

**关于 Gmail 的重要提示：**
- Gmail 不接受您的常规账户密码
- 您必须生成一个 **应用密码**（App Password）：https://myaccount.google.com/apppasswords
- 使用生成的 16 位应用密码作为 `IMAP_PASS` 或 `SMTP_PASS`
- 需要启用两步验证的 Google 账户

**关于 163.com 的重要提示：**
- 使用 **授权码**（authorization code），而不是账户密码
- 首先在网页设置中启用 IMAP/SMTP 功能

## IMAP 命令（接收邮件）

### check
检查是否有新邮件或未读邮件。

```bash
node scripts/imap.js check [--limit 10] [--mailbox INBOX] [--recent 2h]
```

选项：
- `--limit <n>`：最大结果数量（默认：10）
- `--mailbox <名称>`：要检查的邮箱（默认：INBOX）
- `--recent <时间>`：仅显示过去 X 时间内的邮件（例如：30 分钟、2 小时、7 天）

### fetch
根据 UID 获取完整的邮件内容。

```bash
node scripts/imap.js fetch <uid> [--mailbox INBOX]
```

### download
下载邮件中的所有附件，或仅下载特定附件。

```bash
node scripts/imap.js download <uid> [--mailbox INBOX] [--dir <path>] [--file <filename>]
```

选项：
- `--mailbox <名称>`：邮箱（默认：INBOX）
- `--dir <路径>`：输出目录（默认：当前目录）
- `--file <文件名>`：仅下载指定的附件（默认：下载所有附件）

### search
使用过滤器搜索邮件。

```bash
node scripts/imap.js search [options]

Options:
  --unseen           Only unread messages
  --seen             Only read messages
  --from <email>     From address contains
  --subject <text>   Subject contains
  --recent <time>    From last X time (e.g., 30m, 2h, 7d)
  --since <date>     After date (YYYY-MM-DD)
  --before <date>    Before date (YYYY-MM-DD)
  --limit <n>        Max results (default: 20)
  --mailbox <name>   Mailbox to search (default: INBOX)
```

### mark-read / mark-unread
将邮件标记为已读或未读。

```bash
node scripts/imap.js mark-read <uid> [uid2 uid3...]
node scripts/imap.js mark-unread <uid> [uid2 uid3...]
```

### list-mailboxes
列出所有可用的邮箱/文件夹。

```bash
node scripts/imap.js list-mailboxes
```

## SMTP 命令（发送邮件）

### send
通过 SMTP 发送电子邮件。

```bash
node scripts/smtp.js send --to <email> --subject <text> [options]
```

**必需参数：**
- `--to <电子邮件>`：收件人（多个收件人用逗号分隔）
- `--subject <文本>`：邮件主题，或 `--subject-file <文件>`：使用文件作为邮件主题

**可选参数：**
- `--body <文本>`：纯文本邮件正文
- `--html`：以 HTML 格式发送邮件正文
- `--body-file <文件>`：从文件中读取邮件正文
- `--html-file <文件>`：从文件中读取 HTML 内容
- `--cc <电子邮件>`：抄送收件人
- `--bcc <电子邮件>`：密送收件人
- `--attach <文件>`：附加文件（用逗号分隔）
- `--from <电子邮件>`：覆盖默认的发件人

**示例：**
```bash
# Simple text email
node scripts/smtp.js send --to recipient@example.com --subject "Hello" --body "World"

# HTML email
node scripts/smtp.js send --to recipient@example.com --subject "Newsletter" --html --body "<h1>Welcome</h1>"

# Email with attachment
node scripts/smtp.js send --to recipient@example.com --subject "Report" --body "Please find attached" --attach report.pdf

# Multiple recipients
node scripts/smtp.js send --to "a@example.com,b@example.com" --cc "c@example.com" --subject "Update" --body "Team update"
```

### test
通过向自己发送测试邮件来测试 SMTP 连接。

```bash
node scripts/smtp.js test
```

## 依赖项

```bash
npm install
```

## 安全注意事项

- 将凭据存储在 `.env` 文件中（将其添加到 `.gitignore` 文件中）
- **Gmail**：系统不接受常规密码——请在 https://myaccount.google.com/apppasswords 生成应用密码
- 对于 163.com：使用授权码（authorization code），而不是账户密码

## 故障排除

**连接超时：**
- 确认服务器正在运行且可访问
- 检查主机/端口的配置

**身份验证失败：**
- 确认用户名（通常是完整的电子邮件地址）
- 检查密码是否正确
- 对于 163.com：使用授权码，而不是账户密码
- 对于 Gmail：常规密码无效——请在 https://myaccount.google.com/apppasswords 生成应用密码

**TLS/SSL 错误：**
- 确保 `IMAP_TLS`/`SMTPSecure` 设置符合服务器要求
- 对于自签名证书：设置 `IMAP_REJECT_UNAUTHORIZED=false` 或 `SMTP_REJECT_UNAUTHORIZED=false`