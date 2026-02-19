---
name: meegle-api-work-item-attachment
description: Meegle OpenAPI：用于工作项附件操作的功能。
metadata:
  openclaw: {}
---
# Meegle API — 附件

提供与工作项中的附件上传、列出和管理相关的API。

## 功能范围

- 上传附件到工作项
- 列出附件
- 下载或删除附件
- 相关的附件操作端点

---

## 添加附件

将附件添加到指定工作项的附件字段中。每次请求只能添加一个文件；每个文件的最大大小为100MB。对于支持附件类型的字段，最多可添加50个文件。

### 注意事项

1. **如果接口响应成功，但页面上没有显示文件**，请检查表单中文件字段的内容。如果文件字段为空，可能表示文件未被成功上传。
2. **如果浏览器无法显示附件预览**，请检查上传时设置的**MimeType**，并确保使用的MimeType与文件类型匹配（例如：JPEG：`image/jpeg`，MP4音频：`audio/mp4`，MP4视频：`video/mp4`）。
3. **附件类型字段的附件数量限制为50个**。如果已添加的附件数量超过50个，再次尝试添加将会失败。

### 使用场景

- 当需要将文件上传到工作项的附件字段时
- 当需要按`field_key`或`field_alias`将文件添加到特定字段时
- 当需要将文件上传到复合字段时（使用`index`来指定数组下标）

### API 规范：`add_attachment`

```yaml
name: add_attachment
type: api
description: >
  Add an attachment to an attachment field under a specified work item.
  One file per request; max 100M. Attachment field limit 50 files.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/file/upload
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"
  content_type: multipart/form-data

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
    description: >
      Work item type. Obtainable via "Get work item types in the space".
      Must match the work item instance identified by work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, click ··· in the upper right, then ID to copy.

inputs:
  file:
    type: file
    required: true
    description: >
      Attachment file. Only one attachment per request; max size 100M.
  field_key:
    type: string
    required: false
    description: >
      Unique identifier of the attachment upload field. Pass either field_key or field_alias.
  field_alias:
    type: string
    required: false
    description: >
      Docking identifier for the attachment upload field. Pass either field_key or field_alias.
  index:
    type: string
    required: false
    description: For composite fields, used to specify the array subscript.

outputs:
  description: Success returns err_code 0.

constraints:
  - Permission: Developer Platform – Permissions / Permission Management
  - One file per request; max 100M per file
  - Attachment field limit: 50 files per field
  - Use multipart/form-data; set MimeType correctly for preview

error_mapping:
  1000050255: Project not found (project_key incorrect)
  1000050174: Uploaded file size limit 100M (file exceeds 100M)
  1000050190: Request form is null (form parameters invalid)
  1000050262: Upload file fail
```

### 使用说明

- **file**：以multipart/form-data格式发送文件；每次请求只能上传一个文件；文件大小限制为100MB。
- **field_key** 或 **field_alias**：指定目标附件字段。
- **index**：用于复合字段，以指定数组中的下标。

---

## 上传文件或富文本图片

提供文件上传功能，上传后会返回文件的资源路径（URL）。主要用于在富文本内容中插入图片。上传的文件不会直接附加到工作项的特定字段中，可以使用返回的URL在富文本中或其他地方引用。

### 使用场景

- 当需要将图片上传到富文本（如评论或描述）中时
- 当需要一个稳定的文件URL在内容中引用时
- 当需要上传文件但不希望将其附加到工作项的附件字段时

### API 规范：`upload_files_or_rich_text_images`

```yaml
name: upload_files_or_rich_text_images
type: api
description: >
  General file upload that returns the resource path (URL).
  Mainly used for uploading images in rich text. Max 100M per file.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/file/upload
  headers:
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"
  content_type: multipart/form-data

path_params:
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle.
      simple_name: From space URL, e.g. https://meegle.com/doc/overview → doc.

inputs:
  file:
    type: file
    required: true
    description: Attachment file. Max size 100M.

outputs:
  data:
    type: string
    description: Attachment link (resource URL) to use in rich text or elsewhere.

constraints:
  - Permission: Permission Management – Work Item Instance
  - Max file size 100M

error_mapping:
  30016: Project not found (project_key incorrect)
  1000050174: Uploaded file size limit 100M (file exceeds 100M)
```

### 使用说明

- **file**：以multipart/form-data格式发送文件；文件大小限制为100MB。
- **data**：使用返回的URL作为富文本（如评论、描述）中的图片或文件链接。

---

## 下载附件

下载工作项中指定的附件。响应内容为二进制文件流，最大支持文件大小为100MB。

### 使用场景

- 当需要根据附件的uuid下载附件时
- 当需要从富文本（`multi_texts`）或附件字段（`multi_file`）中获取文件内容时
- 当需要同步或备份工作项的附件时

### API 规范：`download_attachment`

```yaml
name: download_attachment
type: api
description: >
  Download a specified attachment under a work item.
  Returns a binary file stream. Max supported size 100M.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/file/download
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
    description: >
      Work item type. Obtainable via "Get work item types in the space".
      Must match the work item instance identified by work_item_id.
  work_item_id:
    type: string
    required: true
    description: Work item instance ID. In work item details, click ··· in the upper right, then ID to copy.

inputs:
  uuid:
    type: string
    required: true
    description: >
      Attachment ID. Obtain from the rich text (multi_texts) or attachment field
      (multi_file) in the Get Work Item Details response. Max supported size 100M.

outputs:
  description: Binary file stream (the attachment content).

constraints:
  - Permission: Permission Management – Work Item Instance
  - Max download size 100M

error_mapping:
  1000050255: Project not found (project_key incorrect)
```

### 使用说明

- **uuid**：通过`Get Work Item Details`获取的附件ID（来自`multi_texts`或`multi_file`字段）。
- 响应内容为二进制文件流；在客户端中将其作为文件进行下载。

---

## 删除附件

从指定工作项的附件类型字段中删除一个或多个附件。必须提供`field_key`或`field_alias`来标识目标字段。

### 使用场景

- 当需要从工作项的附件字段中删除附件时
- 当需要清理或替换`multi_file`字段中的文件时
- 当需要将外部系统中的删除操作同步到本地时

### API 规范：`delete_attachment`

```yaml
name: delete_attachment
type: api
description: >
  Delete one or more attachments from an attachment-type field of a specified work item.
  Pass exactly one of field_key or field_alias to identify the target field.

auth:
  type: plugin_access_token
  header: X-Plugin-Token
  user_header: X-User-Key

http:
  method: POST
  url: https://{domain}/open_api/file/delete
  headers:
    Content-Type: application/json
    X-Plugin-Token: "{{resolved_token}}"
    X-User-Key: "{{user_key}}"

inputs:
  work_item_id:
    type: integer
    required: true
    description: >
      Work item instance ID. In work item details, expand ··· > ID in the upper right to obtain.
  project_key:
    type: string
    required: true
    description: >
      Space ID (project_key) or space domain name (simple_name).
      project_key: Double-click space name in Meegle/Feishu project space.
      simple_name: From space URL, e.g. https://project.feishu.cn/doc/overview → doc.
  field_key:
    type: string
    required: false
    description: >
      Attachment field ID. Obtain via Get Work Item Creation Metadata.
      Supports composite sub-fields. Pass either field_key or field_alias, not both and not neither.
  field_alias:
    type: string
    required: false
    description: >
      Docking identifier of the attachment field. Obtain via Get Work Item Creation Metadata.
      Supports composite sub-fields. Pass either field_key or field_alias, not both and not neither.
  uuids:
    type: array
    items: string
    required: true
    description: >
      List of attachment UUIDs to delete. Obtain from the attachment field (multi_file type)
      in the Get Work Item Details response.

outputs:
  data:
    type: object
    description: Empty object on success.

constraints:
  - Permission: Permission Management – Work Item Instances
  - Exactly one of field_key or field_alias must be provided (not both, not neither)

error_mapping:
  30019: File not found (specified file does not exist or cannot be accessed)
```

### 使用说明

- **work_item_id**、**project_key**：用于识别工作项和项目。
- **field_key** 或 **field_alias**：必须提供一个参数来指定目标附件字段。
- **uuids**：通过`Get Work Item Details`获取的附件UUID列表（来自`multi_file`字段）。