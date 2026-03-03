---
name: clawdtalk-client
version: 2.0.0
description: >
  **ClawdTalk** — 为 **Clawdbot** 提供的语音通话、短信发送以及人工智能任务处理功能  
  ClawdTalk 是一款专为 **Clawdbot** 设计的通信与任务管理工具，它支持语音通话、短信发送以及基于人工智能（AI）的任务执行。通过集成这些功能，**Clawdbot** 能够更高效地与用户进行交互、处理信息，并执行各种自动化任务。
metadata: {"clawdbot":{"emoji":"📞","primaryEnv":"CLAWDTALK_API_KEY","homepage":"https://github.com/team-telnyx/clawdtalk-client","requires":{"env":["CLAWDTALK_API_KEY"],"bins":["bash","node","jq","python3"],"config":["skill-config.json","~/.openclaw/openclaw.json","~/.clawdbot/clawdbot.json"]}}}
---
# ClawdTalk

> ⚠️ **首次设置？** 在进行任何操作之前，请先阅读本目录中的 `SETUP.md` 文件。该文件会逐步指导您完成整个配置流程。

Clawdbot 支持语音通话、短信发送以及人工智能任务。您可以通过电话呼叫机器人、发送短信，或运行自动化的多步骤推广活动——这一切都由 ClawdTalk 提供支持。

> **注意事项：** 使用此功能时，语音记录、短信内容以及任务数据将会被发送到 clawdtalk.com（由 Telnyx 运营）。只有在您信任该服务会妥善处理您的对话数据的情况下，才请安装该功能。

## 外部端点

| 端点 | 使用者 | 发送的数据 |
|----------|---------|-----------|
| `https://clawdtalk.com` (WebSocket) | `ws-client.js` | 语音记录、工具结果、对话状态 |
| `https://clawdtalk.com/v1/*` | `telnyx_api.py` | 任务状态、事件、预定的通话/短信、助手配置 |
| `http://127.0.0.1:<port>` | `ws-client.js` | 转录的语音（仅限本地网关） |
| `https://raw.githubusercontent.com/team-telnyx/clawdtalk-client/...` | `update.sh` | 无（仅用于下载） |

## 安全与隐私

- 语音记录和短信内容会传输到 clawdtalk.com。
- 任务状态和事件会被存储在服务器端，以便进行追踪和分析。
- `setup.sh` 会读取网关配置以提取连接详细信息；确认后，它会将 `sessions_send` 添加到 `gateway.tools.allow` 中。
- API 密钥存储在 `skill-config.json` 中——请使用环境变量 `CLAWDTALK_API_KEY` 或 `${CLAWDTALK_API_KEY}` 来避免明文存储。

---

# ⚠️ 重要提示：**slug 一致性**

`init` 命令会自动从任务名称生成一个 slug（小写，空格替换为连字符）。**所有需要使用 slug 的命令（如 `setup-agent`、`save-memory`、`complete`）都必须使用完全相同的 slug**。
如果 slug 不匹配，会导致代理未关联，从而导致预定的事件在用户界面上显示不出来。

```bash
# After init, ALWAYS confirm the slug:
python scripts/telnyx_api.py list-state
# Output: find-window-washing-contractors: Find window washing contractors [running]
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ COPY-PASTE THIS. NEVER ABBREVIATE.
```

---

# ⚠️ 重要提示：**任务生命周期由您控制**

**服务器不会自动更新任务步骤或任务状态**。这是作为机器人的您的职责。如果您不更新步骤或完成任务，用户界面将永远显示“运行中”，并且所有步骤都会显示为“待处理”。

## 您的责任

对于每个任务，您必须：
1. **更新任务步骤**——将每个步骤的状态从“进行中”更改为“已完成”或“失败”。
2. **记录事件**——在每个重要操作之后。
3. **检查任务是否完成**——确认预定的通话/短信是否已经发送。
4. **完成任务**——将任务状态更改为“成功”或“失败”。
5. **清理**——任务结束后，删除所有相关的定时任务。

用户界面会准确反映您的操作。如果您不进行任何更新，界面上也不会显示任何变化。

---

# 🚨 强制要求：**每次操作后都必须保存到内存**

**每次重要操作完成后，都必须立即使用 `save-memory` 或 `append-memory` 命令将其保存到内存中**。前端会从服务器内存中读取数据。如果不保存，这些操作将不会显示在界面上。仅使用 `log-event` 是不够的。

> **规则：** 如果您进行了任何操作，就必须立即保存到内存中。没有例外，不要说“稍后处理”。现在就执行。

示例（安排短信）：
```bash
# 1. Schedule it
python scripts/telnyx_api.py schedule-sms $AID "$TO" "$FROM" "$DATETIME" "$MESSAGE" $MID $RID $STEP_ID

# 2. IMMEDIATELY save to memory
python scripts/telnyx_api.py append-memory "$SLUG" "scheduled_events" \
  '{"event_id": "<id>", "type": "sms", "to": "<to>", "message": "<msg>", "scheduled_at": "<dt>", "step_id": "<step>"}'

# 3. Then log the event
python scripts/telnyx_api.py log-event $MID $RID custom "Scheduled SMS event_id=<id>" $STEP_ID
```

**跳过步骤 2 是导致“用户界面上什么都没有显示”的最主要原因**。

---

# 🚨 强制要求：**每次步骤完成后都必须检查任务状态**

**在完成或失败任何步骤后，都必须确认任务是否应该被视为已完成或失败**。切勿将任务状态留在“进行中”状态，即使任务实际上已经完成或失败。

> **规则：** 每次步骤状态发生变化后，都要问自己：这个任务是否已经完成？

### 决策树（在每个步骤之后执行）：

```
Step finished →
  ├── Succeeded?
  │     ├── All steps done? → COMPLETE MISSION (update-run succeeded)
  │     ├── More steps remain? → Continue to next step
  │     └── Only verify left? → Set up polling cron
  └── Failed?
        ├── Recoverable (retry/reschedule)? → Retry
        └── Unrecoverable? → FAIL MISSION NOW:
              1. update-step <step_id> failed
              2. log-event error "Failed: <reason>" <step_id>
              3. save-memory "$SLUG" "error_<step_id>" '{"error": "...", "recoverable": false}'
              4. update-run $MID $RID failed
              5. save-memory "$SLUG" "result" '{"status": "failed", "reason": "...", "failed_step": "..."}'
              6. Clean up any polling cron jobs
```

**如果任务实际上已经完成或失败，但仍然显示为“进行中”，那就是一个错误。用户会误以为任务仍在继续进行。**

---

# 架构概述

## 各部分之间的协作方式

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│  You (Bot)   │────▶│  ClawdTalk Server │────▶│  Telnyx API  │
│              │     │  (dev/prod)       │     │  (cloud)     │
│ telnyx_api.py│     │  Local DB + proxy │     │  Executes    │
│              │     │  to Telnyx        │     │  calls/SMS   │
└──────────────┘     └──────────────────┘     └──────────────┘
```

- **telnyx_api.py** — Python 命令行接口脚本。您执行的每个命令都会通过这个脚本与 ClawdTalk 服务器通信，而不会直接与 Telnyx 交互。
- **ClawdTalk 服务器** — Node.js 后端。它将任务、助手和事件存储在本地 Postgres 数据库中，并将请求代理到 Telnyx API。
- **Telnyx API** — 云服务。它会在预定时间实际发起通话并发送短信。

## 关键文件

| 文件 | 用途 |
|---|---|
| `scripts/telnyx_api.py` | 用于所有任务/助手/事件操作的命令行工具 |
| `scripts/connect.sh` | 用于处理传入语音通话的 WebSocket 客户端 |
| `skill-config.json` | API 密钥和服务器地址 |
| `.missions_state.json` | 活动任务的本地状态跟踪 |
| `.connect.log` | WebSocket 连接日志 |

## 两种 ID

每个实体在两个地方都有不同的 ID：
- **本地数据库 ID** — ClawdTalk 服务器返回的 ID（例如 `3df24dde-...`）
- **Telnyx ID** — Telnyx API 内部使用的 ID

脚本始终使用本地 ID。您无需关心 Telnyx ID。

---

## 快速入门

1. **在 [clawdtalk.com](https://clawdtalk.com) 注册**
2. **在设置中添加您的电话号码**
3. **从仪表板获取 API 密钥**
4. **运行设置脚本**：`./setup.sh`
   > `setup.sh` 会读取您的网关配置以提取连接详细信息，并在确认后，将 `sessions_send` 添加到 `gateway.tools.allow` 中。网关配置文件位于 `~/.openclaw/openclaw.json` 或 `~/.clawdbot/clawdbot.json`。
5. **启动连接**：`./scripts/connect.sh start`

## 语音通话

WebSocket 客户端会将通话路由到您网关的主代理会话，从而提供对内存、工具和上下文的完全访问权限。

```bash
./scripts/connect.sh start     # Start connection
./scripts/connect.sh stop      # Stop
./scripts/connect.sh status    # Check status
```

### 外出通话

让机器人给您或其他人打电话：

```bash
./scripts/call.sh                              # Call your phone
./scripts/call.sh "Hey, what's up?"            # Call with greeting
./scripts/call.sh --to +15551234567            # Call external number*
./scripts/call.sh --to +15551234567 "Hello!"   # External with greeting
./scripts/call.sh status <call_id>             # Check call status
./scripts/call.sh end <call_id>                # End call
```

*外部通话需要一个付费账户和专用号码。在拨打外部号码时，AI 会以隐私模式运行（不会泄露您的私人信息）。

## 短信

发送和接收短信：

```bash
./scripts/sms.sh send +15551234567 "Hello!"
./scripts/sms.sh list
./scripts/sms.sh conversations
```

## 人工智能任务（通过 Python 完全跟踪）

对于需要完整跟踪、状态保存、重试和对话分析的复杂多步骤任务，请使用基于 Python 的任务 API。

**要求**：Python 3.7 及以上版本，以及 `CLAWDTALK_API_KEY` 环境变量。可选地，您可以通过设置 `CLAWDTALK_API_URL` 来覆盖默认的 API 端点（默认为 `https://clawdtalk.com/v1`）。

```bash
python scripts/telnyx_api.py check-key    # Verify setup
```

# 重要提示：**频繁保存状态**

**每次进行重要操作后，都必须保存进度**。如果会话崩溃或重新启动，未保存的数据将会丢失。

## 双层存储：内存 + 事件

数据必须同时保存在两个地方：
1. **本地内存**（`.missions_state.json`）——快速，可恢复重启后的数据。
2. **事件 API**（云端）——永久的审计记录，可在本地文件丢失后仍然可用。

## 何时保存（每次操作后！）

| 操作 | 保存到内存 | 记录事件 |
|--------|-------------|-----------|
| 网页搜索返回结果 | append-memory | log-event (tool_call) |
| 找到承包商/潜在客户 | append-memory | log-event (custom) |
| 创建助手 | save-memory | log-event (custom) |
| 分配电话号码 | save-memory | log-event (custom) |
| 预定通话/短信 | append-memory | log-event (custom) |
| 通话完成 | save-memory | log-event (custom) |
| 获得报价/洞察 | save-memory | log-event (custom) |
| 做出决定 | save-memory | log-event (message) |
| 步骤开始 | save-memory | update-step (in_progress) + log-event (step_started) |
| 步骤完成 | save-memory | update-step (completed) + log-event (step_completed) |
| 步骤失败 | save-memory | update-step (failed) + log-event (error) |
| 发生错误 | save-memory | log-event (error) |

## 内存操作（本地备份）

```bash
# Save a single value
python scripts/telnyx_api.py save-memory "<slug>" "key" '{"data": "value"}'

# Append to a list (great for collecting multiple items)
python scripts/telnyx_api.py append-memory "<slug>" "contractors" '{"name": "ABC Co", "phone": "+1234567890"}'

# Retrieve memory
python scripts/telnyx_api.py get-memory "<slug>"           # Get all memory
python scripts/telnyx_api.py get-memory "<slug>" "key"     # Get specific key
```

## 事件操作（云端备份）

```bash
# Log an event (step_id is REQUIRED - links event to a plan step)
python scripts/telnyx_api.py log-event <mission_id> <run_id> <type> "<summary>" <step_id> '[payload_json]'

# Event types: tool_call, custom, message, error, step_started, step_completed
# step_id: Use the step_id from your plan (e.g., "research", "setup", "calls")
#          Use "-" if event doesn't belong to a specific step
```

---

## 何时使用任务

此功能有两种模式：**完整任务**（可跟踪、多步骤）和 **简单通话**（一次性、无需任务开销）。请根据需要选择合适的模式。

### 在以下情况下使用完整任务：
- 任务涉及**多次通话或短信**（批量推广、调查、扫雷）
- 需要**完整的审计记录**，包括事件、计划和状态跟踪
- 任务是**多步骤的**，且需要跨多个阶段进行
- 需要**重试和失败跟踪**
- 需要**比较多次通话的结果**

示例：
- “在芝加哥寻找窗户清洗承包商，给他们打电话并协商价格”
- “联系列表中的所有潜在客户并安排演示”
- “拨打 10 个气象站的电话，找出温度最高的一个”

### 以下情况下不要使用任务：
- 任务是一次性**外出通话**——只需创建一个助手（或重用现有的助手）并直接安排通话
- 这是一次性**短信**——安排好即可
- 任务不需要跟踪、计划或状态恢复
- 如果任务只包含一个步骤和一次通话，那么创建任务就是过度设计

**对于简单通话，只需：**
```bash
# Reuse or create an assistant
python scripts/telnyx_api.py list-assistants --name=<relevant>
# Schedule the call
python scripts/telnyx_api.py schedule-call <assistant_id> <to> <from> <datetime> <mission_id> <run_id>
# Poll for completion
python scripts/telnyx_api.py get-event <assistant_id> <event_id>
# Get insights
python scripts/telnyx_api.py get-insights <conversation_id>
```

不需要任务，无需运行，也无需计划。保持简单。

## 状态保存

脚本会自动在 `.missions_state.json` 中管理状态。这可以在重启后保持数据的一致性，并支持多个并发任务。

```bash
python scripts/telnyx_api.py list-state                              # List all active missions
python scripts/telnyx_api.py get-state "find-window-washing-contractors"  # Get state for specific mission
python scripts/telnyx_api.py remove-state "find-window-washing-contractors" # Remove mission from state
```

## 核心工作流程

## 第 1 阶段：初始化跟踪

### 步骤 1.1：创建任务

```bash
python scripts/telnyx_api.py create-mission "Brief descriptive name" "Full description of the task"
```

**保存返回的 `mission_id`**——后续所有通话都需要这个 ID。

### 步骤 1.2：启动任务

```bash
python scripts/telnyx_api.py create-run <mission_id> '{"original_request": "The exact user request", "context": "Any relevant context"}'
```

**保存返回的 `run_id`**。

### 步骤 1.3：制定计划**

在执行之前，先规划好您的计划：

```bash
python scripts/telnyx_api.py create-plan <mission_id> <run_id> '[
  {"step_id": "step_1", "description": "Research contractors online", "sequence": 1},
  {"step_id": "step_2", "description": "Create voice agent for calls", "sequence": 2},
  {"step_id": "step_3", "description": "Schedule calls to each contractor", "sequence": 3},
  {"step_id": "step_4", "description": "Monitor call completions", "sequence": 4},
  {"step_id": "step_5", "description": "Analyze results and select best options", "sequence": 5}
]'
```

### 步骤 1.4：将任务设置为“进行中”

```bash
python scripts/telnyx_api.py update-run <mission_id> <run_id> running
```

### 高级替代方案：一次性完成所有设置

使用 `init` 命令一次性创建任务、启动任务、制定计划并设置状态：

```bash
python scripts/telnyx_api.py init "Find window washing contractors" "Find contractors in Chicago, call them, negotiate rates" "User wants window washing quotes" '[
  {"step_id": "research", "description": "Find contractors online", "sequence": 1},
  {"step_id": "setup", "description": "Create voice agent", "sequence": 2},
  {"step_id": "calls", "description": "Schedule and make calls", "sequence": 3},
  {"step_id": "analyze", "description": "Analyze results", "sequence": 4}
]'
```

如果已经存在同名任务，这个命令也会自动恢复任务。

**⚠️ 在执行 `init` 命令后，立即运行 `list-state` 并复制返回的 slug。在后续的所有命令中都使用这个 slug。**

---

## 第 2 阶段：设置语音/短信助手

当您的任务需要拨打电话或发送短信时，首先创建一个 AI 助手。

### 步骤 2.1：创建语音/短信助手

**对于电话通话：**
```bash
python scripts/telnyx_api.py create-assistant "Contractor Outreach Agent" "You are calling on behalf of [COMPANY]. Your goal is to [SPECIFIC GOAL]. Be professional and concise. Collect: [WHAT TO COLLECT]. If they cannot talk now, ask for a good callback time." "Hi, this is an AI assistant calling on behalf of [COMPANY]. Is this [BUSINESS NAME]? I am calling to inquire about your services. Do you have a moment?" '["telephony", "messaging"]'
```

**对于短信：**
```bash
python scripts/telnyx_api.py create-assistant "SMS Outreach Agent" "You send SMS messages to collect information. Keep messages brief and professional." "Hi! I am reaching out on behalf of [COMPANY] regarding [PURPOSE]. Could you please reply with [REQUESTED INFO]?" '["telephony", "messaging"]'
```

**保存返回的 `assistant_id`**。

### 步骤 2.2：查找并分配电话号码**

```bash
python scripts/telnyx_api.py get-available-phone                          # Get first available
python scripts/telnyx_api.py get-connection-id <assistant_id> telephony   # Get connection ID
python scripts/telnyx_api.py assign-phone <phone_number_id> <connection_id> voice  # Assign
```

### 高级替代方案：一次性完成设置**

```bash
python scripts/telnyx_api.py setup-agent "find-window-washing-contractors" "Contractor Caller" "You are calling to get quotes for commercial window washing. Ask about: rates per floor, availability, insurance. Be professional." "Hi, I am calling to inquire about your commercial window washing services. Do you have a moment to discuss rates?"
```

这个命令会自动创建助手，将其关联到任务，找到一个可用的电话号码，分配给助手，并将所有 ID 保存到状态文件中。

**⚠️ 确保使用的 slug 与 `init` 命令生成的 slug 相匹配。如果不匹配，助手将无法关联，预定的事件也不会显示在用户界面上。**

**执行关联操作后立即验证：**
```bash
python scripts/telnyx_api.py list-linked-agents <mission_id> <run_id>
# Must show your assistant_id. If empty → slug was wrong. Fix with:
python scripts/telnyx_api.py link-agent <mission_id> <run_id> <assistant_id>
```

### 步骤 2.3：将助手关联到任务**

**如果使用 `setup-agent` 命令**：关联操作会自动完成（前提是 slug 匹配）。

**如果手动设置：**
```bash
python scripts/telnyx_api.py link-agent <mission_id> <run_id> <assistant_id>
python scripts/telnyx_api.py list-linked-agents <mission_id> <run_id>
python scripts/telnyx_api.py unlink-agent <mission_id> <run_id> <assistant_id>
```

---

## 第 3 阶段：安排通话/短信

### 考虑营业时间

**重要提示**：在安排通话之前，请考虑营业时间（当地时间上午 9 点至下午 5 点）。`scheduled_at` 必须在未来（至少 1 分钟之后）。

```bash
python scripts/telnyx_api.py schedule-call <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" <mission_id> <run_id>
python scripts/telnyx_api.py schedule-sms <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" "Your message here"
```

**保存返回的事件 `id`**。

---

## 第 4 阶段：监控通话完成情况

### ⚠️ 这是最重要的部分

安排通话或短信后，**Telnyx 会自动在预定时间执行**。您需要**定期检查**以确认通话是否完成，然后相应地更新任务状态。

### 检查预定事件的状态

```bash
python scripts/telnyx_api.py get-event <assistant_id> <event_id>
```

### 使用定时任务进行检查

使用机器人的定时系统来安排检查。**不要阻塞主会话**。根据预计的等待时间设置检查间隔：

| 预计完成时间 | 检查间隔 | 示例 |
|---|---|---|
| 小于 5 分钟 | 每 30 秒 | 立即发送短信 |
| 5–30 分钟 | 每 2–5 分钟 | 15 分钟后安排的通话 |
| 1–24 小时 | 每 15–30 分钟 | 今晚安排的通话 |
| 多天/多周 | 每 4–8 小时 | 下周安排的通话 |

**如果您知道确切的预定时间**，请在该时间之后再开始检查。首次检查应在 `scheduled_time + 2 分钟` 后进行。**

### 定时任务模式

安排通话/短信后，创建一个定时任务来检查任务进度：

```
Create cron: poll at appropriate interval
  → Run get-event <assistant_id> <event_id>
  → If completed: update step, log event, complete mission if last step, DELETE THIS CRON
  → If failed: update step as failed, log error, DELETE THIS CRON
  → If pending/in_progress: do nothing, cron runs again at next interval
```

**⚠️ 任务达到最终状态（完成、失败或取消）时，必须立即删除相应的定时任务**。任务结束后，务必停止运行定时任务。**

### 调整检查间隔

根据情况变化调整定时任务间隔：
- 如果任务安排在 2 周后：开始时使用 8 小时的检查间隔。
- 随着预定时间的临近（1 小时内），将检查间隔缩短至 5 分钟。
- 预定时间过后：将检查间隔缩短至 30 秒。

### 事件状态含义及相应操作

| 状态 | 含义 | 操作 |
|--------|---------|--------|
| `pending` | 等待预定时间 | 继续检查 |
| `in_progress` | 通话/短信正在进行中 | 继续检查 |
| `completed` | 通话成功完成 | 更新步骤状态，并获取相关洞察 |
| `failed` | 重试后失败 | 将步骤状态更新为失败，并考虑是否需要重试 |

### 通话状态含义及相应操作（仅适用于电话通话）

| call_status | 含义 | 操作 |
|-------------|---------|--------|
| `ringing` | 电话正在响铃 | 1–2 分钟后再检查一次 |
| `in_progress` | 通话正在进行中 | 2–3 分钟后再检查一次 |
| `completed` | 通话正常完成 | 获取相关洞察 |
| `no-answer` | 无人接听 | **可重试**——重新安排 |
| `busy` | 电话占线 | **可重试**——10–15 分钟后再尝试 |
| `cancelled` | 通话被取消 | 查看是否是故意的 |
| `failed` | 系统错误 | **可重试**——10–15 分钟后再尝试 |

---

## 第 5 阶段：获取通话洞察

通话完成后，如果获得了 `conversation_id`，请获取相关洞察。**在状态变为“completed”之前，持续进行检查**（每次检查之间间隔 10 秒）。

```bash
python scripts/telnyx_api.py get-insights <conversation_id>
```

当创建助手时，Telnyx 会自动生成默认的洞察模板。您无需手动管理这些模板——只需读取结果即可。

---

## 第 6 阶段：完成任务

```bash
python scripts/telnyx_api.py update-run <mission_id> <run_id> succeeded

# Or with full results:
python scripts/telnyx_api.py complete "find-window-washing-contractors" <mission_id> <run_id> "Summary of results" '{"key": "payload"}'
```

---

# 事件日志参考

**将每个操作都记录为事件**。始终通过 `update-step` 更新步骤状态，并记录相应的事件。

```bash
# When STARTING a step:
python scripts/telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "research" "in_progress"
python scripts/telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" step_started "Starting: Research" "research"

# When COMPLETING a step:
python scripts/telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "research" "completed"
python scripts/telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" step_completed "Completed: Research" "research"

# When a step FAILS:
python scripts/telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "calls" "failed"
python scripts/telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" error "Failed: Could not reach contractors" "calls"
```

---

# 快速参考：所有 Python 命令

```bash
# Check setup
python scripts/telnyx_api.py check-key

# Missions
python scripts/telnyx_api.py create-mission <name> <instructions>
python scripts/telnyx_api.py get-mission <mission_id>
python scripts/telnyx_api.py list-missions

# Runs
python scripts/telnyx_api.py create-run <mission_id> <input_json>
python scripts/telnyx_api.py get-run <mission_id> <run_id>
python scripts/telnyx_api.py update-run <mission_id> <run_id> <status>
python scripts/telnyx_api.py list-runs <mission_id>

# Plan
python scripts/telnyx_api.py create-plan <mission_id> <run_id> <steps_json>
python scripts/telnyx_api.py get-plan <mission_id> <run_id>
python scripts/telnyx_api.py update-step <mission_id> <run_id> <step_id> <status>

# Events
python scripts/telnyx_api.py log-event <mission_id> <run_id> <type> <summary> <step_id> [payload_json]
python scripts/telnyx_api.py list-events <mission_id> <run_id>

# Assistants
python scripts/telnyx_api.py list-assistants [--name=<filter>] [--page=<n>] [--size=<n>]
python scripts/telnyx_api.py create-assistant <name> <instructions> <greeting> [options_json]
python scripts/telnyx_api.py get-assistant <assistant_id>
python scripts/telnyx_api.py update-assistant <assistant_id> <updates_json>
python scripts/telnyx_api.py get-connection-id <assistant_id> [telephony|messaging]

# Phone Numbers
python scripts/telnyx_api.py list-phones [--available]
python scripts/telnyx_api.py get-available-phone
python scripts/telnyx_api.py assign-phone <phone_id> <connection_id> [voice|sms]

# Scheduled Events
python scripts/telnyx_api.py schedule-call <assistant_id> <to> <from> <datetime> <mission_id> <run_id>
python scripts/telnyx_api.py schedule-sms <assistant_id> <to> <from> <datetime> <text>
python scripts/telnyx_api.py get-event <assistant_id> <event_id>
python scripts/telnyx_api.py cancel-scheduled-event <assistant_id> <event_id>
python scripts/telnyx_api.py list-events-assistant <assistant_id>

# Insights
python scripts/telnyx_api.py get-insights <conversation_id>

# Mission Run Agents
python scripts/telnyx_api.py link-agent <mission_id> <run_id> <telnyx_agent_id>
python scripts/telnyx_api.py list-linked-agents <mission_id> <run_id>
python scripts/telnyx_api.py unlink-agent <mission_id> <run_id> <telnyx_agent_id>

# State Management
python scripts/telnyx_api.py list-state
python scripts/telnyx_api.py get-state <slug>
python scripts/telnyx_api.py remove-state <slug>

# Memory
python scripts/telnyx_api.py save-memory <slug> <key> <value_json>
python scripts/telnyx_api.py get-memory <slug> [key]
python scripts/telnyx_api.py append-memory <slug> <key> <item_json>

# High-Level Workflows
python scripts/telnyx_api.py init <name> <instructions> <request> [steps_json]
python scripts/telnyx_api.py setup-agent <slug> <name> <instructions> <greeting>
python scripts/telnyx_api.py complete <slug> <mission_id> <run_id> <summary> [payload_json]
```

---

# 完整示例：带有定时检查的短信任务

以下是一个包含完整生命周期跟踪和基于定时检查的短信任务的示例流程：

```bash
# 1. Init mission
python scripts/telnyx_api.py init "SMS Test 003" \
  "Send a test SMS to +13322200013" \
  "SMS test with full tracking" \
  '[{"step_id": "setup", "description": "Create SMS agent", "sequence": 1},
    {"step_id": "sms", "description": "Schedule SMS", "sequence": 2},
    {"step_id": "verify", "description": "Verify delivery", "sequence": 3}]'
# Save: mission_id, run_id

# 2. Step 1: Setup agent
python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID setup in_progress
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_started "Starting: Create SMS agent" setup

python scripts/telnyx_api.py setup-agent "sms-test-003" "SMS Agent" "Send test messages" "Test from bot"
# Save: assistant_id, phone_number

python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID setup completed
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_completed "Completed: Created assistant $ASSISTANT_ID" setup

# 3. Step 2: Schedule SMS
python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID sms in_progress
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_started "Starting: Schedule SMS" sms

python scripts/telnyx_api.py schedule-sms $ASSISTANT_ID "+13322200013" "$PHONE" "2026-02-19T18:43:00Z" \
  "What do you call a bear with no teeth? A gummy bear!" \
  $MISSION_ID $RUN_ID sms
# Save: event_id

python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID sms completed
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_completed "Completed: SMS scheduled" sms

# 4. Step 3: Verify delivery — CREATE A CRON JOB TO POLL
python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID verify in_progress
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_started "Starting: Poll for delivery" verify

# >>> Create a cron job that fires AFTER the scheduled time <<<
# >>> Cron runs: get-event $ASSISTANT_ID $EVENT_ID <<<
# >>> On completed: update-step verify completed, log-event, update-run succeeded, DELETE CRON <<<
# >>> On failed: update-step verify failed, log-event, update-run failed, DELETE CRON <<<
# >>> On pending/in_progress: do nothing, cron fires again next interval <<<

# 5. (Cron fires, detects completion)
python scripts/telnyx_api.py update-step $MISSION_ID $RUN_ID verify completed
python scripts/telnyx_api.py log-event $MISSION_ID $RUN_ID step_completed "Completed: SMS delivered" verify
python scripts/telnyx_api.py update-run $MISSION_ID $RUN_ID succeeded
# DELETE the polling cron job!
```

---

# 任务分类

并非所有任务都相同。在规划任务之前，请先确定任务的类型。

```
Does call N depend on results of call N-1?
  YES -> Is it negotiation (leveraging previous results)?
    YES -> Class 3: Sequential Negotiation
    NO  -> Does it have distinct rounds with human approval?
      YES -> Class 4: Multi-Round / Follow-up
      NO  -> Class 5: Information Gathering -> Action
  NO  -> Do you need structured scoring/ranking?
    YES -> Class 2: Parallel Screening with Rubric
    NO  -> Class 1: Parallel Sweep
```

## 类别 1：并行扫雷
同时向多个目标发起通话。将所有通话安排在同一批次中（间隔 1–2 分钟）。所有通话完成后进行统一分析。

## 类别 2：带评分标准的并行筛选
同时向多个目标发起通话，并根据预设的标准进行评分。结果会在所有通话完成后进行排序。

## 类别 3：顺序协商
通话必须依次进行。每个通话的策略取决于之前的结果。在通话之间使用 `update-assistant` 命令来传递上下文。**切勿并行处理这些任务**。

## 类别 4：多轮/跟进
包含两个或更多阶段。第一轮是广泛推广，第二轮针对特定目标。

## 类别 5：信息收集 -> 行动
先通过通话获取信息，然后再采取行动。如果达到目标，则立即终止剩余的通话。

---

# 操作指南

## 默认工具

`send_dtmf` 工具已包含在系统中。大多数外出通话都会首先通过 IVR 进行。

## IVR 指导
即使是在与企业通话时，也请指示助手按 0 键或说“representative”。

## 通话限制和流量控制

将通话分批进行，每批 5–10 次，每次通话之间间隔 1–2 分钟，并监控 429 错误。

## 应答机器检测 (AMD)
- **对于人工接听**：启用此功能（让电话转接语音信箱或跳过自动应答系统）
- **对于 IVR 系统或具有电话分机的企业**：将操作设置为 `continue_assistant`

## 检查结果：使用定时任务
安排通话后，设置定时任务来定期检查结果。不要阻塞主会话。

## 重试策略

根据接收方的类型来调整重试策略：
- **自动系统**：3–15 分钟后重试，最多尝试 3 次
- **服务行业**：30 分钟至 2 小时后重试，避开高峰时段
- **专业机构**：次个工作日再尝试，最多保留一条语音信箱留言

## 审批请求（敏感操作）

在语音通话中进行破坏性或敏感操作之前，必须先获取用户批准：

```bash
./scripts/approval.sh request "Delete GitHub repo myproject"
./scripts/approval.sh request "Send $500 to John" --biometric
./scripts/approval.sh request "Post tweet about X" --details "Full text: ..."
```

**何时请求批准：**
- 删除仓库、文件或数据
- 发送资金或进行购买
- 在社交媒体上发布内容
- 向他人发送电子邮件/短信
- 任何不可逆的操作

**响应结果：**
- `approved` → 执行操作，并确认完成
- `denied` → 告诉用户“好的，我不会执行该操作”
- `timeout` → “我没有收到回复，还需要再试吗？”
- `no_devices` → 跳过审批，不执行该操作（该设备不支持电话）

**语音通话中的示例流程：**
1. 用户：“删除我 GitHub 上的测试仓库”
2. 您：“需要您的批准。请查看您的电话。”
3. 运行：`approval.sh request "Delete GitHub repo test-repo"`
4. 如果获得批准：删除仓库，然后说“已完成，测试仓库已被删除”
5. 如果拒绝：“明白了，我不会删除它”

## 网关要求

语音通话通过 `sessions_send` 将请求路由到主代理。默认情况下，此工具在网关的 HTTP 工具 API 中是被禁止的。您必须明确允许其使用：

```json5
// In openclaw.json → gateway.tools
{
  "gateway": {
    "tools": {
      "allow": ["sessions_send"]
    }
  }
}
```

或者通过命令行接口：`openclaw config patch '{"gateway":{"tools":{"allow":["sessions_send"]}}'`

如果不允许使用此功能，语音通话可以连接，但助手将无法处理任何请求（使用此工具的深度调用会返回 404 错误）。

> ⚠️ **警告：** 此设置必须放在 `gateway.tools.allow` 下，而不能放在顶级的 `tools.allow` 下。顶级的 `tools.allow` 是用于管理助手可使用的工具列表——如果将其放在那里，将会限制助手只能使用该工具，导致其他功能无法使用。如果意外设置了错误的配置，请删除顶级的 `tools.allow` 项并重新启动系统。

## ❌ 常见错误及解决方法

| 错误 | 表现症状 | 解决方法 |
|---------|---------|-----|
| `init` 和 `setup-agent` 使用的 slug 不同** | 预定的事件不会显示在用户界面上 | 在执行 `init` 后运行 `list-state`，并复制 slug |
| 操作后忘记保存数据** | 用户界面没有任何显示 | 每次操作后立即保存数据 |
| 步骤状态更改后未检查任务状态** | 任务状态一直显示为“进行中” | 在每个步骤后运行决策树逻辑 |
| 定时任务持续运行** | 资源浪费，导致不必要的检查 | 任务结束后立即删除相应的定时任务 |
| 在执行 `setup-agent` 后未检查助手关联情况** | 助手未关联，事件无法显示 | 必须始终检查并使用 `link-agent` 命令进行关联 |

## 配置

编辑 `skill-config.json` 文件：

| 选项 | 说明 |
|--------|-------------|
| `api_key` | 来自 clawdtalk.com 的 API 密钥 |
| `server` | 服务器地址（默认：`https://clawdtalk.com`） |
| `owner_name` | 您的名字（从 USER.md 自动检测） |
| `agent_name` | 助手的名字（从 IDENTITY.md 自动检测） |
| `greeting` | 来电时的自定义问候语 |

Python 任务 API 的环境变量：
- `CLAWDTALK_API_KEY` — 您的 ClawdTalk API 密钥（任务所需）
- `CLAWDTALK_API_URL` — 可覆盖默认的 API 端点（默认：`https://clawdtalk.com/v1`）

## 故障排除

- **授权失败**：在 clawdtalk.com 重新生成 API 密钥
- **网关令牌/端口更改**：重新运行 `./setup.sh` 以使用新的配置更新 `skill-config.json`
- **响应为空**：运行 `./setup.sh` 并重启网关
- **响应缓慢**：尝试在网关配置中更换更快的模型
- **调试模式**：`DEBUG=1 ./scripts/connect.sh restart`
- **任务 API 密钥**：运行 `python scripts/telnyx_api.py check-key` 来验证配置
- **JSON 解析错误**：在 JSON 参数周围使用单引号