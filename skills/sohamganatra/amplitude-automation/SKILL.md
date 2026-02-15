---
name: amplitude-automation
description: "通过 Rube MCP (Composio) 自动化 Amplitude 任务：处理事件、用户活动、用户分组以及用户识别。在使用任何工具之前，请务必先查询当前的架构（schema）信息。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Amplitude 自动化

通过 Composio 的 Amplitude 工具包和 Rube MCP 来自动化 Amplitude 产品分析。

## 先决条件

- Rube MCP 必须已连接（可使用 `RUBE_SEARCH_TOOLS`）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `amplitude` 工具包建立有效的 Amplitude 连接
- 在执行任何工作流之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息

## 设置

**添加 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并使用 `amplitude` 工具包。
3. 如果连接状态不是 `ACTIVE`，请按照返回的认证链接完成 Amplitude 认证。
4. 在运行任何工作流之前，确保连接状态显示为 `ACTIVE`。

## 核心工作流

### 1. 发送事件

**使用场景**：用户希望跟踪事件或将事件数据发送到 Amplitude

**工具顺序**：
1. `AMPLITUDE_SEND_events` - 向 Amplitude 发送一个或多个事件 [必需]

**关键参数**：
- `events`：事件对象数组，每个对象包含：
  - `event_type`：事件类型（例如：`page_view`、`purchase`）
  - `user_id`：唯一用户标识符（如果没有 `device_id` 则必需）
  - `device_id`：设备标识符（如果没有 `user_id` 则必需）
  - `event_properties`：包含自定义事件属性的对象
  - `user_properties`：包含要设置的用户属性的对象
  - `time`：自纪元以来的事件时间戳（以毫秒为单位）

**注意事项**：
- 每个事件至少需要 `user_id` 或 `device_id` 中的一个。
- 每个事件都必须指定 `event_type`，不能为空。
- `time` 必须以毫秒为单位（13 位纪元时间）。
- 有批量限制；请查看架构以了解每次请求的最大事件数量。
- 事件是异步处理的；成功的 API 响应并不意味着数据可以立即查询。

### 2. 获取用户活动

**使用场景**：用户希望查看特定用户的事件历史记录

**工具顺序**：
1. `AMPLITUDE_FIND_USER` - 通过 ID 或属性查找用户 [先决条件]
2. `AMPLITUDE_GET_USER_activity` - 获取用户的事件流 [必需]

**关键参数**：
- `user`：Amplitude 内部用户 ID（来自 `FIND_USER`）
- `offset`：事件列表的分页偏移量
- `limit`：返回的最大事件数量

**注意事项**：
- `user` 参数需要使用 Amplitude 的内部用户 ID，而不是您应用程序的用户 ID。
- 必须先调用 `FIND_USER` 将您的用户 ID 转换为 Amplitude 的内部 ID。
- 活动默认按时间倒序返回。
- 如果活动历史记录很长，需要使用 `offset` 进行分页。

### 3. 查找和识别用户

**使用场景**：用户希望查找用户或设置用户属性

**工具顺序**：
1. `AMPLITUDE_FIND_USER` - 通过各种标识符搜索用户 [必需]
2. `AMPLITUDE_IDENTIFY` - 设置或更新用户属性 [可选]

**关键参数**：
- 对于 `FIND_USER`：
  - `user`：搜索词（user_id、email 或 Amplitude ID）
- 对于 `IDENTIFY`：
  - `user_id`：您应用程序的用户标识符
  - `device_id`：设备标识符（作为 `user_id` 的替代选项）
  - `user_properties`：包含 `$set`、`$unset`、`$add`、`$append` 操作的对象

**注意事项**：
- `FIND_USER` 可以通过 `user_id`、`device_id` 和 Amplitude ID 进行搜索。
- `IDENTIFY` 支持特殊的属性操作（`$set`、`$unset`、`$add`、`$append`）。
- `$set` 会覆盖现有值；`$setOnce` 仅在属性未设置时才设置。
- `IDENTIFY` 需要 `user_id` 或 `device_id` 中的至少一个。
- 用户属性的更改是最终一致的，但不是立即生效的。

### 4. 管理用户群体

**使用场景**：用户希望列出用户群体、查看群体详情或更新群体成员资格

**工具顺序**：
1. `AMPLITUDE_LIST_COHORTS` - 列出所有保存的用户群体 [必需]
2. `AMPLITUDE_GET_COHORT` - 获取详细的群体信息 [可选]
3. `AMPLITUDE_UPDATE_COHORT_MEMBERSHIP` - 向群体中添加/移除用户 [可选]
4. `AMPLITUDE_CHECK_COHORT_STATUS` - 检查群体操作的异步状态 [可选]

**关键参数**：
- 对于 `LIST_COHORTS`：无需参数
- 对于 `GET_COHORT`：`cohort_id`（来自列表结果）
- 对于 `UPDATE_COHORT_MEMBERSHIP`：
  - `cohort_id`：目标群体 ID
  - `memberships`：包含用户 ID 的数组（用于添加或移除成员）
- 对于 `CHECK_COHORT_STATUS`：更新响应中的 `request_id`

**注意事项**：
- 所有与群体相关的操作都需要群体 ID。
- `UPDATE_COHORT_MEMBERSHIP` 是异步的；请使用 `CHECK_COHORT_STATUS` 来验证状态。
- 需要更新响应中的 `request_id` 来检查状态。
- 每次请求的成员变更次数可能有限；请分批处理大量更新。
- 仅行为群体支持 API 成员资格更新。

### 5. 浏览事件类别

**使用场景**：用户希望查看 Amplitude 中可用的事件类型和类别

**工具顺序**：
1. `AMPLITUDE_GET_EVENT_CATEGORIES` - 列出所有事件类别 [必需]

**关键参数**：
- 无需参数；返回所有配置的事件类别

**注意事项**：
- 类别在 Amplitude UI 中进行配置；API 提供读取访问权限。
- 类别中的事件名称区分大小写。
- 在发送事件之前，请使用这些类别来验证 `event_type` 的值。

## 常见模式

### ID 转换

**应用程序用户 ID -> Amplitude 内部 ID**：
```
1. Call AMPLITUDE_FIND_USER with user=your_user_id
2. Extract Amplitude's internal user ID from response
3. Use internal ID for GET_USER_ACTIVITY
```

**群体名称 -> 群体 ID**：
```
1. Call AMPLITUDE_LIST_COHORTS
2. Find cohort by name in results
3. Extract id for cohort operations
```

### 用户属性操作

Amplitude 的 `IDENTIFY` 支持以下属性操作：
- `$set`：设置属性值（覆盖现有值）
- `$setOnce`：仅在属性未设置时设置
- `$add`：增加数值属性
- `$append`：将值添加到列表中
- `$unset`：完全删除属性

示例结构：
```json
{
  "user_properties": {
    "$set": {"plan": "premium", "company": "Acme"},
    "$add": {"login_count": 1}
  }
}
```

### 异步操作模式

对于群体成员资格的更新：
```
1. Call AMPLITUDE_UPDATE_COHORT_MEMBERSHIP -> get request_id
2. Call AMPLITUDE_CHECK_COHORT_STATUS with request_id
3. Repeat step 2 until status is 'complete' or 'error'
```

## 已知问题

**用户 ID**：
- Amplitude 有自己的内部用户 ID，与您的应用程序的用户 ID 不同。
- `FIND_USER` 会将您的 ID 转换为 Amplitude 的内部 ID。
- `GET_USER_activity` 需要 Amplitude 的内部 ID，而不是您的用户 ID。

**事件时间戳**：
- 必须以毫秒为单位（13 位纪元时间）。
- 如果使用秒（10 位），会被解释为非常旧的日期。
- 如果省略时间戳，将使用服务器接收时间。

**速率限制**：
- 每个项目都有事件摄入的吞吐量限制。
- 尽可能批量发送事件以减少 API 调用次数。
- 群体成员资格的更新具有异步处理限制。

**响应解析**：
- 响应数据可能嵌套在 `data` 键下。
- 用户活动按时间倒序返回。
- 群体列表可能包含已归档的群体；请检查 `status` 字段。
- 对于可选字段，请采取防御性解析措施。

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 发送事件 | AMPLITUDE_SEND_events | events (array) |
| 查找用户 | AMPLITUDE_FIND_USER | user |
| 获取用户活动 | AMPLITUDE_GET_USER_activity | user, offset, limit |
| 识别用户 | AMPLITUDE_IDENTIFY | user_id, user_properties |
| 列出群体 | AMPLITUDE_LIST_COHORTS | (none) |
| 获取群体 | AMPLITUDE_GET_COHORT | cohort_id |
| 更新群体成员 | AMPLITUDE_UPDATE_COHORT_MEMBERSHIP | cohort_id, memberships |
| 检查群体状态 | AMPLITUDE_CHECK_COHORT_STATUS | request_id |
| 列出事件类别 | AMPLITUDE_GET_EVENT_CATEGORIES | (none) |