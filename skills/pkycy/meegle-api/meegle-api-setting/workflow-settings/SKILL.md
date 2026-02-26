---
name: meegle-api-setting-workflow-settings
description: Meegle OpenAPI for workflow/process template settings: list, get detail, create, update, delete.
metadata: { openclaw: {} }
---

# Meegle API — 工作流设置（Workflow Settings）

- 获取工作流模板（Get Workflow Templates）
- 获取工作流模板的详细信息（Get Detailed Settings of Workflow Templates）
- 创建工作流模板（Create Workflow Templates）
- 更新工作流模板（Update Workflow Templates）
- 删除工作流模板（Delete Workflow Templates）

## 获取工作流模板（Get Workflow Templates）

列出属于特定工作项类型的所有工作流模板：`templateConf`（版本、唯一键、是否禁用、模板ID、模板名称）。权限：配置管理（Configuration）。

```yaml
name: get_workflow_templates
type: api
description: List process templates for work item type.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/template_list/{work_item_type_key}" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, work_item_type_key: { type: string, required: true } }
outputs: { data: array }
constraints: [Permission: Configuration]
```

---

## 获取工作流模板的详细信息（Get Detailed Settings of Workflow Templates）

工作流模板详情：包括节点配置（`workflow_confs`）和连接信息（`connections`）。不支持节点事件配置。权限：流程类型管理（Process Type）。

```yaml
name: get_detailed_settings_of_workflow_templates
type: api
description: Template detail (workflow_confs, connections); node event not supported.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/template_detail/{template_id}" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, template_id: { type: string, required: true } }
outputs: { data: object }
constraints: [Permission: Process Type]
error_mapping: { 50006: Template not found, 30001: Data not found }
```

---

## 创建工作流模板（Create Workflow Templates）

创建新的工作流模板；可选参数：`copy_template_id`（用于复制现有模板）。返回创建的模板ID。权限：配置管理；空间管理员（权限等级：10005）。

```yaml
name: create_workflow_templates
type: api
description: Create template; optional copy_template_id; returns template ID.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/template/v2/create_template" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, work_item_type_key: string, template_name: string, copy_template_id: integer }
outputs: { data: integer }
constraints: [Permission: Configuration, space admin]
error_mapping: { 10005: No project admin, 50006: Template name duplicate }
```

---

## 更新工作流模板（Update Workflow Templates）

更新工作流模板的内容：包括节点流程配置（`workflow_confs`）和状态信息（`state_flow_confs`）。权限：设置管理；空间管理员。

```yaml
name: update_workflow_template
type: api
description: Update template; workflow_confs (action 1/2/3), state_flow_confs.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: PUT, url: "https://{domain}/open_api/template/v2/update_template" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, template_id: integer, workflow_confs: array, state_flow_confs: array }
outputs: { data: object }
constraints: [Permission: Settings, space admin]
error_mapping: { 10005: No project admin, 50006: Template not found }
```

---

## 删除工作流模板（Delete Workflow Templates）

根据项目键（`project_key`）和模板ID（`template_id`）删除工作流模板。权限：设置管理。

```yaml
name: delete_workflow_templates
type: api
description: Delete template; path project_key, template_id.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: DELETE, url: "https://{domain}/open_api/template/v2/delete_template/{project_key}/{template_id}" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: { type: string, required: true }, template_id: { type: string, required: true } }
outputs: { data: object }
constraints: [Permission: Settings]
error_mapping: { 9999: template_id invalid }
```