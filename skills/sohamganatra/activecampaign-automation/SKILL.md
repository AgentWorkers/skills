---
name: activecampaign-automation
description: "通过 Rube MCP (Composio) 自动化 ActiveCampaign 任务：管理联系人、标签、列表订阅、自动化注册以及相关任务。在使用任何工具之前，请务必先查询其当前的架构（schema）信息。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 ActiveCampaign 操作

通过 Composio 的 ActiveCampaign 工具包和 Rube MCP 来自动化 ActiveCampaign 客户关系管理（CRM）及营销自动化流程。

## 先决条件

- Rube MCP 必须已连接（支持使用 `RUBE_SEARCH_TOOLS`）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `active_campaign` 工具包连接到 ActiveCampaign
- 在执行任何操作前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息

## 设置

**添加 Rube MCP**: 在您的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需提供该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否能正常响应来验证 Rube MCP 是否可用。
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并使用 `active_campaign` 工具包进行连接设置。
3. 如果连接状态不是 `ACTIVE`，请按照返回的链接完成 ActiveCampaign 的身份验证。
4. 在运行任何工作流之前，请确保连接状态显示为 `ACTIVE`。

## 核心工作流

### 1. 创建和查找联系人

**使用场景**：用户需要创建新联系人或查找现有联系人。

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 查找现有联系人 [可选]
2. `ACTIVE_CAMPAIGN_CREATE_CONTACT` - 创建新联系人 [必填]

**查找联系人时的关键参数**：
- `email`：按电子邮件地址搜索
- `id`：按 ActiveCampaign 联系人 ID 搜索
- `phone`：按电话号码搜索

**创建联系人时的关键参数**：
- `email`：联系人的电子邮件地址（必填）
- `first_name`：联系人的名字
- `last_name`：联系人的姓氏
- `phone`：联系人的电话号码
- `organization_name`：联系人的所属组织
- `job_title`：联系人的职位
- `tags`：用逗号分隔的标签列表

**注意事项**：
- `email` 是创建联系人时唯一的必填字段。
- 电话号码的搜索使用通用搜索参数，可能会返回部分匹配的结果。
- 在 `FIND_CONTACT` 中同时使用 `email` 和 `phone` 时，搜索结果会在客户端进行过滤。
- 创建联系人时提供的标签会立即生效。
- 使用已存在的电子邮件地址创建联系人可能会更新该联系人信息。

### 2. 管理联系人标签

**使用场景**：用户需要为联系人添加或删除标签。

**工具序列**：
1. `ACTIVE_CAMPAIGN_FINDCONTACT` - 通过电子邮件或 ID 查找联系人 [前提条件]
2. `ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG` - 添加或删除标签 [必填]

**关键参数**：
- `action`：'Add' 或 'Remove'（必填）
- `tags`：标签名称，以逗号分隔的字符串或字符串数组形式
- `contact_id`：联系人 ID（提供此参数或 `contact_email`）
- `contact_email`：联系人的电子邮件地址（作为 `contact_id` 的替代选项）

**注意事项**：
- `action` 的值必须大写：'Add' 或 'Remove'（不能使用小写）。
- 标签可以是逗号分隔的字符串（如 'tag1, tag2'）或数组（如 ['tag1', 'tag2']）。
- 必须提供 `contact_id` 或 `contact_email`；`contact_id` 具有优先级。
- 添加不存在的标签会自动创建该标签。
- 删除不存在的标签不会产生任何错误。

### 3. 管理联系人订阅列表

**使用场景**：用户需要为联系人订阅或取消订阅列表。

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 查找联系人 [前提条件]
2. `ACTIVE_CAMPAIGN_MANAGE_LIST_SUBSCRIPTION` - 订阅或取消订阅 [必填]

**关键参数**：
- `action`：'subscribe' 或 'unsubscribe'（必填）
- `list_id`：列表 ID（数字字符串）
- `email`：联系人的电子邮件地址（提供此参数或 `contact_id`）
- `contact_id`：联系人的 ID（数字字符串，作为 `email` 的替代选项）

**注意事项**：
- `action` 的值必须小写：'subscribe' 或 'unsubscribe'。
- `list_id` 是数字字符串（例如 '2'），而不是列表名称。
- 列表 ID 可以通过 `/api/3/lists` 端点获取（Composio 工具不支持直接访问）；请使用 ActiveCampaign 的 UI 来获取。
- 如果同时提供了 `email` 和 `contact_id`，则以 `contact_id` 为准。
- 取消订阅后，状态会变为 '2'（已取消订阅），但关联记录仍然存在。

### 4. 将联系人添加到自动化流程中

**使用场景**：用户需要将联系人加入自动化流程。

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 确认联系人存在 [前提条件]
2. `ACTIVE_CAMPAIGN_ADD_CONTACT_TO_AUTOMATION` - 将联系人加入自动化流程 [必填]

**关键参数**：
- `contact_email`：要加入自动化流程的联系人电子邮件地址
- `automation_id`：目标自动化流程的 ID

**注意事项**：
- 联系人必须已在 ActiveCampaign 中存在。
- 自动化流程只能通过 ActiveCampaign 的 UI 创建，无法通过 API 创建。
- `automation_id` 必须引用一个现有的、处于活动状态的自动化流程。
- 该工具会执行两步操作：首先通过电子邮件查找联系人，然后将其加入自动化流程。
- 可以通过 ActiveCampaign 的 UI 或 `/api/3/automations` 端点获取自动化流程的 ID。

### 5. 创建联系人任务

**使用场景**：用户需要为联系人创建跟进任务。

**工具序列**：
1. `ACTIVE_CAMPAIGN_FIND_CONTACT` - 查找要关联任务的联系人 [前提条件]
2. `ACTIVE_CAMPAIGN_CREATE_CONTACT_TASK` - 创建任务 [必填]

**关键参数**：
- `relid`：要与任务关联的联系人 ID
- `duedate`：任务的截止日期（ISO 8601 格式，包含时区，例如 '2025-01-15T14:30:00-05:00'）
- `dealTasktype`：任务类型 ID（根据 ActiveCampaign 中配置的类型选择）
- `title`：任务标题
- `note`：任务描述/内容
- `assignee`：任务分配给的用户 ID
- `edate`：任务的结束日期（ISO 8601 格式，必须晚于 `duedate`）
- `status`：0 表示未完成，1 表示已完成

**注意事项**：
- `duedate` 必须是有效的 ISO 8601 日期时间格式，并包含时区偏移量；不要使用占位符值。
- `edate` 必须晚于 `duedate`。
- `dealTasktype` 是一个字符串 ID，用于引用 ActiveCampaign 中配置的任务类型。
- `relid` 是联系人的 ID（数字形式），而不是电子邮件地址。
- `assignee` 是用户 ID；请通过 ActiveCampaign 的 UI 将用户名转换为对应的用户 ID。

## 常见操作模式

### 联系人查找流程

```
1. Call ACTIVE_CAMPAIGN_FIND_CONTACT with email
2. If found, extract contact ID for subsequent operations
3. If not found, create contact with ACTIVE_CAMPAIGN_CREATE_CONTACT
4. Use contact ID for tags, subscriptions, or automations
```

### 批量添加联系人标签

```
1. For each contact, call ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG
2. Use contact_email to avoid separate lookup calls
3. Batch with reasonable delays to respect rate limits
```

### ID 解析

**将联系人电子邮件转换为联系人 ID**：
```
1. Call ACTIVE_CAMPAIGN_FIND_CONTACT with email
2. Extract id from the response
```

## 常见问题

- **操作名称的大小写**：
  - 标签操作（如 'Add', 'Remove'）必须大写。
  - 订阅操作（如 'subscribe', 'unsubscribe'）必须小写。
  - 混淆大小写会导致错误。

- **ID 类型**：
  - 联系人 ID：数字字符串（例如 '123'）
  - 列表 ID：数字字符串
  - 自动化流程 ID：数字字符串
  - 所有 ID 都应以字符串形式传递，不能使用整数。

- **自动化流程**：
  - 无法通过 API 创建自动化流程；只能通过 ActiveCampaign 的 UI 进行操作。
  - 自动化流程必须处于活动状态才能接收新联系人。
  - 将已存在于自动化流程中的联系人重新加入可能不会产生任何效果。

- **速率限制**：
  - ActiveCampaign API 对每个账户有速率限制。
  - 遇到 429 错误时，请实施重试策略。
  - 批量操作应适当间隔进行。

- **响应解析**：
  - 响应数据可能包含在 `data` 或 `data.data` 下。
  - 使用防御性解析方法来处理响应数据。
  - 联系人搜索可能会返回多个结果；为确保准确性，请根据电子邮件地址进行匹配。

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 查找联系人 | ACTIVE_CAMPAIGN_FIND_CONTACT | email, id, phone |
| 创建联系人 | ACTIVE_CAMPAIGN_CREATE_CONTACT | email, first_name, last_name, tags |
| 添加/删除标签 | ACTIVE_CAMPAIGN_MANAGE_CONTACT_TAG | action, tags, contact_email |
| 订阅/取消订阅 | ACTIVE_CAMPAIGN_MANAGE_LIST_SUBSCRIPTION | action, list_id, email |
| 添加到自动化流程 | ACTIVE_CAMPAIGN_ADD_CONTACT_TO_AUTOMATION | contact_email, automation_id |
| 创建任务 | ACTIVE_CAMPAIGN_CREATE_CONTACT_TASK | relid, duedate, dealTasktype, title |