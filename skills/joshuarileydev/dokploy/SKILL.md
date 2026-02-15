---
name: dokploy
description: "通过 Dokploy API 管理 Dokploy 的部署、项目、应用程序和域名。"
emoji: "🐳"
metadata:
  clawdhub:
    requires:
      bins: ["curl", "jq"]
---

# Dokploy 技能

通过与 Dokploy 的 API 交互，可以管理项目、应用程序、域名和部署任务。

## 先决条件

1. 运行中的 Dokploy 实例，并且已启用 API 访问功能。
2. 从 `/settings/profile` 的 “API/CLI” 部分生成 API 密钥。
3. 设置 `DOKPLOY_API_URL` 环境变量（默认值：`http://localhost:3000`）。

## 配置

请设置以下环境变量，或使用 `config` 命令进行配置：

```bash
# Dokploy instance URL
export DOKPLOY_API_URL="https://your-dokploy-instance.com"

# Your API token
export DOKPLOY_API_KEY="your-generated-api-key"

# Or run the config command
dokploy-config set --url "https://your-dokploy-instance.com" --key "your-api-key"
```

## 项目

### 列出所有项目
```bash
dokploy-project list
```

### 获取项目详情
```bash
dokploy-project get <project-id>
```

### 创建新项目
```bash
dokploy-project create --name "My Project" --description "Description here"
```

### 更新项目
```bash
dokploy-project update <project-id> --name "New Name" --description "Updated"
```

### 删除项目
```bash
dokploy-project delete <project-id>
```

## 应用程序

### 列出项目中的应用程序
```bash
dokploy-app list --project <project-id>
```

### 获取应用程序详情
```bash
dokploy-app get <application-id>
```

### 创建应用程序
```bash
dokploy-app create \
  --project <project-id> \
  --name "my-app" \
  --type "docker" \
  --image "nginx:latest"
```

**应用程序类型：** `docker`, `git`, `compose`

### 触发部署
```bash
dokploy-app deploy <application-id>
```

### 获取部署日志
```bash
dokploy-app logs <application-id> --deployment <deployment-id>
```

### 列出部署任务
```bash
dokploy-app deployments <application-id>
```

### 更新应用程序
```bash
dokploy-app update <application-id> --name "new-name" --env "KEY=VALUE"
```

### 删除应用程序
```bash
dokploy-app delete <application-id>
```

## 域名

### 列出应用程序所属的域名
```bash
dokploy-domain list --application <application-id>
```

### 获取域名详情
```bash
dokploy-domain get <domain-id>
```

### 将域名添加到应用程序
```bash
dokploy-domain create \
  --application <application-id> \
  --domain "app.example.com" \
  --path "/" \
  --port 80
```

### 更新域名
```bash
dokploy-domain update <domain-id> --domain "new.example.com"
```

### 删除域名
```bash
dokploy-domain delete <domain-id>
```

## 环境变量

### 列出应用程序的环境变量
```bash
dokploy-app env list <application-id>
```

### 设置环境变量
```bash
dokploy-app env set <application-id> --key "DATABASE_URL" --value "postgres://..."
```

### 删除环境变量
```bash
dokploy-app env delete <application-id> --key "DATABASE_URL"
```

## 实用命令

### 检查 API 连接
```bash
dokploy-status
```

### 查看当前配置
```bash
dokploy-config show
```

## API 参考

基础 URL：`$DOKPLOY_API_URL/api`

| 端点          | 方法        | 描述                                      |
|----------------|------------|-----------------------------------------|
| `/project.all`     | GET         | 列出所有项目                               |
| `/project.create`    | POST         | 创建新项目                               |
| `/projectById`    | GET         | 根据 ID 获取项目                         |
| `/project.update`    | PATCH        | 更新项目                               |
| `/project.delete`    | DELETE       | 删除项目                               |
| `/application.all`    | GET         | 列出所有应用程序                         |
| `/application.create`    | POST         | 创建新应用程序                         |
| `/applicationById`    | GET         | 根据 ID 获取应用程序                         |
| `/application.update`    | PATCH        | 更新应用程序                         |
| `/application.delete`    | DELETE       | 删除应用程序                         |
| `/application.deploy`    | POST         | 触发应用程序部署                         |
| `/deployment.all`    | GET         | 列出所有部署任务                         |
| `/deploymentById`    | GET         | 根据 ID 获取部署任务                         |
| `/deployment.logs`    | GET         | 获取部署任务日志                         |
| `/domain.all`     | GET         | 列出所有域名                             |
| `/domain.create`    | POST         | 创建新域名                             |
| `/domain.update`    | PATCH        | 更新域名                             |
| `/domain.delete`    | DELETE       | 删除域名                             |

## 注意事项

- 所有 API 调用都需要在请求头中添加 `x-api-key`。
- 在脚本中可以使用 `jq` 来解析 JSON 数据。
- 某些操作需要管理员权限。
- 部署是异步进行的——请使用相应的端点来查看部署进度。