---
name: netpad
description: "管理 NetPad 表单、提交记录、用户以及基于角色的访问控制（RBAC）功能。适用场景包括：  
(1) 创建包含自定义字段的表单；  
(2) 向表单提交数据；  
(3) 查询表单提交情况；  
(4) 管理用户/组/角色（实现 RBAC）；  
(5) 从市场平台安装 NetPad 应用程序。  

使用该工具需要 NETPAD_API_KEY（用于 API 接口）或通过 `netpad login`（用于命令行界面 CLI）。"
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["curl","jq","netpad"]},"install":[{"id":"cli","kind":"node","package":"@netpad/cli","bins":["netpad"],"label":"Install NetPad CLI (npm)"}],"author":{"name":"Michael Lynn","github":"mrlynn","website":"https://mlynn.org","linkedin":"https://linkedin.com/in/mlynn"}}}
---

# NetPad

通过 CLI 和 REST API 管理表单、提交记录、用户以及基于角色的访问控制（RBAC）。

## 两种工具

| 工具 | 安装方式 | 用途 |
|------|---------|---------|
| `netpad` CLI | `npm i -g @netpad/cli` | 管理基于角色的访问控制（RBAC）、市场功能、包管理 |
| REST API | `curl` + API 密钥 | 操作表单、提交记录、数据 |

## 认证

```bash
export NETPAD_API_KEY="np_live_xxx"  # Production
export NETPAD_API_KEY="np_test_xxx"  # Test (can submit to drafts)
```

所有请求均使用 Bearer Token 进行身份验证：
```bash
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/..."
```

---

## 快速参考

| 功能 | API 端点 | 方法 |
|------|----------|--------|
| 列出项目 | `/projects` | GET |
| 列出表单 | `/forms` | GET |
| 创建表单 | `/forms` | POST |
| 获取表单详情 | `/forms/{formId}` | GET |
| 更新/发布表单 | `/forms/{formId}` | PATCH |
| 删除表单 | `/forms/{formId}` | DELETE |
| 列出提交记录 | `/forms/{formId}/submissions` | GET |
| 创建提交记录 | `/forms/{formId}/submissions` | POST |
| 获取提交记录详情 | `/forms/{formId}/submissions/{id}` | GET |
| 删除提交记录 | `/forms/{formId}/submissions/{id}` | DELETE |

---

## 项目

表单属于特定项目。在创建表单之前，请先获取项目 ID。

```bash
# List projects
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/projects" | jq '.data[] | {projectId, name}'
```

---

## 表单

### 列出表单

```bash
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms?status=published&pageSize=50"
```

### 创建表单

```bash
curl -X POST -H "Authorization: Bearer $NETPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://www.netpad.io/api/v1/forms" \
  -d '{
    "name": "Contact Form",
    "description": "Simple contact form",
    "projectId": "proj_xxx",
    "fields": [
      {"path": "name", "label": "Name", "type": "text", "required": true},
      {"path": "email", "label": "Email", "type": "email", "required": true},
      {"path": "phone", "label": "Phone", "type": "phone"},
      {"path": "message", "label": "Message", "type": "textarea"}
    ]
  }'
```

### 获取表单详情

```bash
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms/{formId}"
```

### 发布表单

```bash
curl -X PATCH -H "Authorization: Bearer $NETPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://www.netpad.io/api/v1/forms/{formId}" \
  -d '{"status": "published"}'
```

### 更新表单字段

```bash
curl -X PATCH -H "Authorization: Bearer $NETPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://www.netpad.io/api/v1/forms/{formId}" \
  -d '{
    "fields": [
      {"path": "name", "label": "Full Name", "type": "text", "required": true},
      {"path": "email", "label": "Email Address", "type": "email", "required": true},
      {"path": "company", "label": "Company", "type": "text"},
      {"path": "role", "label": "Role", "type": "select", "options": [
        {"value": "dev", "label": "Developer"},
        {"value": "pm", "label": "Product Manager"},
        {"value": "exec", "label": "Executive"}
      ]}
    ]
  }'
```

### 删除表单

```bash
curl -X DELETE -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms/{formId}"
```

---

## 提交记录

### 提交数据

```bash
curl -X POST -H "Authorization: Bearer $NETPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://www.netpad.io/api/v1/forms/{formId}/submissions" \
  -d '{
    "data": {
      "name": "John Doe",
      "email": "john@example.com",
      "message": "Hello from the API!"
    }
  }'
```

### 列出提交记录

```bash
# Recent submissions
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms/{formId}/submissions?pageSize=50"

# With date filter
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms/{formId}/submissions?startDate=2026-01-01T00:00:00Z"

# Sorted ascending
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms/{formId}/submissions?sortOrder=asc"
```

### 获取单个提交记录

```bash
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms/{formId}/submissions/{submissionId}"
```

### 删除提交记录

```bash
curl -X DELETE -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms/{formId}/submissions/{submissionId}"
```

---

## 字段类型

| 类型 | 描述 | 验证规则 |
|------|-------------|------------|
| `text` | 单行文本 | 最小长度、最大长度、正则表达式验证 |
| `email` | 电子邮件地址 | 内置验证 |
| `phone` | 电话号码 | 内置验证 |
| `number` | 数字输入 | 最小值、最大值限制 |
| `date` | 日期选择器 | - |
| `select` | 下拉菜单 | 选项格式：`[{value, label}]` |
| `checkbox` | 布尔值 | - |
| `textarea` | 多行文本 | 最小长度、最大长度限制 |
| `file` | 文件上传 | - |

### 字段结构（字段规范）

```json
{
  "path": "fieldName",
  "label": "Display Label",
  "type": "text",
  "required": true,
  "placeholder": "Hint text",
  "helpText": "Additional guidance",
  "options": [{"value": "a", "label": "Option A"}],
  "validation": {
    "minLength": 1,
    "maxLength": 500,
    "pattern": "^[A-Z].*",
    "min": 0,
    "max": 100
  }
}
```

---

## 常用操作

### 创建并发布表单

```bash
# 1. Create draft
RESULT=$(curl -s -X POST -H "Authorization: Bearer $NETPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://www.netpad.io/api/v1/forms" \
  -d '{"name":"Survey","projectId":"proj_xxx","fields":[...]}')
FORM_ID=$(echo $RESULT | jq -r '.data.id')

# 2. Publish
curl -X PATCH -H "Authorization: Bearer $NETPAD_API_KEY" \
  -H "Content-Type: application/json" \
  "https://www.netpad.io/api/v1/forms/$FORM_ID" \
  -d '{"status":"published"}'
```

### 导出所有提交记录

```bash
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms/{formId}/submissions?pageSize=1000" \
  | jq '.data[].data'
```

### 批量提交

```bash
for row in $(cat data.json | jq -c '.[]'); do
  curl -s -X POST -H "Authorization: Bearer $NETPAD_API_KEY" \
    -H "Content-Type: application/json" \
    "https://www.netpad.io/api/v1/forms/{formId}/submissions" \
    -d "{\"data\":$row}"
done
```

### 搜索表单

```bash
curl -H "Authorization: Bearer $NETPAD_API_KEY" \
  "https://www.netpad.io/api/v1/forms?search=contact&status=published"
```

---

## 辅助脚本

使用 `scripts/netpad.sh` 执行常见操作：

```bash
# Make executable
chmod +x scripts/netpad.sh

# Usage
./scripts/netpad.sh projects list
./scripts/netpad.sh forms list published
./scripts/netpad.sh forms create "Contact Form" proj_xxx
./scripts/netpad.sh forms publish frm_xxx
./scripts/netpad.sh submissions list frm_xxx
./scripts/netpad.sh submissions create frm_xxx '{"name":"John","email":"john@example.com"}'
./scripts/netpad.sh submissions export frm_xxx > data.jsonl
./scripts/netpad.sh submissions count frm_xxx
```

---

## 速率限制

| 限制类型 | 限制值 |
|-------|-------|
| 每小时请求次数 | 1,000 次 |
| 每天请求次数 | 10,000 次 |

请求头：`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

## 响应格式

### 成功响应

```json
{
  "success": true,
  "data": { ... },
  "pagination": {"total": 100, "page": 1, "pageSize": 20, "hasMore": true},
  "requestId": "uuid"
}
```

### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Description",
    "details": {}
  },
  "requestId": "uuid"
}
```

---

## 环境变量

```bash
# Required for REST API
export NETPAD_API_KEY="np_live_xxx"

# Optional (for local/staging)
export NETPAD_BASE_URL="https://staging.netpad.io/api/v1"
```

---

## NetPad CLI (@netpad/cli)

安装方式：`npm i -g @netpad/cli`

### 认证

```bash
netpad login              # Opens browser
netpad whoami             # Check auth status
netpad logout             # Clear credentials
```

### 市场功能与包管理

```bash
# Search for apps
netpad search "helpdesk"

# Install an app
netpad install @netpad/helpdesk-app

# List installed
netpad list

# Create new app scaffold
netpad create-app my-app

# Submit to marketplace
netpad submit ./my-app
```

### 基于角色的访问控制（RBAC） - 用户

```bash
# List org members
netpad users list -o org_xxx

# Add user
netpad users add user@example.com -o org_xxx --role member

# Change role
netpad users update user@example.com -o org_xxx --role admin

# Remove user
netpad users remove user@example.com -o org_xxx
```

### 基于角色的访问控制（RBAC） - 组织

```bash
# List groups
netpad groups list -o org_xxx

# Create group
netpad groups create "Engineering" -o org_xxx

# Add user to group
netpad groups add-member grp_xxx user@example.com -o org_xxx

# Delete group
netpad groups delete grp_xxx -o org_xxx
```

### 基于角色的访问控制（RBAC） - 角色

```bash
# List roles (builtin + custom)
netpad roles list -o org_xxx

# Create custom role
netpad roles create "Reviewer" -o org_xxx --base viewer --description "Can review submissions"

# View role details
netpad roles get role_xxx -o org_xxx

# Delete custom role
netpad roles delete role_xxx -o org_xxx
```

### 基于角色的访问控制（RBAC） - 权限分配

```bash
# Assign role to user
netpad assign user user@example.com role_xxx -o org_xxx

# Assign role to group
netpad assign group grp_xxx role_xxx -o org_xxx

# Remove assignment
netpad unassign user user@example.com role_xxx -o org_xxx
```

### 基于角色的访问控制（RBAC） - 权限设置

```bash
# List all permissions
netpad permissions list -o org_xxx

# Check user's effective permissions
netpad permissions check user@example.com -o org_xxx
```

---

## 参考资料

- `references/api-endpoints.md` — 完整的 REST API 端点文档
- `references/cli-commands.md` — 完整的 CLI 命令参考

---

## 作者

**Michael Lynn** — MongoDB 的首席开发顾问

- 🌐 网站：[mlynn.org](https://mlynn.org)
- 🐙 GitHub：[@mrlynn](https://github.com/mrlynn)
- 💼 LinkedIn：[linkedin.com/in/mlynn](https://linkedin.com/in/mlynn)