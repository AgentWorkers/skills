---
name: coolify
description: 通过 Coolify API 管理 Coolify 的部署、应用程序、数据库和服务。当用户需要部署、启动、停止、重启或管理托管在 Coolify 上的应用程序时，可以使用该 API。
homepage: https://coolify.io
user-invocable: true
metadata: {"openclaw":{"emoji":"🚀","requires":{"bins":["node"],"env":["COOLIFY_TOKEN"]},"primaryEnv":"COOLIFY_TOKEN"}}
---

# Coolify API 技能

通过 Coolify API 对 Coolify 的部署、应用程序、数据库、服务及基础设施进行全面管理。

## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 将应用程序部署到 Coolify
- 管理应用程序的生命周期（启动、停止、重启）
- 查看应用程序日志
- 创建和管理数据库（PostgreSQL、MySQL、MongoDB、Redis 等）
- 部署 Docker Compose 服务
- 管理服务器和基础设施
- 配置环境变量
- 触发和监控部署
- 管理 GitHub 应用程序集成
- 配置 SSH 私钥

## 先决条件

1. **Coolify API 令牌** — 从 Coolify 仪表板生成：
   - 转到 **Keys & Tokens** → **API tokens**
   - 创建具有适当权限（`read`、`write`、`deploy`）的令牌
   - 设置 `COOLIFY_TOKEN` 环境变量

2. **bash、curl、jq** — 运行 bash 脚本所必需的工具

3. **API 访问权限** — Coolify Cloud（`app.coolify.io`）或自托管实例

## 快速入门

### 基本命令

```bash
# List all applications
{baseDir}/scripts/coolify applications list

# Get application details
{baseDir}/scripts/coolify applications get --uuid abc-123

# Deploy an application
{baseDir}/scripts/coolify deploy --uuid abc-123 --force

# View application logs
{baseDir}/scripts/coolify applications logs --uuid abc-123

# Restart an application
{baseDir}/scripts/coolify applications restart --uuid abc-123
```

---

## 应用程序

### 列出应用程序

```bash
{baseDir}/scripts/coolify applications list
```

**输出：**
```json
{
  "success": true,
  "data": [
    {
      "uuid": "abc-123",
      "name": "my-app",
      "status": "running",
      "fqdn": "https://app.example.com"
    }
  ],
  "count": 1
}
```

### 获取应用程序详情

```bash
{baseDir}/scripts/coolify applications get --uuid abc-123
```

### 应用程序生命周期

```bash
# Start
{baseDir}/scripts/coolify applications start --uuid abc-123

# Stop
{baseDir}/scripts/coolify applications stop --uuid abc-123

# Restart
{baseDir}/scripts/coolify applications restart --uuid abc-123
```

### 查看日志

```bash
{baseDir}/scripts/coolify applications logs --uuid abc-123
```

### 环境变量

```bash
# List environment variables
{baseDir}/scripts/coolify applications envs list --uuid abc-123

# Create environment variable
{baseDir}/scripts/coolify applications envs create \
  --uuid abc-123 \
  --key DATABASE_URL \
  --value "postgres://user:pass@host:5432/db" \
  --is-runtime true \
  --is-buildtime false

# Update environment variable
{baseDir}/scripts/coolify applications envs update \
  --uuid abc-123 \
  --env-uuid env-456 \
  --value "new-value"

# Bulk update environment variables
{baseDir}/scripts/coolify applications envs bulk-update \
  --uuid abc-123 \
  --json '{"DATABASE_URL":"postgres://...","API_KEY":"..."}'

# Delete environment variable
{baseDir}/scripts/coolify applications envs delete \
  --uuid abc-123 \
  --env-uuid env-456
```

### 创建应用程序

```bash
# Public Git repository
{baseDir}/scripts/coolify applications create-public \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --git-repository "https://github.com/user/repo" \
  --git-branch main \
  --name "My App"

# Private GitHub App
{baseDir}/scripts/coolify applications create-private-github-app \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --github-app-uuid gh-789 \
  --git-repository "user/repo" \
  --git-branch main

# Dockerfile
{baseDir}/scripts/coolify applications create-dockerfile \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --dockerfile-location "./Dockerfile" \
  --name "My Docker App"

# Docker Image
{baseDir}/scripts/coolify applications create-dockerimage \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --docker-image "nginx:latest" \
  --name "Nginx"

# Docker Compose
{baseDir}/scripts/coolify applications create-dockercompose \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --docker-compose-location "./docker-compose.yml"
```

---

## 数据库

### 列出数据库

```bash
{baseDir}/scripts/coolify databases list
```

### 获取数据库详情

```bash
{baseDir}/scripts/coolify databases get --uuid db-123
```

### 数据库生命周期

```bash
# Start
{baseDir}/scripts/coolify databases start --uuid db-123

# Stop
{baseDir}/scripts/coolify databases stop --uuid db-123

# Restart
{baseDir}/scripts/coolify databases restart --uuid db-123

# Delete
{baseDir}/scripts/coolify databases delete --uuid db-123
```

### 创建数据库

```bash
# PostgreSQL
{baseDir}/scripts/coolify databases create-postgresql \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "my-postgres" \
  --postgres-user admin \
  --postgres-password secret \
  --postgres-db myapp

# MySQL
{baseDir}/scripts/coolify databases create-mysql \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "my-mysql"

# MariaDB
{baseDir}/scripts/coolify databases create-mariadb \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "my-mariadb"

# MongoDB
{baseDir}/scripts/coolify databases create-mongodb \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "my-mongo"

# Redis
{baseDir}/scripts/coolify databases create-redis \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "my-redis"

# KeyDB
{baseDir}/scripts/coolify databases create-keydb \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "my-keydb"

# ClickHouse
{baseDir}/scripts/coolify databases create-clickhouse \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "my-clickhouse"

# Dragonfly
{baseDir}/scripts/coolify databases create-dragonfly \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "my-dragonfly"
```

### 备份

```bash
# List backup configurations
{baseDir}/scripts/coolify databases backups list --uuid db-123

# Create backup configuration
{baseDir}/scripts/coolify databases backups create \
  --uuid db-123 \
  --frequency "0 2 * * *" \
  --enabled true

# Get backup details
{baseDir}/scripts/coolify databases backups get \
  --uuid db-123 \
  --backup-uuid backup-456

# Update backup
{baseDir}/scripts/coolify databases backups update \
  --uuid db-123 \
  --backup-uuid backup-456 \
  --frequency "0 3 * * *"

# Trigger manual backup
{baseDir}/scripts/coolify databases backups trigger \
  --uuid db-123 \
  --backup-uuid backup-456

# List backup executions
{baseDir}/scripts/coolify databases backups executions \
  --uuid db-123 \
  --backup-uuid backup-456

# Delete backup configuration
{baseDir}/scripts/coolify databases backups delete \
  --uuid db-123 \
  --backup-uuid backup-456
```

---

## 服务（Docker Compose）

### 列出服务

```bash
{baseDir}/scripts/coolify services list
```

### 获取服务详情

```bash
{baseDir}/scripts/coolify services get --uuid service-123
```

### 服务生命周期

```bash
# Start
{baseDir}/scripts/coolify services start --uuid service-123

# Stop
{baseDir}/scripts/coolify services stop --uuid service-123

# Restart
{baseDir}/scripts/coolify services restart --uuid service-123

# Delete
{baseDir}/scripts/coolify services delete --uuid service-123
```

### 创建服务

```bash
{baseDir}/scripts/coolify services create \
  --project-uuid proj-123 \
  --server-uuid server-456 \
  --name "My Service" \
  --docker-compose '{"version":"3.8","services":{"web":{"image":"nginx"}}}'
```

### 环境变量

```bash
# List
{baseDir}/scripts/coolify services envs list --uuid service-123

# Create
{baseDir}/scripts/coolify services envs create \
  --uuid service-123 \
  --key API_KEY \
  --value "secret"

# Update
{baseDir}/scripts/coolify services envs update \
  --uuid service-123 \
  --env-uuid env-456 \
  --value "new-secret"

# Bulk update
{baseDir}/scripts/coolify services envs bulk-update \
  --uuid service-123 \
  --json '{"API_KEY":"secret","DB_HOST":"localhost"}'

# Delete
{baseDir}/scripts/coolify services envs delete \
  --uuid service-123 \
  --env-uuid env-456
```

---

## 部署

### 部署应用程序

```bash
# Deploy by UUID
{baseDir}/scripts/coolify deploy --uuid abc-123

# Force rebuild
{baseDir}/scripts/coolify deploy --uuid abc-123 --force

# Deploy by tag
{baseDir}/scripts/coolify deploy --tag production

# Instant deploy (skip queue)
{baseDir}/scripts/coolify deploy --uuid abc-123 --instant-deploy
```

### 列出部署

```bash
# List all running deployments
{baseDir}/scripts/coolify deployments list

# List deployments for specific application
{baseDir}/scripts/coolify deployments list-for-app --uuid abc-123
```

### 获取部署详情

```bash
{baseDir}/scripts/coolify deployments get --uuid deploy-456
```

### 取消部署

```bash
{baseDir}/scripts/coolify deployments cancel --uuid deploy-456
```

---

## 服务器

### 列出服务器

```bash
{baseDir}/scripts/coolify servers list
```

### 获取服务器详情

```bash
{baseDir}/scripts/coolify servers get --uuid server-123
```

### 创建服务器

```bash
{baseDir}/scripts/coolify servers create \
  --name "Production Server" \
  --ip "192.168.1.100" \
  --port 22 \
  --user root \
  --private-key-uuid key-456
```

### 更新服务器

```bash
{baseDir}/scripts/coolify servers update \
  --uuid server-123 \
  --name "Updated Name" \
  --description "Production environment"
```

### 验证服务器

```bash
{baseDir}/scripts/coolify servers validate --uuid server-123
```

### 获取服务器资源

```bash
# List all resources on server
{baseDir}/scripts/coolify servers resources --uuid server-123

# Get domains configured on server
{baseDir}/scripts/coolify servers domains --uuid server-123
```

### 删除服务器

```bash
{baseDir}/scripts/coolify servers delete --uuid server-123
```

---

## 项目

### 列出项目

```bash
{baseDir}/scripts/coolify projects list
```

### 获取项目详情

```bash
{baseDir}/scripts/coolify projects get --uuid proj-123
```

### 创建项目

```bash
{baseDir}/scripts/coolify projects create \
  --name "My Project" \
  --description "Production project"
```

### 更新项目

```bash
{baseDir}/scripts/coolify projects update \
  --uuid proj-123 \
  --name "Updated Name"
```

### 删除项目

```bash
{baseDir}/scripts/coolify projects delete --uuid proj-123
```

### 环境

```bash
# List environments
{baseDir}/scripts/coolify projects environments list --uuid proj-123

# Create environment
{baseDir}/scripts/coolify projects environments create \
  --uuid proj-123 \
  --name "staging"

# Get environment details
{baseDir}/scripts/coolify projects environments get \
  --uuid proj-123 \
  --environment staging

# Delete environment
{baseDir}/scripts/coolify projects environments delete \
  --uuid proj-123 \
  --environment staging
```

---

## 团队

### 列出团队

```bash
{baseDir}/scripts/coolify teams list
```

### 获取当前团队

```bash
{baseDir}/scripts/coolify teams current
```

### 获取团队成员

```bash
{baseDir}/scripts/coolify teams members
```

### 通过 ID 获取团队

```bash
{baseDir}/scripts/coolify teams get --id 1
```

---

## 安全（私钥）

### 列出私钥

```bash
{baseDir}/scripts/coolify security keys list
```

### 获取私钥

```bash
{baseDir}/scripts/coolify security keys get --uuid key-123
```

### 创建私钥

```bash
{baseDir}/scripts/coolify security keys create \
  --name "Production Key" \
  --description "SSH key for production servers" \
  --private-key "$(cat ~/.ssh/id_rsa)"
```

### 更新私钥

```bash
{baseDir}/scripts/coolify security keys update \
  --uuid key-123 \
  --name "Updated Key Name"
```

### 删除私钥

```bash
{baseDir}/scripts/coolify security keys delete --uuid key-123
```

---

## GitHub 应用程序

### 列出 GitHub 应用程序

```bash
{baseDir}/scripts/coolify github-apps list
```

### 获取 GitHub 应用程序

```bash
{baseDir}/scripts/coolify github-apps get --uuid gh-123
```

### 创建 GitHub 应用程序

```bash
{baseDir}/scripts/coolify github-apps create \
  --name "My GitHub App" \
  --app-id 123456 \
  --installation-id 789012 \
  --private-key "$(cat github-app-key.pem)"
```

### 更新 GitHub 应用程序

```bash
{baseDir}/scripts/coolify github-apps update \
  --uuid gh-123 \
  --name "Updated App Name"
```

### 删除 GitHub 应用程序

```bash
{baseDir}/scripts/coolify github-apps delete --uuid gh-123
```

### 列出仓库

```bash
{baseDir}/scripts/coolify github-apps repos --uuid gh-123
```

### 列出分支

```bash
{baseDir}/scripts/coolify github-apps branches \
  --uuid gh-123 \
  --owner myorg \
  --repo myrepo
```

---

## 常见用例

### 部署新应用程序

1. **列出可用服务器：**
   ```bash
   {baseDir}/scripts/coolify servers list
   ```

2. **创建应用程序：**
   ```bash
   {baseDir}/scripts/coolify applications create-public \
     --project-uuid proj-123 \
     --server-uuid server-456 \
     --git-repository "https://github.com/user/repo" \
     --git-branch main \
     --name "My App"
   ```

3. **配置环境变量：**
   ```bash
   {baseDir}/scripts/coolify applications envs create \
     --uuid <new-app-uuid> \
     --key DATABASE_URL \
     --value "postgres://..." \
     --is-runtime true
   ```

4. **部署：**
   ```bash
   {baseDir}/scripts/coolify deploy --uuid <new-app-uuid>
   ```

### 设置数据库并备份

1. **创建数据库：**
   ```bash
   {baseDir}/scripts/coolify databases create-postgresql \
     --project-uuid proj-123 \
     --server-uuid server-456 \
     --name "production-db"
   ```

2. **配置每日备份：**
   ```bash
   {baseDir}/scripts/coolify databases backups create \
     --uuid <db-uuid> \
     --frequency "0 2 * * *" \
     --enabled true
   ```

3. **手动触发备份：**
   ```bash
   {baseDir}/scripts/coolify databases backups trigger \
     --uuid <db-uuid> \
     --backup-uuid <backup-uuid>
   ```

### 监控应用程序状态

1. **检查应用程序状态：**
   ```bash
   {baseDir}/scripts/coolify applications get --uuid abc-123
   ```

2. **查看最近日志：**
   ```bash
   {baseDir}/scripts/coolify applications logs --uuid abc-123
   ```

3. **列出最近部署：**
   ```bash
   {baseDir}/scripts/coolify deployments list-for-app --uuid abc-123
   ```

---

## 故障排除

### “API 令牌未配置”

**原因：** `COOLIFY_TOKEN` 环境变量未设置。

**解决方法：**
```bash
export COOLIFY_TOKEN="your-token-here"
```

或者在 OpenClaw 配置文件 `~/.openclaw/openclaw.json` 中进行配置：
```json
{
  "skills": {
    "entries": {
      "coolify": {
        "apiKey": "your-token-here"
      }
    }
  }
}
```

### “超出速率限制”

**原因：** 短时间内发送了过多 API 请求。

**解决方法：** 客户端会自动进行指数级重试。请等待重试或降低请求频率。

### “找不到应用程序”

**原因：** UUID 无效或不存在。

**解决方法：**
```bash
# List all applications to find correct UUID
{baseDir}/scripts/coolify applications list
```

### “connect ECONNREFUSED”

**原因：** 无法连接到 Coolify API。

**针对自托管实例的解决方案：**
```bash
# Set custom API URL
export COOLIFY_API_URL="https://your-coolify.example.com/api/v1"
```

**针对云环境的解决方案：** 检查网络连接，并确保 `app.coolify.io` 可访问。

### “部署失败”

**原因：** 构建或部署过程中出现错误。

**解决方法：**
1. 检查部署日志：
   ```bash
   {baseDir}/scripts/coolify deployments get --uuid deploy-456
   ```

2. 检查应用程序日志：
   ```bash
   {baseDir}/scripts/coolify applications logs --uuid abc-123
   ```

3. 确认环境变量设置正确：
   ```bash
   {baseDir}/scripts/coolify applications envs list --uuid abc-123
   ```

### 未找到 Node.js

**原因：** 未安装 Node.js 或未将其添加到 PATH 环境变量中。

**解决方法：**
```bash
# macOS (via Homebrew)
brew install node

# Verify installation
node --version
```

---

## 输出格式

所有命令返回结构化的 JSON 数据：

### 成功响应

```json
{
  "success": true,
  "data": { ... },
  "count": 42
}
```

### 错误响应

```json
{
  "success": false,
  "error": {
    "type": "APIError",
    "message": "Application not found",
    "hint": "Use 'applications list' to find valid UUIDs"
  }
}
```

---

## 配置

### 环境变量

| 变量 | 是否必需 | 默认值 | 描述 |
|----------|----------|---------|-------------|
| `COOLIFY_TOKEN` | 是 | — | 来自 Coolify 仪表板的 API 令牌 |
| `COOLIFY_API_URL` | 否 | `https://app.coolify.io/api/v1` | （针对自托管环境的 API 基本地址） |

### 自托管 Coolify

对于自托管实例，请设置 API 地址：

```bash
export COOLIFY_API_URL="https://coolify.example.com/api/v1"
export COOLIFY_TOKEN="your-token-here"
```

---

## 其他资源

- **Coolify 文档：** https://coolify.io/docs/
- **API 参考：** 查看 `{baseDir}/references/API.md`
- **GitHub：** https://github.com/coollabsio/coolify
- **Discord：** https://coollabs.io/discord

---

## 特殊情况与最佳实践

### UUID 与名称

大多数命令需要使用 UUID，而非名称。请始终先使用 `list` 命令来查找 UUID：

```bash
# Bad: Using name (will fail)
{baseDir}/scripts/coolify applications get --uuid "my-app"

# Good: Using UUID
{baseDir}/scripts/coolify applications list  # Find UUID first
{baseDir}/scripts/coolify applications get --uuid abc-123
```

### 强制部署

请谨慎使用 `--force` 标志，因为它会从头开始重建应用程序：

```bash
# Normal deployment (uses cache)
{baseDir}/scripts/coolify deploy --uuid abc-123

# Force rebuild (slower, but ensures clean build)
{baseDir}/scripts/coolify deploy --uuid abc-123 --force
```

### 更新环境变量

更新环境变量后，请重启应用程序：

```bash
# Update env var
{baseDir}/scripts/coolify applications envs update \
  --uuid abc-123 \
  --env-uuid env-456 \
  --value "new-value"

# Restart to apply changes
{baseDir}/scripts/coolify applications restart --uuid abc-123
```

### 备份频率

使用 cron 表达式来安排备份任务：

| 表达式 | 描述 |
|------------|-------------|
| `0 2 * * *` | 每天凌晨 2 点 |
| `0 */6 * * *` | 每 6 小时 |
| `0 0 * * 0` | 每周日午夜 |
| `0 0 1 * *` | 每月 1 日午夜 |

---

## 总结

此技能提供了对 Coolify API 的全面访问权限，涵盖以下方面：
- **应用程序** — 部署、生命周期管理、日志记录、环境变量
- **数据库** — 8 种数据库类型、备份及生命周期管理
- **服务** — Docker Compose 服务编排
- **部署** — 触发、监控、取消部署
- **服务器** — 基础设施管理和验证
- **项目** — 组织结构和环境管理
- **团队** — 访问控制和协作
- **安全** — SSH 密钥管理
- **GitHub 应用程序** — 仓库集成

所有操作返回结构化的 JSON 数据，便于代理程序进行处理。