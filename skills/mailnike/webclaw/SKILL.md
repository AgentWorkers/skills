---
name: webclaw
version: 1.0.11
description: >
  OpenClaw 的 Web 仪表盘：  
  这是一个基于浏览器的用户界面，用于管理已安装的所有技能。该界面采用模式驱动（schema-driven）的渲染方式，支持 JWT 身份验证（JWT auth）、基于角色的访问控制（RBAC）、人工智能聊天功能以及实时数据更新。您可以通过该 Web 仪表盘来安装新技能、管理用户、配置 SSL/TLS 安全协议（SSL HTTPS），并使用 Web 管理面板进行各项设置。
author: AvanSaber / Nikhil Jathar
homepage: https://www.erpclaw.ai
source: https://github.com/avansaber/webclaw
tier: 0
category: infrastructure
requires: []
database: ~/.openclaw/webclaw/webclaw.sqlite
user-invocable: true
tags: [web, dashboard, ui, admin, login, ssl, https, users, roles]
metadata: {"openclaw":{"type":"executable","install":{"pre":"bash scripts/check_deps.sh","post":"bash scripts/install.sh","pip":"api/requirements.txt"},"requires":{"bins":["python3","node","npm","nginx","certbot","git","sudo"],"env":[],"optionalEnv":["WEBCLAW_DOMAIN"]},"os":["linux"]}}
cron:
  - expression: "0 2 * * *"
    timezone: "UTC"
    description: "Clean expired sessions and check SSL cert renewal"
    message: "Using webclaw, run the maintenance action."
    announce: false
---
# webclaw

您是此 OpenClaw 实例的 **Web 仪表板管理员**。您负责管理一个基于浏览器的用户界面，该界面为每个已安装的技能提供表单、表格、图表和 AI 聊天功能——且无需为每个技能编写自定义代码。

## 安全模型

- 通过 Let's Encrypt 强制使用 **HTTPS**（使用 `setup-ssl` 功能进行配置）
- **JWT 认证**：访问令牌（有效期 15 分钟）+ 刷新令牌（有效期 7 天，使用 `httpOnly` cookie）
- **基于角色的访问控制（RBAC）**：在每个技能操作之前进行权限检查
- **速率限制**：每分钟最多 5 次认证请求，每分钟最多 30 次写入操作，每分钟最多 100 次其他操作（由 Nginx 实现）
- **审计日志记录**：所有修改操作都会被记录到 `audit_log` 表中
- 密码使用 PBKDF2-HMAC-SHA256 进行哈希处理（迭代次数为 600,000 次）
- 更改密码后会失效当前会话

### 权限要求

安装过程中需要 **sudo** 权限来执行以下系统级操作：
- **nginx**：将反向代理配置写入 `/etc/nginx/sites-enabled/webclaw`
- **systemd**：在 `/etc/systemd/system/` 目录下创建 `webclaw-api.service` 和 `webclaw-web.service` 服务
- **certbot**：请求 Let's Encrypt SSL 证书（仅使用 `setup-ssl` 功能）
- **git**：在首次安装时从 `https://github.com/avansaber/webclaw` 克隆完整的源代码

**注意：** `ClawHub` 包仅包含元数据（如 SKILL.md 文件和脚本）。完整的应用程序（API 服务器、Next.js 前端、模板等）会在安装后从 GitHub 的指定版本标签处克隆。这需要在目标服务器上安装 git 并具备互联网访问权限。

**供应链注意事项：** 安装脚本会从 `https://github.com/avansaber/webclaw` 克隆特定版本的代码（例如 `v1.0.10`），而不是最新的 `HEAD` 版本。pip 和 npm 依赖项会从标准仓库中安装，并在隔离的虚拟环境中（venv）进行安装。`create-user` 和 `reset-password` 功能生成的临时密码会输出到系统中，以便管理员将其告知用户；用户首次登录后应立即更改这些密码。

无需提供任何凭据或 API 密钥。所有数据都存储在本地 SQLite 数据库中。

### 技能激活触发条件

当用户提到以下关键词时，可激活相应技能：web dashboard、web UI、web interface、login page、HTTPS、SSL certificate、web users、roles、RBAC、nginx、web admin、dashboard access、browser access、setup web、install web dashboard。

### 首次使用时的设置步骤

**重要提示：** 安装完成后，请让用户通过浏览器打开设置页面：

> 打开 **https://YOUR_SERVER/setup** 以创建管理员账户。

操作步骤：
1. 打开安装过程中显示的网址（例如 `https://1.2.3.4/setup`）
2. 创建第一个管理员账户（输入电子邮件地址和密码）
3. 登录后，所有已安装的技能会显示在侧边栏中

**如何为自定义域名启用 HTTPS：** 请输入 “Set up SSL for yourdomain.com”

## 快速入门（基础级别）

### 检查状态
```
Using webclaw, show me the dashboard status
→ runs: status
```

### 启用 HTTPS
```
Set up SSL for erp.example.com
→ runs: setup-ssl --domain erp.example.com
```

### 创建 Web 用户
```
Create a web user for alice@company.com with Manager role
→ runs: create-user --email alice@company.com --full-name "Alice" --role Manager
```

### 重置密码
```
Reset the web password for alice@company.com
→ runs: reset-password --email alice@company.com
```

## 所有可用操作（高级级别）

| 操作 | 参数 | 说明 |
|--------|------|-------------|
| `status` | — | 服务状态、SSL 状态、用户数量 |
| `setup-ssl` | `--domain` | 使用 Let's Encrypt 配置 HTTPS |
| `renew-ssl` | — | 检查并续订 SSL 证书 |
| `list-users` | — | 列出所有 Web 仪表板用户 |
| `create-user` | `--email`, `--full-name`, `--role` | 使用临时密码创建用户 |
| `reset-password` | `--email` | 为用户生成新临时密码 |
| `disable-user` | `--email` | 禁用用户账户 |
| `list-sessions` | — | 显示当前登录会话 |
| `clear-sessions` | — | 强制所有用户重新登录 |
| `maintenance` | — | 定时任务：清理会话记录、检查证书状态 |
| `restart-services` | — | 重启 API 服务和前端服务 |
| `show-config` | — | 显示当前配置 |

### 常用命令参考

| 用户输入 | 对应操作 |
|-----------|--------|
| “仪表板正在运行吗？” | `status` |
| “为 example.com 设置 SSL” | `setup-ssl --domain example.com` |
| “谁有 Web 访问权限？” | `list-users` |
| “添加用户 bob@co.com” | `create-user --email bob@co.com` |
| “重置 bob 的密码” | `reset-password --email bob@co.com` |
| “禁用 bob 的 Web 访问权限” | `disable-user --email bob@co.com` |
| “当前有哪些用户登录？” | `list-sessions` |
| “强制所有用户重新登录” | `clear-sessions` |
| “重启 Web 仪表板” | `restart-services` |
| “显示 Web 仪表板配置” | `show-config` |

### 建议

- 在创建用户后，提醒用户妥善保管临时密码。
- 在配置 HTTPS 后，确认重定向是否正常工作。
- 如果 `status` 显示 SSL 状态为 `false`，建议再次运行 `setup-ssl` 命令。
- 如果 `status` 显示用户数量为 0，建议用户访问 `/setup` 页面进行配置更新。

## 技术细节（高级级别）

### 架构

- **前端**：使用 Next.js 16、React 19、shadcn/ui 和 Tailwind v4 构建（端口 3000）
- **后端**：使用 FastAPI 和 uvicorn（端口 8001）
- **代理**：Nginx（端口 80/443）负责将请求路由到后端（/api）或前端（/）
- **数据库**：使用 SQLite 数据库（文件路径：`~/.openclaw/webclaw/webclaw.sqlite`）

### 8 个通用的 UI 组件

`DataTable`、`FormView`、`DetailView`、`ChatPanel`、`ChartPanel`、`KanbanBoard`、`CalendarView`、`TreeView`——这些组件均根据技能操作的结果动态渲染。

### 所使用的数据库表

`webclaw_user`、`webclaw_session`、`webclaw_config`、`webclaw_role`、`webclaw_user_role`、`webclaw_role_permission`、`chat_session`、`chat_message`、`audit_log`

### 脚本路径
```
scripts/db_query.py --action <action-name> [--key value ...]
```

### 技能自定义

每个技能可以在其 SKILL.md 文件的 frontmatter 部分添加 `webclaw` 部分，以实现自定义功能：
```yaml
webclaw:
  domain: "GRC & Audit"
  database: "~/.openclaw/auditclaw/data.sqlite"
  entities:
    risk:
      table: risk_register
      name_col: risk_title
      id_col: id
      search_cols: [risk_category, severity]
```