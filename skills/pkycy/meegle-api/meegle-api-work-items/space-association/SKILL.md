---
name: meegle-api-space-association
description: Meegle OpenAPI：用于空间关联操作的接口。
metadata: { openclaw: {} }
---
# Meegle API — 空间关联（Space Association）

提供与空间关联相关的API，用于将工作项（work items）与空间（spaces）链接起来以及管理这些关联关系。

## 功能范围

- 将工作项与空间关联起来
- 列出或管理空间关联关系
- 相关的关联操作接口

---

## 获取空间关联规则列表

获取指定空间下配置的所有空间关联规则。可选地，可以根据关联的空间（remote_projects）进行过滤。

### 使用场景

- 当需要列出某个项目的空间关联规则时
- 当需要查看当前空间与哪些远程空间存在关联关系时
- 在开发用于管理空间关联关系的用户界面或自动化脚本时

### API 规范：`get_space_association_rules`

```yaml
name: get_space_association_rules
type: api
description: List space association rules; optional filter by remote_projects.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/relation/rules" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string }
inputs: { remote_projects: array }
outputs: { data: array }
constraints: [Permission: Space Association]
error_mapping: { 1000052062: Project key wrong, 1000052063: Not found simple name }
```

### 使用说明

- `remote_projects`：可选参数；如果提供，返回的规则将仅限于与这些远程空间相关联的规则。
- `data`：每个远程项目的规则组数组；每个规则组包含规则详情（如关联类型、支持的工作项类型、聊天组合并方式等）。

---

## 获取与指定工作项关联的工作项列表

获取与该工作项空间关联的所有工作项实例。可以通过请求参数根据关联规则、远程空间或相关工作项进行过滤。

### 使用场景

- 当需要列出通过空间关联与该工作项关联的所有工作项时
- 当需要根据关联规则、远程项目或工作项类型进行筛选时
- 在开发跨空间关联管理的用户界面或报告时

### API 规范：`get_work_items_under_space_association`

```yaml
name: get_work_items_under_space_association
type: api
description: List work items spatially associated with given work item; optional filters (rule, project, type).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/relation/{work_item_type_key}/{work_item_id}/work_item_list" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { relation_rule_id: string, relation_work_item_id: integer, relation_work_item_type_key: string, relation_project_key: string }
outputs: { data: array }
constraints: [Permission: Work Item Instance]
error_mapping: { 10001: Not permitted, 30005: Work item not found, 50006: Too many records }
```

### 使用说明

- `relation_rule_id`：可选过滤条件；该ID可以从`get_space_association_rules`接口的返回结果中获取。
- `relation_project_key`、`relation_work_item_type_key`、`relation_work_item_id`：可选的过滤条件，用于进一步缩小搜索范围。
- `data`：包含`RelationInstance`对象的数组；每个对象包含远程项目信息、工作项的ID/名称/类型以及关联规则的ID/名称。

---

## 将空间关联规则应用于工作项

在指定的工作项实例与其他工作项实例之间建立空间关联关系。可以选择性地指定关联规则，并提供相关的工作项信息（如项目ID、工作项ID、工作项类型ID、聊天组合并方式）。

### 使用场景

- 当需要将多个工作项通过空间关联方式绑定到当前工作项时
- 当需要为新关联关系应用特定的规则时
- 当需要通过集成或脚本自动化实现跨空间关联操作时

### API 规范：`apply_space_association_rules_to_work_items`

```yaml
name: apply_space_association_rules_to_work_items
type: api
description: Bind work items via space association; optional relation_rule_id, instances (project_key, work_item_id, work_item_type_key, chat_group_merge).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/relation/{work_item_type_key}/{work_item_id}/batch_bind" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { relation_rule_id: string, instances: array }
outputs: { data: object }
constraints: [Permission: Work Item Instances]
error_mapping: { 1000051617: Bind duplicate, 30005: Work item not found, 30015: Record not found }
```

### 使用说明

- `relation_rule_id`：可选参数；该ID可以从`get_space_association_rules`接口的返回结果中获取。
- `instances`：每个元素包含项目ID（`project_key`）、工作项ID（`work_item_id`）、工作项类型ID（`work_item_type_key`）以及聊天组合并方式（`chat_group_merge`）；在API允许的情况下，这些字段可以留空或使用空字符串。
- 成功响应时，`data`字段为空；请检查`err_code`是否为0，以及`err`和`err_msg`是否为空。

---

## 移除与工作项的空间关联关系

解除指定工作项与其他工作项之间的空间关联关系。可以选择性地指定关联规则或要解除关联的工作项。

### 使用场景

- 当需要从当前工作项中移除某个空间关联关系时
- 当需要根据关联规则或相关工作项来清除所有跨空间关联关系时
- 当需要从外部系统同步关联状态时（例如，在删除操作时解除关联）

### API 规范：`remove_work_items_under_space_association`

```yaml
name: remove_work_items_under_space_association
type: api
description: Unbind space association; optional relation_rule_id, relation_work_item_id.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: DELETE, url: "https://{domain}/open_api/{project_key}/relation/{work_item_type_key}/{work_item_id}" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { relation_rule_id: string, relation_work_item_id: integer }
outputs: { data: object }
constraints: [Permission: Work Item Instances]
error_mapping: { 20006: Invalid param }
```

### 使用说明

- `relation_rule_id`和`relation_work_item_id`：可选参数；用于指定要解除的关联关系。如果省略这些参数，系统可能会根据其他规则来自动解除关联（请参考产品文档）。
- 请求示例中`relation_work_item_id`被作为字符串传递；但实际上API文档中该参数的类型为`int64`——两种形式通常都被接受。
- 成功响应时，`data`字段为空；请检查`err_code`是否为0，以及`err`和`err_msg`是否为空。