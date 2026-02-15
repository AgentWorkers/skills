---
name: airtable-automation
description: "通过 Rube MCP (Composio) 自动化 Airtable 任务：包括记录、数据库、表格、字段和视图的操作。在使用任何工具之前，请务必先查询当前的数据库架构（schema）。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Airtable 自动化

通过 Composio 的 Airtable 工具包和 Rube MCP 来自动化 Airtable 操作。

## 先决条件

- Rube MCP 必须已连接（可使用 `RUBE_SEARCH_TOOLS`）
- 通过 `RUBE_MANAGE_connections` 使用 `airtable` 工具包建立有效的 Airtable 连接
- 在执行任何工作流之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息

## 设置

**添加 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可使用。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 使用 `airtable` 工具包调用 `RUBE_MANAGE_connections`。
3. 如果连接状态不是 `ACTIVE`，请按照返回的认证链接完成 Airtable 的认证。
4. 在运行任何工作流之前，确保连接状态显示为 `ACTIVE`。

## 核心工作流

### 1. 创建和管理记录

**使用场景**：用户需要创建、读取、更新或删除记录

**工具执行顺序**：
1. `AIRTABLE_LIST_BASES` - 查找可用的数据库 [先决条件]
2. `AIRTABLE_GET_BASE_SCHEMA` - 检查表格结构 [先决条件]
3. `AIRTABLE_LIST_RECORDS` - 列出/过滤记录 [可选]
4. `AIRTABLE_CREATE_RECORD` / `AIRTABLE_CREATE_RECORDS` - 创建记录 [可选]
5. `AIRTABLE_UPDATE_RECORD` / `AIRTABLE_UPDATE_MULTIPLE_RECORDS` - 更新记录 [可选]
6. `AIRTABLE_DELETE_RECORD` / `AIRTABLE_DELETE_MULTIPLE_RECORDS` - 删除记录 [可选]

**关键参数**：
- `baseId`：数据库 ID（以 'app' 开头，例如 'appXXXXXXXXXXXXXX'）
- `tableIdOrName`：表格 ID（以 'tbl' 开头）或表格名称
- `fields`：字段名称与值的映射对象
- `recordId`：记录 ID（以 'rec' 开头，用于更新/删除操作）
- `filterByFormula`：用于过滤的 Airtable 公式
- `typecast`：设置为 `true` 以进行自动类型转换

**注意事项**：
- 每页显示的记录数上限为 100 条；使用偏移量分页；在不同页面之间切换过滤器可能会导致记录遗漏或重复。
- 每次请求创建记录的最大数量为 10 条；批量导入时需要分多次完成。
- 字段名称区分大小写，必须与数据库架构完全匹配。
- 如果字段名称错误，会返回 422 错误代码；权限问题会导致 403 错误。
- 如果选择多个字段进行更新（`INVALID_MULTIPLE_CHOICE_OPTIONS`），可能需要设置 `typecast=true`。

### 2. 搜索和过滤记录

**使用场景**：用户需要使用公式查找特定记录

**工具执行顺序**：
1. `AIRTABLE_GET_BASE_SCHEMA` - 验证字段名称和类型 [先决条件]
2. `AIRTABLE_LIST_RECORDS` - 使用 `filterByFormula` 进行查询 [必需]
3. `AIRTABLE_GET_RECORD` - 获取完整的记录详情 [可选]

**关键参数**：
- `filterByFormula`：Airtable 公式（例如 `{Status}='Done'`）
- `sort`：排序对象数组
- `fields`：需要返回的字段名称数组
- `maxRecords`：所有页面的总记录数上限
- `offset`：来自上一次响应的分页游标

**注意事项**：
- 公式中的字段名称必须用 `{}` 包围，并且必须与数据库架构完全匹配。
- 字符串值需要用引号括起来：例如 `{Status}='Active'` 而不是 `{Status}=Active`。
- 如果公式语法错误或字段不存在，会返回 422 错误代码。
- Airtable 的请求速率限制为每个数据库每秒约 5 次请求；遇到 429 错误时请使用 `Retry-After` 机制重试。

### 3. 管理字段和架构

**使用场景**：用户需要创建或修改表格字段

**工具执行顺序**：
1. `AIRTABLE_GET_BASE_SCHEMA` - 检查当前数据库架构 [先决条件]
2. `AIRTABLE_CREATE_FIELD` - 创建新字段 [可选]
3. `AIRTABLE_UPDATE_FIELD` - 重命名或修改字段 [可选]
4. `AIRTABLE_UPDATE_TABLE` - 更新表格元数据 [可选]

**关键参数**：
- `name`：字段名称
- `type`：字段类型（如 singleLineText、number、singleSelect 等）
- `options`：特定类型的选项（例如选择框的选项、数字的精度）
- `description`：字段描述

**注意事项**：
- `UPDATE_FIELD` 只能修改字段的名称或描述，不能修改字段类型或选项；如果需要修改字段类型，请先创建新字段并迁移数据。
- 计算字段（如公式字段、汇总字段、查找字段）无法通过 API 创建。
- 如果类型选项缺失或格式错误，会返回 422 错误代码。

### 4. 管理评论

**使用场景**：用户需要查看或添加记录的评论

**工具执行顺序**：
1. `AIRTABLE_LIST_COMMENTS` - 列出记录的评论 [必需]

**关键参数**：
- `baseId`：数据库 ID
- `tableIdOrName`：表格标识符
- `recordId`：记录 ID（17 个字符，以 'rec' 开头）
- `pageSize`：每页显示的评论数量（最多 100 条）

**注意事项**：
- 记录 ID 必须是 17 个字符，以 'rec' 开头。

## 常见模式

### Airtable 公式语法

**比较操作**：
- `{Status}='Done'` - 等于
- `{Priority}>1` - 大于
- `{Name}!=''` - 不为空

**函数**：
- `AND({A}='x', {B}='y')` - 两个条件都满足
- `OR({A}='x', {B}='y')` - 任一条件满足
- `FIND('test', {Name})>0` - 包含指定文本
- `IS_BEFORE({Due Date}, TODAY())` - 日期比较

**转义规则**：
- 值中的单引号需要用双引号括起来：例如 `{Name}='John''s Company'`。

### 分页

- 设置 `pageSize`（最多 100 条）
- 检查响应中的 `offset` 字符串
- 将 `offset` 值传递给下一次请求时保持不变
- 确保在不同页面之间过滤条件、排序方式或显示内容保持一致。

## 已知的常见问题

**ID 格式**：
- 数据库 ID：`appXXXXXXXXXXXXXX`（17 个字符）
- 表格 ID：`tblXXXXXXXXXXXXXX`（17 个字符）
- 记录 ID：`recXXXXXXXXXXXXXX`（17 个字符）
- 字段 ID：`fldXXXXXXXXXXXXXX`（17 个字符）

**批量操作限制**：
- 每次请求创建记录的最大数量为 10 条
- 每次请求更新多条记录的最大数量为 10 条
- 每次请求删除多条记录的最大数量为 10 条

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 列出数据库 | AIRTABLE_LIST_BASES | （无） |
| 获取架构 | AIRTABLE_GET_BASE_SCHEMA | baseId |
| 列出记录 | AIRTABLE_LIST_RECORDS | baseId, tableIdOrName |
| 获取记录 | AIRTABLE_GET_RECORD | baseId, tableIdOrName, recordId |
| 创建记录 | AIRTABLE_CREATE_RECORD | baseId, tableIdOrName, fields |
| 创建多条记录 | AIRTABLE_CREATE_RECORDS | baseId, tableIdOrName, records |
| 更新记录 | AIRTABLE_UPDATE_RECORD | baseId, tableIdOrName, recordId, fields |
| 更新多条记录 | AIRTABLE_UPDATE_MULTIPLE_RECORDS | baseId, tableIdOrName, records |
| 删除记录 | AIRTABLE_DELETE_RECORD | baseId, tableIdOrName, recordId |
| 创建字段 | AIRTABLE_CREATE_FIELD | baseId, tableIdOrName, name, type |
| 更新字段 | AIRTABLE_UPDATE_FIELD | baseId, tableIdOrName, fieldId |
| 更新表格 | AIRTABLE_UPDATE_TABLE | baseId, tableIdOrName, name |
| 列出评论 | AIRTABLE_LIST_COMMENTS | baseId, tableIdOrName, recordId |