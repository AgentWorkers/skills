---
name: nocodb
description: 通过 REST API 访问和管理 NocoDB 数据库。免费计划支持数据库、表、字段、记录、链接、过滤器、排序和附件等功能。企业级计划还提供了工作区、视图、脚本、团队以及协作功能。
metadata:
  openclaw:
    requires:
      env:
        - NOCODB_TOKEN
        - NOCODB_URL
        - NOCODB_VERBOSE
      bins:
        - curl
        - jq
    primaryEnv: NOCODB_TOKEN
---

# NocoDB CLI

NocoDB CLI 是用于操作 NocoDB API 的命令行工具。

## 平台支持

- **Linux / macOS**: `scripts/nocodb.sh`（基于 Bash，需要 `curl` 和 `jq` 工具）

## 计划类型

**免费计划 (Free Plans):** 提供基础 (Base)、表 (Table)、字段 (Field)、记录 (Record)、链接 (Link)、附件 (Attachment) 等 API 功能，以及过滤 (Filter) 和排序 (Sort) 相关 API。

**企业级计划 (Enterprise Plans) (自托管或云托管):** 还提供工作空间 (Workspace)、工作空间协作 (Workspace Collaboration)、基础协作 (Base Collaboration)、视图 (View)、脚本 (Script)、团队 (Team) 等 API 功能，以及 API 令牌 (API Token) 相关服务。

## 设置

```bash
export NOCODB_TOKEN="your-api-token"
export NOCODB_URL="https://app.nocodb.com"  # optional, this is default
export NOCODB_VERBOSE=1                      # optional, shows resolved IDs
```

获取您的 API 令牌：登录 NocoDB → 进入“团队与设置”（Team & Settings）→ 选择“API 令牌”（API Tokens）→ 点击“添加新令牌”（Add New Token）。

## 参数顺序

命令的执行遵循一定的层次结构，参数的顺序始终如下：

```
WORKSPACE → BASE → TABLE → VIEW/FIELD → RECORD
```

您可以使用**名称**（human-readable）或**ID**（ID）来调用 API。  
**ID 前缀说明：**  
`w` = 工作空间 (workspace)  
`p` = 基础数据表 (base)  
`m` = 表 (table)  
`c` = 列 (column)  
`vw` = 视图 (view)  

示例：  
- 使用名称：`nc record:list MyBase Users`  
- 使用 ID：`nc record:list pdef5678uvw mghi9012rst`  

若需查看解析后的 ID，可以设置 `NOCODB_VERBOSE=1`：  
```bash
NOCODB_VERBOSE=1 nc field:list MyBase Users
# → base: MyBase → pdef5678uvw
# → table: Users → mghi9012rst
```

## 快速参考

```bash
# Workspace APIs (Enterprise only)
nc workspace:list                                   # → wabc1234xyz

# Free plan APIs
nc base:list wabc1234xyz                            # → pdef5678uvw
nc table:list pdef5678uvw                           # → mghi9012rst
nc field:list pdef5678uvw mghi9012rst               # → cjkl3456opq
nc record:list pdef5678uvw mghi9012rst
nc record:get pdef5678uvw mghi9012rst 31
nc filter:list pdef5678uvw mghi9012rst vwmno7890abc

# View APIs (Enterprise only: self-hosted or cloud-hosted)
nc view:list pdef5678uvw mghi9012rst                # → vwmno7890abc

# Filter syntax help
nc where:help
```

## 命令列表

### 工作空间 (Workspaces)

**注意：** 工作空间 API 和工作空间协作 API 仅支持企业级自托管计划（Enterprise self-hosted plans）和云托管企业级计划（cloud-hosted Enterprise plans）。

```bash
nc workspace:list                         # → wabc1234xyz
nc workspace:get wabc1234xyz
nc workspace:create '{"title":"New Workspace"}'
nc workspace:update wabc1234xyz '{"title":"Renamed"}'
nc workspace:delete wabc1234xyz
nc workspace:members wabc1234xyz
nc workspace:members:add wabc1234xyz '{"email":"user@example.com","roles":"workspace-creator"}'
nc workspace:members:update wabc1234xyz '{"email":"user@example.com","roles":"workspace-viewer"}'
nc workspace:members:remove wabc1234xyz '{"email":"user@example.com"}'
```

### 基础数据表 (Bases)

```bash
nc base:list wabc1234xyz                  # → pdef5678uvw
nc base:get pdef5678uvw
nc base:create wabc1234xyz '{"title":"New Base"}'
nc base:update pdef5678uvw '{"title":"Renamed"}'
nc base:delete pdef5678uvw
```

**基础数据表协作功能（仅限企业级计划）**

```bash
nc base:members pdef5678uvw
nc base:members:add pdef5678uvw '{"email":"user@example.com","roles":"base-editor"}'
nc base:members:update pdef5678uvw '{"email":"user@example.com","roles":"base-viewer"}'
nc base:members:remove pdef5678uvw '{"email":"user@example.com"}'
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

字段类型包括：  
SingleLineText、LongText、Number、Decimal、Currency、Percent、Email、URL、PhoneNumber、Date、DateTime、Time、SingleSelect、MultiSelect、Checkbox、Rating、Attachment、Links、User、JSON 等。

### 视图 (Views)

**注意：** 视图 API 仅支持自托管企业和云托管企业级计划。

```bash
nc view:list pdef5678uvw mghi9012rst      # → vwmno7890abc
nc view:get pdef5678uvw mghi9012rst vwmno7890abc
nc view:create pdef5678uvw mghi9012rst '{"title":"Active Users","type":"grid"}'
nc view:update pdef5678uvw mghi9012rst vwmno7890abc '{"title":"Renamed"}'
nc view:delete pdef5678uvw mghi9012rst vwmno7890abc
```

视图类型包括：grid（网格视图）、gallery（画廊视图）、kanban（看板视图）、calendar（日历视图）。

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

### 关联记录 (Linked Records)

```bash
nc link:list pdef5678uvw mghi9012rst cjkl3456opq 31
nc link:add pdef5678uvw mghi9012rst cjkl3456opq 31 '[{"id":42}]'
nc link:remove pdef5678uvw mghi9012rst cjkl3456opq 31 '[{"id":42}]'
```

### 过滤与排序（针对视图级别） (Filters & Sorts, View-level)

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

**注意：** 脚本 API 仅支持自托管企业和云托管企业级计划。

```bash
nc script:list pdef5678uvw
nc script:create pdef5678uvw '{"title":"My Script"}'
```

### 团队 (Teams)

**注意：** 团队相关 API 仅适用于企业级计划（Enterprise plans）。

```bash
nc team:list wabc1234xyz
nc team:create wabc1234xyz '{"title":"Engineering"}'
```

### API 令牌 (API Tokens)

**注意：** API 令牌相关服务仅支持自托管企业和云托管企业级计划。

```bash
nc token:list
nc token:create '{"title":"CI Token"}'
nc token:delete tkn1a2b3c4d5e6f7g
```

## 过滤语法

运行 `nc where:help` 可以查看完整的过滤语法说明。

### 基本语法

```
(field,operator,value)
(field,operator)                    # for null/blank/checked operators
(field,operator,sub_op)             # for date operators
(field,operator,sub_op,value)       # for date with value
```

### 常用操作符 (Common Operators)

| 操作符 | 描述 | 示例 |
|----------|-------------|---------|
| eq     | 等于       | `(name,eq,John)` |
| neq     | 不等于      | `(status,neq,archived)` |
| like     | 包含（通配符）   | `(name,like,%john%)` |
| in      | 在列表中     | `(status,in,active,pending)` |
| gt, lt, gte, lte | 数值比较    | `(price,gt,100)` |
| blank, notblank | 是否为空     | `(notes,blank)` |
| checked, notchecked | 布尔值      | `(is_active,checked)` |

### 日期操作符 (Date Operators)

```bash
(created_at,eq,today)
(created_at,isWithin,pastWeek)
(created_at,isWithin,pastNumberOfDays,14)
(due_date,lt,today)                          # overdue
(event_date,eq,exactDate,2024-06-15)
```

### 组合过滤条件

**重要提示：** 使用 `~and`、`~or`、`~not`（以波浪号 `~` 作为前缀）来组合过滤条件。

```bash
(name,eq,John)~and(age,gte,18)
(status,eq,active)~or(status,eq,pending)
~not(is_deleted,checked)
(status,in,active,pending)~and(country,eq,USA)
```

### 复杂示例

```bash
# Active users created this month
"(status,eq,active)~and(created_at,isWithin,pastMonth)"

# Overdue high-priority tasks
"(due_date,lt,today)~and(priority,eq,high)~and(completed,notchecked)"

# Orders $100-$500 in pending/processing
"(amount,gte,100)~and(amount,lte,500)~and(status,in,pending,processing)"
```