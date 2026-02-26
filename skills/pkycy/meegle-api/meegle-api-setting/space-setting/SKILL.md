---
name: meegle-api-setting-space-setting
description: Meegle OpenAPI for space-level setting: work item types, business lines.
metadata: { openclaw: {} }
---

# Meegle API — 设置（空间设置）

**获取空间中的工作项类型**  
**获取空间中的业务线详情**

## 获取空间中的工作项类型  
返回所有工作项类型以及用于其他 API 的 **work_item_type_key** 和 **api_name**。权限：Configuration Categories。  

### API 规范：get_work_item_types_in_space  
```yaml
name: get_work_item_types_in_space
type: api
description: All work item types in space (type_key, name, api_name, is_disable, enable_model_resource_lib).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/work_item/all-types" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true } }
outputs: { data: array }
constraints: [Permission: Configuration Categories]
error_mapping: { 10023: User not exist (X-User-Key invalid) }
```  
**用法：** type_key/api_name → 在其他 API 中使用的工作项类型键。X-User-Key 必须有效（否则使用 10023）。  

---

## 获取空间中的业务线详情  
返回业务线树信息（id、名称、role_owners、watchers、level_id、parent、children）。权限：Configuration。  

### API 规范：get_business_line_details_in_space  
```yaml
name: get_business_line_details_in_space
type: api
description: Business line tree; each node has id, name, role_owners, watchers, level_id, parent, children.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/business/all" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true } }
outputs: { data: array }
constraints: [Permission: Configuration]
error_mapping: { 1000052062: Project key wrong }
```