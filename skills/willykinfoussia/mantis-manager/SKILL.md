---
name: mantis-manager
description: 通过官方的 Mantis REST API 管理 Mantis 错误跟踪器（包括问题、项目、用户、过滤器以及配置）。支持对问题、项目、用户、附件、备注、标签、关系以及配置进行完整的 CRUD 操作（创建、读取、更新、删除）。具备动态实例切换功能，并支持基于上下文的基 URL 和令牌解析机制。
homepage: https://www.mantisbt.org/
metadata: {"openclaw":{"emoji":"🐞","requires":{"env":["MANTIS_BASE_URL","MANTIS_API_TOKEN"]},"primaryEnv":"MANTIS_API_TOKEN"}}
---

# Mantis Manager 技能（增强版）

## 🔐 基础 URL 与令牌解析

### 基础 URL 解析
基础 URL 的优先级（从高到低）：
1. `temporary_base_url` — 用于特定操作的一次性使用 URL
2. `user_base_url` — 当前会话的用户自定义 URL
3. `MANTIS_BASE_URL` — 环境默认 URL

这允许您：
- 动态地在多个 Mantis 实例之间切换
- 在测试/生产环境中进行测试
- 在不更改配置的情况下使用不同的客户端实例

**示例：**
```
// Default: uses MANTIS_BASE_URL from environment
GET {{resolved_base_url}}/issues

// Override for one operation:
temporary_base_url = "https://mantis-staging.example.com/api/rest"
GET {{resolved_base_url}}/issues

// Override for session:
user_base_url = "https://client-mantis.example.com/api/rest"
GET {{resolved_base_url}}/issues
```

### 令牌解析
令牌的优先级（从高到低）：
1. `temporary_token` — 用于特定操作的一次性使用令牌
2. `user_token` — 当前会话的用户自定义令牌
3. `MANTIS_API_TOKEN` — 环境默认令牌

环境变量通过标准的 OpenClaw 元数据进行处理：`requires.env` 声明 **必需** 的变量（`MANTIS_BASE_URL`、`MANTIS_API_TOKEN`）。您为 Mantis 使用的任何其他环境变量应被视为普通的进程环境变量，而不是特殊的 OpenClaw 元数据字段。

### 认证头
**所有 API 请求必须包含：**

```
Authorization: Bearer {{resolved_token}}
Content-Type: application/json
```

**注意：** `{{resolved_base_url}}` 和 `{{resolved_token}}` 是根据上述优先级规则在运行时确定的。

---

## 📌 示例中使用的符号

在本文档中：
- `{{MANTIS_BASE_URL}}` 表示 **解析后的基础 URL**（可能是 `temporary_base_url`、`user_base_url` 或环境变量 `MANTIS_BASE_URL`）
- `{{resolved_token}}` 表示 **解析后的令牌**（可能是 `temporary_token`、`user_token` 或环境变量 `MANTIS_API_TOKEN`）
- 所有端点的格式为：`{{MANTIS_BASE_URL}}/resource/path`

**重要提示：** 始终使用解析逻辑在运行时确定实际的 URL 和令牌。

---

## 🔄 上下文管理

> 这里的 `temporary_*` 和 `user_*` 名称是 **由技能逻辑使用的运行时上下文变量**，而不是 OpenClaw 元数据字段。OpenClaw 并没有定义 `optional.context` 元数据键；上下文是在运行时根据以下描述动态解析的。

### 设置临时值（一次性使用）

**用户查询：**
- “使用 https://staging.mantis.com/api/rest 进行此请求”
- “连接到生产实例以执行此操作”
- “仅此一次使用令牌 ABC123”

**操作：**
```
Set temporary_base_url = "https://staging.mantis.com/api/rest"
Set temporary_token = "ABC123"
... perform operation ...
Clear temporary_base_url
Clear temporary_token
```

**行为：** 临时值在首次使用后会被自动清除。

### 设置会话值（当前会话）

**用户查询：**
- “切换到客户端 XYZ 的 Mantis 实例”
- “对所有请求使用我的个人 API 令牌”
- “连接到测试环境”

**操作：**
```
Set user_base_url = "https://client-xyz.mantis.com/api/rest"
Set user_token = "personal_token_123"
... perform multiple operations ...
// Values persist for the entire session
```

**行为：** 会话值会一直保留，直到明确清除或会话结束。

### 清除上下文值

**用户查询：**
- “重置为默认的 Mantis 实例”
- “清除我的自定义令牌”
- “返回到环境默认设置”

**操作：**
```
Clear user_base_url
Clear user_token
// Now uses MANTIS_BASE_URL and MANTIS_API_TOKEN from environment
```

### 查看当前上下文

**用户查询：**
- “我连接到哪个 Mantis 实例？”
- “显示当前的 API 配置”
- “我正在使用哪个令牌？”

**响应应显示：**
```
Current Context:
- Base URL: https://client-xyz.mantis.com/api/rest (user_base_url)
- Token: user_t***123 (user_token)
- Fallback Base URL: https://default.mantis.com/api/rest (MANTIS_BASE_URL)
- Fallback Token: env_t***789 (MANTIS_API_TOKEN)
```

### 使用案例

#### 多实例管理
```
// Check production issue
Set temporary_base_url = "https://prod.mantis.com/api/rest"
Get issue 123

// Check staging issue  
Set temporary_base_url = "https://staging.mantis.com/api/rest"
Get issue 123

// Compare results
```

#### 客户端切换
```
// Switch to Client A
Set user_base_url = "https://clienta.mantis.com/api/rest"
Set user_token = "clienta_token"
List all projects
Get issues for project 5

// Switch to Client B
Set user_base_url = "https://clientb.mantis.com/api/rest"
Set user_token = "clientb_token"
List all projects
Get issues for project 3
```

#### 以代理身份执行管理员操作
```
// Connect to main instance as admin
Set user_token = "admin_token"

// Perform operation as specific user
Set temporary header: X-Impersonate-User = "john.doe"
Get user issues

// Back to admin
Clear temporary header
```

---

## 🐞 问题操作

### 列出问题
**用户查询：**
- “列出所有问题”
- “获取项目 5 的问题”
- “获取符合过滤器 10 的问题”
- “显示分配给我的问题”
- “获取未分配的问题”

**操作：**
```
GET {{MANTIS_BASE_URL}}/issues
```

**查询参数：**
- `page_size` — 每页的问题数量（默认：50）
- `page` — 页码（从 1 开始计数）
- `filter_id` — 要应用的保存过滤器的 ID
- `project_id` — 按特定项目过滤
- `select` — 要返回的字段（例如，“id,summary,status”）

**特殊端点：**
```
GET {{MANTIS_BASE_URL}}/issues?filter_id={{filter_id}}
GET {{MANTIS_BASE_URL}}/projects/{{project_id}}/issues
```

### 获取单个问题
**用户查询：**
- “显示问题 123”
- “获取错误 456 的详细信息”

**操作：**
```
GET {{MANTIS_BASE_URL}}/issues/{{id}}
```

### 创建问题
**用户查询：**
- “创建一个摘要为‘登录错误’、描述为‘无法登录’的问题”
- “在项目 5 中创建一个优先级为高的错误”
- “创建一个带有附件的问题”

**操作：**
```
POST {{MANTIS_BASE_URL}}/issues
```

**最小内容：**
```json
{
  "summary": "Issue summary",
  "description": "Detailed description",
  "category": {"name": "General"},
  "project": {"id": 1}
}
```

**完整内容（可选字段）：**
```json
{
  "summary": "Issue summary",
  "description": "Detailed description",
  "steps_to_reproduce": "1. Do this\n2. Do that",
  "additional_information": "Extra info",
  "category": {"id": 1, "name": "General"},
  "project": {"id": 1},
  "priority": {"id": 30, "name": "normal"},
  "severity": {"id": 50, "name": "minor"},
  "status": {"id": 10, "name": "new"},
  "reproducibility": {"id": 10, "name": "always"},
  "handler": {"id": 5},
  "tags": [{"name": "bug"}, {"name": "ui"}],
  "custom_fields": [{"field": {"id": 1}, "value": "custom value"}],
  "due_date": "2026-12-31T23:59:59+00:00",
  "version": {"name": "1.0"},
  "target_version": {"name": "2.0"}
}
```

**创建带有附件的问题：**
```
POST {{MANTIS_BASE_URL}}/issues
```
在内容中包含 `files` 数组，并对其进行 base64 编码。

### 更新问题
**用户查询：**
- “将问题 123 的状态更新为已解决”
- “将错误 456 的优先级更改为高”
- “将问题 789 分配给用户 10”

**操作：**
```
PATCH {{MANTIS_BASE_URL}}/issues/{{id}}
```

**示例内容：**
```json
{
  "status": {"name": "resolved"},
  "handler": {"id": 10},
  "priority": {"name": "high"},
  "summary": "Updated summary"
}
```

### 删除问题
**用户查询：**
- “删除问题 123”
- “删除错误 456”

**操作：**
```
DELETE {{MANTIS_BASE_URL}}/issues/{{id}}
```

### 监控/取消监控问题
**用户查询：**
- “监控问题 123”
- “停止监控错误 456”
- “将用户 10 添加为问题 789 的监控者”

**操作：**
```
POST   {{MANTIS_BASE_URL}}/issues/{{id}}/monitors
DELETE {{MANTIS_BASE_URL}}/issues/{{id}}/monitors
```

**内容（针对特定用户）：**
```json
{
  "user": {"id": 10}
}
```

### 添加/删除标签
**用户查询：**
- “向问题 123 添加标签‘critical’”
- “从问题 456 中删除标签‘bug’”

**操作：**
```
POST   {{MANTIS_BASE_URL}}/issues/{{id}}/tags
PATCH  {{MANTIS_BASE_URL}}/issues/{{id}}/tags
DELETE {{MANTIS_BASE_URL}}/issues/{{id}}/tags
```

**内容：**
```json
{
  "tags": [
    {"name": "bug"},
    {"name": "critical"}
  ]
}
```

### 添加问题关联
**用户查询：**
- “将问题 123 关联为问题 456 的重复问题”
- “从 789 添加到 101 的父关联”

**操作：**
```
POST {{MANTIS_BASE_URL}}/issues/{{id}}/relationships
```

**关联类型：**
- `duplicate-of`
- `related-to`
- `parent-of`
- `child-of`
- `has-duplicate`

### 添加附件
**用户查询：**
- “向问题 123 添加附件”
- “向错误 456 添加截图”

**操作：**
```
POST {{MANTIS_BASE_URL}}/issues/{{id}}/files
```

**内容：**
```json
{
  "files": [
    {
      "name": "screenshot.png",
      "content": "base64_encoded_content_here"
    }
  ]
}
```

### 删除附件
**用户查询：**
- “从问题 123 中删除附件 789”
- “从错误 456 中删除文件 101”

**操作：**
```
DELETE {{MANTIS_BASE_URL}}/issues/{{issue_id}}/files/{{file_id}}
```

### 问题备注

#### 添加备注
**用户查询：**
- “向问题 123 添加备注：‘问题现已修复’”
- “添加带有 2 小时时间跟踪的备注”
- “向错误 456 添加私有备注”

**操作：**
```
POST {{MANTIS_BASE_URL}}/issues/{{id}}/notes
```

**内容：**
```json
{
  "text": "Note content here",
  "view_state": {"name": "public"},
  "time_tracking": "PT2H30M"
}
```

**带有附件：**
```json
{
  "text": "Note with file",
  "files": [
    {
      "name": "log.txt",
      "content": "base64_content"
    }
  ]
}
```

#### 删除备注
**用户查询：**
- “从问题 123 中删除备注 55”
- “从错误 456 中删除评论 99”

**操作：**
```
DELETE {{MANTIS_BASE_URL}}/issues/{{issue_id}}/notes/{{note_id}}
```

---

## 📁 项目操作

### 列出所有项目
**用户查询：**
- “列出所有项目”
- “显示所有项目”
- “获取项目”

**操作：**
```
GET {{MANTIS_BASE_URL}}/projects
```

### 按 ID 获取项目
**用户查询：**
- “显示项目 5”
- “获取项目 10 的详细信息”

**操作：**
```
GET {{MANTIS_BASE_URL}}/projects/{{id}}
```

### 创建项目
**用户查询：**
- “创建名为‘New Product’的项目”
- “添加描述为‘内部工具’的项目”

**操作：**
```
POST {{MANTIS_BASE_URL}}/projects
```

**内容：**
```json
{
  "name": "Project Name",
  "description": "Project description",
  "enabled": true,
  "inherit_global": true,
  "view_state": {"name": "public"},
  "status": {"name": "development"}
}
```

### 更新项目
**用户查询：**
- “更新项目 5 的描述”
- “将项目 10 的状态更改为稳定”

**操作：**
```
PATCH {{MANTIS_BASE_URL}}/projects/{{id}}
```

### 删除项目
**用户查询：**
- “删除项目 5”
- “删除项目 10”

**操作：**
```
DELETE {{MANTIS_BASE_URL}}/projects/{{id}}
```

### 子项目

#### 获取子项目
**用户查询：**
- “显示项目 5 的子项目”

**操作：**
```
GET {{MANTIS_BASE_URL}}/projects/{{id}}/subprojects
```

#### 创建子项目
**用户查询：**
- “在项目 5 下创建子项目”

**操作：**
```
POST {{MANTIS_BASE_URL}}/projects/{{id}}/subprojects
```

**内容：**
```json
{
  "subproject": {"id": 10}
}
```

### 删除子项目
**操作：**
```
DELETE {{MANTIS_BASE_URL}}/projects/{{id}}/subprojects/{{subproject_id}}
```

### 项目用户

#### 获取项目用户
**用户查询：**
- “显示项目 5 中的用户”
- “列出项目 10 的成员”

**操作：**
```
GET {{MANTIS_BASE_URL}}/projects/{{id}}/users
```

#### 将用户添加到项目
**用户查询：**
- “将用户 20 添加为项目 5 的开发者”

**操作：**
```
POST {{MANTIS_BASE_URL}}/projects/{{id}}/users
```

**权限级别：**
- `viewer`（10）
- `reporter`（25）
- `updater`（40）
- `developer`（55）
- `manager`（70）
- `administrator`（90）

#### 从项目中删除用户
**操作：**
```
DELETE {{MANTIS_BASE_URL}}/projects/{{project_id}}/users/{{user_id}}
```

### 项目版本

#### 获取版本
**用户查询：**
- “显示项目 5 的版本”
- “列出项目 10 的发布版本”

**操作：**
```
GET {{MANTIS_BASE_URL}}/projects/{{id}}/versions
```

### 创建版本
**用户查询：**
- “为项目 5 创建版本 2.0”
- “为项目 10 添加版本 1.5”

**操作：**
```
POST {{MANTIS_BASE_URL}}/projects/{{id}}/versions
```

**内容：**
```json
{
  "name": "2.0",
  "description": "Major release",
  "released": true,
  "obsolete": false,
  "timestamp": "2026-06-01T00:00:00+00:00"
}
```

### 更新版本
**操作：**
```
PATCH {{MANTIS_BASE_URL}}/projects/{{project_id}}/versions/{{version_id}}
```

### 删除版本
**操作：**
```
DELETE {{MANTIS_BASE_URL}}/projects/{{project_id}}/versions/{{version_id}}
```

---

## 👥 用户操作

### 获取我的用户信息
**用户查询：**
- “显示我的用户信息”
- “获取我的个人资料”
- “我是谁？”

**操作：**
```
GET {{MANTIS_BASE_URL}}/users/me
```

### 按 ID 获取用户
**用户查询：**
- “显示用户 10”
- “获取用户 25 的信息”

**操作：**
```
GET {{MANTIS_BASE_URL}}/users/{{id}}
```

### 按用户名获取用户
**用户查询：**
- “查找用户 ‘john.doe’”
- “获取用户名为 ‘admin’ 的用户”

**操作：**
```
GET {{MANTIS_BASE_URL}}/users?name={{username}}
```

### 创建用户
**用户查询：**
- “创建用户 ‘jane.smith’，邮箱为 ‘jane@example.com’”
- “添加新用户”

**操作：**
```
POST {{MANTIS_BASE_URL}}/users
```

**最小内容：**
```json
{
  "username": "jane.smith",
  "email": "jane@example.com",
  "access_level": {"name": "reporter"}
}
```

**完整内容：**
```json
{
  "username": "jane.smith",
  "password": "SecurePass123!",
  "real_name": "Jane Smith",
  "email": "jane@example.com",
  "access_level": {"name": "developer"},
  "enabled": true,
  "protected": false
}
```

**更新用户**
**用户查询：**
- “将用户 10 的邮箱更新为 ‘new@example.com’”
- “将用户 25 的权限级别更改为开发者”

**操作：**
```
PATCH {{MANTIS_BASE_URL}}/users/{{id}}
```

**内容：**
```json
{
  "real_name": "Updated Name",
  "email": "new@example.com",
  "access_level": {"name": "developer"},
  "enabled": false
}
```

### 重置用户密码
**用户查询：**
- “重置用户 10 的密码”

**操作：**
```
PUT {{MANTIS_BASE_URL}}/users/{{id}}/reset-password
```

**内容：**
```json
{
  "password": "NewSecurePassword123!"
}
```

### 删除用户
**用户查询：**
- “删除用户 10”
- “删除用户 ‘john.doe’”

**操作：**
```
DELETE {{MANTIS_BASE_URL}}/users/{{id}}
```

---

## 🔍 过滤器操作

### 获取所有过滤器
**用户查询：**
- “列出所有过滤器”
- “显示我保存的过滤器”

**操作：**
```
GET {{MANTIS_BASE_URL}}/filters
```

### 按 ID 获取过滤器
**用户查询：**
- “显示过滤器 5”
- “获取过滤器 10 的详细信息”

**操作：**
```
GET {{MANTIS_BASE_URL}}/filters/{{id}}
```

### 删除过滤器
**用户查询：**
- “删除过滤器 5”
- “删除保存的过滤器 10”

**操作：**
```
DELETE {{MANTIS_BASE_URL}}/filters/{{id}}
```

---

## 🔐 令牌管理

### 为自己创建令牌
**用户查询：**
- “为我创建 API 令牌”
- “生成我的令牌”
- “创建名为 ‘automation’ 的新令牌”

**操作：**
```
POST {{MANTIS_BASE_URL}}/user_tokens
```

**内容：**
```json
{
  "name": "automation_token",
  "date_expiry": "2027-12-31T23:59:59+00:00"
}
```

### 为自己删除令牌
**用户查询：**
- “删除我的令牌”
- “撤销我的 API 令牌”

**操作：**
```
DELETE {{MANTIS_BASE_URL}}/user_tokens/{{token_id}}
```

### 为其他用户创建令牌
**用户查询：**
- “为用户 10 创建令牌”
- “为用户 ‘john.doe’ 生成 API 令牌”

**操作：**
```
POST {{MANTIS_BASE_URL}}/users/{{user_id}}/tokens
```

**内容：**
```json
{
  "name": "user_token",
  "date_expiry": "2027-12-31T23:59:59+00:00"
}
```

### 为其他用户删除令牌
**操作：**
```
DELETE {{MANTIS_BASE_URL}}/users/{{user_id}}/tokens/{{token_id}}
```

---

## ⚙️ 配置操作

### 获取单个配置选项
**用户查询：**
- “获取配置选项 ‘bug_report_page_fields’”
- “显示 ‘default_category_for_moves’ 的配置”

**操作：**
```
GET {{MANTIS_BASE_URL}}/config/{{option}}
```

### 获取多个配置选项
**用户查询：**
- “获取项目 5 的配置”
- “显示所有配置选项”

**操作：**
```
GET {{MANTIS_BASE_URL}}/config
```

**查询参数：**
- `option` — 特定选项名称
- `project_id` — 按项目过滤
- `user_id` — 按用户过滤

### 设置配置选项
**用户查询：**
- “将配置 ‘allow_signup’ 设置为 true”
- “更新配置选项”

**操作：**
```
PATCH {{MANTIS_BASE_URL}}/config
```

---

## 🌍 本地化操作

### 获取本地化字符串
**用户查询：**
- “获取本地化字符串 ‘status_new’”
- “将 ‘priority_high’ 翻译成法语”

**查询参数：**
- `language` — 语言代码（例如，'fr', 'en', 'de'）

### 获取多个本地化字符串
**用户查询：**
- “获取所有状态翻译”
- “获取优先级的本地化字符串”

**操作：**
```
GET {{MANTIS_BASE_URL}}/lang
```

**查询参数：**
- `strings` — 以逗号分隔的字符串键列表
- `language` — 语言代码

---

## 🔒 代理操作

### 以代理身份获取用户信息
**用户查询：**
- “以用户 10 的身份获取他们的信息”
- “以用户 ‘john.doe’ 的身份获取信息”

**操作：**
```
GET {{MANTIS_BASE_URL}}/users/me
```

**头部：**
```
X-Impersonate-User: {{username_or_id}}
```

---

## ⚠️ 错误处理

优雅地处理 HTTP 错误：

**401 未经授权：**
- 令牌无效或已过期
- 操作：通知用户检查 `MANTIS_API_TOKEN` 或提供有效的 `temporary_token`

**403 禁止：**
- 用户没有执行此操作的权限
- 操作：通知用户权限不足

**404 未找到：**
- 资源（问题、项目、用户等）不存在
- 操作：通知用户请求的资源未找到

**422 无法处理的实体：**
- 请求体中的验证错误
- 操作：在响应中显示验证错误并指导用户

**500 内部服务器错误：**
- 服务器端错误
- 操作：通知用户服务器错误并建议稍后重试

**通用错误响应格式：**
```json
{
  "message": "Error description",
  "code": 1234,
  "localized": "Localized error message"
}
```

---

## 📋 最佳实践

### 分页
- 对于列表操作，始终支持 `page_size` 和 `page` 参数
- 默认页大小：50
- 在结果分页时通知用户

### 字段选择
- 使用 `select` 参数仅返回所需的字段
- 例如：`select=id,summary,status,priority`
- 减少带宽并提高性能

### 过滤
- 使用 `filter_id` 应用保存的过滤器
- 结合分页处理大型数据集
- 考虑使用 `project_id` 进行项目特定过滤

### 附件
- 文件必须进行 base64 编码
- 在请求中包含文件名和内容
- 验证文件大小限制（检查 Mantis 配置）

### 时间跟踪
- 使用 ISO 8601 时间格式：`PT2H30M`（2 小时 30 分钟）
- 可以添加到备注中进行时间跟踪

### 日期格式
- 使用 ISO 8601 格式：`2026-12-31T23:59:59+00:00`
- 包含时区以确保准确性

### 自定义字段
- 检查项目配置中是否支持自定义字段
- 在请求中引用字段 ID

### 关联
- 验证您的 Mantis 版本支持的关联类型
- 一些关联会自动创建互惠链接

---

## 🚀 快速示例

### 创建并监控问题
```
1. POST /issues with summary and description
2. POST /issues/{{new_id}}/monitors to monitor
```

### 分配问题并添加备注
```
1. PATCH /issues/{{id}} with handler
2. POST /issues/{{id}}/notes with assignment comment
```

### 创建项目并设置版本
```
1. POST /projects with project details
2. POST /projects/{{id}}/versions with version info
```

### 用户管理流程
```
1. POST /users to create user
2. POST /projects/{{id}}/users to add to project
3. POST /users/{{id}}/tokens to create API token
```

---

## 🎯 高级用法

### 批量问题更新
在更新多个问题时：
- 遍历问题 ID
- 对每个问题使用 PATCH 请求
- 收集结果并生成摘要

### 基于过滤器的操作
获取所有高优先级错误：
```
1. GET /filters to find priority filter ID
2. GET /issues?filter_id={{filter_id}}&page_size=100
3. Process paginated results
```

### 项目迁移
复制项目结构：
```
1. GET /projects/{{source_id}} to get project details
2. GET /projects/{{source_id}}/versions for versions
3. POST /projects to create new project
4. POST /projects/{{new_id}}/versions for each version
```

### 用户审计
跟踪用户活动：
```
1. GET /issues?reporter_id={{user_id}}
2. GET /issues?handler_id={{user_id}}
3. GET /issues?monitor_id={{user_id}}
4. Compile activity report
```

### 多实例管理
同时操作多个 Mantis 实例：
```
// Scenario: Compare issue status across environments

1. Check production:
   Set temporary_base_url = "https://prod.mantis.com/api/rest"
   Set temporary_token = "prod_token"
   GET /issues/123
   Record status

2. Check staging:
   Set temporary_base_url = "https://staging.mantis.com/api/rest"
   Set temporary_token = "staging_token"
   GET /issues/123
   Record status

3. Compare and report differences
```

### 实例间同步
在实例间同步数据：
```
// Scenario: Clone project from one instance to another

1. Connect to source instance:
   Set user_base_url = "https://source.mantis.com/api/rest"
   Set user_token = "source_token"
   GET /projects/5 (get project details)
   GET /projects/5/versions (get versions)
   GET /projects/5/users (get users)

2. Connect to target instance:
   Set user_base_url = "https://target.mantis.com/api/rest"
   Set user_token = "target_token"
   POST /projects (create project)
   POST /projects/{{new_id}}/versions (create versions)
   POST /projects/{{new_id}}/users (add users)

3. Report sync results
```

### 客户端特定操作
管理多个客户端实例：
```
// Scenario: Daily status report for all clients

For each client in [ClientA, ClientB, ClientC]:
  1. Set user_base_url = client.mantis_url
  2. Set user_token = client.api_token
  3. GET /issues?filter_id=1 (get today's issues)
  4. Collect statistics
  5. Clear context

Generate consolidated report
```

---

## 📚 资源

- **Mantis API 文档**：请在 `{{MANTIS_BASE_URL}}/api/restswagger.yaml` 中查看您的 Mantis 实例文档
- **问题状态**：新问题、反馈、已确认、已分配、已解决、已关闭
- **优先级**：无、低、正常、高、紧急、立即
- **严重性**：特性、琐碎、文本、微小、重大、崩溃、阻塞
- **访问权限级别**：10=查看者、25=报告者、40=更新者、55=开发者、70=管理员、90=管理员

---

## ✅ 技能能力概述

此技能使您能够：

### 核心操作
- ✅ 对问题进行完整的 CRUD 操作
- ✅ 管理问题关联、标签和监控者
- ✅ 添加带有时间跟踪和附件的备注
- ✅ 完整的项目管理（创建、更新、删除）
- ✅ 管理子项目、版本和项目用户
- ✅ 用户管理（CRUD、密码重置）
- ✅ API 令牌管理（为自己和他人创建/删除）
- ✅ 过滤器管理和过滤查询
- ✅ 配置管理
- ✅ 本地化支持
- ✅ 代理功能

### 高级功能
- ✅ **动态实例切换** — 实时在多个 Mantis 实例之间切换
- ✅ **上下文感知的 URL 解析** — `temporary_base_url` → `user_base_url` → `MANTIS_BASE_URL`
- ✅ **上下文感知的令牌解析** — `temporary_token` → `user_token` → `MANTIS_API_TOKEN`
- ✅ **多实例管理** — 同时管理多个客户端/环境
- ✅ 实例间操作** — 在实例间比较、同步和迁移数据
- ✅ 全面的错误处理
- ✅ 分页和字段选择
- ✅ 高级工作流程和批量操作