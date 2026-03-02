---
name: tms
version: "1.0.6"
description: >
  通过 Telegram Media Server (TMS) 的 REST API 管理下载：  
  - 可通过 URL 添加下载资源（视频、Magnet 链接或种子文件）；  
  - 查看已下载资源的列表；  
  - 删除已下载的资源；  
  - 搜索种子文件。
metadata:
  {"openclaw":{"requires":{"env":[]},"primaryEnv":"TMS_API_URL"}}
---
# TMS（Telegram Media Server）API技能

当用户需要通过TMS后端添加下载任务、检查下载状态、停止下载或搜索种子文件时，可以使用此技能。所有请求都会发送到TMS的REST API。

**使用方法：**此技能不会自动添加“tms”命令。代理程序必须向TMS的API端点发送HTTP请求（GET/POST/DELETE）。完整的API规范（包括路径、请求/响应格式以及示例）包含在以下文档中，无需额外获取API文档。请参考文档中的OpenAPI规范部分来构建和调用API请求。

## 基本URL和身份验证

- **基本URL：** 如果设置了环境变量`TMS_API_URL`，则使用该值；否则，当TMS和OpenClaw运行在同一台主机上时，使用`http://127.0.0.1:8080`（TMS的默认API监听地址）。不要在URL末尾添加斜杠。所有API端点的路径前缀均为`/api/v1`，例如`GET /health`表示`GET {BaseURL}/api/v1/health`。
- **身份验证：** 可选。当TMS和OpenClaw运行在同一台主机上时，TMS会接受来自localhost的请求，无需提供`TMS_API_KEY`。如果OpenClaw运行在另一台主机上，或者需要身份验证，请设置`TMS_API_KEY`，并在每个API请求中添加`Authorization: Bearer <TMS_API_KEY>`或`X-API-Key: <TMS_API_KEY>`头部。

## 主要操作

1. **健康检查** — `GET {BaseURL}/api/v1/health` — 如果API正常运行，返回`{"status":"ok"}`。
2. **列出下载任务** — `GET {BaseURL}/api/v1/downloads` — 返回一个包含下载信息的JSON数组，包括`id`、`title`、`status`（排队中、正在下载、转换中、已完成、失败、已停止）、`progress`、`conversion_progress`、`error`（失败时）以及`position_in_queue`（排队中时）等字段。返回的信息为最佳尝试结果。
3. **添加下载任务** — 使用`POST {BaseURL}/api/v1/downloads`发送JSON请求，请求体包含`{"url": "<url>", "title": "<optional>"}`。`url`可以是视频URL（如yt-dlp格式）、Magnet链接、.torrent文件URL，或者在TMS上配置了Prowlarr代理时使用Prowlarr代理下载URL。建议在添加种子文件时使用搜索结果中的Magnet链接；`title`字段为可选参数，用于覆盖显示名称。响应状态为`201`，返回`{"id": <number>, "title": "<string>"}`。可以使用`id`来删除或查询下载任务的状态。
4. **删除下载任务** — `DELETE {BaseURL}/api/v1/downloads/{id}` — 停止并删除指定的下载任务。响应状态为`204`，不返回任何内容。`id`是从添加或列出下载任务的响应中获取的数字ID。
5. **搜索种子文件** — `GET {BaseURL}/api/v1/search?q=<query>&limit=20&quality=1080` — 需要在TMS上配置Prowlarr。`q`参数是必填项；`limit`（1–100，默认值为20）和`quality`（可选过滤条件）也可使用。返回的结果数组包含`title`、`size`、`magnet`、`torrent_url`、`indexer_name`和`peers`等字段。从搜索结果中添加下载任务时，应使用`POST /downloads`请求中的`magnet`字段；也可以使用搜索结果中的`title`字段。

详细的请求/响应格式和状态代码请参见下面的**OpenAPI规范**。

## OpenAPI规范（内联）

以下YAML内容包含了完整的TMS API规范。所有路径都是相对于`/api/v1`的基本路径；完整URL格式为`{BaseURL}` + 路径（例如`{BaseURL}/api/v1/health`）。此规范直接复制自`internal/api/openapi/openapi-llm.yaml`文件，如有API变更，请及时更新。

```yaml
openapi: 3.1.0
info:
  title: TMS REST API
  description: |
    Telegram Media Server API. Use to add downloads by URL (video/magnet/torrent), list downloads with status,
    delete a download, or search torrents. All endpoints require Authorization Bearer or X-API-Key.
  version: 1.0.0

servers:
  - url: /api/v1
    description: Base path (prepend your TMS base URL, e.g. from TMS_API_URL)

tags:
  - name: health
  - name: downloads
  - name: search

security:
  - BearerAuth: []
  - ApiKeyHeader: []

paths:
  /health:
    get:
      tags: [health]
      summary: Check API availability
      description: Call to verify TMS API is reachable. Returns 200 and {"status":"ok"}. No auth required for this endpoint in some setups; if 401, send Bearer or X-API-Key.
      operationId: getHealth
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/HealthResponse' }

  /downloads:
    get:
      tags: [downloads]
      summary: List downloads
      description: |
        Call to get current downloads (queued, active, completed). Returns array of items with id, title, status (queued|downloading|converting|completed|failed|stopped), progress (0-100), conversion_progress, error (if failed), position_in_queue (if queued). Snapshot is best-effort.
      operationId: listDownloads
      responses:
        '200':
          description: Array of download items
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/DownloadItem' }
    post:
      tags: [downloads]
      summary: Create a download
      description: |
        Call to add a download. Body: JSON with "url" (required) and optional "title" (display name, e.g. from search). URL can be: video URL (yt-dlp), magnet link (magnet:...), .torrent file URL, or Prowlarr proxy download URL when Prowlarr is configured. Prefer magnet from search results. Response gives id (number) and title (string). Use this id for DELETE /downloads/{id}.
      operationId: addDownload
      requestBody:
        required: true
        content:
          application/json:
            schema: { $ref: '#/components/schemas/AddDownloadRequest' }
            example: { url: "magnet:?xt=urn:btih:abc123" }
      responses:
        '201':
          description: Download created
          content:
            application/json:
              schema: { $ref: '#/components/schemas/AddDownloadResponse' }
        '400':
          description: Missing url or invalid URL
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '500':
          description: Server error
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }

  /downloads/{id}:
    delete:
      tags: [downloads]
      summary: Stop and remove a download
      description: Call to stop the download with given id and remove it. id is the numeric id returned by POST /downloads. Returns 204 with no body on success.
      operationId: deleteDownload
      parameters:
        - name: id
          in: path
          required: true
          schema: { type: integer, minimum: 1 }
      responses:
        '204':
          description: Download stopped
        '400':
          description: Invalid id (not a number)
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '500':
          description: Server error
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }

  /search:
    get:
      tags: [search]
      summary: Search torrents
      description: |
        Call to search torrents (requires Prowlarr configured). Query param "q" (required): search string. "limit" (optional, 1-100, default 20): max results. "quality" (optional): filter by substring in release title (e.g. 1080). Returns array of objects with title, size, magnet, torrent_url, indexer_name, peers. When adding a download, prefer the magnet field in POST /downloads; you may also pass title from the result.
      operationId: searchTorrents
      parameters:
        - name: q
          in: query
          required: true
          schema: { type: string }
        - name: limit
          in: query
          schema: { type: integer, minimum: 1, maximum: 100, default: 20 }
        - name: quality
          in: query
          schema: { type: string }
      responses:
        '200':
          description: Array of search results
          content:
            application/json:
              schema:
                type: array
                items: { $ref: '#/components/schemas/SearchResultItem' }
        '400':
          description: Missing q
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '401':
          description: Unauthorized
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }
        '503':
          description: Search not configured or Prowlarr error
          content:
            application/json:
              schema: { $ref: '#/components/schemas/ErrorResponse' }

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: API Key
    ApiKeyHeader:
      type: apiKey
      in: header
      name: X-API-Key

  schemas:
    HealthResponse:
      type: object
      required: [status]
      properties:
        status: { type: string, example: "ok" }

    DownloadItem:
      type: object
      properties:
        id: { type: integer }
        title: { type: string }
        status: { type: string, enum: [queued, downloading, converting, completed, failed, stopped] }
        progress: { type: integer, minimum: 0, maximum: 100 }
        conversion_progress: { type: integer, minimum: 0, maximum: 100 }
        error: { type: string }
        position_in_queue: { type: integer }

    AddDownloadRequest:
      type: object
      required: [url]
      properties:
        url: { type: string }
        title: { type: string, description: Optional display name e.g. from search result }

    AddDownloadResponse:
      type: object
      properties:
        id: { type: integer }
        title: { type: string }

    SearchResultItem:
      type: object
      properties:
        title: { type: string }
        size: { type: integer }
        magnet: { type: string }
        torrent_url: { type: string }
        indexer_name: { type: string }
        peers: { type: integer }

    ErrorResponse:
      type: object
      required: [error]
      properties:
        error: { type: string }
```

## Webhook（可选）

如果TMS配置了`TMS_WEBHOOK_URL`，并且该URL指向OpenClaw可以接收请求的端点，那么当下载任务完成、失败或被停止时，TMS会向该URL发送POST请求。请求体包含`id`、`title`、`status`（已完成|失败|已停止）、`error`（失败时）以及`event_id`（UUID）等信息。如果在TMS配置中设置了`TMS_WEBHOOK_TOKEN`，则请求头中需要包含`Authorization: Bearer <TMS_WEBHOOK_TOKEN>`（这是OpenClaw网关钩子所必需的）。通知机制为最佳尝试方式（不保证一定会发送）。您可以使用此功能在聊天中向用户通知下载任务的完成情况。