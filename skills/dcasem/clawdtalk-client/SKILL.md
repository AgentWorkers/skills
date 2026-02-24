---
name: clawdtalk-client
version: 2.0.0
description: >
  **ClawdTalk** — 专为 **Clawdbot** 设计的语音通话、短信发送及人工智能任务处理功能  
  ClawdTalk 是一款专为 **Clawdbot** 开发的集成工具，它提供了便捷的语音通话、短信发送以及人工智能任务执行功能。通过 **ClawdTalk**，用户可以轻松地与 **Clawdbot** 进行实时语音交流，发送短信指令，并执行各种基于人工智能的任务。该工具与 **Clawdbot** 的其他核心组件（如 **OpenClaw** 和 **ClawHub**）无缝集成，确保了系统的高效性和稳定性。
metadata: {"clawdbot":{"emoji":"📞","primaryEnv":"CLAWDTALK_API_KEY","homepage":"https://github.com/team-telnyx/clawdtalk-client","requires":{"env":["CLAWDTALK_API_KEY"],"bins":["bash","node","jq","python3"],"config":["skill-config.json","~/.openclaw/openclaw.json","~/.clawdbot/clawdbot.json"]}}}
---
# ClawdTalk

ClawdTalk支持语音通话、短信发送以及基于人工智能的自动化任务执行。您可以通过电话联系机器人，发送短信，或运行多步骤的自动化推广活动——所有这些功能都由ClawdTalk提供支持。

> **注意事项：** 使用此功能时，语音记录、短信内容以及任务相关数据将会被发送到clawdtalk.com（由Telnix平台托管）。只有在您信任该平台能够安全处理您的对话数据的情况下，才建议安装此功能。

## 外部接口

| 接口地址 | 使用工具 | 发送的数据 |
|----------|---------|-----------|
| `https://clawdtalk.com` (WebSocket) | `ws-client.js` | 语音记录、任务结果、对话状态 |
| `https://clawdtalk.com/v1/*` | `telnyx_api.py` | 任务状态、事件信息、预定的通话/短信信息、助手配置 |
| `http://127.0.0.1:<port>` | `ws-client.js` | 转录的语音内容（仅限本地使用） |
| `https://raw.githubusercontent.com/team-telnyx/clawdtalk-client/...` | `update.sh` | 无数据（仅用于下载） |

## 安全性与隐私保护

- 语音记录和短信内容会传输至clawdtalk.com。
- 任务状态和事件信息会存储在服务器端，以便进行追踪和分析。
- `setup.sh`脚本会读取代理配置以获取连接详细信息；确认配置无误后，会将语音代理添加到`gateway.tools.allow`列表中。
- API密钥存储在`skill-config.json`文件中；建议使用环境变量`CLAWDTALK_API_KEY`或`${CLAWDTALK_API_KEY}`来避免明文存储。

---

# ⚠️ 重要提示：任务标识符的一致性

`init`命令会自动生成一个任务标识符（使用小写字母，空格替换为连字符）。**所有需要使用该标识符的命令（如`setup-agent`、`save-memory`、`complete`）都必须使用完全相同的标识符**。**

如果标识符不一致，可能会导致代理无法被正确关联，从而使得预定的任务事件在用户界面中显示不出来。

```bash
# After init, ALWAYS confirm the slug:
python scripts/telnyx_api.py list-state
# Output: find-window-washing-contractors: Find window washing contractors [running]
#         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ COPY-PASTE THIS. NEVER ABBREVIATE.
```

---

# ⚠️ 重要提示：您负责管理任务的全生命周期

**服务器不会自动更新任务步骤或状态**。作为任务的执行者，您需要手动完成这些操作：  
- 更新任务步骤（将步骤状态从“进行中”更改为“已完成”或“失败”）；  
- 记录重要操作；  
- 检查预定的通话或短信是否已经完成；  
- 最后，将任务状态更新为“成功”或“失败”。

## 您的责任

对于每个任务，您必须：  
1. 更新任务步骤；  
2. 记录关键操作；  
3. 监控任务是否完成；  
4. 完成任务；  
5. 在任务结束后，清除相关的定时任务。

用户界面会实时显示您的操作结果。如果您不进行任何更新，界面上就不会显示任何变化。

---

# 🚨 强制性要求：每次操作后都必须保存数据

**每次完成重要操作后，都必须立即使用`save-memory`或`append-memory`命令保存数据**。前端会从服务器内存中读取数据。如果不保存数据，这些操作将不会显示在界面上。仅使用`log-event`命令是不够的。

> **规则：** 无论何时执行了操作，都必须立即保存数据。切勿拖延。

**示例：**（调度短信发送）

**跳过步骤2是导致“界面无显示”问题的主要原因。**

---

# 🚨 强制性要求：每次操作后都必须检查任务状态

**无论任务是否完成，都必须检查任务状态**。切勿让任务长时间处于“进行中”状态。

**决策流程（每个步骤执行后都需要执行）：**

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

**如果任务实际上已经完成，但界面仍显示为“进行中”，那就是一个错误。用户会误以为任务仍在继续执行。**

---

# 架构概述

## 各组件之间的协作方式

- `telnyx_api.py`：一个Python命令行脚本，所有操作都会通过这个脚本与ClawdTalk服务器进行交互，而非直接与Telnix服务器通信。  
- **ClawdTalk服务器**：基于Node.js的后端服务，负责存储任务信息、助手配置以及事件数据，并将请求代理转发给Telnix API。  
- **Telnix API**：云服务，负责在预定时间实际发起通话和发送短信。

## 关键文件

| 文件名 | 用途 |
|---|---|
| `scripts/telnyx_api.py` | 用于所有任务/助手/事件操作的命令行工具 |
| `scripts/connect.sh` | 用于处理来电路由的WebSocket客户端 |
| `skill-config.json` | 存储API密钥和服务器地址 |
| `.missions_state.json` | 用于记录活跃任务的状态信息 |
| `.connect.log` | 用于记录WebSocket连接日志 |

## 实体ID的两种表示方式

每个实体在系统中都有两种ID：  
- **本地ID**：由ClawdTalk服务器生成（例如`3df24dde-...`）；  
- **Telnix ID**：由Telnix API内部使用。  
脚本始终使用本地ID进行操作，无需关注Telnix ID。

## 快速入门步骤：  
1. 在[clawdtalk.com](https://clawdtalk.com)注册；  
2. 在设置中添加您的电话号码；  
3. 从控制面板获取API密钥；  
4. 运行`setup.sh`脚本：该脚本会读取代理配置，将语音代理添加到`agents.list`列表中，并（在确认后）将`sessions_send`添加到`gateway.tools.allow`列表中。代理配置文件位于`~/.openclaw/openclaw.json`或`~/.clawdbot/clawdbot.json`；  
5. 运行`./scripts/connect.sh start`以建立连接。

## 语音通话

WebSocket客户端会将通话请求路由到您的代理会话，从而允许代理访问所有内存、工具和上下文信息。

```bash
./scripts/connect.sh start     # Start connection
./scripts/connect.sh stop      # Stop
./scripts/connect.sh status    # Check status
```

### 外拨通话

您可以安排机器人拨打您的电话或他人的电话：

```bash
./scripts/call.sh                              # Call your phone
./scripts/call.sh "Hey, what's up?"            # Call with greeting
./scripts/call.sh --to +15551234567            # Call external number*
./scripts/call.sh --to +15551234567 "Hello!"   # External with greeting
./scripts/call.sh status <call_id>             # Check call status
./scripts/call.sh end <call_id>                # End call
```

* 外拨通话需要订阅付费服务，并使用专用电话号码。在拨打外部号码时，AI会以隐私模式运行，不会泄露您的私人信息。*

## 短信发送与接收

```bash
./scripts/sms.sh send +15551234567 "Hello!"
./scripts/sms.sh list
./scripts/sms.sh conversations
```

## 基于Python的AI任务

对于需要复杂多步骤处理、状态跟踪、重试机制以及对话分析的任务，建议使用基于Python的API。  
**系统要求：** Python 3.7及以上版本；需要设置环境变量`CLAWDTALK_API_KEY`。可选地，您可以通过`CLAWDTALK_API_URL`覆盖默认的API地址（默认为`https://clawdtalk.com/v1`）。

```bash
python scripts/telnyx_api.py check-key    # Verify setup
```

# 重要提示：频繁保存任务状态

**每次完成重要操作后，都必须保存进度数据**。如果会话崩溃或重启，未保存的数据将会丢失。

## 数据持久化策略（双层存储）：  
数据需要同时保存在本地内存（`.missions_state.json`）和云端（通过事件API）中，以确保数据的安全性和持久性。

## 何时需要保存数据（每次操作后）：  
| 操作类型 | 保存方式 | 记录操作类型 |
|--------|-------------|-----------|
| 网页搜索结果返回 | 使用`append-memory` | 使用`log-event`（tool_call） |
| 找到承包商/潜在客户 | 使用`append-memory` | 使用`log-event`（custom） |
| 创建助手 | 使用`save-memory` | 使用`log-event`（custom） |
| 分配电话号码 | 使用`save-memory` | 使用`log-event`（custom） |
| 预定通话/短信 | 使用`append-memory` | 使用`log-event`（custom） |
| 通话完成 | 使用`save-memory` | 使用`log-event`（custom） |
| 获得报价/洞察 | 使用`save-memory` | 使用`log-event`（custom） |
| 做出决策 | 使用`save-memory` | 使用`log-event`（message） |
| 步骤开始 | 使用`save-memory` | 使用`update-step`（in_progress） + `log-event`（step_started） |
| 步骤完成 | 使用`save-memory` | 使用`update-step`（completed） + `log-event`（step_completed） |
| 步骤失败 | 使用`save-memory` | 使用`update-step`（failed） + `log-event`（error） |
| 发生错误 | 使用`save-memory` | 使用`log-event`（error） |

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

## 事件记录（云端备份）  

```bash
# Log an event (step_id is REQUIRED - links event to a plan step)
python scripts/telnyx_api.py log-event <mission_id> <run_id> <type> "<summary>" <step_id> '[payload_json]'

# Event types: tool_call, custom, message, error, step_started, step_completed
# step_id: Use the step_id from your plan (e.g., "research", "setup", "calls")
#          Use "-" if event doesn't belong to a specific step
```

---

## 任务使用说明

此功能有两种模式：  
- **完整任务**（包含多步骤和详细跟踪）；  
- **简单通话**（一次性操作，无需额外任务管理）。根据任务需求选择合适的模式。

### 何时使用完整任务模式：  
- 当任务涉及多次通话或短信发送时；  
- 需要完整的事件记录、计划跟踪和状态管理；  
- 任务包含多个步骤且需要逐步执行；  
- 需要记录重试情况和失败结果；  
- 需要比较多次通话的结果。

**示例：**  
- “在芝加哥寻找窗户清洗承包商并联系他们协商价格”；  
- “联系列表中的所有潜在客户并安排演示会议”；  
- “拨打10个气象站的电话，找出温度最高的那个”。

### 何时不使用任务模式：  
- 当任务仅涉及一次外拨通话时（只需创建一个助手并直接安排通话）；  
- 当任务是一次性短信发送时；  
- 任务不需要跟踪、计划或状态管理；  
- 如果任务只需执行一个步骤和一次通话，则无需使用任务模式。

**对于简单通话，只需执行以下步骤：**  
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

**省略步骤2是导致界面无显示问题的主要原因。**

---

## 状态管理

脚本会自动更新`.missions_state.json`文件中的任务状态。这样即使在系统重启后，数据也能保持完整。

---

# 核心工作流程

## 第1阶段：初始化任务跟踪  

### 步骤1.1：创建任务  

```bash
python scripts/telnyx_api.py create-mission "Brief descriptive name" "Full description of the task"
```  
**保存返回的`mission_id`——后续操作都需要这个ID。**

### 步骤1.2：启动任务执行  

```bash
python scripts/telnyx_api.py create-run <mission_id> '{"original_request": "The exact user request", "context": "Any relevant context"}'
```  
**保存返回的`run_id`。**

### 步骤1.3：制定计划  

在执行任务之前，先制定详细的计划。  

```bash
python scripts/telnyx_api.py create-plan <mission_id> <run_id> '[
  {"step_id": "step_1", "description": "Research contractors online", "sequence": 1},
  {"step_id": "step_2", "description": "Create voice agent for calls", "sequence": 2},
  {"step_id": "step_3", "description": "Schedule calls to each contractor", "sequence": 3},
  {"step_id": "step_4", "description": "Monitor call completions", "sequence": 4},
  {"step_id": "step_5", "description": "Analyze results and select best options", "sequence": 5}
]'
```  

### 步骤1.4：将任务状态设置为“进行中”  

```bash
python scripts/telnyx_api.py update-run <mission_id> <run_id> running
```  

### 高效替代方案：一次性完成所有设置  

可以使用`init`命令一次性完成任务的创建、执行、计划状态设置：

```bash
python scripts/telnyx_api.py init "Find window washing contractors" "Find contractors in Chicago, call them, negotiate rates" "User wants window washing quotes" '[
  {"step_id": "research", "description": "Find contractors online", "sequence": 1},
  {"step_id": "setup", "description": "Create voice agent", "sequence": 2},
  {"step_id": "calls", "description": "Schedule and make calls", "sequence": 3},
  {"step_id": "analyze", "description": "Analyze results", "sequence": 4}
]'
```  
如果已经存在同名任务，该命令会自动恢复任务状态。  
**⚠️ 在执行`init`命令后，立即运行`list-state`命令并复制返回的标识符。后续所有操作都必须使用这个标识符。**

---

## 第2阶段：配置语音/短信助手  

当任务需要发起通话或发送短信时，首先需要创建一个AI助手。  

### 步骤2.1：创建语音/短信助手  

**对于电话通话：**  
```bash
python scripts/telnyx_api.py create-assistant "Contractor Outreach Agent" "You are calling on behalf of [COMPANY]. Your goal is to [SPECIFIC GOAL]. Be professional and concise. Collect: [WHAT TO COLLECT]. If they cannot talk now, ask for a good callback time." "Hi, this is an AI assistant calling on behalf of [COMPANY]. Is this [BUSINESS NAME]? I am calling to inquire about your services. Do you have a moment?" '["telephony", "messaging"]'
```  

**对于短信发送：**  
```bash
python scripts/telnyx_api.py create-assistant "SMS Outreach Agent" "You send SMS messages to collect information. Keep messages brief and professional." "Hi! I am reaching out on behalf of [COMPANY] regarding [PURPOSE]. Could you please reply with [REQUESTED INFO]?" '["telephony", "messaging"]'
```  
**保存返回的`assistant_id`。**

### 步骤2.2：查找并分配电话号码  

```bash
python scripts/telnyx_api.py get-available-phone                          # Get first available
python scripts/telnyx_api.py get-connection-id <assistant_id> telephony   # Get connection ID
python scripts/telnyx_api.py assign-phone <phone_number_id> <connection_id> voice  # Assign
```  

### 高效替代方案：一次性完成所有设置  

**该命令会自动创建助手，将其关联到任务，分配电话号码，并将所有相关信息保存到状态文件中。**  
**⚠️ 确保使用的标识符与`init`命令生成的标识符一致。否则，助手将无法被正确关联，预定的任务事件将不会显示在用户界面中。**  
**执行关联操作后立即验证结果：**  
```bash
python scripts/telnyx_api.py list-linked-agents <mission_id> <run_id>
# Must show your assistant_id. If empty → slug was wrong. Fix with:
python scripts/telnyx_api.py link-agent <mission_id> <run_id> <assistant_id>
```  

### 步骤2.3：将助手关联到任务执行中  

**如果使用`setup-agent`命令，关联操作会自动完成。**  
**如果需要手动配置：**  
```bash
python scripts/telnyx_api.py link-agent <mission_id> <run_id> <assistant_id>
python scripts/telnyx_api.py list-linked-agents <mission_id> <run_id>
python scripts/telnyx_api.py unlink-agent <mission_id> <run_id> <assistant_id>
```  

---

## 第3阶段：安排通话/短信  

### 注意工作时间  

**重要提示：** 在安排通话时，请考虑当地的工作时间（上午9点至下午5点）。`scheduled_at`时间必须在未来（至少1分钟后）。  

```bash
python scripts/telnyx_api.py schedule-call <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" <mission_id> <run_id>
python scripts/telnyx_api.py schedule-sms <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" "Your message here"
```  
**保存返回的事件ID。**

---

## 第4阶段：监控通话完成情况  

### ⚠️ 这是最关键的部分  

安排通话或短信后，**Telnix系统会自动在预定时间执行任务**。您需要通过轮询来确认任务是否完成，并相应地更新任务状态。  

### 检查预定事件的状态  

```bash
python scripts/telnyx_api.py get-event <assistant_id> <event_id>
```  

### 使用定时任务进行轮询  

请使用机器人的定时任务系统来执行轮询。**不要阻塞主会话的运行。** 根据预计完成时间设置轮询间隔：  

| 预计完成时间 | 轮询间隔 | 示例 |
|---|---|---|
| 小于5分钟 | 每30秒 | 立即发送短信 |
| 5–30分钟 | 每2–5分钟 | 15分钟后拨打电话 |
| 1–24小时 | 每15–30分钟 | 今晚拨打电话 |
| 多天/多周 | 每4–8小时 | 下周拨打电话 |

**如果已知确切的预定时间，请在预定时间之后再开始轮询。** 首次轮询应在预定时间后2分钟开始。**

### 定时任务设置方法  

安排通话或短信后，需要创建一个定时任务来执行轮询：  

```
Create cron: poll at appropriate interval
  → Run get-event <assistant_id> <event_id>
  → If completed: update step, log event, complete mission if last step, DELETE THIS CRON
  → If failed: update step as failed, log error, DELETE THIS CRON
  → If pending/in_progress: do nothing, cron runs again at next interval
```  
**⚠️ 任务完成后（无论成功、失败或取消），都必须立即清除相关的定时任务。**切勿让定时任务持续运行。**

### 调整轮询间隔  

根据实际情况调整轮询间隔：  
- 如果预定时间在2周后：初始轮询间隔设为8分钟；  
- 随着预定时间的临近（1小时内），将轮询间隔缩短至5分钟；  
- 预定时间过后：将轮询间隔缩短至30秒。  

### 事件状态的含义及相应操作：  

| 状态 | 含义 | 操作建议 |
|--------|---------|--------|
| `pending` | 等待预定时间 | 继续轮询 |
| `in_progress` | 通话或短信正在进行中 | 继续轮询 |
| `completed` | 通话成功完成 | 更新任务状态并获取详细信息 |
| `failed` | 重试失败 | 将任务状态更新为“失败”，并考虑是否需要重试 |

### 通话状态（仅适用于电话通话）  

| 状态 | 含义 | 操作建议 |
|-------------|---------|--------|
| `ringing` | 电话正在响铃 | 1–2分钟后再次尝试 |
| `in_progress` | 通话正在进行中 | 2–3分钟后再次尝试 |
| `completed` | 通话正常结束 | 获取详细信息 |
| `no-answer` | 无人接听 | 可以重试 | 10–15分钟后再次尝试 |
| `busy` | 电话占线 | 可以重试 | 10–15分钟后再次尝试 |
| `cancelled` | 通话被取消 | 查看是否为人为原因 |
| `failed` | 系统故障 | 10–15分钟后再次尝试 |

---

## 第5阶段：获取通话详细信息  

通话完成后，可以通过`conversation_id`获取通话的详细信息。**在状态变为“completed”之前，持续进行轮询**（每次轮询间隔10秒）。  

```bash
python scripts/telnyx_api.py get-insights <conversation_id>
```  
Telnix会在创建助手时自动生成默认的详细信息模板。您无需手动管理这些模板，只需读取返回的结果即可。  

---

## 第6阶段：完成任务  

```bash
python scripts/telnyx_api.py update-run <mission_id> <run_id> succeeded

# Or with full results:
python scripts/telnyx_api.py complete "find-window-washing-contractors" <mission_id> <run_id> "Summary of results" '{"key": "payload"}'
```  

---

# 事件日志记录规范  

**将所有操作都记录为事件**。务必通过`update-step`命令更新任务状态，并通过`log-event`记录相关事件。  

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

## Python命令快速参考  

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

# 完整示例：使用定时任务进行短信发送的任务  

以下是一个包含完整生命周期跟踪和基于定时任务轮询的短信发送任务的示例：  

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

## 任务类型分类  

并非所有任务都相同。在开始规划之前，请先确定任务的类型。  

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

## 任务类型1：并行处理  
同时向多个目标发起通话或发送短信（批量推广、调查等）。所有通话会分批进行，每次通话之间间隔1–2分钟。所有通话完成后会进行统一分析。  

## 任务类型2：带评分标准的并行筛选  
同时向多个目标发起通话，并根据预设的评分标准进行排序。结果会在所有通话完成后进行汇总分析。  

## 任务类型3：顺序协商  
通话必须按顺序进行。每次通话的策略取决于之前的结果。需要在通话之间使用`update-assistant`命令来传递上下文信息。**切勿并行处理这些任务。**  

## 任务类型4：多轮处理/跟进  
包含两个或更多阶段。第一轮为广泛推广，第二轮针对特定目标进行进一步沟通。  

## 任务类型5：信息收集与行动  
先通过通话获取信息，然后再根据信息采取行动。如果目标达成，则立即结束后续操作。  

## 运营指南  

**默认工具**  
`send_dtmf`工具已包含在系统中。大多数外拨通话会先通过IVR系统处理。  

**IVR使用说明**  
无论联系哪家企业，都请指示助手按0键或说出“representative”（代表）。  

**通话限制与调度**  
每次最多安排5–10个通话，通话间隔为1–2分钟，并监控是否出现429错误（电话占线错误）。  

**自动应答机处理**：  
- 对于需要人工接听的电话，启用自动应答机；  
- 对于IVR系统或具有电话分机的企业，设置自动应答机为“continue_assistant”。  

**结果查询**：  
安排通话后，使用定时任务定期查询结果。请勿阻塞主会话的运行。  

**重试策略**  
根据接收方的类型调整重试策略：  
- **自动化系统**：最多重试3次，间隔5–15分钟；  
- **服务行业**：最多重试2次，间隔30分钟，避开高峰时段；  
- **专业机构**：次个工作日再尝试，最多发送一条语音留言。  

## 需要用户授权的操作  

在涉及破坏性或敏感操作时，请先获取用户授权：  

```bash
./scripts/approval.sh request "Delete GitHub repo myproject"
./scripts/approval.sh request "Send $500 to John" --biometric
./scripts/approval.sh request "Post tweet about X" --details "Full text: ..."
```  
**何时需要授权：**  
- 删除仓库、文件或数据；  
- 发送资金或进行购买；  
- 在社交媒体上发布内容；  
- 向他人发送电子邮件或短信；  
- 任何不可逆的操作。  

**授权响应结果：**  
- `approved`：执行操作并确认完成；  
- `denied`：告知用户“不行，我不会执行该操作”；  
- `timeout`：“没有收到回复，还需要尝试吗？”；  
- `no_devices`：表示无法获取授权，无需执行操作。  

**语音通话中的示例流程：**  
1. 用户：“请删除我的GitHub测试仓库。”  
2. 您：“需要您的授权。请确认一下。”  
3. 运行`approval.sh request "Delete GitHub repo test-repo"`命令。  
4. 如果获得授权，删除仓库并回复：“删除成功。”  
5. 如果未获得授权，回复：“明白了，不会删除。”  

## 网关配置要求  

语音通话会通过`sessions_send`命令路由到代理会话。该命令在Gateway的HTTP工具配置中被默认禁止使用。您需要明确允许其使用：  

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
或者通过命令行配置：`openclaw config patch '{"gateway":{"tools":{"allow":["sessions_send"]}}'`  

如果不允许使用该命令，语音通话虽然可以连接，但代理将无法处理任何请求（否则会返回404错误）。  

> **警告：** 该配置必须添加到`gateway.tools.allow`列表中，**切勿添加到`tools.allow`列表的顶层**。`tools.allow`列表用于指定代理可使用的工具，如果将其添加到顶层，会导致代理只能使用该工具，从而影响其他功能。如果配置错误，请删除顶层配置并重新启动系统。  

## 常见问题及解决方法：  

| 错误类型 | 表现症状 | 解决方法 |  
|---------|---------|---------|  
| `init`和`setup-agent`使用的标识符不一致 | 预定任务事件在用户界面中显示不出来 | 在执行`init`命令后，复制返回的标识符并使用它。 |
| 操作后忘记保存数据 | 用户界面无显示内容 | 每次操作后立即保存数据。 |
| 任务状态更改后未检查状态 | 任务状态一直显示为“进行中” | 每次操作后都执行决策流程。 |
| 定时任务持续运行 | 资源浪费，导致轮询结果失效 | 任务完成后立即删除相关的定时任务。 |
| 在`setup-agent`命令后未检查代理关联情况 | 代理未正确关联，导致事件信息无法显示 | 执行`link-agent`命令以确认代理关联情况。 |

## 配置文件说明  

编辑`skill-config.json`文件：  

| 参数 | 说明 |  
|--------|-------------|---|
| `api_key` | 来自clawdtalk.com的API密钥 |  
| `server` | 服务器地址（默认：`https://clawdtalk.com`） |  
| `owner_name` | 用户名称（从USER.md文件自动获取） |  
| `agent_name` | 助手名称（从IDENTITY.md文件自动获取） |  
| `greeting` | 来电时的自定义问候语 |  

**Python任务API的相关环境变量：**  
- `CLAWDTALK_API_KEY`：您的ClawdTalk API密钥（必需）；  
- `CLAWDTALK_API_URL`：可选的API地址（默认：`https://clawdtalk.com/v1`）  

## 故障排除方法：**  
- **授权失败**：在clawdtalk.com重新生成API密钥；  
- **Gateway配置更改**：重新运行`./setup.sh`命令以更新`skill-config.json`文件；  
- **响应为空**：运行`./setup.sh`命令并重启Gateway；  
- **响应缓慢**：尝试在Gateway配置中更换更快的模型；  
- **调试模式**：运行`DEBUG=1 ./scripts/connect.sh restart`；  
- **任务API错误**：运行`python scripts/telnyx_api.py check-key`命令进行检查；  
- **JSON解析错误**：在JSON参数周围使用单引号。