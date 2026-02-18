---
name: meegle-api-setting-field-settings
description: Meegle OpenAPI用于字段设置：获取、创建和更新自定义字段。
metadata:
  openclaw: {}
---
# Meegle API — 设置（字段设置）

该技能下的API包括：获取字段信息（Get Field Information）、创建自定义字段（Create Custom Field）以及更新自定义字段（Update Custom Field）。

---

## 获取字段信息（Get Field Information）

获取指定空间内所有字段的基本信息；如果提供了**work_item_type_key**，则仅获取该工作项类型下的字段信息。响应数据遵循SimpleField结构（field_key、field_type_key、select字段的选项信息、compound_field字段的子字段信息）。权限要求：权限管理 – 配置（Permission Management – Configuration）。

### 使用场景

- 在构建需要字段键、类型、别名和作用域（work_item_scopes）的字段选择器或表单用户界面时。
- 当需要为select类型的字段设置选项列表（如label、value、order、is_disabled等），或者为compound_field字段设置子字段时。
- 在更新工作项基本信息设置（如schedule_field_key、estimate_point_field_key、actual_work_time_field_key）或进行工作项读写操作时。

### API规范：get_field_information

```yaml
name: get_field_information
type: api
description: >
  Obtain all fields under the space or under a work item type. Returns SimpleField
  list: field_key, field_type_key, field_alias, field_name, is_custom_field,
  work_item_scopes, value_generate_mode, relation_id; options for select; compound_fields for compound_field.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/field/all
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
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).

inputs:
  work_item_type_key:
    type: string
    required: false
    description: Work item type. Obtain via Get work item types in space. Omit to get all fields in space.

outputs:
  data:
    type: array
    description: >
      List of SimpleField. Each has field_key, field_type_key, field_alias, field_name,
      is_custom_field, work_item_scopes, value_generate_mode, relation_id. Select-type
      fields include options (order, color, is_visibility, is_disabled, label, value,
      work_item_type_key). compound_field type includes compound_fields (array of
      field objects with field_key, field_type_key, field_name, etc.).

constraints:
  - Permission: Permission Management – Configuration

error_mapping:
  30001: Data not found (project_key does not match work_item_type_key; no such work item type in this space)
```

### 使用说明

- **work_item_type_key**：省略该参数可获取该空间内的所有字段；设置为特定类型（如`story`、`chart`）时，仅获取该类型下的字段。如果该类型不存在于该空间中，将返回30001。
- **data**字段：在更新工作项类型设置（如schedule_field_key）或通过工作项API发送字段值时使用**field_key**；**field_type_key**（如`multi_text`、`select`、`compound_field`）决定了字段值的格式。

---

## 创建自定义字段（Create Custom Field）

在指定的工作项类型下创建一个新的自定义字段，并返回新的**field_key**。权限要求：权限管理 – 工作项实例（Permission Management – Work Item Instances）。有关详细信息，请参阅权限管理文档。

### 注意事项

- 工作项关联字段的默认数据可见性是固定的，无法修改条件数据范围。
- 附件类型字段以及外部系统信号/多值外部系统信号字段不支持设置默认值。
- 不支持修改字段的有效性（默认的有效性设置）。
- 不支持更新工作项类型、创建者、提交时间、完成时间以及业务线相关字段。
- 不支持投票字段。

### 使用场景

- 当需要向工作项类型添加新的自定义字段（如文本、选择框、日期、用户、数字、链接等）时。
- 当需要重用其他字段的选项（使用`value_type 1`和`reference_work_item_type_key`、`reference_field_key`）或定义自定义选项（使用`field_value`）时。
- 当需要配置团队选项以支持级联单选/多选（tree_select、tree_multi_select）时；这些选项与`field_value`互斥。

### API规范：create_custom_field

```yaml
name: create_custom_field
type: api
description: >
  Create a custom field under the specified work item type. Returns field_key.
  Supports text, select, tree_select, date, user, number, link, multi_file, bool,
  work_item_related_select, etc. field_value and team_option are mutually exclusive.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/field/{work_item_type_key}/create
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
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtain via Get work item types in space.

inputs:
  field_name:
    type: string
    required: true
    description: Field name; must not duplicate other fields.
  field_alias:
    type: string
    required: false
    description: Field alias; cannot duplicate other fields of the same work item type.
  field_type_key:
    type: string
    required: true
    description: >
      Field type. See Attributes and fields. Supported: text, multi_text, select,
      multi_select, tree_select, tree_multi_select, radio, user, multi_user, date,
      schedule, link, number, multi_file, bool, signal, work_item_related_select,
      work_item_related_multi_select.
  value_type:
    type: integer
    required: false
    description: >
      Option source for select/multi_select/tree_select/tree_multi_select/radio.
      0: Custom (default); 1: Reuse. When 1, reference_work_item_type_key and reference_field_key required.
  field_value:
    type: object
    required: false
    description: >
      Option values; structure per Attributes and fields. For select, multi_select,
      tree_select, tree_multi_select, radio. Mutually exclusive with team_option.
  reference_work_item_type_key:
    type: string
    required: false
    description: Required when value_type = 1.
  reference_field_key:
    type: string
    required: false
    description: Required when value_type = 1.
  is_multi:
    type: boolean
    required: false
    description: For text: true = multi-line; false = single-line (default).
  format:
    type: boolean
    required: false
    description: For date: true = date only; false = date + time (default).
  free_add:
    type: integer
    required: false
    description: For select/tree_select etc.: 1 = allow users to add options; 2 = No (default).
  work_item_relation_uuid:
    type: string
    required: false
    description: Work item relationship ID from Get field information. Required for work_item_related_select / work_item_related_multi_select.
  default_value:
    type: object
    required: false
    description: >
      Default value; structure per field type (Attributes and fields). Not supported
      for attachment, external system signal, multi-value external system signal.
  help_description:
    type: string
    required: false
    description: Help instructions.
  authorized_roles:
    type: array
    items: string
    required: false
    description: >
      Roles or system keys that can access/operate this field. Default "Anyone".
      e.g. _master (Administrator), _owner (Creator), _role (Requirement-related person).
  team_option:
    type: object
    required: false
    description: >
      Team scope per TeamOption. Only for tree_select, tree_multi_select.
      Mutually exclusive with field_value.

outputs:
  data:
    type: string
    description: Created field key (e.g. field_73jds7).

constraints:
  - Permission: Permission Management – Work Item Instances
  - field_value and team_option cannot both be sent

error_mapping:
  1000051468: Field alias repeated (field_alias duplicate)
  1000051469: Invalid update version (field being concurrently updated)
  1000051750: Field name has been used (field_name duplicate)
  1000053603: Field name length exceeded (max characters for field name)
```

### 使用说明

- **field_type_key**：使用支持的API类型（如`text`、`select`、`date`、`user`、`number`、`link`、`multi_file`、`bool`、`work_item_related_select`、`work_item_related_multi_select`）。具体类型请参考产品文档中的“属性和字段”（Attributes and Fields）部分。
- **field_value**与**team_option**的区别：`field_value`用于选择框/树形选择框等字段的自定义/重用选项；`team_option`仅用于具有团队作用域的级联单选/多选字段。两者不可同时使用。
- **value_type 1**：设置`reference_work_item_type_key`和`reference_field_key`以重用其他字段的选项。
- **work_item_relation_uuid**：从`Get Field Information` API获取，用于`work_item_related_select`/`work_item_related_multi_select`操作。
- 附件类型字段、外部系统信号字段以及多值外部系统信号字段不支持设置默认值。

---

## 更新自定义字段（Update Custom Field）

更新指定自定义字段的配置。通过**field_key**来标识要更新的字段。权限要求：权限管理 – 配置（Permission Management – Configuration）。

### 注意事项

- 工作项关联字段的默认数据可见性是固定的，无法修改条件数据范围。
- 附件类型字段以及外部系统信号/多值外部系统信号字段不支持设置默认值。
- 不支持修改字段的有效性（默认的有效性设置）。
- 不支持更新工作项类型、创建者、提交时间、完成时间以及业务线相关字段。
- 不支持投票字段。
- 在修改或添加子选项（级联选项）时，必须提供`parent_value`。

### 使用场景

- 当需要更改字段名称、别名、帮助描述、默认值、授权角色或选项列表（通过`field_value`和相应的操作类型add/modify/delete来实现）时。
- 当需要更新团队作用域（team_option）以支持级联单选/多选字段时；这些操作与`field_value`互斥。
- 当更新复合字段时：传递父字段键（parent_field_key）仅更改字段名称/别名/帮助描述；传递子字段键（child_field_key）以更新所有属性。

### API规范：update_custom_field

```yaml
name: update_custom_field
type: api
description: >
  Update configuration of the specified custom field. field_key in body identifies
  the field. field_value supports option actions (add/modify/delete); parent_value
  required for sub-options. field_value and team_option are mutually exclusive.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: PUT
  url: https://{domain}/open_api/{project_key}/field/{work_item_type_key}
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
      project_key: Double-click space name in Meegle. simple_name: from space URL (e.g. doc).
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtain via Get work item types in space.

inputs:
  field_key:
    type: string
    required: false
    description: >
      Unique identifier of the field from Get Field Information. For composite
      fields: parent field_key allows only field_name, field_alias, help_description;
      child field_key allows all attributes.
  field_name:
    type: string
    required: false
    description: Field name.
  field_value:
    type: array
    required: false
    description: >
      Option updates. Each item: label, value (option id), action (0 add, 1 modify, 2 delete).
      For sub-options include parent_value. Structure per Attributes and fields.
      Mutually exclusive with team_option.
  free_add:
    type: integer
    required: false
    description: 1 = allow users to add options; 2 = No (default). For select/tree_select etc.
  work_item_relation_uuid:
    type: string
    required: false
    description: Work item relationship ID from Get Field Information. For work_item_related_select / work_item_related_multi_select.
  default_value:
    type: object
    required: false
    description: Default value; structure per field type. Not supported for attachment, signal, multi-value signal.
  field_alias:
    type: string
    required: false
    description: Field alias; cannot duplicate other fields of same work item type.
  help_description:
    type: string
    required: false
    description: Help instructions.
  authorized_roles:
    type: array
    items: string
    required: false
    description: Role or system keys (e.g. _master, _owner, _role). Default "Anyone".
  team_option:
    type: object
    required: false
    description: Team scope per TeamOption. Only for tree_select, tree_multi_select. Mutually exclusive with field_value.

outputs:
  data:
    type: object
    description: Empty on success (no data in response).

constraints:
  - Permission: Permission Management – Configuration
  - field_value and team_option cannot both be sent

error_mapping:
  1000051468: Field alias repeated (replace field_alias)
  1000051750: Field name has been used (replace field_name)
  1000050746: Field type not supported
  1000053603: Field name length exceeded (max 255 characters)
  1000053604: Field description length exceeded (max 255 characters)
  1000053605: Option count exceeded (up to {Number} options)
```

### 使用说明

- **field_key**：用于标识要更新的字段（需通过`Get Field Information`获取）。对于`compound_field`字段，使用父字段键（parent_field_key）仅更改名称/别名/帮助描述；使用子字段键（child_field_key）更新所有属性。
- **field_value**的操作类型：`action` 0 = 添加选项，1 = 修改选项，2 = 删除选项。在添加或修改子选项时需要提供`parent_value`。
- **field_value**与**team_option**的区别：不要同时使用这两个参数。`field_value`用于选项列表的修改；`team_option`用于树形选择框/树形多选字段的团队作用域设置。
- 附件类型字段、外部系统信号字段以及多值外部系统信号字段不支持设置默认值。