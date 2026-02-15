---
name: tools-marketplace
description: 您可以使用 Danube 的 44 API 和 MCP 服务（如 Gmail、Slack、GitHub、Notion 等）来管理您的所有工具。通过 MCP，您可以搜索工具、验证用户身份、参数化执行操作，并优雅地处理可能出现的错误。
license: MIT
compatibility: openclaw
metadata:
  author: danube
  version: "1.2.0"
  tags: [danube, mcp, apis, tools]
---

# 使用 Danube 工具

Danube 工具可以满足您的所有需求，无需您手动输入任何密码。通过 Danube 的 MCP（Multi-Channel Platform）集成，您可以轻松连接到 Gmail、Slack、GitHub、Notion、Google Calendar 以及另外 39 种服务。

**设置：** 按照以下“代理认证流程”操作，或运行 `bash scripts/setup.sh` 文件进行手动设置。

## 代理认证流程（推荐设置）

**通过编程方式自动认证**（无需手动复制粘贴）：

1. **请求设备代码**（无需认证）：
```python
# POST https://api.danubeai.com/v1/auth/device/code
# Body: {"client_name": "OpenClaw Agent"}
#
# Response:
# {
#   "device_code": "abc123...",      ← keep this (for polling)
#   "user_code": "XKFN-3HTP",       ← show this to the user
#   "verification_url": "https://danubeai.com/device",
#   "expires_in": 600,
#   "interval": 5
# }
```

2. **提示用户进行授权**：
```
"To connect Danube, please:
1. Open https://danubeai.com/device
2. Sign in (or create a free account)
3. Enter this code: XKFN-3HTP

I'll wait while you authorize..."
```

3. **每隔 5 秒轮询一次 API 密钥**：
```python
# POST https://api.danubeai.com/v1/auth/device/token
# Body: {"device_code": "abc123..."}
#
# 428 → authorization_pending (keep polling)
# 410 → expired_token (start over)
# 200 → success! {"api_key": "dk_...", "key_prefix": "dk_xxxxx"}
```

4. **保存 API 密钥**：
```bash
export DANUBE_API_KEY="dk_..."
echo 'export DANUBE_API_KEY="dk_..."' >> ~/.zshrc
```

设备代码的有效期为 10 分钟。如果过期，请从第 1 步重新开始。

## 使用场景

当用户需要执行以下操作时，可以使用 Danube：
- 发送电子邮件、Slack 消息或通知
- 与云服务（如 GitHub、Notion、Google Sheets）交互
- 管理日历、表单、链接和联系人
- 生成图片、翻译文本、转录音频
- 搜索网页、查询天气信息、浏览预测市场数据
- 执行任何外部 API 操作

**不适用场景：** 本地文件操作、计算任务或非 API 相关的任务。

## 核心工作流程

所有工具的操作都遵循以下步骤：

### 1. 搜索工具

使用 `search_tools()` 函数通过自然语言查询工具：
```python
search_tools("send email")          # → Gmail - Send Email, SendGrid, Resend
search_tools("create github issue") # → GitHub - Create Issue
search_tools("send slack message")  # → Slack - Post Message
search_tools("calendar events")     # → Google Calendar
```

### 2. 检查认证状态

如果工具需要认证信息，请引导用户完成认证流程：
```
"To use Gmail, you need to connect your account first.

Visit: https://danubeai.com/dashboard
1. Go to Tools section
2. Find Gmail and click 'Connect'
3. Follow the OAuth flow

Let me know when you're ready!"
```

**在执行任何操作之前，请务必检查认证状态。**

### 3. 收集所需参数

询问用户是否需要输入任何缺失的参数：
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

- **成功**：
```
"✅ Email sent successfully to user@example.com!"
```

- **认证错误**：
```
"🔐 Authentication failed. Reconnect Gmail at:
https://danubeai.com/dashboard → Tools → Gmail"
```

- **其他错误**：
```
"⚠️ Failed: [error]. Let me help troubleshoot..."
```

## 常见操作模式

### 邮件工具（Gmail、SendGrid、Resend）
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

### Slack 工具
```
User: "Send a message to #general about the deployment"

1. search_tools("slack send message") → Find Slack - Post Message
2. Check Slack authentication
3. search_tools("slack list channels") → Get channel list
4. execute_tool() to list channels → Find #general channel ID
5. Confirm: "I'll post to #general. Proceed?"
6. execute_tool() to post message
7. Report: "✅ Message posted to #general!"
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
- **执行前检查认证状态**：在执行任何操作前，请验证用户的认证信息。
- **确认操作内容**：在发送邮件或处理问题之前，务必获得用户的确认。
- **提供详细信息**：例如，明确说明邮件发送给谁（如 “发送邮件至 john@example.com”），而不仅仅是简单地说 “操作完成”。
- **妥善处理错误**：除了显示错误信息外，还要提供具体的解决方法。

### 不推荐的做法：

- 不要在未进行搜索的情况下直接使用工具。
- 未经用户确认就自动执行操作。
- 给出模糊的错误响应（如 “错误” 或 “操作完成”）。
- 跳过认证检查。

## 可用的 MCP 工具

| 工具 | 功能 |
|------|---------|
| `list_services` | 查看所有 44 种可用服务 |
| `search_tools` | 通过自然语言查询工具 |
| `get_service_tools` | 列出特定服务的所有工具 |
| `execute_tool` | 带参数执行工具 |
| `search_contacts` | 查找用户的联系人 |

## 可用的服务（共 44 种）

**通信与邮件：** Gmail、Slack、SendGrid、Resend、Loops、AgentMail

**开发与 DevOps：** GitHub、Supabase、DigitalOcean（Droplets、数据库、应用程序平台、Kubernetes、网络服务、账户管理、Insights、市场平台）、Stripe、Apify

**生产力工具：** Notion、Google Calendar、Google Sheets、Monday、Typeform、Bitly

**人工智能与机器学习：** Replicate、Together AI、Stability AI、AssemblyAI、Remove.bg

**搜索与数据：** Exa、Exa Websets、Firecrawl、Serper、Context7、Microsoft Learn、AlphaVantage

**翻译：** DeepL

**公开数据（无需认证）：** Hacker News、Open-Meteo Weather、OpenWeather、REST Countries、Polymarket、Kalshi

## 错误处理

- **认证错误（401）**：
```
"🔐 [Service] requires authentication.
Visit https://danubeai.com/dashboard → Tools → [Service] → Connect"
```

- **参数缺失**：
```
"I need:
• [param1]: [description]
• [param2]: [description]"
```

- **请求频率限制**：
```
"⚠️ Hit rate limit for [Service].
• Try again in a few minutes
• Use alternative service
• Break into smaller batches"
```

## 多步骤工作流程

有些任务可能需要使用多个工具来完成：
```
User: "Post a summary of today's GitHub commits to Slack"

1. search_tools("github commits") → Get tool
2. execute_tool() → Fetch commits
3. Format into summary
4. search_tools("slack post message") → Get Slack tool
5. search_tools("slack list channels") → Find target channel
6. execute_tool() → Post to Slack
7. Report: "✅ Posted summary of 5 commits to #dev-updates!"
```

## 通信模板

- **请求认证**：
```
"To use [Service], connect your account:
1. Visit https://danubeai.com/dashboard
2. Tools → [Service] → Connect
3. Come back when ready!"
```

- **确认操作执行**：
```
"I'll [action] using [Tool].
Parameters: [list]
Proceed?"
```

- **报告操作结果**：
```
"✅ Done!
[Specific result]
[Link if applicable]"
```

## 快速参考

- **工作流程**：
```
1. User requests action
2. search_tools() → Find tool
3. Check authentication → Guide if needed
4. Gather parameters → Ask for missing info
5. Confirm → Get approval
6. execute_tool() → Run it
7. Report → Success or error
```

- **主要网址**：
  - **MCP 服务器**：https://mcp.danubeai.com/mcp
  - **控制面板**：https://danubeai.com/dashboard
  - **连接服务**：https://danubeai.com/dashboard → Tools

- **调试**：
  - 重启服务：`openclaw gateway restart`
  - 检查错误：`openclaw doctor`
  - 验证 API 密钥：https://danubeai.com/dashboard