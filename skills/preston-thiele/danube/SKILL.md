---
name: tools-marketplace
description: 你所有的工具都可以使用，但不需要使用任何密码。通过 Danube 的 MCP 服务（如 Gmail、Slack、GitHub、Notion 等），你可以访问这些工具的功能。你可以搜索所需的工具，验证用户身份，使用相应的参数执行操作，并优雅地处理可能出现的错误。
license: MIT
compatibility: openclaw
metadata:
  author: danube
  version: "1.1.0"
  tags: [danube, mcp, apis, tools]
---

# 使用 Danube Tools

Danube Tools 可以帮助您管理所有常用的工具，而无需记住各自的密码。通过 Danube 的 MCP（Management Console）集成，您可以轻松连接到 Gmail、Slack、GitHub、Notion、Google Calendar 以及另外 39 种服务。

**设置：** 如果尚未配置，请运行 `bash scripts/setup.sh` 以将 Danube MCP 添加到 OpenClaw 中。

## 使用场景

当用户需要执行以下操作时，可以使用 Danube Tools：
- 发送电子邮件、Slack 消息或通知
- 与云服务（如 GitHub、Notion、Google Sheets）进行交互
- 管理日历、表单、链接和联系人
- 生成图片、翻译文本、转录音频
- 搜索网页、查询天气信息、浏览预测市场数据
- 执行任何外部 API 操作

**不适用场景：** 本地文件操作、计算任务或非 API 相关的任务。

## 核心工作流程

每次使用工具时，都会遵循以下步骤：

### 1. 搜索工具

使用 `search_tools()` 功能通过自然语言查询所需的工具：

```python
search_tools("send email")          # → Gmail - Send Email, SendGrid, Resend
search_tools("create github issue") # → GitHub - Create Issue
search_tools("send slack message")  # → Slack - Post Message
search_tools("calendar events")     # → Google Calendar
```

### 2. 验证身份

如果工具需要用户名和密码，请引导用户完成身份验证：

```
"To use Gmail, you need to connect your account first.

Visit: https://danubeai.com/dashboard
1. Go to Tools section
2. Find Gmail and click 'Connect'
3. Follow the OAuth flow

Let me know when you're ready!"
```

**在执行任何操作之前，请务必先验证用户的身份。**

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

- **成功：** 显示操作结果
- **身份验证错误：** 提供详细的错误信息
- **其他错误：** 显示具体的错误原因

## 常用工具示例

- **电子邮件工具（Gmail、SendGrid、Resend）**
- **Slack 工具**
- **GitHub 工具**
- **日历工具**

## 最佳实践

- **务必先搜索**：始终使用 `search_tools()` 功能来查找工具，不要直接使用工具的 ID。
- **验证身份**：在执行任何操作前，请确认用户的凭据是否正确。
- **明确操作内容**：例如，应明确说明“发送邮件给 john@example.com”，而不仅仅是简单地说“操作完成”。
- **妥善处理错误**：提供具体的解决方案，而不仅仅是错误信息。

### 注意事项

- **不要在没有搜索的情况下直接使用工具**。
- **不要在未经确认的情况下自动执行操作**。
- **不要给出模糊的回应（如“错误”或“操作完成”）**。
- **务必进行身份验证检查**。

## 可用的 MCP 工具

| 工具 | 功能 |
|------|---------|
| `list_services` | 查看所有可用的 44 种服务 |
| `search_tools` | 通过自然语言查询工具 |
| `get_service_tools` | 列出特定服务的所有工具 |
| `execute_tool` | 带参数执行工具 |
| `search_contacts` | 查找用户的联系人 |

## 可用的服务（共 44 种）

- **通信与邮件**：Gmail、Slack、SendGrid、Resend、Loops、AgentMail
- **开发与 DevOps**：GitHub、Supabase、DigitalOcean（Droplets、数据库、应用平台、Kubernetes、网络服务、账户管理、Insights、市场平台）、Stripe、Apify
- **生产力工具**：Notion、Google Calendar、Google Sheets、Monday、Typeform、Bitly
- **AI 与机器学习**：Replicate、Together AI、Stability AI、AssemblyAI、Remove.bg
- **搜索与数据**：Exa、Exa Websets、Firecrawl、Serper、Context7、Microsoft Learn、AlphaVantage
- **翻译工具**：DeepL
- **公共数据（无需身份验证）**：Hacker News、Open-Meteo Weather、OpenWeather、REST Countries、Polymarket、Kalshi

## 错误处理

- **身份验证错误（401）**：提示用户重新输入凭据。
- **缺少参数**：提示用户补充所需的参数。
- **达到请求频率限制**：提示用户稍后再试。

## 多步骤工作流程

某些任务可能需要结合多个工具来完成：

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

- **请求身份验证**：发送请求以获取用户授权。
- **确认操作**：在执行操作前请求用户的确认。
- **报告操作结果**：在操作完成后通知用户结果。

## 快速参考

- **工作流程**：详细说明工具使用的步骤。
- **关键 URL**：提供访问 MCP 服务器、仪表盘和各种服务的链接。
- **调试工具**：提供重启 OpenClaw 服务器或检查错误的命令。

---

（注：由于文件内容较长，部分代码块（如 ````python
search_tools("send email")          # → Gmail - Send Email, SendGrid, Resend
search_tools("create github issue") # → GitHub - Create Issue
search_tools("send slack message")  # → Slack - Post Message
search_tools("calendar events")     # → Google Calendar
````）在实际翻译中可能保持不变，因为它们通常是占位符或具体代码示例，不需要逐行翻译。）