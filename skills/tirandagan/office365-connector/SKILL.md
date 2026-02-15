---
name: office365-connector
description: Office 365 / Outlook 连接器：支持通过弹性 OAuth 认证进行电子邮件（读取/发送）、日历（读取/写入）和联系人（读取/写入）的操作。现已支持多账户功能！您可以通过一个工具管理多个 Microsoft 365 账户。该工具有效解决了连接 Office 365 电子邮件、日历和联系人数据的难题，并采用了 Microsoft Graph API，同时提供了详细的 Azure 应用注册设置指南。非常适合从 OpenClaw 访问您的 Microsoft 365/Outlook 数据。
---

# Office 365 连接器（多账户增强版）

## 概述

该技能提供了对 **Office 365 / Outlook** 服务的稳定、可生产环境的连接支持，包括电子邮件、日历和联系人功能。从 **v2.0.0** 版本开始，支持多账户管理，您可以通过一个技能安装来管理多个 Microsoft 365 身份（工作、个人、咨询等）。

它通过提供 OAuth 认证、自动令牌刷新、每个账户的隔离以及全面的 Azure 应用注册设置指导，解决了从自动化工具连接到 Office 365 的常见挑战。

**适用场景：**
- 在多个组织间管理多个工作身份
- 分离个人和专业的电子邮件/日历
- 访问共享邮箱和委托的日历
- 为在多个客户之间工作的咨询师和自由职业者提供支持

**v2.0.0 的新功能：** 多账户支持！请参阅 [MULTI-ACCOUNT.md](MULTI-ACCOUNT.md) 以获取完整的使用指南。

**致谢：** 该技能由 **Matthew Gordon**（[matt@workandthrive.ai](mailto:matt@workandthrive.ai)）增强 - 详情请参见 [CREDITS.md](CREDITS.md)。

## v2.0.0 的新特性

**Matthew Gordon 的主要增强功能：**
- ✨ **多账户管理** - 从一个技能中管理多个 Microsoft 365 身份
- 🔐 **每个账户的令牌隔离** - 为每个账户存储单独且安全的令牌
- 🔄 **便捷的账户切换** - 在所有操作中使用 `--account=name` 标志
- ⚙️ **默认账户选择** - 设置您喜欢的账户以方便使用
- 📦 **旧版导入工具** - 无缝迁移现有的单账户设置
- 🎯 **账户管理 CLI** - 简单的添加/删除/列出/设置默认账户的命令
- ✅ **完全向后兼容** - 现有的单账户设置可正常使用

请参阅 [CHANGELOG.md](CHANGELOG.md) 以获取完整的版本历史记录。

## 功能

### 电子邮件操作
- 读取电子邮件（收件箱、已发送邮件、文件夹）
- 发送电子邮件（含附件、HTML 格式）
- 按发送者、主题、日期范围搜索电子邮件
- 管理文件夹和移动邮件
- 标记为已读/未读、标记邮件
- 删除邮件

### 日历操作
- 读取日历事件
- 创建/更新/删除事件
- 查看可用性
- 管理会议邀请
- 支持重复事件
- 处理时区

### 联系人操作
- 读取联系人和联系人文件夹
- 创建/更新/删除联系人
- 按姓名、电子邮件、公司名称搜索联系人
- 管理联系人组
- 同步联系人信息

## 快速入门 - 多账户

### 添加您的第一个账户

```bash
cd skills/office365-connector

# Add account
node accounts.js add work <tenant-id> <client-id> <client-secret> you@work.com "Work account"

# Authenticate
node auth.js login --account=work
```

### 添加更多账户

```bash
# Add personal account
node accounts.js add personal <tenant> <client> <secret> you@outlook.com "Personal"

# Add consulting account
node accounts.js add consulting <tenant> <client> <secret> you@client.com "Consulting"

# Set default
node accounts.js default work

# List all accounts
node accounts.js list
```

### 使用您的账户

```bash
# Check work calendar
node calendar.js today --account=work

# Read personal emails
node email.js recent 10 --account=personal

# Send from consulting account
node send-email.js send client@example.com "Subject" "Body" --account=consulting
```

### 从单账户设置迁移

如果您已经在使用 v1.0.0？没问题！

```bash
# Import your existing setup
node accounts.js import-legacy

# Continue using without changes (environment variables still work)
# OR add additional accounts
node accounts.js add secondary <tenant> <client> <secret>
```

## 先决条件

在使用此技能之前，您 **必须** 完成 Azure 应用注册设置，以获取以下信息：
1. **租户 ID** - 您的 Azure AD 租户标识符
2. **客户端 ID** - 您的应用程序（客户端）ID
3. **客户端密钥** - 您的应用程序密钥值

**设置时间：每个账户约 10-15 分钟**

请参阅 [设置指南](references/setup-guide.md) 以获取详细的步骤说明。

## 权限验证

此技能需要以下 **委托权限**（需要用户同意）：

### 电子邮件权限
- `Mail.Read` - 读取用户的电子邮件
- `Mail.ReadWrite` - 读取和写入用户的电子邮件
- `Mail.Send` - 以用户的身份发送电子邮件

### 日历权限
- `Calendars.Read` - 读取用户的日历
- `Calendars.ReadWrite` - 读取和写入用户的日历

### 联系人权限
- `Contacts.Read` - 读取用户的联系人
- `Contacts.ReadWrite` - 读取和写入用户的联系人

### 帖户信息权限（用于认证）
- `User.Read` - 登录并读取用户信息
- `offline_access` - 维持数据访问（刷新令牌）

**重要提示：** 在继续设置之前，请确认您理解并同意这些权限。每个权限都授予对您的 Microsoft 365 数据的特定访问权限。

请参阅 [权限参考](references/permissions.md) 以获取有关每个权限的详细信息。

## 配置

### 多账户配置（v2.0.0+）

账户存储在 `~/.openclaw/auth/office365-accounts.json` 中，令牌存储在 `~/.openclaw/auth/office365/` 中。

使用 `accounts.js` CLI 进行管理：

```bash
node accounts.js list                # List all accounts
node accounts.js add <name> ...      # Add account
node accounts.js remove <name>       # Remove account
node accounts.js default <name>      # Set default
```

### 旧版单账户（向后兼容）

环境变量仍然适用于单账户使用：

```bash
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
```

或者在 OpenClaw 配置中设置：

```json
{
  "env": {
    "vars": {
      "AZURE_TENANT_ID": "your-tenant-id",
      "AZURE_CLIENT_ID": "your-client-id",
      "AZURE_CLIENT_SECRET": "your-client-secret"
    }
  }
}
```

## 认证流程

此技能使用 **OAuth 2.0 设备代码流程** 进行稳定认证：
1. 从 Microsoft 请求设备代码
2. 显示用户代码和验证 URL
3. 用户访问 URL 并输入代码
4. 等待令牌完成
5. 存储访问令牌和刷新令牌（每个账户单独存储）
6. 令牌过期时自动刷新

**令牌存储：** 令牌安全存储在 `~/.openclaw/auth/office365/<account-name>.json` 中，权限设置为 0600（仅所有者可读写）。

## 使用示例

### 多账户电子邮件操作

```bash
# Read from default account
node email.js recent 10

# Read from specific account
node email.js recent 10 --account=work

# Search in consulting account
node email.js search "proposal" --account=consulting

# Send from appropriate identity
node send-email.js send client@example.com "Update" "..." --account=consulting
```

### 多账户日历操作

```bash
# Check work calendar
node calendar.js today --account=work

# Check personal calendar
node calendar.js week --account=personal
```

### 账户管理

```bash
# List all configured accounts
node accounts.js list

# Check authentication status
node auth.js status --account=work

# Re-authenticate if needed
node auth.js login --account=work
```

## 实际应用场景

### 多个工作身份

在多个组织间工作时非常适用：

```bash
# Morning: Check all calendars
node calendar.js today --account=work
node calendar.js today --account=consulting
node calendar.js today --account=startup

# Process emails by identity
node email.js recent --account=work
node email.js recent --account=consulting

# Send from appropriate account
node send-email.js send client@bigcorp.com "Proposal" "..." --account=work
```

### 个人与工作信息的分离

```bash
# Work hours: Work account
node calendar.js today --account=work
node email.js recent --account=work

# After hours: Personal account
node email.js recent --account=personal
```

## 错误处理

该技能具有强大的错误处理能力：
- **令牌过期** - 自动刷新并采用指数退避策略
- **速率限制** - 实施带有适当延迟的重试逻辑
- **网络错误** - 处理连接超时
- **权限错误** - 显示关于缺失权限范围的提示信息
- **API 错误** - 显示来自 Microsoft Graph 的详细错误信息
- **账户未找到** - 提供有用的错误信息和建议

## 速率限制

Microsoft Graph API 有速率限制：
- **每个应用程序的限制**：每小时 130,000 次请求
- **每个用户的限制**：根据工作负载而定
- **节流**：429 状态码会触发自动重试

该技能会自动使用指数退避策略来处理节流。

## 安全考虑

1. **令牌安全**：令牌以受限的文件权限（0600）存储
2. **每个账户的隔离**：每个账户都有单独的令牌存储
3. **权限限制**：仅请求所需的最低权限
4. **令牌刷新**：令牌自动轮换，旧令牌失效
5. **客户端密钥**：不会被记录或公开；以 0600 权限存储
6. **多租户**：此设置仅适用于您的组织

## 故障排除

### 多账户问题

**“未指定账户且未设置默认账户”**
```bash
# Set a default account
node accounts.js default work

# Or always specify --account=
node calendar.js today --account=work
```

**“账户未找到”**
```bash
# List available accounts
node accounts.js list

# Add the missing account
node accounts.js add <name> <tenant> <client> <secret>
```

**认证过期**
```bash
# Check status
node auth.js status --account=work

# Re-authenticate
node auth.js login --account=work
```

### 常见问题

**“AADSTS700016：应用程序在目录中未找到”**
- 确认租户 ID 与您的 Azure AD 租户匹配
- 确保应用程序注册未被删除

**“AADSTS65001：用户未同意”**
- 完成设备代码流程认证
- 如果组织有要求，请检查管理员是否已同意

**“AADSTS700082：刷新令牌过期”**
- 使用设备代码流程重新认证
- 检查令牌存储文件的权限

**“403 禁止访问”**
- 确认 Azure 中已授予 API 权限
- 检查是否需要管理员同意

请参阅 [设置指南](references/setup-guide.md) 和 [MULTI-ACCOUNT.md](MULTI-ACCOUNT.md) 以获取详细的故障排除信息。

## 限制

- **附件大小**：每个附件最大 4MB（API 限制）
- **电子邮件收件人**：每封邮件最多 500 个收件人
- **日历事件**：仅限于未来 1,095 天内的事件
- **批量操作**：每次最多 20 个请求

## 命令参考

### 账户管理
```bash
node accounts.js list                           # List all accounts
node accounts.js add <name> <tenant> <client> <secret> [email] [desc]
node accounts.js remove <name>                  # Remove account
node accounts.js default <name>                 # Set default
node accounts.js import-legacy                  # Import v1.0.0 setup
```

### 认证
```bash
node auth.js login [--account=name]            # Authenticate
node auth.js status [--account=name]           # Check status
node auth.js token [--account=name]            # Get access token
```

### 电子邮件
```bash
node email.js recent [count] [--account=name]
node email.js search "query" [--account=name]
node email.js from email@domain [--account=name]
node email.js read <id> [--account=name]
```

### 日历
```bash
node calendar.js today [--account=name]
node calendar.js week [--account=name]
```

### 发送和管理
```bash
node send-email.js send <to> <subject> <body> [--account=name]
node send-email.js reply <message-id> <body> [--account=name]
node cancel-event.js <event-id> [comment] [--account=name]
```

## 资源

### 文档文件
- [MULTI-ACCOUNT.md](MULTI-ACCOUNT.md) - 完整的多账户使用指南
- [CHANGELOG.md](CHANGELOG.md) - 版本历史和更改
- [CREDITS.md](CREDITS.md) - 致谢和归属信息
- [references/setup-guide.md](references/setup-guide.md) - Azure 应用注册指南
- [references/permissions.md](references/permissions.md) - 安全和权限参考

### Microsoft 资源
- **Microsoft Graph API 文档**：https://learn.microsoft.com/en-us/graph/api/overview
- **委托权限与应用程序权限**：https://learn.microsoft.com/en-us/graph/auth/auth-concepts
- **速率限制**：https://learn.microsoft.com/en-us/graph/throttling

## 致谢

**原始技能：** 来自 ClawHub 社区的 office365-connector v1.0.0

**多账户增强（v2.0.0）：** Matthew Gordon ([matt@workandthrive.ai](mailto:matt@workandthrive.ai))

感谢 Matthew Gordon 对多账户功能的增强，这使得该技能对咨询师、自由职业者以及需要管理多个工作身份的用户更加有用！

请参阅 [CREDITS.md](CREDITS.md) 以获取完整的致谢信息。

## 许可证

该技能保持与原始技能的许可证兼容性。详情请参见 [CREDITS.md](CREDITS.md)。