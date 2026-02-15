---
name: railway
description: 在 Railway.app 上部署和管理应用程序。该平台可用于部署项目、管理服务、查看日志、设置环境变量以及管理数据库。Railway 是一个现代化的云平台，支持无需任何配置即可部署应用程序的功能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🚂",
        "requires": { "bins": ["railway"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "railway",
              "bins": ["railway"],
              "label": "Install Railway CLI (brew)",
            },
            {
              "id": "npm",
              "kind": "npm",
              "package": "@railway/cli",
              "bins": ["railway"],
              "label": "Install Railway CLI (npm)",
            },
          ],
      },
  }
---

# Railway

在 [Railway.app](https://railway.app) 上部署和管理应用程序——这是一个支持零配置部署的现代云平台。

## 认证

```bash
# Login (opens browser)
railway login

# Login with token (CI/CD)
railway login --token <TOKEN>

# Check login status
railway whoami

# Logout
railway logout
```

## 项目管理

### 链接项目并初始化

```bash
# Link current directory to existing project
railway link

# Link to specific project
railway link --project <PROJECT_ID>

# Create new project
railway init

# Unlink project
railway unlink
```

### 查看项目

```bash
# List all projects
railway list

# Open project in browser
railway open

# Show project status
railway status
```

## 部署

### 直接部署

```bash
# Deploy current directory
railway up

# Deploy without watching logs
railway up --detach

# Deploy specific service
railway up --service <SERVICE_NAME>

# Deploy to specific environment
railway up --environment production

# Redeploy latest version
railway redeploy

# Redeploy specific service
railway redeploy --service <SERVICE_NAME>
```

### 从模板部署

```bash
# Deploy a template
railway deploy --template <TEMPLATE_NAME>

# With variables
railway deploy --template postgres --variable POSTGRES_USER=myuser
```

## 服务

```bash
# List services in project
railway service

# Create new service
railway service create

# Delete service
railway service delete <SERVICE_NAME>
```

## 环境变量

```bash
# List all variables
railway variables

# Set variable
railway variables set KEY=value

# Set multiple variables
railway variables set KEY1=value1 KEY2=value2

# Delete variable
railway variables delete KEY

# View specific variable
railway variables get KEY
```

## 日志

```bash
# View logs (live)
railway logs

# View logs for specific service
railway logs --service <SERVICE_NAME>

# View recent logs (not live)
railway logs --no-follow

# View logs with timestamps
railway logs --timestamps
```

## 运行命令

```bash
# Run command with Railway env vars
railway run <command>

# Examples
railway run npm start
railway run python manage.py migrate
railway run prisma db push

# SSH into running service
railway ssh

# SSH into specific service
railway ssh --service <SERVICE_NAME>
```

## 域名

```bash
# List domains
railway domain

# Add custom domain
railway domain add <DOMAIN>

# Remove domain
railway domain delete <DOMAIN>
```

## 数据库

Railway 支持一键式数据库配置：

```bash
# Add PostgreSQL
railway add --plugin postgresql

# Add MySQL
railway add --plugin mysql

# Add Redis
railway add --plugin redis

# Add MongoDB
railway add --plugin mongodb
```

数据库连接字符串会自动添加到环境变量中。

## 环境配置

```bash
# List environments
railway environment

# Switch environment
railway environment <ENV_NAME>

# Create environment
railway environment create <ENV_NAME>

# Delete environment
railway environment delete <ENV_NAME>
```

## 卷（存储资源）

```bash
# List volumes
railway volume

# Create volume
railway volume create --mount /data

# Delete volume
railway volume delete <VOLUME_ID>
```

## 常见工作流程

### 部署新项目

```bash
# 1. Initialize in your project directory
cd my-app
railway init

# 2. Add a database if needed
railway add --plugin postgresql

# 3. Set environment variables
railway variables set NODE_ENV=production

# 4. Deploy
railway up
```

### 连接到生产数据库

```bash
# Run local command with production env vars
railway run psql $DATABASE_URL

# Or use SSH
railway ssh
# Then inside container:
psql $DATABASE_URL
```

### 查看部署状态

```bash
# Check status
railway status

# View logs
railway logs

# Open dashboard
railway open
```

### 回滚部署

```bash
# View deployments in dashboard
railway open

# Redeploy previous version (via dashboard)
# Or redeploy current code
railway redeploy
```

## CI/CD 集成

对于 GitHub Actions 或其他持续集成（CI）工具：

```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Railway CLI
        run: npm i -g @railway/cli
      - name: Deploy
        run: railway up --detach
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## 资源

- [Railway 文档](https://docs.railway.com)
- [Railway 命令行接口参考](https://docs.railway.com/reference/cli-api)
- [Railway 模板](https://railway.app/templates)
- [Railway 的 GitHub 仓库](https://github.com/railwayapp/cli)