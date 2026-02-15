---
name: motion
description: |
  Motion API integration with managed OAuth. Manage tasks, projects, workspaces, and more with AI-powered scheduling.
  Use this skill when users want to create, update, or manage tasks and projects in Motion, or query their scheduled work.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
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

# Motion

您可以使用受管理的 OAuth 认证来访问 Motion API。该 API 支持对任务、项目、工作空间、评论以及重复性任务进行完整的创建（Create）、读取（Read）、更新（Update）和删除（Delete, CRUD）操作。

## 快速入门

```bash
# List tasks
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/motion/v1/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/motion/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Motion API 端点路径。该网关会将请求代理到 `api.usemotion.com`，并自动注入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Motion OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=motion&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'motion'}).encode()
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
    "app": "motion",
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

如果您有多个 Motion 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/motion/v1/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头，网关将使用默认的（最旧的）活动连接。

## API 参考

### 任务操作

#### 列出任务

```bash
GET /motion/v1/tasks
```

**查询参数：**
- `workspaceId` (string) - 按工作空间过滤
- `projectId` (string) - 按项目过滤
- `assigneeId` (string) - 按分配者过滤
- `status` (array) - 按状态过滤（不能与 `includeAllStatuses` 同时使用）
- `includeAllStatuses` (boolean) - 返回所有状态的任务
- `label` (string) - 按标签过滤
- `name` (string) - 搜索任务名称（不区分大小写）
- `cursor` (string) - 分页游标

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/motion/v1/tasks?workspaceId=WORKSPACE_ID')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 获取任务信息

```bash
GET /motion/v1/tasks/{taskId}
```

#### 创建任务

```bash
POST /motion/v1/tasks
Content-Type: application/json

{
  "name": "Task name",
  "workspaceId": "WORKSPACE_ID",
  "dueDate": "2024-03-15T10:00:00Z",
  "duration": 60,
  "priority": "HIGH",
  "description": "Task description in markdown",
  "projectId": "PROJECT_ID",
  "assigneeId": "USER_ID",
  "labels": ["label1", "label2"],
  "autoScheduled": {
    "startDate": "2024-03-14T09:00:00Z",
    "deadlineType": "SOFT",
    "schedule": "Work Hours"
  }
}
```

**必填字段：**
- `name` (string) - 任务名称
- `workspaceId` (string) - 工作空间 ID

**可选字段：**
- `dueDate` (datetime, ISO 8601) - 任务截止日期（计划任务必填）
- `duration` (string | number) - “NONE”, “REMINDER” 或分钟数（整数 > 0）
- `status` (string) - 默认为工作空间的默认状态
- `projectId` (string) - 关联的项目
- `description` (string) - 支持 GitHub 格式的 Markdown
- `priority` (string) - ASAP, HIGH, MEDIUM, 或 LOW
- `labels` (array) - 要添加的标签名称
- `assigneeId` (string) - 任务分配的用户 ID
- `autoScheduled` (object) - 自动调度设置，包含 `startDate`, `deadlineType` (HARD, SOFT, NONE) 和 `schedule`

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    'name': 'New task',
    'workspaceId': 'WORKSPACE_ID',
    'priority': 'HIGH',
    'duration': 30
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/motion/v1/tasks', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 更新任务

```bash
PATCH /motion/v1/tasks/{taskId}
Content-Type: application/json

{
  "name": "Updated task name",
  "status": "Completed",
  "priority": "LOW"
}
```

#### 删除任务

```bash
DELETE /motion/v1/tasks/{taskId}
```

#### 移动任务

```bash
POST /motion/v1/tasks/{taskId}/move
Content-Type: application/json

{
  "workspaceId": "NEW_WORKSPACE_ID"
}
```

#### 解除任务分配

```bash
POST /motion/v1/tasks/{taskId}/unassign
```

### 项目操作

#### 列出项目

```bash
GET /motion/v1/projects?workspaceId={workspaceId}
```

**查询参数：**
- `workspaceId` (string, **必填**) - 工作空间 ID
- `cursor` (string) - 分页游标

#### 获取项目信息

```bash
GET /motion/v1/projects/{projectId}
```

#### 创建项目

```bash
POST /motion/v1/projects
Content-Type: application/json

{
  "name": "Project name",
  "workspaceId": "WORKSPACE_ID",
  "description": "Project description",
  "dueDate": "2024-06-30T00:00:00Z",
  "priority": "HIGH",
  "labels": ["label1"]
}
```

**必填字段：**
- `name` (string) - 项目名称
- `workspaceId` (string) - 工作空间 ID

**可选字段：**
- `dueDate` (datetime, ISO 8601) - 项目截止日期
- `description` (string) - 支持 HTML 输入
- `labels` (array) - 标签名称
- `priority` (string) - ASAP, HIGH, MEDIUM (默认), 或 LOW
- `projectDefinitionId` (string) - 模板 ID（如果提供 `stages` 数组则必需）
- `stages` (array) - 项目模板的阶段对象

### 工作空间操作

#### 列出工作空间

```bash
GET /motion/v1/workspaces
```

### 用户操作

#### 列出用户

```bash
GET /motion/v1/users?workspaceId={workspaceId}
```

**查询参数：**
- `workspaceId` (string) - 工作空间 ID（如果没有 `teamId` 则必填）
- `teamId` (string) - 团队 ID（如果没有 `workspaceId` 则必填）

注意：您必须提供 `workspaceId` 或 `teamId`。

#### 获取当前用户

```bash
GET /motion/v1/users/me
```

### 评论操作

#### 列出评论

```bash
GET /motion/v1/comments?taskId={taskId}
```

**查询参数：**
- `taskId` (string, **必填**) - 按任务过滤评论
- `cursor` (string) - 分页游标

#### 创建评论

```bash
POST /motion/v1/comments
Content-Type: application/json

{
  "taskId": "TASK_ID",
  "content": "Comment in GitHub Flavored Markdown"
}
```

**必填字段：**
- `taskId` (string) - 要评论的任务 ID

**可选字段：**
- `content` (string) - 评论内容（支持 GitHub 格式的 Markdown）

### 重复性任务操作

#### 列出重复性任务

```bash
GET /motion/v1/recurring-tasks?workspaceId={workspaceId}
```

**查询参数：**
- `workspaceId` (string, **必填**) - 按工作空间过滤
- `cursor` (string) - 分页游标

#### 创建重复性任务

```bash
POST /motion/v1/recurring-tasks
Content-Type: application/json

{
  "name": "Weekly review",
  "workspaceId": "WORKSPACE_ID",
  "frequency": "weekly"
}
```

#### 删除重复性任务

```bash
DELETE /motion/v1/recurring-tasks/{recurringTaskId}
```

### 日程操作

#### 列出日程安排

```bash
GET /motion/v1/schedules
```

### 状态操作

#### 列出状态

```bash
GET /motion/v1/statuses?workspaceId={workspaceId}
```

**查询参数：**
- `workspaceId` (string, **必填**) - 按工作空间过滤

### 自定义字段操作

#### 列出自定义字段

```bash
GET /motion/v1/custom-fields
```

#### 创建自定义字段

```bash
POST /motion/v1/custom-fields
Content-Type: application/json

{
  "name": "Field name",
  "type": "text"
}
```

#### 删除自定义字段

```bash
DELETE /motion/v1/custom-fields/{customFieldId}
```

#### 向项目添加自定义字段

```bash
POST /motion/v1/custom-fields/{customFieldId}/project
Content-Type: application/json

{
  "projectId": "PROJECT_ID"
}
```

#### 向任务添加自定义字段

```bash
POST /motion/v1/custom-fields/{customFieldId}/task
Content-Type: application/json

{
  "taskId": "TASK_ID"
}
```

#### 从项目中删除自定义字段

```bash
DELETE /motion/v1/custom-fields/{customFieldId}/project
```

#### 从任务中删除自定义字段

```bash
DELETE /motion/v1/custom-fields/{customFieldId}/task
```

## 分页

Motion 使用基于游标的分页机制：

```bash
GET /motion/v1/tasks?cursor=CURSOR_VALUE
```

响应中包含分页元数据：

```json
{
  "tasks": [...],
  "meta": {
    "nextCursor": "abc123",
    "pageSize": 20
  }
}
```

在后续请求中使用 `nextCursor` 值来获取更多结果。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/motion/v1/tasks',
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
    'https://gateway.maton.ai/motion/v1/tasks',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

## 注意事项

- 所有时间戳均使用 ISO 8601 格式。
- 任务描述支持 GitHub 格式的 Markdown。
- 项目描述支持 HTML 输入。
- 优先级值：ASAP, HIGH, MEDIUM, LOW。
- 自动调度的截止日期类型：HARD, SOFT, NONE。
- 请求速率限制：个人用户 12 次/分钟，团队用户 120 次/分钟。
- 重要提示：当使用 `curl` 命令时，如果 URL 中包含括号，请使用 `curl -g` 以禁用全局解析。
- 重要提示：当将 `curl` 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未建立 Motion 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 请求速率受限 |
| 4xx/5xx | 来自 Motion API 的传递错误 |

## 资源

- [Motion API 文档](https://docs.usemotion.com/)
- [Motion API 参考](https://docs.usemotion.com/api-reference)
- [Motion 使用指南](https://docs.usemotion.com/cookbooks/getting-started)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)