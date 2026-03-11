---
name: wrike
description: >
  **Wrike API集成与托管式OAuth**  
  支持管理任务、文件夹、项目以及团队协作功能。当用户需要管理项目工作、跟踪任务进度、处理时间记录或访问Wrike中的团队资源时，可使用此技能。对于其他第三方应用程序，建议使用`api-gateway`技能（https://clawhub.ai/byungkyu/api-gateway）。  
  **使用要求：**  
  - 需要网络连接；  
  - 拥有有效的Maton API密钥。
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
# Wrike

通过管理的OAuth认证访问Wrike API v4。您可以管理任务、文件夹、项目、工作空间、组、评论、附件、时间日志、工作流等。

## 快速入门

```bash
# List all tasks
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/wrike/api/v4/tasks')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/wrike/api/v4/{endpoint-path}
```

请将 `{endpoint-path}` 替换为实际的Wrike API端点路径。该代理会将请求转发到 `www.wrike.com/api/v4` 并自动插入您的OAuth令牌。

## 认证

所有请求都需要在 `Authorization` 头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Wrike OAuth连接。

### 列出连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=wrike&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'wrike'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection_id": "32c76f2f-54a0-47ca-b4d2-8e99ad852210",
  "status": "PENDING",
  "url": "https://connect.maton.ai/?session_token=...",
  "app": "wrike"
}
```

在浏览器中打开返回的 `url` 以完成OAuth授权。

### 删除连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
urllib.request.urlopen(req)
print("Deleted")
EOF
```

### 指定连接

如果您有多个Wrike连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```python
req.add_header('Maton-Connection', '{connection_id}')
```

如果省略，则代理将使用默认的（最旧的）活动连接。

## API参考

### 工作空间

#### 列出工作空间

```bash
GET /wrike/api/v4/spaces
```

**响应：**
```json
{
  "kind": "spaces",
  "data": [
    {
      "id": "MQAAAAEFzzdO",
      "title": "First space",
      "avatarUrl": "https://www.wrike.com/static/spaceicons2/v3/6/6-planet.png",
      "accessType": "Public",
      "archived": false,
      "defaultProjectWorkflowId": "IEAGXR2EK77ZIOF4",
      "defaultTaskWorkflowId": "IEAGXR2EK4G2YNU4"
    }
  ]
}
```

#### 获取工作空间信息

```bash
GET /wrike/api/v4/spaces/{spaceId}
```

#### 创建工作空间

```bash
POST /wrike/api/v4/spaces
Content-Type: application/json

{
  "title": "New Space"
}
```

#### 更新工作空间

```bash
PUT /wrike/api/v4/spaces/{spaceId}
Content-Type: application/json

{
  "title": "Updated Space Name"
}
```

#### 删除工作空间

```bash
DELETE /wrike/api/v4/spaces/{spaceId}
```

### 文件夹与项目

文件夹和项目是Wrike中组织工作的主要方式。项目是具有额外属性（所有者、日期、状态）的文件夹。

#### 获取文件夹树

```bash
GET /wrike/api/v4/folders
```

**响应：**
```json
{
  "kind": "folderTree",
  "data": [
    {
      "id": "IEAGXR2EI7777777",
      "title": "Root",
      "childIds": ["MQAAAAEFzzdO", "MQAAAAEFzzRZ"],
      "scope": "WsRoot"
    },
    {
      "id": "MQAAAAEFzzdV",
      "title": "My Project",
      "childIds": [],
      "scope": "WsFolder",
      "project": {
        "authorId": "KUAXHKXS",
        "ownerIds": ["KUAXHKXS"],
        "customStatusId": "IEAGXR2EJMG2YNA4",
        "createdDate": "2026-03-09T08:15:07Z"
      }
    }
  ]
}
```

#### 获取工作空间中的文件夹

```bash
GET /wrike/api/v4/spaces/{spaceId}/folders
```

#### 获取文件夹信息

```bash
GET /wrike/api/v4/folders/{folderId}
GET /wrike/api/v4/folders/{folderId},{folderId},... (up to 100 IDs)
```

#### 获取子文件夹

```bash
GET /wrike/api/v4/folders/{folderId}/folders
```

#### 创建文件夹

```bash
POST /wrike/api/v4/folders/{parentFolderId}/folders
Content-Type: application/json

{
  "title": "New Folder"
}
```

#### 更新文件夹

```bash
PUT /wrike/api/v4/folders/{folderId}
Content-Type: application/json

{
  "title": "Updated Folder Name"
}
```

#### 删除文件夹

```bash
DELETE /wrike/api/v4/folders/{folderId}
```

#### 复制文件夹

```bash
POST /wrike/api/v4/copy_folder/{folderId}
Content-Type: application/json

{
  "parent": "{destinationFolderId}",
  "title": "Copy of Folder"
}
```

### 任务

#### 列出任务

```bash
GET /wrike/api/v4/tasks
```

**响应：**
```json
{
  "kind": "tasks",
  "data": [
    {
      "id": "MAAAAAEFzzde",
      "accountId": "IEAGXR2E",
      "title": "First task",
      "status": "Active",
      "importance": "Normal",
      "createdDate": "2026-03-09T08:15:07Z",
      "updatedDate": "2026-03-10T07:07:57Z",
      "dates": {
        "type": "Planned",
        "duration": 2400,
        "start": "2026-03-05T09:00:00",
        "due": "2026-03-11T17:00:00"
      },
      "scope": "WsTask",
      "customStatusId": "IEAGXR2EJMG2YNV2",
      "permalink": "https://www.wrike.com/open.htm?id=4392433502"
    }
  ]
}
```

#### 获取文件夹中的任务列表

```bash
GET /wrike/api/v4/folders/{folderId}/tasks
```

#### 获取工作空间中的任务列表

```bash
GET /wrike/api/v4/spaces/{spaceId}/tasks
```

#### 获取任务信息

```bash
GET /wrike/api/v4/tasks/{taskId}
GET /wrike/api/v4/tasks/{taskId},{taskId},... (up to 100 IDs)
```

#### 创建任务

```bash
POST /wrike/api/v4/folders/{folderId}/tasks
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task description",
  "importance": "Normal",
  "dates": {
    "start": "2026-03-15",
    "due": "2026-03-20"
  }
}
```

**响应：**
```json
{
  "kind": "tasks",
  "data": [
    {
      "id": "MAAAAAEF7ufN",
      "accountId": "IEAGXR2E",
      "title": "New Task",
      "description": "Task description",
      "status": "Active",
      "importance": "Normal",
      "createdDate": "2026-03-10T07:16:07Z",
      "scope": "WsTask",
      "customStatusId": "IEAGXR2EJMG2YNU4",
      "permalink": "https://www.wrike.com/open.htm?id=4394510285"
    }
  ]
}
```

#### 更新任务

```bash
PUT /wrike/api/v4/tasks/{taskId}
Content-Type: application/json

{
  "title": "Updated Task Title",
  "importance": "High"
}
```

#### 同时更新多个任务

```bash
PUT /wrike/api/v4/tasks/{taskId},{taskId},... (up to 100 IDs)
Content-Type: application/json

{
  "status": "Completed"
}
```

#### 删除任务

```bash
DELETE /wrike/api/v4/tasks/{taskId}
```

### 评论

#### 列出评论

```bash
GET /wrike/api/v4/comments
GET /wrike/api/v4/tasks/{taskId}/comments
GET /wrike/api/v4/folders/{folderId}/comments
GET /wrike/api/v4/comments/{commentId},{commentId},... (up to 100 IDs)
```

**响应：**
```json
{
  "kind": "comments",
  "data": [
    {
      "id": "IEAGXR2EIMBGYQMR",
      "authorId": "KUAXI4LC",
      "text": "This is a comment",
      "updatedDate": "2026-03-10T07:07:57Z",
      "createdDate": "2026-03-10T07:07:57Z",
      "taskId": "MAAAAAEFzzde"
    }
  ]
}
```

#### 创建评论

```bash
POST /wrike/api/v4/tasks/{taskId}/comments
Content-Type: application/json

{
  "text": "New comment text"
}
```

#### 更新评论

```bash
PUT /wrike/api/v4/comments/{commentId}
Content-Type: application/json

{
  "text": "Updated comment text"
}
```

#### 删除评论

```bash
DELETE /wrike/api/v4/comments/{commentId}
```

### 附件

#### 列出附件

```bash
GET /wrike/api/v4/attachments
GET /wrike/api/v4/tasks/{taskId}/attachments
GET /wrike/api/v4/folders/{folderId}/attachments
GET /wrike/api/v4/attachments/{attachmentId},{attachmentId},... (up to 100 IDs)
```

**响应：**
```json
{
  "kind": "attachments",
  "data": [
    {
      "id": "IEAGXR2EIYUN54ZV",
      "authorId": "KUAXHKXS",
      "name": "document.pdf",
      "createdDate": "2026-03-09T08:15:08Z",
      "version": 1,
      "type": "Wrike",
      "contentType": "application/pdf",
      "size": 117940,
      "taskId": "MAAAAAEFzzde"
    }
  ]
}
```

#### 下载附件

```bash
GET /wrike/api/v4/attachments/{attachmentId}/download
```

#### 获取附件预览

```bash
GET /wrike/api/v4/attachments/{attachmentId}/preview
```

#### 获取附件访问URL

```bash
GET /wrike/api/v4/attachments/{attachmentId}/url
```

#### 更新附件

```bash
PUT /wrike/api/v4/attachments/{attachmentId}
```

#### 删除附件

```bash
DELETE /wrike/api/v4/attachments/{attachmentId}
```

### 联系人

联系人代表Wrike中的用户和组。

#### 列出联系人

```bash
GET /wrike/api/v4/contacts
GET /wrike/api/v4/contacts/{contactId},{contactId},... (up to 100 IDs)
```

**响应：**
```json
{
  "kind": "contacts",
  "data": [
    {
      "id": "KUAXHKXS",
      "firstName": "Chris",
      "lastName": "",
      "type": "Person",
      "profiles": [
        {
          "accountId": "IEAGXR2E",
          "email": "user@example.com",
          "role": "User",
          "external": false,
          "admin": false,
          "owner": true,
          "active": true
        }
      ],
      "timezone": "US/Pacific",
      "locale": "en",
      "deleted": false,
      "me": true
    }
  ]
}
```

#### 更新联系人信息

```bash
PUT /wrike/api/v4/contacts/{contactId}
Content-Type: application/json

{
  "metadata": [{"key": "customKey", "value": "customValue"}]
}
```

### 组

#### 列出组

```bash
GET /wrike/api/v4/groups
GET /wrike/api/v4/groups/{groupId}
```

**响应：**
```json
{
  "kind": "groups",
  "data": [
    {
      "id": "KX7XIKVN",
      "accountId": "IEAGXR2E",
      "title": "My Team",
      "memberIds": ["KUAXHKXS"],
      "childIds": [],
      "parentIds": [],
      "myTeam": true
    }
  ]
}
```

#### 创建组

```bash
POST /wrike/api/v4/groups
Content-Type: application/json

{
  "title": "New Group",
  "members": ["KUAXHKXS"]
}
```

#### 更新组

```bash
PUT /wrike/api/v4/groups/{groupId}
Content-Type: application/json

{
  "title": "Updated Group Name"
}
```

#### 删除组

```bash
DELETE /wrike/api/v4/groups/{groupId}
```

### 工作流

#### 列出工作流

```bash
GET /wrike/api/v4/workflows
GET /wrike/api/v4/spaces/{spaceId}/workflows
```

**响应：**
```json
{
  "kind": "workflows",
  "data": [
    {
      "id": "IEAGXR2EK77ZIOF4",
      "name": "Default Workflow",
      "standard": true,
      "hidden": false,
      "customStatuses": [
        {
          "id": "IEAGXR2EJMAAAAAA",
          "name": "New",
          "color": "Blue",
          "group": "Active",
          "hidden": false
        },
        {
          "id": "IEAGXR2EJMG2YNA4",
          "name": "In Progress",
          "color": "Turquoise",
          "group": "Active",
          "hidden": false
        },
        {
          "id": "IEAGXR2EJMAAAAAB",
          "name": "Completed",
          "color": "Green",
          "group": "Completed",
          "hidden": false
        }
      ]
    }
  ]
}
```

#### 创建工作流

```bash
POST /wrike/api/v4/workflows
Content-Type: application/json

{
  "name": "Custom Workflow"
}
```

#### 更新工作流

```bash
PUT /wrike/api/v4/workflows/{workflowId}
Content-Type: application/json

{
  "name": "Updated Workflow Name"
}
```

### 自定义字段

#### 列出自定义字段

```bash
GET /wrike/api/v4/customfields
GET /wrike/api/v4/spaces/{spaceId}/customfields
GET /wrike/api/v4/customfields/{customfieldId},{customfieldId},... (up to 100 IDs)
```

**响应：**
```json
{
  "kind": "customfields",
  "data": [
    {
      "id": "IEAGXR2EJUALBS23",
      "accountId": "IEAGXR2E",
      "title": "Impact",
      "type": "DropDown",
      "spaceId": "MQAAAAEFzzdO",
      "settings": {
        "values": ["Low", "Medium", "High"],
        "options": [
          {"value": "Low", "color": "Green"},
          {"value": "Medium", "color": "Yellow"},
          {"value": "High", "color": "Red"}
        ]
      }
    }
  ]
}
```

#### 创建自定义字段

```bash
POST /wrike/api/v4/customfields
Content-Type: application/json

{
  "title": "Priority",
  "type": "DropDown",
  "settings": {
    "values": ["Low", "Medium", "High"]
  }
}
```

#### 更新自定义字段

```bash
PUT /wrike/api/v4/customfields/{customfieldId}
Content-Type: application/json

{
  "title": "Updated Field Name"
}
```

### 时间日志

#### 列出时间日志

```bash
GET /wrike/api/v4/timelogs
GET /wrike/api/v4/tasks/{taskId}/timelogs
GET /wrike/api/v4/folders/{folderId}/timelogs
GET /wrike/api/v4/contacts/{contactId}/timelogs
GET /wrike/api/v4/timelogs/{timelogId},{timelogId},... (up to 100 IDs)
```

#### 创建时间日志

```bash
POST /wrike/api/v4/tasks/{taskId}/timelogs
Content-Type: application/json

{
  "hours": 2,
  "trackedDate": "2026-03-10",
  "comment": "Worked on implementation"
}
```

#### 更新时间日志

```bash
PUT /wrike/api/v4/timelogs/{timelogId}
Content-Type: application/json

{
  "hours": 3,
  "comment": "Updated time entry"
}
```

#### 删除时间日志

```bash
DELETE /wrike/api/v4/timelogs/{timelogId}
```

### 时间日志类别

```bash
GET /wrike/api/v4/timelog_categories
```

### 依赖关系

#### 列出依赖关系

```bash
GET /wrike/api/v4/tasks/{taskId}/dependencies
GET /wrike/api/v4/dependencies/{dependencyId},{dependencyId},... (up to 100 IDs)
```

**响应：**
```json
{
  "kind": "dependencies",
  "data": [
    {
      "id": "MgAAAAEFzzdeMwAAAAEFzzdb",
      "predecessorId": "MAAAAAEFzzde",
      "successorId": "MAAAAAEFzzdb",
      "relationType": "FinishToStart",
      "lagTime": 0
    }
  ]
}
```

#### 创建依赖关系

```bash
POST /wrike/api/v4/tasks/{taskId}/dependencies
Content-Type: application/json

{
  "predecessorId": "{taskId}",
  "relationType": "FinishToStart"
}
```

#### 更新依赖关系

```bash
PUT /wrike/api/v4/dependencies/{dependencyId}
Content-Type: application/json

{
  "relationType": "StartToStart"
}
```

#### 删除依赖关系

```bash
DELETE /wrike/api/v4/dependencies/{dependencyId}
```

### 审批

#### 列出审批记录

```bash
GET /wrike/api/v4/approvals
GET /wrike/api/v4/tasks/{taskId}/approvals
GET /wrike/api/v4/folders/{folderId}/approvals
GET /wrike/api/v4/approvals/{approvalId},{approvalId},... (up to 100 IDs)
```

**响应：**
```json
{
  "kind": "approvals",
  "data": [
    {
      "id": "IEAGXR2EMEB33OQA",
      "taskId": "MAAAAAEFzzde",
      "authorId": "KUAXHKXS",
      "dueDate": "2026-03-12",
      "decisions": [
        {
          "approverId": "KUAXHKXS",
          "status": "Pending",
          "updatedDate": "2026-03-09T08:15:08Z"
        }
      ],
      "status": "Pending",
      "finished": false
    }
  ]
}
```

#### 创建审批记录

```bash
POST /wrike/api/v4/tasks/{taskId}/approvals
Content-Type: application/json

{
  "approvers": ["KUAXHKXS"],
  "dueDate": "2026-03-15"
}
```

#### 更新审批记录

```bash
PUT /wrike/api/v4/approvals/{approvalId}
```

#### 取消审批

```bash
DELETE /wrike/api/v4/approvals/{approvalId}
```

### 邀请

#### 列出邀请记录

```bash
GET /wrike/api/v4/invitations
```

**响应：**
```json
{
  "kind": "invitations",
  "data": [
    {
      "id": "IEAGXR2EJEAVFLCG",
      "accountId": "IEAGXR2E",
      "firstName": "John",
      "email": "john@example.com",
      "status": "Accepted",
      "inviterUserId": "KUAXHKXS",
      "invitationDate": "2026-03-09T08:14:04Z",
      "role": "User",
      "external": false
    }
  ]
}
```

#### 创建邀请

```bash
POST /wrike/api/v4/invitations
Content-Type: application/json

{
  "email": "newuser@example.com",
  "firstName": "New",
  "lastName": "User",
  "role": "User"
}
```

#### 更新邀请

```bash
PUT /wrike/api/v4/invitations/{invitationId}
```

#### 删除邀请

```bash
DELETE /wrike/api/v4/invitations/{invitationId}
```

### 工作计划

#### 列出工作计划

```bash
GET /wrike/api/v4/workschedules
GET /wrike/api/v4/workschedules/{workscheduleId}
```

**响应：**
```json
{
  "kind": "workschedules",
  "data": [
    {
      "id": "IEAGXR2EML7ZIOF4",
      "scheduleType": "Default",
      "title": "Default Schedule",
      "workweek": [
        {
          "workDays": ["Mon", "Tue", "Wed", "Thu", "Fri"],
          "capacityMinutes": 480
        }
      ]
    }
  ]
}
```

#### 创建工作计划

```bash
POST /wrike/api/v4/workschedules
Content-Type: application/json

{
  "title": "Custom Schedule"
}
```

#### 更新工作计划

```bash
PUT /wrike/api/v4/workschedules/{workscheduleId}
```

#### 删除工作计划

```bash
DELETE /wrike/api/v4/workschedules/{workscheduleId}
```

### 用户（管理员）

#### 获取用户信息

```bash
GET /wrike/api/v4/users/{userId}
```

**响应：**
```json
{
  "kind": "users",
  "data": [
    {
      "id": "KUAXHKXS",
      "firstName": "Chris",
      "lastName": "",
      "type": "Person",
      "profiles": [
        {
          "accountId": "IEAGXR2E",
          "email": "user@example.com",
          "role": "User",
          "external": false,
          "admin": false,
          "owner": true,
          "active": true
        }
      ],
      "timezone": "US/Pacific",
      "locale": "en",
      "deleted": false,
      "me": true,
      "title": "Engineer",
      "companyName": "Company",
      "primaryEmail": "user@example.com",
      "userTypeId": "IEAGXR2ENH777777"
    }
  ]
}
```

#### 更新用户信息

```bash
PUT /wrike/api/v4/users/{userId}
PUT /wrike/api/v4/users/{userId},{userId},... (up to 100 IDs)
```

### 访问权限（管理员）

#### 列出访问权限

```bash
GET /wrike/api/v4/access_roles
```

**响应：**
```json
{
  "kind": "accessRoles",
  "data": [
    {
      "id": "IEAGXR2END777777",
      "title": "Full",
      "description": "Can edit"
    },
    {
      "id": "IEAGXR2END777776",
      "title": "Editor",
      "description": "Can edit, but can't share or delete"
    },
    {
      "id": "IEAGXR2END777775",
      "title": "Limited",
      "description": "Can comment, change statuses, attach files, and start approvals"
    },
    {
      "id": "IEAGXR2END777774",
      "title": "Read Only",
      "description": "Can view"
    }
  ]
}
```

### 审计日志（管理员）

#### 获取审计日志

```bash
GET /wrike/api/v4/audit_log
```

**响应：**
```json
{
  "kind": "auditLog",
  "data": [
    {
      "id": "IEAGXR2ENQAAAAABMUI3U3A",
      "operation": "UserLoggedIn",
      "userId": "KUAXHKXS",
      "userEmail": "user@example.com",
      "eventDate": "2026-03-10T07:24:24Z",
      "ipAddress": "35.84.133.252",
      "objectType": "User",
      "objectName": "user@example.com",
      "objectId": "KUAXHKXS",
      "details": {
        "Login Type": "Oauth2",
        "User Agent": "Nango"
      }
    }
  ]
}
```

**常见操作：**
- `UserLoggedIn` - 用户登录事件
- `Oauth2AccessGranted` - OAuth授权事件
- `TaskCreated`, `TaskDeleted`, `TaskModified` - 任务操作
- `FolderCreated`, `FolderDeleted` - 文件夹操作
- `CommentAdded` - 评论操作

### 数据导出（管理员）

#### 获取数据导出

```bash
GET /wrike/api/v4/data_export
GET /wrike/api/v4/data_export/{data_exportId}
```

首次请求时返回202（导出生成开始）。后续请求将返回每日更新的导出数据。

#### 刷新数据导出

```bash
POST /wrike/api/v4/data_export
```

触发新的数据导出刷新。

#### 获取数据导出模式

```bash
GET /wrike/api/v4/data_export_schema
```

检索导出表的模式文档。

## 响应格式

所有Wrike API响应都遵循标准化的JSON结构：

```json
{
  "kind": "[resource_type]",
  "data": [...]
}
```

## 分页

某些端点支持使用 `nextPageToken` 进行分页：

```json
{
  "kind": "timelogs",
  "nextPageToken": "AFZ2V4QAAAAA6AAAAAAAAAAAAAAAAAAA22NEEX6HNLKBU",
  "responseSize": 100,
  "data": [...]
}
```

在后续请求中使用 `pageToken` 参数：

```bash
GET /wrike/api/v4/timelogs?pageToken={nextPageToken}
```

## 代码示例

### JavaScript

```javascript
async function listTasks() {
  const response = await fetch(
    'https://gateway.maton.ai/wrike/api/v4/tasks',
    {
      headers: {
        'Authorization': `Bearer ${process.env.MATON_API_KEY}`
      }
    }
  );
  return await response.json();
}

async function createTask(folderId, title) {
  const response = await fetch(
    `https://gateway.maton.ai/wrike/api/v4/folders/${folderId}/tasks`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ title })
    }
  );
  return await response.json();
}
```

### Python

```python
import os
import json
import urllib.request

def list_tasks():
    url = 'https://gateway.maton.ai/wrike/api/v4/tasks'
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    return json.load(urllib.request.urlopen(req))

def create_task(folder_id, title):
    url = f'https://gateway.maton.ai/wrike/api/v4/folders/{folder_id}/tasks'
    data = json.dumps({'title': title}).encode()
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    req.add_header('Content-Type', 'application/json')
    return json.load(urllib.request.urlopen(req))
```

## 注意事项

- **批量操作**：许多端点支持在单个请求中传递最多100个ID（用逗号分隔）。
- **自定义状态ID**：任务使用 `customStatusId` 来引用工作流状态。
- **项目与文件夹**：项目是具有额外属性（所有者、日期、状态）的文件夹。
- **重要提示**：当使用包含括号的URL的curl命令时，请使用 `curl -g` 以禁用全局解析。
- **重要提示**：当将curl输出传递给 `jq` 时，某些shell环境中环境变量可能无法正确扩展。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求错误或参数无效 |
| 401 | API密钥无效或缺失 |
| 403 | 权限不足 |
| 404 | 资源未找到 |
| 429 | 请求次数限制 |
| 4xx/5xx | 来自Wrike API的传递错误 |

## 资源

- [Wrike API文档](https://developers.wrike.com/)
- [Wrike API概述](https://developers.wrike.com/overview/)
- [OAuth 2.0授权](https://developers.wrike.com/oauth-20-authorization/)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)