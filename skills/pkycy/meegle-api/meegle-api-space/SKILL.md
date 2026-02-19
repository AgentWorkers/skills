---
name: meegle-api-space
description: Meegle OpenAPI 用于空间（project）相关操作。
metadata:
  openclaw: {}
---
# Meegle API — 空间（Spaces）

这些 API 用于管理或查询 Meegle 中的空间（projects）。

## 功能范围

本技能涵盖以下与空间（projects）相关的操作：

- 列出所有空间
- 获取空间详细信息
- 创建或更新空间
- 其他与空间管理相关的接口

---

## 获取空间列表（Get Space List）

获取指定用户有权访问的空间列表，以及这些空间中安装了该插件的信息。

### 注意事项

- 当使用 **虚拟令牌（virtual token）** 时，只能查询“权限管理 > 选择数据范围（Permission Management > Select Data Scope）”中允许访问的空间。如需查询其他空间，请使用官方（非虚拟）令牌。

### 使用场景

- 列出用户可以访问的所有空间
- 构建空间选择器或导航界面
- 检查哪些空间中安装了该插件

### API 规范：get_space_list

```yaml
name: get_space_list
type: api
description: >
  Obtain the list of spaces that the specified user has permission to access
  and where the plugin is installed.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/projects
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  user_key:
    type: string
    required: true
    description: |
      Unique identifier of the user whose spaces to query.
      Own user_key: Double-click personal avatar in Meegle space (lower left).
      Other members: Use Get Tenant User List.
  order:
    type: array
    items: string
    required: false
    description: |
      Sort field(s). Format: prefix + field. + = ascending, - = descending; no prefix = ascending.
      Currently only last_visited is supported.
      Examples: ["last_visited"], ["+last_visited"], ["-last_visited"]

outputs:
  data:
    type: array
    items: string
    description: List of space project_keys that meet the conditions.

constraints:
  - Permission: Permission Management – Space
  - Virtual token: limited to spaces in Permission Management > Select Data Scope

error_mapping:
  30006: User not found (incorrect user_key or empty result)
  10302: User is resigned (queried user has left the company)
```

### 使用说明

- **user_key**：必填项；用于指定要查询的空间所属的用户。
- **order**：可选参数；使用 `["-last_visited"]` 可按最近访问顺序排序。

---

## 获取空间详细信息（Get Space Details）

获取目标空间的详细信息（包括插件安装情况）。如果请求中的用户是该空间的管理员，响应中会包含所有管理员信息。

### 使用场景

- 获取空间的元数据（名称、project_key、simple_name）
- 将 project_key 或 simple_name 解析为完整的空间信息
- 检查空间的管理员（仅当查询用户具有空间管理权限时可见）

### API 规范：get_space_details

```yaml
name: get_space_details
type: api
description: >
  Get detailed information of target query spaces where the plugin is installed.
  When the user is a space administrator, returns full space info including administrators.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/projects/detail
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  user_key:
    type: string
    required: true
    description: >
      Query specified user. When the user is a space administrator,
      return administrator info for the space.
  project_keys:
    type: array
    items: string
    required: false
    constraints:
      max_items: 100
    description: >
      List of space project_keys to query. Either project_keys or simple_names required. Max 100.
  simple_names:
    type: array
    items: string
    required: false
    description: >
      List of space domain names (simple_name) to query.
      Either project_keys or simple_names required.

outputs:
  data:
    type: object
    additionalProperties:
      administrators: array
      name: string
      project_key: string
      simple_name: string
    description: |
      Map of project_key → Project. Key is project_key.
      Project: name, project_key, simple_name, administrators (user_key list).
      administrators visible only if querying user has space admin permission.

constraints:
  - Permission: Developer Platform – Permissions / Permission Management
  - Either project_keys or simple_names must be provided (both can be provided)
  - project_keys max 100
```

### 使用说明

- **user_key**：必填项；用户为空间管理员时，响应中会包含管理员信息。
- **project_keys** 或 **simple_names**：至少需要提供一个；最多可提供 100 个 project_key。
- **data**：一个映射，格式为 `project_key` → `{ name, project_key, simple_name, administrators }`。

---

## 获取空间中的团队成员（Get Team Members in Space）

返回所有可见性设置为“在指定项目中（in specified projects）”且“可见项目空间（visible project spaces）”设置为请求中指定空间的团队列表。每个团队包含成员（user_keys）和管理员信息。

### 使用场景

- 列出在某个空间内可见的团队
- 获取某个空间的团队成员及管理员信息
- 构建团队选择器或成员界面

### API 规范：get_team_members_in_space

```yaml
name: get_team_members_in_space
type: api
description: >
  Return a list of teams whose visibility is "in specified projects" and
  whose visible project spaces includes the requested space.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/teams/all
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).

outputs:
  data:
    type: array
    items:
      team_id: integer
      team_name: string
      user_keys: array
      administrators: array
    description: |
      team_id: Team ID
      team_name: Team name
      user_keys: Member list (user_key)
      administrators: Administrator list (user_key)

constraints:
  - Permission: Developer Platform – Permissions / Permission Management
```

### 使用说明

- **project_key**：用于标识空间的路径参数。
- 响应内容：包含 team_id、team_name、user_keys（成员）和 administrators 的团队列表。