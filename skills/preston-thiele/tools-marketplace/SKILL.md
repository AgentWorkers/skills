---
name: tools-marketplace
description: 通过 MCP（Management Console）使用 Danube 提供的 100 多个 API 工具（如 Gmail、GitHub、Notion 等）。您可以搜索所需的工具，验证其认证信息，使用参数执行相关操作，并优雅地处理可能出现的错误。
license: MIT
compatibility: openclaw
metadata:
  author: danube
  version: "1.0.0"
  tags: [danube, mcp, apis, tools]
---

# 使用 Danube 工具

通过 Danube 的 MCP 集成，您可以访问 100 多种针对 Gmail、GitHub、Notion、Google 日历等服务的 API 工具。

**设置：** 如果尚未配置，请运行 `bash scripts/setup.sh` 以将 Danube MCP 添加到 OpenClaw 中。

## 适用场景

当用户需要执行以下操作时，可以使用 Danube：
- 发送电子邮件、创建问题、管理日历
- 与云服务（如 GitHub、Notion、Google Drive）进行交互
- 执行任何外部 API 操作

**不适用场景：** 本地文件操作、计算任务或非 API 相关的任务。

## 核心工作流程

所有工具的使用都遵循以下步骤：

### 1. 搜索工具

使用 `search_tools()` 函数进行自然语言查询：

```python
search_tools("send email")        # → Gmail, Outlook
search_tools("create github issue") # → GitHub - Create Issue
search_tools("calendar events")   # → Google Calendar
```

### 2. 检查身份验证

如果工具需要凭据，请指导用户完成身份验证：

```
"To use Gmail, you need to connect your account first.

Visit: https://danubeai.com/dashboard
1. Go to Tools section
2. Find Gmail and click 'Connect'
3. Follow the OAuth flow

Let me know when you're ready!"
```

**在执行任何操作之前，请务必检查身份验证状态。**

### 3. 收集所需参数

询问用户是否缺少任何必要的参数：

```
User: "Send an email"
You: "I can help! I need:
     - Who should I send it to?
     - What's the subject?
     - What should the message say?"
```

### 4. 执行工具

```python
execute_tool(
  tool_id="gmail-send-email-uuid",
  parameters={
    "to": "user@example.com",
    "subject": "Meeting",
    "body": "Confirming our 2pm meeting."
  }
)
```

### 5. 处理响应

- **成功：** 
  ```
"✅ Email sent successfully to user@example.com!"
```

- **身份验证错误：** 
  ```
"🔐 Authentication failed. Reconnect Gmail at:
https://danubeai.com/dashboard → Tools → Gmail"
```

- **其他错误：** 
  ```
"⚠️ Failed: [error]. Let me help troubleshoot..."
```

## 常见操作模式

### 邮件工具
```
User: "Email john@example.com about the project"

1. search_tools("send email") → Find Gmail
2. Check Gmail authentication
3. Extract: to="john@example.com", subject="Project"
4. Ask: "What should the message say?"
5. Confirm: "I'll send email to john@example.com. Proceed?"
6. execute_tool()
7. Report: "✅ Email sent!"
```

### GitHub 工具
```
User: "Create issue about the login bug"

1. search_tools("github create issue")
2. Check GitHub authentication
3. Ask: "Which repository?"
4. Ask: "Describe the bug?"
5. execute_tool()
6. Report: "✅ Issue created: [link]"
```

### 日历工具
```
User: "What's on my calendar today?"

1. search_tools("calendar events")
2. Check authentication
3. execute_tool(date=today)
4. Format results:
   "Here's your schedule:
   • 9:00 AM - Team standup
   • 2:00 PM - Client meeting"
```

## 最佳实践

- **务必先搜索**：始终使用 `search_tools()` 函数来查找工具，不要直接使用工具 ID。
- **检查身份验证**：在执行操作前验证用户的凭据。
- **确认操作**：在发送邮件、创建问题等操作前获取用户的确认。
- **提供详细信息**：例如，应明确说明“邮件已发送至 john@example.com”，而不仅仅是简单地说“操作完成”。
- **妥善处理错误**：除了显示错误信息外，还应提供具体的解决方案。

### 不应做的行为：
- 不要未经搜索就直接使用工具。
- 未经确认就自动执行操作。
- 给出模糊的响应（如“错误”或“操作完成”）。
- 跳过身份验证步骤。

## 可用工具

| 工具 | 功能 |
|------|---------|
| `list_services` | 浏览可用服务 |
| `search_tools` | 根据查询条件查找工具 |
| `get_service_tools` | 获取特定服务的工具列表 |
| `execute_tool` | 带参数执行工具 |
| `search_contacts` | 查找用户的联系人 |

## 错误处理

- **身份验证错误（401）：** 
  ```
"🔐 [Service] requires authentication.
Visit https://danubeai.com/dashboard → Tools → [Service] → Connect"
```

- **缺少参数：** 
  ```
"I need:
• [param1]: [description]
• [param2]: [description]"
```

- **请求速率限制：** 
  ```
"⚠️ Hit rate limit for [Service].
• Try again in a few minutes
• Use alternative service
• Break into smaller batches"
```

## 多步骤工作流程

某些任务可能需要使用多个工具来完成：

```
User: "Email me a summary of today's GitHub commits"

1. search_tools("github commits") → Get tool
2. execute_tool() → Fetch commits
3. Format into summary
4. search_tools("send email") → Get Gmail
5. execute_tool() → Send email
6. Report: "✅ Sent summary of 5 commits!"
```

## 通信模板

- **请求身份验证：** 
  ```
"To use [Service], connect your account:
1. Visit https://danubeai.com/dashboard
2. Tools → [Service] → Connect
3. Come back when ready!"
```

- **确认操作结果：** 
  ```
"I'll [action] using [Tool].
Parameters: [list]
Proceed?"
```

- **报告操作成功：** 
  ```
"✅ Done!
[Specific result]
[Link if applicable]"
```

## 快速参考

- **工作流程：** 
  ```
1. User requests action
2. search_tools() → Find tool
3. Check authentication → Guide if needed
4. Gather parameters → Ask for missing info
5. Confirm → Get approval
6. execute_tool() → Run it
7. Report → Success or error
```

- **关键 URL：**
  - **MCP 服务器：** https://mcp.danubeai.com/mcp
  - **控制面板：** https://danubeai.com/dashboard
  - **连接服务：** https://danubeai.com/dashboard → 工具
- **调试：**
  - 检查 API 密钥：`cat ~/.openclaw/.env | grep DANUBE`
  - 重启服务：`openclaw gateway restart`
  - 查看错误信息：`openclaw doctor`