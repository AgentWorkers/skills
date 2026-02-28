---
name: zohoprojects
description: >
  **Zoho Projects API集成与托管式OAuth**  
  该功能支持用户管理项目、任务、里程碑、任务列表以及团队协作。当用户需要管理项目任务、记录工作时间、安排里程碑或进行团队协作时，可使用此功能。  
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
# Zoho Projects

您可以使用受管理的 OAuth 认证来访问 Zoho Projects API，从而管理项目、任务、里程碑、任务列表以及团队协作。

## 快速入门

```bash
# List all portals
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-projects/restapi/portals/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-projects/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Zoho Projects API 端点路径。该网关会将请求代理到 `projectsapi.zoho.com` 并自动插入您的 OAuth 令牌。

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

您可以在 `https://ctrl.maton.ai` 上管理您的 Zoho Projects OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-projects&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-projects'}).encode()
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
    "connection_id": "522c11a9-b879-4504-b267-355e3dbac99f",
    "status": "ACTIVE",
    "creation_time": "2026-02-28T00:12:25.223434Z",
    "last_updated_time": "2026-02-28T00:16:32.882675Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "zoho-projects",
    "metadata": {},
    "method": "OAUTH2"
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

如果您有多个 Zoho Projects 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-projects/restapi/portals/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '522c11a9-b879-4504-b267-355e3dbac99f')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 门户

#### 列出门户

```bash
GET /zoho-projects/restapi/portals/
```

**响应：**
```json
{
  "portals": [
    {
      "id": 916020774,
      "id_string": "916020774",
      "name": "nunchidotapp",
      "plan": "Ultimate",
      "role": "admin",
      "project_count": {"active": 1}
    }
  ]
}
```

#### 获取门户详细信息

```bash
GET /zoho-projects/restapi/portal/{portal_id}/
```

---

### 项目

#### 列出项目

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/
```

查询参数：`index`、`range`、`status`、`sort_column`、`sort_order`

**响应：**
```json
{
  "projects": [
    {
      "id": 2644874000000089119,
      "name": "My Project",
      "status": "active",
      "owner_name": "Byungkyu Park",
      "task_count": {"open": 3, "closed": 0},
      "project_percent": "0"
    }
  ]
}
```

#### 获取项目详细信息

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/
```

#### 创建项目

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/
Content-Type: application/x-www-form-urlencoded

name=New+Project&owner={user_id}&description=Project+description
```

必填参数：`name`
可选参数：`owner`、`description`、`start_date`、`end_date`、`template_id`、`group_id`

**响应：**
```json
{
  "projects": [
    {
      "id": 2644874000000096003,
      "name": "New Project",
      "status": "active"
    }
  ]
}
```

#### 更新项目

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/
Content-Type: application/x-www-form-urlencoded

name=Updated+Name&status=active
```

#### 删除项目

```bash
DELETE /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/
```

**响应：**
```json
{"response": "Project Trashed successfully"}
```

---

### 任务

#### 列出任务

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/
```

查询参数：`index`、`range`、`owner`、`status`、`priority`、`tasklist_id`、`sort_column`

**响应：**
```json
{
  "tasks": [
    {
      "id": 2644874000000089255,
      "name": "Task 3",
      "status": {"name": "Open", "type": "open"},
      "priority": "None",
      "completed": false,
      "tasklist": {"name": "General", "id": "2644874000000089245"}
    }
  ]
}
```

#### 获取任务详细信息

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/
```

#### 获取我的任务

```bash
GET /zoho-projects/restapi/portal/{portal_id}/mytasks/
```

查询参数：`index`、`range`、`owner`、`status`、`priority`、`projects_ids`

#### 创建任务

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/
Content-Type: application/x-www-form-urlencoded

name=New+Task&tasklist_id={tasklist_id}&priority=High
```

必填参数：`name`
可选参数：`person_responsible`、`tasklist_id`、`start_date`、`end_date`、`priority`、`description`

**响应：**
```json
{
  "tasks": [
    {
      "id": 2644874000000094001,
      "key": "EZ1-T4",
      "name": "New Task",
      "status": {"name": "Open", "type": "open"}
    }
  ]
}
```

#### 更新任务

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/
Content-Type: application/x-www-form-urlencoded

name=Updated+Name&priority=High&percent_complete=50
```

#### 删除任务

```bash
DELETE /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/
```

**响应：**
```json
{"response": "Task Trashed successfully"}
```

---

### 任务评论

#### 列出评论

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/comments/
```

#### 添加评论

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/comments/
Content-Type: application/x-www-form-urlencoded

content=This+is+a+comment
```

**响应：**
```json
{
  "comments": [
    {
      "id": 2644874000000094015,
      "content": "This is a comment",
      "added_person": "Byungkyu Park"
    }
  ]
}
```

#### 更新评论

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/comments/{comment_id}/
Content-Type: application/x-www-form-urlencoded

content=Updated+comment
```

#### 删除评论

```bash
DELETE /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/{task_id}/comments/{comment_id}/
```

---

### 任务列表

#### 列出任务列表

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasklists/
```

查询参数：`index`、`range`、`flag`、`milestone_id`、`sort_column`

**响应：**
```json
{
  "tasklists": [
    {
      "id": 2644874000000089245,
      "name": "General",
      "flag": "internal",
      "is_default": true,
      "task_count": {"open": 3}
    }
  ]
}
```

#### 创建任务列表

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasklists/
Content-Type: application/x-www-form-urlencoded

name=New+Tasklist&flag=internal
```

必填参数：`name`
可选参数：`milestone_id`、`flag`

#### 更新任务列表

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasklists/{tasklist_id}/
Content-Type: application/x-www-form-urlencoded

name=Updated+Name&milestone_id={milestone_id}
```

#### 删除任务列表

```bash
DELETE /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasklists/{tasklist_id}/
```

**响应：**
```json
{"response": "Tasklist Trashed successfully"}
```

---

### 里程碑

#### 列出里程碑

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/milestones/
```

查询参数：`index`、`range`、`status`、`flag`、`sort_column`

**注意：** 如果没有里程碑，则返回 204（表示“无内容”）。

#### 创建里程碑

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/milestones/
Content-Type: application/x-www-form-urlencoded

name=Phase+1&start_date=03-01-2026&end_date=03-15-2026&owner={user_id}&flag=internal
```

必填参数：`name`、`start_date`、`end_date`、`owner`、`flag`

**响应：**
```json
{
  "milestones": [
    {
      "id": 2644874000000096133,
      "name": "Phase 1",
      "start_date": "03-01-2026",
      "end_date": "03-15-2026",
      "status": "notcompleted"
    }
  ]
}
```

#### 更新里程碑

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/milestones/{milestone_id}/
Content-Type: application/x-www-form-urlencoded

name=Updated+Phase&start_date=03-01-2026&end_date=03-20-2026&owner={user_id}&flag=internal
```

#### 更改里程碑状态

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/milestones/{milestone_id}/status/
Content-Type: application/x-www-form-urlencoded

status=2
```

状态值：`1` = 未完成；`2` = 已完成

#### 删除里程碑

```bash
DELETE /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/milestones/{milestone_id}/
```

**响应：**
```json
{"response": "Milestone Trashed successfully"}
```

---

### 用户

#### 列出用户

```bash
GET /zoho-projects/restapi/portal/{portal_id}/users/
```

**响应：**
```json
{
  "users": [
    {
      "id": "801698114",
      "zpuid": "2644874000000085003",
      "name": "Byungkyu Park",
      "email": "byungkyu@example.com",
      "role_name": "Administrator",
      "active": true
    }
  ]
}
```

---

### 项目组

#### 列出项目组

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/groups
```

**响应：**
```json
{
  "groups": [
    {
      "id": "2644874000000018001",
      "name": "Ungrouped Projects",
      "is_default": "true"
    }
  ]
}
```

#### 创建项目组

```bash
POST /zoho-projects/restapi/portal/{portal_id}/projectgroups
Content-Type: application/x-www-form-urlencoded

name=New+Group
```

---

## 分页

使用 `index` 和 `range` 参数进行分页：

```bash
GET /zoho-projects/restapi/portal/{portal_id}/projects/{project_id}/tasks/?index=1&range=50
```

- `index`：起始记录编号（从 1 开始）
- `range`：要返回的记录数量

## 代码示例

### JavaScript

```javascript
// List tasks in a project
const response = await fetch(
  'https://gateway.maton.ai/zoho-projects/restapi/portal/916020774/projects/2644874000000089119/tasks/',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.tasks);
```

### Python

```python
import os
import requests

# Create a task
response = requests.post(
    'https://gateway.maton.ai/zoho-projects/restapi/portal/916020774/projects/2644874000000089119/tasks/',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    data={'name': 'New Task', 'priority': 'High'}
)
task = response.json()
print(task['tasks'][0]['id'])
```

## 注意事项

- 所有用于创建/更新的 POST 请求都应使用 `application/x-www-form-urlencoded` 内容类型，而不是 JSON。
- 大多数端点都需要门户 ID，您可以通过 `GET /restapi/portals/` 获取该 ID。
- 日期格式为 `MM-dd-yyyy`（例如：`03-01-2026`）。
- 创建里程碑时需要填写所有字段：`name`、`start_date`、`end_date`、`owner`、`flag`。
- 空列表的响应会返回 HTTP 204（表示“无内容”）。
- 被删除的项目会被移至“回收站”，而不是被永久删除。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 204 | 无内容（列表为空） |
| 400 | 输入参数缺失/无效 |
| 401 | Maton API 密钥无效或缺失 |
| 404 | 资源未找到 |
| 429 | 每 2 分钟请求次数限制（100 次） |
| 4xx/5xx | 来自 Zoho Projects API 的传递错误 |

常见错误代码：
- `6831`：输入参数缺失
- `6832`：输入参数不符合指定格式

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

确保您的 URL 路径以 `zoho-projects` 开头。例如：

- 正确的路径：`https://gateway.maton.ai/zoho-projects/restapi/portals/`
- 错误的路径：`https://gateway.maton.ai/restapi/portals/`

## 资源

- [Zoho Projects API 文档](https://www.zoho.com/projects/help/rest-api/zohoprojectsapi.html)
- [项目 API](https://www.zoho.com/projects/help/rest-api/projects-api.html)
- [任务 API](https://www.zoho.com/projects/help/rest-api/tasks-api.html)
- [里程碑 API](https://www.zoho.com/projects/help/rest-api/milestones-api.html)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)