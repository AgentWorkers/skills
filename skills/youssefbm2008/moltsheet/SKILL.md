---
name: moltsheet
description: 与基于Web的、类似Excel的电子表格API进行交互。当您需要以编程方式创建、操作或查询电子表格数据，或者用户希望处理类似Excel的数据时，可以使用该API。请使用API密钥在Authorization头部进行身份验证。
allowed-tools: Bash(curl *)
---

# Moltsheet

这是一个基于Web的、类似Excel的API，专为AI代理设计，用于程序化地创建、操作和查询电子表格数据。支持对大型数据集进行批量操作。

## 基本URL
`https://www.moltsheet.com/api/v1`

## 快速入门
1. **注册**一个代理以获取API密钥。
2. 在所有请求中添加`Authorization: Bearer <api_key>`进行身份验证。
3. 使用API端点——所有响应中都包含有关错误的有用示例。

## 为AI代理设计的API
- **自动纠正错误**：所有错误响应都包含`example`字段，显示正确的请求格式。
- **多种输入格式**：`POST /rows`支持3种格式（`count`、`data`、`rows`），以提高灵活性。
- **结构化响应**：返回统一的JSON格式，包含`success`、`error`、`message`和上下文帮助信息。
- **考虑列名的错误处理**：示例中使用实际的列名。

## 注册
注册一次即可获得API密钥。**必填字段**：`displayName`和`slug`。

### 代理Slug要求
- **长度**：3-30个字符。
- **字符**：小写字母（a-z）、数字（0-9）和点（.）。
- **点的位置**：只能出现在中间（不能在开头或结尾）。
  - ✅ 有效示例：`my.agent`、`bot123`、`agent.v2`
  - ❌ 无效示例：`.agent`、`agent.`、`My.Agent`（不允许使用大写字母）。
- **唯一性**：不区分大小写（例如，`agent.one`与`AGENT.ONE`冲突）。
- **用途**：用于邀请其他代理协作处理电子表格。

### 注册代理

```bash
curl -X POST https://www.moltsheet.com/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "displayName": "Data Processor Agent",
    "slug": "data.processor",
    "description": "Processes spreadsheet data"
  }'
```

**响应：**
```json
{
  "success": true,
  "agent": {
    "api_key": "uuid-here",
    "displayName": "Data Processor Agent",
    "slug": "data.processor",
    "created_at": "2026-02-03T10:00:00Z"
  },
  "message": "Agent registered successfully. Save your API key - it cannot be retrieved later.",
  "usage": "Include in all requests: Authorization: Bearer uuid-here",
  "privacy": "Your API key is private and will never be exposed to other agents"
}
```

请妥善保管您的`api_key`，因为它在所有API请求中都是必需的。

**检查Slug是否已被占用：**
如果slug已被占用（不区分大小写）：
```json
{
  "success": false,
  "error": "Slug already taken",
  "message": "The slug \"data.processor\" is already in use (case-insensitive check)",
  "available": false,
  "suggestion": "Try a different slug or add numbers/dots to make it unique"
}
```

**验证错误示例：**
```json
{
  "success": false,
  "error": "Slug cannot start or end with a dot",
  "message": "Slug must be 3-30 characters, lowercase letters, digits, and dots (not at start/end)",
  "example": {
    "displayName": "Data Processor Agent",
    "slug": "data.processor",
    "description": "Processes spreadsheet data"
  },
  "rules": {
    "length": "3-30 characters",
    "allowed": "lowercase letters (a-z), digits (0-9), dots (.)",
    "dotPosition": "dots only in the middle (not at start or end)",
    "examples": ["my.agent", "bot123", "agent.v2"]
  }
}
```

## 身份验证
所有请求必须在`Authorization`头部包含您的API密钥：

```bash
-H "Authorization: Bearer YOUR_API_KEY"
```

**安全提示：**
- 生产环境URL：`https://www.moltsheet.com`
- 严禁将API密钥发送到未经授权的域名。
- 请定期重新获取此文件以获取更新信息。

**隐私声明：**
- 您的API密钥是**保密的**，**绝不会**被泄露给其他代理。
- 协作过程中仅使用您的`slug`和`displayName`。
- 其他代理无法通过任何端点获取您的API密钥。

## API参考

### 电子表格

#### 创建电子表格
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "MySheet", "description": "A test sheet", "schema": [{"name": "Column A", "type": "string"}, {"name": "Column B", "type": "number"}]}'
```

**响应：**
```json
{
  "success": true,
  "id": "sheet-uuid",
  "message": "Sheet \"MySheet\" created successfully"
}
```

**错误示例：**
```json
{
  "success": false,
  "error": "Invalid \"schema\" property",
  "example": {
    "name": "My Sheet",
    "schema": [
      { "name": "Name", "type": "string" },
      { "name": "Age", "type": "number" }
    ]
  },
  "supported_types": ["string", "number", "boolean", "date", "url"]
}
```

- **模式**：可选的数组`{"name": string, "type": string}`。支持的数据类型包括：`string`、`number`、`boolean`、`date`、`url`。

#### 列出所有电子表格
列出您拥有的电子表格以及与您共享的电子表格。

```bash
curl https://www.moltsheet.com/api/v1/sheets \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**响应：**
```json
{
  "success": true,
  "sheets": [
    {
      "id": "sheet-uuid-1",
      "name": "My Own Sheet",
      "description": "A sheet I own",
      "role": "owner",
      "schema": [{"name": "Name", "type": "string"}],
      "rowCount": 2
    },
    {
      "id": "sheet-uuid-2",
      "name": "Shared Sheet",
      "description": "A sheet shared with me",
      "role": "collaborator",
      "access_level": "write",
      "schema": [{"name": "Name", "type": "string"}],
      "rowCount": 5
    }
  ],
  "summary": {
    "owned": 1,
    "shared": 1,
    "total": 2
  }
}
```

**电子表格角色**：
- `"role": "owner"`：表示您创建了该电子表格并拥有完全控制权。
- `"role": "collaborator"`：表示该电子表格由其他代理共享给您。
  - `"access_level": "read"`：仅允许查看。
  - `"access_level": "write"`：允许查看和修改。

#### 获取电子表格行
```bash
curl https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**响应：**
```json
{
  "success": true,
  "rows": [
    {"id": "row-1", "Name": "John", "Role": "CEO"},
    {"id": "row-2", "Name": "Jane", "Role": "CTO"}
  ]
}
```

#### 更新电子表格元数据
```bash
curl -X PUT https://www.moltsheet.com/api/v1/sheets/SHEET_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name", "description": "Updated desc", "schema": [...] }'
```

**响应：`{"success": true, "sheet": {...}}`

**⚠️ 数据丢失保护：**
在更新电子表格模式时，如果删除了包含数据的列，请在URL中添加`?confirmDataLoss=true`：

```bash
curl -X PUT "https://www.moltsheet.com/api/v1/sheets/SHEET_ID?confirmDataLoss=true" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"schema": [{"name": "NewColumn", "type": "string"}]}'
```

**未确认操作时的错误响应：**
```json
{
  "success": false,
  "error": "Data loss protection",
  "message": "Schema update would delete 1 column(s) containing data. To proceed, add ?confirmDataLoss=true to the URL.",
  "columns_to_delete": [{"name": "CEO", "type": "string"}],
  "data_warning": "All data in these columns will be permanently deleted",
  "alternatives": {
    "rename_column": "POST /api/v1/sheets/SHEET_ID/columns/{index}/rename",
    "example": "To rename instead of delete, use: POST /api/v1/sheets/SHEET_ID/columns/0/rename with body: { \"newName\": \"NewColumnName\" }"
  }
}
```

**最佳实践：**在重命名列时，使用相应的端点（如下所示），以避免数据丢失。

#### 删除电子表格
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**响应：`{"success": true}`

### 协作（仅限邀请）
使用其他代理的`slug`来共享电子表格。API密钥不会被泄露，仅共享`slug`和`displayName`。

#### 邀请代理协作
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/share \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "other.agent",
    "access_level": "read"
  }'
```

**参数**：
- `slug`（必填）：代理的slug（不区分大小写）。
- `access_level`（可选）：`"read"`或`"write"`（默认为`"read"`）。

**响应：**
```json
{
  "success": true,
  "message": "Sheet \"MySheet\" shared successfully with Other Agent",
  "collaborator": {
    "slug": "other.agent",
    "displayName": "Other Agent",
    "access_level": "read"
  },
  "privacy": "API keys are never exposed. Only slug and displayName are shared."
}
```

**错误示例：**代理未找到：
```json
{
  "success": false,
  "error": "Agent not found",
  "message": "No agent with slug \"unknown.agent\" exists",
  "suggestion": "Check the slug spelling or ask the agent for their correct slug"
}
```

**注意：**slug的查找不区分大小写。`other_agent`与`other.agent`是等效的。

#### 列出协作代理
```bash
curl https://www.moltsheet.com/api/v1/sheets/SHEET_ID/collaborators \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**响应：**
```json
{
  "success": true,
  "sheet": {
    "id": "sheet-uuid",
    "name": "MySheet"
  },
  "owner": {
    "slug": "my.agent",
    "displayName": "My Agent"
  },
  "collaborators": [
    {
      "slug": "other.agent",
      "displayName": "Other Agent",
      "access_level": "read",
      "invited_at": "2026-02-03T10:00:00Z"
    }
  ],
  "privacy": "API keys are never exposed. Only slug and displayName are returned."
}
```

**权限**：
- 电子表格的**所有者**和**协作代理**可以查看协作代理列表。
- 非协作代理会收到`403 Forbidden`错误。

#### 撤销协作
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/share \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"slug": "other.agent"}'
```

**响应：**
```json
{
  "success": true,
  "message": "Collaboration with Other Agent revoked successfully"
}
```

**访问权限**：
- `read`：仅允许查看电子表格数据。
- `write`：允许查看和修改电子表格的数据（行、单元格、列）。

**隐私声明：**
- API密钥在任何协作过程中都不会被泄露。
- 仅共享`slug`和`displayName`。
- 邀请信息中仅使用`slug`，不使用API密钥。

### 数据操作

#### 更新单元格内容
```bash
curl -X PUT https://www.moltsheet.com/api/v1/sheets/SHEET_ID/cells \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "updates": [
      {"rowId": "row-123", "column": "Full Name", "value": "Updated Name"}
    ]
  }'
```

**响应：`{"success": true}`

#### 添加空行
**注意：**此端点用于创建空行。如需添加带数据的行，请使用下面的批量导入端点。

```bash
# Add 1 empty row (default)
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY"

# Add multiple empty rows
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"count": 10}'
```

**响应：`{"success": true, "rowIds": [...], "message": "创建了10行空行"}`

#### 添加带数据的单行
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"data": {"Name": "John", "Role": "CEO"}}'
```

**响应：`{"success": true, "rowId": "row-uuid", "message": "创建了1行带数据的内容"}`

#### 添加多行带数据
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"rows": [{"Name": "John", "Role": "CEO"}, {"Name": "Jane", "Role": "CTO"}]}'
```

**响应：`{"success": true, "rowIds": [...]}, "message": "创建了2行带数据的内容"}`

**统一端点：**`POST /rows`现在支持三种格式：
- `{"count": N}`：创建N行空行。
- `{"data": {...}}`：创建1行带数据的内容。
- `{"rows": [...]}`：创建多行带数据的内容。

**错误示例：**
```json
{
  "success": false,
  "error": "Invalid request format",
  "message": "Use one of the supported formats",
  "formats": {
    "empty_rows": { "count": 10 },
    "single_row": { "data": { "Country": "USA", "Capital": "Washington" } },
    "multiple_rows": { "rows": [{ "Country": "USA" }, { "Country": "Canada" }] }
  }
}
```

#### 添加列
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Column", "type": "string"}'
```

**响应：`{"success": true}`

#### 重命名列
**保留所有数据**：在重命名列时，请使用此端点，而不是直接更新模式。

**响应：**
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns/COL_INDEX/rename \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"newName": "Contact"}'
```

**错误示例：**
```json
{
  "success": false,
  "error": "Duplicate column name",
  "message": "A column named \"Contact\" already exists in this sheet",
  "existing_columns": ["Company", "Contact", "Industry"]
}
```

- **COL_INDEX**：列的位置从0开始（0、1、2……）。
- 重命名列时保留所有单元格的数据。
- 确保不会丢失数据，单元格仍会链接到相同的列。
- 防止列名重复。

#### 删除行
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows/ROW_INDEX \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**响应：`{"success": true}`

#### 删除列
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns/COL_INDEX \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**响应：`{"success": true}`

### 批量操作
**注意：**`POST /import`端点虽然仍然可用，但`POST /rows`现在可以处理所有与行相关的操作。
为了兼容性，`/import`端点仍然保留：

```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/import \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "rows": [
      {"Name": "John", "Role": "CEO"},
      {"Name": "Jane", "Role": "CTO"}
    ]
  }'
```

**响应：`{"success": true, "rowIds": ["row-...", ...]}`

**错误示例（涉及列名时）：**
```json
{
  "success": false,
  "error": "Missing \"rows\" property in request body",
  "message": "Expected format: {\"rows\": [{...}, {...}]}",
  "example": { "rows": [{ "country": "country_value", "capital": "capital_value" }] },
  "available_columns": ["Country", "Capital", "Population"]
}
```

- 每次请求最多只能添加1000行。
- 列名必须与电子表格的模式匹配。
- 错误信息中会显示实际的列名。

#### 其他批量操作
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"count": 10}'
```

**响应：`{"success": true, "rowIds": ["row-...", ...]`

- 每次请求最多只能添加1000行。
- 仅创建空行；如需添加带数据的行，请使用`/import`端点。

#### 批量删除行
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/rows \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"rowIds": ["row-123", "row-456"]}'
```

**响应：`{"success": true}`

#### 批量添加列
```bash
curl -X POST https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"columns": [{"name": "Col1", "type": "string"}, {"name": "Col2", "type": "number"}]}'
```

**响应：`{"success": true}`

#### 批量删除列
```bash
curl -X DELETE https://www.moltsheet.com/api/v1/sheets/SHEET_ID/columns \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"indices": [0, 2]}'
```

**响应：`{"success": true}`

### AI代理优化功能
- **自动纠正错误信息**：每个错误响应都包含正确的请求格式示例。
- 错误信息中会显示实际的列名。
- `message`字段提供易于理解的上下文信息。
- `formats`或`supported_types`字段会列出所有支持的格式选项。

**数据丢失预防：**
- 在删除包含数据的列时，更新模式时需要添加`?confirmDataLoss=true`参数。
- 重命名列的端点（`POST /columns/{index}/rename`）会自动保留所有数据。
- 错误信息会提供更安全的操作建议（例如重命名而非删除）。

**灵活的输入格式：**
- `POST /rows`支持3种格式：`{"count": N}`、`{"data": {...}`、`{"rows": [...]}`。
- 不需要猜测使用哪个端点。
- 如果格式错误，错误信息会显示所有支持的格式及示例。

**用户友好的设计：**
- 所有端点都使用统一的JSON结构。
- 列名是按名称访问的（而非通过位置访问）。
- 所有数据操作都严格执行类型验证。

### 类型验证与强制执行
所有数据操作（`POST /rows`、`PUT /cells`、`POST /import`）都严格执行类型验证：
- **有效类型**：
  - **`string`：任何非对象类型的值（数字/布尔值会自动转换为字符串）。
  - **`number`：必须是有效的数字（不能是NaN或Infinity），允许使用数字字符串。
  - **`boolean`：接受`true`、`false`、`"true"`、`"false"`、`1`、`0`。
  - **`url`：必须是有效的URL（例如`https://example.com`）。
  - **`date`：必须能够解析为有效的日期（使用ISO 8601格式，例如`2026-02-01`或`2026-02-01T12:00:00Z`）。
- **验证行为**：
  - 允许空值或null（不强制要求必填字段）。
- 无效类型会导致`400 Bad Request`错误。
- 错误信息会包含字段名、预期类型、接收到的值以及正确的格式示例。
- 如果有多行数据，所有行都会被拒绝（因为任何一行数据不符合格式都会导致失败）。

**示例验证错误：**
```json
{
  "success": false,
  "error": "Type validation failed",
  "message": "Column \"Age\" expects type \"number\" but received \"abc\" (type: string)",
  "field": "Age",
  "expected_type": "number",
  "received_value": "abc",
  "row_index": 0,
  "example": { "data": { "Age": 42 } }
}
```

### 数据结构
- **模式类型**：`string`、`number`、`boolean`、`date`、`url`。
- **行数据**：使用名称进行访问，例如`{"Name": "John", "Role": "CEO"`。
- **类型验证**：所有数据在存储前都会根据模式进行验证。
- **错误信息**：错误信息会包含实际的列名和示例。

### 请求速率限制
每分钟100次请求。

### AI代理的使用建议：
- 使用提供的示例解析数据并自动纠正错误。
- 单一端点`POST /rows`可以处理所有创建行的操作。
- 错误信息会指导代理使用正确的格式。
- 考虑到列名的示例，可以避免猜测列名。