---
name: hitl-protocol
description: "HITL协议——一种用于自主代理工作流程中处理人类决策的开放标准。当网站或API需要人类输入时，会返回HTTP 202状态码，并附带一个审核URL。像OpenClaw、Claude、Codex或Goose这样的自主代理会转发该URL，定期检查处理结果，然后继续执行后续操作。利用这一协议，您可以轻松地将任何网站适配为适合代理使用的系统，或在代理中实现需要人类参与的处理流程（例如审批、选择、填写表单、确认等）。该协议支持多种交互方式，包括轮询、SSE（Server-Sent Events）传输机制、基于特定渠道的交互按钮（如Telegram、Slack、Discord、WhatsApp、Teams），以及不透明的令牌安全机制。此外，还支持多步骤表单引导和多轮编辑流程。"
license: Apache-2.0
compatibility:
  - claude
  - codex
  - gemini
  - openclaw
  - goose
  - copilot
metadata:
  version: "0.7"
  spec_url: "https://github.com/rotorstar/hitl-protocol/blob/main/spec/v0.7/hitl-protocol.md"
  hitl:
    supported: true
    types: [approval, selection, input, confirmation, escalation]
    info: "Teaches the HITL Protocol itself — for building HITL services and HITL-aware agents."
---
# HITL 协议

人工智能代理越来越多地代表用户访问网站和服务：进行搜索、预订、申请、购买等操作。但某些决策过于重要，不能完全交给代理来处理——代理可能会出现幻觉、误解，或在关键时刻做出错误的选择：例如取消错误的保险政策、预订到错误城市的不可退款旅行、将资金转错账户。HITL 协议（“Human in the Loop”，即“人在回路中”）是一个开放标准，确保人类在这些关键时刻仍能保持控制权。用户可以继续使用他们喜欢的消息应用（如 Telegram、WhatsApp、Slack），直接点击决策按钮，或者点击链接进入一个具有友好用户界面的网页（包含卡片、表单、按钮等）。没有冗长的文本，也没有代理的盲目决策。当遇到 HITL 响应时，应告知用户需要人类进行决策，并提供便捷的操作方式：显示审核链接或渲染操作按钮。

HITL 协议对于人类决策而言，就如同 OAuth 对于身份验证一样——它是一个连接 **服务**、**代理** 和 **人类** 的开放标准。当服务需要人类输入时，它会返回 HTTP 202 响应，并附带一个审核链接。代理将此链接转发给人类，人类在浏览器中打开页面并做出明智的决策。之后代理会轮询结构化结果并继续处理流程。

对于简单的决策（确认/取消、批准/拒绝），代理可以直接在 Telegram、Slack、Discord、WhatsApp 或 Teams 中渲染 **原生消息按钮**，无需使用浏览器。服务需要通过 `submit_url` 来启用此功能。

**无需 SDK，也不强制使用任何用户界面框架。只需 HTTP、URL 和轮询即可。**

**[交互式测试平台](https://rotorstar.github.io/hitl-protocol/playground/index.html)** — 你可以在浏览器中实时尝试各种审核类型、传输方式和内联操作。**

## 你是什么角色？

| 角色 | 你需要... | 阅读内容 |
|-----------|----------------|------|
| 服务/网站开发者 | 在你的 API 中添加 HITL 端点，以便代理可以请求人类输入 | [服务集成指南](skills/references/service-integration.md) |
| 代理开发者 | 处理来自服务的 HTTP 202 响应和 HITL 回应 | [代理集成指南](skills/references/agent-integration.md) |
| 两者都需要/学习者 | 了解整个协议 | 继续阅读以下内容 |

## 流程

```
Standard flow (all review types):
1. Human → Agent:    "Find me jobs in Berlin"
2. Agent → Service:  POST /api/search {query: "Senior Dev Berlin"}
3. Service → Agent:  HTTP 202 + hitl object (review_url, poll_url, type, prompt)
4. Agent → Human:    "Found 5 jobs. Review here: {review_url}"
5. Human → Browser:  Opens review_url → rich UI (cards, forms, buttons)
6. Human → Service:  Makes selection, clicks Submit
7. Agent → Service:  GET {poll_url} → {status: "completed", result: {action, data}}
8. Agent → Human:    "Applied to 2 selected jobs."

Inline flow (v0.7 — simple decisions only, when submit_url present):
1. Human → Agent:    "Send my application emails"
2. Agent → Service:  POST /api/send {emails: [...]}
3. Service → Agent:  HTTP 202 + hitl object (incl. submit_url, submit_token, inline_actions)
4. Agent → Human:    Native buttons in chat: [Confirm] [Cancel] [Details →]
5. Human → Agent:    Taps [Confirm] in chat
6. Agent → Service:  POST {submit_url} {action: "confirm", submitted_via: "telegram"}
7. Service → Agent:  200 OK {status: "completed"}
8. Agent → Human:    Updates message: "Confirmed — 3 emails sent."
```

代理从不渲染用户界面。审核页面由服务方托管。敏感数据始终保留在浏览器中，不会经过代理。对于简单的决策，内联流程是一个可选的快捷方式。

## 功能矩阵

| 功能 | 详情 |
|---------|---------|
| **审核类型** | `approval`（批准）、`selection`（选择）、`input`（输入）、`confirmation`（确认）、`escalation`（升级） |
| **表单字段类型** | `text`（文本）、`textarea`（文本区域）、`number`（数字）、`date`（日期）、`email`（电子邮件）、`url`（网址）、`boolean`（布尔值）、`select`（下拉菜单）、`multiselect`（多选）、`range`（范围）、自定义 `x-*` |
| **传输方式** | 轮询（必需）、SSE（可选）、回调/Webhook（可选） |
| **内联提交** | `submit_url` + 原生消息按钮（Telegram、Slack、Discord、WhatsApp、Teams）——服务需启用 |
| **状态** | `pending`（待处理）→ `opened`（已打开）→ `in_progress`（进行中）→ `completed`（完成）/ `expired`（过期）/ `cancelled`（取消） |
| **安全性** | 不透明的令牌（43 个字符，base64url 格式，256 位熵值），SHA-256 哈希存储，时间安全的比较方式，仅使用 HTTPS |
| **多轮决策** | `previous_case_id`（上一个案例 ID）/ `next_case_id`（下一个案例 ID）用于迭代编辑周期（仅限批准类型） |
| **表单** | 单步字段、多步向导、条件显示、验证规则、进度跟踪 |
| **超时设置** | ISO 8601 时间格式，`default_action`（默认操作）：`skip`（跳过）/ `approve`（批准）/ `reject`（拒绝）/ `abort`（中止） |
| **发现机制** | `.well-known/hitl.json` 文件，SKILL.md 文件中的 `metadata.hitl` 扩展名 |
| **提醒** | `reminder_at` 时间戳，`review.reminder` SSE 事件 |
| **速率限制** | 每个案例每分钟 60 次请求限制，`Retry-After` 头部字段 |

## 五种审核类型

| 类型 | 可执行的操作 | 是否支持多轮决策 | 是否需要表单字段 | 使用场景 |
|------|---------|:-----------:|:-----------:|----------|
| **批准** | `approve`（批准）、`edit`（编辑）、`reject`（拒绝） | 是 | 文档审核（如简历、电子邮件、部署计划） |
| **选择** | `select`（选择） | 否 | 从选项中选择（如职位列表、目标对象） |
| **输入** | `submit`（提交） | 否 | 是 | 结构化数据输入（如薪资、日期、偏好设置） |
| **确认** | `confirm`（确认）、`cancel`（取消） | 否 | 不可逆的操作（如发送邮件、部署） |
| **升级** | `retry`（重试）、`skip`（跳过）、`abort`（中止） | 否 | 错误恢复（如部署失败、API 错误） |

## HITL 对象（HTTP 202 响应体）

当服务需要人类输入时，它会返回如下结构的 HTTP 202 响应：

```json
{
  "status": "human_input_required",
  "message": "5 matching jobs found. Please select which ones to apply for.",
  "hitl": {
    "spec_version": "0.7",
    "case_id": "review_abc123",
    "review_url": "https://service.example.com/review/abc123?token=K7xR2mN4pQ...",
    "poll_url": "https://api.service.example.com/v1/reviews/abc123/status",
    "type": "selection",
    "prompt": "Select which jobs to apply for",
    "timeout": "24h",
    "default_action": "skip",
    "created_at": "2026-02-22T10:00:00Z",
    "expires_at": "2026-02-23T10:00:00Z",
    "context": {
      "total_options": 5,
      "query": "Senior Dev Berlin"
    }
  }
}
```

### 必需字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `spec_version` | `"0.7"` | 协议版本 |
| `case_id` | 字符串 | 唯一的、适合 URL 的标识符（格式：`review_{random}`） |
| `review_url` | URL | 包含不透明令牌的审核页面 URL |
| `poll_url` | URL | 状态轮询端点 |
| `type` | 枚举 | `approval`（批准）/ `selection`（选择）/ `input`（输入）/ `confirmation`（确认）/ `escalation`（升级）/ `x-*` |
| `prompt` | 字符串 | 人类需要做出的决策内容（最多 500 个字符） |
| `created_at` | 字符串 | ISO 8601 格式的创建时间戳 |
| `expires_at` | 字符串 | ISO 8601 格式的过期时间戳 |

### 可选字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `timeout` | 字符串 | 审核页面的开放时长（`24h`、`PT24H`、`P7D`） |
| `default_action` | 枚举 | `skip`（跳过）/ `approve`（批准）/ `reject`（拒绝）/ `abort`（中止）——过期时的默认操作 |
| `callback_url` | URL | 如果代理提供了回调 URL，则返回该 URL |
| `events_url` | URL | 实时状态事件的 SSE 端点 |
| `context` | 对象 | 用于审核页面的任意数据（代理不会处理） |
| `reminder_at` | 字符串 | 重新发送审核链接的时间 |
| `previous_case_id` | 字符串 | 多轮决策中的上一个案例链接 |
| `surface` | 对象 | 用户界面格式声明（`format`、`version`） |
| `submit_url` | URL | 用于在聊天应用中显示原生按钮的提交端点（v0.7 版本） |
| `submit_token` | 字符串 | `submit_url` 需要的认证令牌（如果设置了 `submit_url` 则必需） |
| `inline_actions` | 字符串数组 | 通过 `submit_url` 允许的操作（例如 `["confirm", "cancel"]`）。如果未设置，则允许该类型的全部操作 |

## 轮询响应（完成状态）

```json
{
  "status": "completed",
  "case_id": "review_abc123",
  "completed_at": "2026-02-22T10:15:00Z",
  "result": {
    "action": "select",
    "data": {
      "selected_jobs": ["job-123", "job-456"],
      "note": "Only remote positions"
    }
  }
}
```

只有当 `status` 为 `"completed"` 时，`result` 对象才会出现。它总是包含 `action`（字符串）和 `data`（根据类型不同的内容对象）。

### 轮询响应状态

| 状态 | 描述 | 关键字段 |
|--------|:--------:|-------------|------------|
| `pending` | 否 | 案例已创建，但人类尚未打开审核页面 | `expires_at`（过期时间） |
| `opened` | 否 | 人类已打开审核页面 | `opened_at`（打开时间） |
| `in_progress` | 否 | 人类正在与表单交互 | `progress`（进度信息，可选） |
| `completed` | 是 | 人类已提交响应 | `result`（结果）、`completed_at`（完成时间）、`responded_by`（提交者） |
| `expired` | 是 | 超时 | `expired_at`（过期时间）、`default_action`（默认操作） |
| `cancelled` | 是 | 人类点击了取消按钮 | `cancelled_at`（取消时间）、`reason`（取消原因） |

## 状态机

```
            +---------------------------------------------+
            |                                             v
[created] -> pending -> opened -> in_progress -> completed [terminal]
               |         |          |
               |         |          +---------> cancelled  [terminal]
               |         |
               |         +--> completed     [terminal]
               |         +--> expired       [terminal]
               |         +--> cancelled     [terminal]
               |
               +----------> expired          [terminal]
               +----------> cancelled        [terminal]
```

最终状态（`completed`、`expired`、`cancelled`）是不可变的——不会发生进一步的状态转换。

## 服务方：快速入门

当需要人类输入时，返回 HTTP 202 响应：

```javascript
// Express / Hono / any HTTP framework
app.post('/api/search', async (req, res) => {
  const results = await searchJobs(req.body.query);

  // Create review case with opaque token
  const caseId = `review_${crypto.randomBytes(16).toString('hex')}`;
  const token = crypto.randomBytes(32).toString('base64url'); // 43 chars
  const tokenHash = crypto.createHash('sha256').update(token).digest('hex');

  store.set(caseId, {
    status: 'pending',
    tokenHash,
    results,
    created_at: new Date().toISOString(),
    expires_at: new Date(Date.now() + 86400000).toISOString(),
  });

  res.status(202).json({
    status: 'human_input_required',
    message: `${results.length} jobs found. Please select which ones to apply for.`,
    hitl: {
      spec_version: '0.6',
      case_id: caseId,
      review_url: `https://yourservice.com/review/${caseId}?token=${token}`,
      poll_url: `https://api.yourservice.com/v1/reviews/${caseId}/status`,
      type: 'selection',
      prompt: 'Select which jobs to apply for',
      timeout: '24h',
      default_action: 'skip',
      created_at: store.get(caseId).created_at,
      expires_at: store.get(caseId).expires_at,
    },
  });
});
```

你还需要：一个审核页面（可以使用任何网页框架）、一个轮询端点（`GET /reviews/:caseId/status`）和一个响应端点（`POST /reviews/:caseId/respond`）。详细信息请参阅 [服务集成指南](skills/references/service-integration.md)。

## 代理方：快速入门

处理 HTTP 202 响应——大约 15 行代码：

```python
import time, httpx

response = httpx.post("https://api.jobboard.com/search", json=query)

if response.status_code == 202:
    hitl = response.json()["hitl"]

    # v0.7: Check for inline submit support
    if "submit_url" in hitl and "submit_token" in hitl:
        # Render native buttons in messaging platform (e.g. Telegram, Slack)
        send_inline_buttons(hitl["prompt"], hitl["inline_actions"], hitl["review_url"])
        # When human taps button → POST to submit_url (see Agent Integration Guide)
    else:
        # Standard flow: forward URL to human
        send_to_user(f"{hitl['prompt']}\n{hitl['review_url']}")

    # Poll for result (standard flow or fallback)
    while True:
        time.sleep(30)
        poll = httpx.get(hitl["poll_url"], headers=auth).json()

        if poll["status"] == "completed":
            result = poll["result"]  # {action: "select", data: {...}}
            break
        if poll["status"] in ("expired", "cancelled"):
            break
```

无需 SDK，也无需渲染用户界面。只需处理 HTTP 请求、转发 URL 和轮询。有关内联提交、SSE、回调、多轮决策和边缘情况的详细信息，请参阅 [代理集成指南](skills/references/agent-integration.md)。

## 三种传输方式

| 传输方式 | 代理是否需要公开端点？ | 是否需要实时响应？ | 复杂度？ |
|-----------|:---------------------------:|:----------:|:----------:|
| **轮询**（默认） | 否 | 否 | 最简单 |
| **SSE**（可选） | 否 | 是 | 复杂度中等 |
| **回调**（可选） | 是 | 是 | 复杂度较高 |

轮询是基础要求——所有符合 HITL 协议的服务都必须支持轮询。SSE 和回调是可选的增强功能。

## 原生消息按钮（v0.7 版本）

对于简单的决策，代理可以直接在聊天应用中渲染 **原生消息按钮**，而无需用户切换到浏览器。**工作原理**：服务在 HITL 对象中包含 `submit_url` 和 `submit_token` 字段。代理检测到这些字段后，会在聊天应用中显示相应的原生按钮。当人类点击按钮时，代理会通过 `submit_url` 发送相应的操作请求。消息应用不会自动检测 HITL 协议的支持情况。

**何时使用原生按钮：**

| 审核类型 | 是否支持内联按钮？ | 原因 |
|-------------|:----------------:|--------|
| **确认** | 是 | 支持两个按钮：确认/取消 |
| **升级** | 是 | 支持三个按钮：重试/跳过/中止 |
| **简单批准** | 是 | 支持两个按钮：批准/拒绝（无需编辑） |
| **复杂批准** | 只支持 URL | 需要使用包含表单的界面 |
| **选择** | 只支持 URL | 需要表单字段 |

**务必包含一个 URL 回退按钮**（例如 “Details &#8594;”），链接到审核页面——这样人类可以随时切换到完整的审核页面。

**平台要求**：代理必须是平台机器人（如 Telegram Bot（通过 BotFather）、Slack App、Discord Bot、WhatsApp Business API、Teams Bot），才能显示原生按钮。具体渲染方式请参阅 [代理集成指南](skills/references/agent-integration.md)。

## 注意事项：

- **不负责渲染审核页面**——审核页面由服务方负责托管和渲染。代理仅作为消息传递工具。 |
- **不定义审核页面的实现方式**——任何网页技术（如 React、纯 HTML 等）都可以使用。 |
- **不替代 OAuth**——HITL 协议用于决策，而非身份验证。 |
- **不代表人类执行操作**——除非人类在聊天应用中明确触发了内联操作按钮（v0.7 版本的 `submit_url`）。 |

## 服务方的 SKILL.md 扩展说明

使用 HITL 协议的服务可以在自己的 SKILL.md 文件中声明支持该协议：

```yaml
metadata:
  hitl:
    supported: true
    types: [selection, confirmation]
    supports_inline_submit: true
    review_base_url: "https://yourservice.com/review"
    timeout_default: "24h"
    info: "May ask user to select preferred jobs or confirm applications."
```

有关完整的字段参考，请参阅 [规范第 12 节](spec/v0.7/hitl-protocol.md)。

### 最佳实践：强制使用 HITL 协议

**问题**：代理通常会选择最简单的路径，从而忽略 HITL 协议，直接跳过人工审核环节。尽管协议明确规定代理不得忽略 HTTP 202 响应，但并没有机制阻止代理从不发送触发 HITL 协议的请求。

**解决方案**：强制代理在每次请求时明确选择是否使用 HITL 协议。在 API 中添加 `prefer_hitl` 和 `skip_hitl` 标志，并拒绝那些不提供这些标志的请求。

在 SKILL.md 文件中声明这些设置：

```yaml
metadata:
  hitl:
    supported: true
    hitl_required: true
    types: [selection, confirmation]
    info: "HITL is required. You MUST send prefer_hitl: true or skip_hitl: true."
```

在 SKILL.md 文件的正文中添加一个 **代理使用指南** 部分：

```markdown
## Agent Guidelines

HITL is required for this service. Every request MUST include exactly one of:

| Parameter | Type | Effect |
|-----------|------|--------|
| `prefer_hitl` | boolean | `true` → human reviews via HITL (HTTP 202) |
| `skip_hitl` | boolean | `true` → direct execution, no human review (HTTP 201) |

You MUST choose one. Omitting both returns 400 `HITL_CHOICE_REQUIRED`.
Sending both returns 400 validation error.

### Example: With HITL

POST /api/search
{"query": "Senior Dev Berlin", "prefer_hitl": true}

→ 202 + hitl object (human reviews results)

### Example: Without HITL

POST /api/search
{"query": "Senior Dev Berlin", "skip_hitl": true}

→ 201 {"results": [...], "hitl_skipped": true}

### Example: Missing choice

POST /api/search
{"query": "Senior Dev Berlin"}

→ 400 {"error": "HITL_CHOICE_REQUIRED", "message": "You must send prefer_hitl or skip_hitl."}
```

有关如何实施强制使用 HITL 协议的详细信息，请参阅 [服务集成指南](skills/references/service-integration.md#enforcing-hitl-choice)。

## 相关资源：

- [完整规范（v0.7）](spec/v0.7/hitl-protocol.md) |
- [OpenAPI 3.1 规范](schemas/openapi.yaml) — 所有端点的详细说明 |
- [JSON 规范](schemas/) — HITL 对象、轮询响应、表单字段、提交请求的定义 |
- [参考实现示例](implementations/reference-service/) — 使用 Express 5、Hono、Next.js、FastAPI 的实现示例 |
- [审核页面模板](templates/) — 五种审核类型的 HTML 模板 |
- [示例代码](examples/) — 12 个端到端的交互流程示例（包括内联确认、升级、混合审批等） |
- **代理实现检查清单](agents/checklist.md) — 包含伪代码的详细代理实现指南 |
- [交互式测试平台](playground/) |
- **SDK 开发指南](docs/sdk-guide.md) — 如何开发自定义 SDK