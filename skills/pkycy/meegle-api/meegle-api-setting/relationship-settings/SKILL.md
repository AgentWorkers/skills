---
name: meegle-api-setting-relationship-settings
description: Meegle OpenAPI：用于工作项关系设置（包括列出、创建、更新和删除操作）。
metadata:
  openclaw: {}
---
# Meegle API — 关系设置（Relationship Settings）

该技能下的API包括：获取工作项关系列表（Get the List of Work Item Relationships）、创建工作项关系（Create Work Item Relationships）、更新工作项关系（Update Work Item Relationships）以及删除工作项关系（Delete Work Item Relationships）。

---

## 获取工作项关系列表（Get the List of Work Item Relationships）

获取指定空间内所有工作项关联关系的列表。响应数据遵循WorkItemRelation结构（id、name、relation_type、work_item_type_key/name、relation_details）。权限要求：权限管理 – 工作项实例（Permission Management – Work Item Instances）。

### 使用场景

- 在构建关系配置界面时，或需要列出哪些工作项类型之间存在关联（例如：故事（story）与冲刺（sprint）之间的关系）。
- 当需要关系ID（relation_id）或关系类型（relation_type）来创建/更新/删除工作项关系，或者将关系ID（relation_id）用于自定义字段时。
- 当需要显示每条关系的详细信息（relation_details，包括project_key、project_name、work_item_type_key、work_item_type_name）时。

### API规范：get_list_of_work_item_relationships

```yaml
name: get_list_of_work_item_relationships
type: api
description: >
  Obtain the list of work item association relationships under the space.
  Returns WorkItemRelation list: id, name, disabled, relation_type, work_item_type_key/name, relation_details.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/work_item/relation
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

outputs:
  data:
    type: array
    description: >
      List of WorkItemRelation. Each has id, name, disabled, relation_type,
      work_item_type_key, work_item_type_name, relation_details (array of
      project_key, project_name, work_item_type_key, work_item_type_name).

constraints:
  - Permission: Permission Management – Work Item Instances

error_mapping:
  1000052062: Project key is wrong (project_key incorrect; provide correct value)
```

### 使用说明

- **data**字段：
  - **id**：用于创建/更新/删除工作项关系，或在自定义字段work_item_relation_uuid中引用。
  - **relation_type**和**relation_details**用于描述关联关系（包括来源类型和目标项目/类型）。

---

## 创建工作项关系（Create Work Item Relationships）

在指定空间内添加一个新的工作项关联关系。返回新关系的ID（relation_id，格式为UUID）。权限要求：权限管理 – 工作项实例（Permission Management – Work Item Instances）。详情请参阅权限管理部分。

### 使用场景

- 当需要创建新的工作项关系时（例如：同一个空间内的故事（story）与另一个空间内的故事（story）之间的关系）。
- 当需要定义每条关系的详细信息（relation_details，包括目标项目ID（project_key）和工作项类型ID（work_item_type_key）时。
- 当需要将返回的ID（relation_id）用于自定义字段（work_item_relation_uuid），或用于更新/删除工作项关系时。

### API规范：create_work_item_relationships

```yaml
name: create_work_item_relationships
type: api
description: >
  Add a work item association relationship under the space. Returns relation_id (UUID).
  Requires project_key, work_item_type_key (source type), name, and relation_details.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/relation/create
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params: {}

inputs:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).
  work_item_type_key:
    type: string
    required: true
    description: Work item type (source). Obtain via Get work item types in space.
  name:
    type: string
    required: true
    description: Relationship name; must not duplicate an existing relationship name.
  relation_details:
    type: array
    required: true
    description: List of relationship details. Each must have project_key and work_item_type_key.
    items:
      type: object
      properties:
        project_key: { type: string }
        work_item_type_key: { type: string }

outputs:
  data:
    type: object
    description: relation_id (UUID of the newly added work item relationship).

constraints:
  - Permission: Permission Management – Work Item Instances
  - Operating user must have space administrator privileges (else 10001)

error_mapping:
  50006: Relationship name cannot be repeated (name unavailable or duplicate)
  10001: Invalid request (operating user is not admin of the space; contact admin for permissions)
```

### 使用说明

- **relation_details**中的每个条目都包含目标空间（project_key）和目标工作项类型（work_item_type_key）。
- **name**必须在该空间内的所有工作项关系中保持唯一性；如果名称重复或无效，将返回错误代码50006。
- **data.relation_id**：用于创建类型为work_item_related_select或work_item_related_multi_select的自定义字段（其中包含relation_id），或用于更新/删除该关系。
- 使用者需要具有空间管理员权限（空间管理员权限代码为10001）。

---

## 更新工作项关系（Update Work Item Relationships）

更新指定工作项关系的配置。此接口会执行**完全替换**操作（即替换原有的名称和详细信息）。权限要求：权限管理 – 工作项实例（Permission Management – Work Item Instances）。详情请参阅权限管理部分。

### 注意事项

- 此接口仅支持**完全替换**操作：提供的名称（name）和详细信息（relation_details）将覆盖原有的关系配置。

### 使用场景

- 当需要更改现有关系的名称或详细信息（包括目标项目ID（project_key）和工作项类型ID（work_item_type_key）时。
- 当需要从外部配置文件同步关系信息时；请使用从“获取工作项关系列表”（Get the List of Work Item Relationships）接口获取的relation_id。

### API规范：update_work_item_relationships

```yaml
name: update_work_item_relationships
type: api
description: >
  Update the specified work item relationship (overwrite). Requires relation_id
  from Get the List of Work Item Relationships, plus project_key, work_item_type_key,
  name, and relation_details.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/relation/update
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params: {}

inputs:
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
  name:
    type: string
    required: true
    description: Relationship name; must not duplicate another relationship name.
  relation_id:
    type: string
    required: true
    description: Work item relationship ID from Get the List of Work Item Relationships.
  relation_details:
    type: array
    required: true
    description: List of relationship details. Each must have project_key and work_item_type_key.
    items:
      type: object
      properties:
        project_key: { type: string }
        work_item_type_key: { type: string }
        project_name: { type: string }
        work_item_type_name: { type: string }

outputs:
  data:
    type: object
    description: Empty on success (no data in response).

constraints:
  - Permission: Permission Management – Work Item Instance
  - Operating user must have space administrator privileges (else 10001)

error_mapping:
  50006: Relationship name cannot be repeated (name unavailable or duplicate)
  10001: Invalid request (operating user is not admin; contact admin for permissions)
```

### 使用说明

- **relation_id**：需从“获取工作项关系列表”（Get the List of Work Item Relationships）接口的响应数据（data[]）中获取。
- 该接口会替换整个关系配置；请发送新的名称（name）和详细的关联信息（relation_details）。
- **relation_details**的结构与“创建工作项关系”（Create Work Item Relationships）接口相同；每个条目包含目标空间（project_key）和工作项类型（work_item_type_key），可选还包括目标项目名称（project_name）和工作项类型名称（work_item_type_name）。
- 如果提供的名称重复或无效，将返回错误代码50006。
- 使用者需要具有空间管理员权限（空间管理员权限代码为10001）。

---

## 删除工作项关系（Delete Work Item Relationships）

删除由**relation_id**标识的工作项关联关系。权限要求：权限管理 – 工作项实例（Permission Management – Work Item Instances）。详情请参阅权限管理部分。

### 使用场景

- 当需要从空间中移除某个工作项关系（例如：故事（story）与冲刺（sprint）之间的关系）时。
- 当**relation_id**是从“获取工作项关系列表”（Get the List of Work Item Relationships）接口获取的时。
- 在清理或重新配置关系时（先删除再重新创建关系）。

### API规范：delete_work_item_relationships

```yaml
name: delete_work_item_relationships
type: api
description: >
  Delete the work item association relationship under the space. Requires
  project_key and relation_id from Get the List of Work Item Relationships.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: DELETE
  url: https://{domain}/open_api/work_item/relation/delete
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params: {}

inputs:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).
  relation_id:
    type: string
    required: true
    description: Work item relationship ID from Get the List of Work Item Relationships.

outputs:
  data:
    type: string
    description: Null or empty on success.

constraints:
  - Permission: Permission Management – Work Item Instance

error_mapping:
  50006: RPC call error (relationship already deleted or does not exist; confirm relation_id)
```

### 使用说明

- **relation_id**：需从“获取工作项关系列表”（Get the List of Work Item Relationships）接口的响应数据（data[]）中获取。
- 如果关系已经被删除，该接口将返回错误代码50006（可能附带错误信息“关系已经被删除”）。
- 成功响应的data字段为空或为null；请检查错误代码（err_code）是否为0。