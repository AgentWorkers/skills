---
name: grafana
description: >
  Grafana API集成支持管理认证功能，允许用户对仪表板、数据源、文件夹、注释、警报以及团队进行操作。  
  当用户需要使用Grafana进行监控、数据可视化及故障排查时，可运用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Grafana

您可以通过管理的API认证来访问Grafana的仪表板、数据源、文件夹、注释和警报。

## 快速入门

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/grafana/api/search?type=dash-db')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/grafana/{native-api-path}
```

该网关会将请求代理到您的Grafana实例，并自动进行身份验证。

## 身份验证

所有请求都需要使用Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Grafana连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=grafana&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'grafana'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

在浏览器中打开返回的 `url` 以完成身份验证。您需要提供您的Grafana服务账户令牌。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

---

## API参考

### 组织与用户

#### 获取当前组织

```bash
GET /grafana/api/org
```

**响应：**
```json
{
  "id": 1,
  "name": "Main Org.",
  "address": {
    "address1": "",
    "address2": "",
    "city": "",
    "zipCode": "",
    "state": "",
    "country": ""
  }
}
```

#### 获取当前用户

```bash
GET /grafana/api/user
```

**响应：**
```json
{
  "id": 1,
  "uid": "abc123",
  "email": "user@example.com",
  "name": "User Name",
  "login": "user",
  "orgId": 1,
  "isGrafanaAdmin": false
}
```

---

### 仪表板

#### 搜索仪表板

```bash
GET /grafana/api/search?type=dash-db
```

**查询参数：**
- `type` - `dash-db` 用于搜索仪表板，`dash-folder` 用于搜索文件夹
- `query` - 搜索查询字符串
- `tag` - 按标签过滤
- `folderIds` - 按文件夹ID过滤
- `limit` - 最大结果数量（默认为1000）

**响应：**
```json
[
  {
    "id": 1,
    "uid": "abc123",
    "title": "My Dashboard",
    "uri": "db/my-dashboard",
    "url": "/d/abc123/my-dashboard",
    "type": "dash-db",
    "tags": ["production"],
    "isStarred": false
  }
]
```

#### 通过UID获取仪表板

```bash
GET /grafana/api/dashboards/uid/{uid}
```

**响应：**
```json
{
  "meta": {
    "type": "db",
    "canSave": true,
    "canEdit": true,
    "canAdmin": true,
    "canStar": true,
    "slug": "my-dashboard",
    "url": "/d/abc123/my-dashboard",
    "expires": "0001-01-01T00:00:00Z",
    "created": "2024-01-01T00:00:00Z",
    "updated": "2024-01-02T00:00:00Z",
    "version": 1
  },
  "dashboard": {
    "id": 1,
    "uid": "abc123",
    "title": "My Dashboard",
    "tags": ["production"],
    "panels": [...],
    "schemaVersion": 30,
    "version": 1
  }
}
```

#### 创建/更新仪表板

```bash
POST /grafana/api/dashboards/db
Content-Type: application/json

{
  "dashboard": {
    "title": "New Dashboard",
    "panels": [],
    "schemaVersion": 30,
    "version": 0
  },
  "folderUid": "optional-folder-uid",
  "overwrite": false
}
```

**响应：**
```json
{
  "id": 1,
  "uid": "abc123",
  "url": "/d/abc123/new-dashboard",
  "status": "success",
  "version": 1,
  "slug": "new-dashboard"
}
```

#### 删除仪表板

```bash
DELETE /grafana/api/dashboards/uid/{uid}
```

**响应：**
```json
{
  "title": "My Dashboard",
  "message": "Dashboard My Dashboard deleted",
  "id": 1
}
```

#### 获取首页仪表板

```bash
GET /grafana/api/dashboards/home
```

---

### 文件夹

#### 列出文件夹

```bash
GET /grafana/api/folders
```

**响应：**
```json
[
  {
    "id": 1,
    "uid": "folder123",
    "title": "My Folder",
    "url": "/dashboards/f/folder123/my-folder",
    "hasAcl": false,
    "canSave": true,
    "canEdit": true,
    "canAdmin": true
  }
]
```

#### 通过UID获取文件夹

```bash
GET /grafana/api/folders/{uid}
```

#### 创建文件夹

```bash
POST /grafana/api/folders
Content-Type: application/json

{
  "title": "New Folder"
}
```

**响应：**
```json
{
  "id": 1,
  "uid": "folder123",
  "title": "New Folder",
  "url": "/dashboards/f/folder123/new-folder",
  "hasAcl": false,
  "canSave": true,
  "canEdit": true,
  "canAdmin": true,
  "version": 1
}
```

#### 更新文件夹

```bash
PUT /grafana/api/folders/{uid}
Content-Type: application/json

{
  "title": "Updated Folder Name",
  "version": 1
}
```

#### 删除文件夹

```bash
DELETE /grafana/api/folders/{uid}
```

---

### 数据源

#### 列出数据源

```bash
GET /grafana/api/datasources
```

**响应：**
```json
[
  {
    "id": 1,
    "uid": "ds123",
    "orgId": 1,
    "name": "Prometheus",
    "type": "prometheus",
    "access": "proxy",
    "url": "http://prometheus:9090",
    "isDefault": true,
    "readOnly": false
  }
]
```

#### 通过ID获取数据源

```bash
GET /grafana/api/datasources/{id}
```

#### 通过UID获取数据源

```bash
GET /grafana/api/datasources/uid/{uid}
```

#### 通过名称获取数据源

```bash
GET /grafana/api/datasources/name/{name}
```

#### 创建数据源

```bash
POST /grafana/api/datasources
Content-Type: application/json

{
  "name": "New Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy",
  "isDefault": false
}
```

#### 更新数据源

```bash
PUT /grafana/api/datasources/{id}
Content-Type: application/json

{
  "name": "Updated Prometheus",
  "type": "prometheus",
  "url": "http://prometheus:9090",
  "access": "proxy"
}
```

#### 删除数据源

```bash
DELETE /grafana/api/datasources/{id}
```

---

### 注释

#### 列出注释

```bash
GET /grafana/api/annotations
```

**查询参数：**
- `from` - 时间戳（毫秒）
- `to` - 时间戳（毫秒）
- `dashboardId` - 按仪表板ID过滤
- `dashboardUID` - 按仪表板UID过滤
- `panelId` - 按面板ID过滤
- `tags` - 按标签过滤（用逗号分隔）
- `limit` - 最大结果数量

#### 创建注释

```bash
POST /grafana/api/annotations
Content-Type: application/json

{
  "dashboardUID": "abc123",
  "time": 1609459200000,
  "text": "Deployment completed",
  "tags": ["deployment", "production"]
}
```

**响应：**
```json
{
  "message": "Annotation added",
  "id": 1
}
```

#### 更新注释

```bash
PUT /grafana/api/annotations/{id}
Content-Type: application/json

{
  "text": "Updated annotation text",
  "tags": ["updated"]
}
```

#### 删除注释

```bash
DELETE /grafana/api/annotations/{id}
```

---

### 团队

#### 搜索团队

```bash
GET /grafana/api/teams/search
```

**查询参数：**
- `query` - 搜索查询
- `page` - 页码
- `perpage` - 每页显示的结果数量

**响应：**
```json
{
  "totalCount": 1,
  "teams": [
    {
      "id": 1,
      "orgId": 1,
      "name": "Engineering",
      "email": "engineering@example.com",
      "memberCount": 5
    }
  ],
  "page": 1,
  "perPage": 1000
}
```

#### 通过ID获取团队

```bash
GET /grafana/api/teams/{id}
```

#### 创建团队

```bash
POST /grafana/api/teams
Content-Type: application/json

{
  "name": "New Team",
  "email": "team@example.com"
}
```

#### 更新团队

```bash
PUT /grafana/api/teams/{id}
Content-Type: application/json

{
  "name": "Updated Team Name"
}
```

#### 删除团队

```bash
DELETE /grafana/api/teams/{id}
```

---

### 警报规则（配置API）

#### 列出警报规则

```bash
GET /grafana/api/v1/provisioning/alert-rules
```

#### 获取警报规则

```bash
GET /grafana/api/v1/provisioning/alert-rules/{uid}
```

#### 按文件夹列出警报规则

```bash
GET /grafana/api/ruler/grafana/api/v1/rules
```

---

### 服务账户

#### 搜索服务账户

```bash
GET /grafana/api/serviceaccounts/search
```

**响应：**
```json
{
  "totalCount": 1,
  "serviceAccounts": [
    {
      "id": 1,
      "name": "api-service",
      "login": "sa-api-service",
      "orgId": 1,
      "isDisabled": false,
      "role": "Editor"
    }
  ],
  "page": 1,
  "perPage": 1000
}
```

---

### 插件

#### 列出插件

```bash
GET /grafana/api/plugins
```

**响应：**
```json
[
  {
    "name": "Prometheus",
    "type": "datasource",
    "id": "prometheus",
    "enabled": true,
    "pinned": false
  }
]
```

---

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/grafana/api/search?type=dash-db', {
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  }
});
const dashboards = await response.json();
console.log(dashboards);
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/grafana/api/search?type=dash-db',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'
    }
)
print(response.json())
```

---

## 注意事项

- 仪表板UID是大多数操作中使用的唯一标识符。
- 使用 `/api/search?type=dash-db` 来查找仪表板UID。
- 操作文件夹需要文件夹UID。
- 某些管理操作（如列出所有用户、组织）需要更高的权限。
- 警报规则使用配置API（`/api/v1/provisioning/...`）。
- 注释需要时间戳（以毫秒为单位）。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 200 | 成功 |
| 400 | 请求无效 |
| 401 | 身份验证无效或缺失 |
| 403 | 权限被拒绝 |
| 404 | 资源未找到 |
| 409 | 冲突（例如，名称重复） |
| 412 | 先决条件失败（版本不匹配） |
| 422 | 实体无法处理 |

## 资源

- [Grafana HTTP API文档](https://grafana.com/docs/grafana/latest/developers/http_api/)
- [仪表板API](https://grafana.com/docs/grafana/latest/developers/http_api/dashboard/)
- [文件夹API](https://grafana.com/docs/grafana/latest/developers/http_api/folder/)
- [数据源API](https://grafana.com/docs/grafana/latest/developers/http_api/data_source/)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)