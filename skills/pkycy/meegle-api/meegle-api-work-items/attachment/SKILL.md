---
name: meegle-api-work-item-attachment
description: Meegle OpenAPI：用于工作项附件操作的功能。
metadata: { openclaw: {} }
---
# Meegle API — 附件

提供用于上传、列出和管理工作项附件的相关API。

## 功能范围

- 上传附件到工作项
- 列出附件
- 下载或删除附件
- 相关的附件操作端点

---

## 添加附件

将附件添加到指定工作项的附件字段中。每次请求只能上传一个文件；单个文件的最大大小为100MB。对于支持附件类型的字段，最多可添加50个文件。

### 注意事项

1. **如果接口响应成功，但页面上没有显示文件**，请检查表单中`file`字段的内容。如果该字段为空，可能表示文件未被成功上传。
2. **如果浏览器无法显示附件预览**，请检查上传时设置的`MimeType`，并确保使用的`MimeType`与文件类型匹配（例如：JPEG：`image/jpeg`，MP4音频：`audio/mp4`，MP4视频：`video/mp4`）。
3. **附件类型的字段最多只能添加50个附件**。如果文件数量超过50个，尝试添加新附件将会失败。

### 使用场景

- 当需要将文件上传到工作项的附件字段时
- 当需要按`field_key`或`field_alias`将文件添加到特定字段时
- 当需要将文件上传到复合字段时（使用`index`指定数组下标）

### API 规范：`add_attachment`

```yaml
name: add_attachment
type: api
description: Add attachment to work item field; one file per request max 100M; field limit 50 files; multipart/form-data.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/file/upload" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { file: { type: file, required: true }, field_key: string, field_alias: string, index: string }
outputs: {}
constraints: [Permission: Permissions, one file max 100M, 50 per field]
error_mapping: { 1000050255: Project not found, 1000050174: Size limit 100M, 1000050190: Form null, 1000050262: Upload fail }
```

### 使用说明

- **file**：以`multipart/form-data`格式发送文件；每次请求只能上传一个文件；文件大小上限为100MB。
- **field_key**或`field_alias`：指定目标附件字段的名称。
- **index**：用于复合字段，以指定数组中的下标。

---

## 上传文件或富文本图片

提供上传文件的通用功能，上传后会返回文件的资源路径（URL）。主要用于在富文本内容中插入图片。文件不会被附加到特定的工作项字段中；可以使用返回的URL在富文本中或其他地方显示图片。

### 使用场景

- 当需要将图片上传到富文本（如评论或描述）中时
- 当需要一个稳定的文件URL在内容中引用时
- 当需要上传文件但不希望将其关联到工作项的附件字段时

### API 规范：`upload_files_or_rich_text_images`

```yaml
name: upload_files_or_rich_text_images
type: api
description: General file upload; returns resource URL; for rich text images; max 100M.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/file/upload" }
headers: { X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string }
inputs: { file: { type: file, required: true } }
outputs: { data: string }
constraints: [Permission: Work Item Instance, max 100M]
error_mapping: { 30016: Project not found, 1000050174: Size limit 100M }
```

### 使用说明

- **file**：以`multipart/form-data`格式发送文件；文件大小上限为100MB。
- **data**：使用返回的URL作为富文本（如评论、描述）中的图片或文件链接。

---

## 下载附件

下载工作项中指定的附件。响应结果为二进制文件流。支持的最大文件大小为100MB。

### 使用场景

- 当需要根据附件的`uuid`下载附件时
- 当需要从富文本（`multi_texts`）或附件字段（`multi_file`）中获取文件内容时
- 当需要同步或备份工作项的附件时

### API 规范：`download_attachment`

```yaml
name: download_attachment
type: api
description: Download attachment by uuid; returns binary stream; max 100M.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/{project_key}/work_item/{work_item_type_key}/{work_item_id}/file/download" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
path_params: { project_key: string, work_item_type_key: string, work_item_id: string }
inputs: { uuid: { type: string, required: true } }
outputs: {}
constraints: [Permission: Work Item Instance, max 100M]
error_mapping: { 1000050255: Project not found }
```

### 使用说明

- **uuid**：通过`Get Work Item Details`获取的附件ID（来自`multi_texts`或`multi_file`字段）。
- 响应内容为二进制文件流；在客户端中将其作为文件进行下载。

---

## 删除附件

从指定工作项的附件类型字段中删除一个或多个附件。必须提供`field_key`或`field_alias`来指定目标字段。

### 使用场景

- 当需要从工作项的附件字段中删除附件时
- 当需要清理或替换`multi_file`字段中的文件时
- 当需要与其他系统同步删除操作时

### API 规范：`delete_attachment`

```yaml
name: delete_attachment
type: api
description: Delete attachments from field; exactly one of field_key or field_alias; uuids from Get Work Item Details.
auth: { type: plugin_access_token, header: X-Plugin-Token, user_header: X-User-Key }
http: { method: POST, url: "https://{domain}/open_api/file/delete" }
headers: { Content-Type: application/json, X-Plugin-Token: "{{resolved_token}}", X-User-Key: "{{user_key}}" }
inputs: { work_item_id: integer, project_key: string, field_key: string, field_alias: string, uuids: { type: array, required: true } }
outputs: { data: object }
constraints: [Permission: Work Item Instances, one of field_key/field_alias]
error_mapping: { 30019: File not found }
```

### 使用说明

- **work_item_id**、**project_key**：用于标识工作项和项目。
- **field_key**或`field_alias**：必须提供一个参数来指定目标附件字段。
- **uuids**：通过`Get Work Item Details`获取的附件UUID列表（来自`multi_file`字段）。