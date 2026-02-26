---
name: meegle-api-work-item-tasks
description: Meegle OpenAPI 用于工作项任务操作。
metadata: { openclaw: {} }
---
# Meegle API — 任务管理

这些API用于管理Meegle空间中的工作项任务。

## 功能范围

- 任务的创建、检索和更新
- 任务的生命周期和状态
- 与任务相关的接口

---

## 获取指定空间的任务列表

搜索满足输入条件的子任务，查询范围仅限于安装了该插件的空间。最多返回5000条结果；可使用过滤器来控制结果数量。

### 使用场景

- 当需要在一个或多个空间中列出子任务时
- 当需要按名称、所有者（user_keys）、状态或创建时间进行筛选时
- 当需要为多个项目构建任务仪表板或报告时

### API规范：get_task_list_across_space

```yaml
name: get_task_list_across_space
type: api
description: Search subtasks across spaces; plugin-installed spaces only; max 5000 results.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/work_item/subtask/search" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_keys: array, simple_names: array, page_size: integer, page_num: integer, name: string, user_keys: array, status: integer (0|1), created_at: object }
outputs: { data: array, pagination: object }
constraints: [Subtasks permission, project_keys+simple_names union max 10, max 5000 results, created_at 13-digit ms]
error_mapping: { 20094: Exceeds 5000, 20013: Invalid time interval, 20057: project_keys+simple_names exceeds 10, 50006: Operate fail }
```

### 使用说明

- **project_keys** 或 **simple_names**：可选；省略则查询所有安装了该插件的可用空间。最多可同时查询10个项目。
- **status**：0 = 进行中，1 = 完成。
- **created_at**：使用13位毫秒级时间戳；省略“until now”表示查询截至当前时间的所有任务。

---

## 获取任务详情

获取指定工作项实例的子任务详细信息。返回节点及其关联的子任务数据。该工作项必须是工作流（node-flow）类型。

### 使用场景

- 当需要获取某个工作项的所有子任务时（可按节点进行筛选）
- 当需要为单个工作项生成任务列表或进度视图时
- 当需要同步或审计子任务数据时

### API规范：get_task_details

```yaml
name: get_task_details
type: api
description: Subtask details for a work item; nodes and sub_tasks; workflow (node-flow) only.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/task" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { node_id: string }
outputs: { data: array }
constraints: [Work Item Instance permission, node-flow only]
error_mapping: { 20018: Node ID not exist, 50006: Not workflow mode, 30005: Work item not found, 10001: No permission }
```

### 使用说明

- **node_id**：可选查询参数；用于将结果限制在某个节点的子任务上。该参数与`node_state_key`含义相同，可从任务列表响应中获取。
- **data**：节点列表；每个节点包含子任务数组，其中包含完整的任务详情（id、名称、所有者、计划等）。

---

## 创建任务

在工作项实例的指定节点上创建一个子任务。该工作项必须是工作流（node-flow）类型。需要提供`name`和`node_id`。

### 使用场景

- 当需要向工作流节点添加新子任务时
- 当需要创建带有分配者、计划或自定义字段的任务时
- 当需要从外部系统自动创建任务时

### API规范：create_tasks

```yaml
name: create_tasks
type: api
description: Create subtask on a node; workflow mode; name and node_id required.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/task" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { node_id: string, name: string, alias_key: string, assignee: array, role_assignee: array, schedule: object, note: string, field_value_pairs: array }
outputs: { data: integer }
constraints: [Work Item Instance permission, node-flow, name+node_id required, not both assignee and role_assignee]
error_mapping: { 20018: Node ID not exist, 20007: Work item aborted, 20005: Missing param, 30005: Work item not found, 20090: Request intercepted, 20047: assignee and role_assignee both set, 30015: Record not found }
```

### 使用说明

- **node_id**、**name**：必填参数。`node_id`可从`Get Workflow Details`或`Get Task Details`中获取。
- **assignee** 或 **role_assignee**：根据节点的所有者分配方式选择其中一个参数：如果节点的所有者分配方式是“与角色关联”（使用`role_assignee`），否则使用`assignee`。
- **schedule**：遵循任务列表/详情响应中使用的调度结构。

---

## 更新任务

更新工作项实例指定节点上的子任务详细信息。如需更新子任务的自定义字段，也可以使用`Update Work Item` API（参数为`work_item_type_key=sub_task`）。

### 使用场景

- 当需要编辑子任务的名称、分配者、计划、备注或自定义字段时
- 当需要从外部系统同步任务更新时
- 当需要更改`role_assignee`或`assignee`时

### API规范：update_tasks

```yaml
name: update_tasks
type: api
description: Update subtask on a node; custom fields also via Update Work Item work_item_type_key=sub_task.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/{node_id}/task/{task_id}" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string, node_id: string, task_id: string }
inputs: { name: string, assignee: array, role_assignee: array, schedule: object, note: string, deliverable: array, update_fields: array }
outputs: err_code 0
constraints: [Work Item Instance permission, not both assignee and role_assignee]
error_mapping: { 20007: Work item aborted, 30005: Work item not found, 20046: Task ID not exist, 20018: Node ID not exist, 20090: Request intercepted, 20050: Field option wrong, 50006: No right to edit, 20047: assignee and role_assignee both set, 30009: Field not found }
```

### 使用说明

- **task_id**：路径参数；从`Create Tasks`响应或`Get Task Details`（sub_task.id）中获取。
- **assignee** 或 **role_assignee**：仅使用其中一个参数；规则与`Create Tasks`相同。
- **update_fields**：字段值对列表；新值会覆盖原有值。对于更多自定义字段，建议使用`Update Work Item` API（参数为`work_item_type_key=sub_task`）。

---

## 完成/回滚任务

完成或回滚工作项实例指定节点上的子任务。操作过程中可以选择更新分配者、`role_assignee`、计划、交付物或备注。

### 使用场景

- 当需要将子任务标记为已完成（confirm）或回滚（rollback）时
- 当需要在完成任务或回滚时更新交付物、计划或备注时
- 当需要从外部系统同步任务状态时

### API规范：complete_or_rollback_tasks

```yaml
name: complete_or_rollback_tasks
type: api
description: Complete (confirm) or roll back a subtask; optionally update assignee, schedules, deliverable, note.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/subtask/modify" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { node_id: string, task_id: integer, action: confirm|rollback, assignee: array, role_assignee: array, schedules: array, deliverable: array, note: string }
outputs: err_code 0
constraints: [Work Item Instance permission, action confirm or rollback]
error_mapping: { 50006: Already confirmed or deliverable error, 30005: Work item not found, 20090: Request intercepted, 20082: Action not supported, 20046: Task ID not exist, 20005: Missing param, 20018: Node ID not exist, 20007: Work item aborted }
```

### 使用说明

- **action**：`confirm`表示完成，`rollback`表示回滚。
- **task_id**：从任务列表（跨空间查询）或`Get Task Details`（sub_task.id）中获取。
- 可选参数`assignee`、`role_assignee`、`schedules`、`deliverable`、`note`：用于在操作过程中更新子任务字段；完成操作时可能需要设置交付物。

---

## 删除任务

删除工作项实例中的子任务。无需请求体；通过路径参数来标识要删除的子任务。

### 使用场景

- 当需要从工作项中移除子任务时
- 当需要清理或重新组织工作流任务时
- 当需要从外部系统同步删除操作时

### API规范：delete_tasks

```yaml
name: delete_tasks
type: api
description: Delete subtask; no body; identify by path (project_key, work_item_type_key, work_item_id, task_id).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: DELETE, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/task/{task_id}" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string, task_id: string }
outputs: {}
constraints: [Permission: Work Item Instance]
error_mapping: { 20007: Work item aborted, 20090: Request intercepted, 30005: Work item not found }
```

### 使用说明

- **task_id**：路径参数；从任务列表（跨空间查询）或`Get Task Details`（sub_task.id）中获取。
- 无需请求体；仅使用DELETE请求方法。