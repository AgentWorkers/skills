---
name: nocodb
description: 通过 v3 REST API 访问和管理 NocoDB 数据库。该 API 可用于管理工作区、数据库、表、字段、视图、记录等对象。支持过滤、排序、分页、关联记录、附件管理以及团队协作功能。
---

# NocoDB v3 命令行界面 (CLI)

这是一个功能齐全的 NocoDB v3 API 命令行界面。

## 设置

```bash
export NOCODB_TOKEN="your-api-token"
export NOCODB_URL="https://app.nocodb.com"  # optional, this is default
export NOCODB_VERBOSE=1                      # optional, shows resolved IDs
```

获取您的 API 令牌：登录 NocoDB → 点击“团队与设置” → “API 令牌” → “添加新令牌”。

## 参数顺序

命令遵循层次结构。参数的顺序始终如下：

```
WORKSPACE → BASE → TABLE → VIEW/FIELD → RECORD
```

您可以使用 **名称**（便于人类阅读）或 **ID**（更快捷，直接从 NocoDB 获取）。

**ID 前缀：**  
`w` = 工作区 (workspace)  
`p` = 基础数据库 (base)  
`m` = 表 (table)  
`c` = 列 (column)  
`vw` = 视图 (view)  

示例：  
- 名称：`nc record:list MyBase Users`  
- ID：`nc record:list pdef5678uvw mghi9012rst`  

将 `NOCODB_VERBOSE=1` 设置为 1 可以查看解析后的 ID：  
```bash
NOCODB_VERBOSE=1 nc field:list MyBase Users
# → base: MyBase → pdef5678uvw
# → table: Users → mghi9012rst
```

## 快速参考

```bash
nc workspace:list                                   # → wabc1234xyz
nc base:list wabc1234xyz                            # → pdef5678uvw
nc table:list pdef5678uvw                           # → mghi9012rst
nc field:list pdef5678uvw mghi9012rst               # → cjkl3456opq
nc view:list pdef5678uvw mghi9012rst                # → vwmno7890abc
nc record:list pdef5678uvw mghi9012rst
nc record:get pdef5678uvw mghi9012rst 31
nc filter:list pdef5678uvw mghi9012rst vwmno7890abc
nc where:help
```

## 命令

### 工作区 (Workspaces)

```bash
nc workspace:list                         # → wabc1234xyz
nc workspace:get wabc1234xyz
nc workspace:create '{"title":"New Workspace"}'
nc workspace:update wabc1234xyz '{"title":"Renamed"}'
nc workspace:delete wabc1234xyz
nc workspace:members wabc1234xyz
```

### 基础数据库 (Bases)

```bash
nc base:list wabc1234xyz                  # → pdef5678uvw
nc base:get pdef5678uvw
nc base:create wabc1234xyz '{"title":"New Base"}'
nc base:update pdef5678uvw '{"title":"Renamed"}'
nc base:delete pdef5678uvw
```

### 表 (Tables)

```bash
nc table:list pdef5678uvw                 # → mghi9012rst
nc table:get pdef5678uvw mghi9012rst
nc table:create pdef5678uvw '{"title":"NewTable"}'
nc table:update pdef5678uvw mghi9012rst '{"title":"Customers"}'
nc table:delete pdef5678uvw mghi9012rst
```

### 字段 (Fields)

```bash
nc field:list pdef5678uvw mghi9012rst     # → cjkl3456opq
nc field:get pdef5678uvw mghi9012rst cjkl3456opq
nc field:create pdef5678uvw mghi9012rst '{"title":"Phone","type":"PhoneNumber"}'
nc field:update pdef5678uvw mghi9012rst cjkl3456opq '{"title":"Mobile"}'
nc field:delete pdef5678uvw mghi9012rst cjkl3456opq
```

字段类型：  
SingleLineText（单行文本）、LongText（长文本）、Number（数字）、Decimal（小数）、Currency（货币）、Percent（百分比）、Email（电子邮件）、URL（网址）、PhoneNumber（电话号码）、Date（日期）、DateTime（日期时间）、Time（时间）、SingleSelect（单选）、MultiSelect（多选）、Checkbox（复选框）、Rating（评分）、Attachment（附件）、Links（链接）、User（用户）、JSON（JSON 数据）等。

### 视图 (Views)

```bash
nc view:list pdef5678uvw mghi9012rst      # → vwmno7890abc
nc view:get pdef5678uvw mghi9012rst vwmno7890abc
nc view:create pdef5678uvw mghi9012rst '{"title":"Active Users","type":"grid"}'
nc view:update pdef5678uvw mghi9012rst vwmno7890abc '{"title":"Renamed"}'
nc view:delete pdef5678uvw mghi9012rst vwmno7890abc
```

视图类型：grid（网格）、gallery（画廊）、kanban（看板）、calendar（日历）。

### 记录 (Records)

```bash
nc record:list pdef5678uvw mghi9012rst                # page 1, 25 records
nc record:list pdef5678uvw mghi9012rst 2 50           # page 2, 50 records
nc record:list pdef5678uvw mghi9012rst 1 25 "(status,eq,active)"
nc record:list pdef5678uvw mghi9012rst 1 25 "" '[{"field":"cjkl3456opq","direction":"desc"}]'

nc record:get pdef5678uvw mghi9012rst 31
nc record:get pdef5678uvw mghi9012rst 31 "name,email"

nc record:create pdef5678uvw mghi9012rst '{"fields":{"name":"Alice"}}'
nc record:update pdef5678uvw mghi9012rst 31 '{"status":"active"}'
nc record:update-many pdef5678uvw mghi9012rst '[{"id":31,"fields":{"status":"done"}}]'

nc record:delete pdef5678uvw mghi9012rst 31
nc record:delete pdef5678uvw mghi9012rst '[31,32]'

nc record:count pdef5678uvw mghi9012rst
nc record:count pdef5678uvw mghi9012rst "(status,eq,active)"
```

### 相关联的记录 (Linked Records)

```bash
nc link:list pdef5678uvw mghi9012rst cjkl3456opq 31
nc link:add pdef5678uvw mghi9012rst cjkl3456opq 31 '[{"id":42}]'
nc link:remove pdef5678uvw mghi9012rst cjkl3456opq 31 '[{"id":42}]'
```

### 过滤与排序（视图级别） (Filters & Sorts, View-level)

```bash
nc filter:list pdef5678uvw mghi9012rst vwmno7890abc
nc filter:create pdef5678uvw mghi9012rst vwmno7890abc '{"field_id":"cjkl3456opq","operator":"eq","value":"active"}'
nc sort:list pdef5678uvw mghi9012rst vwmno7890abc
nc sort:create pdef5678uvw mghi9012rst vwmno7890abc '{"field_id":"cjkl3456opq","direction":"desc"}'
```

### 附件 (Attachments)

```bash
nc attachment:upload pdef5678uvw mghi9012rst 31 cjkl3456opq ./report.pdf
```

### 脚本 (Scripts)

```bash
nc script:list pdef5678uvw
nc script:create pdef5678uvw '{"title":"My Script"}'
```

### 团队 (Teams)

```bash
nc team:list wabc1234xyz
nc team:create wabc1234xyz '{"title":"Engineering"}'
```

### API 令牌 (API Tokens)

```bash
nc token:list
nc token:create '{"title":"CI Token"}'
nc token:delete tkn1a2b3c4d5e6f7g
```

## `where` 过滤语法

运行 `nc where:help` 可以查看完整文档。

### 基本语法

```
(field,operator,value)
(field,operator)                    # for null/blank/checked operators
(field,operator,sub_op)             # for date operators
(field,operator,sub_op,value)       # for date with value
```

### 常用运算符 (Common Operators)

| 运算符 | 描述 | 示例 |
|----------|-------------|---------|
| eq     | 等于       | `(name, eq, John)` |
| neq     | 不等于      | `(status, neq, archived)` |
| like     | 包含（通配符）   | `(name, like, %john%)` |
| in      | 在列表中     | `(status, in, active, pending)` |
| gt       | 大于       | `(price, gt, 100)` |
| lt       | 小于       | `(price, lt, 100)` |
| gte      | 大于或等于   | `(price, gte, 100)` |
| lte      | 小于或等于   | `(price, lte, 100)` |
| blank     | 空         | `(notes, blank)` |
| notblank | 非空       | `(notes, notblank)` |
| checked   | 已选中     | `(is_active, checked)` |

### 日期运算符 (Date Operators)

```bash
(created_at,eq,today)
(created_at,isWithin,pastWeek)
(created_at,isWithin,pastNumberOfDays,14)
(due_date,lt,today)                          # overdue
(event_date,eq,exactDate,2024-06-15)
```

### 组合过滤 (Combining Filters)

**重要提示：** 使用 `~and`、`~or`、`~not`（前缀为波浪号 `~`）进行组合过滤。

```bash
(name,eq,John)~and(age,gte,18)
(status,eq,active)~or(status,eq,pending)
~not(is_deleted,checked)
(status,in,active,pending)~and(country,eq,USA)
```

### 复杂示例 (Complex Examples)

```bash
# Active users created this month
"(status,eq,active)~and(created_at,isWithin,pastMonth)"

# Overdue high-priority tasks
"(due_date,lt,today)~and(priority,eq,high)~and(completed,notchecked)"

# Orders $100-$500 in pending/processing
"(amount,gte,100)~and(amount,lte,500)~and(status,in,pending,processing)"
```