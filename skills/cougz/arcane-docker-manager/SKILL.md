# OpenClaw - 高级Docker管理技能

## 概述
此技能允许您通过Arcane Docker Management API来管理Docker容器、Docker Compose堆栈、模板、网络、卷、镜像以及系统监控。Arcane是一个提供REST API的全面Docker管理平台。

## 何时使用此技能
当用户需要执行以下操作时，请使用此技能：
- 管理Docker容器（列出、启动、停止、重启、删除、检查）
- 管理Docker Compose堆栈（部署、更新、删除、查看日志）
- 使用Docker模板（创建、部署、管理）
- 管理Docker镜像（列出、拉取、删除、清理）
- 管理Docker网络和卷
- 监控系统资源和Docker统计信息
- 管理用户账户和API密钥
- 查看系统日志和事件

## API配置

### 基本URL
API的基本URL需要由用户自行配置。默认值：`http://localhost:3552/api`

### 认证
Arcane支持两种认证方式：
1. **Bearer Token (JWT)**：通过登录端点获取
2. **API Key**：使用`X-API-Key`头部进行长期认证

#### 获取Bearer Token
```bash
curl -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your_password"
  }'
```

响应中包含`token`、`refreshToken`和`expiresAt`。

#### 使用API Keys
API密钥可以通过 `/apikeys` 端点进行创建和管理。使用`X-API-Key`头部进行认证。

## 核心功能

### 1. 容器管理

#### 列出容器
```bash
# Get all containers
curl -X GET "$BASE_URL/containers" \
  -H "Authorization: Bearer $TOKEN"

# Filter by status
curl -X GET "$BASE_URL/containers?status=running" \
  -H "Authorization: Bearer $TOKEN"

# Search containers
curl -X GET "$BASE_URL/containers?search=nginx" \
  -H "Authorization: Bearer $TOKEN"
```

#### 容器操作
```bash
# Start container
curl -X POST "$BASE_URL/containers/{id}/start" \
  -H "Authorization: Bearer $TOKEN"

# Stop container
curl -X POST "$BASE_URL/containers/{id}/stop" \
  -H "Authorization: Bearer $TOKEN"

# Restart container
curl -X POST "$BASE_URL/containers/{id}/restart" \
  -H "Authorization: Bearer $TOKEN"

# Remove container
curl -X DELETE "$BASE_URL/containers/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Get container details
curl -X GET "$BASE_URL/containers/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Get container logs
curl -X GET "$BASE_URL/containers/{id}/logs?tail=100" \
  -H "Authorization: Bearer $TOKEN"

# Get container stats
curl -X GET "$BASE_URL/containers/{id}/stats" \
  -H "Authorization: Bearer $TOKEN"
```

#### 高级容器操作
```bash
# Execute command in container
curl -X POST "$BASE_URL/containers/{id}/exec" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "command": ["ls", "-la"],
    "workingDir": "/app"
  }'

# Rename container
curl -X POST "$BASE_URL/containers/{id}/rename" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "new-container-name"
  }'

# Update container resources
curl -X POST "$BASE_URL/containers/{id}/update" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cpuShares": 512,
    "memory": 536870912,
    "restartPolicy": "unless-stopped"
  }'
```

### 2. Docker Compose堆栈管理

#### 列出堆栈
```bash
curl -X GET "$BASE_URL/stacks" \
  -H "Authorization: Bearer $TOKEN"
```

#### 从模板部署堆栈
```bash
curl -X POST "$BASE_URL/stacks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-stack",
    "templateId": "template-id",
    "envVars": {
      "PORT": "8080",
      "DATABASE_URL": "postgres://..."
    }
  }'
```

#### 从Compose文件部署堆栈
```bash
curl -X POST "$BASE_URL/stacks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-stack",
    "composeContent": "version: \"3.8\"\nservices:\n  web:\n    image: nginx:latest\n    ports:\n      - \"80:80\""
  }'
```

#### 堆栈操作
```bash
# Get stack details
curl -X GET "$BASE_URL/stacks/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Update stack
curl -X PUT "$BASE_URL/stacks/{id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "envVars": {
      "PORT": "9090"
    }
  }'

# Remove stack
curl -X DELETE "$BASE_URL/stacks/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Start stack
curl -X POST "$BASE_URL/stacks/{id}/start" \
  -H "Authorization: Bearer $TOKEN"

# Stop stack
curl -X POST "$BASE_URL/stacks/{id}/stop" \
  -H "Authorization: Bearer $TOKEN"

# Restart stack
curl -X POST "$BASE_URL/stacks/{id}/restart" \
  -H "Authorization: Bearer $TOKEN"

# Get stack logs
curl -X GET "$BASE_URL/stacks/{id}/logs?tail=100" \
  -H "Authorization: Bearer $TOKEN"

# Pull latest images for stack
curl -X POST "$BASE_URL/stacks/{id}/pull" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. 模板管理

#### 列出模板
```bash
curl -X GET "$BASE_URL/templates" \
  -H "Authorization: Bearer $TOKEN"
```

#### 创建模板
```bash
curl -X POST "$BASE_URL/templates" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "nginx-template",
    "description": "Basic nginx web server",
    "content": "version: \"3.8\"\nservices:\n  web:\n    image: nginx:{{VERSION}}\n    ports:\n      - \"{{PORT}}:80\"",
    "variables": [
      {
        "name": "VERSION",
        "description": "Nginx version",
        "defaultValue": "latest"
      },
      {
        "name": "PORT",
        "description": "Host port",
        "defaultValue": "80"
      }
    ],
    "category": "web-servers",
    "tags": ["nginx", "web"]
  }'
```

#### 模板操作
```bash
# Get template
curl -X GET "$BASE_URL/templates/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Update template
curl -X PUT "$BASE_URL/templates/{id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "updated-template-name",
    "description": "Updated description"
  }'

# Delete template
curl -X DELETE "$BASE_URL/templates/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Get template content with parsed variables
curl -X GET "$BASE_URL/templates/{id}/content" \
  -H "Authorization: Bearer $TOKEN"
```

#### 全局模板变量
```bash
# Get global variables
curl -X GET "$BASE_URL/templates/global-variables" \
  -H "Authorization: Bearer $TOKEN"

# Update global variables
curl -X PUT "$BASE_URL/templates/global-variables" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "GLOBAL_DOMAIN": "example.com",
    "GLOBAL_NETWORK": "traefik-public"
  }'
```

### 4. 镜像管理

#### 列出镜像
```bash
curl -X GET "$BASE_URL/images" \
  -H "Authorization: Bearer $TOKEN"
```

#### 拉取镜像
```bash
curl -X POST "$BASE_URL/images/pull" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "image": "nginx:latest"
  }'
```

#### 镜像操作
```bash
# Get image details
curl -X GET "$BASE_URL/images/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Remove image
curl -X DELETE "$BASE_URL/images/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Prune unused images
curl -X POST "$BASE_URL/images/prune" \
  -H "Authorization: Bearer $TOKEN"

# Search images in registry
curl -X GET "$BASE_URL/images/search?term=nginx" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. 网络管理

#### 列出网络
```bash
curl -X GET "$BASE_URL/networks" \
  -H "Authorization: Bearer $TOKEN"
```

#### 创建网络
```bash
curl -X POST "$BASE_URL/networks" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-network",
    "driver": "bridge",
    "internal": false,
    "attachable": true
  }'
```

#### 网络操作
```bash
# Get network details
curl -X GET "$BASE_URL/networks/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Remove network
curl -X DELETE "$BASE_URL/networks/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Connect container to network
curl -X POST "$BASE_URL/networks/{id}/connect" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "containerId": "container-id"
  }'

# Disconnect container from network
curl -X POST "$BASE_URL/networks/{id}/disconnect" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "containerId": "container-id"
  }'

# Prune unused networks
curl -X POST "$BASE_URL/networks/prune" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. 卷管理

#### 列出卷
```bash
curl -X GET "$BASE_URL/volumes" \
  -H "Authorization: Bearer $TOKEN"
```

#### 创建卷
```bash
curl -X POST "$BASE_URL/volumes" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-volume",
    "driver": "local",
    "labels": {
      "project": "my-app"
    }
  }'
```

#### 卷操作
```bash
# Get volume details
curl -X GET "$BASE_URL/volumes/{name}" \
  -H "Authorization: Bearer $TOKEN"

# Remove volume
curl -X DELETE "$BASE_URL/volumes/{name}" \
  -H "Authorization: Bearer $TOKEN"

# Prune unused volumes
curl -X POST "$BASE_URL/volumes/prune" \
  -H "Authorization: Bearer $TOKEN"
```

### 7. 系统监控

#### 系统信息
```bash
# Get Docker system info
curl -X GET "$BASE_URL/system/info" \
  -H "Authorization: Bearer $TOKEN"

# Get Docker version
curl -X GET "$BASE_URL/system/version" \
  -H "Authorization: Bearer $TOKEN"

# Get system stats
curl -X GET "$BASE_URL/system/stats" \
  -H "Authorization: Bearer $TOKEN"

# Get disk usage
curl -X GET "$BASE_URL/system/df" \
  -H "Authorization: Bearer $TOKEN"
```

#### 事件和日志
```bash
# Get system events (streaming)
curl -X GET "$BASE_URL/system/events" \
  -H "Authorization: Bearer $TOKEN"

# Get events with filters
curl -X GET "$BASE_URL/system/events?since=1609459200&type=container" \
  -H "Authorization: Bearer $TOKEN"
```

### 8. 用户管理

#### 列出用户
```bash
curl -X GET "$BASE_URL/users" \
  -H "Authorization: Bearer $TOKEN"
```

#### 创建用户
```bash
curl -X POST "$BASE_URL/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepassword123",
    "role": "user"
  }'
```

#### 用户操作
```bash
# Get user details
curl -X GET "$BASE_URL/users/{userId}" \
  -H "Authorization: Bearer $TOKEN"

# Update user
curl -X PUT "$BASE_URL/users/{userId}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "role": "admin"
  }'

# Delete user
curl -X DELETE "$BASE_URL/users/{userId}" \
  -H "Authorization: Bearer $TOKEN"

# Change password
curl -X PUT "$BASE_URL/auth/password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "currentPassword": "oldpassword",
    "newPassword": "newpassword123"
  }'
```

### 9. API密钥管理

#### 列出API密钥
```bash
curl -X GET "$BASE_URL/apikeys" \
  -H "Authorization: Bearer $TOKEN"
```

#### 创建API密钥
```bash
curl -X POST "$BASE_URL/apikeys" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CI/CD Pipeline Key",
    "description": "API key for automated deployments",
    "expiresAt": "2025-12-31T23:59:59Z"
  }'
```

#### API密钥操作
```bash
# Get API key details
curl -X GET "$BASE_URL/apikeys/{id}" \
  -H "Authorization: Bearer $TOKEN"

# Update API key
curl -X PUT "$BASE_URL/apikeys/{id}" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Key Name",
    "description": "Updated description"
  }'

# Delete API key
curl -X DELETE "$BASE_URL/apikeys/{id}" \
  -H "Authorization: Bearer $TOKEN"
```

## 实现指南

### 错误处理
所有API响应都遵循标准格式：
```json
{
  "success": true|false,
  "data": {...},
  "message": "Success or error message"
}
```

错误响应使用HTTP错误详细信息（RFC 7807）：
```json
{
  "type": "about:blank",
  "title": "Error title",
  "status": 400,
  "detail": "Detailed error message"
}
```

### 分页
列表端点支持以下查询参数进行分页：
- `start`：起始索引（默认值：0）
- `limit`：每页显示的项数（默认值：20）
- `sort`：排序列
- `order`：排序方向（升序/降序，默认值：升序）
- `search`：搜索查询

响应中包含分页元数据：
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "start": 0,
    "limit": 20,
    "total": 100,
    "hasMore": true
  }
}
```

### 使用Python
在Python中实现Arcane操作时，请使用`requests`库：

```python
import requests

BASE_URL = "http://localhost:3552/api"
TOKEN = "your-jwt-token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# List containers
response = requests.get(f"{BASE_URL}/containers", headers=headers)
containers = response.json()

# Deploy stack
stack_data = {
    "name": "my-stack",
    "templateId": "template-id",
    "envVars": {
        "PORT": "8080"
    }
}
response = requests.post(f"{BASE_URL}/stacks", headers=headers, json=stack_data)
result = response.json()
```

### 使用Bash
对于简单操作，可以使用带有错误处理的`curl`命令：

```bash
#!/bin/bash

BASE_URL="http://localhost:3552/api"
TOKEN="your-jwt-token"

# Function to make authenticated requests
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    if [ -z "$data" ]; then
        curl -s -X "$method" "$BASE_URL/$endpoint" \
            -H "Authorization: Bearer $TOKEN"
    else
        curl -s -X "$method" "$BASE_URL/$endpoint" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data"
    fi
}

# Example: List containers
containers=$(api_call GET "containers")
echo "$containers" | jq '.data[] | {id, name, status}'
```

## 常见工作流程

### 1. 部署应用程序堆栈
```python
# 1. Create or select template
template_data = {
    "name": "webapp-template",
    "content": "version: '3.8'\nservices:\n  web:\n    image: myapp:{{VERSION}}\n    ports:\n      - '{{PORT}}:8080'",
    "variables": [
        {"name": "VERSION", "defaultValue": "latest"},
        {"name": "PORT", "defaultValue": "80"}
    ]
}
template = requests.post(f"{BASE_URL}/templates", headers=headers, json=template_data).json()

# 2. Deploy stack from template
stack_data = {
    "name": "production-webapp",
    "templateId": template["data"]["id"],
    "envVars": {
        "VERSION": "v1.2.3",
        "PORT": "8080"
    }
}
stack = requests.post(f"{BASE_URL}/stacks", headers=headers, json=stack_data).json()

# 3. Monitor deployment
stack_id = stack["data"]["id"]
logs = requests.get(f"{BASE_URL}/stacks/{stack_id}/logs?tail=50", headers=headers).json()
```

### 2. 扩展和监控容器
```python
# Get running containers
containers = requests.get(f"{BASE_URL}/containers?status=running", headers=headers).json()

# Get stats for each container
for container in containers["data"]:
    stats = requests.get(f"{BASE_URL}/containers/{container['id']}/stats", headers=headers).json()
    print(f"{container['name']}: CPU {stats['data']['cpuPercent']:.2f}%, Memory {stats['data']['memoryPercent']:.2f}%")

# Update container resources if needed
update_data = {
    "cpuShares": 1024,
    "memory": 1073741824  # 1GB
}
requests.post(f"{BASE_URL}/containers/{container_id}/update", headers=headers, json=update_data)
```

### 3. 清理和维护
```python
# Prune unused resources
requests.post(f"{BASE_URL}/images/prune", headers=headers)
requests.post(f"{BASE_URL}/volumes/prune", headers=headers)
requests.post(f"{BASE_URL}/networks/prune", headers=headers)

# Get disk usage before and after
df_before = requests.get(f"{BASE_URL}/system/df", headers=headers).json()
# ... perform cleanup ...
df_after = requests.get(f"{BASE_URL}/system/df", headers=headers).json()
```

## 最佳实践

1. **认证**：对于自动化脚本和服务，始终使用API密钥；对于交互式会话，使用JWT令牌。
2. **错误处理**：检查响应状态码并适当处理错误：
   - 200：成功
   - 400：请求错误（验证错误）
   - 401：未经授权
   - 403：禁止访问
   - 404：未找到
   - 500：内部服务器错误
3. **资源管理**：
   - 创建容器时始终指定资源限制
   - 使用标签来组织资源
   - 定期清理未使用的资源
4. **安全性**：
   - 安全存储API密钥和令牌（使用环境变量）
   - 在生产环境中使用HTTPS
   - 实施基于用户角色的适当访问控制
   - 定期轮换API密钥
5. **监控**：
   - 定期监控容器统计信息
   - 设置资源使用情况的警报
   - 定期查看系统日志
6. **模板**：
   - 使用变量来表示可配置的值
   - 清晰记录模板变量
   - 对模板进行版本控制
   - 使用全局变量进行共享配置

## 故障排除

### 常见问题

**认证失败**
- 确认令牌未过期（检查`expiresAt`）
- 使用刷新令牌获取新的访问令牌
- 确认API密钥正确且未过期

**容器无法启动**
- 查看容器日志：`GET /containers/{id}/logs`
- 检查容器：`GET /containers/{id}`
- 确认端口冲突和资源可用性

**堆栈部署失败**
- 验证Compose文件的语法
- 检查模板变量是否定义正确
- 查看堆栈日志：`GET /stacks/{id}/logs`

**资源未找到**
- 确认资源ID正确
- 检查资源是否已被删除
- 确保具有适当的权限

## 注意事项

- 所有时间戳均采用ISO 8601格式（UTC）
- 容器ID可以是完整的或简短的（前12个字符）
- 镜像名称支持完整的注册表路径（例如：registry.example.com/image:tag）
- 网络和卷名称必须唯一
- 堆栈名称对于每个用户/项目来说必须是唯一的

## 参考链接
有关完整的API文档和模式定义，请参阅提供的JSON模式中的OpenAPI规范。