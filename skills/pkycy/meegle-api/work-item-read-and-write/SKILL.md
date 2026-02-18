---
name: meegle-api-work-item-read-and-write
description: >
  Meegle OpenAPI 用于创建、读取和更新工作项（work items）。  
  先决条件：需要 token 和域名（详情请参阅 skill meegle-api-users）。
metadata:
  openclaw: {}
  required_credentials:
    domain: "From meegle-api-users"
    plugin_access_token_or_user_access_token: "From meegle-api-users (obtain token first)"
---
# Meegle API — 工作项的读写操作

## 创建、获取和更新Meegle空间中的工作项

### 先决条件：  
首先获取域名和访问令牌；请参考技能“meegle-api-users”。

---

## 获取工作项创建元数据  
检索Meegle空间中特定工作项类型的创建元数据（字段配置）。这些元数据用于正确构建创建或更新工作项的请求体。

### 使用场景：  
- 在创建或更新工作项之前，以获取字段定义、必填字段和默认值  
- 在为创建/更新API构建`field_value_pairs`时  
- 当需要选项ID、复合字段结构或角色分配配置时  

### API规范：`get_work_item_creation_metadata`  
```yaml
name: get_work_item_creation_metadata
type: api
description: >
  Retrieve creation metadata (field configuration) for a specific work item type
  in a Meegle space. This metadata is required to correctly construct payloads
  for creating or updating work items.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/meta
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space project_key or simple_name.
      project_key can be obtained by double-clicking the space name.
  work_item_type_key:
    type: string
    required: true
    description: Work item type key in the space

outputs:
  data:
    type: array
    description: >
      Field configuration list (FieldConf), including required fields,
      default values, compound fields, and role assignments.

error_mapping:
  20044: Work item type has been disabled
  30014: Work item type not found
```

### 使用说明：  
- `project_key`, `work_item_type_key`：用于标识空间和工作项类型的路径参数。  
- 在调用“Create Work Item”之前，先使用此API获取字段元数据，然后根据结果构建带有正确选项ID和结构的`field_value_pairs`。

---

## 获取工作项详情  
检索指定Meegle空间和工作项类型下的一个或多个工作项的详细信息。返回包括系统字段、自定义字段、工作流状态和节点/状态信息的完整详情页面数据。

### 使用场景：  
- 当需要通过ID获取特定工作项的完整详情时  
- 当需要工作流状态历史记录、当前节点或全部字段列表时  
- 当需要构建详情视图或同步工作项数据时  

### API规范：`get_work_item_details`  
```yaml
name: get_work_item_details
type: api
description: >
  Retrieve detailed information for one or more work item instances under a
  specified Meegle space and work item type. Returns full detail-page data
  including system fields, custom fields, workflow status, and node/state info.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/query
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space identifier. Can be the space project_key or space domain name
      (simple_name).
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type key (e.g. story, bug). Obtainable via
      "Get work item types in the space".

inputs:
  work_item_ids:
    type: array
    items: integer
    required: true
    constraints:
      max_items: 50
    description: >
      List of work item instance IDs. Maximum 50 per request.
  fields:
    type: array
    items: string
    required: false
    description: |
      Field filtering rules.
      - Specify fields: ["owner","description"]
      - Exclude fields: ["-owner","-description"]
      These two modes cannot be mixed.
  expand:
    type: object
    required: false
    description: Additional expansion parameters (reserved for extended query behavior).

outputs:
  data:
    type: array
    description: >
      Work item detail objects. Includes base attributes (id, name, status,
      timestamps), workflow state history, current nodes, and full field list.

constraints:
  - work_item_ids max 50 per request

error_mapping:
  30005: Work item not found (invalid or non-existent work_item_ids)
  20028: work_item_ids exceeds 50
  30014: Work item type not found (invalid work_item_type_key)
```

### 使用说明：  
- `project_key`, `work_item_type_key`：用于标识空间和工作项类型的路径参数。  
- `work_item_ids`：必填；每次请求最多支持50个ID。  
- `fields`：使用正数值指定要返回的字段，或前缀加上`-`来排除某些字段；不要混合使用不同的字段获取模式。

---

## 创建工作项  
在Meegle空间中创建一个新的工作项。支持多种工作项类型、模板和自定义字段。需要具备“Work Items”权限。  

### 使用场景：  
- 当需要创建新的任务、问题或其他类型的工作项时  
- 当需要将结构化的工作内容保存到Meegle中时  
- 当需要程序化地初始化工作流或计划任务时  

### API规范：`create_work_item`  
```yaml
name: meegle.create_work_item
description: >
  Create a new work item in a specified Meegle space.
  Supports different work item types, templates, and custom fields.
  Requires permission: Work Items.

when_to_use:
  - When creating a new task, story, bug, or other work item
  - When an AI needs to persist structured work into Meegle
  - When initializing workflows or planning items programmatically

http:
  method: POST
  path: /open_api/{project_key}/work_item/create
  auth: plugin_access_token

path_parameters:
  project_key:
    type: string
    required: true
    description: Space ID (project_key) or space domain name (simple_name)

body_parameters:
  work_item_type_key:
    type: string
    required: false
    description: Work item type key (e.g. story, task, bug)

  template_id:
    type: integer
    required: false
    description: >
      Work item process template ID.
      If omitted, the default template of the work item type is used.

  name:
    type: string
    required: false
    description: Work item name

  required_mode:
    type: integer
    required: false
    default: 0
    enum:
      - 0  # do not validate required fields
      - 1  # validate required fields and fail if missing

  field_value_pairs:
    type: list[object]
    required: false
    description: >
      Field configuration list.
      Field definitions must match metadata from
      "Get Work Item Creation Metadata".
    item_schema:
      field_key:
        type: string
        required: true
      field_value:
        type: any
        required: true
      notes:
        - For option/select fields, value must be option ID
        - Cascading fields must follow configured option hierarchy
        - role_owners must follow role + owners structure

response:
  data:
    type: integer
    description: Created work item ID
  err_code:
    type: integer
  err_msg:
    type: string

error_handling:
  - code: 30014
    meaning: Work item type not found or invalid
  - code: 50006
    meaning: Role owners parsing failed or template invalid
  - code: 20083
    meaning: Duplicate fields in request
  - code: 20038
    meaning: Required fields not set

constraints:
  - name must not also appear in field_value_pairs
  - template_id must not appear in field_value_pairs
  - option-type fields must use option ID, not label
  - role_owners default behavior depends on process role configuration

examples:
  minimal:
    project_key: doc
    body:
      work_item_type_key: story
      name: "New Story"

  full:
    project_key: doc
    body:
      work_item_type_key: story
      template_id: 123123
      name: "Example Work Item"
      field_value_pairs:
        - field_key: description
          field_value: "Example description"
        - field_key: priority
          field_value:
            value: "xxxxxx"
        - field_key: role_owners
          field_value:
            - role: rd
              owners:
                - testuser
```

### 使用说明：  
- `project_key`：必填的路径参数。可以使用空间ID（`project_key`）或空间域名（`simple_name`）。  
- `name`：工作项名称；不要在`field_value_pairs`中也发送名称。  
- `field_value_pairs`：在此处发送其他字段（描述、优先级、分配者等）；对于选项类型的字段，请使用选项ID，而不是显示标签。  
- 在创建之前，请先调用“Get Work Item Creation Metadata”以获取该类型和模板的字段元数据，然后据此构建`field_value_pairs`。

---

## 更新工作项  
更新指定空间和工作项类型下的一个或多个可编辑字段。只能修改元数据和权限允许的字段。模板和计算字段不支持修改。  

### 使用场景：  
- 当需要修改现有工作项的字段（名称、描述、状态、分配者等）时  
- 当需要更新工作流状态或自定义字段时  
- 当需要将外部更改同步到Meegle中时  

### API规范：`update_work_item`  
```yaml
name: update_work_item
type: api
description: >
  Update one or more editable fields of a Meegle work item instance under a
  specified space and work item type. Only fields allowed by metadata and
  permissions can be modified. Template and calculated fields are not supported.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: PUT
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space identifier. Can be project_key or space domain name (simple_name).
  work_item_type_key:
    type: string
    required: true
    description: Work item type key (e.g. story, bug).
  work_item_id:
    type: string
    required: true
    description: Work item instance ID.

inputs:
  update_fields:
    type: array
    items:
      type: object
      properties:
        field_key:
          type: string
          required: true
          description: Field identifier
        field_value:
          type: any
          required: true
          description: >
            New field value. For option fields, pass option ID (value),
            not the label.
    required: true
    description: >
      List of fields to update. Each update overwrites the previous value.
      Field definitions must follow metadata from
      "Get Work Item Creation Metadata".

outputs:
  description: Update succeeded

constraints:
  - Cascading option fields must follow configured hierarchy
  - Option-type fields require option ID, not name
  - role_owners behavior depends on process role configuration
  - Template, voting, and calculated fields cannot be updated

error_mapping:
  20007: Work item has already reached terminal status; terminated items cannot be modified
  30009: Field not found (invalid field_key)
  30005: Work item not found (invalid work_item_id)
  50006: No right to edit / WorkItemValue limit exceeded
  20090: Request blocked (field cannot be updated or is calculated)
  20050: Failed to check field (field option invalid due to configuration change)
  10001: Operation not permitted (no permission)
  20014: Project and work item do not match (project_key and work item not in same space)
  1000051743: Can not find user info (invalid X-User-Key)
  10211: Token info invalid (token expired or invalid)
```

### 使用说明：  
- `project_key`, `work_item_type_key`, `work_item_id`：用于标识目标工作项的路径参数。  
- `update_fields`：形如`{field_key, field_value}`的数组；对于选项类型的字段，请使用选项ID，而不是字段标签。  
- 在创建之前，请先调用“Get Work Item Creation Metadata”以了解可编辑字段及其结构。  
- 已终止的工作项无法被更新。模板、投票和计算字段为只读状态。

---

## 中止或恢复工作项  
终止（中止）或恢复指定空间和工作项类型下的工作项实例。用于将工作项标记为终止状态或恢复为活动状态。  

### 使用场景：  
- 当需要终止工作项（如取消、重复项、测试项等）时  
- 当需要恢复之前终止的工作项（如重新启动、回滚、测试）时  
- 当需要管理工作项的生命周期（活动状态 vs 终止状态）时  

### API规范：`abort_or.resume_work_item`  
```yaml
name: abort_or_resume_work_item
type: api
description: >
  Terminate (abort) or resume a work item instance under a specified space
  and work item type. Used to mark work items as terminated or restore them
  back to active status.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: PUT
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/abort
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space identifier. Can be project_key or space domain name (simple_name).
  work_item_type_key:
    type: string
    required: true
    description: Work item type key (e.g. story, bug).
  work_item_id:
    type: string
    required: true
    description: Work item instance ID.

inputs:
  is_aborted:
    type: boolean
    required: false
    description: |
      true: terminate the work item
      false: resume the work item
  reason:
    type: string
    required: false
    description: >
      Reason for termination or recovery.
      Required when reason_option is "other".
  reason_option:
    type: string
    required: false
    description: |
      Termination reason options:
      - cancel: Cancel
      - repeat: Duplicate / merge
      - test: Test
      - other: Other
      Recovery reason options:
      - restart: Restart
      - rollback: Roll back due to misoperation
      - test: Test
      - other: Other

outputs:
  description: Operation succeeded

constraints:
  - Requires Permission Management - Work Item Instances permission
  - reason_option should match configured termination reasons in the space

error_mapping:
  20007: Work item is already aborted (already terminated)
  20008: Work item is already restored (already resumed)
  30005: Work item not found (does not exist or type does not match)
  20090: Request intercepted (request or operation was intercepted)
```

### 使用说明：  
- `project_key`, `work_item_type_key`, `work_item_id`：用于标识目标工作项的路径参数。  
- `is_aborted`：`true`表示终止，`false`表示恢复。  
- `reason_option`：必须与空间配置的选项匹配；在必要时可以使用`other`和`reason`参数。

---

## 批量更新工作项字段  
批量更新指定空间和工作项类型下的多个工作项实例的单一字段。支持APPEND、UPDATE和REPLACE三种模式，并对字段类型有限制。  

### 使用场景：  
- 当需要一次性更新多个工作项的相同字段时（例如批量更改状态、批量分配分配者）  
- 当需要在多选字段或人员字段中追加或替换值时  
- 当需要通过`task_id`异步查询批量更新进度时  

### API规范：`batch_update_work_item_field`  
```yaml
name: batch_update_work_item_field
type: api
description: >
  Batch update a single field across multiple work item instances
  under a specified space and work item type. Supports APPEND, UPDATE,
  and REPLACE modes with field-type restrictions.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/batch_update
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_key:
    type: string
    required: true
    description: Meegle project space identifier (project_key).
  work_item_type_key:
    type: string
    required: true
    description: Work item type key (e.g. story, bug).
  work_item_ids:
    type: array
    items: integer
    required: true
    constraints:
      max_items: 50
    description: List of work item IDs to update. Max 50 IDs per request.
  update_mode:
    type: string
    required: true
    enum: [APPEND, UPDATE, REPLACE]
    description: |
      APPEND: Append values (supports multi-user, multi-select, multi-associated).
      UPDATE: Overwrite values (not supported for calculated or external signal fields).
      REPLACE: Replace values (supports single/multi select, cascading select,
      personnel fields, associated work item fields).
  field_key:
    type: string
    required: true
    description: >
      Field ID to be modified. Batch update supports only one field at a time.
  before_field_value:
    type: any
    required: false
    description: >
      Original field value to be replaced.
      Required only when update_mode = REPLACE.
  after_field_value:
    type: any
    required: true
    description: >
      Target field value after the operation.
      Can be empty, which means deletion of the field value.

outputs:
  data:
    type: object
    properties:
      task_id: string
    description: >
      Batch update task created successfully.
      Use task_id to query progress.

constraints:
  - QPS limit: 1
  - Requires Permission Management - Work Item Instances
  - Only one field can be updated per batch request
  - Max 50 work_item_ids per request
  - Field type support depends on update_mode

error_mapping:
  1000052062: Project key is wrong (invalid project_key)
  50006: ErrOAPIBatchUpdateOverLimit (more than 50 work_item_ids)
```

### 使用说明：  
- `project_key`, `work_item_type_key`：用于标识空间和工作项类型。  
- `work_item_ids`：每次请求最多支持50个ID。  
- `update_mode`：APPEND（添加）、UPDATE（覆盖）、REPLACE（替换原有值）。不同模式支持的字段类型不同。  
- `before_field_value`：当`update_mode=REPLACE`时必填；用于匹配并替换原始值。  
- `after_field_value`：目标值；为空表示删除该字段的值。  
- 返回`task_id`——可以使用`Get Batch Update Progress`异步查询批量更新进度。  

---

## 查询批量更新进度  
查询批量更新工作项字段任务的执行进度和结果。此API需与`batch_update_work_item_field`配合使用。  

### 使用场景：  
- 在提交批量更新任务后，通过轮询来检查完成状态  
- 当需要获取成功/失败的数量和列表（`success_sub_task_list`, `fail_sub_task_list`）时  
- 当需要调试批量失败情况时（`error_scenes`）  

### API规范：`get_batch_update_progress`  
```yaml
name: get_batch_update_progress
type: api
description: >
  Query execution progress and results of a batch work item field update task.
  Used together with the Batch Update Work Item Field API.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/task_result?task_id={{task_id}}
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  task_id:
    type: string
    required: true
    description: >
      Task ID returned by the Batch Update Work Item Field interface.
      Pass as query parameter (?task_id=...).

outputs:
  data:
    type: object
    properties:
      task_id: string
      task_status: string
      total: integer
      success_total: integer
      error_total: integer
      success_sub_task_list: array
      fail_sub_task_list: array
      error_scenes: array
    description: |
      task_status: SUCCESS | IDLE | RUNNING | FAILED | CANCELED | NOT_EXIST
      success_sub_task_list: List of successfully updated work item IDs
      fail_sub_task_list: List of failed work item IDs
      error_scenes: Failure scenarios (e.g. RelationCaseLoops, RelationCaseLevelExceeds,
        DuplicationCheckEnabledForThisField, NoPermissionToModify, WorkItemTerminated)

constraints:
  - No permission application required
  - QPS limit: 1
  - Typically polled after submitting a batch update task
```

### 使用说明：  
- `task_id`：作为查询参数，从`batch_update_work_item_field`的响应中获取。  
- `task_status`： SUCCESS、IDLE、RUNNING、FAILED、CANCELED或NOT_EXIST。  
- 在批量更新后调用此API以跟踪进度并获取成功/失败列表。  

## 冻结或解冻工作项  
冻结或解冻指定Meegle项目空间中的工作项实例。冻结会阻止工作项进入下一阶段；解冻会恢复其正常流程。  

### 使用场景：  
- 当需要暂时阻止工作项进入下一阶段时  
- 当需要恢复之前被冻结的工作项的流程时  
- 当需要管理正在进行中的工作项的暂停或审核流程时  

### API规范：`freeze_or_unfreeze_work_item`  
```yaml
name: freeze_or_unfreeze_work_item
type: api
description: >
  Freeze or unfreeze a work item instance in a specified Meegle project space.
  Freezing prevents the work item from moving to the next stage; unfreezing restores normal flow.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: PUT
  url: https://{domain}/open_api/work_item/freeze
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_key:
    type: string
    required: true
    description: >
      Unique identifier of the Meegle project space (project_key or simple_name).
  work_item_id:
    type: integer
    required: true
    description: Work item instance ID.
  is_frozen:
    type: boolean
    required: true
    description: |
      true = freeze the work item
      false = unfreeze the work item

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Requires Permission Management – Work Item Instance
  - Applies only to the specified work item instance
  - Used to temporarily block or restore workflow progression

error_mapping:
  1000052062: Project key is wrong (incorrect project_key)
```

### 使用说明：  
- `project_key`：空间标识符（`project_key`或`simple_name`）。  
- `work_item_id`：目标工作项实例ID。  
- `is_frozen`：`true`表示冻结（阻止阶段转换），`false`表示解冻。  

---

## 更新复合字段  
更新、添加或删除Meegle工作项中的复合字段组。支持对复合字段组数据的添加/更新/删除操作。  

### 使用场景：  
- 当需要向工作项添加新的复合字段组时  
- 当需要更新现有的复合字段组数据时  
- 当需要删除复合字段组时  

### API规范：`update_compound_field`  
```yaml
name: update_compound_field
type: api
description: >
  Update, add, or delete a compound (composite) field group on a Meegle work item.
  Supports add / update / delete operations on grouped compound field data.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/field_value/update_compound_field
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
  work_item_id:
    type: integer
    required: true
    description: Work item instance ID.
  field_key:
    type: string
    required: false
    description: >
      ID of the compound field. Cannot be empty at the same time as field_alias.
  field_alias:
    type: string
    required: false
    description: >
      Alias of the compound field. Cannot be empty at the same time as field_key.
  group_uuid:
    type: string
    required: false
    description: |
      Identifier of the compound field group.
      Required for update / delete.
      Must NOT be provided for add.
  action:
    type: string
    required: true
    enum: [add, update, delete]
    description: |
      add    = add new group(s)
      update = update existing group
      delete = delete existing group
  fields:
    type: array
    items: object
    required: false
    description: |
      Compound field data (FieldValuePair list).
      add: multiple groups
      update: single group
      delete: not required

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Requires Permission Management – Work Items
  - field_key or field_alias must be provided (one only, cannot both be empty)
  - group_uuid required for update / delete; must NOT be provided for add
  - Target field must be a compound field
  - Use Get Work Item Details with need_group_uuid_for_compound=true to obtain group_uuid

error_mapping:
  1000050244: Work item not found (does not exist or was deleted)
  1000050156: ProjectKey does not match (project_key does not match work item's space)
  1000050248: Field not found (compound field does not exist)
  1000050156: Invalid field (only compound_field supported)
```

### 使用说明：  
- `field_key`或`field_alias`：提供一个参数，用于标识复合字段。  
- `group_uuid`：更新/删除操作时必填；添加操作时可以省略。可通过`get_work_item_details`（设置`need_group_uuid_for_compound=true`）获取。  
- `action`：`add`（添加新组）、`update`（更新现有组）、`delete`（删除组）。  
- `fields`：添加操作时指定多个组；更新操作时指定单个组；删除操作时省略。  

## 获取工作项变更日志  
查询指定空间内一个或多个Meegle工作项实例的变更记录。支持按操作类型、操作方式、模块、时间范围进行过滤和分页。  

### 使用场景：  
- 当需要审计或审查工作项的变更历史时  
- 当需要跟踪谁在何时进行了哪些更改时  
- 当需要按操作类型（创建、修改、删除、终止、恢复等）进行过滤时  

### API规范：`get_work_item_change_log`  
```yaml
name: get_work_item_change_log
type: api
description: >
  Query operation (change) records of one or more Meegle work item instances
  within a specified space. Supports filtering by operator, operation type,
  module, time range, and pagination.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/op_record/work_item/list
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_key:
    type: string
    required: true
    description: Space ID (project_key).
  work_item_ids:
    type: array
    items: integer
    required: true
    constraints:
      max_items: 50
    description: List of work item IDs to query. Maximum 50 per request.
  start_from:
    type: string
    required: false
    description: Pagination cursor. Use the value returned by the previous request.
  operator:
    type: array
    items: string
    required: false
    description: |
      Operator identifiers.
      - user: user_key
      - auto: automation rule ID
  operator_type:
    type: array
    items: string
    required: false
    enum: [user, auto, system, calc_field, plugin, others]
    description: Operator trigger source type.
  source_type:
    type: array
    items: string
    required: false
    enum: [auto, plugin]
    description: Operation channel type.
  source:
    type: array
    items: string
    required: false
    description: |
      Operation channel identifier.
      - auto: automation rule ID
      - plugin: plugin ID
  operation_type:
    type: array
    items: string
    required: false
    enum: [modify, create, delete, terminate, restore, complete, rollback, add, remove]
    description: Operation action types.
  start:
    type: integer
    required: false
    description: Start time (milliseconds timestamp). Must be used with end. Max range: 7 days.
  end:
    type: integer
    required: false
    description: End time (milliseconds timestamp). Must be used with start. Max range: 7 days.
  op_record_module:
    type: array
    items: string
    required: false
    enum: [work_item_mod, node_mod, sub_task_mod, field_mod, role_and_user_mod, baseline_mod]
    description: Operation record module type.
  page_size:
    type: integer
    required: false
    default: 50
    constraints:
      max: 200
    description: Records per page. Max 200, default 50.

outputs:
  data:
    type: object
    properties:
      has_more: boolean
      start_from: string
      op_records: array
      total: integer
    description: |
      has_more: Whether more records exist
      start_from: Pagination cursor for next request
      op_records: Operation record list
      total: Total number of records

constraints:
  - Requires Permission Management – Work Item Instance
  - Historical records before July 2, 2024 are NOT supported
  - Pagination is cursor-based via start_from
  - work_item_ids is mandatory (max 50)
  - Time range (start, end) max 7 days

error_mapping:
  20006: Invalid param (one or more parameters invalid)
  20005: Missing param (required parameters missing)
  20013: Invalid time interval (range exceeds 7 days)
```

### 使用说明：  
- `work_item_ids`：必填；每次请求最多支持50个ID。  
- `start_from`：用于指定下一页的起始位置；可以从之前的响应中获取`start_from`。  
- `start `/ end`：一起使用；以13位毫秒时间戳表示；时间范围最多为7天。  
- `operation_type`：按创建、修改、删除、终止、恢复、完成、回滚、添加、删除等操作类型进行过滤。  

## 获取工作项资源实例详情  
查询指定Meegle工作项*资源库*实例的详细信息，包括字段数据。仅支持启用了资源库的工作项；非资源实例和值为空的字段不会被返回。  

### 使用场景：  
- 当需要查询资源库工作项实例（例如可重用组件、模板）时  
- 当需要获取资源工作项的完整字段数据时  
- 当需要与支持资源库的空间集成时  

### API规范：`get_work_item_resource_instance_detail`  
```yaml
name: get_work_item_resource_instance_detail
type: api
description: >
  Query detailed information of specified Meegle work item *resource library*
  instances, including field data. Only resource-library-enabled work items
  are supported; non-resource instances and null-value fields are not returned.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/resource/query
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_key:
    type: string
    required: true
    description: Project space ID (project_key).
  work_item_ids:
    type: array
    items: integer
    required: true
    constraints:
      max_items: 50
    description: List of resource work item IDs. Maximum 50 per request.
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type key. Obtainable via "Get work item types in the space" API.
  fields:
    type: array
    items: string
    required: false
    description: >
      Specify which fields to return. If omitted, all fields are returned.
      Null-value fields are never returned.
  expand:
    type: object
    required: false
    description: Extended parameters for future expansion.

outputs:
  data:
    type: array
    description: List of resource work item instances.
    item_properties:
      id: integer
      name: string
      project_key: string
      work_item_type_key: string
      template_id: integer
      template_type: string
      simple_name: string
      created_by: string
      updated_by: string
      created_at: integer
      updated_at: integer
      fields: array

constraints:
  - Requires Permission Management – Work Item Instance
  - Only resource-library-enabled work items are supported
  - Non-resource instances will not be returned
  - Fields with null values are automatically filtered out
  - Max 50 work_item_ids per request

error_mapping:
  30005: Work item not found (one or more work items do not exist)
  20005: Invalid work_item_ids parameter
  1000050178: work_item_ids exceeds 50
```

### 使用说明：  
- `work_item_ids`：资源工作项ID列表；最多支持50个ID。仅返回资源库实例。  
- `work_item_type_key`：必填。可以使用“Get work item types in the space”来获取。  
- `fields`：可选；省略该参数可返回所有字段。值为空的字段不会包含在响应中。  

## 更新工作项资源实例  
更新指定Meegle工作项**资源库实例**的字段。仅支持资源字段；非资源字段和角色会被忽略。字段更新会覆盖现有值（不会追加/合并）。  

### 使用场景：  
- 当需要更新资源库工作项实例（例如可重用组件、模板）时  
- 当需要修改资源字段值时  
- 当需要将外部数据同步到资源工作项中时  

### API规范：`update_work_item_resource_instance`  
```yaml
name: update_work_item_resource_instance
type: api
description: >
  Update fields of a specified Meegle work item **resource library instance**.
  Only resource fields are supported. Non-resource fields or roles are ignored.
  Field updates overwrite existing values (not append/merge).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/resource/update
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_key:
    type: string
    required: false
    description: Project space ID (project_key).
  work_item_type_key:
    type: string
    required: false
    description: Work item type key.
  work_item_id:
    type: integer
    required: false
    description: Resource work item ID.
  update_fields:
    type: array
    items:
      type: object
      properties:
        field_key:
          type: string
          required: true
        field_value:
          type: any
          required: true
          description: >
            Field value. Must follow Meegle Field & Attribute Parsing Format.
    required: false
    description: >
      Fields to update. Values overwrite previous values entirely.

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Requires Permission Management – Work Item Instance
  - Resource library must be enabled for the work item
  - Only resource fields are processed; non-resource fields or roles ignored
  - Field updates are full overwrite, not partial append/merge
  - No duplicate field_key in update_fields

error_mapping:
  30014: Work item type key not found (incorrect project_key or work item not found)
  1000053593: NonresourceFieldsRolesUnsupported (one or more fields are not resource fields)
  1000050438: Duplication field exist (duplicate field_key in update_fields)
  1000050183: Update field invalid (update_fields format is invalid)
```

### 使用说明：  
- `project_key`, `work_item_type_key`, `work_item_id`：用于标识目标资源工作项。  
- `update_fields`：形如`{field_key, field_value}`的数组；字段值会覆盖现有值（不会追加）。使用Meegle的字段和属性解析格式。  
- 仅更新资源字段；非资源字段和角色会被忽略。  

## 搜索工作项资源实例  
根据复杂的过滤条件搜索并列出Meegle中的**工作项资源库实例**。支持通过`search_after`进行分页和按需选择字段。仅当工作项类型启用了资源仓库时才可用。  

### 使用场景：  
- 当需要在不同空间/类型中搜索资源库工作项时  
- 当需要根据创建时间、创建者、更新者、更新时间、资源ID进行过滤时  
- 当需要基于游标进行分页和字段选择时  

### API规范：`search_work_item_resource_instances`  
```yaml
name: search_work_item_resource_instances
type: api
description: >
  Search and list **work item resource library instances** in Meegle based on
  complex filtering conditions. Supports pagination via search_after and
  on-demand field selection. Only available when the resource repository
  is enabled for the work item type.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/resource/search/params
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  data_sources:
    type: array
    items:
      type: object
      properties:
        project_key:
          type: string
          required: true
          description: Project space ID (project_key)
        work_item_type_keys:
          type: string
          required: true
          description: Work item type key
    required: true
    description: Define project space and work item type scope for resource instances.
  search_group:
    type: object
    required: true
    description: |
      Filtering conditions. Only limited fields supported:
      creation time, creator, space, resource work item ID,
      updater, update time, repository config.
    schema:
      conjunction:
        type: string
        enum: [AND, OR]
        required: true
      search_params:
        type: array
        required: false
      search_groups:
        type: array
        required: false
  field_selected:
    type: array
    items: string
    required: false
    constraints:
      max_items: 20
    description: >
      Fields to return. If omitted, only work_item_id is returned.
      Maximum 20 fields.
  pagination:
    type: object
    required: false
    properties:
      page_size: integer
      search_after: string
    description: Pagination using search_after.
  features:
    type: object
    required: false
    description: >
      Extended options. Supported keys:
      FindAborted, AllowTruncate, SkipAuthCheck.

outputs:
  data:
    type: array
    description: Resource work item instances
  pagination:
    type: object
    description: Pagination metadata

constraints:
  - Requires Permission Management – Work Item Instances
  - Resource repository must be enabled
  - Default response returns only work_item_id
  - Max 20 fields per query (field_selected)
  - Uses search_after for deep pagination
  - Only limited fields supported in search_group

error_mapping:
  20068: Search param not supported
  30014: Work item type key not found
  20069: Search param value error
  20063: Search operator error
  20072: Conjunction value only supports AND / OR
  30001: Data not found
```

### 使用说明：  
- `data_sources`：形如`{project_key, work_item_type_keys}`的数组，用于定义搜索范围。  
- `search_group`：与其他搜索API相同的结构；仅支持有限的字段（创建时间、创建者、更新者、更新时间、资源ID等）。  
- `field_selected`：最多支持20个字段；省略该参数可仅返回`work_item_id`。  
- `pagination.search_after`：用于深度分页的起始位置。  

## 创建工作项资源仓库  
在指定项目空间和工作项类型下创建一个**工作项资源仓库实例**。工作项类型的高级配置中必须启用了“资源库”功能。  

### 使用场景：  
- 当需要创建新的资源库工作项（例如可重用组件、模板）时  
- 当需要使用字段值初始化资源实例时  
- 当需要向资源仓库中添加条目时  

### API规范：`create_work_item_resource_repository`  
```yaml
name: create_work_item_resource_repository
type: api
description: >
  Create a **work item resource repository instance** under a specified
  project space and work item type. The work item type must have
  **resource library enabled** in advanced configuration.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/resource/create_work_item
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_key:
    type: string
    required: true
    description: Feishu / Meegle project space ID (project_key).
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type key. Obtainable via "Get Work Item Types in Space".
  template_id:
    type: integer
    required: false
    description: >
      Template ID. If omitted, the first process template
      of this work item type is used.
  field_value_pairs:
    type: array
    items: object
    required: false
    description: >
      Initial field values for creating the resource instance.
      Must follow Data Structure Summary. Supported fields can be
      obtained from "Get Work Item Creation Metadata".

outputs:
  data:
    type: object
    properties:
      work_item_id: integer
    description: Newly created resource work item ID.

constraints:
  - Requires Permission Management – Work Item Instance
  - Resource library must be enabled for the work item type
  - If no template_id is provided, the default template is used

error_mapping:
  1000053507: Work item has not enabled resource library (specified type is not a resource repository)
```

### 使用说明：  
- `project_key`, `work_item_type_key`：用于标识空间和工作项类型。  
- `template_id`：可选；省略该参数时将使用默认的模板。  
- `field_value_pairs`：与“Create Work Item”中的结构相同；可以使用`Get Work Item Creation Metadata`来获取支持的字段。  

## 通过资源创建工作项  
使用资源库工作项作为来源创建新的工作项实例。在启用了工作项资源库功能后，可以使用此接口根据资源条目创建相应的工作项实例。  

### 使用场景：  
- 当需要从资源库条目创建工作项实例时（例如可重用组件模板）  
- 当需要将资源工作项实例作为新的工作项在空间中创建时  
- 当需要将资源字段值复制到新的工作项中时  

### API规范：`create_work_item_through_resources`  
```yaml
name: create_work_item_through_resources
type: api
description: >
  Create work item instances using a resource library work item as the source.
  After enabling Work Item Resource Library, use this interface to create
  corresponding work item instances from a resource entry.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/resource/{project_key}/{work_item_id}/create_instance
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
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.
  work_item_id:
    type: string
    required: true
    description: >
      Resource work item instance ID. In work item details, expand ··· in the upper right, click ID.

inputs:
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtainable via "Get work item types in the space".
  name:
    type: string
    required: false
    description: >
      Work item name. When name is a resource field, this value is ignored by default.
  template_id:
    type: integer
    required: false
    description: >
      Template ID. If omitted, the first process template of this work item type is used.
      Obtain from Get Work Item Creation Metadata → template field options.
  field_value_pairs:
    type: array
    items: object
    required: false
    description: >
      Follow FieldValuePair structure. Same as Create Work Item.

outputs:
  data:
    type: object
    properties:
      work_item_id: integer
      ignore_create_info:
        field_keys: array
        role_ids: array
    description: >
      work_item_id: Created work item instance ID.
      ignore_create_info: Fields/roles that were ignored during creation.

constraints:
  - Requires Permission Management – Work Items
  - Work Item Resource Library must be enabled
  - work_item_id is the source resource work item ID

error_mapping:
  20006: Invalid param (field_value_pairs structure does not meet single-select field spec)
```

### 使用说明：  
- `project_key`, `work_item_id`：路径参数。`work_item_id`是指定来源资源工作项的ID。  
- `work_item_type_key`：要创建的工作项类型；必须与资源类型匹配。  
- `name`：可选；如果名称是资源字段，则可以省略。  
- `template_id`：可选；省略该参数时将使用默认的模板。  
- `field_value_pairs`：与“Create Work Item”中的结构相同；遵循`ValuePair`的规范。