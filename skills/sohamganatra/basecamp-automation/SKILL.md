---
name: basecamp-automation
description: 通过 Rube MCP (Composio) 自动化 Basecamp 项目管理工作，包括待办事项、消息、人员管理以及待办事项列表的组织。在使用任何工具之前，请务必先查询其当前使用的架构（schema）。
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 Basecamp 操作

使用 Composio 的 Basecamp 工具包，可以自动化 Basecamp 的各种操作，包括项目管理、待办事项列表创建、任务管理、消息板发布、人员管理以及待办事项组的组织。

## 先决条件

- 必须已连接 Rube MCP（可使用 `RUBE_SEARCH_TOOLS`）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `basecamp` 工具包建立有效的 Basecamp 连接
- 在运行任何工作流之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 使用 `basecamp` 工具包调用 `RUBE_MANAGE_CONNECTIONS`。
3. 如果连接未处于活动状态，请按照返回的认证链接完成 Basecamp 的 OAuth 验证。
4. 在运行任何工作流之前，确保连接状态显示为“活动”（ACTIVE）。

## 核心工作流

### 1. 管理待办事项列表和任务

**使用场景**：用户需要创建待办事项列表、添加任务或在 Basecamp 项目中组织任务。

**工具顺序**：
1. `BASECAMP_GETPROJECTS` - 列出项目以找到目标 `bucket_id` [先决条件]
2. `BASECAMP_GET_BUCKETS_TODOSETS` - 获取项目内的待办事项集 [先决条件]
3. `BASECAMP_GET_BUCKETS_TODOSETS_TODOLISTS` - 列出现有的待办事项列表以避免重复 [可选]
4. `BASECAMP_POST_BUCKETS_TODOSETS_TODOLISTS` - 在待办事项集中创建新的待办事项列表 [创建列表时必需]
5. `BASECAMP_GET_BUCKETS_TODOLISTS` - 获取特定待办事项列表的详细信息 [可选]
6. `BASECAMP_POST_BUCKETS_TODOLISTS_TODOS` - 在待办事项列表中创建待办事项 [创建任务时必需]
7. `BASECAMP_CREATE_TODO` - 另一种创建单个待办事项的工具 [备用方法]
8. `BASECAMP_GET_BUCKETS_TODOLISTS_TODOS` - 列出待办事项列表中的待办事项 [可选]

**创建待办事项列表的关键参数**：
- `bucket_id`：项目/桶的整数 ID（来自 `GETPROJECTS`）
- `todoset_id`：待办事项集的整数 ID（来自 `GET_BUCKETS_TODOSETS`）
- `name`：待办事项列表的名称（必需）
- `description`：支持富文本格式的描述

**创建待办事项的关键参数**：
- `bucket_id`：项目/桶的整数 ID
- `todolist_id`：待办事项列表的整数 ID
- `content`：待办事项的内容（必需）
- `description`：关于待办事项的 HTML 详细信息
- `assignee_ids`：需要通知的人员 ID 数组
- `due_on`：截止日期（格式为 `YYYY-MM-DD`）
- `starts_on`：开始日期（格式为 `YYYY-MM-DD`）
- `notify`：是否通知分配者（默认为 `false`）
- `completion_subscriber_ids`：任务完成时需要通知的人员 ID

**注意事项**：
- 一个项目（桶）可以包含多个待办事项集；选择错误的 `todoset_id` 会导致待办事项列表被创建在错误的分类中。
- 在创建待办事项之前，请务必检查现有的待办事项列表以避免名称重复。
- 成功响应中包含面向用户的 URL（`app_url`、`app_todos_url`）；建议返回这些 URL 而不是原始 ID。
- 所有 ID（`bucket_id`、`todoset_id`、`todolist_id`）都是整数，不是字符串。
- 描述仅支持 HTML 格式，不支持 Markdown。

### 2. 发布和管理消息

**使用场景**：用户需要向项目消息板发布消息或更新现有消息。

**工具顺序**：
1. `BASECAMP_GETPROJECTS` - 查找目标项目和 `bucket_id` [先决条件]
2. `BASECAMP_GET_MESSAGEBOARD` - 获取项目的消息板 ID [先决条件]
3. `BASECAMP_CREATE_MESSAGE` - 在消息板上创建新消息 [必需]
4. `BASECAMP_POST_BUCKETS_MESSAGE_BOARDS_MESSAGES` - 另一种创建消息的工具 [备用方法]
5. `BASECAMP_GET_MESSAGE` - 通过 ID 读取特定消息 [可选]
6. `BASECAMP_PUT_BUCKETS_MESSAGES` - 更新现有消息 [可选]

**关键参数**：
- `bucket_id`：项目/桶的整数 ID
- `message_board_id`：消息板的整数 ID（来自 `GET_MESSAGE_board`）
- `subject`：消息标题（必需）
- `content`：消息的正文（HTML 格式）
- `status`：设置为 `"active"` 以立即发布
- `category_id`：消息类型分类（可选）
- `subscriptions`：需要通知的人员 ID 数组；省略则通知所有项目成员

**注意事项**：
- 使用 `status="draft"` 可能会导致 HTTP 400 错误；建议使用 `status="active"` 作为可靠的选择。
- `bucket_id` 和 `message_board_id` 必须属于同一个项目；不匹配会导致请求失败或路由错误。
- 消息内容仅支持 HTML 标签；不支持 Markdown。
- 通过 `PUT_BUCKETS_MESSAGES` 更新消息时，会替换整个正文——请包含完整的正确内容，而不仅仅是差异部分。
- 建议使用响应中的 `app_url` 作为面向用户的确认链接。
- `CREATE_MESSAGE` 和 `POST_BUCKETS_MESSAGE_BOARDS_MESSAGES` 的功能相同；优先使用 `CREATE_MESSAGE`，如果失败则使用 `POST`。

### 3. 管理人员和访问权限

**使用场景**：用户需要列出人员、管理项目访问权限或添加新用户。

**工具顺序**：
1. `BASECAMP_GET_PEOPLE` - 列出当前用户可见的所有人员 [必需]
2. `BASECAMP_GETPROJECTS` - 查找目标项目 [先决条件]
3. `BASECAMP_LIST_Project_PEOPLE` - 列出特定项目的人员 [必需]
4. `BASECAMP_GET_PROJECTS_PEOPLE` - 列出项目成员的另一种方式 [备用方法]
5. `BASECAMP.PUTPROJECTS_PEOPLE_USERS` - 授予或撤销项目访问权限 [更改访问权限时必需]

**`PUTPROJECTS_PEOPLE_USERS` 的关键参数**：
- `project_id`：项目的整数 ID
- `grant`：要添加到项目中的人员 ID 数组
- `revoke`：要从项目中移除的人员 ID 数组
- `create`：新用户的对象数组，包含 `name`、`email_address` 以及可选的 `company_name`、`title`
- 必须提供 `grant`、`revoke` 或 `create` 中的至少一个参数。

**注意事项**：
- 人员 ID 是整数；在使用前请通过 `GET_PEOPLE` 将名称转换为 ID。
- 用于人员管理的 `project_id` 与其他操作中的 `bucket_id` 是相同的。
- `LIST_Project_PEOPLE` 和 `GETPROJECTS_PEOPLE` 的功能几乎相同；可以选择其中一个使用。
- 通过 `create` 创建用户的同时也会授予他们项目访问权限。

### 4. 使用组别组织待办事项

**使用场景**：用户希望将待办事项按颜色分组。

**工具顺序**：
1. `BASECAMP_GETPROJECTS` - 查找目标项目 [先决条件]
2. `BASECAMP_GET_BUCKETS_TODOLISTS` - 获取待办事项列表的详细信息 [先决条件]
3. `BASECAMP_GET_TODOLIST_groups` - 列出待办事项列表中现有的组别 [可选]
4. `BASECAMP_GET_BUCKETS_TODOLISTS_groups` - 另一种列出组别的方法 [备用方法]
5. `BASECAMP_POST_BUCKETS_TODOLISTS_groups` - 在待办事项列表中创建新的组别 [必需]
6. `BASECAMP_CREATE_TODOLIST_GROUP` - 另一种创建组别的工具 [备用方法]

**关键参数**：
- `bucket_id`：项目/桶的整数 ID
- `todolist_id`：待办事项列表的整数 ID
- `name`：组别的名称（必需）
- `color`：视觉颜色标识符（可选值：`white`、`red`、`orange`、`yellow`、`green`、`blue`、`aqua`、`purple`、`gray`、`pink`、`brown`
- `status`：过滤条件（用于列出）——`"archived"` 或 `"trashed"`（对于活动组别省略）

**注意事项**：
- `POST_BUCKETS_TODOLISTS_groups` 和 `CREATE_TODOLIST_GROUP` 的功能几乎相同；可以选择其中一个使用。
- 颜色值必须来自预定义的调色板；不支持自定义的十六进制/RGB 值。
- 组别是待办事项列表内的子部分，而不是独立的实体。

### 5. 浏览和检查项目

**使用场景**：用户需要列出项目、获取项目详细信息或探索项目结构。

**工具顺序**：
1. `BASECAMP_GETPROJECTS` - 列出所有活动项目 [必需]
2. `BASECAMP_GET_Project` - 获取特定项目的详细信息 [可选]
3. `BASECAMP_GETPROJECTS_BYPROJECT_ID` - 另一种获取项目详细信息的方法 [备用方法]

**关键参数**：
- `status`：按 `"archived"` 或 `"trashed"` 过滤；对于活动项目省略此参数
- `project_id`：用于详细信息查询的项目 ID

**注意事项**：
- 项目按创建时间顺序排序（最新创建的项目排在最前面）。
- 响应中包含一个 `dock` 数组，其中包含工具（如待办事项集、消息板等）及其 ID。
- 使用 `dock` 中的工具 ID 来查找 `todoset_id`、`message_board_id` 等，以便进行后续操作。

## 常见模式

### ID 解析
Basecamp 使用分层 ID 结构。始终从上到下解析：
- **项目（bucket_id）**：`BASECAMP_GETPROJECTS` —— 通过名称查找并获取 `id`
- **待办事项集（todoset_id）**：在项目 `dock` 中查找或通过 `BASECAMP_GET_BUCKETS_TODOSETS` 获取
- **消息板（message_board_id）**：在项目 `dock` 中查找或通过 `BASECAMP_GET_MESSAGEBOARD` 获取
- **待办事项列表（todolist_id）**：`BASECAMP_GET_BUCKETS_TODOSETS_TODOLISTS`
- **人员（person_id）**：`BASECAMP_GET_PEOPLE` 或 `BASECAMP_LIST_Project_PEOPLE`
- 注意：`bucket_id` 和 `project_id` 在不同上下文中指的是同一个实体。

### 分页
Basecamp 在列表端点上使用基于页面的分页机制：
- 响应头或正文可能指示还有更多页面可用。
- `GETPROJECTS`、`GET_BUCKETS_TODOSETS_TODOLISTS` 和列表端点返回分页结果。
- 继续请求直到没有更多结果返回为止。

### 内容格式
- 所有富文本字段都使用 HTML 格式，不使用 Markdown。
- 使用 `<div>` 标签包裹内容；可以使用 `<strong>`、`<em>`、`<ul>`、`<ol>`、`<li>`、`<a>` 等标签。
- 例如：`<div><strong>重要：</strong>请在周五之前完成</div>`

## 已知的注意事项

### ID 格式
- 所有 Basecamp ID 都是整数，不是字符串或 UUID。
- `bucket_id` = `project_id`（相同的实体，但在不同工具中参数名称不同）。
- 待办事项集 ID、待办事项列表 ID 和消息板 ID 都可以在项目的 `dock` 数组中找到。
- 人员 ID 是整数；在使用前请通过 `GET_PEOPLE` 将名称转换为 ID。

### 状态字段
- 对于消息，使用 `status="draft"` 可能会导致 HTTP 400 错误；始终使用 `status="active"`。
- 项目/待办事项列表的状态过滤器：`"archived"`、`"trashed"`；对于活动项目可以省略此字段。

### 内容格式
- 仅支持 HTML 格式，不支持 Markdown。
- 更新操作会替换整个正文，而不仅仅是部分差异。
- 无效的 HTML 标签可能会被自动删除。

### 速率限制
- Basecamp API 有速率限制；请分散快速连续的请求。
- 对于待办事项较多的大型项目，应谨慎使用分页功能。

### URL 处理
- 建议使用 API 响应中的 `app_url` 作为面向用户的链接。
- 不要手动从 ID 重新构建 Basecamp 的 URL。

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 列出项目 | `BASECAMP_GETPROJECTS` | `status` |
| 获取项目 | `BASECAMP_GETPROJECT` | `project_id` |
| 获取项目详细信息 | `BASECAMP_GETPROJECTS_BYPROJECT_ID` | `project_id` |
| 获取待办事项集 | `BASECAMP_GET_BUCKETS_TODOSETS` | `bucket_id`, `todoset_id` |
| 列出待办事项列表 | `BASECAMP_GET_BUCKETS_TODOSETS_TODOLISTS` | `bucket_id`, `todoset_id` |
| 获取待办事项列表 | `BASECAMP_GET_BUCKETS_TODOLISTS` | `bucket_id`, `todolist_id` |
| 创建待办事项列表 | `BASECAMP_POST_BUCKETS_TODOSETS_TODOLISTS` | `bucket_id`, `todoset_id`, `name` |
| 创建待办事项 | `BASECAMP_POST_BUCKETS_TODOLISTS_TODOS` | `bucket_id`, `todolist_id`, `content` |
| 创建待办事项（备用方法） | `BASECAMP_CREATE_TODO` | `bucket_id`, `todolist_id`, `content` |
| 列出待办事项 | `BASECAMP_GET_BUCKETS_TODOLISTS_TODOS` | `bucket_id`, `todolist_id` |
| 列出待办事项组 | `BASECAMP_GET_TODOLIST_groups` | `bucket_id`, `todolist_id` |
| 创建待办事项组 | `BASECAMP_POST_BUCKETS_TODOLISTS_groups` | `bucket_id`, `todolist_id`, `name`, `color` |
| 创建待办事项组（备用方法） | `BASECAMP_CREATE_TODOLIST_GROUP` | `bucket_id`, `todolist_id`, `name` |
| 获取消息板 | `BASECAMP_GET_MESSAGEBOARD` | `bucket_id`, `message_board_id` |
| 创建消息 | `BASECAMP_CREATE_MESSAGE` | `bucket_id`, `message_board_id`, `subject`, `status` |
| 创建消息（备用方法） | `BASECAMP_POST_BUCKETS_MESSAGE_BOARDS_MESSAGES` | `bucket_id`, `message_board_id`, `subject` |
| 获取消息 | `BASECAMP_GET_MESSAGE` | `bucket_id`, `message_id` |
| 更新消息 | `BASECAMP_PUT_BUCKETS_MESSAGES` | `bucket_id`, `message_id` |
| 列出所有人员 | `BASECAMP_GET_PEOPLE` | （无参数） |
| 列出项目人员 | `BASECAMP_LIST_Project_PEOPLE` | `project_id` |
| 管理访问权限 | `BASECAMP.PUTPROJECTS_PEOPLE_USERS` | `project_id`, `grant`, `revoke`, `create` |