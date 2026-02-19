---
name: calendar-bridge
description: 与“Calendar Bridge”进行交互——这是一个自托管的Node.js服务，为Google日历事件提供持久的REST API接口。该服务支持OAuth令牌的自动刷新功能，因此您无需重新进行身份验证。您可以利用它来查看即将发生的事件、列出日历、设置Google日历的访问权限，或解决日历认证相关的问题。
homepage: https://github.com/DanielKillenberger/gcal-oauth-bridge
version: 1.0.2
read_when:
  - User asks about upcoming events or calendar
  - User asks what's scheduled or what meetings they have
  - Calendar Bridge setup or troubleshooting needed
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
        "requires": { "env": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"] },
        "optional": { "env": ["CALENDAR_BRIDGE_API_KEY"] },
        "notes": "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are required for initial OAuth setup only — once authenticated, the agent only needs network access to localhost:3000. CALENDAR_BRIDGE_API_KEY is optional; if set, the agent must send it as Authorization: Bearer <key> when calling /events. Tokens stored locally in tokens.json on your server, never sent externally."
      }
  }
triggers:
  - what's on my calendar
  - upcoming events
  - check my calendar
  - do I have anything scheduled
  - what meetings do I have
  - calendar today
  - calendar this week
  - calendar next week
  - list my calendars
  - google calendar
  - calendar bridge
  - set up calendar
  - calendar auth
  - calendar access
  - calendar not working
---
# 日历桥接技能（Calendar Bridge Skill）

使用此技能可与日历桥接服务（Calendar Bridge）进行交互。该服务是一个基于 REST 的本地 API，它将 Google 日历的 OAuth 功能与持久化令牌存储及自动刷新功能结合在一起。

**GitHub 仓库：** https://github.com/DanielKillenberger/gcal-oauth-bridge

## 什么是日历桥接服务？

这是一个运行在 `http://localhost:3000` 的小型 Node.js/Express 服务，具备以下功能：
- 通过浏览器完成一次 Google 日历的 OAuth 验证流程；
- 存储并自动刷新令牌（解决了令牌每 7 天失效的问题）；
- 提供用于查询事件、日历及进行身份验证的简单 REST API 接口。

## API 端点

| 端点 | 描述 |
|---------|-------------|
| `GET /health` | 服务状态及身份验证状态 |
| `GET /auth/url` | 获取 OAuth 同意页面的 URL |
| `GET /events?days=7` | 获取主日历中的即将发生的事件 |
| `GET /events?days=7&calendar=all` | 获取所有日历中的事件 |
| `GET /events?days=7&calendar=<id>` | 获取特定日历中的事件 |
| `GET /calendars` | 列出所有可用的日历 |
| `POST /auth/refresh` | 强制刷新令牌（通常会自动触发） |

事件响应数据包含：`id`、`summary`、`start`、`end`、`location`、`description`、`htmlLink`、`status`、`calendarId`、`calendarSummary`。

## 查询事件

```bash
# Quick event check (7 days, primary calendar)
curl http://localhost:3000/events

# All calendars, next 14 days
curl http://localhost:3000/events?days=14&calendar=all

# With API key (if CALENDAR_BRIDGE_API_KEY is configured)
curl -H "Authorization: Bearer $API_KEY" http://localhost:3000/events?calendar=all
```

若要在 OpenClaw 的技能框架内调用此服务（在同一主机上运行时无需 API 密钥）：

```
GET http://localhost:3000/events?calendar=all&days=7
```

## 首次设置

### 1. 克隆并安装依赖项
```bash
git clone https://github.com/DanielKillenberger/gcal-oauth-bridge.git
cd gcal-oauth-bridge
npm install
cp .env.example .env
# Edit .env with GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET
```

### 2. 获取 Google OAuth 凭据
- 访问 https://console.cloud.google.com/apis/credentials
- 创建 OAuth 2.0 客户端 ID（适用于桌面应用程序）
- 启用 Google 日历 API
- 设置重定向 URI：`http://localhost:3000/auth/callback`
- 将客户端 ID 和密钥复制到 `.env` 文件中

### 3. 启动服务
```bash
node app.js
# or: npm start
```

### 4. 进行身份验证（一次性的浏览器操作）
如果在远程 VPS 上运行服务，首先需要建立端口 3000 的隧道：
```bash
# From your local machine:
ssh -L 3000:localhost:3000 your-server
```

之后：
```bash
curl http://localhost:3000/auth/url
# Open the returned URL in your browser
# Complete Google consent → tokens saved automatically
```

验证服务是否已成功启动：
```bash
curl http://localhost:3000/health
# {"status":"ok","authenticated":true,"needsRefresh":false}
```

### 5. 保持服务持续运行（使用 systemd）
```bash
systemctl --user enable calendar-bridge.service
systemctl --user start calendar-bridge.service
```

## 重新认证

如果令牌被撤销（这种情况很少发生，因为系统会自动刷新令牌）：
1. 使用 `ssh -L 3000:localhost:3000 your-server` 命令建立隧道连接；
2. 执行 `curl http://localhost:3000/auth/url` 以完成令牌刷新流程；
3. 令牌更新完成后，旧令牌将被替换为新令牌。

## 常见问题解决方法

- **错误信息：“Not authenticated”**：请重新执行上述 OAuth 配置流程。
- **401 Unauthorized**：请确保已设置 `CALENDAR_BRIDGE_API_KEY`，并在请求头中添加 `Authorization: Bearer <key>`。
- **无法访问 `localhost:3000`**：检查服务是否正在运行（使用 `systemctl --user status calendar-bridge` 命令）。
- **错误信息：“invalid_grant” 或 “token expired”**：可能是令牌被外部撤销，请重新进行身份验证。

## 关于个人 Gmail 用户

该服务支持个人 Gmail 账户。Google 可能会显示“未验证的应用程序”警告，此时请点击 **高级设置 → 前往 [应用页面]** 以完成验证。令牌会存储在您的服务器上，不会被共享给他人。

## 相关文件

- **GitHub 仓库：** https://github.com/DanielKillenberger/gcal-oauth-bridge
  - `app.js`：主要的 Express 服务器代码
  - `.env`：配置文件（基于 `.env.example` 示例生成）
  - `tokens.json`：令牌文件（自动生成，由 Git 系统忽略，不会被提交到代码库）