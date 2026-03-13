---
name: nocodb
description: 通过 REST API v3 连接到 NocoDB 数据库。可以查询记录、管理数据库结构（表、字段、视图）、处理关联记录、应用过滤器、进行排序以及操作附件。适用于使用 NocoDB（一个开源的 Airtable 替代品）来读取或操作数据、创建或更新记录、管理数据库模式或上传文件的场景。
license: AGPL-3.0
metadata:
  openclaw:
    requires:
      env:
        - NOCODB_TOKEN
        - NOCODB_URL
      bins:
        - curl
        - jq
    primaryEnv: NOCODB_TOKEN
---
# NocoDB 技能

这是一个用于 NocoDB API v3 的命令行（CLI）封装工具，支持 NocoDB Cloud（app.nocodb.com）和自托管实例。

NocoDB 是一个开源的 Airtable 替代品，它可以将任何数据库转换为智能电子表格。该技能提供了对 NocoDB REST API 的完整访问权限，用于管理工作区、数据库、表格、记录等。

## 设置

### 所需环境变量

```bash
export NOCODB_TOKEN="your-api-token"  # Required - API authentication token
export NOCODB_URL="https://app.nocodb.com"  # Optional - defaults to cloud
```

### 获取 API 令牌

1. 打开 NocoDB 仪表板
2. 转到 **团队与设置** → **API 令牌**
3. 点击 **添加新令牌**
4. 复制令牌并将其设置为 `NOCODB_TOKEN`

### 验证

测试您的连接：
```bash
nc workspace:list
```

## 快速入门

```bash
# List all workspaces
nc workspace:list

# List bases in a workspace
nc base:list <workspace-name-or-id>

# List tables in a base
nc table:list <base-name-or-id>

# Query records
nc record:list <base> <table>

# Create a record
nc record:create <base> <table> '{"fields":{"Name":"Alice"}}'
```

## 使用方法

该技能提供了 `nc` 命令，该命令具有层次化的结构：

```
WORKSPACE → BASE → TABLE → VIEW/FIELD → RECORD
```

### 标识符格式

您可以使用 **名称**（人类可读）或 **ID**（性能更快）：

| 资源 | ID 前缀 | 示例 |
|----------|-----------|---------|
| 工作区 | `w` | `wabc123xyz` |
| 数据库 | `p` | `pdef456uvw` |
| 表格 | `m` | `mghi789rst` |
| 字段 | `c` | `cjkl012opq` |
| 视图 | `vw` | `vwmno345abc` |

**提示：** 直接使用 ID 可以提高性能。将 `NOCODB_VERBOSE=1` 设置为 `true` 可以查看 ID 的解析过程。

## 命令

### 工作区

**注意：** 工作区 API 需要企业计划（自托管或云托管）。

```bash
nc workspace:list
nc workspace:get <workspace>
nc workspace:create '{"title":"New Workspace"}'
nc workspace:update <workspace> '{"title":"Renamed"}'
nc workspace:delete <workspace>
```

**工作区协作（企业版）：**
```bash
nc workspace:members <workspace>
nc workspace:members:add <workspace> '{"email":"user@example.com","roles":"workspace-creator"}'
nc workspace:members:update <workspace> '{"email":"user@example.com","roles":"workspace-viewer"}'
nc workspace:members:remove <workspace> '{"email":"user@example.com"}'
```

### 数据库

```bash
nc base:list <workspace>
nc base:get <base>
nc base:create <workspace> '{"title":"New Base"}'
nc base:update <base> '{"title":"Renamed"}'
nc base:delete <base>
```

**数据库协作（企业版）：**
```bash
nc base:members <base>
nc base:members:add <base> '{"email":"user@example.com","roles":"base-editor"}'
nc base:members:update <base> '{"email":"user@example.com","roles":"base-viewer"}'
nc base:members:remove <base> '{"email":"user@example.com"}'
```

### 表格

```bash
nc table:list <base>
nc table:get <base> <table>
nc table:create <base> '{"title":"New Table"}'
nc table:update <base> <table> '{"title":"Renamed"}'
nc table:delete <base> <table>
```

### 字段

```bash
nc field:list <base> <table>
nc field:get <base> <table> <field>
nc field:create <base> <table> '{"title":"Email","type":"Email"}'
nc field:update <base> <table> <field> '{"title":"Contact Email"}'
nc field:delete <base> <table> <field>
```

**字段类型：**
- `SingleLineText`、`LongText`、`Number`、`Decimal`、`Currency`、`Percent`
- `Email`、`URL`、`PhoneNumber`
- `Date`、`DateTime`、`Time`
- `SingleSelect`、`MultiSelect`
- `Checkbox`、`Rating`
- `Attachment`、`Links`、`User`、`JSON`

### 视图

**注意：** 视图 API 需要企业计划。

```bash
nc view:list <base> <table>
nc view:get <base> <table> <view>
nc view:create <base> <table> '{"title":"Active Users","type":"grid"}'
nc view:update <base> <table> <view> '{"title":"Renamed"}'
nc view:delete <base> <table> <view>
```

**视图类型：`grid`、`gallery`、`kanban`、`calendar`、`form`

### 记录

```bash
# List records (pagination)
nc record:list <base> <table> [page] [pageSize] [where] [sort] [fields] [viewId]

# Get single record
nc record:get <base> <table> <recordId> [fields]

# Create record
nc record:create <base> <table> '{"fields":{"Name":"Alice","Email":"alice@example.com"}}'

# Update record
nc record:update <base> <table> <recordId> '{"Status":"active"}'

# Update multiple records
nc record:update-many <base> <table> '[{"id":1,"fields":{"Status":"done"}}]'

# Delete record
nc record:delete <base> <table> <recordId>

# Delete multiple records
nc record:delete <base> <table> '[1,2,3]'

# Count records
nc record:count <base> <table> [where] [viewId]
```

**分页参数：**
- `page`：页码（默认：1）
- `pageSize`：每页记录数（默认：25）
- `where`：过滤表达式（参见过滤语法）
- `sort`：排序表达式（参见排序语法）
- `fields`：需要返回的字段名称（用逗号分隔）
- `viewId`：按视图进行过滤

### 关联记录

```bash
# List linked records
nc link:list <base> <table> <linkField> <recordId> [page] [pageSize] [where] [sort] [fields]

# Add links
nc link:add <base> <table> <linkField> <recordId> '[{"id":42}]'

# Remove links
nc link:remove <base> <table> <linkField> <recordId> '[{"id":42}]'
```

### 过滤与排序

**视图级别的过滤：**
```bash
nc filter:list <base> <table> <view>
nc filter:create <base> <table> <view> '{"field_id":"field123","operator":"eq","value":"active"}'
nc filter:replace <base> <table> <view> '<json>'
nc filter:update <base> <filterId> '<json>'
nc filter:delete <base> <filterId>
```

**视图级别的排序：**
```bash
nc sort:list <base> <table> <view>
nc sort:create <base> <table> <view> '{"field_id":"field123","direction":"desc"}'
nc sort:update <base> <sortId> '<json>'
nc sort:delete <base> <sortId>
```

### 附件

```bash
nc attachment:upload <base> <table> <recordId> <field> <filepath>
```

### 脚本（企业版）

```bash
nc script:list <base>
nc script:get <base> <scriptId>
nc script:create <base> '{"title":"My Script"}'
nc script:update <base> <scriptId> '<json>'
nc script:delete <base> <scriptId>
```

### 团队（企业版）

```bash
nc team:list <workspace>
nc team:get <workspace> <teamId>
nc team:create <workspace> '{"title":"Engineering"}'
nc team:update <workspace> <teamId> '<json>'
nc team:delete <workspace> <teamId>
nc team:members:add <workspace> <teamId> '<json>'
nc team:members:update <workspace> <teamId> '<json>'
nc team:members:remove <workspace> <teamId> '<json>'
```

### API 令牌（企业版）

```bash
nc token:list
nc token:create '{"title":"CI Token"}'
nc token:delete <tokenId>
```

## 过滤语法

### 基本语法

```
(field,operator,value)
```

### 运算符

| 运算符 | 描述 | 示例 |
|----------|-------------|---------|
| `eq` | 等于 | `(name,eq,John)` |
| `neq` | 不等于 | `(status,neq,archived)` |
| `like` | 包含（% 通配符） | `(name,like,%john%)` |
| `nlike` | 不包含 | `(name,nlike,%test%)` |
| `in` | 在列表中 | `(status,in,active,pending)` |
| `gt` | 大于 | `(price,gt,100)` |
| `lt` | 小于 | `(stock,lt,10)` |
| `gte` | 大于或等于 | `(rating,gte,4)` |
| `lte` | 小于或等于 | `(age,lte,65)` |
| `blank` | 为空 | `(notes,blank)` |
| `notblank` | 不为空 | `(email,notblank)` |
| `null` | 为 null | `(deleted_at,null)` |
| `notnull` | 不为 null | `(created_by,notnull)` |
| `checked` | 被选中/为 true | `(is_active,checked)` |
| `notchecked` | 未被选中/为 false | `(is_archived,notchecked)` |

### 逻辑运算符

**重要提示：** 使用波浪号前缀（`~and`、`~or`、`~not`）

```bash
# AND
(name,eq,John)~and(age,gte,18)

# OR
(status,eq,active)~or(status,eq,pending)

# NOT
~not(is_deleted,checked)

# Complex
(status,in,active,pending)~and(country,eq,USA)
```

### 日期过滤

```bash
# Today
(created_at,eq,today)

# Past week
(created_at,isWithin,pastWeek)

# Last 14 days
(created_at,isWithin,pastNumberOfDays,14)

# Exact date
(event_date,eq,exactDate,2024-06-15)

# Overdue
(due_date,lt,today)
```

### 复杂示例

```bash
# Active users created this month
"(status,eq,active)~and(created_at,isWithin,pastMonth)"

# Overdue high-priority tasks
"(due_date,lt,today)~and(priority,eq,high)~and(completed,notchecked)"

# Orders $100-$500 in pending/processing
"(amount,gte,100)~and(amount,lte,500)~and(status,in,pending,processing)"

# Recently updated, not archived
"(updated_at,isWithin,pastNumberOfDays,14)~and~not(is_archived,checked)"
```

## 排序语法

```bash
# Single field ascending (default)
'[{"field":"name"}]'

# Single field descending
'[{"field":"created_at","direction":"desc"}]'

# Multiple fields
'[{"field":"status"},{"field":"created_at","direction":"desc"}]'
```

## 计划要求

**免费计划：** 支持数据库、表格、字段、记录、链接、附件、过滤和排序 API

**企业计划（自托管或云托管）：**
- 工作区和工作区协作 API
- 视图 API
- 脚本 API
- 团队 API
- API 令牌 API
- 数据库协作 API

## 示例

### 基本查询

```bash
# List all records in a table
nc record:list MyBase Users

# Get specific record
nc record:get MyBase Users 42

# Paginated query
nc record:list MyBase Users 1 50

# Query with fields selection
nc record:list MyBase Users 1 25 "" "" "name,email,phone"
```

### 过滤

```bash
# Simple filter
nc record:list MyBase Users 1 25 "(status,eq,active)"

# Like search
nc record:list MyBase Users 1 25 "(name,like,%john%)"

# Combined filters
nc record:list MyBase Users 1 25 "(status,eq,active)~and(age,gte,18)"

# Date filter
nc record:list MyBase Tasks 1 25 "(due_date,lt,today)"
```

### 排序

```bash
# Sort by name ascending
nc record:list MyBase Users 1 25 "" '[{"field":"name"}]'

# Sort by date descending
nc record:list MyBase Users 1 25 "" '[{"field":"created_at","direction":"desc"}]'

# Multiple sorts
nc record:list MyBase Users 1 25 "" '[{"field":"status"},{"field":"name"}]'
```

### 创建数据

```bash
# Create single record
nc record:create MyBase Users '{"fields":{"name":"Alice","email":"alice@example.com","status":"active"}}'

# Create with number fields
nc record:create MyBase Products '{"fields":{"name":"Widget","price":29.99,"quantity":100}}'
```

### 更新数据

```bash
# Update single field
nc record:update MyBase Users 42 '{"status":"inactive"}'

# Update multiple fields
nc record:update MyBase Users 42 '{"status":"active","last_login":"2024-01-15"}'

# Update multiple records
nc record:update-many MyBase Users '[{"id":1,"fields":{"status":"done"}},{"id":2,"fields":{"status":"done"}}]'
```

### 处理关联记录

```bash
# List linked records
nc link:list MyBase Orders order_items 123

# Add link
nc link:add MyBase Orders order_items 123 '[{"id":456}]'

# Remove link
nc link:remove MyBase Orders order_items 123 '[{"id":456}]'
```

### 使用视图

```bash
# List records through a view
nc record:list MyBase Users 1 25 "" "" "" view123

# Count records in a view
nc record:count MyBase Users "" view123
```

### 上传文件

```bash
nc attachment:upload MyBase Documents 42 file_field ./report.pdf
```

## 故障排除

### 连接问题

```bash
# Check environment variables
echo $NOCODB_TOKEN
echo $NOCODB_URL

# Test connection
nc workspace:list
```

### 详细输出模式

启用详细输出以查看解析后的 ID：

```bash
export NOCODB_VERBOSE=1
nc field:list MyBase Users
# Output: → base: MyBase → pdef5678uvw
#         → table: Users → mghi9012rst
```

### 常见错误

| 错误 | 解决方案 |
|-------|----------|
| `需要 NOCBD_TOKEN` | 设置环境变量 |
| 未找到工作区 | 检查工作区名称或使用 ID |
| 未找到数据库 | 检查数据库名称或使用 ID |
| 未找到表格 | 检查表格名称或使用 ID |
| 401 未经授权 | 检查您的 API 令牌 |

## 帮助

显示完整的命令参考：

```bash
nc
```

显示过滤语法帮助：

```bash
nc where:help
```

## 资源

- **NocoDB 文档：** https://docs.nocodb.com/
- **API 参考：** https://docs.nocodb.com/developer-resources/rest-APIs/
- **GitHub：** https://github.com/nocodb/nocodb

## 许可证

该技能封装了 NocoDB API。NocoDB 是基于 AGPL-3.0 许可证的开源项目。