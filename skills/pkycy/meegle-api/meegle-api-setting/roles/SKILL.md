---
name: meegle-api-setting-roles
description: Meegle OpenAPI for workflow roles: create, get, update, delete.
metadata: { openclaw: {} }
---

# Meegle API — 角色管理

## 创建工作流角色  
创建一个新的工作流角色。返回角色的ID。参数包括：  
- `role`：角色名称  
- `is_owner`：是否为角色所有者  
- `auto_enter_group`：角色是否自动加入指定组  
- `member_assign_mode`：成员分配方式（1：手动；2：指定成员；3：创建者）  
- `members`：角色成员的用户名（以`user_key`形式）  
- `is_member_multi`：角色是否允许多个成员  
- `role_alias`：角色别名  
- `lock_scope`：角色权限范围  

```yaml
name: create_workflow_role
type: api
description: Add role; returns role ID. member_assign_mode 1|2|3; members when 2.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/flow_roles/{work_item_type_key}/create_role" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, work_item_type_key: { type: string, required: true } }
inputs: { role: object }
outputs: { data: string }
constraints: [Permission: Configuration]
error_mapping: { 20006: Role id already exists }
```  

---

## 获取角色详细信息  
查询指定工作流类型下的所有角色信息。返回的角色信息包括：  
- `id`：角色ID  
- `name`：角色名称  
- `is_owner`：是否为角色所有者  
- `member_assign_mode`：成员分配方式  
- `members`：角色成员列表  
- `deletable`：角色是否可删除  
- 其他相关属性...  
权限：`Process Roles`  

```yaml
name: get_detailed_role_settings
type: api
description: All roles and personnel for work item type.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/flow_roles/{work_item_type_key}" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, work_item_type_key: { type: string, required: true } }
outputs: { data: array }
constraints: [Permission: Process Roles]
error_mapping: { 1000052062: Project key wrong }
```  

---

## 更新工作流角色设置  
修改角色的配置信息。需要提供`role_id`或`role_alias`作为参数。当`member_assign_mode`设置为2（指定成员）时，必须提供有效的成员列表。  
权限：`Process Roles`  

```yaml
name: update_workflow_role_settings
type: api
description: Update role by role_id or role_alias; role object with updated config.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/flow_roles/{work_item_type_key}/update_role" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, work_item_type_key: { type: string, required: true } }
inputs: { role_id: string, role_alias: string, role: object }
outputs: { data: object }
constraints: [Permission: Process Roles, one of role_id/role_alias, members non-empty when mode 2]
error_mapping: { 20006: members empty when mode 2, or role_id not exist }
```  

---

## 删除工作流角色配置  
删除指定的工作流角色。需要提供`role_id`或`role_alias`作为参数。注意：被删除的角色不能在模板节点中被使用（错误代码：20093）。  
权限：`Configuration`  

```yaml
name: delete_workflow_role_configuration
type: api
description: Delete role by role_id or role_alias; role not in template nodes.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/flow_roles/{work_item_type_key}/delete_role" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, work_item_type_key: { type: string, required: true } }
inputs: { role_id: string, role_alias: string }
outputs: { data: object }
constraints: [Permission: Configuration, one of role_id/role_alias]
error_mapping: { 20093: Role in use, 20006: role_id not exist }
```