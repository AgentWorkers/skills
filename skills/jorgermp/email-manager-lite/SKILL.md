---
name: portable-email-manager
version: 0.2.0
description: 这款轻量级电子邮件管理器支持 IMAP/SMTP 协议，具备高级搜索功能、文件夹管理功能以及附件检测功能。它可以与 Zoho、Gmail、Outlook 以及任何支持 IMAP/SMTP 协议的邮件服务提供商配合使用。
---

# Email Manager Lite v0.2

这是一个完全独立的电子邮件管理工具，专为 OpenClaw 设计。它使用标准的 IMAP 和 SMTP 协议，无需任何外部依赖。

## ✨ v0.2 的新功能

### 🔍 高级搜索与过滤
- 按发件人搜索 (`--from`)
- 按主题关键词搜索 (`--subject`)
- 按日期范围过滤 (`--since`, `--before`)
- 按已读/未读状态过滤 (`--seen`, `--unseen`)
- 在邮件正文中搜索 (`--body`，注意：此操作可能较慢）

### 📁 文件夹管理
- 使用 `folders` 命令列出所有 IMAP 文件夹
- 使用 `move` 命令在文件夹之间移动邮件
- 自动验证文件夹是否存在

### 📎 附件信息
- 自动检测附件
- 显示附件详情：
  - 文件名
  - MIME 类型
  - 文件大小（以 KB/MB 为单位）
- 附件信息会显示在“已读”和“搜索”结果中

## 🔧 安装

```bash
cd skills/portable-email-manager
npm install
```

依赖项已包含在 `package.json` 中：
- `nodemailer`：用于发送 SMTP 邮件
- `imap-simple`：用于 IMAP 操作
- `mailparser`：用于解析邮件和检测附件

## 🔐 认证信息

请设置以下环境变量：

```bash
export EMAIL_USER="your.email@domain.com"
export EMAIL_PASS="your-app-password"
```

**建议：** 对于 Gmail、Outlook 和 Zoho，使用应用密码（App Password）代替常规账户密码。

### 提供商配置

**Zoho Mail（默认设置）：**
- 已配置为 `smtp.zoho.eu` 和 `imap.zoho.eu`
- 生成应用密码：https://accounts.zoho.eu/home#security/apppasswords

**Gmail：**
- 修改 `scripts/email.js` 文件中的相关配置：
  ```javascript
  host: 'smtp.gmail.com'  // SMTP
  host: 'imap.gmail.com'  // IMAP
  ```
- 启用 2FA 并生成应用密码：https://myaccount.google.com/apppasswords

**Outlook/Hotmail：**
- 修改配置为使用 `smtp.office365.com` / `outlook.office365.com`
- SMTP 使用端口 587（TLS）

## 📖 使用方法

### 发送邮件

```bash
./scripts/email.js send "recipient@example.com" "Subject" "Email body text"
```

**示例：**
```bash
./scripts/email.js send "boss@company.com" "Weekly Report" "Attached is this week's summary."
```

### 阅读最近收到的邮件

```bash
./scripts/email.js read [limit]
```

**示例：**
```bash
# Read last 5 emails (default)
./scripts/email.js read

# Read last 20 emails
./scripts/email.js read 20
```

**输出内容包括：**
- UID（用于移动邮件的唯一标识符）
- 发件人/收件人地址
- 主题和日期
- 附件数量及详情
- 邮件正文预览（前 500 个字符）

### 高级搜索

```bash
./scripts/email.js search [options]
```

**搜索选项：**

| 选项 | 描述 | 示例 |
|--------|-------------|---------|
| `--from <email>` | 按发件人过滤 | `--from "boss@company.com"` |
| `--subject <text>` | 按主题关键词过滤 | `--subject "invoice"` |
| `--since <date>` | 在指定日期之后的邮件 | `--since "Jan 1, 2026"` |
| `--before <date>` | 在指定日期之前的邮件 | `--before "Feb 1, 2026"` |
| `--unseen` | 仅显示未读邮件 | `--unseen` |
| `--seen` | 仅显示已读邮件 | `--seen` |
| `--body <text>` | 在邮件正文中搜索（操作较慢） | `--body "meeting"` |
| `--limit <n>` | 限制搜索结果数量 | `--limit 10` |

**示例：**
```bash
# Find unread emails from specific sender
./scripts/email.js search --from "client@example.com" --unseen

# Search by subject
./scripts/email.js search --subject "invoice" --limit 5

# Date range search
./scripts/email.js search --since "Jan 15, 2026" --before "Feb 1, 2026"

# Search in body (use sparingly - can be slow)
./scripts/email.js search --body "quarterly review"

# Combine multiple filters
./scripts/email.js search --from "boss@company.com" --subject "urgent" --unseen --limit 3
```

### 列出文件夹

```bash
./scripts/email.js folders
```

显示所有 IMAP 文件夹的层次结构。

**示例输出：**
```
📁 INBOX
📁 Sent
📁 Archive
📁 Drafts
📁 Spam
📁 Trash
```

### 将邮件移动到文件夹

```bash
./scripts/email.js move <uid> <folder-name>
```

**重要提示：**
- 请从“已读”或“搜索”结果中获取邮件的 UID
- 文件夹名称区分大小写
- 脚本会在移动邮件前验证文件夹是否存在

**示例：**
```bash
# First, find the email and note its UID
./scripts/email.js search --from "newsletter@example.com"
# Output shows: UID: 12345

# Move to Archive folder
./scripts/email.js move 12345 "Archive"

# Move to custom folder
./scripts/email.js move 67890 "Projects/Work"
```

**错误处理：**
- 如果文件夹不存在，会显示可用的文件夹列表
- 在尝试移动邮件前会验证 UID 是否有效

### 帮助文档

```bash
./scripts/email.js help
```

提供完整的用户手册，包含所有命令和示例。

## 🎯 使用场景

### 日常邮件分类
```bash
# Check unread emails
./scripts/email.js search --unseen --limit 10

# Move newsletters to folder
./scripts/email.js search --from "newsletter@site.com" --limit 1
./scripts/email.js move <uid> "Newsletters"
```

### 查找特定邮件
```bash
# Search by sender and subject
./scripts/email.js search --from "client@example.com" --subject "proposal"

# Search by date
./scripts/email.js search --since "Jan 20, 2026" --subject "meeting notes"
```

### 归档旧邮件
```bash
# Find old read emails
./scripts/email.js search --before "Dec 1, 2025" --seen --limit 50

# Move each to Archive (use UID from output)
./scripts/email.js move <uid> "Archive"
```

### 检查附件
```bash
# Read recent emails and see attachment info
./scripts/email.js read 10

# Search output automatically shows:
# - Number of attachments
# - Filename, type, and size for each
```

## 🔒 安全性
- 认证信息不会被记录或存储在文件中
- 所有连接均使用 TLS/SSL 加密
- 建议使用应用密码而非常规账户密码
- 除了 IMAP/SMTP 连接外，数据不会离开您的设备

## ⚙️ 配置

默认配置适用于 **Zoho Mail EU**。
如需使用其他提供商，请修改 `scripts/email.js` 文件：

```javascript
// SMTP Configuration
const smtpConfig = {
  host: 'smtp.your-provider.com',
  port: 465,  // or 587 for TLS
  secure: true,  // true for SSL (465), false for TLS (587)
  auth: {
    user: EMAIL_USER,
    pass: EMAIL_PASS
  }
};

// IMAP Configuration
const imapConfig = {
  imap: {
    user: EMAIL_USER,
    password: EMAIL_PASS,
    host: 'imap.your-provider.com',
    port: 993,
    tls: true,
    authTimeout: 20000
  }
};
```

## 🚀 性能说明

- **正文搜索**（`--body`）在大型邮件箱中可能较慢，请谨慎使用
- **主题/发件人搜索**速度较快，因为利用了 IMAP 服务器端的过滤功能
- **日期过滤**效率较高
- 使用 `--limit` 限制搜索结果数量以加快响应速度

## 🐛 故障排除

**“认证失败”**
- 确保 `EMAIL_USER` 和 `EMAIL_PASS` 设置正确
- 使用应用密码，而非常规账户密码
- 检查提供商设置（如 2FA 等安全选项）

**“找不到文件夹”**
- 使用 `folders` 命令查看文件夹的准确名称
- 文件夹名称区分大小写
- 部分提供商的文件夹名称可能不同（例如，“Sent Items” 对应“Sent”）

**“连接超时”**
- 检查防火墙/网络设置
- 确保 IMAP/SMTP 端口可访问
- 尝试增加配置中的 `authTimeout` 值

**“未找到邮件”**
- 检查搜索条件
- 确认邮件存在于收件箱（而非其他文件夹）
- 尝试放宽搜索条件（移除部分过滤条件）

## 📝 版本历史

### v0.2.0（当前版本）
- ✨ 增加了多条件的高级搜索功能
- 支持文件夹管理（列出、移动邮件）
- 支持附件检测和显示附件信息
- 改进了输出格式
- 提供了详细的文档

### v0.1.0
- 基本的发送/阅读功能
- 支持 Zoho Mail
- 基于 IMAP/SMTP 协议

## 🤝 兼容性

已测试的兼容平台：
- ✅ Zoho Mail（欧盟和美国）
- ✅ Gmail
- ✅ Outlook/Hotmail
- ✅ iCloud Mail
- ✅ 自定义的 IMAP/SMTP 服务器

## 💡 使用技巧

1. **使用 UID 进行自动化操作：** 将搜索结果中的 UID 保存下来，以便程序化地移动邮件
2. **组合过滤条件：** 多个过滤条件可创建 AND 条件，实现精确搜索
3. **整理文件夹结构：** 先列出所有文件夹，以便规划管理策略
4. **日期格式：** 使用自然语言格式的日期，如 “Jan 1, 2026” 或 “December 25, 2025”
5. **附件过滤：** 在搜索结果中查找 “Attachments: X” 来找到包含附件的邮件

## 📄 许可证

ISC 许可证：您可以在自己的 OpenClaw 环境中自由使用该工具。