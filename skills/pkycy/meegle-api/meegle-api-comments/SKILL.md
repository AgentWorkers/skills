---
name: meegle-api-comments
description: Meegle OpenAPI：用于对工作项进行评论的功能。
metadata: { openclaw: {} }
---
# Meegle API — 评论功能

## 添加评论  
在指定的工作项下添加评论。该评论会显示在工作项详情页面的“评论/备注”标签页中，并会标记为由该插件添加的。  

### 使用场景  
- 当需要向工作项添加纯文本或富文本评论时  
- 当通过该插件记录工作项的备注或反馈时  
- 当需要将外部评论同步到 Meegle 时  

### API 规范：`add_comments`  
```yaml
name: add_comments
type: api
description: Add comment under work item; content or rich_text required (rich_text precedence).
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comment/create" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { content: string, rich_text: object }
outputs: { data: integer }
constraints: [Permission: Comment, content or rich_text required]
error_mapping: { 10211: Token invalid, 30001: Data not found, 50001: No permission, 1000051280: Rich text invalid }
```  

### 使用说明  
- `content`：仅支持纯文本；用于简单评论的输入。  
- `rich_text`：用于格式化的评论；必须遵循富文本格式（Markdown 不被支持）。  

## 搜索评论  
获取指定工作项下的所有评论信息。结果按创建时间顺序返回。  

### 使用场景  
- 当需要列出工作项的评论时  
- 当需要构建评论线程或活动信息流时  
- 当需要同步或审核工作项的评论时  

### API 规范：`search_comments`  
```yaml
name: search_comments
type: api
description: List comments under work item; ascending by creation time.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: GET, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comments" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { page_size: { type: integer, max: 200 }, page_num: { type: integer, default: 1 } }
outputs: { data: array, pagination: object }
constraints: [Permission: Comments, page_size max 200]
error_mapping: { 1000051135: Work item not found, 1000051280: Params invalid, 1000051256: No permission, 20002: Page size limit }
```  

### 使用说明  
- `project_key`、`work_item_type_key`、`work_item_id`：用于标识工作项的路径参数。  
- `page_num`/`page_size`：可选的分页参数；每页最多显示 200 条评论。  

## 更新评论  
更新指定评论的内容。更新后的评论会标记为由该插件添加的。  

### 注意  
**仅评论的创建者才能更新评论内容。**  

### 使用场景  
- 当需要编辑由该插件创建的评论时  
- 当需要修改或修订评论内容时  
- 当需要将外部系统中的评论更新内容同步到 Meegle 时  

### API 规范：`update_comments`  
```yaml
name: update_comments
type: api
description: Update comment; only creator can update; content or rich_text required.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: PUT, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comment/{comment_id}" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string, comment_id: string }
inputs: { content: string, rich_text: object }
outputs: { data: object }
constraints: [Permission: Comment, only creator, content or rich_text required]
error_mapping: { 10211: Token invalid, 1000051280: Params invalid }
```  

### 使用说明  
- `comment_id`：通过 `search_comments` 获取的评论 ID。  
- 必须提供 `content` 或 `rich_text` 中的一项；如果两者都提供，则优先使用 `rich_text`。  

## 删除评论  
删除指定工作项下的评论。  

### 注意  
**仅评论的创建者才能删除评论**。删除操作只能通过 API 完成（无法通过 Meegle 用户界面进行）。  

### 使用场景  
- 当需要删除由该插件创建的评论时  
- 当需要清理过时或错误的评论时  
- 当需要将外部系统中的删除操作同步到 Meegle 时  

### API 规范：`delete_comments`  
```yaml
name: delete_comments
type: api
description: Delete comment; only creator can delete; API-only.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: DELETE, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comment/{comment_id}" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string, comment_id: string }
outputs: {}
constraints: [Permission: Comments, only creator]
error_mapping: { 1000050052: Comment not found, 20014: Project/work item mismatch, 10211: Token invalid, 10001: No permission }
```  

### 使用说明  
- `comment_id`：通过 `search_comments` 获取的评论 ID。  
- 删除操作仅支持通过 API 完成；无法通过 Meegle 用户界面删除评论。