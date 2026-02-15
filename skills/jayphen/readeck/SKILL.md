---
name: readeck
description: Readeck集成用于保存和管理文章。支持通过Readeck的API添加URL、列出条目以及管理书签。可以根据请求配置自定义URL和API密钥，或者通过环境变量`READECK_URL`和`READECK_API_KEY`来进行设置。
---

# Readeck 集成

## 配置

通过以下方式配置 Readeck 的访问权限：
- 请求参数：`url` 和 `apiKey`
- 环境变量：`READECK_URL` 和 `READECK_API_KEY`

## 核心操作

### 添加文章

将一个 URL 添加到 Readeck 进行解析和保存：

```bash
curl -X POST "$READECK_URL/api/bookmarks" \
  -H "Authorization: Bearer $READECK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/article"}'
```

响应中包含 `id`、`url` 和 `title`。

### 列出文章

获取已保存的文章：

```bash
curl "$READECK_URL/api/bookmarks?limit=20" \
  -H "Authorization: Bearer $READECK_API_KEY"
```

查询参数：`page`、`limit`、`status`、`search`。

### 获取单篇文章

```bash
curl "$READECK_URL/api/bookmarks/$ID" \
  -H "Authorization: Bearer $READECK_API_KEY"
```

### 删除文章

```bash
curl -X DELETE "$READECK_URL/api/bookmarks/$ID" \
  -H "Authorization: Bearer $READECK_API_KEY"
```

### 标记为已读

```bash
curl -X PUT "$READECK_URL/api/bookmarks/$ID/status" \
  -H "Authorization: Bearer $READECK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "read"}'
```

## 常见操作模式

**带标签保存：**
```json
{"url": "https://example.com", "tags": ["tech", "readlater"]}
```

**保存到特定集合：**
```json
{"url": "https://example.com", "collection": "my-collection"}
```

**按状态过滤：** `unread`、`read`、`archived`

## 错误处理

- `401`：API 密钥无效
- `404`：未找到文章
- `422`：URL 或请求体无效