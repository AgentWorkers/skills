---
name: zapier-mcp
description: 通过 Zapier MCP，您可以连接 8,000 多个应用程序。该功能支持与 Clawdbot Gateway 仪表板的完整 UI 集成。在设置 Zapier 集成、连接应用程序或通过 mcporter 使用 Zapier 工具时，均可使用此功能。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["mcporter"],"clawdbot":">=2026.1.0"},"category":"integrations"}}
---
# Zapier MCP

通过 Zapier 的 MCP（Model Context Protocol）集成，您可以将您的 AI 代理连接到 8,000 多个应用程序。此功能提供以下优势：

- **完整的 UI 仪表板** — 配置您的 MCP URL、测试连接、浏览可用工具
- **无需处理 OAuth 复杂性** — Zapier 负责处理所有身份验证流程
- **MCP 集成** — 可通过 `mcporter` 访问这些工具

## 概述

Zapier MCP 将您配置的 Zapier 动作暴露为代理可以调用的工具。与 Pipedream（需要管理 OAuth 令牌）不同，Zapier MCP 使用基于 URL 的简单身份验证方式——只需粘贴您的 MCP URL 即可完成连接。

## 先决条件

1. **Zapier 账户** — 在 [zapier.com](https://zapier.com) 注册
2. **mcporter** — MCP 工具运行器（`npm install -g mcporter`）
3. **Clawdbot Gateway** — 版本需达到 v2026.1.0 或更高，并且启用了 UI 功能

## 快速入门

### 第 1 步：获取您的 Zapier MCP URL

1. 访问 [zapier.com/mcp](https://zapier.com/mcp) 并登录
2. 配置要暴露的 Zapier 动作（例如：“发送 Slack 消息”、“创建 Google Sheets 行”）
3. 复制您的个性化 MCP URL（格式类似 `https://actions.zapier.com/mcp/...`）

### 第 2 步：在 Clawdbot UI 中进行配置

1. 打开 Clawdbot 仪表板 → **工具** → **Zapier**
2. 点击 **配置**
3. 粘贴您的 MCP URL
4. 点击 **保存**

完成以上步骤后，Zapier 会验证 URL 并显示可用的工具数量。

### 第 3 步：使用您的工具

连接成功后，您可以通过 `mcporter` 使用这些工具：

```bash
# List available tools
mcporter list zapier-mcp --schema

# Call a tool
mcporter call zapier-mcp.<tool_name> --args '{"instructions": "your request"}'
```

## 使用模式

### `instructions` 参数

每个 Zapier 工具都接受一个 `instructions` 参数。Zapier 的 AI 会解析该参数以填充缺失的参数：

```bash
# ❌ Vague - may prompt for clarification
mcporter call zapier-mcp.slack_send_message \
  --args '{"instructions": "Send a message"}'

# ✅ Specific - AI can resolve parameters
mcporter call zapier-mcp.slack_send_message \
  --args '{"instructions": "Send \"Hello team!\" to the #general channel"}'
```

### `output_hint` 参数

您可以控制返回的数据内容：

```bash
mcporter call zapier-mcp.google_sheets_find_row \
  --args '{
    "instructions": "Find row where email is bob@example.com",
    "output_hint": "name, email, phone number"
  }'
```

### 常见工具模式

```bash
# Slack
mcporter call zapier-mcp.slack_send_message \
  --args '{"instructions": "Send \"Build complete!\" to #deployments"}'

# Gmail
mcporter call zapier-mcp.gmail_send_email \
  --args '{"instructions": "Send email to bob@example.com with subject \"Meeting\" and body \"See you at 3pm\""}'

# Google Sheets
mcporter call zapier-mcp.google_sheets_create_row \
  --args '{"instructions": "Add row with Name=John, Email=john@example.com to Sales Leads spreadsheet"}'

# Notion
mcporter call zapier-mcp.notion_create_page \
  --args '{"instructions": "Create page titled \"Meeting Notes\" in the Team Wiki database"}'

# Calendar
mcporter call zapier-mcp.google_calendar_create_event \
  --args '{"instructions": "Create meeting \"Team Standup\" tomorrow at 10am for 30 minutes"}'
```

## 架构

### 工作原理

1. 在 Zapier 的 MCP 仪表板中配置动作
2. Zapier 为您的账户生成一个唯一的 MCP URL
3. Clawdbot 将该 URL 保存在 `mcporter` 配置中
4. 当您调用某个工具时，`mcporter` 会向 Zapier 发送 JSON-RPC 请求
5. Zapier 执行该动作并返回结果

### 被修改的文件

| 文件位置 | 用途 |
|----------|---------|
| `~/clawd/config/mcporter.json` | 包含 Zapier URL 的 MCP 服务器配置 |

### 后端端点

此功能使用以下 gateway RPC 方法：

| 方法 | 用途 |
|--------|---------|
| `zapier.status` | 获取连接状态和工具数量 |
| `zapier.save` | 验证并保存 MCP URL |
| `zapier.test` | 测试连接 |
| `zapierdisconnect` | 从 `mcporter` 配置中移除 Zapier |
| `zapier.tools` | 列出所有可用工具 |

### SSE 响应格式

Zapier MCP 使用 Server-Sent Events 格式：

```
event: message
data: {"result":{"tools":[...]},"jsonrpc":"2.0","id":1}
```

后端会自动解析这种格式。

## UI 功能

Clawdbot 仪表板中的 Zapier 页面提供以下功能：

- **连接状态** — 显示是否已配置以及可用的工具数量
- **MCP URL 配置** — 粘贴并验证您的 URL
- **测试连接** — 验证 URL 是否有效
- **工具浏览器** — 可展开的组别，按应用程序显示所有可用工具

### 工具分组

工具会自动按应用程序进行分组：
- QuickBooks Online（47 个工具）
- Google Sheets（12 个工具）
- Slack（8 个工具）
- 等等

## Zapier 与 Pipedream 的比较

| 功能 | Zapier MCP | Pipedream Connect |
|---------|------------|-------------------|
| 设置 | 粘贴 URL | OAuth + 凭据 |
| 令牌刷新 | 不需要 | 每 45 分钟一次 |
| 应用程序数量 | 8,000 多个 | 2,000 多个 |
| 成本 | Zapier 订阅费 | Pipedream 订阅费 |
| 复杂性 | 简单 | 更高的控制权限 |

**使用建议：**
- 如果您希望设置简单且已经在使用 Zapier，建议使用 Zapier。
- 如果您需要更细粒度的 OAuth 控制或更喜欢 Pipedream 的定价方案，可以选择 Pipedream。

## 故障排除

### “连接测试失败”
- 确认 URL 是否正确（应以 `https://actions.zapier.com/mcp/` 开头）
- 检查是否在 Zapier 的 MCP 仪表板中配置了至少一项动作
- 尝试在 Zapier 中重新生成 MCP URL

### “没有可用工具”
- 访问 [zapier.com/mcp](https://zapier.com/mcp) 并添加一些动作
- 添加动作后，在 Clawdbot UI 中点击 “刷新”

### 响应中的 “followUpQuestion”
- Zapier 需要更多信息。请在 `instructions` 参数中提供更具体的信息。
- 例如：将 “find customer” 更改为 “find customer named Acme Corp”

### 找不到工具
- 运行 `mcporter list zapier-mcp` 以查看可用的工具
- 工具名称使用下划线分隔：`quickbooks_online_find_customer`
- 可能需要在 Zapier 的 MCP 配置中添加相应的动作

## 添加特定于应用程序的技能

连接 Zapier MCP 后，您可以创建针对常用集成的特定于应用程序的技能。例如：
- `zapier-quickbooks` — 提供 QuickBooks Online 的详细参数文档的技能

这些技能在使用相同的 Zapier MCP 连接的同时，为特定应用程序提供更详细的文档。

## 参考文件

此功能包含以下参考实现文件：

- `reference/zapier-backend.ts` — Gateway RPC 处理程序
- `reference/zapier-controller.ts` — UI 控制逻辑
- `reference/zapier-views.ts` — UI 渲染代码

这些文件可用于构建自定义集成或调试。

## 安全注意事项

| 行为 | 描述 |
|----------|-------------|
| **URL 包含认证信息** | 您的 MCP URL 包含认证信息——请将其视为密码 |
| **存储在配置中** | URL 保存在 `~/clawd/config/mcporter.json` 中 |
| **外部 API 调用** | 调用 `actions.zapier.com` |

**最佳实践：**
- 不要公开分享您的 MCP URL
- 如果 URL 被泄露，请重新生成 URL（在 Zapier 仪表板中操作）
- 审查在 Zapier 的 MCP 设置中暴露了哪些动作

## 支持资源

- **ClawdHub**：[clawdhub.com/skills/zapier-mcp](https://clawdhub.com/skills/zapier-mcp)
- **Zapier MCP**：[zapier.com/mcp](https://zapier.com/mcp)
- **Zapier 帮助文档**：[help.zapier.com](https://help.zapier.com)
- **Clawdbot Discord**：[discord.com/invite/clawd](https://discord.com/invite/clawd)