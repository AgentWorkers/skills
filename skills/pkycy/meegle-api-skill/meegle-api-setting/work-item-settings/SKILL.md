---
name: meegle-api-setting-work-item-settings
description: Meegle OpenAPI：用于工作项类型的基本设置（获取/更新）。
metadata:
  openclaw: {}
---
# Meegle API — 工作项设置（Work Item Settings）

该技能涵盖的API包括：获取工作项的基本设置（Get Basic Work Item Settings）以及更新工作项的基本信息设置（Update Work Item Basic Information Settings）。

---

## 获取工作项的基本设置（Get Basic Work Item Settings）

用于获取指定工作项类型的基本信息配置（如类型键、名称、工作流程模式（flow_mode）、计划时间/估算时间/实际工作时间（schedule/estimate/actual-work-time）、关联角色（belong_roles）、资源库设置等）。权限要求：权限管理 – 工作项实例（Permission Management – Work Item Instance）。详情请参阅权限管理（Permission Management）。

### 使用场景

- 在构建工作项类型配置界面或编辑前显示当前设置时使用（与更新工作项基本信息设置结合使用）
- 当需要了解工作流程模式（workflow或stateflow）、是否启用计划功能（enable_schedule）、字段键/名称、关联角色或资源库设置时使用
- 当需要检查实际工作时间是否通过Open API管理（actual_work_time_switch）或是否启用模型资源库功能（enable_model_resource_lib）时使用

### API规范：get_basic_work_item_settings

```yaml
name: get_basic_work_item_settings
type: api
description: >
  Obtain basic information configuration of the specified work item type:
  type_key, name, flow_mode, api_name, description, is_disabled, is_pinned,
  enable_schedule, schedule/estimate/actual_work_time field keys and names,
  belong_roles, actual_work_time_switch, enable_model_resource_lib, resource_lib_setting.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/work_item/type/{work_item_type_key}
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
    description: Work item type. Obtain via Get work item types in space; must match the type to query.

outputs:
  data:
    type: object
    description: >
      type_key, name, flow_mode (workflow | stateflow), api_name, description,
      is_disabled, is_pinned, enable_schedule, schedule_field_key/name,
      estimate_point_field_key/name, actual_work_time_field_key/name,
      belong_roles (id, name, key), actual_work_time_switch, enable_model_resource_lib,
      resource_lib_setting (enable_roles, enable_fields with field_alias, field_key, field_name, field_type_key).

constraints:
  - Permission: Permission Management – Work Item Instance

error_mapping:
  30014: Work item type not found (no type for given work_item_type_key)
```

### 使用说明

- **flow_mode**：
  - `workflow`：节点流程（node flow）
  - `stateflow`：状态流程（state flow）
- **enable_schedule**：控制整体计划功能：
  - 如果设置为`true`，计划时间/估算时间/实际工作时间字段将生效；
  - 如果设置为`false`，仅适用于状态流程（state-flow）类型的工作项。
- **belong_roles**：一个包含`id`、`name`、`key`的数组，表示与计划和评分估算相关的角色。
- **resource_lib_setting**：
  - 当`enable_model_resource_lib`设置为`true`时，`enable_roles`和`enable_fields`用于描述资源库的配置。

---

## 更新工作项的基本信息设置（Update Work Item Basic Information Settings）

用于更新指定工作项类型的基本信息配置（如描述、是否禁用/固定、计划时间/估算时间字段、关联角色等）。权限要求：权限管理 – 工作项（Permission Management）。详情请参阅权限管理（Permission Management）。

### 使用场景

- 当需要更改工作项类型设置（如描述、是否禁用、是否固定、计划时间/估算时间字段、关联角色或实际工作时间开关）时使用
- 当需要配置哪些字段用于计划、估算和记录实际工作时间时使用
- 当需要启用或禁用用于记录工作项工作时间的API功能时使用

### API规范：update_work_item_basic_information_settings

```yaml
name: update_work_item_basic_information_settings
type: api
description: >
  Update basic information configuration of the specified work item type:
  description, is_disabled, is_pinned, enable_schedule, field keys, belong_role_keys, actual_work_time_switch.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: PUT
  url: https://{domain}/open_api/{project_key}/work_item/type/{work_item_type_key}
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
    description: Work item type. Obtain via Get work item types in space; must match the type to update.

inputs:
  description:
    type: string
    required: false
    description: Work item type description.
  is_disabled:
    type: boolean
    required: false
    description: true = disable this work item type; false = enabled.
  is_pinned:
    type: boolean
    required: false
    description: true = show as entry in navigation bar; false = do not show.
  enable_schedule:
    type: boolean
    required: false
    description: true = work item supports overall scheduling; false = does not.
  schedule_field_key:
    type: string
    required: false
    description: Field key for scheduling; use a date-range type field.
  estimate_point_field_key:
    type: string
    required: false
    description: Field key for estimated score; use a numeric field.
  actual_work_time_field_key:
    type: string
    required: false
    description: Field key for actual working hours; use a numeric field.
  belong_role_keys:
    type: array
    items: string
    required: false
    description: >
      Keys of associated roles for scheduling and score estimation (score split among roles).
      Roles must already exist in process role configuration.
  actual_work_time_switch:
    type: boolean
    required: false
    description: Whether to enable the API for registering work-item working hours.

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Permission Management – Work Items
  - Current user must have space admin permission (else 10005)

error_mapping:
  10005: No project admin permission (current user is not space administrator)
  30014: Work item not found (work_item_type_key incorrect)
```

### 使用说明

- **work_item_type_key**：需从“获取工作项类型”（Get Work Item Types in Space）接口中获取（例如`story`、`issue`）。如果类型错误或不存在，将返回错误代码30014。
- **belong_role_keys**：API中的参数名称为`belong_role_keys`（某些示例可能显示为`belong_roles_keys`）。相关角色必须存在于流程角色配置中。
- **schedule_field_key**、**estimate_point_field_key**、**actual_work_time_field_key**：使用从“获取字段信息”（Get Field Information）接口中获取的字段键。计划时间使用日期范围格式；估算时间和实际工作时间使用数值格式。
- 需要空间管理员权限（非管理员用户需要权限代码10005）。

---