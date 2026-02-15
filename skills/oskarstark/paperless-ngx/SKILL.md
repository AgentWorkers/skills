---
name: paperless-ngx
description: 通过 REST API 与 Paperless-ngx 文档管理系统进行交互。当用户需要在其 Paperless-ngx 实例中搜索、上传、下载、组织文档、管理标签、联系人或文档类型时，可以使用该接口。
---

# Paperless-ngx 技能

通过 HTTP 请求，利用 Paperless-ngx 的 REST API 来管理文档。

## 配置

需要以下环境变量：
- `PAPERLESS_URL`：基础 URL（例如：`https://paperless.example.com`）
- `PAPERLESS_TOKEN`：来自 Paperless-ngx 设置的 API 令牌

## 认证

在所有请求中都需要包含令牌：
```
Authorization: Token $PAPERLESS_TOKEN
```

## 核心操作

### 搜索文档

```bash
curl -s "$PAPERLESS_URL/api/documents/?query=invoice" \
  -H "Authorization: Token $PAPERLESS_TOKEN"
```

过滤选项：
- `correspondent__id`（联系人 ID）
- `document_type__id`（文档类型 ID）
- `tags__id__in`（标签 ID）
- `created__date__gte`（创建日期大于等于指定时间）
- `created__date__lte`（创建日期小于等于指定时间）
- `added__date__gte`（添加日期大于等于指定时间）

### 获取文档详情

```bash
curl -s "$PAPERLESS_URL/api/documents/{id}/" \
  -H "Authorization: Token $PAPERLESS_TOKEN"
```

### 下载文档

```bash
# Original file
curl -s "$PAPERLESS_URL/api/documents/{id}/download/" \
  -H "Authorization: Token $PAPERLESS_TOKEN" -o document.pdf

# Archived (OCR'd) version
curl -s "$PAPERLESS_URL/api/documents/{id}/download/?original=false" \
  -H "Authorization: Token $PAPERLESS_TOKEN" -o document.pdf
```

### 上传文档

```bash
curl -s "$PAPERLESS_URL/api/documents/post_document/" \
  -H "Authorization: Token $PAPERLESS_TOKEN" \
  -F "document=@/path/to/file.pdf" \
  -F "title=Document Title" \
  -F "correspondent=1" \
  -F "document_type=2" \
  -F "tags=3" \
  -F "tags=4"
```

可选字段：
- `title`（标题）
- `created`（创建时间）
- `correspondent`（联系人）
- `document_type`（文档类型）
- `storage_path`（存储路径）
- `tags`（标签，可重复）
- `archive_serial_number`（归档序列号）
- `custom_fields`（自定义字段）

### 更新文档元数据

```bash
curl -s -X PATCH "$PAPERLESS_URL/api/documents/{id}/" \
  -H "Authorization: Token $PAPERLESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Title", "correspondent": 1, "tags": [1, 2]}'
```

### 删除文档

```bash
curl -s -X DELETE "$PAPERLESS_URL/api/documents/{id}/" \
  -H "Authorization: Token $PAPERLESS_TOKEN"
```

## 组织相关端点

### 标签

```bash
# List tags
curl -s "$PAPERLESS_URL/api/tags/" -H "Authorization: Token $PAPERLESS_TOKEN"

# Create tag
curl -s -X POST "$PAPERLESS_URL/api/tags/" \
  -H "Authorization: Token $PAPERLESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Important", "color": "#ff0000"}'
```

### 联系人

```bash
# List correspondents
curl -s "$PAPERLESS_URL/api/correspondents/" -H "Authorization: Token $PAPERLESS_TOKEN"

# Create correspondent
curl -s -X POST "$PAPERLESS_URL/api/correspondents/" \
  -H "Authorization: Token $PAPERLESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "ACME Corp"}'
```

### 文档类型

```bash
# List document types
curl -s "$PAPERLESS_URL/api/document_types/" -H "Authorization: Token $PAPERLESS_TOKEN"

# Create document type
curl -s -X POST "$PAPERLESS_URL/api/document_types/" \
  -H "Authorization: Token $PAPERLESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Invoice"}'
```

## 批量操作

### 批量操作方法：
- `set_correspondent`（设置联系人）
- `set_document_type`（设置文档类型）
- `add_tag`（添加标签）
- `remove_tag`（删除标签）
- `delete`（删除文档）
- `reprocess`（重新处理文档）

## 任务状态

上传文档后，检查任务状态：
```bash
curl -s "$PAPERLESS_URL/api/tasks/?task_id={uuid}" \
  -H "Authorization: Token $PAPERLESS_TOKEN"
```

## 响应处理

- 列表端点返回 `{"count": N, "results": [...]}`（包含分页信息）
- 单个对象直接返回该对象
- 使用 `?page=2` 进行分页
- 使用 `?ordering=-created` 进行排序（前缀 `-` 表示降序排序）