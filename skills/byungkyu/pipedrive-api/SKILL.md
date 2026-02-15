---
name: pipedrive
description: |
  Pipedrive API integration with managed OAuth. Manage deals, persons, organizations, activities, and pipelines. Use this skill when users want to interact with Pipedrive CRM. For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Pipedrive

通过管理的 OAuth 认证来访问 Pipedrive API。您可以管理销售 CRM 工作流程中的交易、人员、组织、活动、管道等。

## 快速入门

```bash
# List deals
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/pipedrive/api/v1/deals')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/pipedrive/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Pipedrive API 端点路径。该网关会将请求代理到 `api.pipedrive.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Pipedrive OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=pipedrive&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'pipedrive'}).encode()
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
    "app": "pipedrive",
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

如果您有多个 Pipedrive 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/pipedrive/api/v1/deals')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 交易

#### 列出交易

```bash
GET /pipedrive/api/v1/deals
```

查询参数：
- `status` - 按状态筛选：`open`（未完成）、`won`（已赢得）、`lost`（已丢失）、`deleted`（已删除）、`all_not_deleted`（所有未删除的交易）
- `filter_id` - 要使用的筛选 ID
- `stage_id` - 按阶段筛选
- `user_id` - 按用户筛选
- `start` - 分页起始位置（默认为 0）
- `limit` - 每页显示的条数（默认为 100）
- `sort` - 排序字段和顺序（例如，`add_time DESC`）

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/pipedrive/api/v1/deals?status=open&limit=50')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取交易信息

```bash
GET /pipedrive/api/v1/deals/{id}
```

#### 创建交易

```bash
POST /pipedrive/api/v1/deals
Content-Type: application/json

{
  "title": "New Enterprise Deal",
  "value": 50000,
  "currency": "USD",
  "person_id": 123,
  "org_id": 456,
  "stage_id": 1,
  "expected_close_date": "2025-06-30"
}
```

#### 更新交易

```bash
PUT /pipedrive/api/v1/deals/{id}
Content-Type: application/json

{
  "title": "Updated Deal Title",
  "value": 75000,
  "status": "won"
}
```

#### 删除交易

```bash
DELETE /pipedrive/api/v1/deals/{id}
```

#### 搜索交易

```bash
GET /pipedrive/api/v1/deals/search?term=enterprise
```

### 人员（联系人）

#### 列出人员

```bash
GET /pipedrive/api/v1/persons
```

查询参数：
- `filter_id` - 筛选 ID
- `start` - 分页起始位置
- `limit` - 每页显示的条数
- `sort` - 排序字段和顺序

#### 获取人员信息

```bash
GET /pipedrive/api/v1/persons/{id}
```

#### 创建人员

```bash
POST /pipedrive/api/v1/persons
Content-Type: application/json

{
  "name": "John Doe",
  "email": ["john@example.com"],
  "phone": ["+1234567890"],
  "org_id": 456,
  "visible_to": 3
}
```

#### 更新人员信息

```bash
PUT /pipedrive/api/v1/persons/{id}
Content-Type: application/json

{
  "name": "John Smith",
  "email": ["john.smith@example.com"]
}
```

#### 删除人员

```bash
DELETE /pipedrive/api/v1/persons/{id}
```

#### 搜索人员

```bash
GET /pipedrive/api/v1/persons/search?term=john
```

### 组织

#### 列出组织

```bash
GET /pipedrive/api/v1/organizations
```

#### 获取组织信息

```bash
GET /pipedrive/api/v1/organizations/{id}
```

#### 创建组织

```bash
POST /pipedrive/api/v1/organizations
Content-Type: application/json

{
  "name": "Acme Corporation",
  "address": "123 Main St, City, Country",
  "visible_to": 3
}
```

#### 更新组织信息

```bash
PUT /pipedrive/api/v1/organizations/{id}
Content-Type: application/json

{
  "name": "Acme Corp International"
}
```

#### 删除组织

```bash
DELETE /pipedrive/api/v1/organizations/{id}
```

### 活动

#### 列出活动

```bash
GET /pipedrive/api/v1/activities
```

查询参数：
- `type` - 活动类型（例如，`call`（电话）、`meeting`（会议）、`task`（任务）、`email`（邮件）
- `done` - 按完成状态筛选（0 或 1）
- `user_id` - 按用户筛选
- `start_date` - 按开始日期筛选
- `end_date` - 按结束日期筛选

#### 获取活动信息

```bash
GET /pipedrive/api/v1/activities/{id}
```

#### 创建活动

```bash
POST /pipedrive/api/v1/activities
Content-Type: application/json

{
  "subject": "Follow-up call",
  "type": "call",
  "due_date": "2025-03-15",
  "due_time": "14:00",
  "duration": "00:30",
  "deal_id": 789,
  "person_id": 123,
  "note": "Discuss contract terms"
}
```

#### 更新活动信息

```bash
PUT /pipedrive/api/v1/activities/{id}
Content-Type: application/json

{
  "done": 1,
  "note": "Completed - customer agreed to terms"
}
```

#### 删除活动

```bash
DELETE /pipedrive/api/v1/activities/{id}
```

### 管道

#### 列出管道

```bash
GET /pipedrive/api/v1/pipelines
```

#### 获取管道信息

```bash
GET /pipedrive/api/v1/pipelines/{id}
```

### 阶段

#### 列出阶段

```bash
GET /pipedrive/api/v1/stages
```

查询参数：
- `pipeline_id` - 按管道筛选

#### 获取阶段信息

```bash
GET /pipedrive/api/v1/stages/{id}
```

### 备注

#### 列出备注

```bash
GET /pipedrive/api/v1/notes
```

查询参数：
- `deal_id` - 按交易筛选
- `person_id` - 按人员筛选
- `org_id` - 按组织筛选

#### 创建备注

```bash
POST /pipedrive/api/v1/notes
Content-Type: application/json

{
  "content": "Meeting notes: Discussed pricing and timeline",
  "deal_id": 789,
  "pinned_to_deal_flag": 1
}
```

### 用户

#### 列出用户

```bash
GET /pipedrive/api/v1/users
```

#### 获取当前用户信息

```bash
GET /pipedrive/api/v1/users/me
```

## 代码示例

### JavaScript

```javascript
const headers = {
  'Authorization': `Bearer ${process.env.MATON_API_KEY}`
};

// List open deals
const deals = await fetch(
  'https://gateway.maton.ai/pipedrive/api/v1/deals?status=open',
  { headers }
).then(r => r.json());

// Create a deal
await fetch(
  'https://gateway.maton.ai/pipedrive/api/v1/deals',
  {
    method: 'POST',
    headers: { ...headers, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: 'New Deal',
      value: 10000,
      currency: 'USD'
    })
  }
);
```

### Python

```python
import os
import requests

headers = {'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}

# List open deals
deals = requests.get(
    'https://gateway.maton.ai/pipedrive/api/v1/deals',
    headers=headers,
    params={'status': 'open'}
).json()

# Create a deal
response = requests.post(
    'https://gateway.maton.ai/pipedrive/api/v1/deals',
    headers=headers,
    json={
        'title': 'New Deal',
        'value': 10000,
        'currency': 'USD'
    }
)
```

## 注意事项

- ID 为整数。
- 电子邮件和电话字段支持多个值的数组。
- `visible_to` 的值：1（仅所有者可见）、3（整个公司可见）、5（所有者和指定可见组可见）、7（整个公司和指定可见组可见）。
- 交易状态：`open`（未完成）、`won`（已赢得）、`lost`（已丢失）、`deleted`（已删除）。
- 使用 `start` 和 `limit` 进行分页。
- 支持通过 API 密钥访问自定义字段（例如，`abc123_custom_field`）。
- 重要提示：当 URL 包含方括号（`fields[]`、`sort[]`、`records[]`）时，使用 `curl -g` 可以防止全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 可能无法正确展开，可能会导致“无效 API 密钥”错误。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 缺少 Pipedrive 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 每个账户的请求速率限制（10 次/秒） |
| 4xx/5xx | 来自 Pipedrive API 的传递错误 |

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

1. 确保您的 URL 路径以 `pipedrive` 开头。例如：
- 正确：`https://gateway.maton.ai/pipedrive/api/v1/deals`
- 错误：`https://gateway.maton.ai/api/v1/deals`

## 资源

- [Pipedrive API 概述](https://developers.pipedrive.com/docs/api/v1)
- [交易](https://developers.pipedrive.com/docs/api/v1/Deals)
- [人员](https://developers.pipedrive.com/docs/api/v1/Persons)
- [组织](https://developers.pipedrive.com/docs/api/v1/Organizations)
- [活动](https://developers.pipedrive.com/docs/api/v1/Activities)
- [管道](https://developers.pipedrive.com/docs/api/v1/Pipelines)
- [阶段](https://developers.pipedrive.com/docs/api/v1/Stages)
- [备注](https://developers.pipedrive.com/docs/api/v1/Notes)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)