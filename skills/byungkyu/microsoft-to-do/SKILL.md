---
name: microsoft-to-do
description: |
  Microsoft To Do API integration with managed OAuth. Manage task lists, tasks, checklist items, and linked resources.
  Use this skill when users want to create, read, update, or delete tasks and task lists in Microsoft To Do.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Microsoft To Do

通过托管的 OAuth 认证来访问 Microsoft To Do API。您可以执行完整的 CRUD 操作（创建、读取、更新和删除）来管理任务列表、任务、待办事项以及关联的资源。

## 快速入门

```bash
# List all task lists
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/microsoft-to-do/v1.0/me/todo/lists')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/microsoft-to-do/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Microsoft Graph API 端点路径。该网关会将请求代理到 `graph.microsoft.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的 Microsoft To Do OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=microsoft-to-do&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'microsoft-to-do'}).encode()
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
    "app": "microsoft-to-do",
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

如果您有多个 Microsoft To Do 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/microsoft-to-do/v1.0/me/todo/lists')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API 参考

### 任务列表操作

#### 列出任务列表

```bash
GET /microsoft-to-do/v1.0/me/todo/lists
```

**响应：**
```json
{
  "value": [
    {
      "id": "AAMkADIyAAAhrbPWAAA=",
      "displayName": "Tasks",
      "isOwner": true,
      "isShared": false,
      "wellknownListName": "defaultList"
    }
  ]
}
```

#### 获取任务列表

```bash
GET /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}
```

#### 创建任务列表

```bash
POST /microsoft-to-do/v1.0/me/todo/lists
Content-Type: application/json

{
  "displayName": "Travel items"
}
```

**响应（201 Created）：**
```json
{
  "id": "AAMkADIyAAAhrbPWAAA=",
  "displayName": "Travel items",
  "isOwner": true,
  "isShared": false,
  "wellknownListName": "none"
}
```

#### 更新任务列表

```bash
PATCH /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}
Content-Type: application/json

{
  "displayName": "Vacation Plan"
}
```

#### 删除任务列表

```bash
DELETE /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}
```

成功时返回 `204 No Content`。

### 任务操作

#### 列出任务

```bash
GET /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks
```

**响应：**
```json
{
  "value": [
    {
      "id": "AlMKXwbQAAAJws6wcAAAA=",
      "title": "Buy groceries",
      "status": "notStarted",
      "importance": "normal",
      "isReminderOn": false,
      "createdDateTime": "2024-01-15T10:00:00Z",
      "lastModifiedDateTime": "2024-01-15T10:00:00Z",
      "body": {
        "content": "",
        "contentType": "text"
      },
      "categories": []
    }
  ]
}
```

#### 获取任务详情

```bash
GET /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}
```

#### 创建任务

```bash
POST /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks
Content-Type: application/json

{
  "title": "A new task",
  "importance": "high",
  "status": "notStarted",
  "categories": ["Important"],
  "dueDateTime": {
    "dateTime": "2024-12-31T17:00:00",
    "timeZone": "Eastern Standard Time"
  },
  "startDateTime": {
    "dateTime": "2024-12-01T08:00:00",
    "timeZone": "Eastern Standard Time"
  },
  "isReminderOn": true,
  "reminderDateTime": {
    "dateTime": "2024-12-01T09:00:00",
    "timeZone": "Eastern Standard Time"
  },
  "body": {
    "content": "Task details here",
    "contentType": "text"
  }
}
```

**任务字段：**

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `title` | String | 任务的简要描述 |
| `body` | itemBody | 任务内容及内容类型（text/html） |
| `importance` | String | `low`、`normal` 或 `high` |
| `status` | String | `notStarted`、`inProgress`、`completed`、`waitingOnOthers`、`deferred` |
| `categories` | String[] | 关联的类别名称 |
| `dueDateTime` | dateTimeTimeZone | 截止日期和时间 |
| `startDateTime` | dateTimeTimeZone | 开始日期和时间 |
| `completedDateTime` | dateTimeTimeZone | 完成日期和时间 |
| `reminderDateTime` | dateTimeTimeZone | 提醒日期和时间 |
| `isReminderOn` | Boolean | 是否启用提醒 |
| `recurrence` | patternedRecurrence | 重复模式 |

#### 更新任务

```bash
PATCH /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}
Content-Type: application/json

{
  "status": "completed",
  "completedDateTime": {
    "dateTime": "2024-01-20T15:00:00",
    "timeZone": "UTC"
  }
}
```

#### 删除任务

```bash
DELETE /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}
```

成功时返回 `204 No Content`。

### 待办事项操作

待办事项是任务中的子任务。

#### 列出待办事项

```bash
GET /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}/checklistItems
```

**响应：**
```json
{
  "value": [
    {
      "id": "51d8a471-2e9d-4f53-9937-c33a8742d28f",
      "displayName": "Create draft",
      "createdDateTime": "2024-01-17T05:22:14Z",
      "isChecked": false
    }
  ]
}
```

#### 创建待办事项

```bash
POST /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}/checklistItems
Content-Type: application/json

{
  "displayName": "Final sign-off from the team"
}
```

#### 更新待办事项

```bash
PATCH /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}/checklistItems/{checklistItemId}
Content-Type: application/json

{
  "isChecked": true
}
```

#### 删除待办事项

```bash
DELETE /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}/checklistItems/{checklistItemId}
```

成功时返回 `204 No Content`。

### 关联资源操作

关联资源用于将任务与外部项目（例如电子邮件、文件）连接起来。

#### 列出关联资源

```bash
GET /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}/linkedResources
```

**响应：**
```json
{
  "value": [
    {
      "id": "f9cddce2-dce2-f9cd-e2dc-cdf9e2dccdf9",
      "webUrl": "https://example.com/item",
      "applicationName": "MyApp",
      "displayName": "Related Document",
      "externalId": "external-123"
    }
  ]
}
```

#### 创建关联资源

```bash
POST /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}/linkedResources
Content-Type: application/json

{
  "webUrl": "https://example.com/item",
  "applicationName": "MyApp",
  "displayName": "Related Document",
  "externalId": "external-123"
}
```

#### 删除关联资源

```bash
DELETE /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks/{taskId}/linkedResources/{linkedResourceId}
```

成功时返回 `204 No Content`。

## 分页

Microsoft Graph 使用 OData 分页。使用 `$top` 限制结果数量，使用 `$skip` 设置偏移量：

```bash
GET /microsoft-to-do/v1.0/me/todo/lists/{todoTaskListId}/tasks?$top=10&$skip=0
```

当还有更多结果时，响应中会包含 `@odata.nextLink`：

```json
{
  "value": [...],
  "@odata.nextLink": "https://graph.microsoft.com/v1.0/me/todo/lists/{id}/tasks?$skip=10"
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/microsoft-to-do/v1.0/me/todo/lists',
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
    'https://gateway.maton.ai/microsoft-to-do/v1.0/me/todo/lists',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 任务列表 ID 和任务 ID 是不可见的字符串（例如：`AAMkADIyAAAhrbPWAAA=`）
- 时间戳默认使用 UTC 格式的 ISO 8601 格式。
- `dateTimeTimeZone` 类型需要同时包含 `dateTime` 和 `timeZone` 字段。
- `wellknownListName` 可以是 `defaultList`、`flaggedEmails` 或 `none`。
- 任务状态值：`notStarted`、`inProgress`、`completed`、`waitingOnOthers`、`deferred`。
- 任务重要性值：`low`、`normal`、`high`。
- 支持 OData 查询参数：`$select`、`$filter`、`$orderby`、`$top`、`$skip`。
- 重要提示：当 URL 包含括号时，使用 `curl -g` 可以防止全局解析。
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确扩展。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Microsoft To Do 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 请求频率受限 |
| 4xx/5xx | 来自 Microsoft Graph API 的传递错误 |

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

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `microsoft-to-do` 开头。例如：

- 正确：`https://gateway.maton.ai/microsoft-to-do/v1.0/me/todo/lists`
- 错误：`https://gateway.maton.ai/v1.0/me/todo/lists`

## 资源

- [Microsoft To Do API 概述](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview)
- [todoTaskList 资源](https://learn.microsoft.com/en-us/graph/api/resources/todotasklist)
- [todoTask 资源](https://learn.microsoft.com/en-us/graph/api/resources/todotask)
- [checklistItem 资源](https://learn.microsoft.com/en-us/graph/api/resources/checklistitem)
- [linkedResource 资源](https://learn.microsoft.com/en-us/graph/api/resources/linkedresource)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)