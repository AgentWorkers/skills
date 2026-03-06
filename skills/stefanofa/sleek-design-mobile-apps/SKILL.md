---
name: sleek-design-mobile-apps
description: >
  **使用场景：**  
  当用户需要设计移动应用程序、创建用户界面（UI），或与他们的 Sleek 项目进行交互时。该功能涵盖了高级请求（例如“设计一个能够执行某功能的应用程序”），以及具体的操作（例如“列出我的项目”、“创建新项目”、“截取某个界面的截图”）。
compatibility: Requires SLEEK_API_KEY environment variable. Network access limited to https://sleek.design only.
metadata:
  requires-env: SLEEK_API_KEY
  allowed-hosts: https://sleek.design
---
# 使用 Sleek 进行设计

[![几分钟内设计移动应用程序](https://raw.githubusercontent.com/sleekdotdesign/agent-skills/main/assets/hero.png)](https://sleek.design)

## 概述

[sleek.design](https://sleek.design) 是一款基于人工智能的移动应用程序设计工具。您可以通过 `/api/v1/*` 的 REST API 与之交互，创建项目、用自然语言描述您想要构建的内容，并获取渲染后的屏幕截图。所有通信都使用标准的 HTTP 协议，并通过 bearer token 进行身份验证。

**基础 URL**: `https://sleek.design`
**身份验证**: 在每个 `/api/v1/*` 请求中添加 `Authorization: Bearer $SLEEK_API_KEY`
**Content-Type**: `application/json`（请求和响应）
**CORS**: 在所有 `/api/v1/*` 端点上启用

---

## 先决条件：API 密钥

请在 **https://sleek.design/dashboard/api-keys** 处创建 API 密钥。密钥的完整格式在创建时仅显示一次——将其存储在 `SLEEK_API_KEY` 环境变量中。

**所需计划**: Pro+（需要 API 访问权限）

### 密钥权限范围

| 权限范围             | 所解锁的功能                          |
| ----------------- | ---------------------------- |
| `projects:read`   | 列出/获取项目                         |
| `projects:write`  | 创建/删除项目                         |
| `components:read` | 列出项目中的组件                         |
| `chats:read`      | 获取聊天运行状态                         |
| `chats:write`     | 发送聊天消息                         |
| `screenshots`     | 生成组件的截图                         |

请仅为您的任务创建所需的权限范围对应的密钥。

---

## 安全性与隐私

- **单一主机**: 所有请求都仅发送到 `https://sleek.design`。不会将任何数据发送给第三方。
- **仅使用 HTTPS**: 所有通信都使用 HTTPS 协议。API 密钥仅在 `Authorization` 头部中传输给 Sleek 服务器。
- **最小权限范围**: 仅为任务创建所需的 API 密钥。建议使用短期有效或可撤销的密钥。
- **图片 URL**: 在聊天消息中使用 `imageUrls` 时，这些 URL 由 Sleek 的服务器获取。避免传递包含敏感内容的 URL。

---

## 处理高级请求

当用户请求“设计一个健身追踪应用程序”或“为我制作一个设置界面”时：

1. **如果项目尚不存在**，则创建一个项目（询问用户名称，或根据请求自动生成名称）。
2. **发送聊天消息**，描述要构建的内容——您可以直接使用用户提供的文字作为 `message.text`；Sleek 的人工智能会解析自然语言。
3. **遵循以下截图展示规则** 来展示结果。

您无需先将请求分解为多个屏幕。只需发送完整的意图作为一条消息，让 Sleek 决定需要创建哪些屏幕。

---

## 截图展示规则

**每当聊天运行产生 `screen_created` 或 `screen_updated` 操作后**，务必生成截图并展示给用户。**切勿在未展示视觉结果的情况下默默完成聊天操作。**

**当项目中的屏幕首次被创建时**（即运行包含 `screen_created` 操作时），需展示：
1. 每个新创建的屏幕的截图（`componentIds: [screenId]`）。
2. 项目中所有屏幕的合并截图（`componentIds: [所有屏幕 ID]`）。

**当仅更新现有屏幕时**，为每个受影响的屏幕生成一张截图。

除非用户另有要求，否则所有截图的背景颜色应设置为 `background: "transparent"`。

---

## 快速参考 — 所有端点

| 方法   | 路径                                      | 权限范围             | 描述       |
| -------- | --------------------------------------- | ----------------- | ----------------- |
| `GET`    | `/api/v1/projects`                      | `projects:read`   | 列出项目                         |
| `POST`   | `/api/v1/projects`                      | `projects:write`  | 创建项目                         |
| `GET`    | `/api/v1/projects/:id`                  | `projects:read`   | 获取项目                         |
| `DELETE` | `/api/v1/projects/:id`                  | `projects:write`  | 删除项目                         |
| `GET`    | `/api/v1/projects/:id/components`       | `components:read` | 列出组件                         |
| `POST`   | `/api/v1/projects/:id/chat/messages`    | `chats:write`     | 发送聊天消息                         |
| `GET`    | `/api/v1/projects/:id/chat/runs/:runId` | `chats:read`      | 查询运行状态                         |
| `POST`   | `/api/v1/screenshots`                   | `screenshots`     | 生成截图                         |

所有 ID 都是稳定的字符串标识符。

---

## 端点

### 项目

#### 列出项目

```http
GET /api/v1/projects?limit=50&offset=0
Authorization: Bearer $SLEEK_API_KEY
```

响应 `200`:

```json
{
  "data": [
    {
      "id": "proj_abc",
      "name": "My App",
      "slug": "my-app",
      "createdAt": "2026-01-01T00:00:00Z",
      "updatedAt": "..."
    }
  ],
  "pagination": { "total": 12, "limit": 50, "offset": 0 }
}
```

#### 创建项目

```http
POST /api/v1/projects
Authorization: Bearer $SLEEK_API_KEY
Content-Type: application/json

{ "name": "My New App" }
```

响应 `201` — 结果与单个项目的响应格式相同。

#### 获取/删除项目

```http
GET    /api/v1/projects/:projectId
DELETE /api/v1/projects/:projectId   → 204 No Content
```

---

### 组件

#### 列出组件

```http
GET /api/v1/projects/:projectId/components?limit=50&offset=0
Authorization: Bearer $SLEEK_API_KEY
```

响应 `200`:

```json
{
  "data": [
    {
      "id": "cmp_xyz",
      "name": "Hero Section",
      "activeVersion": 3,
      "versions": [{ "id": "ver_001", "version": 1, "createdAt": "..." }],
      "createdAt": "...",
      "updatedAt": "..."
    }
  ],
  "pagination": { "total": 5, "limit": 50, "offset": 0 }
}
```

---

### 聊天 — 发送消息

这是核心操作：在 `message.text` 中描述您的需求，人工智能会据此创建或修改屏幕界面。

```http
POST /api/v1/projects/:projectId/chat/messages?wait=false
Authorization: Bearer $SLEEK_API_KEY
Content-Type: application/json
idempotency-key: <optional, max 255 chars>

{
  "message": { "text": "Add a pricing section with three tiers" },
  "imageUrls": ["https://example.com/ref.png"],
  "target": { "screenId": "scr_abc" }
}
```

| 字段                    | 是否必填 | 备注                                         |
| ------------------------ | -------- | --------------------------------------------- |
| `message.text`           | 是      | 至少 1 个字符；内容需经过修剪                         |
| `imageUrls`              | 否       | 仅接受 HTTPS 格式的 URL；作为视觉辅助内容                   |
| `target.screenId`        | 否       | 指定要编辑的屏幕；省略该字段可让 AI 自动选择             |
| `?wait=true/false`       | 否       | 同步等待模式（默认：false）                         |
| `idempotency-key` header | 否       | 用于防止重复发送请求                         |

#### 响应 — 异步（默认，`wait=false`）

状态码 `202 Accepted`。在运行完成之前，`result` 和 `error` 字段均不存在。

```json
{
  "data": {
    "runId": "run_111",
    "status": "queued",
    "statusUrl": "/api/v1/projects/proj_abc/chat/runs/run_111"
  }
}
```

#### 响应 — 同步（`wait=true`）

请求处理时间最长为 **300 秒**。成功完成时返回 `200`，超时时返回 `202`。

```json
{
  "data": {
    "runId": "run_111",
    "status": "completed",
    "statusUrl": "...",
    "result": {
      "assistantText": "I added a pricing section with...",
      "operations": [
        { "type": "screen_created", "screenId": "scr_xyz", "screenName": "Pricing" },
        { "type": "screen_updated", "screenId": "scr_abc" },
        { "type": "theme_updated" }
      ]
    }
  }
}
```

---

### 聊天 — 查询运行状态

在异步发送消息后使用此端点检查进度。

```http
GET /api/v1/projects/:projectId/chat/runs/:runId
Authorization: Bearer $SLEEK_API_KEY
```

响应格式与发送消息时相同：

```json
{
  "data": {
    "runId": "run_111",
    "status": "queued",
    "statusUrl": "..."
  }
}
```

成功完成时，`result` 字段会包含结果：

```json
{
  "data": {
    "runId": "run_111",
    "status": "completed",
    "statusUrl": "...",
    "result": {
      "assistantText": "...",
      "operations": [...]
    }
  }
}
```

失败时，`error` 字段会包含错误信息：

```json
{
  "data": {
    "runId": "run_111",
    "status": "failed",
    "statusUrl": "...",
    "error": { "code": "execution_failed", "message": "..." }
  }
}
```

**运行状态生命周期**: `queued` → `running` → `completed` | `failed`

---

### 截图

用于生成一个或多个渲染组件的截图。

```http
POST /api/v1/screenshots
Authorization: Bearer $SLEEK_API_KEY
Content-Type: application/json

{
  "componentIds": ["cmp_xyz", "cmp_abc"],
  "projectId": "proj_abc",
  "format": "png",
  "scale": 2,
  "gap": 40,
  "padding": 40,
  "background": "transparent"
}
```

| 字段        | 默认值       | 备注                                                                 |
| ------------ | ------------- | --------------------------------------------------------------------- |
| `format`     | `png`         | 图片格式（png 或 webp）                                      |
| `scale`      | `2`           | 缩放比例（1–3，表示设备像素比）                             |
| `gap`        | `40`          | 组件之间的间距                                         |
| `padding`       | `40`          | 所有边的统一内边距                                         |
| `paddingX`      | _(可选)_  | 水平内边距；如果提供了 `paddingY`，则覆盖 `paddingX`             |
| `paddingY`      | _(可选)_  | 垂直内边距；如果提供了 `paddingX`，则覆盖 `paddingY`             |
| `paddingTop`    | _(可选)_  | 上边距；如果提供了 `paddingY`，则覆盖 `paddingTop`             |
| `paddingRight`  | _(可选)_  | 右边距；如果提供了 `paddingX`，则覆盖 `paddingRight`             |
| `paddingBottom` | _(可选)_  | 下边距；如果提供了 `paddingY`，则覆盖 `paddingBottom`             |
| `paddingLeft`   | _(可选)_  | 左边距；如果提供了 `paddingX`，则覆盖 `paddingLeft`             |
| `background`    | `transparent` | 背景颜色（十六进制、名称或 `transparent`）                           |
| `showDots`      | `false`       | 在背景上显示点状图案                                   |

内边距的设置遵循级联规则：先按边设置，再按轴设置，最后采用统一值。例如，`{"padding": 20, "paddingX": 10, "paddingLeft": 5}` 表示上边距 20px、右边距 10px、左边距 5px。

当 `showDots` 为 `true` 时，背景上会显示点状图案。这种效果会根据背景颜色自动调整：深色背景显示浅色点，浅色背景显示深色点。如果 `background` 设置为 `"transparent"`，则此选项无效。

除非用户明确要求特定的背景颜色，否则始终使用 `"background": "transparent"`。

响应格式为原始二进制文件 `image/png` 或 `image/webp`，附带 `Content-Disposition: attachment` 头部。

---

## 错误代码

```json
{ "code": "UNAUTHORIZED", "message": "..." }
```

| HTTP 状态码 | 错误原因                                      |
| -------- | -------------------------------------- |
| 401  | `UNAUTHORIZED`          | API 密钥缺失/无效/过期                         |
| 403  | `FORBIDDEN`             | 密钥有效，但权限范围或计划不正确                         |
| 404  | `NOT_FOUND`             | 资源不存在                         |
| 400  | `BAD_REQUEST`           | 验证失败                         |
| 409  | `CONFLICT`              | 该项目已有其他运行任务在进行中                         |
| 500  | `INTERNAL_SERVER_ERROR` | 服务器内部错误                         |

聊天运行过程中的错误（包含在 `data.error` 字段中）：

| 错误代码               | 错误原因                                      |
| ------------------ | -------------------------------- |
| `out_of_credits`   | 组织的信用额度已用尽                         |
| `execution_failed` | 人工智能执行失败                         |

---

## 流程

### 流程 1：创建项目并生成用户界面（异步 + 轮询）

```
1. POST /api/v1/projects                              → get projectId
2. POST /api/v1/projects/:id/chat/messages            → get runId (202)
3. Poll GET /api/v1/projects/:id/chat/runs/:runId
   until status == "completed" or "failed"
4. Collect screenIds from result.operations
   (screen_created and screen_updated entries)
5. Screenshot each affected screen individually
6. If any screen_created: also screenshot all project screens combined
7. Show all screenshots to the user
```

**轮询建议**: 初始轮询间隔为 2 秒，10 秒后间隔增加到 5 秒，5 分钟后停止轮询。

### 流程 2：同步模式（简单，阻塞式）

适用于简单任务或可以接受延迟的情况。

```
1. POST /api/v1/projects/:id/chat/messages?wait=true
   → blocks up to 300s
   → 200 if completed, 202 if timed out
2. If 202, fall back to Flow 1 polling with the returned runId
3. On completion, screenshot and show affected screens (see screenshot delivery rule)
```

### 流程 3：编辑特定屏幕

```
1. GET /api/v1/projects/:id/components         → find screenId
2. POST /api/v1/projects/:id/chat/messages
   body: { message: { text: "..." }, target: { screenId: "scr_xyz" } }
3. Poll or wait as above
4. Screenshot the updated screen and show it to the user
```

### 流程 4：防重复请求（确保消息的幂等性）

在发送请求时添加 `idempotency-key` 头部。如果网络中断后使用相同的密钥重新发送请求，服务器会返回之前的运行结果而不会重复创建。密钥长度应不超过 255 个字符。

```
POST /api/v1/projects/:id/chat/messages
idempotency-key: my-unique-request-id-abc123
```

### 流程 5：一次只运行一个任务（处理冲突）

每个项目只能有一个活动任务。如果在任务进行中发送新消息，会收到 `409 CONFLICT` 错误。请等待当前任务完成后再发送新消息。

```
409 response → poll existing run → completed → send next message
```

---

## 分页

所有列表端点都支持 `limit`（1–100，默认值 50）和 `offset`（≥0）。响应中始终包含 `pagination.total`，以便您可以遍历所有结果。

```http
GET /api/v1/projects?limit=10&offset=20
```

---

## 常见错误及解决方法

| 错误类型                                         | 解决方法                                                                 |
| --------------------------------------------------- | ------------------------------------------------------------------------------- |
| 未在请求中添加 `Authorization` 头部             | 在每个请求中添加 `Authorization: Bearer $SLEEK_API_KEY`         |
| 使用错误的权限范围                         | 确保密钥的权限范围与端点匹配（例如，发送消息时使用 `chats:write`）         |
| 在任务未完成前发送下一条消息                   | 在发送新消息前，等待任务完成或失败                   |
| 在长时间生成截图时使用 `wait=true`                 | 最长阻塞时间为 300 秒；失败时切换为轮询方式                   |
| 在 `imageUrls` 中使用非 HTTPS URL                         | 仅接受 HTTPS 格式的 URL                         |
| 误以为 `202` 状态码表示任务已完成                   | 实际上 `result` 字段仅在任务完成时才会出现                   |