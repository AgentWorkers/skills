---
name: self-integration
description: 您可以连接到任何外部应用程序，并在其上执行操作。当用户需要与外部服务（如 Slack、Linear、HubSpot、Salesforce、Jira、GitHub、Google Sheets 或其他应用程序）进行交互时，可以使用此功能——发送消息、创建任务、同步数据、管理联系人或执行任何 API 操作。
license: MIT
metadata:
  author: Membrane Inc
  version: "1.0.0"
  homepage: https://getmembrane.com
  openclaw:
    requires:
      env:
        - MEMBRANE_TOKEN
        - MEMBRANE_API_URL
    primaryEnv: MEMBRANE_TOKEN
    homepage: https://getmembrane.com
---

# 自我集成

您可以连接到任何外部应用程序并对其实行操作。该功能使用了 [Membrane](https://getmembrane.com) 的 API。

## 发送 API 请求

所有请求都会发送到 `${MEMBRANE_API_URL:-https://api.getmembrane.com}`，并需要携带 Bearer 令牌：

```
Authorization: Bearer $MEMBRANE_TOKEN
Content-Type: application/json
```

请从 [Membrane 控制面板](https://console.getmembrane.com) 获取 API 令牌。

## 工作流程

### 第 1 步：建立连接

连接是通往外部应用程序的认证链接（例如用户的 Slack 工作空间或 HubSpot 账户）。在执行任何操作之前，您需要先建立连接。

#### 1a. 检查现有连接

`GET /connections`

查找与目标应用程序匹配的连接。关键字段：`id`、`name`、`connectorId`、`disconnected`。

如果找到匹配的连接且 `disconnected` 的值为 `false`，则直接进入 **第 2 步**。

#### 1b. 查找连接器

连接器是针对外部应用程序预先构建的适配器。可以通过应用程序名称进行搜索：

`GET /search?q=slack`

查找结果中 `elementType` 为 “connector” 的条目。使用 `element.id` 作为后续步骤中的 `connectorId`。

如果没有找到合适的连接器，请进入步骤 1c 来创建一个新的连接器。

#### 1c. 创建连接器（如果不存在）

创建一个 Membrane Agent 会话以构建连接器：

`POST /agent/sessions`，请求体为 `{"prompt": "为 Slack (https://slack.com) 创建连接器"}`

根据实际需求调整提示信息。然后通过 `GET /agent/sessions/{sessionId}?wait=true&timeout=30` 进行轮询，直到 `state` 为 “idle” 或 `status` 为 “completed”。

您可以通过 `POST /agent/sessions/{sessionId}/message` 发送后续指令，或通过 `POST /agent/sessions/{sessionId}/interrupt` 中断会话。

连接器创建完成后，再次进行搜索（步骤 1b）。

#### 1d. 提交连接请求

提交连接请求，以便用户能够使用该连接进行身份验证：

`POST /connection-requests`，请求体为 `{"connectorId": "cnt_abc123}`

响应中会包含一个 `url`。**请用户打开该 `url` 以完成身份验证**（例如通过 OAuth 或 API 密钥）。

#### 1e. 检查连接结果

持续轮询，直到用户完成身份验证：

`GET /connection-requests/{requestId}`

- `status: "pending"` — 用户尚未完成身份验证，继续轮询。
- `status: "success"` — 身份验证成功。将 `resultConnectionId` 作为后续使用的连接 ID。
- `status: "error"` — 身份验证失败，请查看 `resultError` 以获取详细信息。

### 第 2 步：获取操作

操作是在已连接的应用程序上可以执行的操作（例如 “创建任务”、“发送消息” 或 “列出联系人”）。

#### 2a. 搜索操作

使用自然语言描述您想要执行的操作来搜索：

`GET /actions?connectionId=con_abc123&intent=send+a+message&limit=10`

每个搜索结果都会包含 `id`、`name`、`description`、`inputSchema`（操作接受的参数）和 `outputSchema`（操作返回的数据）。

如果没有合适的操作，请进入步骤 2b。

#### 2b. 创建操作（如果不存在）

使用 Membrane Agent。请务必在提示信息中包含连接 ID：

`POST /agent/sessions`，请求体为 `{"prompt": "为连接 con_abc123 创建一个发送消息的工具"}`

根据实际需求调整提示信息。与步骤 1c 中的方式相同，进行轮询以完成操作创建。操作创建完成后，再次进行搜索（步骤 2a）。

### 第 3 步：执行操作

使用步骤 2 中获得的操作 ID 和步骤 1 中获得的连接 ID 来执行操作：

`POST /actions/{actionId}/run?connectionId=con_abc123`，请求体为 `{"input": {"channel": "#general", "text": "Hello!"}``

提供符合操作 `inputSchema` 要求的参数。

操作的结果将包含在响应的 `output` 字段中。

## API 参考

基础 URL：`${MEMBRANE_API_URL:-https://api.getmembrane.com}`

认证头：`Authorization: Bearer $MEMBRANE_TOKEN`

### GET /connections

列出所有连接。

响应内容：```json
{
  "items": [
    {
      "id": "string",
      "name": "string",
      "connectorId": "string",
      "integrationId": "string (optional)",
      "disconnected": "boolean",
      "state": "NOT_CONFIGURED | SETUP_IN_PROGRESS | SETUP_FAILED | READY",
      "error": "object (optional)",
      "createdAt": "datetime",
      "updatedAt": "datetime"
    }
  ]
}
```

### GET /search

根据关键词搜索工作空间元素。

查询参数：

| 参数 | 类型 | 说明 |
|---|---|---|
| `q` | 字符串（必填） | 搜索查询（1-200 个字符） |
| `elementType` | 字符串（可选） | 按类型过滤：`Connector`、`Integration`、`Action` 等 |
| `limit` | 数字（可选） | 最大结果数量（1-100） |

响应内容：```json
{
  "items": [
    {
      "elementType": "Connector",
      "element": {
        "id": "string",
        "name": "string",
        "logoUri": "string (optional)"
      }
    }
  ]
}
```

### POST /connection-requests

提交连接请求以进行用户身份验证。

请求体（至少需要提供一个标识符）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `connectorId` | 字符串 | 连接器 ID |
| `integrationId` | 字符串 | 集成 ID（可选） |
| `integrationKey` | 字符串 | 集成密钥（可选） |
| `connectionId` | 字符串 | 现有连接 ID（用于重新连接） |
| `name` | 字符串 | 自定义连接名称 |
| `connectorVersion` | 字符串 | 连接器版本 |
| `connectorParameters` | 对象 | 连接器特定的参数 |

响应内容：```json
{
  "requestId": "string",
  "url": "string",
  "status": "pending | success | cancelled | error",
  "connectorId": "string (optional)",
  "integrationId": "string (optional)",
  "resultConnectionId": "string (optional, set on success)",
  "resultError": "object (optional, set on error)",
  "createdAt": "datetime"
}
```

### GET /connection-requests/:requestId

检查连接请求的状态。响应格式与 POST 请求相同。

### GET /actions

列出或搜索操作。

查询参数：

| 参数 | 类型 | 说明 |
|---|---|---|
| `connectionId` | 字符串 | 按连接进行过滤 |
| `integrationId` | 字符串 | 按集成进行过滤 |
| `intent` | 字符串 | 自然语言搜索（最多 200 个字符） |
| `limit` | 数字 | 最大结果数量（默认为 10） |

响应内容：```json
{
  "items": [
    {
      "id": "string",
      "name": "string",
      "key": "string",
      "description": "string (optional)",
      "type": "string",
      "inputSchema": "JSON Schema (optional)",
      "outputSchema": "JSON Schema (optional)",
      "integrationId": "string (optional)",
      "connectionId": "string (optional)"
    }
  ]
}
```

### POST /actions/:actionId/run

执行操作。

查询参数：

| 参数 | 类型 | 说明 |
|---|---|---|
| `connectionId` | 字符串 | 要执行操作的连接 |
| `input` | 任意类型 | 符合操作 `inputSchema` 要求的参数 |

响应内容：```json
{
  "output": "any"
}
```

### POST /agent/sessions

创建一个 Membrane Agent 会话以构建连接器或操作。

请求体：

| 字段 | 类型 | 说明 |
|---|---|---|
| `prompt` | 字符串（必填） | 任务描述 |

响应内容：```json
{
  "id": "string",
  "status": "queued | starting | running | completed | failed | cancelled",
  "state": "busy | idle",
  "prompt": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

### GET /agent/sessions/:id

获取 Agent 会话的状态。

查询参数：

| 参数 | 类型 | 说明 |
|---|---|---|
| `wait` | 布尔值 | 如果设置为 `true`，则会长时间轮询，直到会话变为空闲状态或超时 |
| `timeout` | 数字 | 最大等待时间（秒，默认为 30） |

响应格式与 POST /agent/sessions 相同。

### POST /agent/sessions/:id/message

向正在运行的 Agent 会话发送后续消息。

请求体：

| 字段 | 类型 | 说明 |
|---|---|---|
| `input` | 字符串（必填） | 要发送的消息 |

响应格式与 POST /agent/sessions 相同。

### POST /agent/sessions/:id/interrupt

中断一个正在运行的 Agent 会话。

响应内容：```json
{
  "interrupted": "boolean"
}
```

## 外部端点

所有请求都会发送到 Membrane API。此技能不会直接与其他外部服务进行交互。

| 端点 | 发送的数据 |
|---|---|
| `${MEMBRANE_API_URL:-https://api.getmembrane.com}/*` | API 令牌、连接参数、操作输入、Agent 提示信息 |

## 安全性与隐私

- 所有数据均通过 HTTPS 发送到 Membrane API。
- `MEMBRANE_TOKEN` 是一个高权限凭证，可用于创建连接并在外部应用程序中执行操作。请将其视为机密信息。
- 连接身份验证（OAuth、API 密钥）由 Membrane 处理——外部应用程序的凭证由 Membrane 服务存储，而非本地存储。
- 操作的输入和输出数据会通过 Membrane API 传递给连接的目标应用程序。

使用此技能时，数据会发送到 [Membrane](https://getmembrane.com)。只有在您信任 Membrane 并允许其访问您的连接应用程序的情况下，才应安装此技能。