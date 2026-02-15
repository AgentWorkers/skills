---
name: outlook-delegate
description: 通过 Microsoft Graph API，您可以读取、搜索和管理 Outlook 邮件及日历，并支持代理访问功能。您的 AI 助手会以自身的身份进行身份验证，但实际上是以代理的身份访问邮箱/日历的所有者数据。该功能已针对代理访问进行了修改，详情请参考：https://clawhub.ai/jotamed/outlook
version: 1.0.0
author: 87marc
---

# Outlook 代理功能

通过 Microsoft Graph API，以代理身份访问其他用户的 Outlook/Microsoft 365 邮箱和日历。

## 代理架构

此功能适用于以下场景：
- **您的 AI 助手** 拥有自己的 Microsoft 365 账户（例如：`assistant@domain.com`）
- **账户所有者** 已授予助手对其邮箱/日历的代理访问权限
- 助手以自己的身份进行身份验证，但访问的是所有者的资源

### 与直接访问的区别

| 功能 | 直接访问（`/me`） | 代理访问（`/users/{id}`） |
|---------|----------------------|--------------------------------|
| API 基址 | `/me/messages` | `/users/{owner}/messages` |
| 发送邮件 | 显示为“发件人：所有者” | 显示为“发件人：助手代表所有者” |
| 日历 | 全权控制 | 根据授予的权限级别而定 |
| 权限 | Mail.ReadWrite, Mail.Send | Mail.ReadWrite.Shared, Mail.Send.Shared, Calendars.ReadWrite.Shared |

## 配置

### 配置文件：`~/.outlook-mcp/config.json`

```json
{
  "client_id": "your-app-client-id",
  "client_secret": "your-app-client-secret",
  "owner_email": "owner@domain.com",
  "delegate_email": "assistant@domain.com"
}
```

`owner_email` 是助手将以代理身份访问的邮箱地址。

## 设置要求

### 1. Azure AD 应用注册

应用注册需要以下代理权限（而非普通应用权限）：
- `Mail.ReadWrite.Shared` - 读写共享邮箱的权限
- `Mail.Send.Shared` - 代表他人发送邮件的权限
- `Calendars.ReadWrite.Shared` - 读写共享日历的权限
- `User.Read` - 读取助手自己的个人资料
- `offline_access` - 刷新令牌

### 2. Exchange 代理权限（管理员或所有者）

所有者必须通过 Exchange/Outlook 授予助手代理访问权限：

**PowerShell（管理员）：**
```powershell
# Grant mailbox access
Add-MailboxPermission -Identity "owner@domain.com" -User "assistant@domain.com" -AccessRights FullAccess

# Grant Send-on-Behalf
Set-Mailbox -Identity "owner@domain.com" -GrantSendOnBehalfTo "assistant@domain.com"

# Grant calendar access (Editor = can create/modify events)
Add-MailboxFolderPermission -Identity "owner@domain.com:\Calendar" -User "assistant@domain.com" -AccessRights Editor -SharingPermissionFlags Delegate
```

**或通过 Outlook 设置：**
所有者可以在 Outlook 中将助手添加为代理 → 文件 → 账户设置 → 代理访问。

### 3. 令牌流程

助手通过 OAuth2 以自己的身份进行身份验证，然后使用 `/users/{owner@domain.com}/` 端点访问所有者的资源。

## 使用方法

### 令牌管理
```bash
./scripts/outlook-token.sh refresh   # Refresh expired token
./scripts/outlook-token.sh test      # Test connection to BOTH accounts
./scripts/outlook-token.sh get       # Print access token
```

### 阅读所有者的邮件
```bash
./scripts/outlook-mail.sh inbox [count]           # Owner's inbox
./scripts/outlook-mail.sh unread [count]          # Owner's unread
./scripts/outlook-mail.sh search "query" [count]  # Search owner's mail
./scripts/outlook-mail.sh from <email> [count]    # Owner's mail from sender
./scripts/outlook-mail.sh read <id>               # Read email content
```

### 管理所有者的邮件
```bash
./scripts/outlook-mail.sh mark-read <id>          # Mark as read
./scripts/outlook-mail.sh mark-unread <id>        # Mark as unread
./scripts/outlook-mail.sh flag <id>               # Flag as important
./scripts/outlook-mail.sh delete <id>             # Move to trash
./scripts/outlook-mail.sh archive <id>            # Move to archive
./scripts/outlook-mail.sh move <id> <folder>      # Move to folder
```

### 代表所有者发送邮件
```bash
./scripts/outlook-mail.sh send <to> <subj> <body>  # Send on behalf of owner
./scripts/outlook-mail.sh reply <id> "body"        # Reply on behalf of owner
```

**注意：** 邮件中的“发件人”字段会显示为“助手代表所有者”。

### 所有者的日历
```bash
./scripts/outlook-calendar.sh events [count]      # Owner's upcoming events
./scripts/outlook-calendar.sh today               # Owner's today
./scripts/outlook-calendar.sh week                # Owner's week
./scripts/outlook-calendar.sh read <id>           # Event details
./scripts/outlook-calendar.sh free <start> <end>  # Owner's availability
```

### 在所有者的日历上创建事件
```bash
./scripts/outlook-calendar.sh create <subj> <start> <end> [location]
./scripts/outlook-calendar.sh quick <subject> [time]
```

## API 端点变更

主要的变更是将 `/me` 替换为 `/users/{owner_email}`：

```bash
# Direct access (old)
API="https://graph.microsoft.com/v1.0/me"

# Delegate access (new)
OWNER=$(jq -r '.owner_email' "$CONFIG_FILE")
API="https://graph.microsoft.com/v1.0/users/$OWNER"
```

## 代表所有者发送邮件的实现

在代表所有者发送邮件时，必须指定 `from` 地址：

```json
{
  "message": {
    "subject": "Meeting follow-up",
    "from": {
      "emailAddress": {
        "address": "owner@domain.com"
      }
    },
    "toRecipients": [{"emailAddress": {"address": "recipient@example.com"}}],
    "body": {"contentType": "Text", "content": "..."}
  }
}
```

收件人会看到：**“发件人：助手代表所有者 <owner@domain.com>”

## 权限总结

| 操作 | 所需权限 | Exchange 设置 |
|--------|-------------------|-----------------|
| 阅读所有者的邮件 | Mail.ReadWrite.Shared | FullAccess 或 Reviewer |
| 修改所有者的邮件 | Mail.ReadWrite.Shared | FullAccess 或 Editor |
| 以所有者的身份发送邮件 | Mail.Send.Shared | SendOnBehalf |
| 阅读所有者的日历 | Calendars.ReadWrite.Shared | Reviewer+ |
| 在所有者的日历上创建事件 | Calendars.ReadWrite.Shared | Editor |

## 故障排除

- **“访问被拒绝”或“403 禁止访问”**：检查助手是否具有访问所有者邮箱的权限。
- **“找不到邮箱”**：确认 `config.json` 中的 `owner_email` 是否正确。
- **权限不足**：检查应用注册是否缺少 `.Shared` 权限（请查看 Azure AD）。
- **邮件发送后未显示“代表所有者”**：检查是否缺少 `SendOnBehalf` 权限。运行以下命令：
    ```powershell
Set-Mailbox -Identity "owner@domain.com" -GrantSendOnBehalfTo "assistant@domain.com"
```

- **令牌过期**：运行 `outlook-token.sh refresh` 刷新令牌。

## 安全考虑

1. **审计记录**：助手的所有操作都会记录在所有者的邮箱审计日志中。
2. **令牌存储**：凭证存储在 `~/.outlook-mcp/` 目录中——请保护该目录的安全。
3. **权限限制**：助手只能访问所有者明确授予的权限范围。
4. **权限撤销**：所有者可以随时通过代理设置撤销代理权限。

## 相关文件

- `~/.outlook-mcp/config.json`：客户端 ID、密钥以及所有者/代理的邮箱地址。
- `~/.outlook-mcp/credentials.json`：OAuth 令牌（用于访问和刷新）。

## 更新日志

### v1.0.0（代理版）
- **变更**：API 调用现在使用 `/users/{owner}` 而不是 `/me`。
- 新增：`owner_email` 和 `delegate_email` 配置字段。
- 新增：支持代表所有者发送邮件，并正确设置发件人字段。
- 权限更新为 `.Shared` 类型。
- 新增：代理设置文档。
- 新增：令牌测试以验证对所有者邮箱的访问权限。
- 基于 jotamed 的 outlook v1.3.0 版本实现（https://clawhub.ai/jotamed/outlook）。