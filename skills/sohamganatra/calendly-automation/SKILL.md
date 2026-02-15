---
name: calendly-automation
description: 通过 Rube MCP (Composio) 自动化 Calendly 的日程安排、事件管理、受邀者跟踪、可用性检查以及组织管理工作。在使用任何工具之前，请务必先查询其当前的架构和功能规范（schemas）。
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 Calendly 操作

通过 Composio 的 Calendly 工具包，可以自动化执行 Calendly 的各种操作，包括事件列表、受邀者管理、日程链接创建、可用时间查询以及组织管理。

## 先决条件

- 必须已连接 Rube MCP（支持 `RUBE_SEARCH_TOOLS` 功能）。
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `calendly` 工具包建立有效的 Calendly 连接。
- 在执行任何操作之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息。
- 许多操作需要用户的 Calendly URI，该 URI 可通过 `CALENDLY_GET_CURRENT_USER` 获取。

## 设置

**添加 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥，只需添加该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 使用 `calendly` 工具包调用 `RUBE_MANAGE_CONNECTIONS`。
3. 如果连接状态不是 `ACTIVE`，请按照返回的授权链接完成 Calendly 的 OAuth 认证。
4. 在运行任何工作流程之前，确保连接状态显示为 `ACTIVE`。

## 核心工作流程

### 1. 列出并查看已安排的事件

**使用场景**：用户希望查看即将发生的、过去的或筛选后的 Calendly 事件。

**工具序列**：
1. `CALENDLY_GET_CURRENT_USER` - 获取经过身份验证的用户 URI 和组织 URI [必备条件]
2. `CALENDLY_LIST_events` - 按用户、组织或组范围列出事件 [必需]
3. `CALENDLY_GET_EVENT` - 根据 UUID 获取特定事件的详细信息 [可选]

**关键参数**：
- `user`：完整的 Calendly API URI（例如：`https://api.calendly.com/users/{uuid}`），不能使用 `"me"`
- `organization`：用于组织范围查询的完整组织 URI
- `status`：`"active"` 或 `"canceled"`
- `min_start_time` / `max_start_time`：UTC 时间戳（例如：`2024-01-01T00:00:00.000000Z`
- `invitee_email`：按受邀者电子邮件过滤事件（仅用于过滤，而非指定范围）
- `sort`：`"start_time:asc"` 或 `"start_time:desc"`
- `count`：每页显示的结果数量（默认为 20）
- `page_token`：上一次请求的分页令牌

**注意事项**：
- 必须提供 `user`、`organization` 或 `group` 中的一个；省略或同时提供多个范围会导致错误。
- `user` 参数需要完整的 API URI，不能使用 `"me"`，请先使用 `CALENDLY_GET_CURRENT_USER`。
- `invitee_email` 用于过滤，而非指定范围；仍需要提供用户、组织或组中的一个范围。
- 分页使用 `count` 和 `page_token`；循环调用直到 `page_token` 不存在为止以获取所有结果。
- 对于组织或组范围的查询，可能需要管理员权限。

### 2. 管理事件受邀者

**使用场景**：用户希望查看被邀请参加事件的人员或获取受邀者的详细信息。

**工具序列**：
1. `CALENDLY_LIST_events` - 查找目标事件 [必备条件]
2. `CALENDLY_LIST_EVENT_INVITEES` - 列出特定事件的所有受邀者 [必需]
3. `CALENDLY_GET_EVENT_INVITEE` - 获取单个受邀者的详细信息 [可选]

**关键参数**：
- `uuid`：事件 UUID（用于 `LIST_EVENT_INVITEES`）
- `event_uuid` + `invitee_uuid`：两者都用于 `GET_EVENT_INVITEE`
- `email`：按电子邮件地址过滤受邀者
- `status`：`"active"` 或 `"canceled"`
- `sort`：`"created_at:asc"` 或 `"created_at:desc"`
- `count`：每页显示的结果数量（默认为 20）

**注意事项**：
- `CALENDLY_LIST_EVENT_INVITEES` 中的 `uuid` 是事件 UUID，而非受邀者的 UUID。
- 使用 `page_token` 分页以获取所有受邀者的列表。
- 默认情况下，已取消的受邀者会被排除在外；如需查看已取消的受邀者，请使用 `status: "canceled"`。

### 3. 创建日程链接并检查可用时间

**使用场景**：用户希望生成预订链接或检查可用时间段。

**工具序列**：
1. `CALENDLY_GET_CURRENT_USER` - 获取用户 URI [必备条件]
2. `CALENDLY_LIST_USER_S_EVENT_TYPES` - 列出可用的事件类型 [必需]
3. `CALENDLY_LIST_EVENT_TYPE_AVAILABLE_times` - 检查特定事件类型的可用时间段 [可选]
4. `CALENDLY_CREATE_SCHEDULING_LINK` - 生成一次性使用的日程链接 [必需]
5. `CALENDLY_LIST_USER_AVAILABILITY_SCHEDULES` - 查看用户的可用日程安排 [可选]

**关键参数**：
- `owner`：事件类型 URI（例如：`https://api.calendly.com/event_types/{uuid}`）
- `owner_type`：`"EventType"`（默认值）
- `max_event_count`：对于一次性链接，必须设置为 `1`
- `start_time` / `end_time`：用于查询可用时间的 UTC 时间戳（最多 7 天的范围）
- `active`：布尔值，用于筛选活动/非活动的事件类型
- `user`：用于事件类型列表的用户 URI

**注意事项**：
- 如果令牌权限不足或所有者 URI 无效，`CALENDLY_CREATE_SCHEDULING_LINK` 可能返回 403 错误。
- `CALENDLY_LIST_EVENT_TYPE_AVAILABLE_times` 需要 UTC 时间戳和最多 7 天的范围；较长的查询需要分多次调用。
- 可用时间的结果不会分页显示——所有结果会一次性返回。

### 4. 取消事件

**使用场景**：用户希望取消已安排的 Calendly 事件。

**工具序列**：
1. `CALENDLY_LIST_events` - 查找要取消的事件 [必备条件]
2. `CALENDLY_GET_EVENT` - 在取消前确认事件详情 [必备条件]
3. `CALENDLY_LIST_EVENT_INVITEES` - 查看受影响的受邀者 [可选]
4. `CALENDLY_CANCEL_EVENT` - 取消事件 [必需]

**关键参数**：
- `uuid`：要取消的事件 UUID
- `reason`：可选的取消原因（可能会包含在通知中）

**注意事项**：
- 取消操作是不可逆的——在执行前务必确认用户的意愿。
- 取消操作可能会触发对受邀者的通知。
- 只能取消活动中的事件；已取消的事件会返回错误。
- 在执行 `CALENDLY_CANCEL_EVENT` 之前，必须获得用户的明确确认。

### 5. 管理组织和邀请

**使用场景**：用户希望邀请成员、管理组织或处理组织邀请。

**工具序列**：
1. `CALENDLY_GET_CURRENT_USER` - 获取用户和组织信息 [必备条件]
2. `CALENDLY_GET_ORGANIZATION` - 获取组织详情 [可选]
3. `CALENDLY_LIST_ORGANIZATION_INVITATIONS` - 查看现有的邀请 [可选]
4. `CALENDLY_CREATE_ORGANIZATION_INVITATION` - 发送组织邀请 [必需]
5. `CALENDLY_REVOKE_USER_S_ORGANIZATION_INVITATION` - 撤销待处理的邀请 [可选]
6. `CALENDLY_REMOVE_USER_FROM_ORGANIZATION` - 从组织中移除成员 [可选]

**关键参数**：
- `uuid`：组织 UUID
- `email`：要邀请的用户的电子邮件地址
- `status`：按 `"pending"`、`accepted` 或 `"declined"` 过滤邀请

**注意事项**：
- 只有组织所有者或管理员才能管理和删除邀请；其他人会收到权限错误。
- 对于同一电子邮件地址，系统会拒绝重复的活跃邀请——请先检查现有的邀请。
- 组织所有者不能通过 `CALENDLY_REMOVE_USER_FROM_ORGANIZATION` 被移除。
- 邀请状态包括 pending、accepted、declined 和 revoked——请相应地处理这些状态。

## 常见模式

### ID 解析
Calendly 使用完整的 API URI 作为标识符，而不是简单的 ID：
- **当前用户 URI**：`CALENDLY_GET_CURRENT_USER` 返回 `resource.uri`（例如：`https://api.calendly.com/users/{uuid}`）
- **组织 URI**：在当前用户响应中的 `resource.current_organization` 处获取
- **事件 UUID**：从事件 URI 或列表响应中提取
- **事件类型 URI**：来自 `CALENDLY_LIST_USER_S_EVENT_TYPES` 的响应

**重要提示**：在列表/过滤端点中，切勿使用 `"me"` 作为用户参数。始终先解析为完整的 URI。

### 分页
大多数 Calendly 列表端点使用基于令牌的分页：
- 设置 `count` 以指定每页显示的数量（默认为 20）
- 使用 `pagination.next_page_token` 进行分页，直到 `page_token` 不存在为止
- 使用 `field:direction` 格式进行排序（例如：`start_time:asc`、`created_at:desc`）

### 时间处理
- 所有时间戳都必须采用 UTC 格式：`yyyy-MM-ddTHH:mm:ss.ffffffZ`
- 使用 `min_start_time` / `max_start_time` 对事件进行日期范围过滤
- 可用时间查询的最大范围为 7 天；较长的查询需要分多次调用。

## 常见问题

### URI 格式
- 所有实体引用都使用完整的 Calendly API URI（例如：`https://api.calendly.com/users/{uuid}`）
- 在需要 URI 的地方，切勿传递裸露的 UUID，也切勿在列表端点中使用 `"me"`。
- 当工具需要 UUID 参数时（例如：`CALENDLY_GET_EVENT`），请从 URI 中提取 UUID。

### 范围要求
- `CALENDLY_LIST_events` 必须指定一个范围（用户、组织或组）——不能多于或少于一个。
- 组织/组范围的查询可能需要管理员权限。
- 令牌范围决定了可用的操作；403 错误表示权限不足。

### 数据关系
- 事件有受邀者（参加预订的人员）。
- 事件类型定义了日程安排页面（持续时间、可用性规则）。
- 组织包含用户和组。
- 日程链接与事件类型相关联，而非直接与事件相关。

### 速率限制
- Calendly API 有速率限制；避免对大量数据集进行循环调用。
- 负责任地分页处理数据，并为批量操作添加延迟。

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 获取当前用户 | `CALENDLY_GET_CURRENT_USER` | （无） |
| 通过 UUID 获取用户 | `CALENDLY_GET_USER` | `uuid` |
| 列出事件 | `CALENDLY_LIST_events` | `user`, `status`, `min_start_time` |
| 获取事件详情 | `CALENDLY_GET_EVENT` | `uuid` |
| 取消事件 | `CALENDLY_CANCEL_EVENT` | `uuid`, `reason` |
| 列出受邀者 | `CALENDLY_LIST_EVENT_INVITEES` | `uuid`, `status`, `email` |
| 获取受邀者信息 | `CALENDLY_GET_EVENT_INVITEE` | `event_uuid`, `invitee_uuid` |
| 列出事件类型 | `CALENDLY_LIST_USER_S_EVENT_TYPES` | `user`, `active` |
| 获取事件类型 | `CALENDLY_GET_EVENT_TYPE` | `uuid` |
| 检查可用时间 | `CALENDLY_LIST_EVENT_TYPE_AVAILABLE_times` | event_type URI, `start_time`, `end_time` |
| 创建日程链接 | `CALENDLY_CREATE_SCHEDULING_LINK` | `owner`, `max_event_count` |
| 查看用户可用日程 | `CALENDLY_LIST_USER_AVAILABILITY_SCHEDULES` | user URI |
| 获取组织信息 | `CALENDLY_GET_ORGANIZATION` | `uuid` |
| 向组织发送邀请 | `CALENDLY_CREATE_ORGANIZATION_INVITATION` | `uuid`, `email` |
| 列出组织邀请 | `CALENDLY_LIST_ORGANIZATION_INVITATIONS` | `uuid`, `status` |
| 撤销组织邀请 | `CALENDLY_REVOKE_USER_S_ORGANIZATION_INVITATION` | org UUID, invitation UUID |
| 从组织中移除成员 | `CALENDLY_REMOVE_USER_FROM_ORGANIZATION` | membership UUID |