---
name: cloudflare
description: 使用 Wrangler CLI 管理 Cloudflare Workers、KV（键值存储）、D1（对象存储）和 R2（对象存储）以及相关秘密信息。该工具适用于部署 Workers、管理数据库、存储对象以及配置 Cloudflare 资源等场景。内容包括 Workers 的部署、KV 命名空间的管理、D1 SQL 数据库的操作、R2 对象存储的利用、秘密信息的处理，以及日志的跟踪与分析。
---

# Cloudflare（Wrangler CLI）

通过 `wrangler` CLI 管理 Cloudflare Workers 及相关服务。

## 前提条件

- 需要 Node.js v20 或更高版本
- 安装方法：`npm install -g wrangler` 或使用项目内的 `npx wrangler`
- 登录：`wrangler login`（会打开浏览器进行 OAuth 登录）
- 查看用户信息：`wrangler whoami`

## 快速参考

### Workers

```bash
# Initialize new worker
wrangler init <name>

# Local development
wrangler dev [script]

# Deploy
wrangler deploy [script]

# List deployments
wrangler deployments list

# View deployment
wrangler deployments view [deployment-id]

# Rollback
wrangler rollback [version-id]

# Delete worker
wrangler delete [name]

# Tail logs (live)
wrangler tail [worker]
```

### Secrets（密钥值对）

```bash
# Add/update secret (interactive)
wrangler secret put <key>

# Add secret from stdin
echo "value" | wrangler secret put <key>

# List secrets
wrangler secret list

# Delete secret
wrangler secret delete <key>

# Bulk upload from JSON file
wrangler secret bulk secrets.json
```

### KV（键值存储）

```bash
# Create namespace
wrangler kv namespace create <name>

# List namespaces
wrangler kv namespace list

# Delete namespace
wrangler kv namespace delete --namespace-id <id>

# Put key
wrangler kv key put <key> <value> --namespace-id <id>

# Get key
wrangler kv key get <key> --namespace-id <id>

# Delete key
wrangler kv key delete <key> --namespace-id <id>

# List keys
wrangler kv key list --namespace-id <id>

# Bulk operations (JSON file)
wrangler kv bulk put <file> --namespace-id <id>
wrangler kv bulk delete <file> --namespace-id <id>
```

### D1（SQL 数据库）

```bash
# Create database
wrangler d1 create <name>

# List databases
wrangler d1 list

# Database info
wrangler d1 info <name>

# Execute SQL
wrangler d1 execute <database> --command "SELECT * FROM users"

# Execute SQL file
wrangler d1 execute <database> --file schema.sql

# Local execution (for dev)
wrangler d1 execute <database> --local --command "..."

# Export database
wrangler d1 export <name> --output backup.sql

# Delete database
wrangler d1 delete <name>

# Migrations
wrangler d1 migrations create <database> <name>
wrangler d1 migrations apply <database>
wrangler d1 migrations list <database>
```

### R2（对象存储）

```bash
# Create bucket
wrangler r2 bucket create <name>

# List buckets
wrangler r2 bucket list

# Delete bucket
wrangler r2 bucket delete <name>

# Upload object
wrangler r2 object put <bucket>/<key> --file <path>

# Download object
wrangler r2 object get <bucket>/<key> --file <path>

# Delete object
wrangler r2 object delete <bucket>/<key>
```

### Queues（队列）

```bash
# Create queue
wrangler queues create <name>

# List queues
wrangler queues list

# Delete queue
wrangler queues delete <name>
```

## 配置文件

Wrangler 支持 TOML 和 JSON/JSONC 两种配置格式：

- `wrangler.toml` — 传统格式
- `wrangler.json` 或 `wrangler.jsonc` — 新格式，支持 JSON 模式

**⚠️ 重要提示：** 如果两种配置文件都存在，JSON 格式优先。请选择一种格式以避免因修改 TOML 文件而导致配置被忽略的问题。

### JSONC 格式（支持自动补全）

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2024-12-30"
}
```

### TOML 格式

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-30"
```

### 使用绑定（Bindings）进行配置

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-12-30"

# KV binding
[[kv_namespaces]]
binding = "MY_KV"
id = "xxx"

# D1 binding
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxx"

# R2 binding
[[r2_buckets]]
binding = "BUCKET"
bucket_name = "my-bucket"

# Environment variables
[vars]
API_URL = "https://api.example.com"

# Secrets (set via `wrangler secret put`)
# Referenced as env.SECRET_NAME in worker code
```

### 静态资源（适用于 Next.js 等框架）

```toml
name = "my-site"
main = ".open-next/worker.js"
compatibility_date = "2024-12-30"
compatibility_flags = ["nodejs_compat"]

[assets]
directory = ".open-next/assets"
binding = "ASSETS"
```

## 常见操作模式

### 基于环境变量进行部署

```bash
wrangler deploy -e production
wrangler deploy -e staging
```

### 自定义域名（通过控制台或 API）

自定义域名需要在 Cloudflare 控制台的 Worker Settings > Domains & Routes 中配置，或通过 Cloudflare API 进行配置。Wrangler 不直接管理自定义域名。

### 使用绑定进行本地开发

```bash
# Creates local D1/KV/R2 for dev
wrangler dev --local
```

### 检查部署状态

```bash
wrangler deployments list
wrangler deployments view
```

## Wrangler 不支持的功能

- **DNS 管理** — 请使用 Cloudflare 控制台或 API 进行 DNS 记录管理
- **自定义域名** — 请通过控制台（Worker Settings > Domains & Routes）或 API 进行配置
- **SSL 证书** — 当添加自定义域名时，由 Cloudflare 自动管理
- **防火墙/WAF 规则** — 请使用控制台或 API 进行配置

有关 DNS/域名管理的更多信息，请参阅 `cloudflare` 技能文档（直接使用 Cloudflare API）。

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| “未授权” | 运行 `wrangler login` 命令登录 |
| Node 版本错误 | 需要 Node.js v20 或更高版本 |
| “未找到配置文件” | 确保配置文件（`wrangler.toml` 或 `wrangler.jsonc`）存在，或使用 `-c path/to/config` 参数指定配置文件路径 |
| 配置更改未被应用 | 检查 `wrangler.json`/`wrangler.jsonc` 文件的内容 — JSON 格式优先于 TOML 格式 |
| 绑定配置未找到 | 确认 `wrangler.toml` 中的绑定配置与代码中的引用一致 |

## 资源

- [Wrangler 文档](https://developers.cloudflare.com/workers/wrangler/)
- [Workers 文档](https://developers.cloudflare.com/workers/)
- [D1 文档](https://developers.cloudflare.com/d1/)
- [R2 文档](https://developers.cloudflare.com/r2/)
- [KV 文档](https://developers.cloudflare.com/kv/)