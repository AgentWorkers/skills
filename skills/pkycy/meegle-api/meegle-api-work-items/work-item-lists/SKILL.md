---
name: meegle-api-work-item-lists
description: Meegle OpenAPI：用于列出、搜索以及查询工作项（支持过滤、全文搜索以及关联功能）。
metadata: { openclaw: {} }
---
# Meegle API — 工作项列表与搜索

用于列出、过滤、搜索和查询 Meegle 空间中的工作项。这些 API 均为只读接口。

---

## 获取单个工作项列表

根据指定空间（project_key）内的条件查询工作项列表。排除已终止的工作项。此 API 仅用于检索、分析和汇总数据。

### 使用场景

- 当需要根据名称、分配者、状态、类型、日期等条件过滤工作项时。
- 在单个空间内构建仪表板、报告或搜索结果时。
- 与需要工作项列表的外部工具集成时。

### API 规范：work_item_list_single_space

```yaml
name: meegle.work_item.list.single_space
type: action
description: Query work item list by conditions in one space; excludes terminated; read-only.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/filter" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string }
inputs: { work_item_name: string, user_keys: array (max 10), work_item_ids: array, work_item_type_keys: array, created_at: object, updated_at: object, work_item_status: array, businesses: array, priorities: array, tags: array, search_id: string, page_num: number, page_size: number (max 200), expand: object }
outputs: { data: array, pagination: object }
constraints: [terminated not returned by default, time 13-digit ms, search_id exclusive, QPS 15]
error_mapping: { 20003: work_item_type_keys invalid, 20013: Invalid time range, 20004: user_keys exceeds 10, 20005: search_id invalid, 30005: Work item not exist, 30014: Type not exist or no permission }
```

### 使用说明

- **project_key**：路径参数，必填项。表示空间 ID 或空间域名（simple_name）。
- **work_item_name**：对工作项名称进行模糊匹配。
- **user_keys**：最多支持 10 个，用于筛选创建者、观察者或角色成员。可通过双击用户头像获取这些信息。
- **work_item_ids / work_item_type_keys**：用于缩小搜索范围，仅显示特定工作项或类型。
- **created_at / updated_at**：使用 13 位毫秒级时间戳；省略 `end` 选项表示“截至当前时间”。
- **search_id**：如果提供此参数，将覆盖其他所有筛选条件。
- **page_size**：每页最多显示 200 条记录；总记录数上限为 200,000 条。

---

## 获取跨空间的工作项列表

在多个空间中查询符合特定条件的工作项。适用于全局搜索、跨项目统计和分析。此 API 仅用于检索数据。

### 使用场景

- 需要在多个空间/项目中搜索工作项时。
- 在构建全局仪表板或跨项目报告时。
- 需要对整个组织的工作项进行汇总或分析时。

### API 规范：work_item_list_across_space

```yaml
name: meegle.work_item.list.across_space
type: action
description: Query work item list across spaces; global search; max 5000 results.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/work_items/filter_across_project" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_keys: array, simple_names: array, work_item_type_key: string, work_item_name: string, search_user: object, work_item_ids: array (max 50), created_at: object, updated_at: object, work_item_status: array, businesses: array, priorities: array, tags: array, template_ids: array, tenant_group_id: number, page_num: number, page_size: number (max 50), expand: object }
outputs: { data: array, pagination: object }
constraints: [max 5000 results, work_item_type_key required, work_item_ids max 50, QPS 15]
error_mapping: { 20094: Result exceeds 5000, 20005: search_user invalid, 20028: work_item_ids exceeds 50, 20003: work_item_type_key invalid, 20013: Time invalid, 20059: search_user.user_keys missing, 50006: Platform/user error, 50005: Internal error }
```

### 使用说明

- **project_keys / simple_names**：指定搜索范围。如果两者都省略，则会搜索用户可访问的所有空间。
- **work_item_type_key**：必填项，用于指定工作项类型。
- **search_user**：结合 `field_key`（如 owner、watchers、issue_operator、issue_reporter）和 `user_keys` 进行搜索；`user_keys` 是必填项。
- **work_item_ids**：每页最多显示 50 条记录。
- **page_size**：每页最多显示 50 条记录；总记录数上限为 5000 条（单空间查询时为 200,000 条）。

---

## 复杂条件搜索工作项

在单个 Meegle 空间中使用复杂的 AND/OR 条件搜索工作项。支持嵌套分组，并提供分页功能（最多返回 5000 条结果）。

### 使用场景

- 需要使用 AND/OR 逻辑构建高级筛选条件时。
- 需要结合多个字段条件进行搜索时（例如：状态 AND 优先级 AND 分配者）。
- 需要对返回的字段进行精确控制（指定或排除某些字段）时。

### API 规范：search_work_items_complex

```yaml
name: search_work_items_complex
type: api
description: Search work items in one space with AND/OR filters; max 5000 results, pagination.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/search/params" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string }
inputs: { search_group: object (max 50, conjunction AND|OR), page_num: integer, page_size: integer (max 50), fields: array, expand: object }
outputs: { data: array, pagination: object }
constraints: [search_group max 50, conjunction AND or OR, max 5000 total]
error_mapping: { 20094: Exceeds 5000, 20069: Param value error, 20068: Param not supported, 20072: Conjunction AND/OR only, 30014: Type not found or no permission, 50006: Internal error }
```

### 使用说明

- **search_group**：包含基础筛选条件（conjunction：AND/OR）、搜索参数（search_params：字段条件数组）以及可选的嵌套搜索组（search_groups）的搜索对象。
- **search_params**：每个参数包含 `param_key`（字段键）、`operator`（如 HAS ANY OF、=、!=、IN）和 `value`（值数组）。
- **fields**：使用正数值指定要返回的字段；前缀为 `-` 可以排除某些字段；请注意不要混合使用不同的字段筛选方式。
- **page_size**：每页最多显示 50 条记录；总记录数上限为 5000 条。

---

## 全文搜索工作项

在多个 Meegle 空间中执行全文搜索。支持根据标题、描述及相关字段搜索工作项或视图。返回排名靠前的结果（最多 200 条）。

### 使用场景

- 需要根据关键词（如标题、描述等）在多个空间中搜索时。
- 需要查找符合自由文本查询的工作项或视图时。
- 需要对跨项目的数据进行相关性排序时。

### API 规范：fulltext_search_work_items

```yaml
name: fulltext_search_work_items
type: api
description: Full-text search across spaces; work items or views; max 200 results by relevance.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/compositive_search" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_keys: array, query_type: workitem|view, query_sub_type: array, query: string (1–200 chars), page_size: integer, page_num: integer }
outputs: { data: array, pagination: object }
constraints: [max 200 results, query 1–200 chars]
error_mapping: { 20080: Query length 0 or >200, 20081: Query type not supported }
```

### 使用说明

- **project_keys**：必填项，指定搜索的空间列表。
- **query_type**：`workitem` 或 `view` — 分别表示搜索工作项或视图。
- **query_sub_type**：当 `query_type=workitem` 时，可指定具体的工作项类型（如 story、task、bug）。
- **query**：搜索关键词，长度不超过 200 个字符。
- **page_size**：默认每页显示 50 条记录；总记录数上限为 200 条。

---

## 获取与指定工作项相关的工作项（单空间）

检索与单个 Meegle 空间中的指定工作项相关联的工作项。可通过配置的关联字段（relation_key）来查询相关项。

### 使用场景

- 当需要获取某个工作项的子任务等相关项时。
- 当需要遍历关联关系（如父子关系、被阻塞关系）时。
- 当需要构建依赖关系或层级视图时。

### API 规范：get_associated_work_items_single_space

```yaml
name: get_associated_work_items_single_space
type: api
description: Get work items associated with a work item in one space via relation_key.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/search_by_relation" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { relation_work_item_type_key: string, relation_key: string, relation_type: integer (0|1), page_size: integer (max 50), page_num: integer }
outputs: { data: array, pagination: object }
constraints: [max 5000 associated, relation_key must exist in config]
error_mapping: { 20055: Exceeds 5000, 30018: RelationKey not found, 20060: Type mismatch, 50005: Internal error }
```

### 使用说明

- **project_key, work_item_type_key, work_item_id**：用于指定源工作项的路径参数。
- **relation_work_item_type_key**：指定要返回的相关工作项类型（如 task、bug）。
- **relation_key**：定义关联关系的字段键或对接标识符。
- **relation_type**：0 表示使用关联字段 ID；1 表示使用对接标识符。
- **page_size**：每页最多显示 50 条记录；总关联项数上限为 5000 条。

---

## 全文搜索工作项（单空间）

在指定 Meegle 空间中使用全文搜索功能，支持复杂的筛选条件和字段选择。支持基于游标的深度分页。

### 使用场景

- 需要在单个空间中使用复杂的筛选条件（SearchGroup）并进行明确的字段选择时。
- 当处理大量结果集时，可以使用基于游标的分页功能（search_after）。
- 当需要仅返回所需字段以减少数据传输量时。

### API 规范：get_work_items_full_search_single_space

```yaml
name: get_work_items_full_search_single_space
type: api
description: Full search in one space with SearchGroup filters and field_selected; cursor pagination.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/view_search/universal_search" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { project_key: string, work_item_type_key: string, search_group: object (max 50), pagination: object, field_selected: array (max 20) }
outputs: { datas: array, pagination: object }
constraints: [search_group max 50, field_selected max 20]
error_mapping: { 20069: Param value error, 30001: Data not found, 20063: Operator error, 30014: Type not found or no permission, 20067: Signal not supported, 20068: Param not supported }
```

### 使用说明

- **project_key, work_item_type_key**：指定搜索的空间和工作项类型。
- **search_group**：与 `search_work_items_complex` 中的 SearchGroup 结构相同，包括联合条件（conjunction）、搜索参数（search_params）和嵌套搜索组（search_groups）。
- **pagination**：使用上一次响应中的 `search_after` 参数进行基于游标的深度分页；根据需要设置 `page_size`。
- **field_selected**：最多返回 20 个字段；如仅需要 `work_item_id`，可省略此参数。