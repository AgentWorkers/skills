---
name: meegle-api-work-item-group
description: Meegle OpenAPI：用于工作项组操作的功能。
metadata: { openclaw: {} }
---
# Meegle API — 组（Groups）

用于组织和管理工作项组（work item groups）的相关API。

## 功能范围

- 创建、列出、更新工作项组
- 管理组成员关系及组层级结构
- 提供与组相关的其他接口

---

## 邀请机器人（Bots）加入组（Invite Robots into Groups）

将指定的Feishu机器人添加到与工作项关联的组中。该组必须已经存在，并且已与工作项关联。

### 注意事项

- 在使用此接口之前，**Feishu项目机器人（Feishu Project bot）必须已经加入相应的Feishu组**。
- 该接口**仅支持将机器人添加到与工作项关联的组中**（不能添加到任意组）。

### 使用场景

- 当需要将Feishu/Lark机器人邀请到与工作项关联的组聊天中时
- 当需要为工作项的组自动化发送通知或执行相关工作流程时
- 当工作项有关联的组且机器人需要加入该组时

### API规范：`invite_bots_into_groups`

```yaml
name: invite_bots_into_groups
type: api
description: Add Feishu bot to work item's associated group; bot must already be in Feishu group.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_id}/bot_join_chat" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_id: string }
inputs: { work_item_type_key: string, app_ids: { type: array, required: true } }
outputs: { data: { chat_id: string, failed_members: array, success_members: array } }
constraints: [Permission: Work Item Instance, bot in group, app_ids non-empty]
error_mapping: { 50006: Lark OpenAPI error, 30005: Work item not found, 20021: Chat not belong to work item, 20020: app_ids empty, 20014: Project/work item mismatch }
```

### 使用说明

- **work_item_id**：路径参数；该工作项必须具有关联的组。
- **work_item_type_key**：必须与工作项的类型相匹配。
- **app_ids**：要邀请的机器人的Feishu Open Platform应用ID；不能为空。
- 在调用此API之前，请确保Feishu项目机器人已经加入相应的Feishu组。