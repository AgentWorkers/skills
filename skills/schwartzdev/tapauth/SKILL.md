---
name: tapauth
description: 通过 TapAuth 获取 AI 代理的代理访问权限——这是连接人类与 AI 代理的信任机制。当您的代理需要代表用户访问 GitHub、Google Workspace、Gmail、Linear 或其他 OAuth 提供商的服务时，可以使用此方法。只需进行一次 API 调用来创建授权请求，用户通过浏览器进行批准，代理即可获得相应的访问令牌。无需使用 API 密钥。
  Get delegated access for AI agents via TapAuth — the trust layer between humans and AI agents.
  Use when your agent needs to access GitHub, Google Workspace, Gmail, Linear, or other OAuth
  providers on behalf of a user. One API call to create an auth request, user approves in browser,
  agent gets scoped tokens. No API key required.
license: MIT
compatibility: Requires curl or any HTTP client. Works with Claude Code, Cursor, OpenClaw, Codex, GitHub Copilot, and any agent with HTTP access.
metadata:
  author: tapauth
  version: "1.0"
  website: https://tapauth.ai
  docs: https://tapauth.ai/docs
---
# TapAuth — 为AI代理提供委托访问功能

TapAuth允许您的代理在无需直接处理用户凭证的情况下获取OAuth令牌。用户会在浏览器中完成授权流程，之后您就能获得相应的令牌。

## 最快捷的入门方式：使用CLI

`tapauth` CLI脚本已随此功能一起提供。请将其保存并设置为可执行文件：

```bash
# Copy from this skill directory and make executable
cp /path/to/skill/tapauth ./tapauth
chmod +x tapauth
```

然后通过命令行调用它：

```bash
# One line. Get a token. Use it.
curl -H "Authorization: Bearer $(./tapauth google drive.readonly)" \
  https://www.googleapis.com/drive/v3/files
```

**首次运行：** 生成授权请求，将授权URL输出到标准错误流（stderr），等待用户批准后，将令牌输出到标准输出流（stdout）。

**后续运行：** 如果令牌未过期，将立即返回缓存的令牌；如果令牌已过期，系统会自动刷新令牌。

```bash
# Example: access Google Calendar
curl -H "Authorization: Bearer $(./tapauth google calendar.events)" \
  https://www.googleapis.com/calendar/v3/calendars/primary/events
```

**环境变量：**
- `TAPAUTH_BASE_URL` — 可以覆盖基础URL（默认值：`https://tapauth.ai`）
- `TAPAUTH_HOME` — 可以覆盖缓存目录（默认值：`./.tapauth`）

**安全性：** 令牌会被缓存在`.tapauth/`目录中（目录权限设置为700，文件权限设置为600）。授权所需的密钥（`grant_secret`）也会与令牌一起存储在本地，以实现自动刷新。

## API流程（v1）

### 第1步：生成授权请求

```bash
# JSON
curl -X POST https://tapauth.ai/api/v1/grants \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "github",
    "scopes": ["repo", "read:user"],
  }'

# Or form-urlencoded (what the CLI uses)
curl -X POST https://tapauth.ai/api/v1/grants \
  -H "Accept: text/plain" \
  --data-urlencode "provider=github" \
  --data-urlencode "scopes=repo,read:user"
```

JSON响应格式：
```json
{
  "grant_id": "abc123",
  "grant_secret": "gs_live_xxxx",
  "approve_url": "https://tapauth.ai/approve/abc123"
}
```

文本响应格式（响应头包含`Accept: text/plain`）：
```
TAPAUTH_GRANT_ID=abc123
TAPAUTH_GRANT_SECRET=gs_live_xxxx
TAPAUTH_APPROVE_URL=https://tapauth.ai/approve/abc123
```

**重要提示：** 请保存`grant_secret`，因为您需要它来获取令牌。该密钥仅会生成一次。

### 第2步：用户授权

向用户展示`approve_url`。用户将看到以下信息：
- 请求访问权限的代理
- 所使用的提供者及所需权限范围
- 可选的授权方式：全权限、只读权限或限时权限（1小时/24小时/7天/永久）

授权URL在**10分钟后**失效。如果授权URL失效，请重新生成授权请求。

### 第3步：获取令牌

持续轮询用户的授权状态。使用`grant_secret`通过Bearer认证方式获取令牌：

```bash
# Plain text (just the token)
curl https://tapauth.ai/api/v1/token/{grant_id} \
  -H "Authorization: Bearer <grant-secret>"

# .env format (token + expiry + grant ID for caching)
curl https://tapauth.ai/api/v1/token/{grant_id}.env \
  -H "Authorization: Bearer <grant-secret>"

# JSON format
curl https://tapauth.ai/api/v1/token/{grant_id}.json \
  -H "Authorization: Bearer <grant-secret>"
```

| HTTP状态码 | 含义 |
|------|---------|
| 200 | 令牌已成功返回 |
| 202 | 用户尚未授权，请在2-5秒后重新尝试 |
| 401 | `grant_secret`无效或丢失 |
| 404 | 未找到相应的授权请求 |
| 410 | 令牌已过期、被撤销或链接失效 |

JSON响应格式（`.json`）：
```json
{
  "token": "gho_xxxx",
  "expires": "2026-03-05T17:00:00Z",
  "provider": "github",
  "grant_id": "abc123"
}
```

环境变量响应格式（`.env`）：
```
TAPAUTH_TOKEN=gho_xxxx
TAPAUTH_EXPIRES=1741194000
TAPAUTH_GRANT_ID=abc123
TAPAUTH_GRANT_SECRET=gs_live_xxxx
```

## 令牌的生命周期与撤销

TapAuth采用零知识加密技术：令牌会使用`grant_secret`进行加密，而TapAuth本身不会存储该密钥。这意味着：
- **TapAuth无法在提供者端直接撤销令牌**（因为我们无法解密这些加密后的令牌）。
- 当令牌过期时，我们会直接删除加密后的密文，而不会对其进行解密。
- 对于有效期较短的提供者（如Google、Linear、Sentry），令牌会自动过期。
- 对于有效期永久的提供者（如GitHub、Slack、Vercel、Notion），您可以在提供者的设置中手动撤销令牌。

我们建议为需要长期有效令牌的请求设置`expires_in`参数。

## 快速参考

| 功能 | API端点 | 方法 |
|------|----------|--------|
| 生成授权请求 | `/api/v1/grants` | POST |
| 获取令牌 | `/api/v1/token/{id}` | GET |
| 获取令牌（环境变量格式） | `/api/v1/token/{id}.env` | GET |
| 获取令牌（JSON格式） | `/api/v1/token/{id}.json` | GET |
| 使用CLI | `$(tapauth <provider> <scopes>` | — |

无需API密钥，也无需注册账号。用户的授权是访问权限的唯一依据。

## 支持的提供者

具体提供者的权限范围、使用示例及注意事项请参见`references/`目录：
- **GitHub** (`github`) → `references/github.md` — 仓库、问题、Pull请求、用户数据、代码片段、工作流
- **Google** (`google`) → `references/google.md` — Gmail、Google Drive、日历、表格、文档、联系人
- **Gmail** → `references/gmail.md` — 阅读、发送和管理邮件（使用`google`提供者的功能）
- **Google Drive** (`google_drive`) → `references/google_drive.md` — 仅限访问Google Drive
- **Google Contacts** (`google_contacts`) → `references/google_contacts.md` — 查看和管理联系人
- **Google Sheets** (`google_sheets`) → `references/google_sheets.md` — 读写电子表格
- **Google Docs** (`google_docs`) → `references/google_docs.md` — 读写文档
- **Linear** (`linear`) → `references/linear.md` — 问题、项目、团队
- **Vercel** (`vercel`) → `references/vercel.md` — 部署、项目、环境变量、域名
- **Notion** (`notion`) → `references/notion.md` — 页面、数据库、搜索功能
- **Slack** (`slack`) → `references/slack.md` — 频道、消息、用户、文件
- **Sentry** (`sentry`) → `references/sentry.md` — 错误跟踪、项目、组织信息
- **Asana** (`asana`) → `references/asana.md` — 任务、项目、工作空间

> **提示：** 对于仅使用某个Google服务的场景，建议使用专门的提供者（如`google_drive`、`google_sheets`等），因为它们的授权流程更简单。如果需要使用多个Google服务，请使用`google`提供者。

## 提供者信息查询

可以通过以下命令程序化地列出所有可用的提供者及其支持的权限范围：

```bash
curl https://tapauth.ai/api/providers
```

该命令会返回每个提供者的ID、名称、类别、支持的权限范围以及是否支持令牌刷新功能。

## 提供者相关说明：
- **GitHub：** 令牌使用OAuth应用认证。`repo`权限允许读写仓库内容；创建仓库需要用户具有相应的GitHub权限。某些仅通过GitHub PAT可执行的操作可能无法使用OAuth令牌完成。
- **Google：** 所有Google提供者都支持令牌的自动刷新。如果只需要使用某个特定服务，建议使用专门的提供者（如`google_drive`、`google_sheets`等），以简化授权流程。
- **Discord：** 使用用户的OAuth令牌（而非机器人令牌）。令牌有效期约为7天，并支持自动刷新。`guilds`权限仅用于查看服务器列表，不包含频道或消息访问权限。
- **Vercel/Slack/Notion：** 这些提供者的权限范围在安装时固定，不会根据每次请求进行更改。

## CLI工具

要完成完整的授权请求生成、轮询和缓存流程，请使用`tapauth` CLI：

```bash
# Install: copy packages/cli/tapauth to your PATH
TOKEN=$(tapauth github repo,read:user)

# First run: creates grant, shows approval URL, polls until approved
# Subsequent runs: returns cached token (auto-refreshes when expired)
```

CLI会将用户凭证存储在`.tapauth/`目录中（目录权限设置为700），并为每个提供者和权限范围创建单独的缓存文件。

## 常见操作模式：
- **先请求用户授权，再继续执行操作**
- **优雅地处理令牌过期情况**：如果收到`link_expired`（410）错误，只需重新生成授权请求并再次请求用户的授权。
- **权限范围选择**：仅请求所需的最低权限范围。这样用户能更清楚地了解您的需求，从而提高授权通过率。权限范围越少，用户的信任度越高，授权成功率也越高。