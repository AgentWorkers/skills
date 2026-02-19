---
name: meegle-api-work-item-tasks
description: Meegle OpenAPI 用于工作项任务操作。
metadata:
  openclaw: {}
---
# Meegle API — 任务管理

这些API用于管理Meegle工作项中的任务。

## 功能范围

- 任务的创建、检索和更新
- 任务的生命周期和状态
- 与任务相关的接口

---

## 获取指定空间的任务列表

搜索符合输入条件的子任务，查询范围仅限于安装了该插件的空间。最多返回5000条结果；可以使用过滤器来控制结果数量。

### 使用场景

- 当需要在一个或多个空间中列出子任务时
- 当需要根据名称、所有者（user_keys）、状态或创建时间进行筛选时
- 当需要跨项目构建任务仪表板或报告时

### API规范：get_task_list_across_space

```yaml
name: get_task_list_across_space
type: api
description: >
  Search for subtasks that meet input conditions across spaces.
  Only spaces where the plugin is installed. Max 5000 results.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/subtask/search
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_keys:
    type: array
    items: string
    required: false
    description: >
      Space IDs to query. Obtain by double-clicking space name in Meegle.
      If neither project_keys nor simple_names is provided, defaults to spaces
      where the plugin is installed and user_key in header can access.
      Union of project_keys and simple_names cannot exceed 10.
  simple_names:
    type: array
    items: string
    required: false
    description: >
      Space simple_name list. From space URL, e.g. https://project.feishu.cn/doc/overview → doc.
      Same default and limit as project_keys; union with project_keys max 10.
  page_size:
    type: integer
    required: false
    default: 50
    description: Page size. Default 50. Total results cap 5000.
  page_num:
    type: integer
    required: false
    default: 1
    description: Page number. Default 1.
  name:
    type: string
    required: false
    description: Subtask name, fuzzy match.
  user_keys:
    type: array
    items: string
    required: false
    description: >
      Subtask owner user_keys. Own: double-click avatar in Meegle; others: Get Tenant User List.
  status:
    type: integer
    required: false
    enum: [0, 1]
    description: |
      0: In progress
      1: Completed
  created_at:
    type: object
    required: false
    properties:
      start: integer
      end: integer
    description: >
      Creation time interval (millisecond timestamps, 13-digit).
      If end is omitted, current time is used as default.

outputs:
  data:
    type: array
    description: >
      Subtask list. Max 5000 total. Each item includes work_item_id, work_item_name,
      node_id, sub_task (id, name, owners, assignee, schedules, passed, actual_begin_time, etc.).
  pagination:
    type: object
    properties:
      page_num: integer
      page_size: integer
      total: integer

constraints:
  - Permission: Permission Management – Subtasks
  - Union of project_keys and simple_names max 10
  - Total results max 5000; refine filters if exceeded
  - created_at must be 13-digit millisecond timestamps

error_mapping:
  20094: Search result exceeds 5000 (refine search params)
  20013: Invalid time interval (not millisecond timestamps)
  20057: project_keys and simple_names union exceeds 10
  50006: Operate fail (contact platform)
```

### 使用说明

- **project_keys** 或 **simple_names**：可选；省略则查询所有安装了该插件的可用空间。两者组合最多可查询10个空间。
- **status**：0 = 进行中，1 = 完成。
- **created_at**：使用13位毫秒级时间戳；省略末尾部分表示“截至当前时间”。

---

## 获取任务详情

获取指定工作项实例的子任务详细信息。返回节点及其关联的子任务数据。该工作项必须是工作流（node-flow）类型。

### 使用场景

- 当需要获取某个工作项的所有子任务时（可选，可根据节点进行筛选）
- 当需要为单个工作项构建任务列表或进度视图时
- 当需要同步或审核子任务数据时

### API规范：get_task_details

```yaml
name: get_task_details
type: api
description: >
  Obtain detailed information of subtasks on the specified work item instance.
  Returns nodes and their sub_tasks. Work item must be workflow (node-flow) mode.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/task
  headers:
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
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtainable via "Get work item types in the space".
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, click ··· in the upper right, then ID to copy.

inputs:
  node_id:
    type: string
    required: false
    description: >
      state_key of the target node; query subtasks of that node only.
      Obtain from Get a List of Specified Tasks (Across Space) (node_id / state_key).
      If omitted, returns subtasks of all nodes.

outputs:
  data:
    type: array
    description: >
      Array of nodes, each with id, state_key, node_name, template_id, version, sub_tasks.
      sub_tasks: array of task objects (id, name, owners, assignee, schedules, fields,
      passed, actual_begin_time, actual_finish_time, role_assignee, etc.).

constraints:
  - Permission: Permission Management – Work Item Instance
  - Work item must be workflow (node-flow) mode

error_mapping:
  20018: Node ID not exist in workflow (node_id incorrect)
  50006: Work item is not workflow mode
  30005: Work item not found (check project_key, work_item_type_key, work_item_id)
  10001: Operation not permitted (no permission)
```

### 使用说明

- **node_id**：可选查询参数；用于将结果限制在某个节点的子任务上。该参数与node_state_key相同，可从任务列表响应中获取。
- **data**：节点列表；每个节点包含子任务数组，其中包含完整的任务详情（id、名称、所有者、计划等）。

---

## 创建任务

在工作项实例的指定节点上创建一个子任务。该工作项必须是工作流（node-flow）类型。需要提供`name`和`node_id`参数。

### 使用场景

- 当需要向工作流节点添加新子任务时
- 当需要创建带有分配者、计划或自定义字段的任务时
- 当需要从外部系统自动创建任务时

### API规范：create_tasks

```yaml
name: create_tasks
type: api
description: >
  Create a subtask on a specified node of a work item instance.
  Work item must be workflow mode. name and node_id are required.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/task
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
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type. Obtainable via "Get work item types in the space".
      Must match the work item instance identified by work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID to which the new subtask belongs.

inputs:
  node_id:
    type: string
    required: true
    description: >
      Target node ID (equivalent to node state_key). Obtain via Get Workflow Details.
  name:
    type: string
    required: true
    description: Name of the subtask.
  alias_key:
    type: string
    required: false
    description: Docking identifier of the target node for external system reference.
  assignee:
    type: array
    items: string
    required: false
    description: >
      List of user_key for subtask owners. Use only when node owner assignment is NOT "linked with roles".
      Cannot be set together with role_assignee.
  role_assignee:
    type: array
    items: object
    required: false
    description: >
      List of role owners (RoleOwner structure: role ID + owners user_key array).
      Use only when node owner assignment is "linked with roles".
      Cannot be set together with assignee.
  schedule:
    type: object
    required: false
    description: Scheduling information. Follow Schedule structure.
  note:
    type: string
    required: false
    description: Remarks for the subtask.
  field_value_pairs:
    type: array
    items: object
    required: false
    description: Custom fields and values. Follow FieldValuePair structure.

outputs:
  data:
    type: integer
    description: ID of the successfully created subtask.

constraints:
  - Permission: Permission Management – Work Item Instance
  - Work item must be workflow (node-flow) mode
  - name and node_id are required
  - Do not set both assignee and role_assignee

error_mapping:
  20018: Node ID not exist in workflow (node_id incorrect)
  20007: Work item is already aborted (cannot operate on terminated work items)
  20005: Missing param (name required, or node_id required)
  30005: Work item not found
  20090: Request intercepted
  20047: role_assignee and assignee cannot be set together
  30015: Record not found (workflow err)
```

### 使用说明

- **node_id**、**name**：必填参数。请从Get Workflow Details或Get Task Details中获取node_id（state_key）。
- **assignee** 与 **role_assignee**：根据节点的所有者分配方式选择其中一个参数：如果分配方式是“与角色关联”（使用role_assignee），否则使用assignee。
- **schedule**：遵循任务列表/详情响应中使用的调度结构。

---

## 更新任务

更新工作项实例指定节点上的子任务详细信息。如需更新子任务的自定义字段，也可以使用Update Work Item接口（参数为work_item_type_key=sub_task）。

### 使用场景

- 当需要编辑子任务的名称、分配者、计划、备注或自定义字段时
- 当需要从外部系统同步任务更新时
- 当需要更改role_assignee或assignee时（只能选择其中一个参数）

### API规范：update_tasks

```yaml
name: update_tasks
type: api
description: >
  Update detailed information of a subtask on the specified node of a work item instance.
  For subtask custom fields, Update Work Item with work_item_type_key=sub_task is also supported.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/{node_id}/task/{task_id}
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
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type. Obtainable via "Get work item types in the space".
      Must match the work item instance identified by work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, click ··· in the upper right, then ID to copy.
  node_id:
    type: string
    required: true
    description: Target node ID (equivalent to node state_key). Obtain via Get Workflow Details.
  task_id:
    type: string
    required: true
    description: Subtask ID. Returned by Create Tasks or from Get Task Details (sub_task.id).

inputs:
  name:
    type: string
    required: false
    description: Subtask name.
  assignee:
    type: array
    items: string
    required: false
    description: >
      List of user_key for subtask owners. Use when node owner type is not role-based.
      Cannot be set together with role_assignee.
  role_assignee:
    type: array
    items: object
    required: false
    description: >
      List of role owners (RoleOwner: role + owners). Use when node owner type is role assignee.
      Cannot be set together with assignee.
  schedule:
    type: object
    required: false
    description: Scheduling information. Follow Schedule structure.
  note:
    type: string
    required: false
    description: Remarks for the subtask.
  deliverable:
    type: array
    items: object
    required: false
    description: Deliverables. Follow FieldValuePair structure.
  update_fields:
    type: array
    items: object
    required: false
    description: >
      Fields to update. Follow FieldValuePair structure. Updated values overwrite previous ones.

outputs:
  description: Success returns err_code 0.

constraints:
  - Permission: Permission Management – Work Item Instance
  - Do not set both assignee and role_assignee

error_mapping:
  20007: Work item is already aborted (terminated)
  30005: Work item not found
  20046: Task ID not exist in workflow
  20018: Node ID not exist in workflow
  20090: Request intercepted
  20050: Field option value wrong (config updated)
  50006: No right to edit (no permission to edit this subtask)
  20047: role_assignee and assignee cannot be set together
  30009: Field not found
```

### 使用说明

- **task_id**：路径参数；从Create Tasks响应或Get Task Details（sub_task.id）中获取。
- **assignee** 与 **role_assignee**：只能选择其中一个参数；规则与Create Tasks相同。
- **update_fields**：字段值对列表；新值会覆盖原有值。对于更多自定义字段，建议使用Update Work Item接口（参数为work_item_type_key=sub_task）。

---

## 完成/回滚任务

完成或回滚工作项实例指定节点上的子任务。操作过程中可以选择更新分配者、role_assignee、计划、交付物或备注。

### 使用场景

- 当需要将子任务标记为已完成（confirm）或回滚（rollback）时
- 当需要在完成/回滚过程中更新交付物、计划或备注时
- 当需要从外部系统同步任务状态时

### API规范：complete_or_rollback_tasks

```yaml
name: complete_or_rollback_tasks
type: api
description: >
  Complete or roll back a subtask on a specified node of a work item instance.
  Optionally update assignee, schedules, deliverable, or note during the operation.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/subtask/modify
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
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type. Obtainable via "Get work item types in the space".
      Must match the work item instance identified by work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, click ··· in the upper right, then ID to copy.

inputs:
  node_id:
    type: string
    required: true
    description: Target node ID (equivalent to state_key). Obtain via Get Workflow Details.
  task_id:
    type: integer
    required: true
    description: Subtask ID. Obtain via Get a List of Specified Tasks (Across Space) or Get Task Details.
  action:
    type: string
    required: true
    enum: [confirm, rollback]
    description: |
      confirm: Complete the subtask
      rollback: Roll back the subtask
  assignee:
    type: array
    items: string
    required: false
    description: List of user_key for subtask leaders. Use when node leader type is non-role.
  role_assignee:
    type: array
    items: object
    required: false
    description: >
      Role owners (RoleOwner structure). Use when node responsible person type is role assignee.
      Can update subtask fields while completing/rolling back.
  schedules:
    type: array
    items: object
    required: false
    description: Schedule structure. Can update subtask schedule during complete/rollback.
  deliverable:
    type: array
    items: object
    required: false
    description: Deliverables. Follow FieldValuePair structure.
  note:
    type: string
    required: false
    description: Remarks. Can update note during complete/rollback.

outputs:
  description: Success returns err_code 0.

constraints:
  - Permission: Permission Management – Work Item Instance
  - action must be confirm or rollback

error_mapping:
  50006: Subtask already confirmed (refresh and try again) or task deliverable error (required deliverable not entered)
  30005: Work item not found
  20090: Request intercepted
  20082: Action not supported (use confirm or rollback)
  20046: Task ID not exist in workflow
  20005: Missing param (node_id, task_id, or action required)
  20018: Node ID not exist in workflow
  20007: Work item is already aborted (terminated)
```

### 使用说明

- **action**：`confirm` 表示完成，`rollback` 表示回滚。
- **task_id**：从任务列表（跨空间查询）或Get Task Details（sub_task.id）中获取。
- 可选参数**assignee**、**role_assignee**、**schedules**、**deliverable**、**note**：在操作过程中可以更新子任务的这些字段；完成操作可能需要设置交付物。

---

## 删除任务

删除工作项实例中的子任务。无需请求体；通过路径参数来标识子任务。

### 使用场景

- 当需要从工作项中删除子任务时
- 当需要清理或重新组织工作流任务时
- 当需要从外部系统同步删除操作时

### API规范：delete_tasks

```yaml
name: delete_tasks
type: api
description: >
  Delete a subtask in the specified work item instance.
  No body; subtask identified by path parameters.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: DELETE
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/task/{task_id}
  headers:
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
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type. Obtainable via "Get work item types in the space".
      Must match the work item instance identified by work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, click ··· in the upper right, then ID to copy.
  task_id:
    type: string
    required: true
    description: Subtask ID. Obtain via Get a List of Specified Tasks (Across Space) or Get Task Details (sub_task.id).

outputs:
  description: Success returns err_code 0.

constraints:
  - Permission: Permission Management – Work Item Instance

error_mapping:
  20007: Work item is already aborted (terminated)
  20090: Request intercepted
  30005: Work item not found
```

### 使用说明

- **task_id**：路径参数；从任务列表（跨空间查询）或Get Task Details（sub_task.id）中获取。
- 无需请求体；仅使用DELETE请求方法。