---
name: meegle-api-workflows-and-nodes
description: Meegle OpenAPI：用于工作流和节点操作。
metadata:
  openclaw: {}
---
# Meegle API — 工作流与节点

提供用于管理工作项工作流及工作流节点的相关API。

## 功能范围

- 获取工作流详细信息（节点/状态流程、节点、连接关系、计划安排、子任务、表单）
- 获取工作流详细信息（WBS）
- 更新节点/计划安排
- 完成/回滚节点
- 状态流程转换
- 获取节点或状态流程所需的信息
- 审核管理

---

## 获取工作流详细信息

获取指定工作空间和工作项类型下的工作流信息，包括节点状态、负责人、预估得分、节点表单、子任务和连接关系。支持基于节点的工作流（例如需求）和基于状态的工作流（例如缺陷、版本）。

### 使用场景

- 在为工作项构建工作流用户界面或报告时
- 当需要节点级别的数据（如计划安排、负责人、节点字段、子任务、检查者、完成信息）时
- 当区分基于节点的流程（`flow_type`为0）和基于状态的流程（`flow_type`为1）时

### API规范：`get_workflow_detail`

```yaml
name: get_workflow_detail
type: api
description: >
  Obtain workflow information of a work item instance: nodes, connections,
  schedules, assignees, node forms, subtasks. Supports node workflow (0) and status workflow (1).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/query
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
    description: Work item type. Obtain via Get work item types in the space.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In details, expand ··· in the upper right, then click ID.

inputs:
  fields:
    type: array
    items: string
    required: false
    description: >
      Control which node form fields are returned. Default: all. Two modes (do not mix):
      Specified: e.g. ["name", "created_at"] returns only those fields.
      Excluded: fields starting with "-", e.g. ["-name", "-created_at"] returns all except those.
  flow_type:
    type: integer
    required: false
    description: >
      Workflow type. Default 0.
      0: Node workflow (e.g. requirements).
      1: Status workflow (required for defects, versions, etc.).
  expand:
    type: object
    required: false
    description: Extra options. Only need_user_detail is supported.
    properties:
      need_user_detail:
        type: boolean
        description: When true, response includes user_details for owners/assignees.

outputs:
  data:
    type: object
    description: >
      Instance workflow per NodesConnections: workflow_nodes (id, name, state_key, status,
      schedules, node_fields, finished_infos, sub_tasks, owners, checker, node_schedule,
      actual_begin_time, actual_finish_time, etc.), connections (source_state_key,
      target_state_key), user_details (when expand.need_user_detail), template_id, version.

constraints:
  - Permission: Permission Management – Work Items

error_mapping:
  30005: Work item not found (no instance for given work_item_id)
  20026: FlowType is error (flow_type in body incorrect)
  20027: FlowType is error (flow_type in body incorrect)
  10001: Operation not permitted (current user lacks permission)
  20014: Project and work item not match (project_key vs work_item_id mismatch)
  50006: Fail to read/write db (retry; escalate if repeated)
  20015: Field mix with '-' and without '-' (use either specified or excluded fields, not both)
```

### 使用说明

- **flow_type**：使用`0`表示基于节点的工作流（例如故事/需求）；使用`1`表示基于状态的工作流（例如缺陷、版本）。
- **fields**：仅使用一种模式——正列表（例如`["name","created_at"]`）或负列表（例如`["-name","-created_at"]`）。混合使用会导致错误（20015）。
- **expand.need_user_detail**：设置为`true`可在响应中获取负责人的详细信息（电子邮件、中文名称、英文名称、用户键、用户名）。
- **data**：遵循`NodesConnections`的结构；`workflow_nodes`包含计划安排、节点字段、子任务、检查者、完成信息、负责人使用模式等；`connections`定义状态键值之间的转换关系。

---

## 获取工作流详细信息（WBS）

获取基于节点的工作项实例的WBS（工作分解结构）信息。此功能仅在行业特别版中提供。返回WBS树（`related_sub_work_items`、`related_parent_work_item`）、可交付成果和连接关系。

### 使用场景

- 在为基于节点的工作项构建WBS视图或层次结构用户界面时
- 当需要集成可交付成果（`need_union_deliverable`）或计划表汇总（`need_schedule_table_agg`）时
- 当工作项是WBS工作项或WBS子工作项时

### API规范：`get_workflow_details_wbs`

```yaml
name: get_workflow_details_wbs
type: api
description: >
  Obtain WBS workflow information of a node flow work item instance (industry special edition).
  Returns WBS tree, deliverables, and connections.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/wbs_view
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
    description: Work item type. Obtain via Get work item types in the space.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In details, expand ··· in the upper right, then click ID.

inputs:
  need_union_deliverable:
    type: boolean
    required: false
    description: Whether to include integrated deliverables in the response (query).
  need_schedule_table_agg:
    type: boolean
    required: false
    description: Extended query; whether to include custom column aggregation fields for the schedule (query).
  expand:
    type: object
    required: false
    description: Optional expand options (query; structure as per product).

outputs:
  data:
    type: object
    description: >
      WBS details: template_key, related_sub_work_items (node_uuid, work_item_id, type, name,
      wbs_status_map, sub_work_item, deliverable, union_deliverable, role_owners), related_parent_work_item
      (is_top, work_item_id, name, template_key, template_version, work_item_type_key, template_id, template_name),
      connections (source_state_key, target_state_key).

constraints:
  - Permission: Permission Management – Work Item Instance
  - Work item must be a WBS work item or WBS sub–work item (node flow; industry special edition)

error_mapping:
  30005: Work item not found (work_item_id incorrect)
  20089: Current work item is not WBS or WBS children (not a WBS / sub–WBS work item)
  20014: Project and work item not match (space does not match work item)
```

### 使用说明

- **WBS**：仅适用于行业特别版中的WBS工作项或WBS子工作项；否则会返回错误代码（20089）。
- **查询参数**：传递`need_union_deliverable`和`need_schedule_table_agg`作为查询参数（例如`?need_union_deliverable=true&need_schedule_table_agg=true`）。
- **datarelated_sub_work_items**：包含节点和子任务的树结构，以及它们的可交付成果和负责人；`related_parent_work_item`提供父WBS上下文；`connections`定义状态转换关系。

---

## 更新节点/计划安排

更新工作项中的特定节点信息：节点负责人、计划安排（`node_schedule`或差异计划安排）、节点表单字段和角色分配者。权限要求参见开发者平台 – 权限管理（Permission Management）。

### 使用场景

- 当更新节点负责人（`node_owners`或`role_assignee`）、计划安排（`node_schedule`或`schedules`）或节点表单字段时
- 当对至少有两个负责人的任务节点使用差异计划安排时
- 当通过传递空数组`node_owners`来清除所有节点负责人时

### API规范：`update_nodes_scheduling`

```yaml
name: update_nodes_scheduling
type: api
description: >
  Update node information in a work item: owners, scheduling, fields, role assignees.
  Supports dynamic scheduling (node_schedule) and differential scheduling (schedules).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: PUT
  url: https://{domain}/open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/{node_id}
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
    description: Work item type. Refer to Get work item types in space.
  work_item_id:
    type: string
    required: true
    description: Work item ID (API types as int64; string accepted in path).
  node_id:
    type: string
    required: true
    description: Target node ID.

inputs:
  node_owners:
    type: array
    items: string
    required: false
    description: >
      user_key array. Omit to leave unchanged; pass empty array [] to remove all owners.
  node_schedule:
    type: object
    required: false
    description: >
      Node-level schedule (dynamic calculation). Omit or null to leave unchanged.
    properties:
      estimate_start_date:
        type: integer
        description: Start timestamp (ms).
      estimate_end_date:
        type: integer
        description: End timestamp (ms).
      points:
        type: number
        description: Points.
  schedules:
    type: array
    required: false
    description: >
      Subscheduling array (differential scheduling). Omit or null to leave unchanged.
      Requires at least 2 responsible persons on the task node to take effect.
    items:
      type: object
      properties:
        estimate_start_date: { type: integer }
        estimate_end_date: { type: integer }
        points: { type: number }
        owners: { type: array, items: string }
  fields:
    type: array
    required: false
    description: Node form fields to update (FieldValuePair).
    items:
      type: object
      properties:
        field_alias: { type: string }
        field_key: { type: string }
        field_type_key: { type: string }
        field_value: {}
  role_assignee:
    type: array
    required: false
    description: >
      Role owners for the node. Use when node is bound to roles (e.g. PM, DA).
    items:
      type: object
      properties:
        role: { type: string }
        owners: { type: array, items: string }

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Developer Platform – Permissions (Permission Management)
```

### 使用说明

- **node_owners**：省略表示不进行任何更改；`[]`表示移除所有负责人。值应为`user_key`（来自Meegle，例如在开发者平台中双击头像）。
- **node_schedule**与`schedules`：使用`node_schedule`表示单个动态计划；使用`schedules`表示按负责人划分的差异计划安排（任务节点必须至少有两个负责人）。
- **fields**：每个字段都需要`field_key`、`field_type_key`和`field_value`；`field_alias`是字段的标识符。
- **role_assignee**：传递`role`和`owners`（用户键列表）；空数组`owners`表示清除该角色的分配者。

---

## 完成/回滚节点

完成或回滚特定工作项的节点。可选地，在同一请求中更新节点负责人、计划安排、字段和角色分配者。权限要求参见开发者平台 – 权限管理（Permission Management）。

### 使用场景

- 当完成节点（操作`confirm`）或回滚节点（操作`rollback`）时
- 当提交回滚原因时（`rollback_reason`是必填项）
- 当更新节点数据（负责人、计划安排、字段和角色分配者）时

### API规范：`node_completion_rollback`

```yaml
name: node_completion_rollback
type: api
description: >
  Complete or rollback a node; optionally update node owners, scheduling, fields, and role assignees.
  Same permission and path pattern as workflow node operations.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/{node_id}/operate
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
    description: Work item type. Refer to Get work item types in space.
  work_item_id:
    type: string
    required: true
    description: Work item ID (API types as int64; string accepted in path).
  node_id:
    type: string
    required: true
    description: Target node ID; same as node state_key from Get Workflow Detail.

inputs:
  action:
    type: string
    required: true
    description: Operation type. confirm = completion; rollback = rollback.
    enum: [confirm, rollback]
  rollback_reason:
    type: string
    required: false
    description: Reason for rollback; required when action is rollback.
  node_owners:
    type: array
    items: string
    required: false
    description: >
      user_key array. Omit to leave unchanged; pass empty array [] to remove all owners.
  node_schedule:
    type: object
    required: false
    description: Node schedule (non-differentiated). Omit or empty if no update.
    properties:
      estimate_start_date: { type: integer }
      estimate_end_date: { type: integer }
      points: { type: number }
  schedules:
    type: array
    required: false
    description: Sub-scheduling array (differential scheduling). Null if no update.
    items:
      type: object
      properties:
        estimate_start_date: { type: integer }
        estimate_end_date: { type: integer }
        points: { type: number }
        owners: { type: array, items: string }
  fields:
    type: array
    required: false
    description: Node form fields to update (FieldValuePair).
    items:
      type: object
      properties:
        field_alias: { type: string }
        field_key: { type: string }
        field_type_key: { type: string }
        field_value: {}
  role_assignee:
    type: array
    required: false
    description: Role owners for the node (e.g. PM, DA).
    items:
      type: object
      properties:
        role: { type: string }
        owners: { type: array, items: string }

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Developer Platform – Permissions (Permission Management)
```

### 使用说明

- **action**：使用`confirm`完成节点，使用`rollback`回滚节点。当`action`为`rollback`时，`rollback_reason`是必填项。
- **node_id**：必须与`Get Workflow Detail`中返回的节点`state_key`匹配（例如`start`、`doing`、`end`）。
- 可选的身体字段（`node_owners`、`node_schedule`、`schedules`、`fields`、`role_assignee`）的使用方式与`Update Nodes/Scheduling`相同：省略表示不进行任何更改；空数组`node_owners`表示移除所有负责人。

---

## 状态流程转换

将基于状态的工作项实例转换到指定的状态，并可选地更新状态表单字段和角色负责人。使用`Get Workflow Detail`中的`transition_id`（来自`connections`）。权限要求参见权限管理 – 工作项实例（Permission Management – Work Item Instance）。

### 使用场景

- 当将基于状态的工作项（例如缺陷、版本）转换到另一个状态时
- 在转换过程中更新状态表单字段或角色负责人
- 通过集成或自动化驱动状态变更时

### API规范：`status_flow_transition`

```yaml
name: status_flow_transition
type: api
description: >
  Transfer a state flow work item to the specified state; optionally update
  status form fields and role_owners. transition_id comes from Get Workflow Detail (connections).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/state_change
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
    description: Work item type. Obtain via Get work item types in the space.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In details, expand ··· in the upper right, then click ID.

inputs:
  transition_id:
    type: integer
    required: false
    description: >
      ID for transitioning to the next state. Obtain from Get Workflow Detail (flow_type 1):
      connections structure, transition_id field. Must not be null or 0 for a valid transition.
  fields:
    type: array
    required: false
    description: Fields to update; only status form fields can be updated (FieldValuePair).
    items:
      type: object
      properties:
        field_alias: { type: string }
        field_key: { type: string }
        field_type_key: { type: string }
        field_value: {}
  role_owners:
    type: array
    required: false
    description: Roles and responsible persons (role, owners).
    items:
      type: object
      properties:
        role: { type: string }
        owners: { type: array, items: string }

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Permission Management – Work Item Instance
  - Applies to state-flow work items (flow_type 1), not node-flow

error_mapping:
  10002: Illegal operation (status transition does not match current instance status)
  20005: Missing param (transition_id cannot be null or 0)
  30005: Work item not found (no instance for given work_item_id)
  20090: Request intercepted (plugin interception rules in space)
  20038: Param missing (required status transition form field not filled; check template)
  30009: Field not found (field key not found for current work item type)
  30012: State not found in state flow (workflow template incorrect; try upgrading template)
  50006: Failed to check field (admin config changed; option values no longer exist or disabled)
```

### 使用说明

- **transition_id**：从`Get Workflow Detail`中获取（`flow_type`为1）；使用`connections`结构中的`transition_id`来指定目标状态。该值不能为空或为0（否则会返回错误代码20005）。
- **fields**：只有`status form`字段可以更新；使用`field_key`、`field_type_key`和`field_value`（以及`field_alias`作为字段标识符）。转换所需的字段必须填写（20038）。
- **role_owners**：与`role_assignee`的格式相同；空数组`owners`表示清除该角色的分配者。
- **10002**：确保请求的转换状态是从工作项的当前状态允许的。**20090**：如果请求被阻止，请检查空间插件拦截规则。

## 获取节点或状态转换所需的信息

获取指定节点转换或状态转换所需的信息。仅支持单点查询。返回所需的表单项、节点字段、子任务和可交付成果。权限要求参见权限管理 – 工作项实例（Permission Management – Work Item Instance）。

### 使用场景

- 在执行节点或状态转换之前，确定需要完成哪些表单字段、节点字段、子任务或可交付成果
- 在构建显示“缺失内容”的转换用户界面时（使用`mode: unfinished`）
- 适用于基于节点的流程（`state_key` = 节点ID）和基于状态的流程（`state_key` = 目标状态键）的工作项

### API规范：`get_required_info_node_or_status_flow`

```yaml
name: get_required_info_node_or_status_flow
type: api
description: >
  Get required information for a node or status transition: required form items,
  node fields, subtasks, deliverables. Single-point query. state_key meaning
  depends on workflow type (node flow vs state flow).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/transition_required_info/get
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
      project_key: Double-click space name in Meegle project space.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.
  work_item_type_key:
    type: string
    required: false
    description: Work item type. Obtain via Get work item types under the space.
  work_item_id:
    type: integer
    required: true
    description: Work item instance ID. In details, expand ··· > ID in the upper right.
  state_key:
    type: string
    required: true
    description: >
      Node flow: node ID (node_key / state_key).
      State flow: target state key for the state flow transfer.
      Query specific values via Get Workflow Detail.
  mode:
    type: string
    required: false
    description: >
      Query mode. Default: all required fields.
      unfinished: Only return incomplete required information.

outputs:
  data:
    type: object
    description: >
      TransRequiredInfo: form_items (required form fields; class control/field; key; finished;
      state_info with node_fields for “node info component”; sub_field for compound/multi-member),
      tasks (task_id, finished), deliverables (deliverable_id, finished), node_fields
      (field_key, field_type_key, finished, sub_field, not_finished_owner).

constraints:
  - Permission: Permission Management – Work Item Instance
  - Single-point query only

error_mapping:
  30005: Work item not found (work_item_id incorrect)
  50006: This node no longer exists (state_key incorrect; query via Get Workflow Detail)
```

### 使用说明

- **state_key**：对于基于节点的流程，使用节点的ID（来自`workflow_nodes`的`state_key`）；对于基于状态的流程，使用转换的目标状态键。从`Get Workflow Detail`中获取有效值。
- **mode**：省略或留空表示获取所有未完成的信息；设置`unfinished`仅获取未填写/完成的项目（例如用于“缺失内容”界面）。
- **data.form_items**：包含`class: control`（例如`workflow_state_info`和`state_info.node_fields`）和`class: field`（字段键、字段类型键、完成状态）的组合。`finished`表示需求是否满足。
- **data.tasks` / **data.deliverables**：转换所需的子任务和可交付成果；`finished`表示是否完成。`data.node_fields`：所需的节点级字段，`sub_field`和`not_finished_owner`用于多负责人字段。

## 批量请求审核意见和审核结论

批量查询节点的审核意见和结论。返回每个节点的`summary_mode`、意见（`finished_opinion_result`、`owners_finished_opinion_result`）和结论（`finished_conclusion_result`、`owners_finished_conclusion_result`）。权限要求参见权限管理 – 工作项实例（Permission Management – Work Item Instances）。

### 使用场景

- 在一次请求中加载多个工作项的审核意见和结论
- 在构建显示每个节点意见和结论的审核/批准用户界面时（每次请求最多10个节点）
- 当节点ID或状态键来自`Get Workflow Detail`时

### API规范：`batch_request_review_opinion_and_conclusion`

```yaml
name: batch_request_review_opinion_and_conclusion
type: api
description: >
  Query review opinions and conclusions of nodes in batches. Returns opinion and
  conclusion per node (summary_mode, opinion, conclusion). Max 10 node_ids per request.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/finished/batch_query
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
      Space ID (project_key). Double-click space name in Meegle project space to obtain.
  work_item_id:
    type: integer
    required: true
    description: Work item instance ID. In details, expand ··· > ID in the upper right.
  node_ids:
    type: array
    items: string
    required: true
    description: >
      List of target node IDs (node IDs or state_keys). Obtain via Get Workflow Detail.
      Number of nodes must not exceed 10.

outputs:
  data:
    type: object
    description: >
      project_key, work_item_id, finished_infos (list). Each element: node_id,
      summary_mode (calculation | independence), opinion (finished_opinion_result,
      owners_finished_opinion_result with owner user_key and finished_opinion_result),
      conclusion (finished_conclusion_result and owners_finished_conclusion_result
      with key, label, origin_label).

constraints:
  - Permission: Permission Management – Work Item Instances
  - node_ids length ≤ 10

error_mapping:
  1000051120: Workflow not found (work item instance does not exist; check work_item_id)
  1000051280: Params invalid (required parameters not filled)
```

### 使用说明

- **node_ids**：使用来自`Get Workflow Detail`的节点ID或`state_key`值（例如`start_0`、`start_1`）。每次请求最多10个节点。
- **summary_mode**：`calculation`表示汇总计算；`independence`表示独立完成。
- **opinion` / **conclusion**：`finished_opinion_result`和`finished_conclusion_result`是汇总结果；`owners_finished_opinion_result`和`owners_finished_conclusion_result`分别表示每个负责人的结果。结论使用`key`、`label`、`origin_label`。

## 更新审核意见和结论

更新节点的审核意见或结论，或执行重置操作。支持节点级别的审核（仅限节点负责人）和所有者级别的个人评论。权限要求参见权限管理 – 工作项实例（Permission Management – Work Item Instance）。

### 使用场景

- 当更新节点的审核意见（`opinion`）或结论（`finished_conclusion_option_key`）时
- 当清除意见或结论时（传递空字符串）或重置所有审核信息时（`reset: true`；仅限转移操作）
- 当对节点审核（`operation_type: node`）或个人评论（`operation_type: owner`）进行操作时

### API规范：`update_review_opinion_and_conclusion`

```yaml
name: update_review_opinion_and_conclusion
type: api
description: >
  Update review opinion and conclusion for a node, or reset. Supports node-level
  (node leader) and owner-level (personal) operations.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/finished/update
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params: {}

inputs:
  project_key:
    type: string
    required: true
    description: Space ID (project_key). Double-click space name in Meegle project space.
  work_item_id:
    type: integer
    required: true
    description: Work item instance ID. In details, expand ··· > ID in the upper right.
  node_id:
    type: string
    required: false
    description: Target node ID (same as state_key). Obtain via Get Workflow Detail.
  opinion:
    type: string
    required: false
    description: Review comments. Empty string = delete; omit = no change.
  finished_conclusion_option_key:
    type: string
    required: false
    description: >
      Review conclusion label key. From Batch Request Review Opinion and Conclusion
      (conclusion key). Empty string = delete; omit = no change.
  operation_type:
    type: string
    required: false
    description: >
      node: Operate on node review info (only node leader).
      owner: Operate on personal comments. Required when reset is false for owner-level update.
    enum: [node, owner]
  reset:
    type: boolean
    required: false
    description: >
      Whether to empty current review info. Default false. Only the transfer person can reset.
      When true, opinion, finished_conclusion_option_key, and operation_type may be omitted.

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Permission Management – Work Item Instance

error_mapping:
  1000051814: The node does not exist
  1000051120: Workflow not found (instance does not exist)
  20007: Work item is already aborted (cannot operate on terminated work items)
  1000053308: The review conclusion label does not exist
  1000053219: Only node owners can operate (no node owner permission)
  1000051280: Parameter invalid
```

### 使用说明

- **opinion** / **finished_conclusion_option_key**：省略表示不进行任何更改；**""`表示删除该值。`finished_conclusion_option_key`应与`Batch Request Review Opinion and Conclusion`或`Get Conclusion Option Label`中的结论键匹配。
- **operation_type**：使用`node`表示节点级别的审核；使用`owner`表示个人评论。当`reset`为`false`且正在更新所有者级别数据时需要此参数。
- **reset: true`：清除当前的审核信息；仅限“转移操作”可以执行此操作。当`reset`为`true`时，`opinion`、`finished_conclusion_option_key`和`operation_type`可以留空。

## 获取结论选项标签

查询指定节点的配置审核结论标签。用于填充节点审核结论（例如在`Update Review Opinion and Conclusion`中）。权限要求参见权限管理 – 工作项实例（Permission Management – Work Item Instances）。

### 使用场景

- 在构建需要显示每个节点允许的结论选项列表的审核/批准用户界面时
- 在验证或显示结论选项（`key`、`label`、`origin_label`）时
- 当节点ID或状态键来自`Get Workflow Detail`时（每次请求最多10个节点）

### API规范：`get_conclusion_option_label`

```yaml
name: get_conclusion_option_label
type: api
description: >
  Query configured review conclusion labels per node. Returns finished_conclusion_option,
  finished_owners_conclusion_option, finished_overall_conclusion_option (key, label, origin_label).
  Max 10 node_ids per request.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/work_item/finished/query_conclusion_option
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params: {}

inputs:
  project_key:
    type: string
    required: true
    description: Space ID (project_key). Double-click space name in Meegle project space.
  work_item_id:
    type: integer
    required: true
    description: Work item instance ID. In details, ··· in the upper right, then ID to copy.
  node_ids:
    type: array
    items: string
    required: true
    description: >
      List of target node IDs (node IDs or state_key). Obtain via Get Workflow Detail.
      Number of nodes must not exceed 10.

outputs:
  data:
    type: array
    description: >
      One object per node. Each has node_id, finished_conclusion_option (key, label, origin_label),
      finished_owners_conclusion_option, finished_overall_conclusion_option (same key/label/origin_label structure).

constraints:
  - Permission: Permission Management – Work Item Instances
  - node_ids length ≤ 10

error_mapping:
  1000051120: Workflow not found (instance does not exist)
```

### 使用说明

- **node_ids**：使用来自`Get Workflow Detail`的节点ID或`state_key`（例如`start_0`、`started_0`）。每次请求最多10个节点。
- **data`项：`finished_conclusion_option`表示节点级别的选项；`finished_overall_conclusion_option`表示所有者的选项；`finished_overall_conclusion_option`表示整体选项。在`Update Review Opinion and Conclusion`中使用`key`作为`finished_conclusion_option_key`。
- 产品文档中可能将此字段称为“Get Conclusion Option Lable”；API名称中使用“Label”。

---

---

（由于文档内容较长，此处仅展示了部分API的中文翻译。完整翻译需要继续处理剩余的API规范和用法说明。）