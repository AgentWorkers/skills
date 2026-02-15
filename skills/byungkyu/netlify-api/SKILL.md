---
name: netlify
description: |
  Netlify API integration with managed OAuth. Deploy sites, manage builds, configure DNS, and handle environment variables.
  Use this skill when users want to manage Netlify sites, deployments, build settings, or DNS configurations.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: https://maton.ai
    requires:
      env:
        - MATON_API_KEY
---

# Netlify

您可以使用受管理的 OAuth 认证来访问 Netlify API。该 API 允许您管理网站、进行部署、构建项目、配置 DNS 区域、设置环境变量以及设置 Webhook。

## 快速入门

```bash
# List all sites
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/netlify/api/v1/sites')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/netlify/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Netlify API 端点路径。网关会将请求代理到 `api.netlify.com`，并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Netlify OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=netlify&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'netlify'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "9e674cd3-2280-4eb4-9ff7-b12ec8ca3f55",
    "status": "ACTIVE",
    "creation_time": "2026-02-12T11:15:33.183756Z",
    "last_updated_time": "2026-02-12T11:15:51.556556Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "netlify",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Netlify 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/netlify/api/v1/sites')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '9e674cd3-2280-4eb4-9ff7-b12ec8ca3f55')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户与账户

#### 获取当前用户

```bash
GET /netlify/api/v1/user
```

#### 列出账户

```bash
GET /netlify/api/v1/accounts
```

#### 获取账户信息

```bash
GET /netlify/api/v1/accounts/{account_id}
```

### 网站

#### 列出网站

```bash
GET /netlify/api/v1/sites
```

支持过滤：

```bash
GET /netlify/api/v1/sites?filter=all&page=1&per_page=100
```

#### 获取网站信息

```bash
GET /netlify/api/v1/sites/{site_id}
```

#### 创建网站

```bash
POST /netlify/api/v1/{account_slug}/sites
Content-Type: application/json

{
  "name": "my-new-site"
}
```

#### 更新网站信息

```bash
PUT /netlify/api/v1/sites/{site_id}
Content-Type: application/json

{
  "name": "updated-site-name"
}
```

#### 删除网站

```bash
DELETE /netlify/api/v1/sites/{site_id}
```

### 部署

#### 列出部署信息

```bash
GET /netlify/api/v1/sites/{site_id}/deploys
```

#### 获取部署详情

```bash
GET /netlify/api/v1/deploys/{deploy_id}
```

#### 创建部署任务

```bash
POST /netlify/api/v1/sites/{site_id}/deploys
Content-Type: application/json

{
  "title": "Deploy from API"
}
```

#### 锁定部署任务

```bash
POST /netlify/api/v1/deploys/{deploy_id}/lock
```

#### 解锁部署任务

```bash
POST /netlify/api/v1/deploys/{deploy_id}/unlock
```

#### 恢复部署（回滚）

```bash
PUT /netlify/api/v1/deploys/{deploy_id}
```

### 构建项目

#### 列出构建记录

```bash
GET /netlify/api/v1/sites/{site_id}/builds
```

#### 获取构建详情

```bash
GET /netlify/api/v1/builds/{build_id}
```

#### 触发构建任务

```bash
POST /netlify/api/v1/sites/{site_id}/builds
```

### 环境变量

环境变量在账户级别进行管理，支持可选的站点范围。

#### 列出环境变量

```bash
GET /netlify/api/v1/accounts/{account_id}/env?site_id={site_id}
```

#### 创建环境变量

```bash
POST /netlify/api/v1/accounts/{account_id}/env?site_id={site_id}
Content-Type: application/json

[
  {
    "key": "MY_VAR",
    "values": [
      {"value": "my_value", "context": "all"}
    ]
  }
]
```

**环境变量范围：** `all`, `production`, `deploy-preview`, `branch-deploy`, `dev`

#### 更新环境变量

```bash
PUT /netlify/api/v1/accounts/{account_id}/env/{key}?site_id={site_id}
Content-Type: application/json

{
  "key": "MY_VAR",
  "values": [
    {"value": "updated_value", "context": "all"}
  ]
}
```

#### 删除环境变量

```bash
DELETE /netlify/api/v1/accounts/{account_id}/env/{key}?site_id={site_id}
```

### DNS 区域

#### 列出 DNS 区域

```bash
GET /netlify/api/v1/dns_zones
```

#### 创建 DNS 区域

```bash
POST /netlify/api/v1/dns_zones
Content-Type: application/json

{
  "name": "example.com",
  "account_slug": "my-account"
}
```

#### 获取 DNS 区域信息

```bash
GET /netlify/api/v1/dns_zones/{zone_id}
```

#### 删除 DNS 区域

```bash
DELETE /netlify/api/v1/dns_zones/{zone_id}
```

### DNS 记录

#### 列出 DNS 记录

```bash
GET /netlify/api/v1/dns_zones/{zone_id}/dns_records
```

#### 创建 DNS 记录

```bash
POST /netlify/api/v1/dns_zones/{zone_id}/dns_records
Content-Type: application/json

{
  "type": "A",
  "hostname": "www",
  "value": "192.0.2.1",
  "ttl": 3600
}
```

#### 删除 DNS 记录

```bash
DELETE /netlify/api/v1/dns_zones/{zone_id}/dns_records/{record_id}
```

### 构建触发器

#### 列出构建触发器

```bash
GET /netlify/api/v1/sites/{site_id}/build_hooks
```

#### 创建构建触发器

```bash
POST /netlify/api/v1/sites/{site_id}/build_hooks
Content-Type: application/json

{
  "title": "My Build Hook",
  "branch": "main"
}
```

响应中包含一个 URL，您可以通过 POST 请求来触发构建任务。

#### 删除构建触发器

```bash
DELETE /netlify/api/v1/hooks/{hook_id}
```

### Webhook

#### 列出 Webhook

```bash
GET /netlify/api/v1/hooks?site_id={site_id}
```

#### 创建 Webhook

```bash
POST /netlify/api/v1/hooks?site_id={site_id}
Content-Type: application/json

{
  "type": "url",
  "event": "deploy_created",
  "data": {
    "url": "https://example.com/webhook"
  }
}
```

**事件：** `deploy_created`, `deploy_building`, `deploy_failed`, `deploy_succeeded`, `formsubmission`

#### 删除 Webhook

```bash
DELETE /netlify/api/v1/hooks/{hook_id}
```

### 表单

#### 列出表单

```bash
GET /netlify/api/v1/sites/{site_id}/forms
```

#### 列出表单提交记录

```bash
GET /netlify/api/v1/sites/{site_id}/submissions
```

#### 删除表单

```bash
DELETE /netlify/api/v1/sites/{site_id}/forms/{form_id}
```

### 函数

#### 列出可用的函数

```bash
GET /netlify/api/v1/sites/{site_id}/functions
```

### 服务/插件

#### 列出可用的服务

```bash
GET /netlify/api/v1/services
```

#### 获取服务详情

```bash
GET /netlify/api/v1/services/{service_id}
```

## 分页

使用 `page` 和 `per_page` 查询参数进行分页：

```bash
GET /netlify/api/v1/sites?page=1&per_page=100
```

默认的 `per_page` 值因 API 端点而异。请查看响应头中的分页信息。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/netlify/api/v1/sites',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const sites = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/netlify/api/v1/sites',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
sites = response.json()
```

### 创建网站并设置环境变量

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# Create site
site = requests.post(
    'https://gateway.maton.ai/netlify/api/v1/my-account/sites',
    headers=headers,
    json={'name': 'my-new-site'}
).json()

# Add environment variable
requests.post(
    f'https://gateway.maton.ai/netlify/api/v1/accounts/{site["account_id"]}/env',
    headers=headers,
    params={'site_id': site['id']},
    json=[{'key': 'API_KEY', 'values': [{'value': 'secret', 'context': 'all'}]}]
)
```

## 注意事项

- 网站 ID 是 UUID（例如：`d37d1ce4-5444-40f5-a4ca-a2c40a8b6835`）。
- 账户别名用于在团队内创建网站（例如：`my-team-slug`）。
- 创建部署任务时会返回部署 ID，可用于跟踪部署状态。
- 构建触发器返回的 URL 可以通过 POST 请求来触发外部构建任务。
- 环境变量的作用范围可以通过 `all`, `production`, `deploy-preview`, `branch-deploy`, `dev` 来控制。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 命令可以避免全局解析问题。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立 Netlify 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Netlify API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的 URL 路径以 `netlify` 开头。例如：
  - 正确的路径：`https://gateway.maton.ai/netlify/api/v1/sites`
  - 错误的路径：`https://gateway.maton.ai/api/v1/sites`

## 资源

- [Netlify API 文档](https://open-api.netlify.com/)
- [Netlify CLI](https://docs.netlify.com/cli/get-started/)
- [Netlify 构建触发器](https://docs.netlify.com/configure-builds/build-hooks/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 技术支持](mailto:support@maton.ai)