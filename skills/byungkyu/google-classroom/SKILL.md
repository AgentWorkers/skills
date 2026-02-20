---
name: google-classroom
description: >
  **Google Classroom API集成与托管的OAuth认证**  
  支持管理课程、作业、学生、教师以及公告功能。  
  当用户需要创建课程、管理作业、跟踪学生提交情况或发布公告时，可使用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。  
  该功能需要网络连接以及有效的Maton API密钥。
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
# Google Classroom

您可以使用托管的 OAuth 认证来访问 Google Classroom API。该 API 允许您管理课程、课程作业、学生、教师、公告以及学生的提交内容。

## 快速入门

```bash
# List all courses
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-classroom/v1/courses')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/google-classroom/{api-path}
```

Google Classroom API 使用以下路径模式：
```
https://gateway.maton.ai/google-classroom/v1/{resource}
```

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
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 Google Classroom OAuth 连接。

### 列出连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-classroom&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python3 <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'google-classroom'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python3 <<'EOF'
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
    "connection_id": "8efa1361-0e86-40b1-a63b-53a5051f8ac6",
    "status": "ACTIVE",
    "creation_time": "2026-02-14T00:00:00.000000Z",
    "last_updated_time": "2026-02-14T00:00:00.000000Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "google-classroom",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 Google Classroom 连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python3 <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-classroom/v1/courses')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '8efa1361-0e86-40b1-a63b-53a5051f8ac6')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略该头部，系统将使用默认的（最旧的）活动连接。

## API 参考

### 课程

#### 列出课程

```bash
GET /v1/courses
GET /v1/courses?courseStates=ACTIVE
GET /v1/courses?teacherId=me
GET /v1/courses?studentId=me
GET /v1/courses?pageSize=10
```

**查询参数：**
- `courseStates` - 按状态过滤：`ACTIVE`（活动）、`ARCHIVED`（已归档）、`PROVISIONED`（已提供）、`DECLINED`（被拒绝）、`SUSPENDED`（暂停）
- `teacherId` - 按教师 ID 过滤（使用 `me` 表示当前用户）
- `studentId` - 按学生 ID 过滤（使用 `me` 表示当前用户）
- `pageSize` - 每页显示的结果数量（最多 100 个）
- `pageToken` - 下一页的令牌

**响应：**
```json
{
  "courses": [
    {
      "id": "825635865485",
      "name": "Introduction to Programming",
      "section": "Section A",
      "descriptionHeading": "CS 101",
      "description": "Learn the basics of programming",
      "ownerId": "102753038276005039640",
      "creationTime": "2026-02-14T01:53:58.991Z",
      "updateTime": "2026-02-14T01:53:58.991Z",
      "enrollmentCode": "3qsua37m",
      "courseState": "ACTIVE",
      "alternateLink": "https://classroom.google.com/c/ODI1NjM1ODY1NDg1",
      "guardiansEnabled": false
    }
  ],
  "nextPageToken": "..."
}
```

#### 获取课程信息

```bash
GET /v1/courses/{courseId}
```

#### 创建课程

```bash
POST /v1/courses
Content-Type: application/json

{
  "name": "Course Name",
  "section": "Section A",
  "descriptionHeading": "Course Title",
  "description": "Course description",
  "ownerId": "me"
}
```

**响应：**
```json
{
  "id": "825637533405",
  "name": "Course Name",
  "section": "Section A",
  "ownerId": "102753038276005039640",
  "courseState": "PROVISIONED",
  "enrollmentCode": "abc123"
}
```

#### 更新课程

```bash
PATCH /v1/courses/{courseId}?updateMask=name,description
Content-Type: application/json

{
  "name": "Updated Course Name",
  "description": "Updated description"
}
```

**注意：** 使用 `updateMask` 查询参数来指定要更新的字段。

#### 删除课程

```bash
DELETE /v1/courses/{courseId}
```

**注意：** 在删除课程之前，必须先将其归档。要归档课程，请将其 `courseState` 设置为 `ARCHIVED`。

### 课程作业（作业）

#### 列出课程作业

```bash
GET /v1/courses/{courseId}/courseWork
GET /v1/courses/{courseId}/courseWork?courseWorkStates=PUBLISHED
GET /v1/courses/{courseId}/courseWork?orderBy=dueDate
```

**查询参数：**
- `courseWorkStates` - 按状态过滤：`PUBLISHED`（已发布）、`DRAFT`（草稿）、`DELETED`（已删除）
- `orderBy` - 排序方式：`dueDate`（截止日期）、`updateTime`（更新时间）
- `pageSize` - 每页显示的结果数量
- `pageToken` - 下一页的令牌

#### 获取课程作业信息

```bash
GET /v1/courses/{courseId}/courseWork/{courseWorkId}
```

#### 创建课程作业

```bash
POST /v1/courses/{courseId}/courseWork
Content-Type: application/json

{
  "title": "Assignment Title",
  "description": "Assignment description",
  "workType": "ASSIGNMENT",
  "state": "PUBLISHED",
  "maxPoints": 100,
  "dueDate": {
    "year": 2026,
    "month": 3,
    "day": 15
  },
  "dueTime": {
    "hours": 23,
    "minutes": 59
  }
}
```

**作业类型：**
- `ASSIGNMENT`（常规作业）
- `SHORT_ANSWER QUESTION`（简答题）
- `MULTIPLE_CHOICE QUESTION`（选择题）

**状态：**
- `DRAFT`（对学生不可见）
- `PUBLISHED`（对学生可见）

#### 更新课程作业

```bash
PATCH /v1/courses/{courseId}/courseWork/{courseWorkId}?updateMask=title,description
Content-Type: application/json

{
  "title": "Updated Title",
  "description": "Updated description"
}
```

#### 删除课程作业

```bash
DELETE /v1/courses/{courseId}/courseWork/{courseWorkId}
```

### 学生提交内容

#### 列出学生提交的内容

```bash
GET /v1/courses/{courseId}/courseWork/{courseWorkId}/studentSubmissions
GET /v1/courses/{courseId}/courseWork/{courseWorkId}/studentSubmissions?states=TURNED_IN
```

**查询参数：**
- `states` - 按状态过滤：`NEW`（新建）、`CREATED`（已创建）、`TURNED_IN`（已提交）、`RETURNED_BY_STUDENT`（被学生取回）
- `userId` - 按学生 ID 过滤
- `pageSize` - 每页显示的结果数量
- `pageToken` - 下一页的令牌

**注意：** 只有当课程作业处于 `PUBLISHED` 状态时，才能列出提交的内容。

**响应：**
```json
{
  "studentSubmissions": [
    {
      "courseId": "825635865485",
      "courseWorkId": "825637404958",
      "id": "Cg4I8ufNwwYQ7tSZgYIB",
      "userId": "102753038276005039640",
      "creationTime": "2026-02-14T02:30:00.000Z",
      "state": "NEW",
      "alternateLink": "https://classroom.google.com/..."
    }
  ]
}
```

#### 获取学生提交的内容

```bash
GET /v1/courses/{courseId}/courseWork/{courseWorkId}/studentSubmissions/{submissionId}
```

#### 给提交的内容评分

```bash
PATCH /v1/courses/{courseId}/courseWork/{courseWorkId}/studentSubmissions/{submissionId}?updateMask=assignedGrade,draftGrade
Content-Type: application/json

{
  "assignedGrade": 95,
  "draftGrade": 95
}
```

#### 返回提交的内容

```bash
POST /v1/courses/{courseId}/courseWork/{courseWorkId}/studentSubmissions/{submissionId}:return
Content-Type: application/json

{}
```

### 教师

#### 列出教师

```bash
GET /v1/courses/{courseId}/teachers
```

**响应：**
```json
{
  "teachers": [
    {
      "courseId": "825635865485",
      "userId": "102753038276005039640",
      "profile": {
        "id": "102753038276005039640",
        "name": {
          "givenName": "John",
          "familyName": "Doe",
          "fullName": "John Doe"
        },
        "emailAddress": "john.doe@example.com"
      }
    }
  ]
}
```

#### 获取教师信息

```bash
GET /v1/courses/{courseId}/teachers/{userId}
```

#### 添加教师

```bash
POST /v1/courses/{courseId}/teachers
Content-Type: application/json

{
  "userId": "teacher@example.com"
}
```

#### 删除教师

```bash
DELETE /v1/courses/{courseId}/teachers/{userId}
```

### 学生

#### 列出学生

```bash
GET /v1/courses/{courseId}/students
```

#### 获取学生信息

```bash
GET /v1/courses/{courseId}/students/{userId}
```

#### 添加学生

```bash
POST /v1/courses/{courseId}/students
Content-Type: application/json

{
  "userId": "student@example.com"
}
```

#### 删除学生

```bash
DELETE /v1/courses/{courseId}/students/{userId}
```

### 公告

#### 列出公告

```bash
GET /v1/courses/{courseId}/announcements
GET /v1/courses/{courseId}/announcements?announcementStates=PUBLISHED
```

#### 获取公告信息

```bash
GET /v1/courses/{courseId}/announcements/{announcementId}
```

#### 创建公告

```bash
POST /v1/courses/{courseId}/announcements
Content-Type: application/json

{
  "text": "Announcement text content",
  "state": "PUBLISHED"
}
```

**状态：**
- `DRAFT`（对学生不可见）
- `PUBLISHED`（对学生可见）

#### 更新公告

```bash
PATCH /v1/courses/{courseId}/announcements/{announcementId}?updateMask=text
Content-Type: application/json

{
  "text": "Updated announcement text"
}
```

#### 删除公告

```bash
DELETE /v1/courses/{courseId}/announcements/{announcementId}
```

### 主题

#### 列出主题

```bash
GET /v1/courses/{courseId}/topics
```

#### 获取主题信息

```bash
GET /v1/courses/{courseId}/topics/{topicId}
```

#### 创建主题

```bash
POST /v1/courses/{courseId}/topics
Content-Type: application/json

{
  "name": "Topic Name"
}
```

#### 更新主题

```bash
PATCH /v1/courses/{courseId}/topics/{topicId}?updateMask=name
Content-Type: application/json

{
  "name": "Updated Topic Name"
}
```

#### 删除主题

```bash
DELETE /v1/courses/{courseId}/topics/{topicId}
```

### 课程作业材料

#### 列出课程作业材料

```bash
GET /v1/courses/{courseId}/courseWorkMaterials
```

#### 获取课程作业材料信息

```bash
GET /v1/courses/{courseId}/courseWorkMaterials/{courseWorkMaterialId}
```

### 邀请

#### 列出邀请信息

```bash
GET /v1/invitations?courseId={courseId}
GET /v1/invitations?userId=me
```

**注意：** 必须提供 `courseId` 或 `userId`。

#### 创建邀请

```bash
POST /v1/invitations
Content-Type: application/json

{
  "courseId": "825635865485",
  "userId": "user@example.com",
  "role": "STUDENT"
}
```

**角色：**
- `STUDENT`（学生）
- `TEACHER`（教师）
- `OWNER`（所有者）

#### 接受邀请

```bash
POST /v1/invitations/{invitationId}:accept
```

#### 删除邀请

```bash
DELETE /v1/invitations/{invitationId}
```

### 用户资料

#### 获取当前用户信息

```bash
GET /v1/userProfiles/me
```

**响应：**
```json
{
  "id": "102753038276005039640",
  "name": {
    "givenName": "John",
    "familyName": "Doe",
    "fullName": "John Doe"
  },
  "emailAddress": "john.doe@example.com",
  "permissions": [
    {
      "permission": "CREATE_COURSE"
    }
  ],
  "verifiedTeacher": false
}
```

#### 获取用户资料

```bash
GET /v1/userProfiles/{userId}
```

### 课程别名

#### 列出课程别名

```bash
GET /v1/courses/{courseId}/aliases
```

## 分页

Google Classroom API 使用基于令牌的分页机制。当还有更多结果时，响应中会包含 `nextPageToken`。

```bash
GET /v1/courses?pageSize=10
```

**响应：**
```json
{
  "courses": [...],
  "nextPageToken": "Ci8KLRIrEikKDmIMCLK8v8wGEIDQrsYBCgsI..."
}
```

要获取下一页，请使用以下代码：

```bash
GET /v1/courses?pageSize=10&pageToken=Ci8KLRIrEikKDmIMCLK8v8wGEIDQrsYBCgsI...
```

## 代码示例

### JavaScript

```javascript
// List all courses
const response = await fetch(
  'https://gateway.maton.ai/google-classroom/v1/courses',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.courses);
```

### Python

```python
import os
import requests

# List all courses
response = requests.get(
    'https://gateway.maton.ai/google-classroom/v1/courses',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
print(data['courses'])
```

### 创建作业的示例

```python
import os
import requests

course_id = "825635865485"

# Create an assignment
assignment = {
    "title": "Week 1 Homework",
    "description": "Complete exercises 1-10",
    "workType": "ASSIGNMENT",
    "state": "PUBLISHED",
    "maxPoints": 100,
    "dueDate": {"year": 2026, "month": 3, "day": 15},
    "dueTime": {"hours": 23, "minutes": 59}
}

response = requests.post(
    f'https://gateway.maton.ai/google-classroom/v1/courses/{course_id}/courseWork',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json=assignment
)
print(response.json())
```

## 注意事项

- **必填参数：** `updateMask`：PATCH 请求需要 `updateMask` 查询参数来指定要更新的字段。
- **课程删除：** 在删除课程之前，必须先将其归档（`courseState: "ARCHIVED"`）。
- **学生提交内容：** 只有当课程作业处于 `PUBLISHED` 状态时，才能获取学生的提交内容。
- **用户 ID：** 使用 `me` 来表示当前已认证的用户。
- **时间戳：** 日期使用 `{year, month, day}` 格式；时间使用 `{hours, minutes}` 格式。
- **重要提示：** 当将 curl 输出传递给 `jq` 或其他命令时，环境变量（如 `$MATON_API_KEY`）在某些 shell 环境中可能无法正确解析。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求无效、参数错误或前置条件失败 |
| 401 | API 密钥无效或令牌过期 |
| 403 | 没有权限 |
| 404 | 资源未找到 |
| 409 | 冲突（例如，用户已注册） |
| 429 | 请求次数限制 |
| 4xx/5xx | 来自 Google Classroom API 的传递错误 |

### 常见错误

**前置条件检查失败（400）**
- 在删除课程时：课程必须先被归档。
- 在列出提交内容时：课程作业必须已发布。

**权限被拒绝（403）**
- 用户没有执行该操作所需的角色（教师/所有者）。
- 试图访问监护信息时没有正确的权限范围。

## 资源

- [Google Classroom API 文档](https://developers.google.com/workspace/classroom/reference/rest)
- [课程资源参考](https://developers.google.com/workspace/classroom/reference/rest/v1/courses)
- [课程作业资源参考](https://developers.google.com/workspace/classroom/reference/rest/v1/courses.courseWork)
- [学生提交内容参考](https://developers.google.com/workspace/classroom/reference/rest/v1/courses.courseWork.studentSubmissions)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)