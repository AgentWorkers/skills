---
name: meegle-api-space-association
description: Meegle OpenAPI：用于空间关联操作的功能。
metadata:
  openclaw: {}
---
# Meegle API — 空间关联（Space Association）

提供用于将工作项（work items）与空间（spaces）关联以及管理这些关联的API。

## 功能范围

- 将工作项与空间关联
- 列出或管理空间关联关系
- 相关的关联操作端点（association endpoints）

---

## 获取空间关联规则列表（Get the List of Space Association Rules）

获取指定空间下配置的所有空间关联规则。可选择根据关联的空间（remote_projects）进行过滤。

### 使用场景

- 列出某个项目的空间关联规则
- 检查当前空间与哪些远程空间存在关联
- 构建用于管理空间关联的UI或自动化脚本

### API规范：get_space_association_rules

```yaml
name: get_space_association_rules
type: api
description: >
  Obtain the list of space association rules configured under the specified space.
  Response follows ProjectRelationRules structure.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/relation/rules
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

inputs:
  remote_projects:
    type: array
    items: string
    required: false
    description: >
      List of project_key for associated (remote) spaces.
      Used to filter rules for specific spaces.

outputs:
  data:
    type: array
    description: >
      List of ProjectRelationRules. Each item includes remote_project_key,
      remote_project_name, and rules array (id, name, disabled,
      work_item_relation_id, work_item_relation_name, current_work_item_type_key,
      remote_work_item_type_key, chat_group_merge, etc.).

constraints:
  - Permission: Permission Management – Space Association

error_mapping:
  1000052062: Project key is wrong (project_key incorrect)
  1000052063: Not found simple name (project_key incorrect)
```

### 使用说明

- **remote_projects**：可选参数；指定后，返回的规则将仅限于与这些远程空间相关联的规则。
- **data**：每个远程项目的规则组数组；每个规则组包含规则详细信息（如关联类型、支持的工作项类型、聊天组合并方式等）。

---

## 获取与指定工作项关联的工作项列表（Get the List of Work Items under Space Association）

获取与指定工作项关联的所有工作项实例。可通过请求参数根据关联规则、远程空间或相关工作项进行过滤。

### 使用场景

- 列出通过空间关联与当前工作项关联的所有工作项
- 根据关联规则、远程项目或工作项类型筛选工作项
- 构建跨空间关联的UI或报告

### API规范：get_work_items_under_space_association

```yaml
name: get_work_items_under_space_association
type: api
description: >
  Obtain the list of work item instances that are spatially associated with
  the specified work item instance. Optional filters by rule, project, or related work item.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/relation/{work_item_type_key}/{work_item_id}/work_item_list
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
    description: Work item type. Obtainable via "Get work item types in the space". Must match work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, click ··· in the upper right, then ID to copy.

inputs:
  relation_rule_id:
    type: string
    required: false
    description: Space association rule ID. Obtain via Get the List of Rules for Space Association.
  relation_work_item_id:
    type: integer
    required: false
    description: ID of the associated work item; used to filter by a specific related work item.
  relation_work_item_type_key:
    type: string
    required: false
    description: Work item type key of the associated work items.
  relation_project_key:
    type: string
    required: false
    description: project_key of the associated (remote) space.

outputs:
  data:
    type: array
    description: >
      List of associated work items (RelationInstance). Each item includes
      relation_project_name, relation_work_item_id, relation_work_item_name,
      relation_work_item_type_key/name, project_relation_rule_id/name, relation_project_key.

constraints:
  - Permission: Permission Management – Work Item Instance

error_mapping:
  10001: Operation not permitted (insufficient permissions)
  30005: Work item not found (work_item_id incorrect or does not match work_item_type_key)
  50006: Too many records (exceed system limit; reduce or batch)
```

### 使用说明

- **relation_rule_id**：可选过滤条件；可从“获取空间关联规则列表”（get_space_association_rules）接口获取。
- **relation_project_key**、**relation_work_item_type_key**、**relation_work_item_id**：可选过滤条件，用于进一步缩小搜索范围。
- **data**：包含关联关系信息的RelationInstance对象数组（包含远程项目信息、工作项ID/名称/类型以及规则ID/名称）。

---

## 将空间关联规则应用于工作项（Apply Space Association Rules to Work Items）

建立指定工作项与其他工作项之间的空间关联。可选择指定关联规则，并提供相关的工作项实例（project_key、work_item_id、work_item_type_key、chat_group_merge）。

### 使用场景

- 将多个工作项通过空间关联绑定到当前工作项
- 为新关联关系应用特定的规则
- 通过集成或脚本自动化实现跨空间关联操作

### API规范：apply_space_association_rules_to_work_items

```yaml
name: apply_space_association_rules_to_work_items
type: api
description: >
  Establish spatial association binding between the specified work item instance
  and the incoming list of work item instances. Optional relation_rule_id and instances list.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/relation/{work_item_type_key}/{work_item_id}/batch_bind
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
    description: Work item type. Obtain via Get work item types under the space. Must match work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In details, expand ··· > ID in the upper right to obtain.

inputs:
  relation_rule_id:
    type: string
    required: false
    description: Space association rule ID. Obtain via Get the List of Rules for Space Association.
  instances:
    type: array
    required: false
    description: List of work item instances to bind.
    items:
      type: object
      properties:
        project_key:
          type: string
          description: project_key of the associated space (can be empty in some cases).
        work_item_id:
          type: string
          description: Work item instance ID to associate.
        work_item_type_key:
          type: string
          description: Work item type key of the instance (can be empty in some cases).
        chat_group_merge:
          type: integer
          description: Chat group merge option (e.g. 1).

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Permission Management – Work Item Instances

error_mapping:
  1000051617: Project relation instance bind duplicate (binding already exists)
  30005: Work item not found (path work item does not exist)
  30015: Record not found (associated work item does not exist)
```

### 使用说明

- **relation_rule_id**：可选参数；可从“获取空间关联规则列表”（get_space_association_rules）接口获取。
- **instances**：每个元素包含工作项的关联信息（project_key、work_item_id、work_item_type_key、chat_group_merge）；在API允许的情况下，这些字段可以留空。
- 成功响应时，**data**字段为空；请检查**err_code**是否为0，以及**err**和**err_msg**是否为空。

---

## 删除与指定工作项关联的工作项（Remove Work Items under Space Association）

解除指定工作项与其他工作项之间的空间关联。可选择指定关联规则或要解除关联的工作项。

### 使用场景

- 单个删除当前工作项与某个空间的关联
- 根据规则或相关工作项清除所有跨空间关联
- 从外部系统同步关联状态（例如在删除操作时解除关联）

### API规范：remove_work_items_under_space_association

```yaml
name: remove_work_items_under_space_association
type: api
description: >
  Unbind the space association relationship between the specified work item instance
  and the incoming work item instance. Optional relation_rule_id and relation_work_item_id.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: DELETE
  url: https://{domain}/open_api/{project_key}/relation/{work_item_type_key}/{work_item_id}
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
    description: Work item type. Obtain via Get work item types under the space. Must match work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In details, expand ··· > ID in the upper right to obtain.

inputs:
  relation_rule_id:
    type: string
    required: false
    description: Space association rule ID. Obtain via Get the List of Rules for Space Association.
  relation_work_item_id:
    type: integer
    required: false
    description: >
      Work item instance ID to unbind. In work item details, expand ··· > ID in the upper right to obtain.
      API types this as int64; string IDs in request body are accepted (e.g. "301228xxxx").

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Permission Management – Work Item Instances

error_mapping:
  20006: Invalid param (work_item or relation_rule_id not found; relation_work_item_id or relation_rule_id incorrect)
```

### 使用说明

- **relation_rule_id**和**relation_work_item_id**：可选参数；用于指定要解除的关联关系。如果省略，系统可能会根据其他规则自动解除关联（请参考产品文档）。
- 请求示例中**relation_work_item_id**以字符串形式提供；API文档中指定其类型为int64——实际使用时两者均可接受。
- 成功响应时，**data**字段为空；请检查**err_code**是否为0，以及**err**和**err_msg**是否为空。