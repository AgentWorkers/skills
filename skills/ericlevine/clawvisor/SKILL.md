---
name: clawvisor
description: 通过 Clawvisor 路由工具请求，以实现凭证管理、基于任务的授权以及人工审批流程。该功能适用于 Gmail、Calendar、Drive、Contacts、GitHub 和 iMessage（macOS）等应用。Clawvisor 负责执行各种限制措施、管理任务权限，并负责注入凭证；代理程序从不直接处理敏感信息（即凭证）。
version: 0.2.0
homepage: https://github.com/clawvisor/clawvisor
metadata:
  openclaw:
    requires_env:
      - CLAWVISOR_URL
      - CLAWVISOR_AGENT_TOKEN
      - OPENCLAW_HOOKS_URL
    user_setup:
      - "Set CLAWVISOR_URL to your Clawvisor instance URL"
      - "Create an agent in the Clawvisor dashboard, copy the token, then run: openclaw credentials set CLAWVISOR_AGENT_TOKEN"
      - "Set OPENCLAW_HOOKS_URL to your OpenClaw gateway URL (default http://localhost:18789)"
      - "Activate services in the dashboard under Services"
---
# Clawvisor 技能

## 概述

Clawvisor 作为您与外部 API 之间的桥梁：您声明需要执行的操作，用户批准操作的范围，Clawvisor 负责处理凭证注入、执行操作以及审计日志记录。您无需保管 API 密钥。

授权机制分为三个层级，按顺序执行：

1. **限制**——由用户设置的硬性规则。匹配的请求会立即被阻止。
2. **任务**——您预先批准的操作范围。属于该范围内的操作（且设置了 `auto_execute` 属性）可以无需每次请求都进行批准即可自动执行。
3. **每次请求的批准**——适用于未包含在预先批准任务中的操作。

在每次会话开始时，请获取您的服务目录，以查看可用的服务：

```
GET $CLAWVISOR_URL/api/skill/catalog
Authorization: Bearer $CLAWVISOR_AGENT_TOKEN
```

---

## 典型流程

1. 获取服务目录，确认服务是否可用且操作未被限制。
2. 创建一个任务，声明您的操作目的及所需执行的操作。
3. 告知用户进行批准，并等待回调（或进行轮询）。
4. 根据任务执行相应的操作；属于该范围内的操作会自动执行。
5. 操作完成后，标记任务为已完成。

对于一次性操作，可以直接跳过任务创建步骤，直接进行每次请求的批准。

---

## 任务创建

创建一个任务时，需要指定 `purpose`（操作目的）、`authorized_actions`（允许执行的操作列表）以及 `TTL`（任务的有效期限）。所有任务初始状态均为 `pending_approval`。

```bash
curl -s -X POST "$CLAWVISOR_URL/api/tasks" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "purpose": "Review last 30 iMessage threads and classify reply status",
    "authorized_actions": [
      {
        "service": "apple.imessage",
        "action": "list_threads",
        "auto_execute": true,
        "expected_use": "List recent threads to find ones needing replies"
      },
      {
        "service": "apple.imessage",
        "action": "get_thread",
        "auto_execute": true,
        "expected_use": "Read individual threads to classify reply status"
      }
    ],
    "expires_in_seconds": 1800,
    "callback_url": "${OPENCLAW_HOOKS_URL}/clawvisor/callback?session=<session_key>"
  }'
```

- **`purpose`**——在用户审批过程中显示，并用于验证操作是否符合预期目的。请确保描述具体明确。
- **`expected_use`**——每项操作的详细使用说明。在审批过程中也会显示。描述越详细越好。
- **`auto_execute`**——如果设置为 `true`，则属于该范围内的操作会立即执行；如果设置为 `false`，则每次请求仍需进行批准（例如发送消息等可能具有破坏性的操作）。
- **`expires_in_seconds`**——如果省略此字段，则将任务的有效期限设置为 `"lifetime": "standing"`，即任务会一直有效，直到用户手动撤销。

**扩展任务范围**——如果您需要执行原本不在任务范围内的操作，请执行以下步骤：

```bash
curl -s -X POST "$CLAWVISOR_URL/api/tasks/<task-id>/expand" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "apple.imessage",
    "action": "send_message",
    "auto_execute": false,
    "reason": "User asked me to reply to this thread"
  }'
```

## 完成任务

```bash
curl -s -X POST "$CLAWVISOR_URL/api/tasks/<task-id>/complete" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN"
```

---

## 网关请求

一旦任务被激活，在每个请求中都必须包含 `task_id`：

```bash
curl -s -X POST "$CLAWVISOR_URL/api/gateway/request" \
  -H "Authorization: Bearer $CLAWVISOR_AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "apple.imessage",
    "action": "get_thread",
    "params": {"thread_id": "+15551234567", "max_results": 5},
    "reason": "Checking if this thread needs a reply",
    "request_id": "<unique-id>",
    "task_id": "<task-uuid>",
    "context": {
      "source": "user_message",
      "data_origin": null,
      "callback_url": "${OPENCLAW_HOOKS_URL}/clawvisor/callback?session=<session_key>"
    }
  }'
```

- **`reason`**——简短的一句话，用于在审批过程和审计日志中显示。描述要具体明确。
- **`request_id`**——每个请求的唯一标识符，用于关联回调请求以及进行幂等性轮询。
- **`data_origin`**——影响此次请求的任何外部内容的来源（例如 `"gmail:msg-abc123"`、`https://example.com` 或 GitHub 问题链接）。仅当操作完全基于用户消息时，才将此字段设置为 `null`。这对于追踪请求来源至关重要（尤其是在处理外部数据时）。

**响应状态**：

| 状态 | 含义 | 应采取的措施 |
|---|---|---|
| `executed` | 操作已完成 | 可使用 `result.summary` 和 `result.data` 获取结果。 |
| `pending` | 正在等待批准 | 告知用户并等待回调；切勿重试。 |
| `blocked` | 触发了硬性限制 | 直接将错误信息告知用户；切勿尝试绕过限制。 |
| `restricted` | 操作目的验证失败 | 调整请求参数或原因，并使用新的 `request_id` 重新尝试。 |
| `pending_task_approval` | 任务尚未获得批准 | 等待任务回调。 |
| `pending_scope_expansion` | 操作超出了任务允许的范围 | 调用 `POST /api/tasks/{id}/expand` 来扩展任务范围。 |
| `task_expired` | 任务已过期 | 扩展任务范围或创建新任务。 |
| `error` (`SERVICE_NOT_CONFIGURED`) | 服务未配置 | 请用户通过控制面板激活该服务。 |
| `error`（其他原因） | 执行失败 | 向用户报告错误；切勿默默重试。 |

---

## 回调与轮询

所有回调请求都包含一个 `type` 字段（`"request"` 或 `"task"`），以便正确处理这些请求。

**请求已处理**：
```json
{
  "type": "request",
  "request_id": "req-001",
  "status": "executed",
  "result": {"summary": "...", "data": {...}},
  "audit_id": "a8f3..."
}
```
请求状态：`executed`、`denied`、`timeout`、`error`。

**任务状态变化**：
```json
{
  "type": "task",
  "task_id": "<task-id>",
  "status": "approved"
}
```
任务状态：`approved`、`denied`、`scope_expanded`、`scope_expansion_denied`、`expired`。

**回调 URL（OpenClaw）**：
```
${OPENCLAW_HOOKS_URL}/clawvisor/callback?session=<session_key>
```
从 `session_status`（🧵 会话字段）中获取 `session_key`。

**回调验证**——为了确认回调请求确实来自 Clawvisor，请为每个代理注册一个签名密钥：
```
POST $CLAWVISOR_URL/api/callbacks/register
Authorization: Bearer $CLAWVISOR_AGENT_TOKEN
```
将返回的 `callback_secret` 存储为 `CLAWVISOR_CALLBACK_SECRET`，并通过检查 `X-Clawvisor-Signature` 是否等于 `sha256=` + `HMAC-SHA256(body, secret)` 来验证回调请求的真实性。

**轮询**——如果您没有提供 `callback_url`，请使用相同的 `request_id` 重新发送请求。Clawvisor 会识别该请求并返回当前状态，而无需重新执行操作。

---

## 常见问题与解答

**收到 “401 Unauthorized” 错误**：
您的令牌无效或已丢失。令牌在创建任务时会被显示一次；请在控制面板中生成新的令牌。

**所需的服务不在服务目录中**：
请在控制面板的 “服务” 页面中激活该服务。Google 服务（Gmail、Calendar、Drive、Contacts）共享同一个 OAuth 连接。

**请求一直处于 “pending” 状态**：
为该操作创建一个 `auto_execute` 为 `true` 的任务，或者让用户通过 “审批” 面板进行批准。

**收到 “restricted” 错误**：
操作目的验证失败——您的请求参数或原因与任务声明的目的不匹配。响应中的 `reason` 字段会说明具体问题。调整参数后使用新的 `request_id` 重新尝试。

**被拒绝（显示 “blocked”）**：
`reason` 字段中列出了具体的限制原因。请将原因原样告知用户，切勿自行猜测或尝试绕过限制。