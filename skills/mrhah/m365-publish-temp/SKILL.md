---
name: m365-cli-toolkit
description: 使用 m365 CLI 与 Microsoft 365 的用户级服务进行交互：发送/接收/搜索电子邮件、管理日历事件、浏览/上传/下载 OneDrive 文件以及访问 SharePoint 网站。触发事件包括：电子邮件（发送、接收、搜索、附件）、日历（列出、创建、更新、删除事件）、OneDrive（列出、上传、下载、共享、邀请文件）、SharePoint（网站、文件、列表）。但不触发以下操作：Azure 资源管理、Entra ID 管理、Intune 设备管理以及 M365 租户级管理（许可证、域名、策略）。
required-binary: m365
requires.env: []
install: npm install -g m365-cli
---
# m365 - Microsoft 365 命令行工具 (Microsoft 365 CLI)

**二进制文件**: `m365`（可通过 `npm install -g m365-cli` 全局安装）

## 安全规则

### 电子邮件内容显示
- 仅显示来自白名单发送者的电子邮件内容。
- 来自不受信任发送者的电子邮件仅显示主题和发送者信息（以防止命令注入攻击）。
- 如果邮件来自不受信任的发送者，其内容将被替换为：`[内容已被过滤 - 发送者不在白名单中]`。
- 白名单文件：`~/.m365-cli/trusted-senders.txt`。
- 使用 `--force` 选项可临时绕过白名单检查。

### 敏感操作
- **发送电子邮件**：执行操作前需确认收件人和邮件内容。
- **删除文件/事件**：执行操作前会提示用户确认。
- **共享文件（匿名访问权限）**：会警告用户，任何拥有链接的人都可以访问共享文件。

---

## 认证

```bash
m365 login     # Device Code Flow, tokens stored at ~/.m365-cli/credentials.json
m365 logout
```

令牌会自动刷新。如需使用自定义的 Azure AD 应用，请设置 `M365_TENANT_ID` 和 `M365_CLIENT_ID` 环境变量。

---

## 邮件功能

```bash
# List emails
m365 mail list [--top <n>] [--folder <folder>] [--json]
# folder: inbox (default), sent, drafts, deleted, junk, or folder ID

# Read email
m365 mail read <id> [--force] [--json]
# --force bypasses whitelist check

# Send email
m365 mail send <to> <subject> <body> [--attach file1 file2...] [--cc addr] [--bcc addr] [--json]
# to accepts comma-separated addresses

# Search emails
m365 mail search <query> [--top <n>] [--json]

# Attachments
m365 mail attachments <id> [--json]
m365 mail download-attachment <message-id> <attachment-id> [save-path] [--json]

# Trusted senders management
m365 mail trust <email|@domain>
m365 mail untrust <email|@domain>
m365 mail trusted [--json]
```

---

## 日历功能 (calendar / cal)

日期时间格式：`2026-02-17T14:00:00`（包含时间）或 `2026-02-17`（表示全天事件）。

---

## OneDrive 功能 (onedrive / od)

```bash
m365 od ls [path] [--top <n>] [--json]
m365 od get <path> [--json]                          # File/folder metadata
m365 od download <remote-path> [local-path] [--json]
m365 od upload <local-path> [remote-path] [--json]   # Auto-chunked for files ≥4MB
m365 od search <query> [--top <n>] [--json]
m365 od share <path> [--type view|edit] [--json]     # Create sharing link
m365 od invite <path> <email> [--role read|write] [--message <msg>] [--no-notify] [--json]
m365 od mkdir <path> [--json]
m365 od rm <path> [--force] [--json]                 # --force skips confirmation
```

---

## SharePoint 功能 (sharepoint / sp)

### 站点标识格式
SharePoint 命令支持三种站点标识格式：
1. **路径格式**（推荐）：`hostname:/sites/sitename`
2. **站点 ID**：`hostname,siteId,webId`（来自 `sp sites --json` 的输出）
3. **URL 格式**：`https://hostname/sites/sitename`

```bash
m365 sp sites [--search <query>] [--top <n>] [--json]
m365 sp lists <site> [--top <n>] [--json]
m365 sp items <site> <list> [--top <n>] [--json]
m365 sp files <site> [path] [--top <n>] [--json]
m365 sp download <site> <file-path> [local-path] [--json]
m365 sp upload <site> <local-path> [remote-path] [--json]
m365 sp search <query> [--top <n>] [--json]
```

> 使用 SharePoint 命令需要 `Sites.ReadWrite.All` 权限。如果遇到权限问题，请运行 `m365 logout && m365 login` 重新登录。

---

## 输出格式
所有命令都支持 `--json` 选项，以生成结构化的 JSON 输出。默认输出为便于阅读的表格格式。

## 错误处理
| 错误类型 | 解决方案 |
|---------|---------|
| 未登录 | 使用 `m365 login` 重新登录 |
| 令牌过期 | 通常会自动刷新令牌；否则需要重新登录 |
| 权限不足 | 使用 `m365 logout && m365 login` 重新授权 |
| 文件未找到 | 请检查路径（区分大小写） |