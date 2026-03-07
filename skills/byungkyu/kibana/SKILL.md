---
name: kibana
description: >
  **Kibana API集成与托管式身份验证**  
  支持管理保存的对象、仪表盘、数据视图、工作区（spaces）、警报（alerts）以及整个Kibana系统。  
  当用户需要通过Kibana进行监控、安全分析或搜索操作时，可使用此功能。  
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
# Kibana

您可以通过管理的API认证来访问Kibana中的保存对象、仪表盘、数据视图、空间（spaces）、警报（alerts）以及代理群组（fleet）。

## 快速入门

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/kibana/api/saved_objects/_find?type=dashboard')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('kbn-xsrf', 'true')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/kibana/{native-api-path}
```

该网关会代理请求到您的Kibana实例，并自动进行身份验证。

## 身份验证

所有请求都需要提供Maton API密钥以及`kbn-xsrf`头部信息：

```
Authorization: Bearer $MATON_API_KEY
kbn-xsrf: true
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的Kibana连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=kibana&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'kibana'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

在浏览器中打开返回的`url`以完成身份验证。您需要提供您的Kibana API密钥。

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

**重要提示：** 所有Kibana API请求都必须包含`kbn-xsrf: true`头部信息。

### 状态与功能

#### 获取状态

```bash
GET /kibana/api/status
```

**响应：**
```json
{
  "name": "kibana",
  "uuid": "abc123",
  "version": {
    "number": "8.15.0",
    "build_hash": "..."
  },
  "status": {
    "overall": {"level": "available"}
  }
}
```

#### 列出功能

```bash
GET /kibana/api/features
```

返回所有Kibana功能及其相应功能。

---

### 保存对象

#### 查找保存的对象

```bash
GET /kibana/api/saved_objects/_find?type={type}
```

**查询参数：**
- `type` - 对象类型：`dashboard`（仪表盘）、`visualization`（数据可视化）、`index-pattern`（索引模式）、`search`（搜索）、`lens`（透镜效果）、`map`（地图可视化）
- `search` - 搜索查询
- `page` - 页码
- `per_page` - 每页显示的结果数量（默认20条，最多10000条）
- `fields` - 需要返回的字段

**响应：**
```json
{
  "page": 1,
  "per_page": 20,
  "total": 5,
  "saved_objects": [
    {
      "id": "abc123",
      "type": "dashboard",
      "attributes": {
        "title": "My Dashboard",
        "description": "Dashboard description"
      },
      "version": "1",
      "updated_at": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

#### 获取保存的对象

```bash
GET /kibana/api/saved_objects/{type}/{id}
```

#### 创建保存的对象

```bash
POST /kibana/api/saved_objects/{type}/{id}
Content-Type: application/json

{
  "attributes": {
    "title": "My Index Pattern",
    "timeFieldName": "@timestamp"
  }
}
```

#### 更新保存的对象

```bash
PUT /kibana/api/saved_objects/{type}/{id}
Content-Type: application/json

{
  "attributes": {
    "title": "Updated Title"
  }
}
```

#### 删除保存的对象

```bash
DELETE /kibana/api/saved_objects/{type}/{id}
```

#### 批量操作

```bash
POST /kibana/api/saved_objects/_bulk_get
Content-Type: application/json

[
  {"type": "dashboard", "id": "abc123"},
  {"type": "visualization", "id": "def456"}
]
```

---

### 数据视图

#### 列出数据视图

```bash
GET /kibana/api/data_views
```

**响应：**
```json
{
  "data_view": [
    {
      "id": "abc123",
      "title": "logs-*",
      "timeFieldName": "@timestamp"
    }
  ]
}
```

#### 获取数据视图

```bash
GET /kibana/api/data_views/data_view/{id}
```

#### 创建数据视图

```bash
POST /kibana/api/data_views/data_view
Content-Type: application/json

{
  "data_view": {
    "title": "logs-*",
    "timeFieldName": "@timestamp"
  }
}
```

**响应：**
```json
{
  "data_view": {
    "id": "abc123",
    "title": "logs-*",
    "timeFieldName": "@timestamp"
  }
}
```

#### 更新数据视图

```bash
POST /kibana/api/data_views/data_view/{id}
Content-Type: application/json

{
  "data_view": {
    "title": "updated-logs-*"
  }
}
```

#### 删除数据视图

```bash
DELETE /kibana/api/data_views/data_view/{id}
```

---

### 空间（Spaces）

#### 列出空间

```bash
GET /kibana/api/spaces/space
```

**响应：**
```json
[
  {
    "id": "default",
    "name": "Default",
    "description": "Default space",
    "disabledFeatures": []
  }
]
```

#### 获取空间信息

```bash
GET /kibana/api/spaces/space/{id}
```

#### 创建空间

```bash
POST /kibana/api/spaces/space
Content-Type: application/json

{
  "id": "marketing",
  "name": "Marketing",
  "description": "Marketing team space",
  "disabledFeatures": []
}
```

#### 更新空间

```bash
PUT /kibana/api/spaces/space/{id}
Content-Type: application/json

{
  "id": "marketing",
  "name": "Marketing Team",
  "description": "Updated description"
}
```

#### 删除空间

```bash
DELETE /kibana/api/spaces/space/{id}
```

---

### 警报（Alerting）

#### 查找警报规则

```bash
GET /kibana/api/alerting/rules/_find
```

**查询参数：**
- `search` - 搜索查询
- `page` - 页码
- `per_page` - 每页显示的结果数量

**响应：**
```json
{
  "page": 1,
  "per_page": 10,
  "total": 5,
  "data": [
    {
      "id": "abc123",
      "name": "CPU Alert",
      "consumer": "alerts",
      "enabled": true,
      "rule_type_id": "metrics.alert.threshold"
    }
  ]
}
```

#### 获取警报规则

```bash
GET /kibana/api/alerting/rule/{id}
```

#### 启用/禁用规则

```bash
POST /kibana/api/alerting/rule/{id}/_enable
POST /kibana/api/alerting/rule/{id}/_disable
```

#### 静音/取消静音规则

```bash
POST /kibana/api/alerting/rule/{id}/_mute_all
POST /kibana/api/alerting/rule/{id}/_unmute_all
```

#### 获取警报系统状态

```bash
GET /kibana/api/alerting/_health
```

---

### 连接器（Connectors）

#### 列出连接器

```bash
GET /kibana/api/actions/connectors
```

**响应：**
```json
[
  {
    "id": "abc123",
    "name": "Email Connector",
    "connector_type_id": ".email",
    "is_preconfigured": false,
    "is_deprecated": false
  }
]
```

#### 获取连接器信息

```bash
GET /kibana/api/actions/connector/{id}
```

#### 列出连接器类型

```bash
GET /kibana/api/actions/connector_types
```

#### 执行连接器操作

```bash
POST /kibana/api/actions/connector/{id}/_execute
Content-Type: application/json

{
  "params": {
    "to": ["user@example.com"],
    "subject": "Alert",
    "message": "Alert triggered"
  }
}
```

---

### 代理群组（Fleet）

#### 列出代理策略

```bash
GET /kibana/api/fleet/agent_policies
```

**响应：**
```json
{
  "items": [
    {
      "id": "abc123",
      "name": "Default policy",
      "namespace": "default",
      "status": "active"
    }
  ],
  "total": 1,
  "page": 1,
  "perPage": 20
}
```

#### 列出代理（Agents）

```bash
GET /kibana/api/fleet/agents
```

#### 列出插件（Packages）

```bash
GET /kibana/api/fleet/epm/packages
```

返回所有可用的插件/集成组件。

---

### 安全性

#### 列出角色

```bash
GET /kibana/api/security/role
```

**响应：**
```json
[
  {
    "name": "admin",
    "metadata": {},
    "elasticsearch": {
      "cluster": ["all"],
      "indices": [...]
    },
    "kibana": [...]
  }
]
```

#### 获取角色信息

```bash
GET /kibana/api/security/role/{name}
```

---

### 案例（Cases）

#### 查找案例

```bash
GET /kibana/api/cases/_find
```

**查询参数：**
- `status` - 状态（`open`、`in-progress`、`closed`）
- `severity` - 严重程度（`low`、`medium`、`high`、`critical`）
- `page` - 页码
- `perPage` - 每页显示的结果数量

**响应：**
```json
{
  "cases": [],
  "page": 1,
  "per_page": 20,
  "total": 0
}
```

---

## 代码示例

### JavaScript

```javascript
const response = await fetch('https://gateway.maton.ai/kibana/api/saved_objects/_find?type=dashboard', {
  headers: {
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
    'kbn-xsrf': 'true'
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
    'https://gateway.maton.ai/kibana/api/saved_objects/_find?type=dashboard',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'kbn-xsrf': 'true'
    }
)
print(response.json())
```

---

## 注意事项

- 所有请求都必须包含`kbn-xsrf: true`头部信息。
- 保存的对象类型包括：`dashboard`（仪表盘）、`visualization`（数据可视化）、`index-pattern`（索引模式）、`search`（搜索）、`lens`（透镜效果）、`map`（地图可视化）。
- 数据视图（Data Views）是索引模式的现代替代方案。
- 空间（Spaces）支持多租户功能。
- 代理群组（Fleet）用于管理Elastic Agents和插件。
- 某些操作需要特定的Kibana权限。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 200 | 操作成功 |
| 204 | 无内容（删除成功） |
| 400 | 请求无效 |
| 401 | 身份验证无效或缺失 |
| 403 | 没有权限 |
| 404 | 资源未找到 |
| 409 | 冲突（例如，对象已存在） |

## 资源

- [Kibana REST API文档](https://www.elastic.co/docs/api/doc/kibana/)
- [保存对象API](https://www.elastic.co/guide/en/kibana/current/saved-objects-api.html)
- [警报API](https://www.elastic.co/guide/en/kibana/current/alerting-apis.html)
- [代理群组API](https://www.elastic.co/guide/en/fleet/current/fleet-apis.html)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)