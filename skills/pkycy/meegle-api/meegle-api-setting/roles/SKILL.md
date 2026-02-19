---
name: meegle-api-setting-roles
description: Meegle OpenAPI 用于工作流角色相关操作：创建（create）、获取（get）、更新（update）和删除（delete）。
metadata:
  openclaw: {}
---
# Meegle API — 角色管理

该技能下的API包括：创建工作流角色、获取角色详细信息、更新工作流角色设置以及删除工作流角色配置。

---

## 创建工作流角色

在指定的工作项类型下添加一个角色，并返回新的**角色ID**。权限要求：权限管理 – 配置。

### 使用场景

- 为某种工作项类型创建工作流角色（例如：任务管理器、数据分析师等）。
- 配置角色分配方式（手动分配、分配给指定人员、分配给创建者），以及角色是否为所有者（is_owner）、是否自动加入组（auto_enter_group），或成员列表（members）。
- 当需要使用返回的角色ID来执行获取/更新/删除工作流角色操作，或进行节点/字段的角色绑定时。

### API规范：create_workflow_role

```yaml
name: create_workflow_role
type: api
description: >
  Add a role under the specified work item type. Returns role ID. role object
  includes name, is_owner, auto_enter_group, member_assign_mode, members, is_member_multi, role_alias, lock_scope.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/flow_roles/{work_item_type_key}/create_role
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtain via Get work item types in space.

inputs:
  role:
    type: object
    required: true
    description: Role configuration.
    properties:
      id:
        type: string
        description: Role ID. Optional; if not provided, auto-generated and returned on create.
      name:
        type: string
        description: Role name.
      is_owner:
        type: boolean
        description: Whether this role is the manager for the task.
      auto_enter_group:
        type: boolean
        description: Whether members are automatically added to the group.
      member_assign_mode:
        type: integer
        description: >
          1: Add manually; 2: Assign to a specified person by default; 3: Assign to the creator by default.
          When 2, members (user_key array) is used.
      members:
        type: array
        items: string
        description: Assigned members (user_key). Used when member_assign_mode is 2.
      is_member_multi:
        type: boolean
        description: Restrict to single-person configuration (false) or allow multiple.
      role_alias:
        type: string
        description: Role identifier/alias.
      lock_scope:
        type: array
        description: Lock scope (structure per product).

outputs:
  data:
    type: string
    description: Role ID (e.g. 5727769).

constraints:
  - Permission: Permission Management – Configuration

error_mapping:
  20006: Invalid param (role id already exists; change the id)
```

### 使用说明

- **role.id**：可选；如果省略，服务器会自动生成并返回角色ID。如果提供该ID且该ID已存在，则返回20006。
- **member_assign_mode**：
  - **1**：手动分配角色。
  - **2**：将角色分配给指定人员（使用user_key列表）。
  - **3**：默认情况下将角色分配给创建者。
- **members**：仅当**member_assign_mode**设置为**2**时才有意义；值类型为user_key（例如：在开发者平台中双击头像即可查看用户ID）。
- **data**：在调用获取角色详细信息、更新工作流角色设置或删除工作流角色配置的API时，需要使用返回的角色ID；同时，在进行节点/字段的角色绑定时也需要使用该ID。

---

## 获取角色详细信息

获取指定工作项类型下所有角色及其配置信息。响应数据遵循RelationDetail结构（id、name、is_owner、role_appear_mode、deletable、auto_enter_group、member_assign_mode、members、is_member_multi）。权限要求：权限管理 – 角色管理。

### 使用场景

- 列出某种工作项类型下的所有工作流角色及其配置信息。
- 当需要获取角色ID、角色分配方式、成员列表（用于更新/删除工作流角色操作）或用于用户界面展示时。
- 在构建角色管理界面或同步角色配置时。

### API规范：get_detailed_role_settings

```yaml
name: get_detailed_role_settings
type: api
description: >
  Obtain all roles and personnel configuration under the specified work item type.
  Returns list per RelationDetail: id, name, is_owner, role_appear_mode, deletable,
  auto_enter_group, member_assign_mode, members, is_member_multi.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/flow_roles/{work_item_type_key}
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtain via Get work item types in space.

outputs:
  data:
    type: array
    description: >
      List of RelationDetail. Each has id, name, is_owner, role_appear_mode,
      deletable, auto_enter_group, member_assign_mode, members (user_key array),
      is_member_multi.

constraints:
  - Permission: Permission Management – Process Roles

error_mapping:
  1000052062: Project key is wrong (project_key incorrect)
```

### 使用说明

- **data**字段：
  - **id**：在更新或删除角色时使用（调用更新工作流角色设置或删除工作流角色配置的API时）。
  - **deletable**：表示该角色是否可以被删除。
- **member_assign_mode**和**members**的含义与创建工作流角色时的参数相同。
- **role_appear_mode**：表示角色在各个产品中的显示/可见模式。

---

## 更新工作流角色设置

更新指定工作项类型下的角色信息。可以通过**role_id**或**role_alias**来识别角色（必须提供一个参数；如果同时提供两个参数，则优先使用**role_id**）。权限要求：权限管理 – 角色管理。

### 使用场景

- 更改角色的名称、所有者、是否自动加入组、角色分配方式、成员列表、是否为多成员角色（is_member_multi）、别名（role_alias）或锁定范围（lock_scope）。
- 当**role_id**或**role_alias**来自获取角色详细信息的API时使用。
- 如果**member_assign_mode**设置为2，则必须提供成员列表（members），且列表不能为空。

### API规范：update_workflow_role_settings

```yaml
name: update_workflow_role_settings
type: api
description: >
  Update a role under the specified work item type. One of role_id or role_alias
  required (role_id preferred). role object contains updated config.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/flow_roles/{work_item_type_key}/update_role
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtain via Get work item types in space.

inputs:
  role_id:
    type: string
    required: false
    description: Process role ID from Get Detailed Role Settings. One of role_id or role_alias required; role_id preferred if both sent.
  role_alias:
    type: string
    required: false
    description: Role docking identifier from Get Detailed Role Settings. One of role_id or role_alias required.
  role:
    type: object
    required: true
    description: Updated role configuration.
    properties:
      name: { type: string }
      is_owner: { type: boolean }
      auto_enter_group: { type: boolean }
      member_assign_mode: { type: integer }
      members: { type: array, items: string }
      is_member_multi: { type: boolean }
      role_alias: { type: string }
      lock_scope: { type: array }

outputs:
  data:
    type: object
    description: Empty on success.

constraints:
  - Permission: Permission Management – Process Roles
  - One of role_id or role_alias must be provided
  - When member_assign_mode is 2, members must be non-empty

error_mapping:
  20006: Invalid param (members should not be empty when member_assign_mode is 2)
  20006: Invalid param (role_id does not exist; obtain via Get Detailed Role Settings)
```

### 使用说明

- **role_id**或**role_alias**：提供一个参数来标识要更新的角色；该参数可以从获取角色详细信息的API中获取（data[]中的id或role_alias）。如果同时提供两个参数，则优先使用**role_id**。
- **role**参数的结构与创建工作流角色时的参数相同（包括name、is_owner、auto_enter_group、member_assign_mode、members、is_member_multi、role_alias、lock_scope）。
- 当**member_assign_mode**设置为2时，**members**必须是一个非空的user_key数组；否则会导致错误（返回代码20006）。

---

## 删除工作流角色配置

删除指定工作项类型下的角色配置。可以通过**role_id**或**role_alias**来识别角色（必须提供一个参数；如果同时提供两个参数，则优先使用**role_id**）。权限要求：权限管理 – 配置。

### 使用场景

- 从某种工作项类型中移除工作流角色（例如：任务管理器、数据分析师等）。
- 当**role_id**或**role_alias**来自获取角色详细信息的API时使用。
- 注意：被删除的角色不能在工作流模板节点中被引用；否则会返回错误代码20093。

### API规范：delete_workflow_role_configuration

```yaml
name: delete_workflow_role_configuration
type: api
description: >
  Delete a role under the specified work item type. One of role_id or role_alias
  required (role_id preferred). Role cannot be referenced in template nodes.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/flow_roles/{work_item_type_key}/delete_role
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtain via Get work item types in space.

inputs:
  role_id:
    type: string
    required: false
    description: Process role ID from Get Detailed Role Settings. One of role_id or role_alias required; role_id preferred if both sent.
  role_alias:
    type: string
    required: false
    description: Role docking identifier from Get Detailed Role Settings. One of role_id or role_alias required.

outputs:
  data:
    type: object
    description: Empty on success.

constraints:
  - Permission: Permission Management – Configuration
  - One of role_id or role_alias must be provided
  - Role must not be referenced in process template nodes (else 20093)

error_mapping:
  20093: Role in use (cannot delete; role is referenced in template nodes)
  20006: Invalid param (role_id does not exist or has been deleted; obtain via Get Detailed Role Settings)
```

### 使用说明

- **role_id**或**role_alias**：提供一个参数来标识要删除的角色；该参数可以从获取角色详细信息的API中获取。如果同时提供两个参数，则优先使用**role_id**。
- 如果返回代码20093，表示该角色被工作流模板节点引用，因此无法删除；此时需要先删除这些引用。
- 如果返回代码20006，表示提供的角色ID不存在或已被删除；请通过获取角色详细信息的API进行确认。