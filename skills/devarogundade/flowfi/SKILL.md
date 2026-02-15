---
name: flowfi
description: FlowFi工作流操作的REST API说明——包括授权、智能账户管理、生成工作流、获取建议、通过提示进行编辑、部署工作流、卸载工作流以及创建工作流草稿等功能。这些API可用于与后端API集成，或在用户需要了解工作流或授权相关端点信息时使用。
---

# 工作流 REST API

以下是 FlowFi REST 端点的使用说明。基础 URL 为后端 API 的根路径（例如：`https://api.example.com`）。使用工作流和智能账户相关功能时，需要 **JWT** 令牌（详见授权部分）。

## 功能

您可以使用该 API 完成以下操作：

- **列出智能账户** — 使用 `GET /smart-accounts` 获取用户的智能账户信息，并在生成工作流时使用 `id` 作为 `smartAccountId`。
- **根据提示生成工作流** — 使用 `POST /ai/generate-workflow` 发送请求，例如：`{"prompt": "当 ETH 价格超过 3000 时通知我", "smartAccountId": "..."}`，以创建一个新的工作流草稿。
- **获取编辑建议** — 使用 `GET /ai/workflow/:id/suggestions` 获取 AI 提供的编辑建议（例如：“添加延迟”或“添加通知”）。
- **根据提示编辑工作流** — 使用 `POST /ai/workflow/:id/prompt` 发送请求，例如：`{"prompt": "在通知前添加 5 秒的延迟"}`，以修改现有的工作流草稿。
- **部署工作流** — 使用 `POST /workflows/:id/deploy` 将工作流草稿激活并使其可执行。
- **取消部署工作流** — 使用 `POST /workflows/:id/undeploy` 停止工作流的执行，并将其恢复为草稿状态，以便进一步编辑。

## 示例提示

**生成工作流**（请求体中的 `prompt`）：
- “当 ETH 价格超过 3500 时，通过 Telegram 发送消息给我”
- “每天上午 9 点检查 Uniswap 上的 WETH/USDC 并将价格发布到 Discord”
- “如果 gas 低于 20 gwei，在 Uniswap 上执行交易并通知我”

**编辑工作流**（请求体中的 `prompt`）：
- “在价格检查后添加 10 秒的延迟”
- “将阈值修改为 4000”
- “工作流执行时发送电子邮件通知”

---

## 授权

用户需要生成一个 JWT 令牌（例如通过应用程序生成），并将其发送给 OpenClaw。所有后续的 API 调用都必须使用该令牌。

**长期有效的 API 令牌（bearer）：** 使用 `POST` 请求 `/auth/bearer-token`  
请求头中必须包含 `Authorization: Bearer <token>`，并且需要提供有效的 JWT 令牌。

| 字段                | 类型   | 是否必需 | 描述                |
|--------------------|--------|------------------|-------------------------|
| `expiresInSeconds` | 数字    | 是       | 令牌的有效时间（60–31536000 秒，即 1 年）         |
|                    |        |                    |

响应：一个新的 JWT 令牌，用于后续的 API 调用，格式为 `Authorization: Bearer <token>`。

**撤销所有 bearer 令牌：** 使用 `POST` 请求 `/auth/bearer-token/revoke`（需要提供 JWT 令牌）。此操作不会影响会话登录令牌。

**使用令牌：** 对于所有受保护的 API 路由，需要在请求头中添加：  
`Authorization: Bearer <your-jwt>`。

---

## 获取智能账户信息

- **列出智能账户**：`GET /smart-accounts`  
需要 JWT 令牌。返回已认证用户的智能账户列表。支持分页：`page`、`limit`、`sortBy`、`sortOrder`、`search`（查询参数）。
- **获取单个智能账户**：`GET /smart-accounts/:id`  
需要 JWT 令牌。用户必须拥有该智能账户。
- **获取智能账户的工作流数量**：`GET /smart-accounts/:id/workflows/count`  
响应格式：`{"count": 数字}`。

在调用 `POST /ai/generate-workflow` 或创建工作流时，可以使用这些端点返回的智能账户 `id` 作为 `smartAccountId`。

---

## 生成工作流

**POST /ai/generate-workflow**

根据用户提供的自然语言提示，使用 AI 生成新的工作流。新工作流的状态为 **draft**（草稿）。

**请求体（JSON）：**

| 字段            | 类型     | 是否必需 | 描述                          |
|-----------------|--------|------------------|--------------------------------------|
| `prompt`         | 字符串    | 是       | 用户对工作流的描述                    |
| `smartAccountId`     | 字符串    | 是       | 需要关联的智能账户 ID                    |

**示例：**

```json
{
  "prompt": "When ETH price drops below 2000, send a Telegram notification",
  "smartAccountId": "0x..."
}
```

**响应：** `200` — 返回包含 `id`、`name`、`nodes`、`connections` 的工作流对象。

---

## 获取工作流编辑建议

**GET /ai/workflow/:id/suggestions**

返回针对工作流的 AI 生成的建议（例如：4 条可操作的编辑建议）。这些建议用于 “使用 AI 编辑工作流” 界面。

**路径说明：** `id` 必须与工作流的 ID 相匹配，且请求者必须具有该工作流的权限。

**响应：** `200` — 返回一个包含建议的数组：`{"suggestions": 字符串[]}`。

---

## 根据提示编辑工作流

**POST /ai/workflow/:id/prompt**

根据用户提供的提示编辑现有的工作流。可以修改工作流的名称、节点、连接和变量。请确保工作流处于 **draft**（草稿）状态（如果已部署，则需要先取消部署）。

**路径说明：** `id` 必须与工作流的 ID 相匹配。

**请求体（JSON）：**

| 字段            | 类型     | 是否必需 | 描述                          |
|-----------------|--------|------------------|--------------------------------------|
| `prompt`         | 字符串    | 是       | 编辑指令（例如：“添加 5 秒的延迟”）                   |

**响应：** `200` — 返回更新后的工作流信息：`{"message": 字符串, "workflow": 工作流对象}`。

---

## 部署工作流

**POST /workflows/:id/deploy**

将工作流部署为可执行状态（可以安排执行或触发）。工作流必须处于 **draft** 或 **ended**（已完成）状态，并且必须关联一个智能账户。

**路径说明：** `id` 必须与工作流的 ID 相匹配。

**响应：** `200` — 表示工作流已成功部署，状态变为 `active`。

**错误代码：** `400` — 如果工作流已部署或未关联智能账户。

---

## 取消部署工作流

**POST /workflows/:id/undeploy**

停止已部署的工作流，并将其状态恢复为 **draft**。在编辑已部署的工作流之前必须执行此操作。

**路径说明：** `id` 必须与工作流的 ID 相匹配。

**响应：** `200` — 表示工作流状态已更新为 `draft`。

**错误代码：** `400` — 如果工作流未部署（例如：已经是草稿状态或已被归档）。

---

## 工作流管理

- **创建草稿**：`POST /ai/generate-workflow` 和 `POST /workflows` 都可以创建状态为 **draft** 的工作流。
- **列出草稿工作流**：`GET /workflows?status=draft`（可选查询参数）。
- **编辑草稿工作流**：只有处于草稿或已完成状态的工作流才能被编辑。可以使用 `POST /ai/workflow/:id/prompt` 或 `PATCH /workflows/:id` 来编辑草稿工作流。
- **部署工作流**：准备好后，使用 `POST /workflows/:id/deploy` 将草稿工作流激活为可执行状态。

---

## 功能概览

| 功能                | 方法     | 对应的 API 端点                         |
|-------------------|--------|----------------------------------------|
| 生成工作流           | POST     | /ai/generate-workflow                   |
| 获取工作流建议       | GET     | /ai/workflow/:id/suggestions         |
| 根据提示编辑工作流       | POST     | /ai/workflow/:id/prompt                 |
| 部署工作流           | POST     | /workflows/:id/deploy                   |
| 取消部署工作流         | POST     | /workflows/:id/undeploy                   |

所有受保护的 API 路由都需要使用 `Authorization: Bearer <jwt>` 进行身份验证。用户身份通过 JWT 令牌确定；工作流和智能账户的所有权通过 `smartAccountAddress` 或 `userId` 进行验证。