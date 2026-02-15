---
name: fabric-api
description: 通过 HTTP API 创建/搜索 Fabric 资源（记事本、文件夹、书签、文件）。
homepage: https://fabric.so
metadata: {"clawdbot":{"emoji":"🧵","requires":{"env":["FABRIC_API_KEY"],"bins":["curl"]},"primaryEnv":"FABRIC_API_KEY"}}
---

# Fabric API（通过curl进行HTTP请求）

使用此技能，可以通过Fabric HTTP API（`https://api.fabric.so`）读取或写入用户的工作空间中的内容。

## 重要注意事项（请先阅读）

- “笔记”是通过**POST `/v2/notepads`**创建的（而非 `/v2/notes`）。
- 大多数创建资源的接口都需要提供**`parentId`**：
  - 一个UUID，或者以下之一：`@alias::inbox`、`@alias::bin`。
- 创建笔记时需要提供：
  - `parentId`
  - 以及`text`（Markdown格式的字符串）或`ydoc`（高级/结构化格式的文档）。
- `tags`必须是一个对象数组，每个对象可以是：
  - `{ "name": "标签名称" }` 或 `{ "id": "<uuid>" }`
  - 不能使用嵌套数组或字符串。

当用户未指定目标文件夹时，系统会默认使用 `parentId: "@alias::inbox"`。

## 设置（Clawdbot）

此技能需要以下API密钥：

- `FABRIC_API_KEY`

推荐配置（使用 `apiKey`；Clawdbot 会自动设置 `FABRIC_API_KEY`，因为 `primaryEnv` 已被配置）：

```json5
{
  skills: {
    entries: {
      "fabric-api": {
        enabled: true,
        apiKey: "YOUR_FABRIC_API_KEY"
      }
    }
  }
}
```

## HTTP基本请求格式

- 基本URL：`https://api.fabric.so`
- 认证头：`X-Api-Key: $FABRIC_API_KEY`
- 请求内容格式：`Content-Type: application/json`

为了便于调试，建议使用 `--fail-with-body` 选项，这样错误信息会以JSON格式显示。

## 标准的curl请求模板（使用heredocs以避免编码错误）

### 获取请求（GET）

```bash
curl -sS --fail-with-body "https://api.fabric.so/v2/user/me" \
  -H "X-Api-Key: $FABRIC_API_KEY"
```

### 创建请求（POST，使用JSON）

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/ENDPOINT" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{ "replace": "me" }
JSON
```

## 核心工作流程

### 1) 创建笔记

- 接口：`POST /v2/notepads`
  - 将用户提供的“标题”映射到API请求中的`name`字段。
- 必须包含`parentId`字段。
- 使用`text`字段来存储Markdown格式的内容。

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/notepads" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "name": "Calendar Test Note",
  "text": "Created via Clawdbot",
  "parentId": "@alias::inbox",
  "tags": [{"name":"calendar"},{"name":"draft"}]
}
JSON
```

如果标签导致验证错误，请省略标签信息，之后可以通过`/v2/tags`接口进行创建或修改。

### 2) 创建文件夹

- 接口：`POST /v2/folders`

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/folders" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "name": "My new folder",
  "parentId": "@alias::inbox",
  "description": null
}
JSON
```

### 3) 创建书签

- 接口：`POST /v2/bookmarks`

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/bookmarks" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "url": "https://example.com",
  "parentId": "@alias::inbox",
  "name": "Example",
  "tags": [{"name":"reading"}]
}
JSON
```

### 4) 浏览资源（列出文件夹内的内容）

- 接口：`POST /v2/resources/filter`
  - 使用文件夹的UUID作为`parentId`来列出该文件夹内的所有资源。

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/resources/filter" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "parentId": "PARENT_UUID_HERE",
  "limit": 50,
  "order": { "property": "modifiedAt", "direction": "DESC" }
}
JSON
```

### 5) 搜索

- 接口：`POST /v2/search`
  - 当用户提供模糊搜索条件时，可以使用此接口进行搜索。

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/search" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "queries": [
    {
      "mode": "text",
      "text": "meeting notes",
      "filters": { "kinds": ["notepad"] }
    }
  ],
  "pagination": { "page": 1, "pageSize": 20 },
  "sort": { "field": "modifiedAt", "order": "desc" }
}
JSON
```

## 标签的使用规则

### 列出所有标签

- 请求：`GET /v2/tags?limit=100`

### 创建新标签

- 请求：`POST /v2/tags`，参数格式为：`{"name": "标签名称", "description": null, "resourceId": null}`

### 在创建资源时分配标签

- 可以使用 `tags: [{"name":"x"}]` 或 `tags: [{"id":"<uuid>"}]` 来指定标签。

## 速率限制与重试机制

如果收到 `429 Too Many Requests` 的错误（请求过多），请：
- 暂停请求（等待一段时间后重试）。
- 避免连续快速重复请求；采用分页方式逐步请求。

**注意**：不要在没有确保请求具有幂等性的情况下盲目重试，否则可能会导致重复创建资源。

## 常见问题排查指南

- `404 Not Found`：通常表示请求的接口或资源ID/父ID错误，或者权限问题。
- `400 Bad Request`：表示请求格式不正确，请检查必填字段和标签格式。
- `403 Forbidden`：表示订阅或权限限制。
- `429 Too Many Requests`：请暂停请求并稍后重试。

## API参考文档

OpenAPI的完整规范位于：
- `{baseDir}/fabric-api.yaml`

在不确定接口名称或请求参数格式时，请先查阅该文档。