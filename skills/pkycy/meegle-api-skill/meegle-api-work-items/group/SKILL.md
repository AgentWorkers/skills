---
name: meegle-api-work-item-group
description: Meegle OpenAPI：用于工作项组操作的功能。
metadata:
  openclaw: {}
---
# Meegle API — 组（Groups）

用于组织和管理工作项组（work item groups）的相关 API。

## 功能范围

- 创建、列出、更新工作项组
- 管理组成员关系及组层级结构
- 提供与组相关的其他接口

---

## 邀请机器人（Bots）加入组

将指定的 Feishu 机器人添加到与工作项关联的组中。该组必须已经存在，并且必须已与工作项关联。

### 注意事项

- 在使用此接口之前，**Feishu 项目机器人（Feishu Project bot）必须已经加入相应的 Feishu 组**。
- 该接口**仅支持将机器人添加到与工作项关联的组中**（不能添加到任意组）。

### 使用场景

- 当需要将 Feishu/Lark 机器人邀请到与工作项关联的组聊天中时
- 当需要为工作项的组自动发送通知或执行相关工作流程时
- 当工作项有关联的组且机器人需要加入该组时

### API 规范：`invite_bots_into_groups`

```yaml
name: invite_bots_into_groups
type: api
description: >
  Add the specified Feishu robot to the group associated with the work item.
  The Feishu Project bot must already be in the corresponding Feishu group.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_id}/bot_join_chat
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
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, click ··· in the upper right, then ID to copy.

inputs:
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type. Obtainable via "Get work item types in the space".
      Must match the work item instance identified by work_item_id.
  app_ids:
    type: array
    items: string
    required: true
    description: >
      App ID(s) of the Feishu Open Platform application (bot).
      For acquisition, refer to Feishu Documentation.

outputs:
  data:
    type: object
    properties:
      chat_id: string
      failed_members: array
      success_members: array
    description: |
      chat_id: Associated group chat ID.
      failed_members: List of app_id that failed to join.
      success_members: List of app_id that successfully joined the chat.

constraints:
  - Permission: Permission Management – Work Item Instance
  - Feishu Project bot must already be in the Feishu group
  - Only adds bot to the group associated with the work item
  - app_ids cannot be empty

error_mapping:
  50006: Lark OpenAPI error (e.g. robot not in group; operator cannot be out of chat; bot invisible to user; no permission to invite; work item ID changed)
  30005: Work item not found
  20021: Chat ID not belong to work item (group not bound to this work item)
  20020: Bot app_ids empty
  20014: Project and work item not match (work item does not belong to this space)
```

### 使用说明

- **work_item_id**：路径参数；该工作项必须有一个关联的组。
- **work_item_type_key**：必须与工作项的类型相匹配。
- **app_ids**：要邀请的机器人的 Feishu Open Platform 应用程序 ID；不能为空。
- 在调用此 API 之前，请确保 Feishu 项目机器人已经加入相应的 Feishu 组。