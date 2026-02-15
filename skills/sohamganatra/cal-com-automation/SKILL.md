---
name: cal-com-automation
description: "通过 Rube MCP (Composio) 自动化 Cal.com 的各项任务：管理预订、检查可用性、配置 Webhook 以及处理团队相关操作。在使用任何工具之前，请务必先查找其当前的接口规范（schemas）。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 Cal.com 操作

通过 Composio 的 Cal 工具包和 Rube MCP 自动化 Cal.com 的调度操作。

## 先决条件

- Rube MCP 必须已连接（可使用 `RUBE_SEARCH_TOOLS`）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `cal` 工具包建立与 Cal.com 的活动连接
- 在运行任何工作流之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 使用 `cal` 工具包调用 `RUBE_MANAGE_CONNECTIONS`。
3. 如果连接状态不是 `ACTIVE`，请按照返回的链接完成 Cal.com 的身份验证。
4. 在运行任何工作流之前，确保连接状态显示为 `ACTIVE`。

## 核心工作流

### 1. 管理预订

**使用场景**：用户需要列出、创建或查看预订信息。

**工具序列**：
1. `CAL-fetch_ALL_BOOKINGS` - 列出所有预订信息（必选）
2. `CAL_POST_NEW_BOOKING_REQUEST` - 创建新的预订（可选）

**列出预订的关键参数**：
- `status`：按预订状态过滤（'upcoming'、'recurring'、'past'、'cancelled'、'unconfirmed'）
- `afterStart`：在此日期之后的预订（ISO 8601 格式）
- `beforeEnd`：在此日期之前的预订（ISO 8601 格式）

**创建预订的关键参数**：
- `eventTypeId`：预订的事件类型 ID
- `start`：预订开始时间（ISO 8601 格式）
- `end`：预订结束时间（ISO 8601 格式）
- `name`：参与者姓名
- `email`：参与者邮箱
- `timeZone`：参与者时区（IANA 格式）
- `language`：参与者语言代码
- `metadata`：额外的元数据对象

**注意事项**：
- 日期过滤器使用包含时区的 ISO 8601 格式（例如：'2024-01-15T09:00:00Z'）
- `eventTypeId` 必须引用一个有效且处于活动状态的事件类型
- 创建预订时需要确保有可用的时间段；请先检查可用性
- 时区必须是有效的 IANA 时区字符串（例如：'America/New_York'）
- 状态过滤器的值必须是特定的字符串；无效的值将返回空结果

### 2. 检查可用性

**使用场景**：用户需要查找空闲时间或可用的预订时间段。

**工具序列**：
1. `CAL_RETRIEVE_CALENDARBusy_times` - 获取繁忙时间段（必选）
2. `CAL_GET_AVAILABLE_SLOTS_INFO` - 获取特定的可用时间段（必选）

**关键参数**：
- `dateFrom`：可用性检查的开始日期（YYYY-MM-DD 格式）
- `dateTo`：可用性检查的结束日期（YYYY-MM-DD 格式）
- `eventTypeId`：要检查时间段的事件类型
- `timeZone`：可用性响应的时区
- `loggedInUsersTz`：请求用户的时区

**注意事项**：
- 繁忙时间段显示的是用户不可用的时间
- 可用的时间段取决于事件类型的持续时间和配置
- 日期范围应合理（不要提前数月），以获得准确的结果
- 时区会影响时间段的显示方式；请务必明确指定时区
- 可用性信息受日历集成（如 Google 日历、Outlook 等）的影响

### 3. 配置 Webhook

**使用场景**：用户需要设置或管理预订事件的 Webhook 通知。

**工具序列**：
1. `CAL_RETRIEVE_WEBHOOKS_LIST` - 列出现有的 Webhook（必选）
2. `CAL_GET_WEBHOOK_BY_ID` - 获取特定的 Webhook 详细信息（可选）
3. `CAL_UPDATE_WEBHOOK_BY_ID` - 更新 Webhook 配置（可选）
4. `CAL_DELETE_WEBHOOK_BY_ID` - 删除 Webhook（可选）

**关键参数**：
- `id`：用于 GET/UPDATE/DELETE 操作的 Webhook ID
- `subscriberUrl`：Webhook 端点 URL
- `eventTriggers`：触发 Webhook 的事件类型数组
- `active`：Webhook 是否处于活动状态
- `secret`：Webhook 签名密钥

**注意事项**：
- Webhook URL 必须是公开可访问的 HTTPS 端点
- 可触发的事件类型包括：'BOOKING_CREATED'、'BOOKING_RESCHEDULED'、'BOOKING_CANCELLED' 等
- 不活动的 Webhook 不会触发；通过切换 `active` 来启用或禁用它们
- Webhook 密钥用于验证请求负载

### 4. 管理团队

**使用场景**：用户需要创建、查看或管理团队及团队事件类型。

**工具序列**：
1. `CAL_GET_TEAMS_LIST` - 列出所有团队（必选）
2. `CAL_GET_TEAM_INFORMATION_BY_TEAM_ID` - 获取特定团队的详细信息（可选）
3. `CAL_CREATE_TEAM_IN_ORGANIZATION` - 创建新的团队（可选）
4. `CAL_RETRIEVE_TEAM_EVENT_TYPES` - 列出团队的事件类型（可选）

**关键参数**：
- `teamId`：团队标识符
- `name`：团队名称（用于创建）
- `slug`：适合 URL 的团队标识符

**注意事项**：
- 创建团队可能需要组织级别的权限
- 团队事件类型与个人事件类型是分开的
- 团队标识符（slug）必须是 URL 安全的，并且在组织内必须是唯一的

### 5. 组织管理

**使用场景**：用户需要查看组织详细信息。

**工具序列**：
1. `CAL_GET_ORGANIZATION_ID` - 获取组织 ID（必选）

**关键参数**：（无）

**注意事项**：
- 组织 ID 用于创建团队和组织级别的操作
- 并非所有 Cal.com 账户都有组织；个人计划可能会返回错误

## 常见模式

### 预订创建流程

```
1. Call CAL_GET_AVAILABLE_SLOTS_INFO to find open slots
2. Present available times to the user
3. Call CAL_POST_NEW_BOOKING_REQUEST with selected slot
4. Confirm booking creation response
```

### ID 解析

**团队名称 -> 团队 ID**：
```
1. Call CAL_GET_TEAMS_LIST
2. Find team by name in response
3. Extract id field
```

### Webhook 设置

```
1. Call CAL_RETRIEVE_WEBHOOKS_LIST to check existing hooks
2. Create or update webhook with desired triggers
3. Verify webhook fires on test booking
```

## 常见问题

**日期/时间格式**：
- 预订时间：使用包含时区的 ISO 8601 格式（例如：'2024-01-15T09:00:00Z'）
- 可用性日期：使用 YYYY-MM-DD 格式
- 请始终明确指定时区以避免混淆

**事件类型**：
- 事件类型 ID 是数字整数
- 事件类型定义了持续时间、地点和预订规则
- 被禁用的事件类型无法接受新的预订

**权限**：
- 团队操作需要团队成员资格或管理员权限
- 组织操作需要组织级别的权限
- Webhook 管理需要适当的访问权限

**速率限制**：
- Cal.com API 对每个 API 密钥都有速率限制
- 在收到 429 错误响应时，请实施重试机制

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 列出预订 | CAL_FETCH_ALL_BOOKINGS | status, afterStart, beforeEnd |
| 创建预订 | CAL_POST_NEW_BOOKING_REQUEST | eventTypeId, start, end, name, email |
| 获取繁忙时间段 | CAL_RETRIEVE_CALENDARBusy_times | dateFrom, dateTo |
| 获取可用时间段 | CAL_GET_AVAILABLE_SLOTS_INFO | eventTypeId, dateFrom, dateTo |
| 列出 Webhook | CAL_RETRIEVE_WEBHOOKS_LIST | （无） |
| 获取 Webhook | CAL_GET_WEBHOOK_BY_ID | id |
| 更新 Webhook | CAL_UPDATE_WEBHOOK_BY_ID | id, subscriberUrl, eventTriggers |
| 删除 Webhook | CAL_DELETE_WEBHOOK_BY_ID | id |
| 列出团队 | CAL_GET_TEAMS_LIST | （无） |
| 获取团队信息 | CAL_GET_TEAM_INFORMATION_BY_TEAM_ID | teamId |
| 创建团队 | CAL_CREATE_TEAM_IN_ORGANIZATION | name, slug |
| 团队事件类型 | CAL_RETRIEVE_TEAM_EVENT_TYPES | teamId |
| 获取组织 ID | CAL_GET_ORGANIZATION_ID | （无） |