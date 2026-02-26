---
name: meegle-api-setting-field-settings
description: Meegle OpenAPI for field settings: get, create, update custom fields.
metadata: { openclaw: {} }
---

# Meegle API — 设置（字段设置）

用于获取字段信息、创建自定义字段以及更新自定义字段。

## 获取字段信息

所有以“space”开头或属于工作项类型的字段（例如：SimpleField、field_key、field_type_key、options、compound_fields）。权限级别：Configuration。

```yaml
name: get_field_information
type: api
description: All fields in space or under work item type (field_key, field_type_key, options, compound_fields).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/field/all" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true } }
inputs: { work_item_type_key: { type: string, required: false } }
outputs: { data: array }
constraints: [Permission: Configuration]
error_mapping: { 30001: Data not found }
```

**使用说明：**  
- 对于所有以“space”开头的字段，可以省略`work_item_type_key`；对于特定类型的工作项字段，则需要设置`work_item_type_key`（例如：`schedule_field_key`等）。  
- `field_key`是在工作项类型设置中指定的字段名称。

---

## 创建自定义字段

在工作项类型下创建自定义字段。返回字段的`field_key`。`field_value`与`team_option`是互斥的（即不能同时设置）。权限级别：Work Item Instances。

```yaml
name: create_custom_field
type: api
description: Create custom field; returns field_key. field_value vs team_option (tree_select) mutually exclusive.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/field/{work_item_type_key}/create" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, work_item_type_key: { type: string, required: true } }
inputs: { field_name: string, field_alias: string, field_type_key: string, value_type: integer, field_value: object, reference_work_item_type_key: string, reference_field_key: string, is_multi: boolean, format: boolean, free_add: integer, work_item_relation_uuid: string, default_value: object, help_description: string, authorized_roles: array, team_option: object }
outputs: { data: string }
constraints: [Permission: Work Item Instances, field_value and team_option not both]
error_mapping: { 1000051468: Field alias repeated, 1000051750: Field name used, 1000053603: Field name length }
```

**使用说明：**  
- `field_type_key`的示例值包括：`text`、`select`、`date`、`user`、`number`、`link`等。  
- 如果需要引用其他工作项，可以使用`value_type`（例如：`1`），并指定要引用的工作项的`reference_work_item_type_key`和`reference_field_key`。  
- `work_item_relation_uuid`可以通过调用`Get Field Information`函数获取，用于关联相关的工作项。

---

## 更新自定义字段

根据`field_key`更新自定义字段的值（支持添加、修改或删除操作）。对于子选项，还可以设置`parent_value`。`field_value`与`team_option`是互斥的。权限级别：Configuration。

```yaml
name: update_custom_field
type: api
description: Update field by field_key; field_value actions add/modify/delete; parent_value for sub-options.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: PUT, url: "https://{domain}/open_api/{project_key}/field/{work_item_type_key}" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, work_item_type_key: { type: string, required: true } }
inputs: { field_key: string, field_name: string, field_value: array, free_add: integer, work_item_relation_uuid: string, default_value: object, field_alias: string, help_description: string, authorized_roles: array, team_option: object }
outputs: { data: object }
constraints: [Permission: Configuration, field_value and team_option not both]
error_mapping: { 1000051468: Alias repeated, 1000051750: Name used, 1000050746: Field type not supported }
```

**使用说明：**  
- 使用`Get Field Information`函数获取所需的`field_key`。  
- 对于复合字段（compound_fields）：`parent_field_key`仅用于设置字段的名称/别名/帮助信息；`child_field_key`则用于设置所有子字段的属性。