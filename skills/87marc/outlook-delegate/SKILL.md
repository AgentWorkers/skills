---
name: outlook-delegate
description: 通过 Microsoft Graph API，您可以阅读、搜索和管理 Outlook 邮件及日历，并支持代理访问功能。支持以“自己”的身份发送邮件、以“所有者”的身份发送邮件（Send As），以及代表所有者发送邮件（Send on Behalf）。该功能已针对代理访问进行了修改，详情请参考：https://clawhub.ai/jotamed/outlook
version: 1.1.0
author: 87marc
---

# Outlook 代理技能

通过 Microsoft Graph API，以代理身份访问其他用户的 Outlook/Microsoft 365 邮箱和日历。支持三种发送模式：以代理自身身份发送、以所有者身份发送或代表所有者发送。

## 代理架构

此技能适用于以下场景：
- **您的 AI 助手**（即代理）拥有自己的 Microsoft 365 账户；
- **所有者**已授予助手对其邮箱/日历的代理访问权限；
- 助手可以以自身身份、所有者身份或代表所有者身份发送邮件。

### 发送模式说明

三种模式都使用相同的 Graph API 调用（`/users/{delegate}/sendMail`），并设置 `from` 字段。**“以代理自身身份发送”（Send As）和“代表所有者发送”（Send On Behalf）之间的区别完全取决于 Exchange 授予的权限，而非 API 端点**。

| 模式 | 命令 | 所需 Exchange 权限 | `from` 字段 | `sender` 字段 | 收件人看到的内容 |
|------|---------|------------------------------|--------------|----------------|---------------------|
| 以代理自身身份发送 | `send` | （无需额外权限） | 代理 | 代理 | “发件人：助手” |
| 以所有者身份发送（Send As） | `send-as` | **仅需要 SendAs 权限** | 所有者 | 所有者 | “发件人：所有者” |
| 代表所有者发送 | `send-behalf` | **仅需要 SendOnBehalf 权限** | 所有者 | 代理 | “发件人：助手代表所有者” |

> **⚠️ 重要提示：** 请不要同时授予 SendAs 和 SendOnBehalf 权限。如果同时授予这两种权限，Exchange 会始终使用 SendAs，且“代表所有者”这一提示将不会显示。请根据您的需求选择其中一种权限。

### 内部工作原理

当您调用 `send-as` 或 `send-behalf` 时，该技能会通过代理的端点发送邮件，并在 `from` 字段中设置所有者信息。Microsoft Graph 会自动将 `sender` 属性设置为已认证的用户（即助手）。收件人是否看到“代表所有者”这一提示，完全取决于 Exchange 的权限设置：
- **具有 SendAs 权限** → Graph 会将 `sender` 和 `from` 都设置为所有者。此时不会显示代理信息。
- **具有 SendOnBehalf 权限** → Graph 会将 `sender` 设置为助手，`from` 设置为所有者。此时收件人会看到“代表所有者”这一提示。

## 配置

### 配置文件：`~/.outlook-mcp/config.json`

```json
{
  "client_id": "Microsoft Entra ID 应用注册客户端 ID",
  "client_secret": "Microsoft Entra ID 应用注册客户端密钥",
  "tenant_id": "您的 Microsoft Entra 租户 ID" (设置时会自动检测),
  "owner_email": "助手作为代理访问的邮箱地址",
  "owner_name": "所有者的显示名称（用于 `from` 字段）",
  "delegate_email": "助手自己的电子邮件地址",
  "delegate_name": "助手的显示名称",
  "timezone": "日历操作的 IANA 时区（例如：America/New_York, Europe/London, UTC)"
}
```

## 设置要求

### 1. Microsoft Entra ID 应用注册

在 Azure 门户中创建应用注册：
1. 访问 portal.azure.com → Microsoft Entra ID → 应用注册
2. 新建注册：
   - 名称："AI Assistant Mail Access"
   - 支持的账户类型：**“仅此组织目录内的账户”**（单租户）
   - 重定向 URI：`http://localhost:8400/callback`
3. 记下 **应用程序（client）ID** 和 **目录（tenant）ID**。

### 2. 配置 API 权限

在您的应用设置中 → API 权限 → 添加权限 → Microsoft Graph → 代理权限：
- **所有模式都需要**：
  - `Mail.ReadWrite` — 读取/写入助手自己的邮件
  - `Mail.Send` — 以助手身份发送邮件
  - `Calendars.ReadWrite` — 读取/写入日历
  - `User.Read` — 读取自己的个人资料
  - `offline_access` — 刷新令牌

- **代理访问需要**：
  - `Mail.ReadWrite.Shared` — 读取/写入共享邮箱
  - `Mail.Send.Shared` — 代表他人发送邮件
  - `Calendars.ReadWrite.Shared` — 读取/写入共享日历

点击 **“授予管理员同意”**（需要管理员权限）。

### 3. 创建客户端密钥

1. 在证书和密钥设置中创建新的客户端密钥
2. 描述："AI Assistant"
3. 设置有效期
4. **立即复制密钥值**（仅显示一次）

### 4. 授予 Exchange 代理权限

所有者（或管理员）必须通过 PowerShell 授予助手相应的权限。

**首先选择您的发送模式**，然后授予相应的权限：

**然后选择以下其中一种权限——切勿同时授予两种权限：**

**验证权限：**

### 权限概览

| 功能 | Graph 权限 | Exchange 权限 |
|--------|-----------------|---------------------|
| 读取所有者的邮件 | `Mail.ReadWrite.Shared` | FullAccess |
| 以代理自身身份发送 | `Mail.Send` | （无需额外权限） |
| 以所有者身份发送 | `Mail.Send.Shared` | 仅需要 SendAs 权限 |
| 代表所有者发送 | `Mail.Send.Shared` | 仅需要 SendOnBehalf 权限 |
| 读取/写入所有者的日历 | `Calendars.ReadWrite.Shared` | Editor |

## 使用方法

### 令牌管理

### 读取所有者的邮件

### 管理所有者的邮件

### 发送邮件

**以代理自身身份发送：**
收件人看到的内容：**“发件人：AI Assistant <assistant@domain.com>”

**以所有者身份发送（需要 SendAs 权限）：**
收件人看到的内容：**“发件人：所有者 <owner@domain.com>”

**代表所有者发送（需要 SendOnBehalf 权限）：**
收件人看到的内容：**“发件人：AI Assistant 代表所有者 <owner@domain.com>”

### 草稿

### 文件夹和日历操作

### 查看日历事件：

### 创建日历事件：
日期格式：`YYYY-MM-DDTHH:MM`（例如：`2026-01-26T10:00`

### 管理日历事件：
字段：`subject`（主题）、`location`（地点）、`start`（开始时间）、`end`（结束时间）

## 发送邮件的行为

发送邮件的副本保存位置取决于使用的 API 端点，而非发送模式：

| 命令 | 使用的 API 端点 | 保存位置 |
|---------|--------------|----------|
| `send`（以代理自身身份发送） | `/users/{delegate}/sendMail` | 代理的已发送邮件文件夹 |
| `send-as` | `/users/{delegate}/sendMail` | 代理的已发送邮件文件夹 |
| `send-behalf` | `/users/{delegate}/sendMail` | 代理的已发送邮件文件夹 |
| 所有草稿的发送 | `/users/{owner}/messages/{id}/send` | 所有者的已发送邮件文件夹 |

**管理员可以通过以下方式配置 Exchange，使副本也保存在所有者的已发送邮件文件夹中：**

## 故障排除

- **“访问被拒绝”或“403 禁止访问”**：检查助手是否具有对所有者邮箱的 `MailboxPermission` 权限。
- **“ErrorSendAsDenied”**：可能是因为缺少 SendAs 或 SendOnBehalf 权限。请运行上述 PowerShell 命令。
- **邮件未显示“代表所有者”**：可能是同时授予了 SendAs 和 SendOnBehalf 权限。在这种情况下，Exchange 会始终使用 SendAs，导致“代表所有者”提示无法显示。如果需要显示该提示，请取消 SendAs 权限。
- **“找不到邮箱”**：请确认 `config.json` 中的 `owner_email` 是否正确。
- **“AADSTS90002: 租户未找到”**：请检查 `config.json` 中的 `tenant_id` 是否与您的 Microsoft Entra 租户匹配。
- **令牌过期**：运行 `outlook-token.sh refresh` 命令刷新令牌。
- **日历时区设置错误**：请更新 `config.json` 中的 `timezone`（使用 IANA 格式，例如：`America/New_York`）。

## 安全注意事项

1. **凭证保护**：`~/.outlook-mcp/` 目录的权限设置为 700，凭证文件的权限设置为 600。
2. **防止信息泄露**：令牌刷新和 Exchange 操作通过标准输入（stdin）传递凭证，不会通过命令行参数。
3. **输入验证**：所有用户输入都会通过 `jq` 进行 JSON 转义，以防止注入攻击。
4. **审计记录**：所有操作都会记录在所有者的日历审计日志中。
5. **权限限制**：助手只能访问明确授予的权限范围。
6. **权限撤销**：所有者可以通过 Exchange PowerShell 或 Outlook 设置撤销代理权限。

## 相关文件

- `~/.outlook-mcp/config.json` — 配置信息（客户端 ID、租户 ID、邮箱地址、时区）
- `~/.outlook-mcp/credentials.json` — OAuth 令牌（访问权限和刷新令牌）

## 更新日志

### v1.1.0
- **修复**：回复命令不再发送重复邮件（移除了发送无效邮件的代码）。
- **修复**：所有回复/转发操作现在都使用正确的 Graph API 调用顺序（`createReply/createForward → patch from → send`）。
- **修复**：`send-as` 和 `send-behalf` 的文档已更新——其行为取决于 Exchange 权限，而非 API 端点。
- **修复**：`send-draft-behalf` 命令在发送前不再删除草稿（防止发送失败时数据丢失）。
- **修复**：所有用户输入现在都会通过 `jq` 进行 JSON 转义，以防止注入攻击和格式错误。
- **修复**：对所有写入操作强制执行凭证文件权限（`chmod 600`）。
- **修复**：配置目录的权限设置（`chmod 700`）。
- **修复**：客户端密钥不再在进程列表中显示（通过 stdin 传递）。
- **修复**：日历 `events` 命令现在只显示未来的事件。
- **修复**：已发送邮件的保存位置说明已更新。
- **修复**：版本号已更新。
- 更新了 Microsoft Entra ID 的命名（之前称为 Azure Active Directory）。
- 设置指南现在明确警告不要同时授予 SendAs 和 SendOnBehalf 权限。
- 更新了撤销权限的命令（`GrantSendOnBehalfTo` 使用 `{Remove=...}` 语法）。

### v1.0.0
- 支持三种发送模式：以代理自身身份发送、以所有者身份发送、代表所有者发送。
- 使用租户特定的身份验证（不再使用 `/common` 端点）。
- 日历操作的时区可配置。
- 显示所有者和代理的显示名称。
- 草稿保存在所有者的邮箱中。
- 提供了详细的 PowerShell 设置命令。
- 基于 jotamed 的 outlook v1.3.0 版本（https://clawhub.ai/jotamed/outlook）开发。