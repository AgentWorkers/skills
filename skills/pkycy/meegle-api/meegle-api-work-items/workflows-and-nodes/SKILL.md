---
name: meegle-api-workflows-and-nodes
description: Meegle OpenAPI：用于工作流和节点操作。
metadata: { openclaw: {} }
---
# Meegle API — 工作流与节点

提供用于管理工作项工作流及工作流节点的相关API。

## 范围

- 获取工作流详细信息（节点/状态流程、节点、连接关系、调度计划、子任务、表单）
- 获取工作流详细信息（WBS）
- 更新节点/调度计划
- 完成/回滚节点
- 状态流程转换
- 获取节点或状态流程所需的信息
- 审核管理

---

## 获取工作流详细信息

获取指定工作空间和工作项类型下的工作流实例的详细信息，包括节点状态、负责人、预估得分、节点表单、子任务和连接关系。支持基于节点的工作流（如需求）和基于状态的工作流（如缺陷、版本）。

### 使用场景

- 在为工作项构建工作流用户界面或报告时
- 当需要节点级别的数据（如调度计划、负责人、节点字段、子任务、检查者、完成信息）时
- 当需要区分基于节点的工作流（`flow_type`为0）和基于状态的工作流（`flow_type`为1）时

### API 规范：`get_workflow_detail`

```yaml
name: get_workflow_detail
type: api
description: Workflow info for a work item: nodes, connections, schedules, assignees, subtasks; flow_type 0 node / 1 status.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/workflow/query" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { fields: array, flow_type: integer (0|1), expand: object }
outputs: { data: object }
constraints: [Permission Management – Work Items]
error_mapping: { 30005: Work item not found, 20026: FlowType error, 20027: FlowType error, 10001: No permission, 20014: Project mismatch, 50006: DB error, 20015: Field mix specified/excluded }
```

### 使用说明

- **flow_type**：使用**0**表示基于节点的工作流（例如需求）；使用**1**表示基于状态的工作流（例如缺陷、版本）。
- **fields**：仅使用一种模式——正列表（例如`["name","created_at"]`）或负列表（例如`["-name","-created_at"]`）。混合使用会导致错误（20015）。
- **expand.need_user_detail**：设置为`true`可在响应中获取负责人的详细信息（电子邮件、中文名、英文名、用户键、用户名）。
- **data**：遵循`NodesConnections`的结构；`workflow_nodes`包含调度计划、节点字段、子任务、检查者、完成信息、负责人使用模式等；`connections`定义状态键值之间的转换关系。

---

## 获取工作流详细信息（WBS）

获取基于节点的工作流实例的WBS（工作分解结构）信息。该功能仅在行业特别版中提供。返回WBS树（`related_sub_work_items`、`related_parent_work_item`）、可交付成果和连接关系。

### 使用场景

- 在为基于节点的工作流实例构建WBS视图或层次结构用户界面时
- 当需要集成可交付成果（`need_union_deliverable`）或调度表聚合（`need_schedule_table_agg`）时
- 当工作项是WBS工作项或WBS子工作项时

### API 规范：`get_workflow_details_wbs`

```yaml
name: get_workflow_details_wbs
type: api
description: WBS workflow for node-flow work item (industry edition); tree, deliverables, connections.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/wbs_view" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { need_union_deliverable: boolean, need_schedule_table_agg: boolean, expand: object }
outputs: { data: object }
constraints: [Work Item Instance permission, WBS or WBS sub work item only]
error_mapping: { 30005: Work item not found, 20089: Not WBS/WBS children, 20014: Project mismatch }
```

### 使用说明

- **WBS**：仅适用于行业特别版中的WBS工作项或WBS子工作项；否则会返回错误代码（20089）。
- **查询参数**：传递`need_union_deliverable`和`need_schedule_table_agg`作为查询参数（例如`?need_union_deliverable=true&need_schedule_table_agg=true`）。
- **datarelated_sub_work_items**：包含可交付成果、角色所有者、WBS状态映射的节点和子任务树；`related_parent_work_item`提供父WBS上下文；`connections`定义状态转换关系。

---

## 更新节点/调度计划

更新工作项中的特定节点信息：节点所有者、调度计划（`node_schedule`或差异调度计划）、节点表单字段和角色负责人。权限要求参见开发者平台 – 权限管理。

### 使用场景

- 当更新节点所有者（`node_owners`或`role_assignee`）、调度计划（`node_schedule`或`schedules`）或节点表单字段时
- 当对至少有两个负责人的任务节点使用差异调度计划（`schedules`数组）时
- 当通过传递空数组`node_owners`来清除所有节点所有者时

### API 规范：`update_nodes_scheduling`

```yaml
name: update_nodes_scheduling
type: api
description: Update node: owners, node_schedule or schedules, fields, role_assignee.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: PUT, url: "https://{domain}/open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/{node_id}" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string, node_id: string }
inputs: { node_owners: array, node_schedule: object, schedules: array, fields: array, role_assignee: array }
outputs: { data: object }
constraints: [Permission Management]
```

### 使用说明

- **node_owners**：省略表示不进行更改；`[]`表示移除所有所有者。值应为`user_key`（来自Meegle，例如在开发者平台中双击头像）。
- **node_schedule**与`schedules`：使用`node_schedule`表示单个动态调度计划；使用`schedules`表示按所有者划分的差异调度计划（任务节点必须至少有两个负责人）。
- **fields**：每个字段都需要`field_key`、`field_type_key`和`field_value`；`field_alias`是字段标识符。
- **role_assignee**：传递`role`和`owners`（用户键列表）；空数组`owners`表示清除该角色的负责人。

---

## 完成/回滚节点

完成或回滚特定工作项的节点。可选地在同一请求中更新节点所有者、调度计划、字段和角色负责人。权限要求参见开发者平台 – 权限管理。

### 使用场景

- 当完成节点（操作`confirm`）或回滚节点（操作`rollback`）时
- 当提交回滚原因（`rollback_reason`对于回滚操作是必填的）时
- 当同时更新节点数据（所有者、调度计划、字段和角色负责人）时

### API 规范：`node_completion_rollback`

```yaml
name: node_completion_rollback
type: api
description: Complete (confirm) or rollback a node; optionally update owners, schedule, fields, role_assignee.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/{node_id}/operate" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string, node_id: string }
inputs: { action: confirm|rollback, rollback_reason: string, node_owners: array, node_schedule: object, schedules: array, fields: array, role_assignee: array }
outputs: { data: object }
constraints: [Permission Management]
```

### 使用说明

- **action**：使用`confirm`完成节点，使用`rollback`回滚节点。当`action`为`rollback`时，`rollback_reason`是必填的。
- **node_id**：必须与`Get Workflow Detail`中返回的节点`state_key`匹配（例如`start`、`doing`、`end`）。
- 可选的身体字段（`node_owners`、`node_schedule`、`schedules`、`fields`、`role_assignee`）的使用方式与`Update Nodes/Scheduling`相同：省略表示不进行更改；空数组`node_owners`表示移除所有所有者。

---

## 状态流程转换

将基于状态的工作流实例转换到指定状态，并可选地更新状态表单字段和角色所有者。使用`Get Workflow Detail`中的`transition_id`（来自`connections`）。权限要求参见权限管理 – 工作项实例。

### 使用场景

- 当将基于状态的工作流（例如缺陷、版本）转移到另一个状态时
- 在转换过程中更新状态表单字段或角色所有者时
- 通过集成或自动化驱动状态变更时

### API 规范：`status_flow_transition`

```yaml
name: status_flow_transition
type: api
description: Transfer state-flow work item to target state; optional fields and role_owners; transition_id from Get Workflow Detail.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/workflow/{work_item_type_key}/{work_item_id}/node/state_change" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { transition_id: integer, fields: array, role_owners: array }
outputs: { data: object }
constraints: [Work Item Instance permission, state-flow only]
error_mapping: { 10002: Illegal transition, 20005: transition_id missing, 30005: Work item not found, 20090: Request intercepted, 20038: Param missing, 30009: Field not found, 30012: State not found, 50006: Field check failed }
```

### 使用说明

- **transition_id**：从`Get Workflow Detail`中获取（`flow_type`为1）；使用`connections`结构中的`transition_id`指定目标状态。该值不能为空或为0（20005）。
- **fields**：只有`status form`字段可以更新；使用`field_key`、`field_type_key`和`field_value`（以及`field_alias`作为标识符）。转换所需的字段必须填写（20038）。
- **role_owners**：与`role_assignee`的格式相同；空数组`owners`表示清除该角色的负责人。
- **10002**：确保请求的转换状态是从工作项的当前状态允许的。**20090**：如果请求被阻止，需要检查空间插件拦截规则。

## 获取节点或状态流程所需的信息

获取指定节点转换或状态转换所需的信息。仅支持单点查询。返回所需的表单项、节点字段、子任务和可交付成果。权限要求参见权限管理 – 工作项实例。

### 使用场景

- 在执行节点或状态转换之前，确定需要完成哪些表单字段、节点字段、子任务或可交付成果
- 在构建显示“缺少哪些内容”的转换用户界面时（使用`mode: unfinished`）
- 适用于基于节点的工作流（`state_key = 节点ID`）和基于状态的工作流（`state_key = 目标状态键`）的工作项

### API 规范：`get_required_info_node_or_status_flow`

```yaml
name: get_required_info_node_or_status_flow
type: api
description: Required info for node/status transition (form_items, node fields, tasks, deliverables); state_key = node or target state; mode optional (unfinished).

auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/work_item/transition_required_info/get" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, work_item_type_key: string, work_item_id: integer, state_key: string, mode: string }
outputs: { data: object }

constraints: [Permission: Work Item Instance, single-point query]
error_mapping: { 30005: Work item not found, 50006: Node no longer exists }
```

### 使用说明

- **state_key**：对于基于节点的工作流，使用节点的ID（来自`workflow_nodes`的`state_key`）。对于基于状态的工作流，使用转换的目标状态键。从`Get Workflow Detail`中获取有效值。
- **mode**：省略或留空表示获取所有未完成的信息；设置`unfinished`仅获取未填写/完成的项（例如用于“缺少哪些内容”的界面）。
- **data.form_items**：包括`class: control`（例如`workflow_state_info`和`state_info.node_fields`）和`class: field`（字段键、字段类型键、完成状态）的组合/多成员字段。`finished`表示需求是否满足。
- **data.tasks`/**data.deliverables**：转换所需的子任务和可交付成果；`finished`表示完成情况。**data.node_fields`：所需的节点级字段，`sub_field`和`not_finished_owner`用于多所有者字段。

## 批量请求审核意见和审核结论

批量查询节点的审核意见和结论。返回每个节点的`summary_mode`、意见（`finished_opinion_result`、`owners_finished_opinion_result`）和结论（`finished_conclusion_result`、`owners_finished_conclusion_result`）。权限要求参见权限管理 – 工作项实例。

### 使用场景

- 在一次请求中加载多个工作项的审核意见和结论时
- 在构建显示每个节点意见和结论的审核/批准用户界面时（每次请求最多10个节点）
- 当节点ID或状态键来自`Get Workflow Detail`时

### API 规范：`batch_request_review_opinion_and_conclusion`

```yaml
name: batch_request_review_opinion_and_conclusion
type: api
description: Batch query review opinions and conclusions per node; max 10 node_ids.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/work_item/finished/batch_query" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, work_item_id: integer, node_ids: array (max 10) }
outputs: { data: object }
constraints: [Work Item Instances permission, node_ids ≤ 10]
error_mapping: { 1000051120: Workflow not found, 1000051280: Params invalid }
```

### 使用说明

- **node_ids**：使用来自`Get Workflow Detail`的节点ID或`state_key`值（例如`start_0`、`start_1`）。每次请求最多10个节点。
- **summary_mode**：`calculation`表示汇总计算；`independence`表示独立完成。
- **opinion**/**conclusion**：`finished_opinion_result`和`finished_conclusion_result`是汇总结果；`owners_finished_opinion_result`和`owners_finished_conclusion_result`分别表示每个所有者（用户键）的结果。结论使用`key`、`label`、`origin_label`。

## 更新审核意见和结论

更新节点的审核意见或结论，或执行重置操作。支持节点级别的审核（仅限节点负责人）和所有者级别的个人评论。权限要求参见权限管理 – 工作项实例。

### 使用场景

- 当更新节点的审核意见（`opinion`）或结论（`finished_conclusion_option_key`）时
- 当清除意见或结论（传递空字符串）或重置所有审核信息（`reset: true`；仅限转移操作）时
- 当操作节点审核（`operation_type: node`）或个人评论（`operation_type: owner`）时

### API 规范：`update_review_opinion_and_conclusion`

```yaml
name: update_review_opinion_and_conclusion
type: api
description: Update or reset review opinion and conclusion; node-level or owner-level (operation_type).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/work_item/finished/update" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, work_item_id: integer, node_id: string, opinion: string, finished_conclusion_option_key: string, operation_type: node|owner, reset: boolean }
outputs: { data: object }
constraints: [Work Item Instance permission]
error_mapping: { 1000051814: Node not exist, 1000051120: Workflow not found, 20007: Work item aborted, 1000053308: Conclusion label not exist, 1000053219: Only node owners, 1000051280: Parameter invalid }
```

### 使用说明

- **opinion**/**finished_conclusion_option_key**：省略表示不进行更改；**""`表示删除该值。**finished_conclusion_option_key`应与`Batch Request Review Opinion and Conclusion`或`Get Conclusion Option Label`中的结论键匹配。
- **operation_type**：使用`node`表示节点级别的审核；使用`owner`表示个人评论。当`reset`为`false`且正在更新所有者级别数据时需要此参数。
- **reset: true`：清除当前的审核信息；仅`transfer person`可以执行此操作。当`reset`为`true`时，`opinion`、`finished_conclusion_option_key`和`operation_type`可以留空。

## 获取结论选项标签

查询指定节点的配置审核结论标签。用于填充节点审核结论（例如在`Update Review Opinion and Conclusion`中）。权限要求参见权限管理 – 工作项实例。

### 使用场景

- 在构建需要显示每个节点允许的审核结论选项列表的审核/批准用户界面时
- 在验证或显示结论选项（`key`、`label`、`origin_label`）时
- 当节点ID或状态键来自`Get Workflow Detail`时（每次请求最多10个节点）

### API 规范：`get_conclusion_option_label`

```yaml
name: get_conclusion_option_label
type: api
description: Query conclusion labels per node (key, label, origin_label); max 10 node_ids.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/work_item/finished/query_conclusion_option" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, work_item_id: integer, node_ids: array (max 10) }
outputs: { data: array }
constraints: [Work Item Instances permission, node_ids ≤ 10]
error_mapping: { 1000051120: Workflow not found }
```

### 使用说明

- **node_ids**：使用来自`Get Workflow Detail`的节点ID或`state_key`（例如`start_0`、`started_0`）。每次请求最多10个节点。
- **data`项：`finished_conclusion_option`表示节点级别的选项；`finished_overall_conclusion_option`表示所有者的选项；`finished_overall_conclusion_option`表示整体选项。在`Update Review Opinion and Conclusion`中使用`key`作为`finished_conclusion_option_key`。
- 产品文档中的标题可能显示为“Get Conclusion Option Lable”；API名称使用“Label”。

---

---

（由于文档内容较长，上述翻译仅包含了部分内容。如果需要完整翻译，请提供更多文档内容。）