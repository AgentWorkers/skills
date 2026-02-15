---
name: neondb
description: 管理Neon无服务器Postgres数据库。可以创建项目、分支、数据库并执行查询。非常适合需要持久存储且支持分支结构的代理工作流程（类似于数据库中的Git），具备零扩展能力以及即时配置功能。
homepage: https://neon.tech
metadata: {"openclaw":{"emoji":"🐘","requires":{"bins":["neonctl"]},"install":[{"id":"brew","kind":"brew","package":"neonctl","bins":["neonctl"],"label":"Install neonctl (Homebrew)"},{"id":"npm","kind":"node","package":"neonctl","bins":["neonctl"],"label":"Install neonctl (npm)"}]}}
---

# NeonDB

Neon 是一款 **无服务器版的 Postgres** 数据库解决方案——支持零成本扩展、类似 Git 的分支管理功能以及即时资源分配。它非常适合那些需要数据库但无需运维开销的 AI 代理系统。

## 为什么选择 Neon 作为代理系统的数据库？

- **即时创建数据库**：只需几秒钟即可创建新数据库，无需进行任何服务器配置。
- **分支管理**：可以像使用 Git 一样创建数据库分支（进行测试时不会影响生产环境）。
- **零成本扩展**：在空闲状态下无需支付任何费用。
- **内置连接池**：无需额外安装 PgBouncer 等中间件。
- **丰富的免费 tier**：提供 0.5 GB 的存储空间和每月 190 小时的计算资源。

## 快速入门

### 1. 安装命令行工具（CLI）

```bash
# Homebrew (recommended)
brew install neonctl

# Or npm
npm i -g neonctl
```

### 2. 进行身份验证

```bash
# Interactive (opens browser)
neonctl auth

# Or with API key (get from console.neon.tech)
export NEON_API_KEY=your_api_key_here
```

### 3. 创建第一个项目

```bash
neonctl projects create --name "my-agent-db"
```

## 核心命令

### 项目（顶层容器）

```bash
# List all projects
neonctl projects list

# Create project
neonctl projects create --name "project-name"

# Delete project
neonctl projects delete <project-id>

# Get project details
neonctl projects get <project-id>
```

### 分支（数据库快照）

```bash
# List branches
neonctl branches list --project-id <project-id>

# Create branch (fork from main)
neonctl branches create --project-id <project-id> --name "dev-branch"

# Create branch from specific point
neonctl branches create --project-id <project-id> --name "restore-test" --parent main --timestamp "2024-01-15T10:00:00Z"

# Reset branch to parent
neonctl branches reset <branch-id> --project-id <project-id> --parent

# Delete branch
neonctl branches delete <branch-id> --project-id <project-id>

# Compare schemas
neonctl branches schema-diff --project-id <project-id> --base-branch main --compare-branch dev
```

### 数据库

```bash
# List databases
neonctl databases list --project-id <project-id> --branch <branch-name>

# Create database
neonctl databases create --project-id <project-id> --branch <branch-name> --name "mydb"

# Delete database
neonctl databases delete <db-name> --project-id <project-id> --branch <branch-name>
```

### 连接字符串

```bash
# Get connection string (default branch)
neonctl connection-string --project-id <project-id>

# Get connection string for specific branch
neonctl connection-string <branch-name> --project-id <project-id>

# Pooled connection (recommended for serverless)
neonctl connection-string --project-id <project-id> --pooled

# Extended format (with all details)
neonctl connection-string --project-id <project-id> --extended
```

### 角色（数据库用户）

```bash
# List roles
neonctl roles list --project-id <project-id> --branch <branch-name>

# Create role
neonctl roles create --project-id <project-id> --branch <branch-name> --name "app_user"
```

## 执行查询

### 使用 psql 命令行工具

```bash
# Get connection string and connect
neonctl connection-string --project-id <project-id> | xargs psql

# Or direct
psql "$(neonctl connection-string --project-id <project-id>)"
```

### 在代码中使用连接字符串

```bash
# Get the string
CONNECTION_STRING=$(neonctl connection-string --project-id <project-id> --pooled)

# Use in any Postgres client
psql "$CONNECTION_STRING" -c "SELECT * FROM users LIMIT 5;"
```

## 避免重复输入项目 ID

为了简化操作，可以设置一个上下文变量来避免每次都手动输入 `--project-id`：

```bash
# Set project context
neonctl set-context --project-id <project-id>

# Now commands use that project automatically
neonctl branches list
neonctl databases list
neonctl connection-string
```

## 代理系统工作流程示例

### 创建带有分支结构的组织数据库

```bash
# Create project for org
neonctl projects create --name "website-org-db" -o json

# Create production branch (main is created by default)
# Create dev branch for testing
neonctl branches create --name "dev" --project-id <id>

# Get connection strings
neonctl connection-string main --project-id <id> --pooled  # for prod
neonctl connection-string dev --project-id <id> --pooled   # for dev
```

### 创建客户信息表

```bash
# Connect and create schema
psql "$(neonctl cs --project-id <id>)" <<EOF
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    business_name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    location VARCHAR(255),
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    status VARCHAR(50) DEFAULT 'identified',
    priority VARCHAR(20) DEFAULT 'medium',
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_category ON leads(category);
EOF
```

### 为实验创建临时分支

```bash
# Create a branch to test schema changes
neonctl branches create --name "schema-experiment" --project-id <id>

# Test your changes on the branch
psql "$(neonctl cs schema-experiment --project-id <id>)" -c "ALTER TABLE leads ADD COLUMN score INT;"

# If it works, apply to main. If not, just delete the branch
neonctl branches delete schema-experiment --project-id <id>
```

## 输出格式

```bash
# JSON (for parsing)
neonctl projects list -o json

# YAML
neonctl projects list -o yaml

# Table (default, human-readable)
neonctl projects list -o table
```

## 环境变量

```bash
# API key (required if not using `neonctl auth`)
export NEON_API_KEY=your_key

# Default project (alternative to set-context)
export NEON_PROJECT_ID=your_project_id
```

## 常用操作模式

### 检查 neonctl 是否已正确配置

```bash
neonctl me -o json 2>/dev/null && echo "Authenticated" || echo "Need to run: neonctl auth"
```

### 快速查询数据库

```bash
# One-liner query
psql "$(neonctl cs)" -c "SELECT COUNT(*) FROM leads WHERE status='contacted';"
```

### 将数据导出为 CSV 格式

```bash
psql "$(neonctl cs)" -c "COPY (SELECT * FROM leads) TO STDOUT WITH CSV HEADER" > leads.csv
```

### 从 CSV 文件导入数据

```bash
psql "$(neonctl cs)" -c "\COPY leads(business_name,category,location) FROM 'import.csv' WITH CSV HEADER"
```

## 故障排除

### 错误提示 “Connection refused”：
  - 检查分支的计算资源是否处于激活状态（零成本扩展模式可能导致计算资源被暂停）。
  - 对于无服务器工作负载，建议使用带有 `--pooled` 参数的连接字符串。

### 错误提示 “Permission denied”：
  - 确认 API 密钥是否正确：`neonctl me`。
  - 重新进行身份验证：`neonctl auth`。

### 首次连接速度较慢：
  - 这是零成本扩展模式下的正常现象，首次连接可能需要 1-2 秒的时间来启动计算资源。
  - 使用连接池可以保持连接的活跃状态，提高访问效率。

## 相关资源

- [Neon 控制台](https://console.neon.tech)：Web 管理界面。
- [API 文档](https://api-docs.neon.tech)：REST API 参考。
- [CLI 文档](https://neon.tech/docs/reference/neon-cli)：完整的 CLI 使用指南。
- [GitHub 仓库](https://github.com/neondatabase/neonctl)：CLI 源代码。