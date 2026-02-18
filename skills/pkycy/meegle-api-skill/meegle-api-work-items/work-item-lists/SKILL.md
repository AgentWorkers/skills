---
name: meegle-api-work-item-lists
description: >
  Meegle OpenAPI 用于列出、搜索和查询工作项。  
  支持单空格过滤、跨空格过滤、复杂搜索、全文搜索，以及关联工作项的查询功能。
metadata:
  openclaw: {}
---
# Meegle API — 工作项列表与搜索

用于在 Meegle 空间中列出、过滤、搜索和查询工作项。这些均为只读 API。

---

## 获取工作项列表（单空间）

根据指定空间（project_key）内的条件查询工作项列表。排除已终止的工作项。此 API 仅用于读取数据，适用于数据检索、分析和汇总。

### 使用场景

- 当需要按名称、分配者、状态、类型、日期等条件过滤工作项时。
- 在单个空间内构建仪表板、报告或搜索结果时。
- 与需要工作项列表的外部工具集成时。

### API 规范：work_item_list_single_space

```yaml
name: meegle.work_item.list.single_space
type: action
description: |
  Query work item list by conditions within a specified space (project_key).
  Excludes terminated items. Read-only API, suitable for retrieval / analysis / aggregation.

context:
  project_key:
    type: string
    required: true
    description: |
      Space unique identifier.
      How to obtain:
      1. Double-click the Meegle space name
      2. simple_name in the space URL

auth:
  operation_type: read
  token_strategy:
    - plugin_access_token + X-User-Key
    - user_access_token (optional, if already available)

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/filter
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  work_item_name:
    type: string
    required: false
    description: Work item name (fuzzy match)

  user_keys:
    type: array
    items: string
    required: false
    constraints:
      max_items: 10
    description: |
      List of user user_keys.
      Used to match creator / watcher / role member.
      How to obtain: Double-click user avatar

  work_item_ids:
    type: array
    items: number
    required: false
    description: |
      List of work item IDs.
      How to obtain: Work item top-right ··· → ID

  work_item_type_keys:
    type: array
    items: string
    required: false
    description: |
      Work item type keys.
      How to obtain: Get Work Item Types in Space

  created_at:
    type: object
    required: false
    schema:
      start: number
      end: number
    description: |
      Created-at time range (millisecond timestamp).
      end can be omitted to mean "until now"

  updated_at:
    type: object
    required: false
    schema:
      start: number
      end: number
    description: |
      Updated-at time range (millisecond timestamp)

  work_item_status:
    type: array
    required: false
    description: |
      Status filter (WorkItemStatus structure).
      How to obtain: Get field information → work_item_status.options

  businesses:
    type: array
    items: string
    required: false
    description: Business line list

  priorities:
    type: array
    items: string
    required: false
    description: |
      Priorities.
      Source: priority field options

  tags:
    type: array
    items: string
    required: false
    description: |
      Tags.
      Source: tags field options

  search_id:
    type: string
    required: false
    exclusive: true
    description: |
      Exact search ID.
      ⚠️ If provided, all other parameters are ignored

  page_num:
    type: number
    required: false
    default: 1
    description: Page number (1-based)

  page_size:
    type: number
    required: false
    default: 20
    constraints:
      max: 200
    description: |
      Items per page.
      Max 200; up to 200,000 records can be retrieved

  expand:
    type: object
    required: false
    description: |
      Extended parameters (e.g. need_workflow).
      ⚠️ Workflow work items do not allow need_workflow=true

outputs:
  data:
    type: array
    description: |
      Work item list.
      Each element includes:
      - id
      - name
      - work_item_type_key
      - project_key
      - work_item_status
      - current_nodes
      - fields
      - created_at / updated_at

  pagination:
    type: object
    description: |
      Pagination info:
      - page_num
      - page_size
      - total

constraints:
  - Terminated work items are not returned by default
  - Terminated status must be queried separately and merged
  - Custom sorting not supported (uses platform default order)
  - Time fields must be 13-digit millisecond timestamps
  - search_id is mutually exclusive with other parameters
  - QPS limit: 15 / token

error_mapping:
  20003: work_item_type_keys missing or invalid
  20013: Invalid time range (not milliseconds)
  20004: user_keys exceeds 10
  20005: search_id invalid
  30005: Work item does not exist
  30014: Work item type does not exist or no permission
```

### 使用说明

- **project_key**：路径参数，必填项。空间 ID 或空间域名（simple_name）。
- **work_item_name**：工作项名称的模糊匹配。
- **user_keys**：最多 10 个；用于筛选创建者、观察者或角色成员。可通过双击用户头像获取。
- **work_item_ids / work_item_type_keys**：缩小搜索范围至特定工作项或类型。
- **created_at / updated_at**：使用 13 位毫秒级时间戳；省略 `end` 表示“直到现在”。
- **search_id**：如果提供，将覆盖所有其他筛选参数。
- **page_size**：每页最多 200 条记录；总记录数最多 200,000 条。

---

## 获取跨空间的工作项列表

在多个空间中查询符合条件的工作项。适用于全局搜索、跨项目统计和分析。此 API 仅用于读取数据。

### 使用场景

- 当需要在多个空间/项目中搜索工作项时。
- 在构建全局仪表板或跨项目报告时。
- 在整个组织范围内汇总或分析工作项时。

### API 规范：work_item_list_across_space

```yaml
name: meegle.work_item.list.across_space
type: action
description: |
  Query work item list matching criteria across multiple spaces.
  Suitable for global search, cross-project statistics and analysis. Read-only.

auth:
  operation_type: read
  token_strategy:
    - plugin_access_token + X-User-Key
    - user_access_token

http:
  method: POST
  url: https://{domain}/open_api/work_items/filter_across_project
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_keys:
    type: array
    items: string
    required: false
    description: |
      List of space project_keys.
      How to obtain: Double-click space name.
      If omitted, queries all spaces where the plugin is installed and user has permission

  simple_names:
    type: array
    items: string
    required: false
    description: |
      List of space simple_names.
      Source: Space URL, e.g. https://project.feishu.cn/doc/overview → doc

  work_item_type_key:
    type: string
    required: true
    description: |
      Work item type key.
      How to obtain: Get Work Item Types in Space

  work_item_name:
    type: string
    required: false
    description: Work item name (fuzzy search)

  search_user:
    type: object
    required: false
    description: |
      User-related search conditions.
      field_key only supports:
      - owner
      - watchers
      - issue_operator
      - issue_reporter
      ⚠️ user_keys must be present
    schema:
      field_key: string
      user_keys:
        type: array
        items: string
      role: string

  work_item_ids:
    type: array
    items: number
    required: false
    constraints:
      max_items: 50
    description: |
      List of work item IDs.
      How to obtain: Work item detail page ··· → ID

  created_at:
    type: object
    required: false
    schema:
      start: number
      end: number
    description: |
      Created-at time range (millisecond timestamp)

  updated_at:
    type: object
    required: false
    schema:
      start: number
      end: number
    description: |
      Updated-at time range (millisecond timestamp)

  work_item_status:
    type: array
    required: false
    description: |
      Work item status list.
      Source: Get field information → work_item_status.options

  businesses:
    type: array
    items: string
    required: false
    description: |
      Business line list.
      Source: Get business list in space

  priorities:
    type: array
    items: string
    required: false
    description: |
      Priorities.
      Source: priority field options

  tags:
    type: array
    items: string
    required: false
    description: |
      Tags.
      Source: tags field options

  template_ids:
    type: array
    items: number
    required: false
    description: |
      Template ID list.
      Source: template field options

  tenant_group_id:
    type: number
    required: false
    description: |
      Tenant group ID (required only for tenant users)

  page_num:
    type: number
    required: false
    default: 1
    description: Page number (1-based)

  page_size:
    type: number
    required: false
    default: 20
    constraints:
      max: 50
    description: |
      Items per page, max 50

  expand:
    type: object
    required: false
    description: |
      Extended parameters (e.g. need_workflow).
      ⚠️ Workflow work items do not allow need_workflow=true

outputs:
  data:
    type: array
    description: |
      Work item list (WorkItemInfo).
      Each element includes:
      - id
      - name
      - work_item_type_key
      - project_key
      - simple_name
      - work_item_status
      - current_nodes
      - fields
      - created_at / updated_at

  pagination:
    type: object
    description: |
      Pagination info:
      - page_num
      - page_size
      - total

constraints:
  - Max 5000 results returned; use filters to narrow scope
  - Time parameters must be 13-digit millisecond timestamps
  - work_item_type_key is required
  - user_keys in search_user must be present
  - work_item_ids max 50
  - QPS limit: 15 / token

error_mapping:
  20094: Query result exceeds 5000
  20005: search_user parameter invalid
  20028: work_item_ids exceeds 50
  20003: work_item_type_key missing or invalid
  20013: Time parameter invalid
  20059: search_user.user_keys missing
  50006: Platform error or user does not exist
  50005: Internal service error
```

### 使用说明

- **project_keys / simple_names**：指定搜索范围。如果两者都省略，则查询用户可访问的所有空间。
- **work_item_type_key**：必填项。与单空间 API 不同，这里需要指定工作项类型。
- **search_user**：结合 `field_key`（所有者、观察者、问题操作者、问题报告者）和 `user_keys` 使用；`user_keys` 是必填项。
- **work_item_ids**：每页最多 50 条记录。
- **page_size**：每页最多 50 条记录；总记录数上限为 5000 条（单空间为 200,000 条）。

---

## 复杂条件搜索工作项

在单个 Meegle 空间中使用复杂的组合条件（AND/OR）搜索工作项。支持嵌套分组，最多返回 5000 条结果，并支持分页。

### 使用场景

- 当需要使用 AND/OR 逻辑构建高级筛选条件时。
- 当需要结合多个字段条件（例如状态 AND 优先级 AND 分配者）时。
- 当需要对返回的列进行字段级控制（指定或排除某些字段）时。

### API 规范：search_work_items_complex

```yaml
name: search_work_items_complex
type: api
description: >
  Search work items in a single Meegle space using complex combined
  filtering conditions (AND / OR). Supports up to 5000 results with pagination.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/search/params
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain (simple_name).
  work_item_type_key:
    type: string
    required: true
    description: >
      Work item type key, e.g. story / task / bug.

inputs:
  search_group:
    type: object
    required: true
    description: >
      Combined filter conditions (max 50). Supports nested AND / OR.
    schema:
      conjunction:
        type: string
        enum: [AND, OR]
        required: true
      search_params:
        type: array
        required: true
        items:
          type: object
          properties:
            param_key:
              type: string
              required: true
              description: Field key to filter on
            operator:
              type: string
              required: true
              description: >
                Operator, e.g. HAS ANY OF / = / != / IN
            value:
              type: array
              required: true
              description: Value list for the filter
      search_groups:
        type: array
        required: false
        description: Nested search_group conditions

  page_num:
    type: integer
    required: false
    default: 1
    description: Page number (start from 1)

  page_size:
    type: integer
    required: false
    default: 10
    constraints:
      max: 50
    description: Items per page (max 50)

  fields:
    type: array
    items: string
    required: false
    description: |
      Returned fields.
      - Specify mode: ["name","created_at"]
      - Exclude mode: ["-name","-created_at"]
      (modes cannot be mixed)

  expand:
    type: object
    required: false
    description: Additional expand parameters

outputs:
  data:
    type: array
    description: Work item list (max 5000 total)
  pagination:
    type: object
    properties:
      page_num: integer
      page_size: integer
      total: integer

constraints:
  - Max 50 search conditions in search_group
  - conjunction only supports AND or OR
  - Max 5000 total results; refine filters if exceeded

error_mapping:
  20094: Search result exceeds 5000, refine filters
  20069: Search param value error
  20068: Search param not supported
  20072: Conjunction only supports AND / OR
  30014: Work item type not found or no permission
  50006: Internal service error
```

### 使用说明

- **search_group**：根筛选对象，包含 `conjunction`（AND/OR）、`search_params`（字段条件数组）以及可选的嵌套 `search_groups` 以实现复杂逻辑。
- **search_params**：每个条目包含 `param_key`（字段键）、`operator`（例如 HAS ANY OF、=、!=、IN）和 `value`（值数组）。
- **fields**：使用正数值指定要返回的字段，或以 `-` 为前缀排除某些字段；请勿混合使用不同模式。
- **page_size**：每页最多 50 条记录；总结果数上限为 5000 条。

---

## 全文搜索工作项

在多个 Meegle 空间中执行全文搜索。支持按标题、描述及相关字段搜索工作项或视图。返回排名靠前的结果（最多 200 条）。

### 使用场景

- 当需要按关键词（标题、描述等）在多个空间中搜索时。
- 当需要查找符合自由文本查询的工作项或视图时。
- 当需要跨项目获取相关性排序的结果时。

### API 规范：fulltext_search_work_items

```yaml
name: fulltext_search_work_items
type: api
description: >
  Perform full-text search across multiple Meegle spaces.
  Supports searching work items or views by title, description, and related fields.
  Returns top-ranked results (max 200).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/compositive_search
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_keys:
    type: array
    items: string
    required: true
    description: List of space project_keys to search in

  query_type:
    type: string
    required: true
    enum: [workitem, view]
    description: Search target type

  query_sub_type:
    type: array
    items: string
    required: false
    description: >
      Work item type keys (effective only when query_type = workitem)

  query:
    type: string
    required: true
    constraints:
      min_length: 1
      max_length: 200
    description: >
      Full-text search keyword (1–200 characters)

  page_size:
    type: integer
    required: false
    default: 50
    description: Page size

  page_num:
    type: integer
    required: false
    default: 1
    description: Page number (start from 1)

outputs:
  data:
    type: array
    description: >
      Search result list (max 200 items, sorted by relevance)
  pagination:
    type: object
    properties:
      page_num: integer
      page_size: integer
      total: integer

constraints:
  - Max 200 total results (top-ranked by relevance)
  - query length 1–200 characters

error_mapping:
  20080: Query length must be larger than 0 and <= 200
  20081: Query type is not supported
```

### 使用说明

- **project_keys**：必填项。指定搜索的空间列表。
- **query_type**：`workitem` 或 `view` — 搜索工作项或视图。
- **query_sub_type**：当 `query_type=workitem` 时，指定具体的工作项类型（例如故事、任务、漏洞）。
- **query**：搜索关键词；长度为 1–200 个字符。
- **page_size**：默认每页 50 条记录；总结果数最多 200 条。

---

## 获取关联的工作项（单空间）

检索与指定工作项相关联的工作项。通过配置的关联字段（relation_key）来查询相关项。

### 使用场景

- 当需要获取链接/相关的工作项（例如故事中的子任务）时。
- 当遍历关联关系（父子关系、被阻塞关系）时。
- 当构建依赖关系或层次结构视图时。

### API 规范：get_associated_work_items_single_space

```yaml
name: get_associated_work_items_single_space
type: api
description: >
  Retrieve work items associated with a specified work item within a single Meegle space.
  Used to query related items via configured association fields (relation_key).

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/search_by_relation
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: Space project_key or simple_name
  work_item_type_key:
    type: string
    required: true
    description: Source work item type key
  work_item_id:
    type: string
    required: true
    description: Source work item ID

inputs:
  relation_work_item_type_key:
    type: string
    required: true
    description: Related work item type key

  relation_key:
    type: string
    required: true
    description: Association field key or docking identifier

  relation_type:
    type: integer
    required: false
    default: 0
    enum: [0, 1]
    description: |
      Relation identification method
      0 = association field ID
      1 = docking identifier

  page_size:
    type: integer
    required: false
    default: 50
    constraints:
      max: 50
    description: Max 50 per page

  page_num:
    type: integer
    required: false
    default: 1
    description: Page number (start from 1)

outputs:
  data:
    type: array
    description: Associated work item list (WorkItemInfo)
  pagination:
    type: object
    properties:
      page_num: integer
      page_size: integer
      total: integer

constraints:
  - Max 5000 associated items; use pagination
  - relation_key must exist in association field configuration

error_mapping:
  20055: Search result exceeds 5000
  30018: RelationKey not found in configuration
  20060: Work item type mismatch in relation field configuration
  50005: Internal server error
```

### 使用说明

- **project_key, work_item_type_key, work_item_id**：源工作项的路径参数。
- **relation_work_item_type_key**：要返回的相关工作项类型（例如任务、漏洞）。
- **relation_key**：定义关联关系的关联字段键或对接标识符。
- **relation_type**：0 表示使用关联字段 ID；1 表示使用对接标识符。
- **page_size**：每页最多 50 条记录；总关联项数最多 5000 条。

---

## 全文搜索工作项（单空间）

在指定的 Meegle 空间中使用全文搜索功能，支持复杂的筛选条件和按需选择字段。支持基于游标的深度分页。

### 使用场景

- 当需要在单个空间中使用复杂的筛选条件（SearchGroup）和明确的字段选择时。
- 当处理大量结果集时，使用基于游标的分页（search_after）。
- 当仅需要某些字段以减少数据量时。

### API 规范：get_work_items_full_search_single_space

```yaml
name: get_work_items_full_search_single_space
type: api
description: >
  Search work item instances in a specified Meegle space using full search with
  complex filtering and on-demand field selection.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/view_search/universal_search
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  project_key:
    type: string
    required: true
    description: Space project_key (double-click space name to obtain)

  work_item_type_key:
    type: string
    required: true
    description: Work item type key in the space

  search_group:
    type: object
    required: true
    description: >
      Combined filter conditions (max 50). Conforms to SearchGroup structure.

  pagination:
    type: object
    required: false
    properties:
      page_size:
        type: integer
        description: Page size
      search_after:
        type: string
        description: Cursor for deep pagination

  field_selected:
    type: array
    items: string
    required: false
    constraints:
      max_items: 20
    description: >
      Fields to return. If omitted, only work_item_id is returned by default.

outputs:
  datas:
    type: array
    description: Work item detail list (new model)
  pagination:
    type: object
    properties:
      page_size: integer
      total: integer
      search_after: string

constraints:
  - search_group max 50 conditions; conforms to SearchGroup structure
  - field_selected max 20 fields; omit for work_item_id only

error_mapping:
  20069: Search parameter value error
  30001: Data not found
  20063: Search operator error
  30014: Work item type not found or no permission
  20067: Search signal value not supported
  20068: Search parameter not supported
```

### 使用说明

- **project_key, work_item_type_key**：指定要搜索的空间和工作项类型。
- **search_group**：与“复杂条件搜索工作项”相同的结构，包括 `conjunction`（AND/OR）、`search_params` 和嵌套的 `search_groups`。
- **pagination**：使用上一次响应中的 `search_after` 进行基于游标的深度分页；根据需要设置 `page_size`。
- **field_selected**：最多返回 20 个字段；如果只需要 `work_item_id`，可以省略此参数。