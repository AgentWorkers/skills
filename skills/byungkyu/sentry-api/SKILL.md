---
name: sentry
description: >
  **Sentry API集成与受管理的认证系统**  
  通过该功能，您可以监控应用程序中的错误、问题以及性能表现。当用户需要列出问题、检索事件、管理项目、团队或发布版本时，可充分利用这一功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Sentry

您可以使用托管的认证方式访问Sentry API，以监控错误、管理问题、项目、团队和发布版本。

## 快速入门

```bash
# List issues for a project
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/sentry/api/0/projects/{organization_slug}/{project_slug}/issues/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/sentry/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Sentry API端点路径。该网关会将请求代理到 `{subdomain}.sentry.io` 并自动插入您的凭据。

## 认证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的Sentry OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=sentry&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'sentry'}).encode()
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
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "sentry",
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

如果您有多个Sentry连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/sentry/api/0/organizations/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用默认的（最旧的）活动连接。

## API参考

### 组织操作

#### 列出组织

```bash
GET /sentry/api/0/organizations/
```

#### 获取组织信息

```bash
GET /sentry/api/0/organizations/{organization_slug}/
```

#### 更新组织信息

```bash
PUT /sentry/api/0/organizations/{organization_slug}/
Content-Type: application/json

{
  "name": "Updated Organization Name"
}
```

#### 列出组织项目

```bash
GET /sentry/api/0/organizations/{organization_slug}/projects/
```

#### 列出组织成员

```bash
GET /sentry/api/0/organizations/{organization_slug}/members/
```

### 项目操作

#### 获取项目信息

```bash
GET /sentry/api/0/projects/{organization_slug}/{project_slug}/
```

#### 更新项目信息

```bash
PUT /sentry/api/0/projects/{organization_slug}/{project_slug}/
Content-Type: application/json

{
  "name": "Updated Project Name",
  "slug": "updated-project-slug"
}
```

#### 删除项目

```bash
DELETE /sentry/api/0/projects/{organization_slug}/{project_slug}/
```

#### 创建新项目

```bash
POST /sentry/api/0/teams/{organization_slug}/{team_slug}/projects/
Content-Type: application/json

{
  "name": "New Project",
  "slug": "new-project"
}
```

### 问题操作

#### 列出项目中的问题

```bash
GET /sentry/api/0/projects/{organization_slug}/{project_slug}/issues/
```

**查询参数：**
- `statsPeriod` - 统计周期：`24h`、`14d` 或空
- `shortIdLookup` - 启用简短ID查询（设置为 `1`）
- `query` - Sentry搜索查询（默认：`is:unresolved`）
- `cursor` - 分页游标

#### 列出组织中的问题

```bash
GET /sentry/api/0/organizations/{organization_slug}/issues/
```

#### 获取问题信息

```bash
GET /sentry/api/0/issues/{issue_id}/
```

#### 更新问题信息

```bash
PUT /sentry/api/0/issues/{issue_id}/
Content-Type: application/json

{
  "status": "resolved"
}
```

**状态值：** `resolved`、`unresolved`、`ignored`

#### 删除问题

```bash
DELETE /sentry/api/0/issues/{issue_id}/
```

#### 列出问题事件

```bash
GET /sentry/api/0/issues/{issue_id}/events/
```

#### 列出问题哈希值

```bash
GET /sentry/api/0/issues/{issue_id}/hashes/
```

### 事件操作

#### 列出项目中的事件

```bash
GET /sentry/api/0/projects/{organization_slug}/{project_slug}/events/
```

#### 获取事件信息

```bash
GET /sentry/api/0/projects/{organization_slug}/{project_slug}/events/{event_id}/
```

### 团队操作

#### 列出组织中的团队

```bash
GET /sentry/api/0/organizations/{organization_slug}/teams/
```

#### 创建团队

```bash
POST /sentry/api/0/organizations/{organization_slug}/teams/
Content-Type: application/json

{
  "name": "New Team",
  "slug": "new-team"
}
```

#### 获取团队信息

```bash
GET /sentry/api/0/teams/{organization_slug}/{team_slug}/
```

#### 更新团队信息

```bash
PUT /sentry/api/0/teams/{organization_slug}/{team_slug}/
Content-Type: application/json

{
  "name": "Updated Team Name"
}
```

#### 删除团队

```bash
DELETE /sentry/api/0/teams/{organization_slug}/{team_slug}/
```

#### 列出团队项目

```bash
GET /sentry/api/0/teams/{organization_slug}/{team_slug}/projects/
```

### 发布版本操作

#### 列出组织中的发布版本

```bash
GET /sentry/api/0/organizations/{organization_slug}/releases/
```

#### 创建发布版本

```bash
POST /sentry/api/0/organizations/{organization_slug}/releases/
Content-Type: application/json

{
  "version": "1.0.0",
  "projects": ["project-slug"]
}
```

#### 获取发布版本信息

```bash
GET /sentry/api/0/organizations/{organization_slug}/releases/{version}/
```

#### 更新发布版本信息

```bash
PUT /sentry/api/0/organizations/{organization_slug}/releases/{version}/
Content-Type: application/json

{
  "ref": "main",
  "commits": [
    {
      "id": "abc123",
      "message": "Fix bug"
    }
  ]
}
```

#### 删除发布版本

```bash
DELETE /sentry/api/0/organizations/{organization_slug}/releases/{version}/
```

#### 列出发布版本的部署信息

```bash
GET /sentry/api/0/organizations/{organization_slug}/releases/{version}/deploys/
```

#### 创建部署记录

```bash
POST /sentry/api/0/organizations/{organization_slug}/releases/{version}/deploys/
Content-Type: application/json

{
  "environment": "production"
}
```

## 分页

Sentry 使用基于游标的分页机制，通过 `Link` 头部实现分页。

```bash
GET /sentry/api/0/projects/{organization_slug}/{project_slug}/issues/?cursor=0:100:0
```

响应头中包含分页链接：

```
Link: <...?cursor=0:0:1>; rel="previous"; results="false"; cursor="0:0:1",
      <...?cursor=0:100:0>; rel="next"; results="true"; cursor="0:100:0"
```

- `results="true"` 表示还有更多结果
- `results="false"` 表示该方向上没有更多结果

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/sentry/api/0/organizations/',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/sentry/api/0/organizations/',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### Python - 解决问题

```python
import os
import requests

response = requests.put(
    'https://gateway.maton.ai/sentry/api/0/issues/12345/',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'status': 'resolved'}
)
```

## 注意事项

- Sentry API 使用 `0` 前缀：`/api/0/`
- 组织和项目的标识符使用短横线分隔的 lowercase 字符串
- 问题ID 是数字
- 发布版本的名称可以包含特殊字符（需要根据需要进行 URL 编码）
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含括号，请使用 `curl -g` 以避免全局解析问题
- 重要提示：当将 `curl` 的输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未建立Sentry连接 |
| 401 | Maton API密钥无效或缺失 |
| 403 | 权限不足（请检查 OAuth 范围） |
| 404 | 资源未找到 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自Sentry API 的传递错误 |

## 资源

- [Sentry API 文档](https://docs.sentry.io/api/)
- [Sentry API 认证](https://docs.sentry.io/api/auth/)
- [Sentry 事件 API](https://docs.sentry.io/api/events/)
- [Sentry 项目 API](https://docs.sentry.io/api/projects/)
- [Sentry 组织 API](https://docs.sentry.io/api/organizations/)
- [Sentry 团队 API](https://docs.sentry.io/api/teams/)
- [Sentry 发布版本 API](https://docs.sentry.io/api/releases/)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)