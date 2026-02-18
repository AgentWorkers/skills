---
name: meegle-api-setting-space-setting
description: Meegle OpenAPI用于空间级别的设置：工作项类型（work item types）和业务线（business lines）。
metadata:
  openclaw: {}
---
# Meegle API — 空间设置（Space Settings）

属于此技能的API包括：`Get Work Item Types in Space` 和 `Get Business Line Details in Space`。

---

## 获取空间中的工作项类型（Get Work Item Types in Space）

该API用于获取空间中所有工作项类型的列表及其对应的标识符（`work_item_type_key` / `api_name`），以便在后续API中使用。权限要求：权限管理 > 配置类别（Permission Management > Configuration Categories）。

### 使用场景

- 当您需要其他接口（如工作项的创建、读取、更新、删除操作、工作流管理、列表展示等）所需的`work_item_type_key`或`api_name`时。
- 在构建空间配置界面或列出可用的工作项类型（如故事、问题、版本、冲刺、子任务等）时。
- 当需要检查某种工作项类型是否被禁用（`is_disable`）或是否支持模型资源库（`enable_model_resource_lib`）时。

### API规范：`get_work_item_types_in_space`

```yaml
name: get_work_item_types_in_space
type: api
description: >
  Obtain all work item types in the space (WorkItemKeyType). Returns type_key, name,
  api_name, is_disable, enable_model_resource_lib for each type.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/work_item/all-types
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space unique identifier (project_key). Double-click space name in Meegle project space to obtain.

outputs:
  data:
    type: array
    description: >
      List of work item types per WorkItemKeyType: type_key, name, is_disable,
      api_name, enable_model_resource_lib. type_key / api_name are used as work_item_type_key in other APIs.

constraints:
  - Permission: Permission Management – Configuration Categories

error_mapping:
  10023: User not exist (X-User-Key in header incorrect or user not found)
```

### 使用说明

- `type_key` 和 `api_name`：可在工作项、工作流、列表等相关API中作为`work_item_type_key`使用（例如：`story`、`issue`、`version`、`sub_task`）。
- `is_disable`：表示该工作项类型是否被禁用（不同产品的值可能不同，通常2表示启用）。
- `enable_model_resource_lib`：表示该类型是否支持模型资源库功能。
- `X-User-Key`：必须是一个有效的用户键；无效或缺失的键会返回错误代码10023。

---

## 获取空间中的业务线详细信息（Get Business Line Details in Space）

该API用于获取空间的业务线信息。响应数据遵循业务线结构（以树形结构呈现，包含id、名称、角色所有者、观察者、层级ID、父级业务线、子业务线等）。有关平台的相关功能，请参阅“业务线配置”（Business Line Configuration）。权限要求：权限管理 – 配置（Permission Management – Configuration）。

### 使用场景

- 在构建需要显示空间内所有业务线信息的界面时。
- 当您需要获取特定业务线的角色所有者、观察者、超级管理员信息，或了解业务线的层级结构（父级、子级、层级ID）时。
- 在验证或显示工作项的业务线ID时。

### API规范：`get_business_line_details_in_space`

```yaml
name: get_business_line_details_in_space
type: api
description: >
  Obtain business line information of the space. Returns list of Business objects
  (tree: id, name, role_owners, watchers, level_id, parent, children, disabled, labels, order, project, super_masters).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/business/all
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space unique identifier (project_key). Double-click space name in Meegle project space to obtain.

outputs:
  data:
    type: array
    description: >
      List of Business objects. Each has id, name, role_owners (role, owners, name),
      watchers, level_id, parent, disabled, labels, order, project, super_masters,
      children (nested Business objects with same structure).

constraints:
  - Permission: Permission Management – Configuration

error_mapping:
  1000052062: Project key is wrong (not found simple name; project_key incorrect)
```

### 使用说明

- `data`：根级数组表示最高级别的业务线；每个元素可以包含子业务线（形成树结构）。
- `parent`：指向父级业务线的ID。
- `level_id`：表示业务线的层级。
- `role_owners`：可以是`{ role, owners }`类型的数组，也可以是以角色为键的对象（例如：`role_test: { name, owners, role }`）；`owners`表示该业务线的所有者用户ID列表。
- `watchers` / `super_masters`：表示观察者或超级管理员的用户ID列表。
- `project`：表示当前操作的空间的标识符。

- 有关产品的业务线配置，请参阅平台文档中的“业务线配置”（Business Line Configuration）部分。