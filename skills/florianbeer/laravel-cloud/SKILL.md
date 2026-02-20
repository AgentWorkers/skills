---
name: laravel-cloud
description: 通过 API 管理 Laravel Cloud 基础设施——包括应用程序、环境、部署、数据库、缓存、域名、扩展能力、命令、存储以及 WebSockets。
metadata:
  openclaw:
    requires:
      bins: [curl, jq]
      env: [LARAVEL_CLOUD_API_TOKEN]
    credentials:
      primary:
        env: LARAVEL_CLOUD_API_TOKEN
        file: ~/.openclaw/credentials/laravel-cloud/config.json
        description: Laravel Cloud API token (generate at cloud.laravel.com → Settings → API Tokens)
    scripts:
      laravel-cloud:
        path: scripts/laravel-cloud
        description: Laravel Cloud CLI wrapper
---
# Laravel Cloud API 工具

该工具将整个 [Laravel Cloud REST API](https://cloud.laravel.com/docs) 封装在一个 Bash 脚本中，方便用户统一管理和使用。

## 设置

**选项 1 — 使用环境变量（推荐）：**
```bash
export LARAVEL_CLOUD_API_TOKEN="your-token-here"
```

**选项 2 — 使用凭据文件：**
```bash
mkdir -p ~/.openclaw/credentials/laravel-cloud
echo '{"token":"your-token-here"}' > ~/.openclaw/credentials/laravel-cloud/config.json
```

请在以下地址生成您的 API 令牌：**cloud.laravel.com → 设置 → API 令牌**

## 使用方法

```bash
laravel-cloud <resource> <action> [args...]
```

## 快速参考

| 资源 | 操作 |
|---|---|
| `apps` | 列出、获取、创建、更新、删除 |
| `envs` | 列出、获取、创建、更新、删除、启动、停止、查看指标、日志、添加变量、替换变量 |
| `commands` | 列出、获取、运行命令 |
| `deployments` | 列出、获取、启动部署 |
| `domains` | 列出、获取、创建、更新、删除、验证域名 |
| `instances` | 列出、获取实例信息、调整实例大小、创建、更新、删除 |
| `bg-processes` | 列出、获取、创建、更新、删除后台进程 |
| `databases` | 管理数据库集群（包括创建、更新、删除集群、查看集群指标等） |
| `caches` | 管理缓存（包括列出、获取、创建、更新、删除缓存等） |
| `buckets` | 管理存储桶（包括列出、获取、创建、删除存储桶等） |
| `bucket-keys` | 管理存储桶键（包括列出、获取、创建、删除存储桶键等） |
| `websockets` | 管理 WebSocket 服务（包括列出、获取、创建、更新、删除 WebSocket 服务等） |
| `ws-apps` | 管理 WebSocket 应用程序（包括列出、获取、创建、更新、删除 WebSocket 应用程序等） |
| `ips` | 列出 IP 地址 |
| `org` | 获取组织信息 |
| `regions` | 列出可用区域 |

## 常见使用示例

```bash
# List all applications
laravel-cloud apps list

# Create an application
laravel-cloud apps create --name "my-app" --region us-east-1

# List environments for an app
laravel-cloud envs list <app-id>

# Create an environment
laravel-cloud envs create <app-id> --name "Production" --branch main

# Start / stop an environment
laravel-cloud envs start <env-id>
laravel-cloud envs stop <env-id>

# View environment metrics and logs
laravel-cloud envs metrics <env-id> --period 24h
laravel-cloud envs logs <env-id>

# Set environment variables
laravel-cloud envs vars-add <env-id> --vars 'APP_KEY=base64:...,DB_HOST=localhost'
laravel-cloud envs vars-replace <env-id> --vars 'KEY1=val1,KEY2=val2'

# Trigger a deployment
laravel-cloud deployments initiate <env-id>

# Run an Artisan command
laravel-cloud commands run <env-id> --command "php artisan migrate --force"

# Get organization and regions
laravel-cloud org get
laravel-cloud regions list

# Manage databases
laravel-cloud databases clusters
laravel-cloud databases cluster-create --name my-db --type neon-serverless-postgres --region us-east-1

# Manage caches
laravel-cloud caches list
laravel-cloud caches create --name my-cache --type valkey --region us-east-1 --size cache.t3.micro

# Object storage
laravel-cloud buckets list
laravel-cloud buckets create --name my-bucket --region us-east-1

# WebSocket clusters
laravel-cloud websockets list
laravel-cloud ws-apps list <ws-cluster-id>

# Per-resource help
laravel-cloud help
laravel-cloud envs help
laravel-cloud databases help
```

## 所需依赖库

- `curl`：用于发送 HTTP 请求
- `jq`：用于解析和美化 JSON 数据