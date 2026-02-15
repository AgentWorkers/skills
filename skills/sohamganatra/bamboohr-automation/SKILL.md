---
name: bamboohr-automation
description: "通过 Rube MCP (Composio) 自动化 BambooHR 的各项任务：员工信息管理、休假申请处理、福利发放、家属信息更新等。在使用任何工具之前，请务必先查询其当前的数据库架构（schema）。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 BambooHR 操作

通过 Composio 的 BambooHR 工具包和 Rube MCP 来自动化 BambooHR 的人力资源管理操作。

## 先决条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `bamboohr` 工具包建立有效的 BambooHR 连接
- 在运行任何工作流之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息

## 设置

**添加 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 使用 `bamboohr` 工具包调用 `RUBE_MANAGE_CONNECTIONS`。
3. 如果连接状态不是 `ACTIVE`，请按照返回的认证链接完成 BambooHR 的身份验证。
4. 在运行任何工作流之前，确保连接状态显示为 `ACTIVE`。

## 核心工作流

### 1. 列出和搜索员工

**使用场景**：用户需要查找员工或获取完整的员工目录。

**工具顺序**：
1. `BAMBOOHR_GET_ALL_EMPLOYEES` - 获取员工目录 [必需]
2. `BAMBOOHR_GET_EMPLOYEE` - 获取特定员工的详细信息 [可选]

**关键参数**：
- 对于 `GET_ALL_EMPLOYEES`：无需参数；返回员工目录。
- 对于 `GET_EMPLOYEE`：
  - `id`：员工 ID（数字）
  - `fields`：以逗号分隔的字段列表（例如，'firstName, lastName, department, jobTitle'）

**注意事项**：
- 员工 ID 是数字整数。
- `GET_ALL_EMPLOYEES` 返回基本目录信息；如需完整详细信息，请使用 `GET_EMPLOYEE`。
- `fields` 参数用于控制返回的字段；省略该参数可能会返回最少的数据。
- 常见字段：firstName, lastName, department, division, jobTitle, workEmail, status。
- 包括非活跃/已终止的员工；请检查 `status` 字段。

### 2. 跟踪员工信息变更

**使用场景**：用户需要检测员工的最新数据变更以进行同步或审计。

**工具顺序**：
1. `BAMBOOHR_EMPLOYEE_GET_CHANGED` - 获取发生变更的员工 [必需]

**关键参数**：
- `since`：用于检测变更的 ISO 8601 日期时间字符串。
- `type`：要检查的变更类型（例如，'inserted', 'updated', 'deleted'）。

**注意事项**：
- `since` 参数是必需的；请使用 ISO 8601 格式（例如，'2024-01-15T00:00:00Z'）。
- 返回的是发生变更的员工的 ID，而不是完整的员工信息。
- 需要为每个变更的员工单独调用 `GET_EMPLOYEE` 来获取详细信息。
- 适用于增量同步工作流；请缓存上次同步的时间戳。

### 3. 管理休假

**使用场景**：用户需要查看休假余额、申请休假或管理休假请求。

**工具顺序**：
1. `BAMBOOHR_GET_meta_TIME_OFF_TYPES` - 列出可用的休假类型 [必需]
2. `BAMBOOHR_GET_TIME_OFF_BALANCES` - 检查当前休假余额 [可选]
3. `BAMBOOHR_GET_TIME_OFF_REQUESTS` - 列出现有的休假请求 [可选]
4. `BAMBOOHR_CREATE_TIME_OFF_REQUEST` - 提交新的休假请求 [可选]
5. `BAMBOOHR_UPDATE_TIME_OFF_REQUEST` - 修改或批准/拒绝休假请求 [可选]

**关键参数**：
- 对于余额：`employeeId`, 休假类型 ID
- 对于请求：`start`, `end`（日期范围），`employeeId`
- 对于创建请求：
  - `employeeId`：要申请休假的员工 ID
  - `timeOffTypeId`：来自 `GET_META_TIME_OFF_TYPES` 的类型 ID
  - `start`：开始日期（YYYY-MM-DD）
  - `end`：结束日期（YYYY-MM-DD）
  - `amount`：休假天数/小时数
  - `notes`：请求的备注（可选）
- 对于更新请求：`requestId`, `status`（'approved', 'denied', 'cancelled'）

**注意事项**：
- 休假类型 ID 是数字；请先通过 `GET_META_TIME_OFF_TYPES` 获取。
- 开始和结束日期的格式为 'YYYY-MM-DD'。
- 余额可能以小时或天为单位，具体取决于公司配置。
- 更新请求状态需要相应的权限（经理/管理员级别）。
- 创建请求不会自动批准；需要单独的批准步骤。

### 4. 更新员工信息

**使用场景**：用户需要修改员工资料。

**工具顺序**：
1. `BAMBOOHR_GET_EMPLOYEE` - 获取当前员工信息 [必需]
2. `BAMBOOHR_UPDATE_EMPLOYEE` - 更新员工字段 [必需]

**关键参数**：
- `id`：员工 ID（数字，必需）
- 需要更新的字段及其值（例如，`department`, `jobTitle`, `workPhone`）

**注意事项**：
- 只有请求中包含的字段才会被更新；其他字段保持不变。
- 某些字段是只读的，无法通过 API 进行更新。
- 字段名称必须与 BambooHR 的预期名称完全匹配。
- 更新操作会被记录在员工的变更历史中；更新前请使用 `GET_EMPLOYEE` 验证当前值，以避免覆盖。

### 5. 管理员工依赖关系和福利

**使用场景**：用户需要查看员工的依赖关系或福利覆盖情况。

**工具顺序**：
1. `BAMBOOHR_DEPENDENTS_GET_ALL` - 列出所有依赖关系 [必需]
2. `BAMBOOHR_BENEFIT_GET_COVERAGES` - 获取福利覆盖详情 [可选]

**关键参数**：
- 对于依赖关系：可选的 `employeeId` 过滤条件
- 对于福利：具体参数取决于架构；请查阅 RUBE_SEARCH_TOOLS 以获取当前参数。

**注意事项**：
- 依赖关系数据包含敏感的个人信息（PII）；请妥善处理。
- 每位员工的福利覆盖可能包含多种计划类型。
- 并非所有 BambooHR 计划都包含福利管理功能；请查看账户设置。
- 数据访问权限取决于 API 密钥。

## 常见模式

### ID 解析

**员工姓名 -> 员工 ID**：
```
1. Call BAMBOOHR_GET_ALL_EMPLOYEES
2. Find employee by name in directory results
3. Extract id (numeric) for detailed operations
```

**休假类型名称 -> 类型 ID**：
```
1. Call BAMBOOHR_GET_META_TIME_OFF_TYPES
2. Find type by name (e.g., 'Vacation', 'Sick Leave')
3. Extract id for time-off requests
```

### 增量同步模式

为了保持外部系统与 BambooHR 的同步：
```
1. Store last_sync_timestamp
2. Call BAMBOOHR_EMPLOYEE_GET_CHANGED with since=last_sync_timestamp
3. For each changed employee ID, call BAMBOOHR_GET_EMPLOYEE
4. Process updates in external system
5. Update last_sync_timestamp
```

### 休假工作流
```
1. GET_META_TIME_OFF_TYPES -> find type ID
2. GET_TIME_OFF_BALANCES -> verify available balance
3. CREATE_TIME_OFF_REQUEST -> submit request
4. UPDATE_TIME_OFF_REQUEST -> approve/deny (manager action)
```

## 已知问题

**员工 ID**：
- 始终为数字整数。
- 通过 `GET_ALL_EMPLOYEES` 将姓名解析为 ID。
- 已终止的员工仍保留其 ID。

**日期格式**：
- 休假日期：'YYYY-MM-DD'。
- 变更检测：使用带时区的 ISO 8601 格式。
- 不同端点的格式可能不一致；请检查每个端点的架构。

**权限**：
- API 密钥权限决定了可访问的字段和操作。
- 某些操作需要管理员或经理级别的权限。
- 休假批准需要相应的角色权限。

**敏感数据**：
- 员工数据包含个人信息（姓名、地址、SSN 等）。
- 请采取适当的安全措施处理所有响应数据。
- 依赖关系数据尤其敏感。

**速率限制**：
- BambooHR API 对每个 API 密钥有速率限制。
- 应对批量操作进行节流。
- `GET_ALL_EMPLOYEES` 比单独的 `GET_EMPLOYEE` 调用更高效。

**响应解析**：
- 响应数据可能嵌套在 `data` 键下。
- 员工字段会根据 `fields` 参数而有所不同。
- 空字段可能被省略或返回为 null。
- 请采取防御性措施进行解析，并设置默认值。

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 列出所有员工 | BAMBOOHR_GET_ALL_EMPLOYEES | （无） |
| 获取员工详情 | BAMBOOHR_GET_EMPLOYEE | id, fields |
| 跟踪变更 | BAMBOOHR_EMPLOYEE_GET_CHANGED | since, type |
| 休假类型 | BAMBOOHR_GET_meta_TIME_OFF_TYPES | （无） |
| 休假余额 | BAMBOOHR_GET_TIME_OFF_BALANCES | employeeId |
| 列出休假请求 | BAMBOOHR_GET_TIME_OFF_REQUESTS | start, end, employeeId |
| 创建休假请求 | BAMBOOHR_CREATE_TIME_OFF_REQUEST | employeeId, timeOffTypeId, start, end |
| 更新休假请求 | BAMBOOHR_UPDATE_TIME_OFF_REQUEST | requestId, status |
| 更新员工信息 | BAMBOOHR_UPDATE_EMPLOYEE | id, (field updates) |
| 列出依赖关系 | BAMBOOHR_DEPENDENTS_GET_ALL | employeeId |
| 福利覆盖 | BAMBOOHR_BENEFIT_GET_COVERAGES | （请查看架构） |