---
name: pipedream-connect
description: 通过 Pipedream，您可以连接 2,000 多个 API，并使用托管的 OAuth 进行身份验证。该解决方案还支持与 Clawdbot Gateway 仪表板的完全集成。
metadata: {"clawdbot":{"emoji":"🔌","requires":{"bins":["mcporter"],"clawdbot":">=2026.1.0"},"category":"integrations"}}
---

# Pipedream Connect

通过 Pipedream，您可以将您的 AI 代理连接到 2,000 多个 API，并使用托管的 OAuth 进行身份验证。该功能提供以下优势：

- **完整的 UI 仪表盘**：配置凭据、连接应用程序、管理令牌。
- **自动令牌刷新**：通过 Cron 作业保持令牌的有效性。
- **MCP 集成**：应用程序可通过 `mcporter` 成为代理可使用的工具。

## 概述

Pipedream Connect 可处理数千个 API 的 OAuth 流程，因此您的代理无需手动管理令牌即可访问 Gmail、Google 日历、Slack、GitHub 等服务。

## 先决条件

1. **Pipedream 账户**：在 [pipedream.com](https://pipedream.com) 注册。
2. **mcporter**：MCP 工具运行器（`npm install -g mcporter`）。
3. **Clawdbot Gateway**：版本需为 v2026.1.0 或更高，并且启用了 UI 功能。

## 快速入门

### 第 1 步：创建 Pipedream OAuth 客户端

1. 访问 [pipedream.com/settings/api](https://pipedream.com/settings/api)。
2. 点击 “新建 OAuth 客户端”。
3. 复制 **客户端 ID** 和 **客户端密钥**。

### 第 2 步：创建 Pipedream 项目

1. 访问 [pipedream.com/projects](https://pipedream.com/projects)。
2. 创建一个新项目（例如：“clawdbot”）。
3. 复制 **项目 ID**（以 `proj_` 开头）。

### 第 3 步：在 Clawdbot UI 中进行配置

1. 打开 Clawdbot 仪表盘 → **工具** → **Pipedream**。
2. 点击 **配置**，并输入以下信息：
   - 客户端 ID
   - 客户端密钥
   - 项目 ID
   - 环境（开发/生产）
   - 外部用户 ID（例如：“clawdbot”）。
3. 点击 **保存凭据**。

### 第 4 步：连接应用程序

1. 在 Pipedream UI 中，点击任何应用程序（例如 Gmail、Google 日历）上的 “连接” 按钮。
2. 完成弹出的 OAuth 流程。
3. 再次点击 “连接” 以完成连接。

### 第 5 步：设置令牌刷新（推荐）

Pipedream 令牌在 1 小时后过期。请设置自动刷新：

```bash
# Copy the token refresh script
cp ~/clawd/skills/pipedream-connect/scripts/pipedream-token-refresh.py ~/clawd/scripts/

# Set up cron job (runs every 45 minutes)
(crontab -l 2>/dev/null; echo "*/45 * * * * /usr/bin/python3 $HOME/clawd/scripts/pipedream-token-refresh.py >> $HOME/clawd/logs/pipedream-cron.log 2>&1") | crontab -
```

## 使用方法

连接成功后，您的代理可以通过 `mcporter` 使用这些应用程序工具：

```bash
# Gmail
mcporter call pipedream-clawdbot-gmail.gmail-find-email \
  instruction="Find unread emails from today"

mcporter call pipedream-clawdbot-gmail.gmail-send-email \
  instruction="Send email to bob@example.com with subject 'Hello' and body 'Hi there!'"

# Google Calendar
mcporter call pipedream-clawdbot-google-calendar.google_calendar-list-events \
  instruction="Show my events for this week"

mcporter call pipedream-clawdbot-google-calendar.google_calendar-create-event \
  instruction="Create a meeting tomorrow at 2pm called 'Team Standup'"

# Slack
mcporter call pipedream-clawdbot-slack.slack-send-message \
  instruction="Send 'Hello team!' to the #general channel"
```

## 架构

### 创建的文件

| 位置 | 用途 |
|----------|---------|
| `~/clawd/config/pipedream-credentials.json` | 加密后的凭据存储 |
| `~/clawd/config/mcporter.json` | MCP 服务器配置 |
| `~/clawd/scripts/pipedream-token-refresh.py` | 令牌刷新脚本 |
| `~/clawd/logs/pipedream-token-refresh.log` | 令牌刷新日志 |

### 后端端点

该功能添加了以下 gateway RPC 方法：

| 方法 | 用途 |
|--------|---------|
| `pipedream.status` | 获取连接状态和已配置的应用程序 |
| `pipedream.saveCredentials` | 验证并存储凭据 |
| `pipedream.token` | 获取新的访问令牌 |
| `pipedream.getConnectUrl` | 获取应用程序的 OAuth URL |
| `pipedream.connectApp` | 将应用程序配置保存到 mcporter |
| `pipedream.disconnectApp` | 从 mcporter 中删除应用程序 |
| `pipedream.refreshToken` | 更新存储的令牌 |

### UI 组件

Clawdbot 仪表板中的 Pipedream 页面提供：

- 凭据配置表单
- 已连接的应用程序列表，带有测试/断开连接按钮
- 支持 100 多个流行应用程序的应用程序浏览器
- 用于输入任何受 Pipedream 支持的应用程序 slug 的手动输入框

## 应用程序 slug 参考

可以在 [mcp.pipedream.com](https://mcp.pipedream.com) 查找应用程序 slug。常见示例：

| 应用程序 | Slug |
|-----|------|
| Gmail | `gmail` |
| Google 日历 | `google-calendar` |
| Google 表格 | `google-sheets` |
| Google 驱动 | `google-drive` |
| Slack | `slack` |
| Discord | `discord` |
| GitHub | `github` |
| Notion | `notion` |
| Linear | `linear` |
| Airtable | `airtable` |
| OpenAI | `openai` |
| Stripe | `stripe` |

## 故障排除

### “没有可用工具”
- OAuth 流程未完成。请再次点击 “连接” 并完成弹出窗口中的操作。
- 检查 Pipedream 仪表板 → “连接” → “用户” 以确认应用程序已链接。

### “令牌过期”/401 错误
- 手动运行令牌刷新脚本：`python3 ~/clawd/scripts/pipedream-token-refresh.py`。
- 确认 Cron 作业正在运行：`crontab -l | grep pipedream`。

### “无法获取数据”/CORS 错误
- 确保您使用的 Clawdbot 版本为 v2026.1.0 或更高，并且启用了 Pipedream 后端修复功能。
- 所有 API 调用都应通过 gateway 后端进行，而不是浏览器。

### 应用程序未显示在 Pipedream 仪表板上
- 对于 MCP 调用，请使用 `google_calendar`（带下划线的格式）。
- UI 使用 `google-calendar`（带连字符的格式），后端会自动转换。

### OAuth 弹窗被阻止
- 在浏览器中允许来自 `localhost:18789` 的弹窗。
- 或者手动复制连接 URL 并打开它。

## 多代理设置

每个代理可以使用不同的 `externalUserId` 值来拥有自己的连接账户：

```
User ID: koda      → Apps connected for Koda
User ID: assistant → Apps connected for Assistant
```

这将为每个代理创建单独的 mcporter 服务器条目：
- `pipedream-koda-gmail`
- `pipedream-assistant-gmail`

## 开发说明

### 令牌过期

Pipedream 访问令牌在 1 小时后过期。刷新脚本应至少每 50 分钟运行一次。

### MCP 端点

所有 MCP 调用都发送到 `https://remote.mcp.pipedream.net`，并包含以下头部信息：
- `Authorization: Bearer <access_token>`
- `x-pd-project-id: <project_id>`
- `x-pd-environment: development|production`
- `x-pd-external-user-id: <user_id>`
- `x-pd-app-slug: <app_slug>`（使用下划线，而非连字符）
- `Accept: application/json, text/event-stream`

### SSE 响应

MCP 端点可能返回 Server-Sent Events 格式的数据：
```
event: message
data: {"result":{"tools":[...]},"jsonrpc":"2.0","id":1}
```

解析 `data:` 行以提取 JSON 数据。

## 参考文件

该功能包含以下参考实现文件：

- `reference/pipedream-backend.ts` — gateway RPC 处理程序
- `reference/pipedream-controller.ts` — UI 控制器逻辑
- `reference/pipedream-views.ts` — UI 渲染代码
- `scripts/pipedream-token-refresh.py` — 令牌刷新脚本

这些文件可用于构建自定义集成或进行调试。

## 支持资源

- **Pipedream 文档**：[pipedream.com/docs](https://pipedream.com/docs)
- **MCP 应用程序**：[mcp.pipedream.com](https://mcp.pipedream.com)
- **Clawdbot Discord**：[discord.com/invite/clawd](https://discord.com/invite/clawd)