---
name: meegle-api-comments
description: Meegle OpenAPI 用于对工作项或其他实体进行评论。
metadata:
  openclaw: {}
---
# Meegle API — 评论功能

以下API用于管理与工作项相关的评论操作（如添加、列出、更新评论等）。当您需要创建或查询评论时，请使用这些API。

## 功能范围

本功能涵盖以下评论操作：
- 在工作项或其他实体下添加评论
- 列出评论
- 更新和删除评论
- 相关的评论接口

---

## 添加评论

在指定的工作项下添加评论。该评论会显示在工作项详情页面的“评论/备注”标签页中，并会标记为由该插件添加的。

### 使用场景
- 当您需要向工作项添加纯文本或富文本评论时
- 当您通过插件记录工作项的备注或反馈时
- 当您需要将外部评论同步到Meegle时

### API规范：`add_comments`

```yaml
name: add_comments
type: api
description: >
  Add a comment under the specified work item. The comment appears on the
  Comments/Notes tab and is marked as added by the plugin.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comment/create
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtainable via "Get work item types in the space".
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, expand ··· in the upper right, click ID.

inputs:
  content:
    type: string
    required: false
    description: >
      Plain text comment content. Either content or rich_text required; both cannot be empty.
      When both have values, rich_text takes precedence.
  rich_text:
    type: object
    required: false
    description: >
      Rich text format. Either content or rich_text required; rich_text takes precedence when both present.
      Refer to Rich Text Format. Direct Markdown is not supported.

outputs:
  data:
    type: integer
    description: ID of the newly created comment.

constraints:
  - Permission: Permission Management – Comment
  - Either content or rich_text must be provided (both cannot be empty)
  - When both provided, rich_text takes precedence

error_mapping:
  10211: Token info invalid (user_key is empty)
  30001: Data not found (project_key error)
  50001: Create fail (no permission to comment)
  1000051280: Params invalid (rich text format incorrect; refer to Rich Text Format)
```

### 使用说明
- `content`：仅支持纯文本；适用于简单评论。
- `rich_text`：用于格式化的评论；必须遵循富文本格式（Markdown不支持）。

---

## 搜索评论

获取指定工作项下的所有评论信息。结果按创建时间升序返回。

### 使用场景
- 当您需要列出工作项的评论时
- 当您需要构建评论线程或活动信息流时
- 当您需要同步或审核工作项的评论时

### API规范：`search_comments`

```yaml
name: search_comments
type: api
description: >
  Obtain all comment information under the specified work item.
  Results returned in ascending order of creation time.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: GET
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comments
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtainable via "Get work item types in the space".
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, expand ··· in the upper right, click ID.

inputs:
  page_size:
    type: integer
    required: false
    constraints:
      max: 200
    description: Items per page. Max 200.
  page_num:
    type: integer
    required: false
    default: 1
    description: Page number, 1-based. Default 1.

outputs:
  data:
    type: array
    items:
      id: integer
      work_item_id: integer
      work_item_type_key: string
      created_at: integer
      operator: string
      content: string
    description: |
      Comment list. id: comment ID; operator: user_key; created_at: millisecond timestamp.
  pagination:
    type: object
    properties:
      total: integer
      page_num: integer
      page_size: integer
    description: Pagination info (total, page_num, page_size).

constraints:
  - Permission: Permission Management – Comments
  - page_size max 200

error_mapping:
  1000051135: Work item not found (work item does not exist)
  1000051280: Params invalid (user_key, work_item_id, or work_item_type_key is empty)
  1000051256: No permission (no permission to query comments)
  20002: Page size limit (page size exceeds 200)
```

### 使用说明
- `project_key`、`work_item_type_key`、`work_item_id`：用于标识工作项的路径参数。
- `page_num`/`page_size`：可选的分页参数；每页最多显示200条评论。

---

## 更新评论

更新指定评论的内容。更新后的评论会标记为由该插件添加的。

### 注意事项
**只有评论的创建者才能更新评论。**

### 使用场景
- 当您需要编辑由插件创建的评论时
- 当您需要修改或修订评论内容时
- 当您需要将外部系统中的更新内容同步到Meegle时

### API规范：`update_comments`

```yaml
name: update_comments
type: api
description: >
  Update the content of a specified comment. The updated comment is marked
  as added by the plugin. Only the creator can update.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: PUT
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comment/{comment_id}
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtainable via "Get work item types in the space".
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, expand ··· in the upper right, click ID.
  comment_id:
    type: string
    required: true
    description: Comment ID. Obtainable via Search Comments.

inputs:
  content:
    type: string
    required: false
    description: >
      Plain text comment content. Either content or rich_text required; both cannot be empty.
      When both have values, rich_text takes precedence.
  rich_text:
    type: object
    required: false
    description: >
      Rich text format. Either content or rich_text required; rich_text takes precedence when both present.
      Refer to Rich Text Format. Direct Markdown is not supported.

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Permission Management – Comment
  - Only the creator of the comment can update it
  - Either content or rich_text must be provided (both cannot be empty)

error_mapping:
  10211: Token info invalid (access authorization expired; re-obtain access)
  1000051280: Params invalid (rich text format error)
```

### 使用说明
- `comment_id`：通过`search_comments`获取的评论ID。
- `content`或`rich_text`：至少需要提供一个参数；如果同时提供两个参数，则`rich_text`优先生效。

---

## 删除评论

删除指定工作项下的评论。

### 注意事项
**只有评论的创建者才能删除评论。** 删除操作只能通过API完成（无法通过用户界面进行）。

### 使用场景
- 当您需要删除由插件创建的评论时
- 当您需要清理过时或错误的评论时
- 当您需要将外部系统中的删除操作同步到Meegle时

### API规范：`delete_comments`

```yaml
name: delete_comments
type: api
description: >
  Delete a specified comment under the work item.
  Only the creator can delete; deletion is API-only.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: DELETE
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/comment/{comment_id}
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.
  work_item_type_key:
    type: string
    required: true
    description: Work item type. Obtainable via "Get work item types in the space".
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, expand ··· in the upper right, click ID.
  comment_id:
    type: string
    required: true
    description: Comment ID. Obtainable via Search Comments.

outputs:
  description: Success returns err_code 0.

constraints:
  - Permission: Permission Management – Comments
  - Only the creator of the comment can delete it

error_mapping:
  1000050052: Db record not found (comment_id incorrect)
  20014: Project and work item not match (project_key does not match work item)
  10211: Token info invalid (token expired)
  10001: No permission (only creator can delete)
```

### 使用说明
- `comment_id`：通过`search_comments`获取的评论ID。
- 删除操作只能通过API完成；无法通过Meegle用户界面删除评论。