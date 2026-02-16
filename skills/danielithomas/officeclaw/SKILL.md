---
name: officeclaw
description: 通过 Microsoft Graph API 连接到个人 Microsoft 账户，以管理电子邮件、日历事件和任务。当用户需要读取/写入 Outlook 邮件、管理日历约会或处理 Microsoft To-Do 任务时，可以使用此功能。
license: Apache-2.0
homepage: https://github.com/danielithomas/officeclaw
user-invocable: true
compatibility: Requires Python 3.9+, network access to graph.microsoft.com, and one-time OAuth setup
metadata:
  author: Daniel Thomas
  version: "1.0.0"
  openclaw: {"requires": {"anyBins": ["python", "python3", "officeclaw"]}, "os": ["darwin", "linux", "win32"]}
---
# Outclaw：Microsoft Graph API集成

将您的OpenClaw代理连接到个人Microsoft账户（Outlook.com、Hotmail、Live），以便通过Microsoft Graph API管理电子邮件、日历和任务。

## 何时使用此技能

当用户需要执行以下操作时，请激活此技能：

### 电子邮件操作
- **阅读电子邮件**：“显示我的最新邮件”，“查找来自john@example.com的邮件”
- **发送电子邮件**：“给...发送邮件”，“回复来自...的最后一封邮件”
- **管理收件箱**：“将邮件标记为已读”，“归档旧邮件”，“删除邮件”

### 日历操作
- **查看事件**：“我今天的日历有什么安排？”，“显示本周的会议”
- **创建事件**：“与...安排会议”，“在周五添加看牙医的预约”
- **更新事件**：“将下午2点的会议推迟到下午3点”，“取消明天的站立会议”

### 任务管理
- **列出任务**：“我的待办事项有哪些？”，“显示未完成的任务”
- **创建任务**：“在任务列表中添加‘购买杂货’”，“创建一个审查报告的任务”
- **完成任务**：“将‘完成提案’标记为已完成”，“完成所有购物任务”

## 先决条件

在使用此技能之前，用户必须完成以下一次性设置：
1. **Azure应用注册**：在https://entra.microsoft.com注册一个应用
2. **OAuth授权**：运行`officeclaw auth login`并批准权限
3. **环境配置**：在.env文件中设置CLIENT_ID和CLIENT_SECRET

## 可用命令

### 认证

```bash
# Authenticate (opens browser)
officeclaw auth login

# Check authentication status
officeclaw auth status

# Clear stored tokens
officeclaw auth logout
```

### 邮件命令

```bash
# List recent messages
officeclaw mail list --limit 10

# List unread messages only
officeclaw mail list --unread

# Get specific message
officeclaw mail get <message-id>

# Send email
officeclaw mail send --to user@example.com --subject "Hello" --body "Message text"

# JSON output (for parsing)
officeclaw --json mail list
```

### 日历命令

```bash
# List events in date range
officeclaw calendar list --start 2026-02-01 --end 2026-02-28

# Create event
officeclaw calendar create \
  --subject "Team Meeting" \
  --start "2026-02-15T10:00:00" \
  --end "2026-02-15T11:00:00" \
  --location "Conference Room"

# JSON output
officeclaw --json calendar list --start 2026-02-01 --end 2026-02-28
```

### 任务命令

```bash
# List task lists
officeclaw tasks list-lists

# List tasks in a list
officeclaw tasks list --list-id <list-id>

# List only active (not completed) tasks
officeclaw tasks list --list-id <list-id> --status active

# Create task
officeclaw tasks create --list-id <list-id> --title "Complete report" --due-date "2026-02-20"

# Mark task complete
officeclaw tasks complete --list-id <list-id> --task-id <task-id>

# Reopen a completed task
officeclaw tasks reopen --list-id <list-id> --task-id <task-id>
```

## 输出格式

使用`--json`标志以获得结构化的JSON输出：

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
| `AccessDenied` | 权限不足 | 使用所需的权限范围重新认证 |
| `ResourceNotFound` | ID无效 | 验证ID是否存在 |
| `RateLimitError` | API调用次数过多 | 等待60秒后重试 |

## 代理使用指南

使用此技能时，请注意以下事项：
1. **确认破坏性操作**：在删除或发送内容之前先询问用户
2. **汇总结果**：不要直接显示原始JSON数据，而是提供汇总信息
3. **优雅地处理错误**：引导用户重新认证
4. **尊重隐私**：不要记录电子邮件内容
5. **使用JSON格式**：如需程序化解析，请使用`--json`标志
6. **批量操作**：高效处理多个项目

## 代理交互示例

### 示例1：检查紧急邮件

```
User: "Do I have any urgent emails?"
Agent: I'll check your inbox.
[Runs: officeclaw --json mail list --limit 20]
Agent: You have 2 unread emails:
       • From your manager about tomorrow's deadline
       • From IT about a password reset
```

### 示例2：安排会议

```
User: "Schedule a meeting with john@example.com tomorrow at 2pm for 1 hour"
Agent: I'll create that calendar event.
[Runs: officeclaw calendar create --subject "Meeting with John" 
       --start "2026-02-13T14:00:00" --end "2026-02-13T15:00:00"]
Agent: Meeting scheduled for tomorrow at 2:00 PM.
```

### 示例3：完成任务

```
User: "Mark the 'finish slides' task as complete"
Agent: I'll mark that task as done.
[Runs: officeclaw --json tasks list --list-id <id>]
[Runs: officeclaw tasks complete --list-id <id> --task-id <id>]
Agent: Done! "Finish slides" has been marked as complete.
```

## 安全与隐私

- **令牌安全存储**：使用系统密钥环或加密文件存储令牌
- **不存储数据**：Outclaw仅传输数据，从不存储内容
- **无数据收集**：不收集任何使用数据
- **最小权限原则**：仅请求必要的权限

## 故障排除

如果此技能无法正常使用，请尝试以下步骤：
1. **检查认证状态**：运行`officeclaw auth status`
2. **重新认证**：运行`officeclaw auth login`
3. **检查网络连接**：确保可以访问`graph.microsoft.com`
4. **验证环境设置**：确认OUTCLAW_CLIENT_ID已正确设置

## 参考资料

- [Outclaw文档](https://github.com/danielithomas/officeclaw)
- [Microsoft Graph API](https://docs.microsoft.com/graph/)
- [OpenClaw](https://docs.openclaw.ai)