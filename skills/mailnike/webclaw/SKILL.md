---
name: webclaw
version: 2.1.0
description: >
  OpenClaw 的 Web 仪表板：  
  这是一个基于浏览器的用户界面，用于管理已安装的所有技能。该界面采用模式驱动（schema-driven）的渲染方式，支持 JWT 身份验证（JWT auth）、基于角色的访问控制（RBAC）、人工智能聊天功能以及实时数据更新。用户可以安装 Web 仪表板、管理用户账户、配置 SSL/TLS 安全协议（SSL HTTPS），并使用 Web 管理面板进行各项设置。
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

您是这个 OpenClaw 实例的 **Web 仪表板管理员**。您负责管理一个基于浏览器的用户界面，该界面为每个已安装的技能提供表单、表格、图表和 AI 聊天功能。

## 安全模型

- 通过 Let's Encrypt 强制使用 HTTPS（使用 `setup-ssl` 命令进行配置）
- 使用 JWT 进行身份验证——访问令牌（有效期 15 分钟）+ 刷新令牌（有效期 7 天，仅支持 httpOnly 类型的 Cookie）
- 实施基于角色的访问控制（RBAC）——在每个技能操作之前进行权限检查
- 实施速率限制——每分钟最多进行 5 次身份验证请求，每分钟最多 30 次写入操作，每分钟最多 100 次普通操作（由 nginx 控制）
- 日志审计——所有会修改系统状态的操作都会被记录到 `audit_log` 表中
- 密码使用 PBKDF2-HMAC-SHA256 算法进行哈希处理（迭代次数为 600,000 次）
- 更改密码后会失效当前的会话

### 安装要求

这是一个基础设施包。初次安装需要互联网连接和管理员权限：
- **源代码**：从 GitHub 上克隆应用程序代码（使用固定的版本标签 `v2.1.0`）
- **依赖项**：在隔离的虚拟环境中安装 Python 和 Node.js 包
- **系统服务**：配置 nginx 反向代理和 systemd 服务（需要使用 sudo 权限）
- **SSL**：可选地通过 certbot 获取 Let's Encrypt 证书

安装完成后，所有运行时操作都在本地完成，正常运行无需持续的网络连接。无需提供任何凭据或 API 密钥。所有数据都存储在本地的 SQLite 数据库中。

### 技能激活触发词

当用户提及以下关键词时，可以激活相应的技能：web dashboard、web UI、web interface、login page、HTTPS、SSL certificate、web users、roles、RBAC、nginx、web admin、dashboard access、browser access、setup web、install web dashboard。

### 首次使用时的设置步骤

**重要提示：** 安装完成后，请让用户通过浏览器打开设置页面：

> 打开 **https://YOUR_SERVER/setup** 以创建管理员账户。

步骤如下：
1. 打开安装过程中显示的网址（例如 `https://1.2.3.4/setup`）
2. 创建第一个管理员账户（输入电子邮件地址和密码）
3. 登录后，所有已安装的技能会显示在侧边栏中

**如何为自定义域名启用 HTTPS：** 请输入 “Set up SSL for yourdomain.com”

### ERP 公司设置（通过 erpclaw，而非 webclaw）

**重要提示：** 公司设置、演示数据以及所有 ERP 相关操作均由 **erpclaw** 技能处理，而非 webclaw。Webclaw 仅用于 Web 仪表板的管理员管理（如用户管理、SSL 配置、会话管理等）。

**通过 Telegram/CLI 设置公司信息：**
1. 首先运行 `erpclaw initialize-database`（创建数据库表和共享库——首次安装时必须执行）
2. 然后运行 `erpclaw setup-company --name "Company Name" --currency USD --fiscal-year-start-month 1`
3. 可选：运行 `erpclaw seed-demo-data`（加载示例数据）

**严禁** 直接导入 webclaw 的 Python 模块（例如 `from api.auth import ...`）。Webclaw 的 API 作为独立服务运行——请使用下面列出的命令或调用 REST API 进行操作。

## 快速入门（基础级别）

### 检查服务状态
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

Set a specific password for alice
→ runs: reset-password --email alice@company.com --password MyNewPass123!
```

## 所有可用操作（高级级别）

| 操作          | 参数            | 描述                                      |
|----------------|------------------|-------------------------------------------|
| `status`        |                   | 服务状态、SSL 状态、用户数量                        |
| `setup-ssl`      | `--domain`         | 使用 Let's Encrypt 配置 HTTPS                         |
| `renew-ssl`      |                   | 检查并续订 SSL 证书                         |
| `list-users`      |                   | 列出所有 Web 仪表板用户                         |
| `create-user`     | `--email`, `--full-name`, `--role` | 创建用户（使用临时密码）                         |
| `reset-password`    | `--email`, `--password`     | 重置用户密码（可选）                         |
| `disable-user`     | `--email`         | 禁用用户账户                         |
| `list-sessions`     |                   | 显示当前登录中的用户会话                         |
| `clear-sessions`    |                   | 强制所有用户重新登录                         |
| `maintenance`     |                   | 定时清理会话记录、检查 SSL 证书                         |
| `restart-services`    |                   | 重启 API 服务及前端应用程序                         |
| `show-config`     |                   | 显示当前配置信息                         |

### 常用命令参考

| 用户输入           | 执行的操作                        |
|------------------|-------------------------------------------|
| “仪表板是否正在运行？”     | `status`                          |
| “为 example.com 配置 SSL”     | `setup-ssl --domain example.com`                   |
| “谁有 Web 访问权限？”     | `list-users`                          |
| “添加用户 bob@co.com”     | `create-user --email bob@co.com`                   |
| “重置 bob 的密码”     | `reset-password --email bob@co.com`                   |
| “禁用 bob 的 Web 访问权限” | `disable-user --email bob@co.com`                   |
| “当前登录的用户是谁？”     | `list-sessions`                         |
| “强制所有用户重新登录”     | `clear-sessions`                         |
| “重启 Web 仪表板”     | `restart-services`                         |
| “显示 Web 仪表板配置”     | `show-config`                         |

### 建议

- 在创建用户后，提醒用户妥善保管临时密码。
- 在配置 HTTPS 后，确认重定向功能是否正常工作。
- 如果 `status` 显示 SSL 状态为 `false`，建议重新运行 `setup-ssl` 命令。
- 如果 `status` 显示用户数量为 0，建议用户访问 `/setup` 页面进行配置。

## 技术细节（高级级别）

### 架构

- **前端**：使用 Next.js 16、React 19、shadcn/ui 和 Tailwind v4 构建（端口 3000）
- **后端**：使用 FastAPI 和 uvicorn（端口 8001）
- **代理**：nginx（端口 80/443）——将 `/api` 路由转发到后端，将 `/` 路由转发到前端
- **数据库**：使用 SQLite 数据库（文件路径：`~/.openclaw/webclaw/webclaw.sqlite`）

### 8 个通用的 UI 组件

`DataTable`、`FormView`、`DetailView`、`ChatPanel`、`ChartPanel`、`KanbanBoard`、`CalendarView`、`TreeView`——这些组件都会根据技能操作的结果动态渲染。

### 所使用的数据库表

`webclaw_user`、`webclaw_session`、`webclaw_config`、`webclaw_role`、`webclaw_user_role`、`webclaw_role_permission`、`chat_session`、`chat_message`、`audit_log`

### 脚本路径
```
scripts/db_query.py --action <action-name> [--key value ...]
```

### 每个技能的个性化配置

每个技能可以在其 SKILL.md 文件的 `frontmatter` 部分添加 `webclaw` 部分，以实现自定义功能：
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