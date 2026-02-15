---
name: zoho-recruit
description: |
  Zoho Recruit API integration with managed OAuth. Manage candidates, job openings, interviews, and recruitment workflows.
  Use this skill when users want to read, create, update, or search recruitment data like candidates, job openings, interviews, and applications in Zoho Recruit.
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

# Zoho Recruit

您可以使用管理型OAuth认证来访问Zoho Recruit API。该API支持对候选人、职位空缺、面试、申请以及招聘工作流程进行完整的CRUD（创建、读取、更新、删除）操作。

## 快速入门

```bash
# List all candidates
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates?per_page=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/zoho-recruit/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Zoho Recruit API端点路径。该代理服务会将请求转发到 `recruit.zoho.com` 并自动插入您的OAuth令牌。

## 认证

所有请求都必须在 `Authorization` 头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Zoho Recruit OAuth连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-recruit&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-recruit'}).encode()
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
    "connection_id": "0c9fa9b1-80b6-4caa-afc2-8629fe4d9661",
    "status": "ACTIVE",
    "creation_time": "2026-02-06T07:48:59.474215Z",
    "last_updated_time": "2026-02-06T07:57:52.950167Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "zoho-recruit",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成OAuth认证。

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

如果您有多个Zoho Recruit连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '0c9fa9b1-80b6-4caa-afc2-8629fe4d9661')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此字段，代理服务将使用默认的（最旧的）活动连接。

## API参考

### 模块

#### 列出所有模块

获取您Zoho Recruit账户中所有可用模块的列表。

```bash
GET /zoho-recruit/recruit/v2/settings/modules
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/settings/modules')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 候选人

#### 列出候选人

```bash
GET /zoho-recruit/recruit/v2/Candidates
```

**查询参数：**

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `fields` | 字符串 | - | 用逗号分隔的字段名称 |
| `sort_order` | 字符串 | - | `asc` 或 `desc` |
| `sort_by` | 字符串 | - | 按字段名称排序 |
| `converted` | 字符串 | - | `true`、`false` 或 `both` |
| `approved` | 字符串 | - | `true`、`false` 或 `both` |
| `page` | 整数 | 1 | 页码 |
| `per_page` | 整数 | 200 | 每页记录数（最多200条） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates?per_page=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "id": "846336000000552208",
      "First_Name": "Christina",
      "Last_Name": "Palaskas",
      "Email": "c.palaskas@example.com",
      "Candidate_Status": "Converted - Employee",
      "Current_Employer": "Chandlers",
      "Current_Job_Title": "Technical Consultant",
      "Experience_in_Years": 3,
      "Skill_Set": "Communication, Presentation, Customer service",
      "Candidate_Owner": {
        "name": "Byungkyu Park",
        "id": "846336000000549541"
      }
    }
  ],
  "info": {
    "per_page": 10,
    "count": 1,
    "page": 1,
    "more_records": false
  }
}
```

#### 根据ID获取候选人信息

```bash
GET /zoho-recruit/recruit/v2/Candidates/{record_id}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates/846336000000552208')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 搜索候选人

```bash
GET /zoho-recruit/recruit/v2/Candidates/search?criteria={criteria}
```

**查询参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `criteria` | 字符串 | 搜索条件（例如：`(Last_Name:contains:Smith)` |
| `email` | 字符串 | 按电子邮件搜索 |
| `phone` | 字符串 | 按电话号码搜索 |
| `word` | 字符串 | 全文搜索 |
| `page` | 整数 | 页码 |
| `per_page` | 整数 | 每页记录数 |

**搜索操作符：**
- 文本：`equals`、`not_equal`、`starts_with`、`ends_with`、`contains`、`not_contains`、`in`
- 日期/数字：`equals`、`not_equal`、`greater_than`、`less_than`、`greater_equal`、`less_equal`、`between`

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
import urllib.parse
criteria = urllib.parse.quote('(Candidate_Status:equals:Active)')
req = urllib.request.Request(f'https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates/search?criteria={criteria}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 创建候选人信息

```bash
POST /zoho-recruit/recruit/v2/Candidates
Content-Type: application/json

{
  "data": [
    {
      "First_Name": "John",
      "Last_Name": "Doe",
      "Email": "john.doe@example.com",
      "Phone": "555-123-4567",
      "Current_Job_Title": "Software Engineer"
    }
  ]
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "data": [{
        "First_Name": "John",
        "Last_Name": "Doe",
        "Email": "john.doe@example.com",
        "Phone": "555-123-4567"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "code": "SUCCESS",
      "status": "success",
      "message": "record added",
      "details": {
        "id": "846336000000600001",
        "Created_Time": "2026-02-06T10:00:00-08:00",
        "Created_By": {
          "name": "User Name",
          "id": "846336000000549541"
        }
      }
    }
  ]
}
```

#### 更新候选人信息

```bash
PUT /zoho-recruit/recruit/v2/Candidates/{record_id}
Content-Type: application/json

{
  "data": [
    {
      "Current_Job_Title": "Senior Software Engineer"
    }
  ]
}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({
    "data": [{
        "Current_Job_Title": "Senior Software Engineer"
    }]
}).encode()
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates/846336000000552208', data=data, method='PUT')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 删除候选人信息

```bash
DELETE /zoho-recruit/recruit/v2/Candidates?ids={record_id1},{record_id2}
```

### 职位空缺

#### 列出职位空缺

```bash
GET /zoho-recruit/recruit/v2/Job_Openings
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Job_Openings?per_page=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "data": [
    {
      "id": "846336000000552093",
      "Posting_Title": "Senior Accountant (Sample)",
      "Job_Opening_Status": "Waiting for approval",
      "Date_Opened": "2026-01-21",
      "Target_Date": "2026-02-20",
      "Industry": "Accounting",
      "City": "Tallahassee",
      "No_of_Candidates_Hired": 0,
      "No_of_Candidates_Associated": 0
    }
  ],
  "info": {
    "per_page": 10,
    "count": 1,
    "page": 1,
    "more_records": false
  }
}
```

#### 根据ID获取职位空缺信息

```bash
GET /zoho-recruit/recruit/v2/Job_Openings/{record_id}
```

#### 创建职位空缺

```bash
POST /zoho-recruit/recruit/v2/Job_Openings
Content-Type: application/json

{
  "data": [
    {
      "Posting_Title": "Software Engineer",
      "Job_Opening_Status": "In-progress",
      "Date_Opened": "2026-02-01",
      "Target_Date": "2026-03-01"
    }
  ]
}
```

#### 更新职位空缺信息

```bash
PUT /zoho-recruit/recruit/v2/Job_Openings/{record_id}
Content-Type: application/json
```

#### 删除职位空缺

```bash
DELETE /zoho-recruit/recruit/v2/Job_Openings?ids={record_id1},{record_id2}
```

### 面试

#### 列出面试记录

```bash
GET /zoho-recruit/recruit/v2/Interviews
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Interviews?per_page=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 根据ID获取面试记录

```bash
GET /zoho-recruit/recruit/v2/Interviews/{record_id}
```

#### 创建面试记录

```bash
POST /zoho-recruit/recruit/v2/Interviews
Content-Type: application/json

{
  "data": [
    {
      "Interview_Name": "Technical Interview",
      "Candidate_Name": {"id": "846336000000552208"},
      "Posting_Title": {"id": "846336000000552093"},
      "Start_DateTime": "2026-02-10T10:00:00-08:00",
      "End_DateTime": "2026-02-10T11:00:00-08:00"
    }
  ]
}
```

### 部门

#### 列出部门信息

```bash
GET /zoho-recruit/recruit/v2/Departments
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-recruit/recruit/v2/Departments?per_page=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 申请信息

#### 列出申请记录

```bash
GET /zoho-recruit/recruit/v2/Applications
```

### 通用记录操作

所有模块都支持相同的CRUD操作：

```bash
# List records
GET /zoho-recruit/recruit/v2/{module_api_name}

# Get record by ID
GET /zoho-recruit/recruit/v2/{module_api_name}/{record_id}

# Create records
POST /zoho-recruit/recruit/v2/{module_api_name}

# Update records
PUT /zoho-recruit/recruit/v2/{module_api_name}/{record_id}

# Delete records
DELETE /zoho-recruit/recruit/v2/{module_api_name}?ids={id1},{id2}

# Search records
GET /zoho-recruit/recruit/v2/{module_api_name}/search?criteria={criteria}
```

## 可用模块

| 模块 | API名称 | 描述 |
|--------|----------|-------------|
| Candidates | `Candidates` | 候选人信息 |
| Job_Openings | `Job_Openings` | 职位空缺信息 |
| Applications | `Applications` | 申请信息 |
| Interviews | `Interviews` | 面试记录 |
| Departments | `Departments` | 部门信息 |
| Clients | `Clients` | 客户信息 |
| Contacts | `Contacts` | 联系人信息 |
| Campaigns | `Campaigns` | 招聘活动 |
| Referrals | `Referrals` | 员工推荐信息 |
| Tasks | `Tasks` | 待办事项 |
| Events | `Events` | 日历事件 |
| Vendors | `Vendors` | 外部供应商信息 |

## 分页

Zoho Recruit使用基于页码的分页机制：

```bash
GET /zoho-recruit/recruit/v2/{module_api_name}?page=1&per_page=200
```

- `page`：页码（默认值：1）
- `per_page`：每页记录数（默认值：200，最大值：200）

响应中包含分页信息：
```json
{
  "data": [...],
  "info": {
    "per_page": 200,
    "count": 50,
    "page": 1,
    "more_records": false
  }
}
```

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates?per_page=10',
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
    'https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'per_page': 10}
)
data = response.json()
```

## 注意事项

- 记录ID是数字字符串（例如：`846336000000552208`）
- 每次GET请求最多返回200条记录。
- 每次POST/PUT请求最多返回100条记录。
- 每次DELETE请求最多返回100条记录。
- 模块API名称区分大小写（例如：`Job_Openings`，而不是 `job_openings`）。
- 对于候选人信息，`Last_Name` 是必填字段。
- 日期格式：`yyyy-MM-dd`。
- 时间格式：`yyyy-MM-ddTHH:mm:ss±HH:mm`（ISO 8601）。
- 查找字段使用包含 `id` 和可选的 `name` 的JSON对象。
- 重要提示：当URL包含特殊字符时，使用 `curl -g` 命令。
- 重要提示：在将curl输出传递给 `jq` 或其他命令时，某些shell环境中环境变量（如 `$MATON_API_KEY`）可能无法正确解析。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到Zoho Recruit连接或请求无效 |
| 401 | Maton API密钥无效或缺失 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自Zoho Recruit API的传递错误 |

### 常见错误代码

| 代码 | 描述 |
|------|-------------|
| INVALID_DATA | 字段值无效 |
| MANDATORY_NOT_FOUND | 必填字段缺失 |
| DUPLICATE_DATA | 检测到重复记录 |
| INVALID_MODULE | 模块API名称无效 |
| NO_PERMISSION | 权限不足 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称错误

1. 确保您的URL路径以 `zoho-recruit` 开头。例如：
- 正确格式：`https://gateway.maton.ai/zoho-recruit/recruit/v2/Candidates`
- 错误格式：`https://gateway.maton.ai/recruit/v2/Candidates`

## 资源

- [Zoho Recruit API v2概述](https://www.zoho.com/recruit/developer-guide/apiv2/)
- [获取记录API](https://www.zoho.com/recruit/developer-guide/apiv2/get-records.html)
- [插入记录API](https://www.zoho.com/recruit/developer-guide/apiv2/insert-records.html)
- [更新记录API](https://www.zoho.com/recruit/developer-guide/apiv2/update-records.html)
- [删除记录API](https://www.zoho.com/recruit/developer-guide/apiv2/delete-records.html)
- [搜索记录API](https://www.zoho.com/recruit/developer-guide/apiv2/search-records.html)
- [模块API](https://www.zoho.com/recruit/developer-guide/apiv2/modules-api.html)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)