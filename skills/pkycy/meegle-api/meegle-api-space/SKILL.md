---
name: meegle-api-space
description: Meegle OpenAPI：用于空间（项目）操作的接口。
metadata: { openclaw: {} }
---
# Meegle API — 空间（Spaces）

## 空间（Space）的 OpenAPI 功能：
- 列出所有空间（list spaces）
- 获取空间详情（get details）
- 获取空间成员信息（get team members）

---

## 获取空间列表（Get Space List）

获取指定用户有权访问的空间列表，以及这些空间中安装了该插件的情况。

### 注意事项：
- 当使用 **虚拟令牌**（virtual token）时，只能查询权限管理（Permission Management）> **选择数据范围**（Select Data Scope）中允许访问的空间。如需查询其他空间，请使用官方的（非虚拟）令牌。

### 使用场景：
- 列出用户可以访问的所有空间
- 构建空间选择器或导航界面
- 检查哪些空间安装了该插件

### API 规范：`get_space_list`
```yaml
name: get_space_list
type: api
description: List spaces user can access where plugin is installed.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/projects" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { user_key: { type: string, required: true }, order: { type: array, required: false } }
outputs: { data: array }
constraints: [Permission: Space; virtual token limited to Select Data Scope]
error_mapping: { 30006: User not found, 10302: User resigned }
```

### 使用说明：
- **user_key**：必填参数；用于指定要查询的空间所属的用户。
- **order**：可选参数；使用 `["-last_visited"]` 可以按最近访问的顺序显示空间。

---

## 获取空间详情（Get Space Details）

获取目标空间的详细信息（包括该空间中安装的插件）。如果请求中的用户是该空间的管理员，系统会返回包括管理员在内的所有空间信息。

### 使用场景：
- 获取空间的元数据（名称、项目键、简称）
- 将项目键或简称解析为完整的空间信息
- 检查空间的管理员信息（仅当查询用户具有空间管理员权限时可见）

### API 规范：`get_space_details`
```yaml
name: get_space_details
type: api
description: Space details; if user is space admin, includes administrators.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/projects/detail" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { user_key: { type: string, required: true }, project_keys: { type: array, max_items: 100 }, simple_names: { type: array } }
outputs: { data: object }
constraints: [Permission: Permissions, project_keys or simple_names required, max 100]
```

### 使用说明：
- **user_key**：必填参数；如果用户是空间管理员，响应中会包含管理员信息。
- **project_keys** 或 **simple_names**：至少需要提供一个；最多可提供 100 个项目键。
- **data**：一个映射结构，键为项目键（project_key），值为一个对象，包含以下字段：`name`、`project_key`、`simple_name` 和 `administrators`。

---

## 获取空间中的团队成员（Get Team Members in Space）

返回所有可见性设置为“在指定项目中”（in specified projects），且“可见项目空间”（visible project spaces）设置为请求空间的团队列表。每个团队包含成员（user_keys）和管理员信息。

### 使用场景：
- 列出在某个空间内可见的所有团队
- 获取某个空间的团队成员和管理员信息
- 构建团队选择器或成员界面

### API 规范：`get_team_members_in_space`
```yaml
name: get_team_members_in_space
type: api
description: Teams visible in the space (user_keys, administrators).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/teams/all" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true } }
outputs: { data: array }
constraints: [Permission: Permissions]
```

### 使用说明：
- **project_key**：用于标识空间的路径参数。
- 响应结果包含团队的信息，包括 `team_id`、`team_name`、`user_keys`（团队成员）和 `administrators`（团队管理员）。

---

---

（注：由于提供的代码块为空，实际翻译内容将根据 API 规范和文档内容进行填充。）