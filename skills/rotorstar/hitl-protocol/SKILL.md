---
name: hitl-protocol
description: "HITL协议——这是一种用于自主代理工作流程中处理人类决策的开放标准。当网站或API需要人类输入时，它会返回HTTP 202状态码，并附带一个用于审核的URL。像OpenClaw、Claude、Codex或Goose这样的自主代理会转发该URL，定期检查审核结果，然后继续执行后续操作。利用这一协议，你可以使任何网站都支持代理的交互需求，或者在你的代理系统中实现需要人类参与的交互流程（例如审批、选择、填写表单、确认等）。该协议支持多种交互方式，包括轮询、SSE（Server-Sent Events）、Webhook传输、原生渠道内的交互按钮（如Telegram、Slack、Discord、WhatsApp、Teams），以及不透明的令牌安全机制。此外，它还支持多步骤表单引导和多轮编辑流程。"
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

人工智能代理越来越多地代表用户访问网站和服务：进行搜索、预订、申请、购买等操作。但有些决策过于重要，不能完全交给代理来决定——代理可能会出现幻觉、误解，或在关键时刻做出错误的判断（例如：取消错误的保险政策、预订到错误的城市、将钱转错账户）。HITL 协议（“Human in the Loop”）是一个开放标准，确保人类在这些关键时刻仍能保持控制权。用户可以继续使用他们喜欢的消息工具（如 Telegram、WhatsApp、Slack），直接点击决策按钮，或者点击链接进入一个界面友好的网页（包含卡片、表单、按钮等）。页面上没有冗长的文字，也没有代理的盲目决策。当遇到 HITL 响应时，应告知用户需要人类参与决策，并提供相应的操作提示（如查看评论链接或执行特定操作）。

HITL 协议对于人类决策来说，就如同 OAuth 对于身份验证一样——它是一个连接 **服务**、**代理** 和 **人类** 的开放标准。当服务需要人类输入时，它会返回 HTTP 202 响应，并附带一个评论页面的 URL。代理将这个 URL 发送给用户，用户可以在浏览器中打开页面并做出明智的决策。之后，代理会等待用户的反馈并继续处理流程。

对于简单的决策（如确认/取消、批准/拒绝），代理可以直接在 Telegram、Slack、Discord、WhatsApp 或 Teams 中显示 **原生消息按钮**，无需使用浏览器。服务需要通过 `submit_url` 参数来启用这一功能。

**无需 SDK，也不强制使用任何 UI 框架。只需 HTTP 请求、URL 和轮询机制即可。**

**[交互式测试平台](https://rotorstar.github.io/hitl-protocol/playground/index.html)** — 你可以在浏览器中实时测试各种评论类型、传输方式和内联操作。**

## 你是什么角色？

| 角色 | 你的需求 | 参考文档 |
|-----------|----------------|------|
| 服务/网站开发者 | 在你的 API 中添加 HITL 端点，以便代理可以请求人类输入 | [服务集成指南](skills/references/service-integration.md) |
| 代理开发者 | 处理来自服务的 HTTP 202 响应和 HITL 回复 | [代理集成指南](skills/references/agent-integration.md) |
| 两者都需要 / 学习者 | 了解整个协议的内容 | 继续阅读以下内容 |

## 流程

代理从不负责显示用户界面；评论页面由服务端托管。敏感数据始终保留在浏览器中，不会经过代理。对于简单的决策，内联流程是一个可选的快捷方式。

## 功能矩阵

| 功能 | 详细信息 |
|---------|---------|
| **评论类型** | `approval`（批准）、`selection`（选择）、`input`（输入）、`confirmation`（确认）、`escalation`（升级） |
| **表单字段类型** | `text`（文本）、`textarea`（文本区域）、`number`（数字）、`date`（日期）、`email`（电子邮件）、`url`（网址）、`boolean`（布尔值）、`select`（单选）、`multiselect`（多选）、`range`（范围）、自定义 `x-*` |
| **传输方式** | 轮询（必需）、SSE（可选）、回调/Webhook（可选） |
| **内联提交** | `submit_url` + 原生消息按钮（Telegram、Slack、Discord、WhatsApp、Teams）——服务需自行配置 |
| **状态** | `pending`（待处理）→ `opened`（已打开）→ `in_progress`（进行中）→ `completed`（完成）/ `expired`（过期）/ `cancelled`（取消） |
| **安全性** | 使用 43 个字符的随机令牌（base64url 格式，256 位熵值）、SHA-256 哈希存储、时间安全的比较机制，仅支持 HTTPS |
| **多轮决策** | `previous_case_id`/`next_case_id`（用于迭代编辑流程，仅适用于 `approval` 类型） |
| **表单** | 单步字段、多步向导、条件性显示、验证规则、进度跟踪 |
| **超时设置** | ISO 8601 格式的持续时间，`default_action` 可设置为 `skip`（跳过）、`approve`（批准）、`reject`（拒绝）、`abort`（中止） |
| **发现机制** | 使用 `.well-known/hitl.json` 文件或 SKILL.md 文件中的 `metadata.hitl` 扩展名 |
| **提醒** | 设置 `reminder_at` 时间戳，通过 SSE 事件发送提醒 |
| **速率限制** | 每个案例每分钟最多 60 次请求，`Retry-After` 头部字段用于控制重试间隔 |

## 五种评论类型

| 类型 | 可执行的操作 | 是否支持多轮决策 | 是否需要表单字段 | 使用场景 |
|------|---------|:-----------:|:-----------:|----------|
| **Approval**（批准） | `approve`（批准）、`edit`（编辑）、`reject`（拒绝） | 是 | 需要人类审核的文件（如简历、电子邮件、部署计划） |
| **Selection**（选择） | `select`（选择） | 否 | 从选项中选择（如职位列表、目标对象） |
| **Input**（输入） | `submit`（提交） | 否 | 需要用户输入结构化数据（如薪资、日期、偏好设置） |
| **Confirmation**（确认） | `confirm`（确认）、`cancel`（取消） | 否 | 需要用户执行不可逆的操作（如发送邮件、部署） |
| **Escalation**（升级） | `retry`（重试）、`skip`（跳过）、`abort`（中止） | 否 | 用于处理错误（如部署失败、API 错误） |

## HITL 对象（HTTP 202 响应体）

当服务需要人类输入时，它会返回如下结构的 HTTP 202 响应：

### 必需字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `spec_version` | `"0.7"` | 协议版本 |
| `case_id` | 字符串 | 唯一的、适合 URL 的标识符（格式：`review_{random}`） |
| `review_url` | URL | 包含随机令牌的评论页面 URL |
| `poll_url` | URL | 用于获取状态更新的轮询端点 |
| `type` | 枚举 | `approval`（批准）、`selection`（选择）、`input`（输入）、`confirmation`（确认）、`escalation`（升级）/ `x-*`（其他类型） |
| `prompt` | 字符串 | 需要人类决定的内容（最多 500 个字符） |
| `created_at` | datetime | 创建时间戳（ISO 8601 格式） |
| `expires_at` | datetime | 过期时间戳（ISO 8601 格式） |

### 可选字段

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `timeout` | 时间长度 | 评论页面的显示时长（例如 `24h`、`PT24H`、`P7D`） |
| `default_action` | 枚举 | `skip`（跳过）、`approve`（批准）、`reject`（拒绝）、`abort`（中止） | 过期时的默认操作 |
| `callback_url` | URL | 如果代理提供了回调 URL，则返回该 URL |
| `events_url` | URL | 用于实时状态更新的 SSE 端点 |
| `context` | 对象 | 用于评论页面的附加数据（代理不会处理） |
| `reminder_at` | datetime | 重新发送评论页面的时间戳 |
| `previous_case_id` | 字符串 | 多轮决策中的前一个案例的链接 |
| `surface` | 对象 | 用户界面的格式设置（`format`、`version`） |
| `submit_url` | URL | 用于在聊天应用中显示原生按钮的提交端点（v0.7 版本） |
| `submit_token` | 字符串 | `submit_url` 需要的认证令牌（如果设置了 `submit_url` 则必须提供） |
| `inline_actions` | 字符串数组 | 通过 `submit_url` 允许执行的操作（例如 `["confirm", "cancel"]`）。如果未设置，则允许所有操作 |

## 轮询响应（完成状态）

`result` 对象仅在 `status` 为 `"completed"` 时出现。它总是包含 `action`（字符串）和 `data`（根据类型不同的数据内容）。

### 轮询响应状态

| 状态 | 描述 | 关键字段 |
|--------|:--------:|-------------|------------|
| `pending` | 否 | 案例已创建，但用户尚未打开评论页面 | `expires_at`（过期时间） |
| `opened` | 否 | 用户已打开评论页面 | `opened_at`（打开时间） |
| `in_progress` | 否 | 用户正在填写表单 | `progress`（进度信息，可选） |
| `completed` | 是 | 用户已提交响应 | `result`（结果）、`completed_at`（完成时间）、`responded_by`（提交者） |
| `expired` | 是 | 超时 | `expired_at`（过期时间）、`default_action`（默认操作） |
| `cancelled` | 是 | 用户点击了取消按钮 | `cancelled_at`（取消时间）、`reason`（取消原因） |

## 状态机

`completed`、`expired`、`cancelled` 状态是不可变的，无法进一步转换。

## 服务端快速入门

当需要人类输入时，返回 HTTP 202 响应：

此外，你还需要：一个评论页面（可以使用任何 Web 框架实现）、一个轮询端点（`GET /reviews/:caseId/status`）以及一个响应端点（`POST /reviews/:caseId/respond`）。详细信息请参阅 [服务集成指南](skills/references/service-integration.md)。

## 代理端快速入门

处理 HTTP 202 响应（大约 15 行代码）：

**无需 SDK，也无需渲染用户界面。只需处理 HTTP 请求、转发 URL 和轮询即可。**有关内联提交、SSE、回调、多轮决策等功能的详细信息，请参阅 [代理集成指南](skills/references/agent-integration.md)。

## 三种传输方式

| 传输方式 | 代理是否需要公开端点？ | 是否支持实时更新？ | 复杂度？ |
|-----------|:---------------------------:|:----------:|:----------:|
| **Polling**（默认方式） | 否 | 否 | 最简单的方式 |
| **SSE**（可选） | 否 | 是 | 适用于需要实时更新的场景 |
| **Callback**（可选） | 是 | 是 | 适用于需要回调的场景 |

轮询是基础要求——所有符合 HITL 协议的服务都必须支持轮询。SSE 和回调是可选的增强功能。

## 原生消息按钮（v0.7 版本）

对于简单的决策，代理可以直接在聊天界面中显示 **原生消息按钮**，用户无需切换浏览器。**工作原理：**服务会在 HITL 响应中包含 `submit_url` 和 `submit_token` 字段；代理检测到这些字段后，会显示平台自带的按钮。用户点击按钮后，代理会通过 `submit_url` 发送相应的请求。消息平台会自动显示按钮内容，无需用户手动操作。

**何时使用原生按钮：**

| 评论类型 | 是否支持内联按钮？ | 原因 |
|-------------|:----------------:|--------|
| **Confirmation**（确认） | 是 | 提供“确认”和“取消”两个按钮 |
| **Escalation**（升级） | 是 | 提供“重试”、“跳过”和“中止”三个按钮 |
| **Approval**（简单审批） | 是 | 提供“批准”和“拒绝”两个按钮（无需编辑） |
| **Approval**（需要编辑） | 仅提供链接 | 需要使用包含表单的界面 |
| **Selection**（选择） | 仅提供链接 | 需要列表或卡片形式的界面 |

**务必提供一个链接按钮**（例如 “查看详情 &#8594;”），引导用户返回评论页面。**

**平台要求：**代理必须是平台提供的机器人（如 Telegram Bot、Slack App、Discord Bot、WhatsApp Business API、Teams Bot）才能显示原生按钮。具体实现方式请参阅 [代理集成指南](skills/references/agent-integration.md)。

## 注意事项：

- **服务端不负责显示评论界面**——评论页面由服务端负责渲染。
- **服务端不定义评论页面的实现细节**——任何 Web 技术（如 React、纯 HTML 等）都可以使用。
- **HITL 不替代 OAuth**——它仅用于决策过程，不涉及身份验证。
- **服务端不会自动执行操作**——除非用户通过聊天界面主动触发内联按钮（v0.7 版本的 `submit_url`）。

## 服务端的 SKILL.md 扩展说明

使用 HITL 协议的服务可以在自己的 SKILL.md 文件中声明支持该协议：

详细字段说明请参阅 [spec Section 12](spec/v0.7/hitl-protocol.md)。

### 最佳实践：强制使用 HITL 协议

**问题：**代理通常会选择最简单的路径，直接跳过 HITL 流程，导致无需人类参与审核。尽管协议规定代理必须处理 HTTP 202 响应，但并没有机制阻止代理完全忽略这些请求。

**解决方案：**强制代理在每次请求时明确选择是否使用 HITL 协议。在 API 中添加 `prefer_hitl` 和 `skip_hitl` 标志，并拒绝那些不提供这些标志的请求。

在 SKILL.md 文件中声明这些设置：

在 SKILL.md 的正文中添加一个 **代理使用指南** 部分：

有关如何实施这一规则的详细信息，请参阅 [服务集成指南——强制使用 HITL 协议](skills/references/service-integration.md#enforcing-hitl-choice)。

### 可选：提供反馈建议

服务可以在成功的响应中包含 `improvement_suggestions`，为代理提供结构化的反馈，以便他们根据这些反馈进行改进——无需再次触发 HITL 流程。

在 SKILL.md 中声明支持这一功能：

**建议对象的结构：**

| 字段 | 类型 | 说明 |
|-------|------|-------------|
| `field` | 字符串 | 需要改进的数据字段 |
| `issue` | 字符串 | 需要改进的问题或不足之处 |
| `agent_action` | 字符串 | 代理应采取的具体操作 |
| `impact` | 字符串 | 对代理的改进效果（例如：“提升 25 分”） |
| `priority` | `"high"` / `"medium"` / `"low"` | 优先级 |

**代理的行为建议：**
- 首先始终提供主要结果 |
- 提供最多两次改进机会——每个建议对应一个改进方向，提交更新后的数据 |
- 当 `improvement_suggestions` 为空或达到最大尝试次数时停止 |
- 避免无限循环

有关详细信息，请参阅 [代理检查清单——质量改进循环](agents/checklist.md#enhanced-quality-improvement-loop) 和 [示例 13](examples/13-quality-improvement-loop.json)。

## 协议与 RFC 的一致性

本协议和文档符合以下 RFC 标准：

- [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) — HTTP 响应语义（如 `202` 状态码、条件请求、重试机制）
- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) + [RFC 8174](https://www.rfc-editor.org/rfc8174) — 规范性术语（如 `MUST`、`SHOULD`、`MAY`）
- [RFC 3339](https://www.rfc-editor.org/rfc3339) — HITL 协议中使用的时间戳格式 |
- [RFC 6750](https://www.rfc-editor.org/rfc6750) — 用于评论和内联提交的令牌机制

有关完整的实现细节，请参阅 [README 文件中的 RFC 对齐信息](README.md#rfc-alignment)。

## 相关资源：

- [完整规范（v0.7 版本）](spec/v0.7/hitl-protocol.md)
- [OpenAPI 3.1 规范](schemas/openapi.yaml) — 所有端点的详细说明 |
- [JSON 格式定义](schemas/) — HITL 对象、轮询响应、表单字段、提交请求的格式 |
- [参考实现示例](implementations/reference-service/) — 使用 Express 5、Hono、Next.js、FastAPI 的实现示例 |
- [评论页面模板](templates/) — 五种评论类型的 HTML 模板 |
- [示例代码](examples/) — 包含内联确认、升级、混合审批等完整流程的示例 |
- [代理实现检查清单](agents/checklist.md) — 包含伪代码的详细代理实现指南 |
- [交互式测试平台](playground/) |
- [SDK 开发指南](docs/sdk-guide.md) — 如何开发自定义 SDK