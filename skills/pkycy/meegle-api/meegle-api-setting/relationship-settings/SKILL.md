---
name: meegle-api-setting-relationship-settings
description: Meegle OpenAPI for work item relationship settings: list, create, update, delete.
metadata: { openclaw: {} }
---

# Meegle API — 设置（关系设置）

**功能：** 获取工作项之间的关系列表、创建工作项之间的关系、更新工作项之间的关系以及删除工作项之间的关系。

## 获取工作项之间的关系列表

列出工作项之间的关联关系（WorkItemRelation：id、name、relation_type、work_item_type_key/name、relation_details）。权限要求：具有工作项实例的访问权限。

```yaml
name: get_list_of_work_item_relationships
type: api
description: List work item relationships (id, name, relation_type, relation_details).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/work_item/relation" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true } }
outputs: { data: array }
constraints: [Permission: Work Item Instances]
error_mapping: { 1000052062: Project key wrong }
```

**使用说明：** 使用 `id` 可以通过 `work_item_relation_uuid` 在自定义字段中创建/更新/删除相关关系。

---

## 创建工作项之间的关系

用于添加新的工作项之间的关系。返回关系ID（UUID）。参数包括：`project_key`、`work_item_type_key`、`name` 以及 `relation_details`（一个包含 `project_key` 和 `work_item_type_key` 的数组）。权限要求：具有工作项实例的访问权限；或具有空间管理员权限（权限码：10001）。

```yaml
name: create_work_item_relationships
type: api
description: Add relationship; returns relation_id. Inputs project_key, work_item_type_key, name, relation_details.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/work_item/relation/create" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, work_item_type_key: string, name: string, relation_details: array }
outputs: { data: { relation_id: string } }
constraints: [Permission: Work Item Instances, space admin]
error_mapping: { 50006: Name repeated, 10001: Not admin }
```

---

## 更新工作项之间的关系

用于修改指定关系ID的名称和`relation_details`。权限要求：具有工作项实例的访问权限；或具有空间管理员权限。

```yaml
name: update_work_item_relationships
type: api
description: Overwrite relationship; relation_id + project_key, work_item_type_key, name, relation_details.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/work_item/relation/update" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, work_item_type_key: string, name: string, relation_id: string, relation_details: array }
outputs: { data: object }
constraints: [Permission: Work Item Instance, space admin]
error_mapping: { 50006: Name repeated, 10001: Not admin }
```

---

## 删除工作项之间的关系

根据关系ID来删除相关关系。权限要求：具有工作项实例的访问权限。

```yaml
name: delete_work_item_relationships
type: api
description: Delete relationship by project_key and relation_id.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: DELETE, url: "https://{domain}/open_api/work_item/relation/delete" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, relation_id: string }
outputs: { data: null }
constraints: [Permission: Work Item Instance]
error_mapping: { 50006: Already deleted or not exist }
```