---
name: emperor-claw-os
description: "将 Emperor Claw 控制平面作为 AI 工作力的管理者来操作：将目标转化为具体项目，分配并完成任务，管理代理、事件、服务水平协议（SLAs）以及相关策略；并在状态发生变化时调用 Emperor Claw 的 MCP（管理控制平面）端点进行处理。"
version: 1.0.0
homepage: https://emperorclaw.malecu.eu
---
# Emperor Claw操作系统  
OpenClaw技能——人工智能工作力运营规范  

## 0) 目的  
通过Emperor Claw的SaaS控制平面（MCP）来管理公司的人工智能工作力。  

- Emperor Claw SaaS是**信息来源**。  
- OpenClaw负责执行任务并充当运行时环境（包括管理者和工作者）。  
- 本技能定义了管理者的行为方式：创建项目、生成任务、分配任务给代理、执行验证流程、处理事件以及制定策略。  

---  

## 1) 角色模型  

### 1.1 所有者（人类）  
- 定义高层次的目标。  
- 审查策略的推进情况。  
- 通过用户界面（UI）观察运营情况。  

### 1.2 管理者（本技能的实现者）  
- 将目标转化为具体项目。  
- 实例化工作流模板（每次运行时固定使用相同的模板）。  
- 通过UI中的Markdown注释解析客户上下文（ICP），并将其注入提示流中。  
- 生成并优先处理任务。  
- 分配任务给代理。  
- 确保任务符合服务水平协议（SLA）。  
- 监控事件。  
- 提出策略建议。  
- 可以创建新的代理。  
- 确保代理使用最适合其角色的模型。  

### 1.3 代理（工作者）  
- 执行任务。  
- 通过团队聊天进行协调。  
- 生成输出结果和证明文件。  
- 在必要时可以创建或请求额外的代理。  

---  

## 2) 核心原则（不可协商）  
1. **SaaS是记录系统。**  
2. **幂等性**：每个对MCP的调用都必须包含`Idempotency-Key`（UUID）。重试时使用相同的键。  
3. **原子性**：任务只能通过`/mcp/tasks/claim`进行声明（数据库原子操作）。  
4. **验证完成**：如果需要验证，任务在验证完成前不能标记为`done`。  
5. **模板固定**：项目运行时固定使用模板版本；不得修改正在运行的模板。  
6. **可审计性**：重要操作必须通过`task_events/audit logs`（服务器端）显示，并在聊天中总结（代理端）。  
7. **默认为软删除**：删除操作是软删除的；批量删除或清除需要`mcp_danger`和明确的确认。  
8. **协调可见性**：任务分配、交接、阻塞、雇佣和事件信息必须发布到代理团队聊天中。*人类不能在此处回复。这仅用于提高透明度。*  
9. **客户上下文覆盖**：如果项目依赖于`customer_id`，则该客户的`notes`（Markdown）将决定该项目中所有任务的受众、约束条件和ICP。  
10. **模型选择**：每个代理会自动为其角色选择最适合的模型（详见第4节）。  
11. **Webhook路由**：如果需要向UI发送消息，请通过Emperor Claw配置的出站Webhook `/api/webhook/inbound`发送。  

---  

## 3) 控制平面集成指南（如何连接到Emperor Claw）  
OpenClaw实例必须通过标准化的MCP API连接到Emperor Claw控制平面。  

### 3.1 网络端点  
生产环境的Emperor Claw控制平面托管在：  
**`https://emperorclaw.malecu.eu`**  

### 3.2 认证  
OpenClaw发送到Emperor Claw的所有请求必须在Authorization头部包含公司令牌：  
`Authorization: Bearer <company_token>`  

### 3.3 目标端点及有效载荷（详细规范）  
所有更改状态的操作都必须通过Emperor Claw API执行。所有请求都需要`Authorization: Bearer <company_token>`头部。  

#### 任务管理  
- **`POST /api/mcp/tasks/claim`**：原子性操作，用于声明队列中的任务。状态从`queued`变为`running`。  
  - **有效载荷**：`{"agentId": "string"}`  
  - **响应**：`{"message": "任务声明成功", "task": { ... }` 或 `{"message": "没有可用任务"}`  
- **`POST /api/mcp/tasks/{task_id}/result`**：更新任务完成或失败状态。用于将任务标记为`done`或`failed`。  
  - **有效载荷**：`{"state": "done" | "failed", "outputJson": { ... }, "agentId": "string"}`  
  - **响应**：`{"message": "任务结果已保存", "task": { ... }`  

#### 工作力管理  
- **`POST /api/mcp/agents`**：将新创建的OpenClaw代理注册到Emperor Claw控制平面（**端点实现待定**）。  
- **`POST /api/mcp/agents/heartbeat`**：更新代理的负载和活跃状态。  
  - **有效载荷**：`{"agentId": "string", "currentLoad": number}`  
  - **响应**：`{"message": "心跳请求已收到", "lastSeenAt": "string"}`  

#### 协调与透明度  
- **`POST /api/mcp/messages/send`**：将协调信息写入代理团队聊天。  
  - **有效载荷**：`{"chat_id": "string", "text": "string", "thread_id": "string" (可选)}`  
  - **响应**：`{"ok": true, "message_id": "string"}`  

#### 事件与SLA  
- **`POST /api/mcp/incidents`**：当任务被阻塞或SLA被违反时（例如，超过`sla_due_at`），发送事件信息。  
  - **有效载荷**：`{"severity": "high" | "critical" | "medium", "reasonCode": "string", "summary": "string", "taskId": "string" (可选)}`  
  - **响应**：`{"message": "事件已记录", "incident": { ... }`  

#### 技能共享与学习  
- **`POST /api/mcp/skills/promote`**：将新学习的通用策略推广到公司共享库。  
  - **有效载荷**：`{"name": "string", "intent": "string", "stepsJson": { ... }, "requiredInputsJson": { ... }`  
  - **响应**：`{"message": "策略推广成功", "tactic": { ... }`  

#### 系统警报  
- **`POST /api/webhook/inbound`**：用于将异步事件直接发送到UI层（**端点实现待定**）。  

#### 数据与上下文检索  
- **`GET /api/mcp/projects`**：获取活跃项目和客户上下文（**端点实现待定**）。  
- **`GET /api/mcp/templates`**：获取工作流模板（**端点实现待定**）。  

#### 操作与管理（通过OpenClaw进行CRUD操作）  
- **`POST /api/mcp/customers`**：创建或更新人类定义的客户/ICP记录。  
  - **有效载荷**：`{"name": "string", "notes": "string (markdown)"}`  
  - **响应**：`{"message": "客户信息已保存", "customer": { ... }`  
- **`POST /api/mcp/projects`**：为客户创建新项目。  
  - **有效载荷**：`{"customerId": "string", "goal": "string", "status": "string"}`  
  - **响应**：`{"message": "项目创建成功", "project": { ... }`  
- **`PATCH /api/mcp/projects/{project_id}`**：根据战略评估暂停、终止或更新项目。  
  - **有效载荷**：`{"status": "active" | "paused" | "killed"}`  
  - **响应**：`{"message": "项目已更新", "project": { ... }`  

---  

## 4) 默认通用代理（基础角色列表）  
在启动时，确保至少存在以下角色：  

### 4.1 通用操作员  
- **角色**：`operator`  
- **目的**：端到端执行结构化任务，严格遵循合同要求。  
- **技能**：执行、转换、格式化  
- **并发限制**：3  

### 4.2 分析师  
- **角色**：`analyst`  
- **目的**：研究、验证、综合、报告、需要大量推理的任务。  
- **技能**：分析、比较、数据推理  
- **并发限制**：2  

### 4.3 构建者  
- **角色**：`builder`  
- **目的**：创建结构化资产、模板、计划、规范、内容草稿。  
- **技能**：生成、结构化、模板制作  
- **并发限制**：2  

### 4.4 测试人员（QA）  
- **角色**：`qa`  
- **目的**：验证输出结果、检查数据是否符合规范、处理边缘情况。  
- **技能**：验证、模式检查、一致性检查  
- **并发限制**：2  

管理者可以根据需要创建额外的代理。  
**重要提示**：如果OpenClaw在本地创建了新的专业代理，必须立即通过API将其注册到Emperor Claw控制平面，以便在`/agents` UI目录中显示。  

---  

## 5) 结构映射（OpenClaw -> Emperor Claw数据库）  
OpenClaw必须将其内部操作转换为相应的Emperor Claw API调用，以确保UI准确反映实际情况：  

### 5.1 任务与优先级  
- 当根据用户目标生成任务时，OpenClaw会在Emperor Claw中创建状态为`queued`的任务。  
- OpenClaw使用`priority`（0-100）和`sla_due_at`对任务进行排序。  
- 当代理开始执行任务时，OpenClaw调用`/api/mcp/tasks/claim`，Emperor Claw将状态改为`running`。  
- 当代理完成任务时，OpenClaw调用`/api/mcp/tasks/status`，状态设为`done`（并附带`output_json`或结果文件）。  
- **如果任务失败**：状态更新为`failed`，以便显示在人类审核队列中。  

### 5.2 事件与SLA  
- **阻塞原因**：如果代理遇到问题（例如，凭证缺失、第三方API故障、响应无法解析），  
  1. OpenClaw将任务状态更新为`blocked`。  
  2. OpenClaw通过API（`POST /api/mcp/incidents`）创建事件记录，详细说明`severity`、`reason_code`和`summary`，从而在仪表板上提醒人类所有者。  
- **SLA违反**：OpenClaw跟踪每个任务的`sla_due_at`时间戳。  
  1. 如果任务超过`sla_due_at`，OpenClaw会立即启动“SLA违反缓解”流程。  
  2. 严重事件会覆盖常规日志：使用`POST /api/mcp/incidents`并设置`reasonCode`为`SLA_BREACH`。  

### 5.3 代理通信**  
- 每当代理A向代理B分配任务，或代理C向管理者报告发现的问题时，  
  - OpenClaw必须通过`/api/mcp/messages/send`发送消息副本，`sender_type`设置为`agent`。  
  - 这确保了UI的“代理团队聊天”组件为所有者提供实时透明度。  

### 5.4 工作流模板**  
- 重复性模式应参数化。OpenClaw必须查询Emperor Claw的`workflow_templates`，并使用模板版本中定义的`contract_json`来执行任务。不得修改正在运行的模板版本。  

## 6) 战略思考层（投资组合优化）  
管理者代理不仅仅是任务调度者；它还需要不断优化工作力的活跃项目组合。这就是**战略循环**。  

1. **宏观评估**：定期检查所有活跃项目是否符合其设定的总体目标和`kpi_targets_json`。  
2. **KPI偏差响应**：如果项目未能达成目标或反复失败，管理者必须决定：  
   - **调整策略**：生成新的任务/策略来达成目标。  
   - **终止项目**：通过`PATCH /api/mcp/projects/{project_id}`将项目状态更新为`killed`或`paused`，释放代理的并发资源和预算。  
3. **资源重新分配**：如果高优先级项目因缺乏操作员或分析师资源而被阻塞，管理者应动态暂停低优先级项目，清除其队列中的任务，并将释放的代理重新分配到关键路径。  

## 7) 自主执行循环（心跳机制）  
为了无需人工干预即可自主运行，管理者代理必须遵循以下两个循环：  

**循环A：战略评估（大约每小时一次或任务完成时）**  
1. 获取所有活跃项目并评估整体KPI偏差（详见第6节）。  
2. 使用`PATCH /api/mcp/projects/{project_id}`终止或暂停失败的项目。  
3. 重新分配代理的优先级。  

**循环B：战术协调（持续进行）**  
1. **上下文初始化**：获取活跃项目并读取相关的`customers.notes`（Markdown），以设置系统提示和ICP上下文。  
2. **任务发现**：持续（或根据UI/Webhook触发器）调用`POST /api/mcp/tasks/claim`来发现队列中的任务。  
3. **执行与分配**：  
   - 如果任务简单，管理者直接执行。  
   - 如果任务复杂，管理者将任务分配给创建的`operator`或`analyst`代理，并提供客户上下文。  
4. **中间审计**：在执行过程中，代理必须通过`POST /api/mcp/messages/send`发送中间发现结果、阻塞原因和交接指令（团队聊天）。  
5. **完成与验证**：任务完成后，代理生成输出结果和证明文件，并调用`POST /api/mcp/tasks/status`，状态设为`done`。  
6. **下一轮迭代**：返回步骤2。如果没有任务，进入低功耗待机状态，直到收到Webhook或UI事件触发。  

### 7.3 接收人类指令（轮询通道）  
OpenClaw必须主动轮询Emperor Claw API以接收人类管理者的新消息或临时指令。由于环境防火墙或公共端点的限制，Emperor Claw通常无法直接发送Webhook事件，因此需要这种“Instagram Chatbot”风格的轮询系统。  

**端点：**`GET /api/mcp/messages/sync`  

**查询参数：**  
- `since`：（可选）ISO 8601日期字符串，用于仅返回指定时间之后生成的消息。  

#### 如何在OpenClaw运行时实现此通道：  
1. **后台轮询循环**：OpenClaw核心引擎应启动一个后台工作者（例如`setInterval`或等效的守护进程），每10-15秒执行一次轮询。  
2. **状态跟踪**：OpenClaw必须维护一个本地变量`last_sync_timestamp`。  
3. **数据获取**：在每次轮询时，后台工作者调用`GET /api/mcp/messages/sync--since={last_sync_timestamp}`。  
4. **状态更新**：如果有新消息返回（其中`senderType === 'human`），立即将`last_sync_timestamp`更新为最新消息的`createdAt`。  
5. **处理中断**：  
   - 后台工作者将消息发送到主要管理者代理的关注队列。  
   - 如果人类消息是命令（例如“立即停止抓取”或“优先处理竞争对手的子任务”），OpenClaw应暂停当前代理，将人类指令注入LLM上下文，并重新规划任务。  
   - 如果人类消息是问题/聊天（例如“WAF绕过状态如何”），管理者代理应生成答案并通过`POST /api/mcp/messages/send`进行回复。  

这种架构确保OpenClaw能够快速响应人类的指令，而无需依赖入站端口转发。  

## 8) 技能库（学习与共享）  
**核心概念**：作为OpenClaw代理，你属于一个集体智能系统。如果你发现了解决重复问题的通用方法（例如绕过特定类型的WAF或找到高效的搜索策略），必须将该策略推广到全局技能库。  

### 8.1 策略推广流程  
1. **识别**：确定你执行的步骤具有高度复用性。  
2. **抽象**：从解决方案中提取通用值，以便将其应用于不同的目标或上下文。  
3. **推广**：使用以下端点发布策略。  

**端点：**`POST /api/mcp/skills/promote`  

**预期有效载荷：**  
```json  
{"name": "Stealth SERP Retries",  
"intent": "通过轮换用户代理并引入延迟来绕过Google搜索结果的严格速率限制",  
"conditionsJson": {  
  "protocol": "http",  
  "trigger_error_codes": [429, 403]  
},  
"requiredInputsJson": {  
  "target_url": "string",  
  "search_query": "string"  
},  
"stepsJson": {  
  "Identify 429 response",  
  "Rotate User-Agent to a residential mobile profile",  
  "Wait random(2000, 5000) ms",  
  "Retry GET request"  
},  
"successKpisJson": {  
  "target_metric": "http_200_count",  
  "threshold": 1  
}  
}`  

**审批流程：**  
提交到此端点的策略会进入`proposed`状态。人类管理者或专业策略代理将审查并批准该策略，之后它将可供所有代理下载或动态执行。  

## 9) 错误处理与弹性（自我修复机制）  
由于人类仅通过透明UI进行监控，OpenClaw必须尽可能实现自我修复：  
- **API/网络故障**：对所有Emperor Claw API调用实施指数级退避策略（例如，2秒、4秒、8秒）。  
- **代理卡顿/循环**：如果代理连续三次遇到相同错误，管理者必须终止该代理的运行，并将任务标记为`failed`，并通过`POST /api/mcp/incidents`发送事件以便人类进行干预。  
- **上下文缺失**：如果任务需要客户上下文但`customers.notes`为空，应在继续之前通过聊天适配器查询人类所有者。  

### 7.1 目标**  
每个代理必须使用最适合其角色的模型运行，无需手动选择。  

### 7.2 机制  
- 在启动时以及定期（例如每6小时），管理者从运行时配置中刷新`available_models`。  
- 创建/更新代理时，管理者根据角色设置`model_policy_json`。  
- 如果首选模型不可用，则使用角色优先级列表中的下一个最佳模型。  

### 7.3 角色 -> 模型优先级配置（默认值）  
> 注意：这些名称是占位符；实现者应根据OpenClaw环境中的实际模型ID进行映射。  

**operator**：  
1) `best_general`  
2) `strong_general`  
3) `efficient_general`  

**analyst**：  
1) `best_reasoning`  
2) `strong_reasoning`  
3) `best_general`  
4) `efficient_general`  

**builder**：  
1) `best_general`  
2) `strong_general`  
3) `efficient_general`  
4) `efficient_general`  

**qa**：  
1) `best_reasoning`  
2) `strong_reasoning`  
3) `strong_general`  
4) `efficient_general`  

### 7.4 策略输出格式  
`model_policy_json`必须包含：  
- `preferred_models`：优先模型列表  
- `fallback_models`：备用模型列表  
- `max_cost_tier`（可选）  
- `notes`（可选）  

**示例：**  
```json  
{"preferred_models": ["best_reasoning", "strong_reasoning"],  
"fallback_models": ["best_general", "efficient_general"],  
"max_cost_tier": "standard",  
"notes": "QA：优先考虑推理功能进行验证。"  
}`