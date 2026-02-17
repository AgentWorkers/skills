---
name: officeclaw
description: 通过 Microsoft Graph API 连接到个人 Microsoft 账户，以管理电子邮件、日历事件和任务。当用户需要读取/写入 Outlook 邮件、管理日历约会或处理 Microsoft To-Do 任务时，可以使用此功能。
license: Apache-2.0
homepage: https://github.com/danielithomas/officeclaw
user-invocable: true
compatibility: Requires Python 3.9+, network access to graph.microsoft.com, and one-time OAuth setup
metadata:
  author: Daniel Thomas
  version: "1.0.1"
  openclaw:
    requires:
      anyBins: ["python", "python3", "officeclaw"]
      env: []
    os: ["darwin", "linux", "win32"]
---
# OfficeClaw：Microsoft Graph API集成

将您的OpenClaw代理连接到个人Microsoft账户（Outlook.com、Hotmail、Live），通过Microsoft Graph API管理电子邮件、日历和任务。

## 安装

通过PyPI安装：

```bash
pip install officeclaw
```

或使用uv安装：

```bash
uv pip install officeclaw
```

验证安装：

```bash
officeclaw --version
```

## 设置（一次性操作）

> **快速入门：** OfficeClaw自带默认的应用程序注册功能——只需运行 `officeclaw auth login` 即可开始使用，无需进行Azure设置。
>
> **高级设置：** 希望获得完全控制权？创建您自己的Azure应用程序注册（免费，约5分钟），并在`.env`文件中设置`OFFICECLAW_CLIENT_ID`。请参考[Microsoft的指南](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app)或按照以下步骤操作。

### 1. 创建Azure应用程序注册

1. 访问[entra.microsoft.com](https://entra.microsoft.com) → 应用程序注册 → 新注册
2. 应用程序名称：`officeclaw`（或您喜欢的名称）
3. 支持的账户类型：**仅限个人Microsoft账户**
4. 重定向URI：保持空白（设备代码流不需要此信息）
5. 点击**注册**
6. 复制**应用程序（客户端）ID**——这就是您的`OFFICECLAW_CLIENT_ID`
7. 转到**身份验证** → 高级设置 → **允许公共客户端流** → **是** → 保存
8. 转到**API权限** → 添加权限 → Microsoft Graph → 委托权限。根据需要选择权限：

**仅读权限（最安全）：**
- `Mail.Read`, `Calendars.Read`, `Tasks.ReadWrite`*

**完全访问权限（包括发送/删除）：**
- `Mail.Read`, `Mail.ReadWrite`, `Mail.Send`
- `Calendars.Read`, `Calendars.ReadWrite`
- `Tasks.ReadWrite`

*\*对于Microsoft To Do来说，`Tasks.ReadWrite`是最基本的权限范围——没有仅读选项。*

> **最小权限原则：** 仅授予实际需要的权限。如果您仅需要读取电子邮件和日历信息，可以跳过`Mail.ReadWrite`、`Mail.Send`和`Calendars.ReadWrite`。OfficeClaw会在缺少权限时优雅地提示错误。*

### 2. 配置环境

在您的技能目录中创建一个`.env`文件：

```bash
OFFICECLAW_CLIENT_ID=your-client-id-here

# Capability gates (disabled by default for safety)
# OFFICECLAW_ENABLE_SEND=true    # Allow sending/replying/forwarding emails
# OFFICECLAW_ENABLE_DELETE=true   # Allow deleting emails, events, and tasks
```

设备代码流不需要客户端密钥。默认情况下，写入操作（发送、删除）是被禁用的——仅启用您需要的功能。

### 3. 进行身份验证

```bash
officeclaw auth login
```

系统会显示一个URL和验证码。在浏览器中打开该URL，输入验证码，然后使用您的Microsoft账户登录。令牌将安全地存储在`~/.officeclaw/token_cache.json`文件中（权限设置为600秒）。

## 何时使用此技能

当用户需要执行以下操作时，激活此技能：

### 电子邮件操作
- **读取电子邮件**：“显示我的最新邮件”，“查找来自john@example.com的邮件”
- **发送电子邮件**：“发送邮件给...”，“回复上一封邮件”
- **管理收件箱**：“将邮件标记为已读”，“归档旧邮件”，“删除邮件”

### 日历操作
- **查看事件**：“我今天的日程安排是什么？”，“显示本周的会议”
- **创建事件**：“与...安排会议”，“在周五预约看牙医”
- **更新事件**：“将下午2点的会议推迟到下午3点”，“取消明天的站立会议”

### 任务管理
- **列出任务**：“我的待办事项有哪些？”，“显示未完成的任务”
- **创建任务**：“在任务列表中添加‘购买杂货’”，“创建一个查看报告的任务”
- **完成任务**：“将‘完成提案’标记为已完成”，“完成所有购物任务”

## 可用命令

### 身份验证

```bash
officeclaw auth login       # Authenticate via device code flow
officeclaw auth status      # Check authentication status
officeclaw auth logout      # Clear stored tokens
```

### 邮件命令

```bash
officeclaw mail list --limit 10                # List recent messages
officeclaw mail list --unread                   # List unread messages only
officeclaw mail get <message-id>               # Get specific message
officeclaw mail send --to user@example.com --subject "Hello" --body "Message text"
officeclaw mail send --to user@example.com --subject "Report" --body "Attached" --attachment report.pdf
officeclaw mail search --query "from:boss@example.com"
officeclaw mail archive <message-id>           # Archive a message
officeclaw mail mark-read <message-id>         # Mark as read
officeclaw --json mail list                    # JSON output for parsing
```

### 日历命令

```bash
officeclaw calendar list --start 2026-02-01 --end 2026-02-28
officeclaw calendar create \
  --subject "Team Meeting" \
  --start "2026-02-15T10:00:00" \
  --end "2026-02-15T11:00:00" \
  --location "Conference Room"
officeclaw calendar get <event-id>
officeclaw calendar update <event-id> --subject "Updated Meeting"
officeclaw calendar delete <event-id>
officeclaw --json calendar list --start 2026-02-01 --end 2026-02-28
```

### 任务命令

```bash
officeclaw tasks list-lists                              # List task lists
officeclaw tasks list --list-id <list-id>                # List tasks
officeclaw tasks list --list-id <list-id> --status active  # Active tasks only
officeclaw tasks create --list-id <list-id> --title "Complete report" --due-date "2026-02-20"
officeclaw tasks complete --list-id <list-id> --task-id <task-id>
officeclaw tasks reopen --list-id <list-id> --task-id <task-id>
```

## 输出格式

使用`--json`标志以获取结构化的JSON输出：

```bash
officeclaw --json mail list
```

返回结果：

```json
{
  "status": "success",
  "data": [
    {
      "id": "AAMkADEzN...",
      "subject": "Meeting Notes",
      "from": {"emailAddress": {"address": "sender@example.com"}},
      "receivedDateTime": "2026-02-12T10:30:00Z",
      "isRead": false
    }
  ]
}
```

## 错误处理

常见错误及解决方法：

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `AuthenticationError` | 未登录或令牌过期 | 运行`officeclaw auth login` |
| `AccessDenied` | 缺少权限 | 使用所需的权限范围重新登录 |
| `ResourceNotFound` | ID无效 | 验证ID是否存在 |
| `RateLimitError` | API调用次数过多 | 等待60秒后重试 |

## 对代理的指导

使用此技能时，请注意：

1. **确认破坏性操作**：在删除或发送数据前请用户确认。
2. **提供结果摘要**：不要直接显示原始JSON数据，而是提供摘要信息。
3. **优雅地处理错误**：引导用户重新登录。
4. **尊重隐私**：不要记录电子邮件内容。
5. **使用JSON格式**：如需程序化处理数据，请使用`--json`标志。
6. **批量操作**：高效处理多个项目。

## 安全性与隐私

- **默认禁用写入操作**：除非通过`OFFICECLAW_ENABLE_SEND`和`OFFICECLAW_ENABLE_DELETE`环境变量明确启用，否则发送、回复、转发和删除操作均被禁止。这可以防止意外或未经授权的写入操作。
- **无需客户端密钥**：默认使用设备代码流（公共客户端）。
- **最小权限原则**：您可以选择授予哪些Graph API权限——对于大多数使用场景，仅读权限已足够。
- **令牌安全存储**：令牌存储在`~/.officeclaw/token_cache.json`文件中，文件权限设置为600秒。
- **不存储数据**：OfficeClaw仅传递数据，不会存储电子邮件或日历内容。
- **不收集使用数据**：不会收集任何使用数据。
- **独立的Azure应用程序**：每个用户都会创建自己的Azure应用程序注册，并使用自己的客户端ID——不会共享凭证。

## 故障排除

如果技能无法正常使用，请尝试以下步骤：

1. **检查身份验证状态**：运行`officeclaw auth status`。
2. **重新登录**：运行`officeclaw auth login`。
3. **检查网络连接**：确保可以访问`graph.microsoft.com`。
4. **验证环境设置**：确认`.env`文件中设置了`OFFICECLAW_CLIENT_ID`。

## 参考资料

- [OfficeClaw在GitHub上的页面](https://github.com/danielithomas/officeclaw)
- [OfficeClaw在PyPI上的页面](https://pypi.org/project/officeclaw/)
- [Microsoft Graph API文档](https://docs.microsoft.com/graph/)
- [OpenClaw文档](https://docs.openclaw.ai)