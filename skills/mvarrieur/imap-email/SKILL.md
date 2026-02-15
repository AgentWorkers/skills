---
name: imap-email
description: 通过 IMAP（如 ProtonMail Bridge、Gmail 等）阅读和管理电子邮件。可以查看新邮件/未读邮件、获取邮件内容、搜索邮件箱，并将邮件标记为已读/未读。该功能支持与所有 IMAP 服务器配合使用，包括 ProtonMail Bridge。
---

# IMAP 邮件阅读器

通过 IMAP 协议读取、搜索和管理电子邮件。支持 ProtonMail Bridge、Gmail IMAP 以及任何标准的 IMAP 服务器。

## 快速入门

**检查新邮件：**
```bash
node skills/imap-email/scripts/imap.js check
```

**获取特定邮件：**
```bash
node skills/imap-email/scripts/imap.js fetch <uid>
```

**标记为已读：**
```bash
node skills/imap-email/scripts/imap.js mark-read <uid>
```

**搜索邮箱：**
```bash
node skills/imap-email/scripts/imap.js search --from "sender@example.com" --unseen
```

## 配置

**快速设置（ProtonMail Bridge）：**
```bash
cd skills/imap-email
./setup.sh
```
设置助手会提示您输入 Bridge 的凭据并测试连接。

**手动设置：**
1. 将 `.env.example` 复制到 skill 文件夹中的 `.env` 文件。
2. 输入您的 IMAP 凭据。
3. `.env` 文件会被 git 自动忽略。

**环境变量：**
```bash
IMAP_HOST=127.0.0.1          # Server hostname
IMAP_PORT=1143               # Server port
IMAP_USER=your@email.com
IMAP_PASS=your_password
IMAP_TLS=false               # Use TLS/SSL connection
IMAP_REJECT_UNAUTHORIZED=false  # Set to false for self-signed certs (optional)
IMAP_MAILBOX=INBOX           # Default mailbox
```

**⚠️ 安全提示：** 请勿提交您的 `.env` 文件！该文件已被添加到 `.gitignore` 文件中，以防止意外丢失。

**ProtonMail Bridge 设置：**
- 安装并运行 ProtonMail Bridge。
- 使用 `127.0.0.1:1143` 作为 IMAP 端口。
- 密码由 Bridge 生成（而非您的 ProtonMail 密码）。
- TLS 设置：使用 `false`（Bridge 使用 STARTTLS）。
- `REJECT_UNAUTHORIZED` 设置为 `false`（Bridge 使用自签名证书）。

**Gmail IMAP 设置：**
- 主机：`imap.gmail.com`
- 端口：`993`
- TLS：`true`
- 启用“低安全应用访问”或使用应用密码。
- `REJECT_UNAUTHORIZED`：省略或设置为 `true`（默认值）。

## 命令

### check
检查邮箱中的未读/新邮件。

```bash
node scripts/imap.js check [--limit 10] [--mailbox INBOX] [--recent 2h]
```

选项：
- `--limit <n>`：最大结果数量（默认：10）
- `--mailbox <name>`：要检查的邮箱（默认：INBOX）
- `--recent <time>`：仅显示过去 X 小时的邮件（例如：30 分钟、2 小时、7 天）

返回包含以下信息的 JSON 数组：
- uid、发件人、主题、日期、邮件内容摘要、标记信息

### fetch
根据 UID 获取邮件的完整内容。

```bash
node scripts/imap.js fetch <uid> [--mailbox INBOX]
```

返回包含邮件全文（文本 + HTML）的 JSON 数据。

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

时间格式示例：
- `30m` = 过去 30 分钟
- `2h` = 过去 2 小时
- `7d` = 过去 7 天

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

## Cron 集成

使用 Clawdbot 的 cron 任务定期检查邮件：

```bash
# Check email every 15 minutes, deliver to iMessage
clawdbot cron add \
  --name "email-check" \
  --cron "*/15 * * * *" \
  --session isolated \
  --message "Check for new ProtonMail emails and summarize them" \
  --deliver \
  --channel imessage \
  --to "+15085600825"
```

在隔离的会话中，代理可以执行以下操作：
```bash
node /Users/mike/clawd/skills/imap-email/scripts/imap.js check --limit 5
```

## 工作流程示例

**晨间邮件摘要：**
1. 运行 `check --limit 10 --recent 12h`
2. 总结夜间收到的未读邮件
3. 将摘要发送到指定渠道

**检查特定发件人的最近邮件：**
1. 运行 `search --from "important@company.com" --recent 24h`
2. 如有需要，获取邮件全文
3. 处理后将其标记为已读

**每小时紧急邮件检查：**
1. 运行 `search --recent 1h --unseen`
2. 筛选重要关键词
3. 提取需要处理的邮件
4. 如果邮件紧急，发送通知

**每周摘要：**
1. 运行 `search --recent 7d --limit 20`
2. 总结邮件活动
3. 生成每周报告

## 依赖项**

**所需包：** imap-simple、mailparser、dotenv

**安装：**
```bash
cd skills/imap-email
npm install
```

这将安装 `package.json` 中列出的所有依赖项。

## 安全注意事项

- 将凭据存储在 `.env` 文件中（并将其添加到 `.gitignore` 文件中）。
- ProtonMail Bridge 的密码不是您的账户密码。
- 使用 ProtonMail Bridge 时，确保 Bridge 正在运行。
- 对于 Gmail，建议使用应用专用密码。

## 故障排除

**连接超时：**
- 确认 IMAP 服务器正在运行且可访问。
- 检查主机/端口配置。
- 使用 `telnet <host> <port>` 进行测试。

**身份验证失败：**
- 确认用户名（通常是完整的电子邮件地址）。
- 检查密码是否正确。
- 对于 ProtonMail Bridge：使用 Bridge 生成的密码，而非您的账户密码。
- 对于 Gmail：如果启用了 2FA，请使用应用密码。

**TLS/SSL 错误：**
- 确保 `IMAP_TLS` 设置与服务器要求一致（SSL 时设置为 `true`，STARTTLS 时设置为 `false`）。
- 对于自签名证书（例如 ProtonMail Bridge），将 `IMAP_REJECT_UNAUTHORIZED` 设置为 `false`。
- 检查端口是否与 TLS 设置匹配（SSL 时为 993，STARTTLS 时为 143）。

**结果为空：**
- 确认邮箱名称是否正确（区分大小写）。
- 检查搜索条件。
- 使用 `list-mailboxes` 命令列出所有邮箱。