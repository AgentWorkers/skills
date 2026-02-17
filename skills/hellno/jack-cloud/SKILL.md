---
name: jack-cloud
description: 使用 Jack 将 Web 服务部署到云端。适用场景：当你需要创建 API、网站或后端服务并将其实时部署到云端时。该工具会教授项目创建、部署、数据库管理、日志记录以及所有与 Jack Cloud 相关的服务的使用方法。
homepage: https://getjack.org
metadata: {"clawdbot":{"emoji":"🃏","homepage":"https://github.com/getjack-org/skills","requires":{"bins":["node","npm"],"env":[]},"install":[{"id":"npm","kind":"npm","package":"@getjack/jack","bins":["jack"],"label":"Install Jack CLI (npm)"}]}}
allowed-tools: Read, Edit, Grep, Glob
---
# Jack Cloud — 通过终端部署任何内容

Jack 可以通过一个命令部署 Cloudflare Workers 项目。创建 API、添加数据库，然后将其上线——所有这些操作都可以在终端中完成。

## 安装

```bash
npm i -g @getjack/jack
jack login
```

## 外部端点

| 端点 | 发送的数据 | 用途 |
|----------|-----------|---------|
| `auth.getjack.org` | OAuth 令牌（通过 WorkOS 从 GitHub/Google 获取） | 认证 |
| `control.getjack.org` | 项目元数据及部署时的源代码 | 项目管理和部署 |

## 安全与隐私

- `jack login` 通过浏览器 OAuth（通过 WorkOS 从 GitHub/Google 获取）进行身份验证。认证令牌存储在 `~/.config/jack/auth.json` 文件中 |
- 不需要环境变量——认证过程是交互式的 |
- 源代码会在执行 `jack ship` 时上传，并通过 Jack Cloud 部署到 Cloudflare Workers |
- 项目元数据（名称、slug、部署历史记录）存储在 Jack Cloud 上 |
- 未经用户同意，不会发送任何遥测数据（可以通过 `jack telemetry` 配置） |
- **npm 包：** [@getjack/jack](https://www.npmjs.com/package/@getjack/jack) — 开源命令行工具（CLI） |

## MCP 工具

如果您的代理支持 `mcp__jack__*` 工具，请优先使用这些工具，因为它们返回结构化的 JSON 数据，并且会自动进行跟踪。对于不支持 MCP 的代理，下面会列出相应的 CLI 命令。

---

## 创建并部署项目

```bash
jack new my-api
```

此命令会从模板创建一个项目，然后将其部署并显示上线后的 URL。

**选择模板**（系统会提示您选择）（或使用 `--template` 参数）：

| 模板 | 获得的成果 |
|----------|-------------|
| `api` | 带有示例路由的 Hono API |
| `hello` | 最简单的 “hello-world” 启动项目 |
| `miniapp` | 全栈应用程序（包含前端） |
| `ai-chat` | 带有实时聊天功能的 AI 应用程序 |
| `nextjs` | 使用 Next.js 构建的全栈应用程序 |

运行 `jack new` 可查看所有可用模板。

**MCP：** 使用 `mcp__jack__create_project` 命令，并传入 `name` 和 `template` 参数。

创建完成后，您的项目将上线，网址为 `https://<slug>.runjack.xyz`。

---

## 部署更改

编辑代码后，将更改推送到服务器：

```bash
jack ship
```

（此部分提供机器可读的输出，适用于脚本和代理程序）

```bash
jack ship --json
```

该命令会构建项目并将其部署到生产环境，整个过程需要几秒钟。

**MCP：** 使用 `mcp__jack__deploy_project` 命令。

---

## 检查项目状态

```bash
jack info
```

显示项目的上线 URL、最后一次部署时间以及所使用的服务（数据库、存储等）。

**MCP：** 使用 `mcp__jack__get_project_status` 命令。

---

## 数据库（D1）

```bash
jack services db create                  # Add D1 database (auto-configures wrangler.jsonc)
jack db execute "SELECT * FROM users"    # Query data
jack db execute --json "SELECT ..."      # JSON output
jack db execute --write "INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')"
jack db execute --write "CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT, body TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
jack db execute "SELECT name FROM sqlite_master WHERE type='table'"   # View schema
jack db execute "PRAGMA table_info(users)"
```

修改数据库架构后，需要使用 `jack ship` 命令重新部署项目。

**MCP：** 使用 `mcp__jack__create_database` 和 `mcp__jack__execute_sql` 命令；请确保设置 `allow_write: true` 以允许写入操作；默认情况下，`DROP` 和 `TRUNCATE` 操作是被禁止的。

---

## 日志

将生产环境的日志流式输出以便调试问题：

```bash
jack logs
```

显示实时的请求/响应日志。按 Ctrl+C 可停止日志输出。

**MCP：** 使用 `mcp__jack__tail_logs` 命令，可以通过 `duration_ms` 和 `max_events` 参数来限制日志输出的范围。

---

## 常见工作流程：API 与数据库的结合使用

```bash
# 1. Create project
jack new my-api --template api

# 2. Add database
jack services db create

# 3. Create tables
jack db execute --write "CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"

# 4. Edit src/index.ts — add routes that query the DB
#    Access DB via: c.env.DB (the D1 binding)

# 5. Deploy
jack ship

# 6. Verify
curl https://my-api.runjack.xyz/api/items
```

---

## 保密信息

如何存储 API 密钥和敏感数据：

```bash
# Set a secret (prompts for value)
jack secrets set STRIPE_SECRET_KEY

# Set multiple
jack secrets set API_KEY WEBHOOK_SECRET

# List secrets (names only, values hidden)
jack secrets list
```

这些保密信息可以在 worker 中通过 `c.env.SECRET_NAME` 变量访问。添加新保密信息后，需要重新部署项目：

```bash
jack ship
```

---

## 项目结构

```
my-project/
├── src/
│   └── index.ts          # Worker entry point
├── wrangler.jsonc        # Config: bindings, routes, compatibility
├── package.json
└── .jack/
    └── project.json      # Links to Jack Cloud
```

- `wrangler.jsonc` 文件定义了数据库连接信息（D1）、环境变量以及兼容性设置 |
- `.jack/project.json` 文件将本地目录与 Jack Cloud 项目关联起来 |
- `src/index.ts` 是项目的入口文件——通常是一个 Hono 应用程序 |

---

## 高级功能

### 存储服务（R2）

```bash
jack services storage create          # Create R2 bucket
jack services storage list            # List buckets
jack services storage info            # Bucket details
```

在 worker 中通过 `c.env.BUCKET` 变量访问存储服务。可用于文件上传、图片存储等操作。

**MCP：** 使用 `mcp__jack__create_storage_bucket`、`mcp__jack__list_storage_buckets` 和 `mcp__jack__get_storage_info` 命令。

### 向量搜索（Vectorize）

```bash
jack services vectorize create                    # Create index (768 dims, cosine)
jack services vectorize create --dimensions 1536  # Custom dimensions
jack services vectorize list
jack services vectorize info
```

通过 `c.env.VECTORIZE_INDEX` 变量访问向量化服务。适用于语义搜索、RAG（Retrieval with Aggregation）和嵌入模型等场景。

**MCP：** 使用 `mcp__jack__create_vectorize_index`、`mcp__jack__list_vectorize_indexes` 和 `mcp__jack__get_vectorize_info` 命令。

### 定时任务调度

```bash
jack services cron create "*/15 * * * *"   # Every 15 minutes
jack services cron create "0 * * * *"      # Every hour
jack services cron list
jack services cron test "0 9 * * MON"      # Validate + show next runs
```

您的 worker 需要配置 `scheduled()` 处理程序或使用 `/__scheduled` 路由来实现定时任务。

**MCP：** 使用 `mcp__jack__create_cron`、`mcp__jack__list_crons` 和 `mcp__jack__test_cron` 命令。

### 自定义域名

```bash
jack domain connect app.example.com      # Reserve domain
jack domain assign app.example.com       # Assign to current project
jack domain unassign app.example.com     # Unassign
jack domain disconnect app.example.com   # Fully remove
```

请按照 `assign` 命令后的 DNS 指示进行操作。通常需要添加一个 CNAME 记录。

---

## 列出所有项目

```bash
jack ls           # List all your projects
jack info my-api  # Details for a specific project
jack open my-api  # Open in browser
```

**MCP：** 使用 `mcp__jack__list_projects` 命令列出所有项目，支持 `filter` 参数（可过滤所有项目、仅显示本地项目或已部署到云上的项目）。

---

## 故障排除

| 问题 | 解决方案 |
|---------|-----|
| “无法认证” | 运行 `jack login` 命令进行登录 |
| “找不到 wrangler 配置” | 请从 Jack 项目的目录中运行命令 |
| “找不到数据库” | 运行 `jack services db create` 命令创建数据库 |
| 部署失败 | 查看 `jack logs` 中的错误信息，修复代码后再次使用 `jack ship` 命令部署 |
| 需要重新开始 | 使用 `jack new` 命令创建一个新的项目 |

---

## 参考资料

- [服务详细指南](reference/services-guide.md) — 每项服务的详细使用说明 |
- [Jack 文档](https://docs.getjack.org) — 官方文档