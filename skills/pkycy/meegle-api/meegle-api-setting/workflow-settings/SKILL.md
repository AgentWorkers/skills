---
name: meegle-api-setting-workflow-settings
description: Meegle OpenAPI：用于工作流/流程模板设置的操作（包括列出、获取详情、创建、更新和删除）。
metadata:
  openclaw: {}
---
# Meegle API — 设置（工作流设置）

该技能下的API包括：获取工作流模板、获取工作流模板的详细设置、创建工作流模板、更新工作流模板以及删除工作流模板。

---

## 获取工作流模板

获取指定工作项类型下的所有流程模板列表。响应数据遵循`TemplateConf`结构（包含`version`、`unique_key`、`is_disabled`、`template_id`、`template_name`等字段）。权限要求：权限管理 – 配置（Permission Management – Configuration）。

### 使用场景

- 当需要列出某种工作项类型（如故事或问题）的工作流/流程模板时
- 当需要`template_id`、`unique_key`或`template_name`以执行获取工作流模板详细设置、更新工作流模板或删除工作流模板操作时
- 在构建模板选择界面或检查每个模板的`is_disabled`状态/版本信息时

### API规范：`get_workflow_templates`

```yaml
name: get_workflow_templates
type: api
description: >
  Obtain the list of all process templates under the specified work item type.
  Returns list per TemplateConf: version, unique_key, is_disabled, template_id, template_key, template_name.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/template_list/{work_item_type_key}
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
    description: Work item type. Obtain via Get work item types in space.

outputs:
  data:
    type: array
    description: >
      List of TemplateConf. Each has version, unique_key, is_disabled, template_id,
      template_key, template_name.

constraints:
  - Permission: Permission Management – Configuration
```

### 使用说明

- **data**字段：在调用获取工作流模板详细设置、更新工作流模板或删除工作流模板时，需要提供`template_id`或`unique_key`。`is_disabled`字段表示模板是否被禁用（具体含义因产品而异）。
- 有关常见错误代码和服务器端调用分析，请参考产品文档中的“Open API错误代码”（Open API Error Codes）。

---

## 获取工作流模板的详细设置

获取指定流程模板的详细配置信息，包括节点配置和节点转移规则。该接口不支持节点事件配置。响应数据遵循`TemplateDetail`结构（包含`template_id`、`template_name`、`version`、`work_item_type_key`、`workflow_confs`、`connections`等字段）。权限要求：权限管理 – 流程类型（Permission Management – Process Type）。

### 使用场景

- 当需要编辑或显示工作流模板的节点、字段、子任务、子工作项以及转换规则（连接关系）时
- 当`template_id`通过`get_workflow_templates`获取时，或者需要获取创建工作项的元数据或字段信息时
- 在构建模板编辑器或同步工作流配置时；如果省略`template_id`，系统将使用该工作项类型下的第一个流程模板（具体行为因产品而异）

### API规范：`get_detailed_settings_of_workflow_templates`

```yaml
name: get_detailed_settings_of_workflow_templates
type: api
description: >
  Obtain detailed configuration of the specified process template: node info and
  node transfer config. TemplateDetail includes workflow_confs (nodes) and connections.
  Node event configuration not supported.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/template_detail/{template_id}
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
  template_id:
    type: string
    required: true
    description: >
      Process template ID. Obtain from Get Workflow Templates, or from template
      field options in Get metadata for creating work items / Get field information.
      When not passed, first process template of the work item type may be used (product-dependent).

outputs:
  data:
    type: object
    description: >
      TemplateDetail: template_id, template_name, version, is_disabled,
      work_item_type_key, workflow_confs (nodes with name, state_key, owner_usage_mode,
      fields, sub_tasks, sub_work_items, done_operation_role, connections, etc.),
      connections (source_state_key, target_state_key).

constraints:
  - Permission: Permission Management – Process Type
  - Node event configuration not supported

error_mapping:
  50006: Template not found (check template_id)
  30001: Data not found (template_id not found in project_key space)
```

### 使用说明

- **template_id**：可以从`get_workflow_templates`（返回的`data[]`中的`template_id`）或通过“获取创建工作项的元数据”/“获取字段信息”接口获取。该ID必须属于由`project_key`（默认值为30001）标识的模板空间。
- `data.workflow_confs`：一个包含节点配置的数组，每个节点配置包含`state_key`、`name`、`fields`、`sub_tasks`、`sub_work_items`、`done_operation_role`、`connections`等字段。`dataconnections`表示状态键值之间的转换关系。
- 该接口不支持节点事件配置。

---

## 创建工作流模板

在指定工作项类型下创建一个新的流程模板。可以选择通过`copy_template_id`从现有模板复制配置。返回新的`template_id`。权限要求：权限管理 – 配置（Permission Management – Configuration）。

### 使用场景

- 当需要为某种工作项类型创建新的流程模板时
- 当需要复制现有模板时：使用`get_workflow_templates`获取的`copy_template_id`
- 当需要使用返回的`template_id`来执行获取工作流模板详细设置、更新或删除操作时

### API规范：`create_workflow_templates`

```yaml
name: create_workflow_templates
type: api
description: >
  Create a new process template under the specified work item type. Optional
  copy_template_id to reuse an existing template. Returns new template ID (int64).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/template/v2/create_template
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
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtain via Get work item types in space.
  template_name:
    type: string
    required: true
    description: Process template name; must not duplicate an existing template name.
  copy_template_id:
    type: integer
    required: false
    description: >
      ID of template to copy from. Obtain via Get Workflow Templates (list of process
      templates under the work item type). Omit to create an empty new template.

outputs:
  data:
    type: integer
    description: Template ID of the newly created process template (int64).

constraints:
  - Permission: Permission Management – Configuration
  - Current user must have space configuration permission (else 10005)

error_mapping:
  10005: No project admin permission (no permission to configure the space)
  50006: Template name duplicate (template name already exists; change the name)
```

### 使用说明

- `template_name`必须在该工作项类型下的所有流程模板中保持唯一性；重复的名称会导致错误代码50006。
- `copy_template_id`：来自`get_workflow_templates`（返回的`data[]`中的`template_id`）。提供此ID时，新模板将基于该模板创建；如果省略，则创建一个空模板。
- 在调用获取工作流模板详细设置、更新工作流模板或删除工作流模板时，需要使用返回的`template_id`。
- 创建模板需要管理员权限（权限代码为10005）。

---

## 更新工作流模板

更新指定流程模板的配置。支持节点流程配置（`workflow_confs`）和状态流程配置（`state_flow_confs`）。权限要求：权限管理 – 设置（Permission Management – Settings）。

### 使用场景

- 当需要修改工作流模板中的节点配置（通过`workflow_confs`或`state_flow_confs`中的`action`字段添加/删除/修改节点时
- 当`template_id`通过`get_workflow_templates`、获取创建工作项的元数据或获取字段信息获取时
- 当需要更新模板的所有者使用模式（`owner_usage_mode`）、所有者角色（`owner_roles`）、所有者信息（`owners`）、调度需求（`need_schedule`）、传递模式（`pass_mode`）、已完成操作的角色（`done_operation_role`）等属性时

### API规范：`update_workflow_template`

```yaml
name: update_workflow_template
type: api
description: >
  Update the specified process template. workflow_confs for node flow (WorkflowConf),
  state_flow_confs for state flow (StateFlowConf). Node action: 1 Add, 2 Delete (state_key only), 3 Modify.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: PUT
  url: https://{domain}/open_api/template/v2/update_template
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
  template_id:
    type: integer
    required: true
    description: >
      Process template ID. From Get Workflow Templates, or template field options in
      Get metadata for creating work items / Get field information.
  workflow_confs:
    type: array
    required: false
    description: Node flow configuration per WorkflowConf. Each can have action (1 add, 2 delete, 3 modify), state_key, name, tags, pre_node_state_key, owner_usage_mode, owner_roles, owners, need_schedule, different_schedule, deletable, deletable_operation_role, pass_mode, done_operation_role, done_schedule, done_allocate_owner, task_confs, etc. For action 2 (delete), only state_key required.
  state_flow_confs:
    type: array
    required: false
    description: State flow configuration per StateFlowConf structure.

outputs:
  data:
    type: object
    description: Empty on success (no data in response).

constraints:
  - Permission: Permission Management – Settings
  - Current user must have space configuration permission (else 10005)

error_mapping:
  10005: No project admin permission (operator cannot configure the space)
  1000052062: Project key is wrong (project_key incorrect)
  20006: Invalid param (state_key illegal for node flow work item)
  50006: Template not found (template_id incorrect)
```

### 使用说明

- `template_id`：可以从`get_workflow_templates`获取，或者通过“获取创建工作项的元数据”/“获取字段信息”接口获取。该ID必须属于正确的模板空间；如果找不到该ID，将返回错误代码50006。
- `workflow_confs`：用于定义节点流程的配置；`action`字段的取值包括：1 = 添加节点，2 = 删除节点（仅需要`state_key`），3 = 修改节点。结构遵循`WorkflowConf`格式（包含`state_key`、`name`、`tags`、`owner_usage_mode`、`owner_roles`、`owners`、`need_schedule`、`different_schedule`、`pass_mode`、`done_operation_role`等字段）。
- `state_flow_confs`：用于定义状态流程的配置；仅适用于支持状态流程的工作项类型。
- 创建或修改此类模板需要管理员权限（权限代码为10005）。

---

## 删除工作流模板

删除指定的流程模板。权限要求：权限管理 – 设置（Permission Management – Settings）。

### 使用场景

- 当需要删除某种工作项类型下的流程模板时
- 当`template_id`通过`get_workflow_templates`、获取创建工作项的元数据或获取字段信息获取时

### API规范：`delete_workflow_templates`

```yaml
name: delete_workflow_templates
type: api
description: >
  Delete the specified process template. Path parameters project_key and template_id.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: DELETE
  url: https://{domain}/open_api/template/v2/delete_template/{project_key}/{template_id}
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
  template_id:
    type: string
    required: true
    description: >
      Process template ID. From Get Workflow Templates, or template field options in
      Get metadata for creating work items / Get field information.

outputs:
  data:
    type: object
    description: Empty on success (no data in response).

constraints:
  - Permission: Permission Management – Settings

error_mapping:
  9999: Invalid param (key template_id value invalid; template_id incorrect)
```

### 使用说明

- `template_id`：可以从`get_workflow_templates`（返回的`data[]`中的`template_id`）或通过“获取创建工作项的元数据”/“获取字段信息”接口获取。无效或不存在的`template_id`会导致错误代码9999。
- 成功响应不包含`data`字段；请检查`err_code`是否为0。