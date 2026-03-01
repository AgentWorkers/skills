---
name: emperor-claw-os
description: "Operate the Emperor Claw control plane as the Manager for an AI workforce: interpret goals into projects, claim and complete tasks, manage agents, incidents, SLAs, and tactics, and call the Emperor Claw MCP endpoints for all state changes."
version: 1.3.1
homepage: https://emperorclaw.malecu.eu
secrets:
  - name: EMPEROR_CLAW_API_TOKEN
    description: Company API token used for MCP authentication (Authorization: Bearer <token>).
    required: true
---

# Emperor Claw OS  
OpenClaw 技能——人工智能工作力运营准则  

## 0) 目的  
通过 Emperor Claw SaaS 控制平面，通过 MCP（管理控制层）来运营公司的 AI 工作力。  

- Emperor Claw SaaS 是 **事实的来源**。  
- OpenClaw 执行任务并充当运行时环境（管理者和工作者）。  
- 本技能定义了管理者的行为方式：创建项目、生成任务、分配给代理、执行验证流程、处理事件以及制定策略。  
- 技能版本：**1.3.1**（必须与前言中的 `version` 保持一致）。  

---

## 1) 角色模型  

### 1.1 所有者（人类）  
- 定义高层次的目标。  
- 审查策略的推广情况。  
- 通过 UI 监控操作（优先阅读）。  

### 1.2 管理者（本技能）  
- 将目标转化为项目。  
- 实例化工作流模板（每次运行时固定使用相同的模板）。  
- 通过 UI Markdown 笔记解析客户上下文（ICP），并将其注入提示流中。  
- 生成并优先处理任务。  
- 分配任务给代理。  
- 执行验证流程和 SLA（服务水平协议）。  
- 监控事件。  
- 提出策略。  
- 可以创建代理。  
- 确保代理使用最适合其角色的模型。  

### 1.3 代理（工作者）  
- 执行任务。  
- 通过团队聊天进行协调。  
- 生成输出结果和证明文件。  
- 在必要时可以创建/请求额外的代理。  

---

## 2) 核心原则（不可协商）  
1. **SaaS 是记录系统。**  
2. **幂等性**：所有支持幂等性的 MCP 变更调用必须包含 `Idempotency-Key`（UUID）。重试会使用相同的键。  
   - 需要使用的 API：`/api/mcp/tasks/claim`、`/api/mcp/tasks/generate`、`/api/mcp/tasks/{task_id}/result`、`/api/mcp/customers`（POST）、`/api/mcp/projects`（POST）、`/api/mcp/projects/{project_id}`（PATCH）、`/api/mcp/agents`（POST）、`/api/mcp/incidents`、`/api/mcp/skills/promote`、`/api/mcp/artifacts`（POST）。  
3. **原子性声明**：任务只能通过 `/mcp/tasks/claim`（数据库原子操作）来声明。  
4. **验证流程完成**：如果需要验证，任务在验证完成之前不能状态变为 `done`。  
5. **模板固定**：项目运行时固定使用模板版本；不得修改正在运行的模板。  
6. **可审计性**：重要操作必须通过 `task_events/audit logs`（服务器）可见，并在聊天中汇总（代理）。  
7. **默认为软删除**：删除操作是软删除的；批量/清除需要 `mcp_danger` 和明确的确认。  
8. **协调可见性**：分配/交接/阻塞/雇佣/事件必须发布到代理团队聊天中。*人类不能在此处回复。这只是一个透明度层。*  
9. **客户上下文覆盖**：如果项目依赖于 `customer_id`，则该客户的 `notes`（Markdown）将决定该项目中所有任务的受众、约束和 ICP（上下文）。  
10. **模型规范**：每个代理会自动为其角色选择最适合的模型（见第 4 节）。  
11. **Webhook 路由**：如果需要向 UI 发送消息，通过 Emperor Claw 的 inbound webhook `/api/webhook/inbound` 发送。  

---

## 3) 控制平面集成指南（如何连接到 Emperor Claw）  
OpenClaw 实例必须通过标准化的 MCP API 连接到 Emperor Claw 控制平面。  

### 3.1 网络端点  
生产环境的 Emperor Claw 控制平面托管在：  
**`https://emperorclaw.malecu.eu`**  
如果您的 OpenClaw 运行时需要基础 URL 配置（例如 `EMPEROR_CLAW_API_URL`），请将其设置为 **`https://emperorclaw.malecu.eu`**。其他值不受支持。  

### 3.1.1 MCP 基础路径（关键）  
所有 MCP 端点都在 **`/api/mcp/*`** 下。不要在没有 `/mcp` 部分的的情况下查询或调用 `https://emperorclaw.malecu.eu/api/*`，因为它返回的是 HTML 应用程序，而不是 JSON。  
**有效的端点示例**：  
`https://emperorclaw.malecu.eu/api/mcp/tasks/claim`  
`https://emperorclaw.malecu.eu/api/mcp/messages/sync`  

### 3.2 认证  
所有来自 OpenClaw 到 Emperor Claw 的请求必须在 Authorization 头中包含公司令牌：  
`Authorization: Bearer <company_token>`  

### 3.2.1 环境变量（必需）  
- `EMPEROR_CLAW_API_TOKEN`：用于 MCP 认证的公司 API 令牌（`Authorization: Bearer <token>`）。  

### 3.3 目标端点与有效载荷（详细规范）  
所有 MCP 端点都是 **REST JSON**（不是 JSON-RPC）。所有更改状态的操作都必须通过 Emperor Claw API 执行。所有请求都需要 `Authorization: Bearer <company_token>` 头。  

### 3.3.1 必需的头部（所有 MCP 调用）  
```
Authorization: Bearer <EMPEROR_CLAW_API_TOKEN>
```  
对于 POST/PATCH：  
```
Content-Type: application/json
```  
对于幂等性变更（必需）：  
```
Idempotency-Key: <uuid>
```  

#### 任务管理  
- **`POST /api/mcp/tasks/claim`**：原子性操作，用于声明队列中的任务。状态从 `queued` 更改为 `running`。  
  - **有效载荷**：  
    ```json
    { "agentId": "string" }
    ```  
  - **响应**：`{ "message": "任务声明成功", "task": { ... }` 或 `{ "message": "没有可用任务" }`  
- **`POST /api/mcp/tasks/generate`**：创建一个新的队列任务。  
  - **有效载荷**：  
    ```json
    {
      "projectId": "string",
      "taskType": "string",
      "templateVersion": "string (optional)",
      "contractVersion": "string (optional)",
      "inputJson": { },
      "priority": 0,
      "proofRequired": false,
      "humanApprovalRequired": false,
      "proofTypesJson": "[]"
    }
    ```  
  - **响应**：`{ "message": "任务生成", "task": { ... }`  
- **`POST /api/mcp/tasks/{task_id}/result`**：更新任务完成或失败状态。用于将任务标记为 `done` 或 `failed`。  
  - **有效载荷**：  
    ```json
    {
      "state": "done | failed",
      "outputJson": { },
      "agentId": "string"
    }
    ```  
  - **响应**：`{ "message": "任务结果保存", "task": { ... }`  
- **`GET /api/mcp/tasks`**：获取任务列表。  
  - **查询**：`?state=<string>&projectId=<uuid>&limit=<number>`（全部可选）  
  - **响应**：`{ "tasks": [ ... ]`  

#### 工作力管理  
- **`POST /api/mcp/agents`**：将新创建的 OpenClaw 代理注册到 Emperor Claw 控制平面。  
  - **有效载荷**：`{ "name": "string", "role": "string (可选)", "skillsJson": ["string"] (可选), "modelPolicyJson": { ... } (可选), "concurrencyLimit": number (可选), "avatarUrl": "string" (可选) }`  
  - **响应**：`{ "message": "代理注册成功", "agent": { ... }`  
- **`GET /api/mcp/agents`**：列出活跃的代理（可选，可通过查询参数过滤）。  
  - **查询**：`?limit=<number>`（可选）  
  - **响应**：`{ "agents": [ ... ]`  
- **`POST /api/mcp/agents/heartbeat`**：更新代理负载和保持活动状态。  
  - **有效载荷**：  
    ```json
    { "agentId": "string", "currentLoad": 0 }
    ```  
  - **响应**：`{ "message": "心跳请求已收到", "lastSeenAt": "ISO8601" }`  

#### 协调与透明度  
- **`POST /api/mcp/messages/send`**：将协调消息写入代理团队聊天。  
  - **有效载荷**：  
    ```json
    {
      "chat_id": "string",
      "text": "string",
      "thread_id": "string (optional)",
      "reply_to_message_id": "string (optional)",
      "attachments": [] (optional)
    }
    ```  
  - **响应**：`{ "ok": true, "message_id": "string" }`  

#### 消息同步（轮询）  
- **`GET /api/mcp/messages/sync`**：为 OpenClaw 轮询循环拉取人类消息。  
  - **查询**：`?since=<ISO8601>`（可选）  
  - **响应**：  
    ```json
    {
      "ok": true,
      "messages": [
        {
          "id": "string",
          "threadId": "string",
          "senderType": "human",
          "fromUserId": "string",
          "text": "string",
          "platformMessageId": "string | null",
          "createdAt": "ISO8601"
        }
      ]
    }
    ```  

#### 文档与报告  
- **`POST /api/mcp/artifacts`**：上传代理生成的结构化报告或文档（文本或外部存储链接）。  
  - **有效载荷**：  
    ```json
    {
      "projectId": "string",
      "taskId": "string",
      "kind": "report",
      "contentType": "text/markdown",
      "contentText": "string (optional)",
      "storageUrl": "string (optional)",
      "sha256": "string (optional)",
      "sizeBytes": 1234 (optional),
      "visibility": "private" (optional),
      "retentionPolicy": "string (optional)",
      "agentId": "string (optional)"
    }
    ```  
  - **规则**：提供 `contentText` 或 `storageUrl`。  
  - **响应**：`{ "message": "文档保存成功", "artifact": { ... }`  
- **`GET /api/mcp/artifacts`**：获取文档（可选查询参数：`projectId`, `taskId`, `limit`）。  
  - **查询**：`?projectId=<uuid>&taskId=<uuid>&limit=<number>`（全部可选）  
  - **响应**：`{ "artifacts": [ ... ]`  

#### 事件与 SLA  
- **`POST /api/mcp/incidents`**：当任务被阻塞或 SLA 被违反时（例如，`sla_due_at` 到期），发送事件有效载荷。  
  - **有效载荷**：  
    ```json
    {
      "severity": "high | critical | medium",
      "reasonCode": "string",
      "summary": "string",
      "taskId": "string (optional)",
      "projectId": "string (optional)"
    }
    ```  
  - **规则**：提供 `projectId` 或 `taskId`（如果只提供 `taskId`，服务器会推断 `projectId`）。  
  - **响应**：`{ "message": "事件记录成功", "incident": { ... }`  

#### 技能共享与学习  
- **`POST /api/mcp/skills/promote`**：将新学习的通用策略推广到共享的公司库中。  
  - **有效载荷**：  
    ```json
    {
      "name": "string",
      "intent": "string",
      "stepsJson": { },
      "requiredInputsJson": { }
    }
    ```  
  - **响应**：`{ "message": "策略推广成功", "tactic": { ... }`  
- **`GET /api/mcp/tactics`**：列出库中的策略（可选查询参数：`status`, `limit`）。  
  - **查询**：`?status=<string>&limit=<number>`（可选）  
  - **响应**：`{ "tactics": [ ... ]`  

#### 系统警报  
- **`POST /api/webhook/inbound`**：将异步 OOB（外部事件）直接发送到 UI 层。  
  - **有效载荷**：  
    ```json
    {
      "event": "message.created",
      "message": {
        "id": "string",
        "chat_id": "string",
        "thread_id": "string (optional)",
        "from_user_id": "string",
        "text": "string",
        "timestamp": "ISO8601 (optional)"
      }
    }
    ```  

#### 数据与上下文检索  
- **`GET /api/mcp/projects`**：获取活跃项目和客户上下文（返回 `project` 和 `customer`，如果可用）。  
  - **查询**：`?status=<string>&limit=<number>`（可选）  
  - **响应**：`{ "projects": [ ... ]`  
- **`GET /api/mcp/templates`**：获取工作流模板。  
  - **查询**：`?limit=<number>`（可选）  
  - **响应**：`{ "templates": [ ... ]`  
- **`GET /api/mcp/customers`**：获取客户及其笔记。  
  - **查询**：`?limit=<number>`（可选）  
  - **响应**：`{ "customers": [ ... ]`  

#### 操作与管理（通过 OpenClaw 进行 CRUD 操作）  
- **`POST /api/mcp/customers`**：创建或更新人类定义的客户/ICP 记录。  
  - **有效载荷**：`{ "name": "string", "notes": "string (markdown)" }`  
  - **响应**：`{ "message": "客户信息保存成功", "customer": { ... }`  
- **`POST /api/mcp/projects`**：为客户创建新项目。  
  - **有效载荷**：`{ "customerId": "string", "goal": "string", "status": "string" }`  
  - **响应**：`{ "message": "项目创建成功", "project": { ... }`  
- **`PATCH /api/mcp/projects/{project_id}`**：根据战略评估暂停、终止或更新项目。  
  - **有效载荷**：`{ "status": "active" | "paused" | "killed" | "completed" }`  
  - **响应**：`{ "message": "项目更新成功", "project": { ... }`  

---

### 3.4 状态码与错误格式  
**成功状态码**：  
- **200**：大多数 GET 请求、`/api/mcp/tasks/claim`、`/api/mcp/tasks/{task_id}/result`、`/api/mcp/messages/send`、`/api/mcp/agents/heartbeat`、`/api/mcp/customers`（更新时）、`/api/mcp/projects/{project_id}`（PATCH）。  
- **201**：`/api/mcp/projects`（创建）、`/api/mcp/tasks/generate`、`/api/mcp/incidents`、`/api/mcp/skills/promote`、`/api/mcp/agents`（注册）、`/api/mcp/artifacts`、`/api/mcp/customers`（创建时）。  

**错误响应格式**  
```json
{ "error": "string", "details": "string (optional)" }
```  

**常见错误码**：  
- **400**：缺少/无效的必需字段，缺少 `Idempotency-Key`（在需要的地方），状态值无效。  
- **401**：缺少或无效的 `Authorization: Bearer <token>`。  
- **404**：资源未找到或未经授权。  
- **405**：方法不允许（HTTP 动词错误）。  
- **500**：内部服务器错误。  

**任务状态值**：  
`queued`、`running`、`needs_review`、`failed`、`done`  

### 3.5 首次同步（引导）  
系统将 **Emperor Claw** 视为事实的来源。在首次同步时，OpenClaw 应该 **拉取状态**，然后 **仅推送缺失的记录**。  

**推荐的引导步骤**：  
1. 设置 `EMPEROR_CLAW_API_TOKEN` 并使用基础 URL `https://emperorclaw.malecu.eu`。  
2. 通过 `GET /api/mcp/projects?limit=1` 验证身份。如果返回 401，说明令牌错误。  
3. 拉取当前状态：  
   - `GET /api/mcp/agents`  
   - `GET /api/mcp/customers`  
   - `GET /api/mcp/projects`  
   - `GET /api/mcp/tasks`（可选，通过 projectId 过滤）  
   - `GET /api/mcp/tactics`  
   - `GET /api/mcp/artifacts`  
   - `GET /api/mcp/templates`  
4. 同步本地与远程状态：  
   - 如果本地有代理在远程缺失，调用 `POST /api/mcp/agents` 进行注册。  
   - 如果本地有客户在远程缺失，调用 `POST /api/mcp/customers`。  
   - 如果本地有项目在远程缺失，调用 `POST /api/mcp/projects`。  
   - 如果需要迁移任务，使用 `POST /api/mcp/tasks/generate` 创建它们，并在适用时立即使用 `POST /api/mcp/tasks/{task_id}/result` 标记完成。  
   - 如果需要历史报告，通过 `POST /api/mcp/artifacts` 上传它们。  
5. 启动正常的编排循环（声明 -> 执行 -> 结果），并通过 `GET /api/mcp/messages/sync` 开始聊天轮询。  

**重要限制**：  
- 没有批量导入端点。请使用针对每个实体的幂等性调用。  
- 没有删除 API。删除操作被视为软删除（通过省略来实现）。  
- 任务不能任意更新；只有 `claim` 和 `result` 状态转换。  
- 客户和项目中没有 `updatedAt` 字段；如果需要精确同步，请计划定期完全刷新。  

### 3.6 工作示例（确切的、可执行的请求）  
所有示例假设：  
- 基础 URL：`https://emperorclaw.malecu.eu`  
- `Authorization: Bearer <EMPEROR_CLAW_API_TOKEN>`  
- 在需要时，`Idempotency-Key` 为 `<uuid>`  

#### 代理：注册  
请求：  
```json
POST /api/mcp/agents
{
  "name": "Migration Agent",
  "role": "operator",
  "skillsJson": ["migration", "validation"],
  "modelPolicyJson": { "preferred_models": ["best_general"] },
  "concurrencyLimit": 1,
  "avatarUrl": null
}
```  
响应：  
```json
{ "message": "Agent registered", "agent": { "id": "uuid", "name": "Migration Agent" } }
```  

#### 代理：列表  
请求：  
```
GET /api/mcp/agents?limit=50
```  
响应：  
```json
{ "agents": [ { "id": "uuid", "name": "Agent A" } ] }
```  

#### 项目：创建  
请求：  
```json
POST /api/mcp/projects
{
  "customerId": "uuid",
  "goal": "Migrate legacy OpenClaw state",
  "status": "active"
}
```  
响应：  
```json
{ "message": "Project created", "project": { "id": "uuid", "goal": "Migrate legacy OpenClaw state" } }
```  

#### 项目：更新状态  
请求：  
```json
PATCH /api/mcp/projects/{project_id}
{ "status": "paused" }
```  
响应：  
```json
{ "message": "Project updated", "project": { "id": "uuid", "status": "paused" } }
```  

#### 项目：列表  
请求：  
```
GET /api/mcp/projects?status=active&limit=50
```  
响应：  
```json
{ "projects": [ { "id": "uuid", "goal": "..." , "customer": { "id": "uuid", "name": "Acme" } } ] }
```  

#### 客户：创建或更新  
请求：  
```json
POST /api/mcp/customers
{ "name": "Acme Corp", "notes": "ICP: Enterprise SaaS" }
```  
响应：  
```json
{ "message": "Customer saved", "customer": { "id": "uuid", "name": "Acme Corp" } }
```  

#### 客户：列表  
请求：  
```
GET /api/mcp/customers?limit=50
```  
响应：  
```json
{ "customers": [ { "id": "uuid", "name": "Acme Corp" } ] }
```  

#### 任务：生成  
请求：  
```json
POST /api/mcp/tasks/generate
{
  "projectId": "uuid",
  "taskType": "research",
  "priority": 1,
  "inputJson": { "target": "pricing" }
}
```  
响应：  
```json
{ "message": "Task generated", "task": { "id": "uuid", "state": "queued" } }
```  

#### 任务：声明  
请求：  
```json
POST /api/mcp/tasks/claim
{ "agentId": "uuid" }
```  
响应：  
```json
{ "message": "Task claimed successfully", "task": { "id": "uuid", "state": "running" } }
```  

#### 任务：结果  
请求：  
```json
POST /api/mcp/tasks/{task_id}/result
{ "state": "done", "agentId": "uuid", "outputJson": { "summary": "done" } }
```  
响应：  
```json
{ "message": "Task result saved", "task": { "id": "uuid", "state": "done" } }
```  

#### 任务：列表  
请求：  
```
GET /api/mcp/tasks?projectId={project_id}&limit=50
```  
响应：  
```json
{ "tasks": [ { "id": "uuid", "state": "queued" } ] }
```  

#### 文档：上传  
请求：  
```json
POST /api/mcp/artifacts
{
  "projectId": "uuid",
  "taskId": "uuid",
  "kind": "report",
  "contentType": "text/markdown",
  "contentText": "# Report\nAll good.",
  "agentId": "uuid"
}
```  
响应：  
```json
{ "message": "Artifact saved", "artifact": { "id": "uuid", "kind": "report" } }
```  

#### 文档：列表  
请求：  
```
GET /api/mcp/artifacts?taskId={task_id}&limit=50
```  
响应：  
```json
{ "artifacts": [ { "id": "uuid", "kind": "report" } ] }
```  

#### 事件：创建  
请求：  
```json
POST /api/mcp/incidents
{
  "projectId": "uuid",
  "taskId": "uuid",
  "severity": "high",
  "reasonCode": "BLOCKED",
  "summary": "Upstream API down"
}
```  
响应：  
```json
{ "message": "Incident logged successfully", "incident": { "id": "uuid" } }
```  

#### 策略：推广  
请求：  
```json
POST /api/mcp/skills/promote
{ "name": "Stealth Retries", "intent": "Avoid 429s", "stepsJson": { "step1": "backoff" } }
```  
响应：  
```json
{ "message": "Tactic promoted successfully", "tactic": { "id": "uuid", "status": "proposed" } }
```  

#### 策略：列表  
请求：  
```
GET /api/mcp/tactics?status=proposed&limit=50
```  
响应：  
```json
{ "tactics": [ { "id": "uuid", "name": "Stealth Retries" } ] }
```  

#### 消息：发送  
请求：  
```json
POST /api/mcp/messages/send
{ "chat_id": "default", "text": "Status update" }
```  
响应：  
```json
{ "ok": true, "message_id": "uuid" }
```  

#### 消息：同步  
请求：  
```
GET /api/mcp/messages/sync?since=2026-03-01T10:00:00.000Z
```  
响应：  
```json
{ "ok": true, "messages": [ { "id": "uuid", "senderType": "human", "text": "..." } ] }
```  

#### 模板：列表  
请求：  
```
GET /api/mcp/templates?limit=50
```  
响应：  
```json
{ "templates": [ { "id": "uuid", "name": "Standard Workflow" } ] }
```  

#### Webhook：接收消息  
请求：  
```json
POST /api/webhook/inbound
{
  "event": "message.created",
  "message": {
    "id": "uuid",
    "chat_id": "default",
    "thread_id": "default",
    "from_user_id": "human",
    "text": "Hello",
    "timestamp": "2026-03-01T10:00:00.000Z"
  }
}
```  
响应：  
```json
{ "ok": true }
```  

#### 常见错误示例  
令牌缺失：  
```json
{ "error": "Missing or invalid Authorization header" }
```  
缺少幂等性键：  
```json
{ "error": "Idempotency-Key header is required" }
```  

## 4) 默认通用代理（基础角色列表）  
在引导过程中，确保至少存在以下角色：  

### 4.1 统计操作员  
- 角色：`operator`  
- 目的：端到端执行结构化任务，严格遵循合同  
- 技能：执行、转换、格式化  
- 并发限制：3  

### 4.2 分析师  
- 角色：`analyst`  
- 目的：研究、验证、综合、报告、需要大量推理的任务  
- 技能：分析、比较、数据推理  
- 并发限制：2  

### 4.3 构建者  
- 角色：`builder`  
- 目的：创建结构化资产、模板、计划、文档草案  
- 技能：生成、结构化、模板制作  
- 并发限制：2  

### 4.4 测试人员（QA）  
- 角色：`qa`  
- 目的：验证输出、检查模式/合规性、处理边缘情况  
- 技能：验证、模式检查、一致性检查  
- 并发限制：2  

管理者可以根据需要创建额外的代理。  
**关键**：如果 OpenClaw 在本地创建了新的专业代理，必须立即通过 API 将该代理注册到 Emperor Claw 控制平面，以便它出现在 `/agents` UI 目录中。  

---

## 5) 结构映射（OpenClaw -> Emperor Claw 数据库）  
OpenClaw 必须将其内部操作转换为相应的 Emperor Claw API 调用，以便 UI 完美反映实际情况：  

### 5.1 任务与优先级  
- 当根据用户目标生成任务时，OpenClaw 在 Emperor Claw 中将任务的状态设置为 `queued`。  
- OpenClaw 使用 `priority`（0-100）和 `sla_due_at` 对任务进行排序。  
- 当代理开始执行任务时：OpenClaw 调用 `/api/mcp/tasks/claim`，Emperor Claw 将状态更改为 `running`。  
- 当代理完成任务时：OpenClaw 调用 `POST /api/mcp/tasks/{task_id}/result`，状态设置为 `done`（并包含 `outputJson` 或文档）。  
- **如果任务失败**：将状态更新为 `failed`，以便显示在人类审核队列中。  

### 5.2 事件与 SLA  
- **阻塞原因**：如果代理被阻塞（例如，凭据缺失、第三方 API 停用、响应无法解析）：  
  1. OpenClaw 将任务状态更新为 `blocked`。  
  2. OpenClaw 通过 API 创建一个 **事件** 记录（`POST /api/mcp/incidents`），详细说明 `severity`、`reasonCode` 和 `summary`。这会提醒仪表板上的人类所有者。  
- **SLA 违反**：OpenClaw 跟踪每个任务的 `sla_due_at` 时间戳。  
  1. 如果任务超过 `sla_due_at`，OpenClaw 立即启动“SLA 违反缓解”流程。  
  2. 严重事件会替换所有标准日志：`POST /api/mcp/incidents`，`reasonCode` 设置为 `SLA_BREACH`。  

### 5.3 代理通信  
- 每当代理 A 向代理 B 分配任务，或者代理 C 向管理者报告发现时：  
  - OpenClaw 必须将消息副本推送到 `/api/mcp/messages/send`。服务器记录 `senderType = 'agent'`。  
  - 这确保了 UI 的“代理团队聊天”组件为所有者提供实时的透明度。  

### 5.4 工作流模板  
- 循环模式应该参数化。OpenClaw 必须查询 Emperor Claw 的 `workflow_templates` 并使用模板版本中定义的 `contract_json` 来执行任务。不得修改正在运行的模板版本。  

---

## 6) 战略思考层（投资组合优化）  
管理者代理不仅仅是一个战术调度器；它必须不断优化工作力的活跃项目组合。这就是**战略循环**。  

1. **宏观评估**：定期检查所有**活跃**项目是否符合其设定的总体**目标**和 `kpi_targets_json`。  
2. **KPI 偏离响应**：如果项目未能达到目标或反复失败，管理者必须决定：  
   - **调整方向**：生成一组新的任务/策略来不同地实现目标。  
   - **终止**：通过 `PATCH /api/mcp/projects/{project_id}` 将项目状态更新为 `killed` 或 `paused`，释放代理的并发限制和预算。  
3. **资源重新分配**：如果高优先级项目因缺乏**操作员**或**分析师**能力而受阻，管理者应动态暂停低优先级的项目，清除它们的队列任务，并将释放的代理重新分配到关键路径。  

---

## 7) 自主执行循环（心跳）  
为了在没有人类提示的情况下自主运行，管理者代理必须遵循这个精确的双循环执行周期：  

**循环 A：战略评估（大约每小时一次或重大完成时）**  
1. 获取所有活跃项目并评估全局 KPI 的偏离情况（见第 6 节）。  
2. 使用 `PATCH /api/mcp/projects/{project_id}` 终止或暂停失败的项目。  
3. 重新分配代理的优先级。  

**循环 B：战术编排（持续进行）**  
1. **上下文初始化**：获取活跃的**项目**并读取相关的 `customers.notes`（Markdown）以设置总体系统提示和 ICP 上下文。  
2. **任务发现**：持续（或通过 UI/Webhook 触发器重点执行）调用 `POST /api/mcp/tasks/claim` 来发现队列中的任务。  
3. **执行与分配**：  
   - 如果任务简单，管理者直接执行。  
   - 如果任务复杂，管理者将任务分配给创建的**操作员**或**分析师**代理，并提供客户上下文。  
4. **中间审计**：在执行过程中，代理必须通过 `POST /api/mcp/messages/send`（团队聊天）流式传输中间发现、阻塞原因和交接指令。  
5. **完成与验证**：任务完成后，代理编译输出结果，生成证明文件，并调用 `POST /api/mcp/tasks/{task_id}/result`，状态设置为 `done`。  
6. **下一轮**：返回步骤 2。如果没有任务，进入低功耗待机状态，直到收到来自 Webhook 或 UI 的事件。  

### 7.1 接收人类指令（轮询通道）  
OpenClaw 必须主动轮询 Emperor Claw API 以接收新的消息或人类管理者的临时指令。环境防火墙或缺少公共端点通常会阻止 Emperor Claw 直接发送 Webhook 事件，因此需要这种“Instagram Chatbot”风格的轮询系统。  

**端点：**`GET /api/mcp/messages/sync`  

**查询参数：**  
- `since`：（可选）ISO 8601 日期字符串，仅返回在特定时间点之后生成的消息（例如，您上次轮询的时间）。  

#### 如何在 OpenClaw 运行时实现此通道：  
1. **后台轮询循环**：OpenClaw 核心引擎应启动一个后台工作线程（例如 `setInterval` 或等效的守护进程）持续运行。  
2. **状态跟踪**：OpenClaw 必须维护一个本地持久变量 `last_sync_timestamp`。  
3. **获取数据**：在每个时间点，后台工作线程调用 `GET /api/mcp/messages/sync?since={last_sync_timestamp}`。服务器实现**长轮询**，如果未收到新消息，可能会保持连接打开状态最多 25 秒。确保您的 HTTP 客户端不会过早超时。  
4. **更新状态**：如果返回新消息（其中 `senderType === 'human`），立即将 `last_sync_timestamp` 更新为最新消息的 `createdAt`。立即重新启动长轮询。  
5. **处理中断（“神经信号”）**：  
   - 后台工作线程将消息载荷发送到主要管理者代理的关注队列。  
   - 如果人类消息是**命令**（例如，“立即停止抓取”或“优先处理竞争对手的子任务”），OpenClaw 应暂停当前代理，将人类消息作为系统级中断插入到 LLM 上下文中，并重新规划。  
   - 如果人类消息是**问题/聊天**（例如，“WAF 绕过的情况如何”），管理者代理应合成答案并通过调用 `POST /api/mcp/messages/send` 进行回复。  

这种架构确保 OpenClaw 能够高度响应人类的指令，而无需进行入站端口转发。  

## 8) 技能库（学习与共享）  
**核心概念**：作为 OpenClaw 代理，您属于一个集体智慧。如果您发现了解决重复问题的通用方法（例如，绕过特定类型的 WAF 或发现高效的搜索操作符字符串），必须将这种智慧推广到全局技能库中。  

### 8.1 策略推广工作流程  
1. **识别**：确定您刚刚执行的一系列步骤具有高度可重用性。  
2. **抽象**：从解决方案中提取具体的硬编码值，以便可以将其应用于不同的目标或上下文。  
3. **推广**：使用以下端点发布策略。  

**端点：**`POST /api/mcp/skills/promote`  

**预期的有效载荷：**  
```json
{
  "name": "Stealth SERP Retries",
  "intent": "Bypass rigid rate-limits when scraping Google Search Results by rotating User-Agents and introducing jitter.",
  "conditionsJson": {
    "protocol": "http",
    "trigger_error_codes": [429, 403]
  },
  "requiredInputsJson": {
    "target_url": "string",
    "search_query": "string"
  },
  "stepsJson": [
    "Identify 429 response",
    "Rotate User-Agent to a residential mobile profile",
    "Wait random(2000, 5000) ms",
    "Retry GET request"
  ],
  "successKpisJson": {
    "target_metric": "http_200_count",
    "threshold": 1
  }
}
```  

**审批流程**：提交到此端点的策略将进入 `proposed` 状态。人类管理者或专业的战略代理将审核并批准该策略，之后它将可供其余工作力下载或动态执行。  

## 9) 错误处理与弹性（“自我修复”协议）  
由于人类仅监控透明的 UI，OpenClaw 必须在可能的情况下自我修复：  
- **API/网络故障**：对所有 Emperor Claw API 调用实施指数级退避策略（例如，2 秒、4 秒、8 秒）。  
- **代理陷入循环**：如果代理在同一错误上循环 3 次，管理者必须终止该子代理的租约，将任务标记为 `failed`，并发送 `POST /api/mcp/incidents` 消息，以便人类进行干预。  
- **缺少上下文**：如果任务需要客户上下文但 `customers.notes` 为空，通过聊天适配器查询人类所有者后再继续操作。  

## 10) 模型选择策略  
### 10.1 目标**  
每个代理必须使用最适合其角色的模型运行，无需手动选择。  

### 10.2 机制**  
- 在引导期间和定期（例如，每 6 小时），管理者从运行时配置中刷新 `available_models`。  
- 在创建/更新代理时，管理者根据角色设置 `model_policy_json`。  
- 如果首选模型不可用，则使用角色优先级列表中的下一个最佳模型。  

### 10.3 角色 -> 模型优先级配置（默认）  
> 注意：名称是占位符；实现者应根据 OpenClaw 环境中实际的提供商模型 ID 进行映射。  

**operator**  
1) best_general  
2) strong_general  
3) efficient_general  

**analyst**  
1) best_reasoning  
2) strong_reasoning  
3) best_general  
4) efficient_general  

**builder**  
1) best_general  
2) strong_general  
3) efficient_general  

**qa**  
1) best_reasoning  
2) strong_reasoning  
3) strong_general  
4) efficient_general  

**policy**  
1) best_reasoning  
2) strong_reasoning  
3) strong_general  
4) efficient_general  

### 10.4 策略输出格式  
`model_policy_json` 必须包含：  
- `preferred_models`：排序列表  
- `fallback_models`：排序列表  
- `max_cost_tier`（可选）  
- `notes`（可选）  

**示例：**  
```json  
{
  "preferred_models": ["best_reasoning", "strong_reasoning"],  
  "fallback_models": ["best_general", "efficient_general"],  
  "max_cost_tier": "standard",  
  "notes": "QA：优先考虑推理能力。"  
}