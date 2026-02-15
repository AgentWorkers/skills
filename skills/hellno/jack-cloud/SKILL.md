---
name: jack-cloud
description: >
  Deploy web services to the cloud with Jack.
  Use when: you need to create APIs, websites, or backends and deploy them live.
  Teaches: project creation, deployment, databases, logs, and all Jack Cloud services.
allowed-tools: Read, Edit, Grep, Glob
---

# Jack Cloud — 通过终端部署任何内容

Jack 可以通过一个命令来部署 Cloudflare Workers 项目。创建 API、添加数据库，然后将其上线——所有这些操作都可以在终端中完成。

## 安装

```bash
npm i -g @getjack/jack
jack login
```

## MCP 工具

如果您的代理支持 `mcp__jack__*` 工具，建议优先使用这些工具而非 CLI 命令。这些工具会返回结构化的 JSON 数据，并且会自动进行跟踪。对于不支持 MCP 的代理，下面会列出相应的 CLI 命令。

---

## 创建并部署项目

```bash
jack new my-api
```

该命令会根据模板创建一个项目，然后将其部署并显示项目的在线 URL。

**选择模板**（在提示时选择）或使用 `--template` 参数：

| 模板 | 获取的内容 |
|----------|-------------|
| `api` | 带有示例路由的 Hono API |
| `miniapp` | 全栈应用程序（包含前端） |
| `simple-api-starter` | 最简单的 API 开发起点 |

**MCP**：使用 `mcp__jack__create_project` 命令，并传入 `name` 和 `template` 参数。

创建完成后，您的项目将上线，访问地址为 `https://<slug>.runjack.xyz`。

---

## 部署更改

编辑代码后，将更改推送到生产环境：

```bash
jack ship
```

（此命令的输出格式适合脚本和代理程序阅读）

```bash
jack ship --json
```

该命令会构建项目并将其部署到生产环境，整个过程大约需要几秒钟。

**MCP**：使用 `mcp__jack__deploy_project` 命令。

---

## 检查项目状态

```bash
jack info
```

显示项目的在线 URL、最后一次部署时间以及所使用的相关服务（如数据库、存储等）。

**MCP**：使用 `mcp__jack__get_project_status` 命令。

---

## 数据库（D1）

### 创建数据库

```bash
jack services db create
```

该命令会在项目中添加一个 D1 数据库。数据库的绑定信息会自动配置到 `wrangler.jsonc` 文件中。

**MCP**：使用 `mcp__jack__create_database` 命令。

### 查询数据

```bash
jack db execute "SELECT * FROM users LIMIT 10"
```

（若需要 JSON 格式的输出）

```bash
jack db execute --json "SELECT * FROM users LIMIT 10"
```

### 写入数据

```bash
jack db execute --write "INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')"
```

### 创建表格

```bash
jack db execute --write "CREATE TABLE posts (id INTEGER PRIMARY KEY, title TEXT, body TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)"
```

### 查看数据库架构

```bash
jack db execute "SELECT name FROM sqlite_master WHERE type='table'"
jack db execute "PRAGMA table_info(users)"
```

**MCP**：使用 `mcp__jack__execute_sql` 命令；写入操作时需要设置 `allow_write: true`。默认情况下，删除（DROP）和截断（TRUNCATE）等操作是被禁止的。

### 在修改数据库架构后重新部署

创建表格或修改数据库架构后，需要重新部署项目，以便 Workers 能够使用新的数据库结构：

```bash
jack ship
```

---

## 日志

将生产环境的日志流式输出以帮助调试问题：

```bash
jack logs
```

该命令会显示实时的请求/响应日志。按 Ctrl+C 可以停止日志输出。

**MCP**：使用 `mcp__jack__tail_logs` 命令，并通过 `duration_ms` 和 `max_events` 参数来限制日志输出的时长。

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

## 保密信息（Secrets）

用于存储 API 密钥和敏感数据：

```bash
# Set a secret (prompts for value)
jack secrets set STRIPE_SECRET_KEY

# Set multiple
jack secrets set API_KEY WEBHOOK_SECRET

# List secrets (names only, values hidden)
jack secrets list
```

这些保密信息可以在 Workers 中通过 `c.env.SECRET_NAME` 变量访问。添加保密信息后，需要重新部署项目：

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

- `wrangler.jsonc` 文件用于定义数据库绑定信息、环境变量以及兼容性设置。
- `.jack/project.json` 文件用于将本地目录关联到 Jack Cloud 项目。
- `src/index.ts` 是项目的入口文件（通常是一个 Hono 应用程序）。

---

## 高级服务

### 存储（R2）

```bash
jack services storage create          # Create R2 bucket
jack services storage list            # List buckets
jack services storage info            # Bucket details
```

在 Workers 中通过 `c.env.BUCKET` 变量访问存储服务。可用于文件上传、图片存储等操作。

**MCP**：使用 `mcp__jack__create_storage_bucket`、`mcp__jack__list_storage_buckets` 和 `mcp__jack__get_storage_info` 命令。

### 向量搜索（Vectorize）

```bash
jack services vectorize create                    # Create index (768 dims, cosine)
jack services vectorize create --dimensions 1536  # Custom dimensions
jack services vectorize list
jack services vectorize info
```

通过 `c.env.VECTORIZE_INDEX` 变量访问向量搜索功能。适用于语义搜索、RAG（Retrieval with Aggregation）和嵌入计算等场景。

**MCP**：使用 `mcp__jack__create_vectorize_index`、`mcp__jack__list_vectorize_indexes` 和 `mcp__jack__get_vectorize_info` 命令。

### 定时任务（Cron Scheduling）

```bash
jack services cron create "*/15 * * * *"   # Every 15 minutes
jack services cron create "0 * * * *"      # Every hour
jack services cron list
jack services cron test "0 9 * * MON"      # Validate + show next runs
```

您的 Workers 需要实现 `scheduled()` 函数或配置 `POST /__scheduled` 路由来执行定时任务。

**MCP**：使用 `mcp__jack__create_cron`、`mcp__jack__list_crons` 和 `mcp__jack__test_cron` 命令。

### 自定义域名

```bash
jack domain connect app.example.com      # Reserve domain
jack domain assign app.example.com       # Assign to current project
jack domain unassign app.example.com     # Unassign
jack domain disconnect app.example.com   # Fully remove
```

请按照 `assign` 命令后的 DNS 指示操作来配置自定义域名。通常需要添加一个 CNAME 记录。

---

## 列出项目

```bash
jack ls           # List all your projects
jack info my-api  # Details for a specific project
jack open my-api  # Open in browser
```

**MCP**：使用 `mcp__jack__list_projects` 命令列出所有项目，支持 `filter` 参数（可筛选所有项目、本地项目或已部署的项目）。

---

## 故障排除

| 问题 | 解决方法 |
|---------|-----|
| “未认证” | 运行 `jack login` 命令登录 |
| “找不到 wrangler 配置” | 从 Jack 项目目录中运行命令 |
| “找不到数据库” | 运行 `jack services db create` 命令创建数据库 |
| 部署失败 | 查看 `jack logs` 中的错误信息，修复代码后重新部署 |
| 需要重新开始 | 使用 `jack new` 命令创建一个新的项目 |

---

## 参考资料

- [服务详细指南](reference/services-guide.md) — 每项服务的详细使用说明
- [Jack 文档](https://docs.getjack.org)