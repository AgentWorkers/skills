---
name: zoho-people
description: |
  Zoho People API integration with managed OAuth. Manage employees, departments, designations, attendance, and leave.
  Use this skill when users want to read, create, update, or query HR data like employees, departments, designations, and forms in Zoho People.
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

# Zoho People

您可以使用受管理的 OAuth 认证来访问 Zoho People API。该 API 允许您对员工、部门、职位、考勤记录以及自定义人力资源表单进行完整的创建（Create）、读取（Read）、更新（Update）和删除（Delete, CRUD）操作。

## 快速入门

```bash
# List all employees
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms/employee/getRecords?sIndex=1&limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/zoho-people/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 Zoho People API 端点路径。该网关会将请求代理到 `people.zoho.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都必须在 `Authorization` 标头中包含 Maton API 密钥：

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

您可以在 `https://ctrl.maton.ai` 管理您的 Zoho People OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=zoho-people&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'zoho-people'}).encode()
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
    "connection_id": "7d11ea2e-c580-43fe-bc56-d9d4765b9bc6",
    "status": "ACTIVE",
    "creation_time": "2026-02-06T07:42:07.681370Z",
    "last_updated_time": "2026-02-06T07:46:12.648445Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "zoho-people",
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

如果您有多个 Zoho People 连接，请使用 `Maton-Connection` 标头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '7d11ea2e-c580-43fe-bc56-d9d4765b9bc6')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 表单操作

#### 列出所有表单

获取您 Zoho People 账户中所有可用表单的列表。

```bash
GET /zoho-people/people/api/forms
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "result": [
      {
        "componentId": 943596000000035679,
        "iscustom": false,
        "displayName": "Employee",
        "formLinkName": "employee",
        "PermissionDetails": {
          "Add": 3,
          "Edit": 3,
          "View": 3
        },
        "isVisible": true,
        "viewDetails": {
          "view_Id": 943596000000035705,
          "view_Name": "P_EmployeeView"
        }
      }
    ],
    "message": "Data fetched successfully",
    "status": 0
  }
}
```

### 员工操作

#### 列出员工（批量记录）

```bash
GET /zoho-people/people/api/forms/employee/getRecords?sIndex={startIndex}&limit={limit}
```

**查询参数：**

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `sIndex` | 整数 | 1 | 开始索引（从 1 开始） |
| `limit` | 整数 | 200 | 记录数量（最多 200 条） |
| `SearchColumn` | 字符串 | - | `EMPLOYEEID` 或 `EMPLOYEEMAILALIAS` |
| `SearchValue` | 字符串 | - | 要搜索的值 |
| `modifiedtime` | 长整型 | - | 记录修改的时间戳（以毫秒为单位） |

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms/employee/getRecords?sIndex=1&limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "result": [
      {
        "943596000000294355": [
          {
            "FirstName": "Christopher",
            "LastName": "Brown",
            "EmailID": "christopherbrown@zylker.com",
            "EmployeeID": "S20",
            "Department": "Management",
            "Designation": "Administration",
            "Employeestatus": "Active",
            "Gender": "Male",
            "Date_of_birth": "02-Feb-1987",
            "Zoho_ID": 943596000000294355
          }
        ]
      }
    ],
    "message": "Data fetched successfully",
    "status": 0
  }
}
```

#### 列出员工（按视图查看）

```bash
GET /zoho-people/api/forms/{viewName}/records?rec_limit={limit}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-people/api/forms/P_EmployeeView/records?rec_limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 按 ID 搜索员工

```bash
GET /zoho-people/people/api/forms/employee/getRecords?SearchColumn=EMPLOYEEID&SearchValue={employeeId}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms/employee/getRecords?SearchColumn=EMPLOYEEID&SearchValue=S20')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### 按电子邮件搜索员工

```bash
GET /zoho-people/people/api/forms/employee/getRecords?SearchColumn=EMPLOYEEMAILALIAS&SearchValue={email}
```

### 部门操作

#### 列出部门

```bash
GET /zoho-people/people/api/forms/department/getRecords?sIndex={startIndex}&limit={limit}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms/department/getRecords?sIndex=1&limit=50')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "result": [
      {
        "943596000000294315": [
          {
            "Department": "IT",
            "Department_Lead": "",
            "Parent_Department": "",
            "Zoho_ID": 943596000000294315
          }
        ]
      }
    ],
    "message": "Data fetched successfully",
    "status": 0
  }
}
```

### 职位操作

#### 列出职位信息

```bash
GET /zoho-people/people/api/forms/designation/getRecords?sIndex={startIndex}&limit={limit}
```

**示例：**

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms/designation/getRecords?sIndex=1&limit=50')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "result": [
      {
        "943596000000294399": [
          {
            "Designation": "Team Member",
            "EEO_Category": "Professionals",
            "Zoho_ID": 943596000000294399
          }
        ]
      }
    ],
    "message": "Data fetched successfully",
    "status": 0
  }
}
```

### 插入记录

向任何表单中添加新记录。

```bash
POST /zoho-people/people/api/forms/json/{formLinkName}/insertRecord
Content-Type: application/x-www-form-urlencoded

inputData={field1:'value1',field2:'value2'}
```

**示例 - 创建部门：**

```bash
python <<'EOF'
import urllib.request, os, json
from urllib.parse import urlencode

inputData = json.dumps({"Department": "Engineering"})
data = urlencode({"inputData": inputData}).encode()

req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms/json/department/insertRecord', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "response": {
    "result": {
      "pkId": "943596000000300001",
      "message": "Successfully Added"
    },
    "message": "Data added successfully",
    "status": 0
  }
}
```

### 更新记录

修改现有记录。

```bash
POST /zoho-people/people/api/forms/json/{formLinkName}/updateRecord
Content-Type: application/x-www-form-urlencoded

inputData={field1:'newValue'}&recordId={recordId}
```

**示例 - 更新员工信息：**

```bash
python <<'EOF'
import urllib.request, os, json
from urllib.parse import urlencode

inputData = json.dumps({"Department": "Engineering"})
data = urlencode({
    "inputData": inputData,
    "recordId": "943596000000294355"
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/zoho-people/people/api/forms/json/employee/updateRecord', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/x-www-form-urlencoded')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 考勤操作

**注意：** 考勤相关的 API 需要额外的 OAuth 权限范围。

#### 获取考勤记录

```bash
GET /zoho-people/people/api/attendance/getAttendanceEntries?date={date}&dateFormat={format}
```

**参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `date` | 字符串 | 组织规定的日期格式 |
| `dateFormat` | 字符串 | 日期格式（例如：`dd-MMM-yyyy`） |
| `empId` | 字符串 | 员工 ID（可选） |
| `emailId` | 字符串 | 员工电子邮件（可选） |

#### 登录/签出

```bash
POST /zoho-people/people/api/attendance
Content-Type: application/x-www-form-urlencoded

dateFormat=dd/MM/yyyy HH:mm:ss&checkIn={datetime}&checkOut={datetime}&empId={empId}
```

## 常见表单链接名称

| 表单 | 表单链接名称 | 描述 |
|------|--------------|-------------|
| Employee | `employee` | 员工记录 |
| Department | `department` | 部门信息 |
| Designation | `designation` | 职位信息 |
| Leave | `leave` | 休假申请 |
| Clients | `P_ClientDetails` | 客户信息 |

## 分页

Zoho People 使用基于索引的分页方式：

```bash
GET /zoho-people/people/api/forms/{formLinkName}/getRecords?sIndex=1&limit=200
```

- `sIndex`：开始索引（从 1 开始）
- `limit`：每次请求的记录数量（最多 200 条）

对于后续页面：
- 第 1 页：`sIndex=1&limit=200`
- 第 2 页：`sIndex=201&limit=200`
- 第 3 页：`sIndex=401&limit=200`

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/zoho-people/people/api/forms/employee/getRecords?sIndex=1&limit=10',
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
    'https://gateway.maton.ai/zoho-people/people/api/forms/employee/getRecords',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'sIndex': 1, 'limit': 10}
)
data = response.json()
```

## 注意事项

- 记录 ID 是数字字符串（例如：`943596000000294355`）
- 响应中的 `Zoho_ID` 字段包含记录 ID
- 每次 GET 请求最多返回 200 条记录
- 插入/更新操作使用 `inputData`（以 JSON 格式编码的数据）
- 日期格式因字段和组织设置而异
- 某些 API（如考勤、休假）需要额外的 OAuth 权限范围。如果您收到 `INVALID_OAUTHSCOPE` 错误，请联系 Maton 支持团队（support@maton.ai），并提供具体的操作、API 以及使用场景
- 响应数据包含在 `response.result[]` 数组中
- 重要提示：当 URL 包含特殊字符时，使用 `curl -g` 命令
- 重要提示：在将 curl 输出传递给 `jq` 或其他命令时，某些 shell 环境中可能无法正确解析 `$MATON_API_KEY` 环境变量

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 400 | 未找到 Zoho People 连接或请求无效 |
| 401 | Maton API 密钥无效或缺失，或 OAuth 权限范围无效 |
| 429 | 请求频率限制 |
| 4xx/5xx | 来自 Zoho People API 的传递错误 |

### 常见错误代码

| 代码 | 描述 |
|------|-------------|
| 7011 | 表单名称无效 |
| 7012 | 视图名称无效 |
| 7021 | 记录数量超过限制（最多 200 条） |
| 7024 | 未找到记录 |
| 7042 | 搜索值无效 |
| 7218 | OAuth 权限范围无效 |

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

1. 确保您的 URL 路径以 `zoho-people` 开头。例如：
- 正确的路径：`https://gateway.maton.ai/zoho-people/people/api/forms`
- 错误的路径：`https://gateway.maton.ai/people/api/forms`

## 资源

- [Zoho People API 概述](https://www.zoho.com/people/api/overview.html)
- [批量记录 API](https://www.zoho.com/people/api/bulk-records.html)
- [获取表单 API](https://www.zoho.com/people/api/forms-api/fetch-forms.html)
- [插入记录 API](https://www.zoho.com/people/api/insert-records.html)
- [更新记录 API](https://www.zoho.com/people/api/update-records.html)
- [考勤 API](https://www.zoho.com/people/api/attendance-entries.html)
- [休假 API](https://www.zoho.com/people/api/add-leave.html)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持团队](mailto:support@maton.ai)