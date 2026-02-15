---
name: telnyx-missions
description: 使用 Telnyx AI Missions API 来追踪代理的活动。在执行需要记录和追踪的多步骤任务时，请使用此功能。该 API 支持创建语音/短信代理、安排通话以及检索通话记录。适用于涉及拨打电话、发送短信或任何需要详细追踪的工作场景。
metadata: {"openclaw":{"emoji":"🎯","requires":{"bins":["python3"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx AI Missions

使用Telnix AI Missions API跟踪多步骤代理活动。创建语音/SMS助手，安排通话，并检索对话洞察。

## 设置

Python脚本`telnyx_api.py`处理所有API调用：

```bash
# Set your API key
export TELNYX_API_KEY="your_key_here"

# Run commands using the script
python3 {baseDir}/scripts/telnyx_api.py <command> [args...]

# Or create an alias for convenience
alias missions="python3 {baseDir}/scripts/telnyx_api.py"
```

**注意：**本文档中的所有命令示例都使用`python telnyx_api.py`来简化表示。请将其替换为完整路径`python3 {baseDir}/scripts/telnyx_api.py`，或使用上述别名。

---

此技能使您能够使用Telnix AI Missions API跟踪您的工作，包括通过AI助手拨打电话和发送短信。

---

# ⚠️ 重要提示：频繁保存状态 ⚠️

**您必须在每个重要操作后保存进度。** 如果会话崩溃或重新启动，未保存的工作将会丢失。

## 双层持久化：内存 + 事件

始终保存到以下两个地方：
1. **本地内存**（`.missions_state.json`）- 快速，可恢复重启
2. **事件API**（云端）- 永久审计追踪，可恢复本地文件丢失

## 何时保存（每次操作后！）
| 操作 | 保存内存 | 记录事件 |
|--------|-------------|-----------|
| 网页搜索返回结果 | ✅ append-memory | ✅ log-event (tool_call) |
| 找到承包商/潜在客户 | ✅ append-memory | ✅ log-event (custom) |
| 创建助手 | ✅ save-memory | ✅ log-event (custom) |
| 分配电话号码 | ✅ save-memory | ✅ log-event (custom) |
| 安排通话/SMS | ✅ append-memory | ✅ log-event (custom) |
| 通话完成 | ✅ save-memory | ✅ log-event (custom) |
| 获得报价/洞察 | ✅ save-memory | ✅ log-event (custom) |
| 做出决定 | ✅ save-memory | ✅ log-event (message) |
| 步骤开始 | ✅ save-memory | ✅ update-step (in_progress) + log-event (step_started) |
| 步骤完成 | ✅ save-memory | ✅ update-step (completed) | log-event (step_completed) |
| 步骤失败 | ✅ save-memory | ✅ update-step (failed) | log-event (error) |
| 发生错误 | ✅ save-memory | ✅ log-event (error) |

## 内存命令（本地备份）

```bash
# Save a single value
python telnyx_api.py save-memory "<slug>" "key" '{"data": "value"}'

# Append to a list (great for collecting multiple items)
python telnyx_api.py append-memory "<slug>" "contractors" '{"name": "ABC Co", "phone": "+1234567890"}'

# Retrieve memory
python telnyx_api.py get-memory "<slug>"           # Get all memory
python telnyx_api.py get-memory "<slug>" "key"     # Get specific key
```

## 事件命令（云端备份）

```bash
# Log an event (step_id is REQUIRED - links event to a plan step)
python telnyx_api.py log-event <mission_id> <run_id> <type> "<summary>" <step_id> '[payload_json]'

# Event types: tool_call, custom, message, error, step_started, step_completed
# step_id: Use the step_id from your plan (e.g., "research", "setup", "calls")
#          Use "-" if event doesn't belong to a specific step
```

## 示例：完整的保存模式

通过网页搜索找到承包商后，执行以下两个操作：

```bash
# 1. Save to local memory (fast recovery)
python telnyx_api.py append-memory "find-window-washers" "contractors_found" '{"name": "ABC Cleaning", "phone": "+13125551234", "source": "google search"}'

# 2. Log to events API with step_id (permanent cloud record linked to plan step)
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Found contractor: ABC Cleaning +13125551234" "research" '{"contractor": "ABC Cleaning", "phone": "+13125551234", "source": "google search"}'
```

安排通话后：

```bash
# 1. Local memory
python telnyx_api.py append-memory "find-window-washers" "calls_scheduled" '{"event_id": "evt_123", "contractor": "ABC Cleaning", "time": "2024-12-01T15:00:00Z"}'

# 2. Cloud event with step_id
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Scheduled call to ABC Cleaning for 3:00 PM" "calls" '{"scheduled_event_id": "evt_123", "contractor": "ABC Cleaning", "scheduled_for": "2024-12-01T15:00:00Z"}'
```

从通话中获取报价后：

```bash
# 1. Local memory
python telnyx_api.py save-memory "find-window-washers" "quotes" '{"ABC Cleaning": {"amount": 350, "available": "next week"}}'

# 2. Cloud event with step_id
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Call completed: ABC Cleaning quoted $350" "calls" '{"contractor": "ABC Cleaning", "quote": 350, "availability": "next week", "conversation_id": "conv_xyz"}'
```

## 最佳实践

1. **立即保存** - 不要等待，不要批量保存
2. **保存到两个地方** - 内存（本地）和事件（云端）
3. **详细记录** - 保存的数据越多，恢复越容易
4. **包含上下文** - 时间戳、来源、ID
5. **保存部分结果** - 有总比没有好
6. **在高风险操作前保存** - 在进行长时间API调用或等待之前

---

## 何时使用此技能

此技能有两种模式：**完整任务**（跟踪的、多步骤的）和**简单通话**（一次性的，无需任务开销）。选择合适的一种。

### 在以下情况下使用完整任务：
- 任务涉及**多次通话或短信**（批量外联、调查、扫雷）
- 需要包含事件、计划和状态跟踪的**完整审计追踪**
- 任务是**多步骤的**，并且需要在多个阶段付出大量努力
- **需要跟踪重试和失败情况**
- 需要**比较多次通话的结果**

示例：
- “在芝加哥找到擦窗承包商，给他们打电话并协商价格”
- “联系此列表中的所有潜在客户并安排演示”
- “拨打10个气象站的电话，找出温度最高的”

### 不要在以下情况下使用任务：
- 任务是**单次外拨电话** — 只需要创建一个助手（或重用一个）并直接安排通话
- 是**一次性短信** — 安排好即可
- 任务不需要跟踪、计划或状态恢复
- 如果您只为一个步骤和一次通话创建任务 — 那就是过度设计了

**对于简单通话，只需：**
```bash
# Reuse or create an assistant
python telnyx_api.py list-assistants --name=<relevant>
# Schedule the call
python telnyx_api.py schedule-call <assistant_id> <to> <from> <datetime> <mission_id> <run_id>
# Poll for completion
python telnyx_api.py get-event <assistant_id> <event_id>
# Get insights
python telnyx_api.py get-insights <conversation_id>
```

没有任务，就不需要运行，也不需要计划。保持简单。

## 所需设置

Python脚本`telnyx_api.py`处理所有API调用。请确保`TELNYX_API_KEY`环境变量已设置：

```bash
python telnyx_api.py check-key
```

# 状态持久化

脚本自动在`.missions_state.json`中管理状态。这可以在重启后保留，并支持多个并发任务。

## 状态命令

```bash
# List all active missions
python telnyx_api.py list-state

# Get state for a specific mission
python telnyx_api.py get-state "find-window-washing-contractors"

# Remove a mission from state
python telnyx_api.py remove-state "find-window-washing-contractors"
```

---

# 核心工作流程

## 第1阶段：初始化跟踪

### 步骤1.1：创建任务

```bash
python telnyx_api.py create-mission "Brief descriptive name" "Full description of the task"
```

**保存返回的`mission_id`** - 您将在后续所有通话中需要它。

### 步骤1.2：开始运行

```bash
python telnyx_api.py create-run <mission_id> '{"original_request": "The exact user request", "context": "Any relevant context"}'
```

**保存返回的`run_id`**。

### 步骤1.3：创建计划

在执行之前，概述您的计划：

```bash
python telnyx_api.py create-plan <mission_id> <run_id> '[
  {"step_id": "step_1", "description": "Research contractors online", "sequence": 1},
  {"step_id": "step_2", "description": "Create voice agent for calls", "sequence": 2},
  {"step_id": "step_3", "description": "Schedule calls to each contractor", "sequence": 3},
  {"step_id": "step_4", "description": "Monitor call completions", "sequence": 4},
  {"step_id": "step_5", "description": "Analyze results and select best options", "sequence": 5}
]'
```

### 步骤1.4：将运行设置为进行中

```bash
python telnyx_api.py update-run <mission_id> <run_id> running
```

### 高级替代方案：一次性初始化所有内容

使用`init`命令一步创建任务、运行、计划并设置状态：

```bash
python telnyx_api.py init "Find window washing contractors" "Find contractors in Chicago, call them, negotiate rates" "User wants window washing quotes" '[
  {"step_id": "research", "description": "Find contractors online", "sequence": 1},
  {"step_id": "setup", "description": "Create voice agent", "sequence": 2},
  {"step_id": "calls", "description": "Schedule and make calls", "sequence": 3},
  {"step_id": "analyze", "description": "Analyze results", "sequence": 4}
]'
```

如果已经存在同名任务，这也会自动恢复。

---

## 第2阶段：语音/SMS代理设置

当您的任务需要拨打电话或发送短信时，首先创建一个AI助手。

### 步骤2.1：创建语音/SMS助手

**对于电话通话：**
```bash
python telnyx_api.py create-assistant "Contractor Outreach Agent" "You are calling on behalf of [COMPANY]. Your goal is to [SPECIFIC GOAL]. Be professional and concise. Collect: [WHAT TO COLLECT]. If they cannot talk now, ask for a good callback time." "Hi, this is an AI assistant calling on behalf of [COMPANY]. Is this [BUSINESS NAME]? I am calling to inquire about your services. Do you have a moment?" '["telephony"]'
```

**对于短信：**
```bash
python telnyx_api.py create-assistant "SMS Outreach Agent" "You send SMS messages to collect information. Keep messages brief and professional." "Hi! I am reaching out on behalf of [COMPANY] regarding [PURPOSE]. Could you please reply with [REQUESTED INFO]?" '["messaging"]'
```

**保存返回的`assistant_id`**。

### 步骤2.2：查找并分配电话号码

#### 2.2.1：列出可用电话号码

```bash
python telnyx_api.py list-phones --available
```

或者直接获取第一个可用的号码：

```bash
python telnyx_api.py get-available-phone
```

**如果没有可用电话号码，请停止并通知用户：**
> “未找到可用电话号码。您需要从Telnyx（https://portal.telnyx.com）购买电话号码才能进行通话。”

#### 2.2.2：获取助手的连接ID**

```bash
# For voice calls
python telnyx_api.py get-connection-id <assistant_id> telephony

# For SMS
python telnyx_api.py get-connection-id <assistant_id> messaging
```

#### 2.2.3：将电话号码分配给助手

```bash
# For voice calls
python telnyx_api.py assign-phone <phone_number_id> <connection_id> voice

# For SMS
python telnyx_api.py assign-phone <phone_number_id> <connection_id> sms
```

### 高级替代方案：一步设置代理

使用`setup-agent`命令创建助手并分配电话号码：

```bash
python telnyx_api.py setup-agent "find-window-washing-contractors" "Contractor Caller" "You are calling to get quotes for commercial window washing. Ask about: rates per floor, availability, insurance. Be professional." "Hi, I am calling to inquire about your commercial window washing services. Do you have a moment to discuss rates?"
```

这会自动：
- 创建具有电话功能的助手
- **将助手与任务运行关联**（如果`mission_id`和`run_id`存在于状态中）
- 查找可用的电话号码
- 将其分配给助手
- 将所有ID保存到状态文件中

### 步骤2.3：将代理与任务运行关联

**重要提示：** 创建助手后，必须将其与任务运行关联。这允许系统跟踪哪些代理正在处理哪些任务。

**如果使用`setup-agent`命令**：当`mission_id`和`run_id`存在于状态中时，关联会自动完成。

**如果手动设置：**
```bash
python telnyx_api.py link-agent <mission_id> <run_id> <assistant_id>
```

您还可以列出和解除代理的关联：
```bash
# List all agents linked to a run
python telnyx_api.py list-linked-agents <mission_id> <run_id>

# Unlink an agent from a run
python telnyx_api.py unlink-agent <mission_id> <run_id> <assistant_id>
```

### 步骤2.4：记录设置

```bash
python telnyx_api.py log-event <mission_id> <run_id> custom "Created voice assistant and assigned phone number" "setup" '{"assistant_id": "<assistant_id>", "phone_number": "+15551234567", "type": "telephony"}'
```

---

## 第3阶段：研究与数据收集

搜索您需要的信息（承包商、潜在客户等）：

1. 如果有可用的网络搜索工具，请使用它们
2. 使用为任务提供的任何专用工具
3. 将每次搜索记录为事件，并附带`step_id`

```bash
python telnyx_api.py log-event <mission_id> <run_id> tool_call "Searching for window washing contractors in Chicago" "research" '{"tool": "WebSearch", "query": "commercial window washing contractors Chicago"}'
```

---

## 第4阶段：安排通话/SMS

### 考虑营业时间

**重要提示**：在安排通话之前，请考虑营业时间：
- 典型的营业时间：当地时间上午9点至下午5点
- 如果当前时间不在营业时间内，请安排在下一个营业日
- `scheduled_at_fixed_datetime`必须在未来（至少距离现在1分钟）

### 步骤4.1：安排电话通话

```bash
python telnyx_api.py schedule-call <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" <mission_id> <run_id>
```

**保存返回的`scheduled_event_id`**。

### 步骤4.2：安排短信

```bash
python telnyx_api.py schedule-sms <assistant_id> "+15551234567" "+15559876543" "2024-12-01T14:30:00Z" "Hi! I am reaching out on behalf of [COMPANY] to inquire about your window cleaning rates for commercial buildings. Could you share your pricing?"
```

### 步骤4.3：记录每个安排的事件

```bash
python telnyx_api.py log-event <mission_id> <run_id> custom "Scheduled call to ABC Window Cleaning for 2:30 PM" "calls" '{"scheduled_event_id": "<event_id>", "contractor": "ABC Window Cleaning", "phone": "+15551234567", "scheduled_for": "2024-12-01T14:30:00Z"}'
```

---

## 第5阶段：监控通话完成情况

在安排通话后，您需要轮询通话是否完成。

### 步骤5.1：检查安排的事件状态

```bash
python telnyx_api.py get-event <assistant_id> <scheduled_event_id>
```

### 事件状态值

事件级别的`status`跟踪整个生命周期：

| 状态 | 含义 | 操作 |
|--------|---------|--------|
| `pending` | 等待预定时间 | 等待并稍后再次检查 |
| `in_progress` | 通话/SMS正在进行中 | 几分钟后再次检查 |
| `completed` | 成功完成 | 获取`conversation_id`，获取洞察 |
| `failed` | 失败后尝试重试 | 考虑重新安排 |

### 通话状态值（仅限电话通话）

`call_status`字段提供了电话级别的结果。**这是决定下一步行动的最重要字段。**

| call_status | 含义 | 操作 |
|-------------|---------|--------|
| `ringing` | 电话正在响铃，尚未接听 | 仍然进行中 — 1-2分钟后再次尝试 |
| `in_progress` | 通话正在进行中 | 2-3分钟后再次尝试 |
| `completed` | 通话已连接并完成 | 成功 — 获取`conversation_id`，获取洞察 |
| `no-answer` | 电话响了但无人接听 | **可重试** — 在不同的时间重新安排 |
| `busy` | 线路忙 | **可重试** — 10-15分钟后再次尝试 |
| `cancelled` | 通话被取消 | 查看是否已取消；如果没有，可能需要重新安排 |
| `failed` | 通话失败（网络/系统错误） | **可重试** — 在短暂等待后（5-10分钟）再次尝试 |

### 步骤5.2：轮询策略

**何时开始轮询**：在`scheduled_at_fixed_datetime`之后几分钟

**根据`call_status`调整轮询间隔**：
- `ringing` → 1-2分钟后再次尝试（电话可能随时接通）
- `in_progress` → 2-3分钟后再次尝试（通话正在进行中）
- `pending`（事件状态） → 每5分钟轮询一次，直到预定时间过去
- `no-answer` / `busy` / `failed` → 停止轮询，立即重试
- `completed` → 完成后，继续获取洞察

### 步骤5.3：处理可重试的通话状态

当`call_status`为`no-answer`、`busy`或`failed`时，可以尝试重试：

1. 使用失败原因更新通话跟踪器
2. 检查重试次数 — 默认最多重试3次（除非用户另有指定）
3. 根据失败类型安排不同的重试时间：
   - `busy` → 10-15分钟后再次尝试（线路可能很快空闲）
   - `no-answer` → 30分钟到2小时后再次尝试（尝试不同的时间）
   - `failed` → 5-10分钟后再次尝试（尝试不同的时间）

### 步骤5.4：获取对话洞察

一旦通话完成并且您有了`conversation_id`，就获取对话洞察。

**重要提示**：始终使用洞察来获取通话摘要。**不要获取原始对话消息 — 洞察提供了对话结果的结构化摘要。**

### 步骤6.1：获取对话洞察

```bash
python telnyx_api.py get-insights <conversation_id>
```

### 步骤6.2：轮询直到洞察完成

对话洞察可能在通话结束后不会立即准备好。**您必须轮询，直到洞察状态变为“completed”。**

**轮询策略：**
- 在获取`conversation_id`后立即检查
- 如果状态不是“completed”，等待10秒后再次尝试
- 继续轮询，直到状态变为“completed”或20分钟过去
**只有在状态为“completed”时才使用洞察数据**

**示例轮询流程：**
```bash
# First attempt
python telnyx_api.py get-insights "conv_xyz"
# Output: Insight status: in_progress

# Wait 10 seconds, try again
python telnyx_api.py get-insights "conv_xyz"
# Output: Insight status: in_progress

# Wait 10 seconds, try again
python telnyx_api.py get-insights "conv_xyz"
# Output: Insight: Customer quoted $350 for a 10-story building...
```

### 步骤6.3：记录洞察

```bash
python telnyx_api.py log-event <mission_id> <run_id> custom "Call completed with ABC Window Cleaning - quoted $350" "calls" '{"conversation_id": "<conv_id>", "contractor": "ABC Window Cleaning", "outcome": "success", "quote": "$350", "availability": "next week", "notes": "Willing to negotiate for recurring contracts"}'
```

---

## 第7阶段：完成任务

### 步骤7.1：分析结果

在所有通话完成后：
1. 比较报价和结果
2. 根据标准选择最佳选项
3. 为用户准备摘要

### 步骤7.2：完成运行

```bash
python telnyx_api.py update-run <mission_id> <run_id> succeeded
```

或者使用完整结果：

```bash
python telnyx_api.py complete "find-window-washing-contractors" <mission_id> <run_id> "Contacted 5 contractors, received 4 quotes. Best options: ABC Cleaning ($350) and XYZ Windows ($380)." '{"contractors_contacted": 5, "quotes_received": 4, "recommended": [{"name": "ABC Cleaning", "quote": 350}, {"name": "XYZ Windows", "quote": 380}]}'
```

`complete`命令还会从状态文件中删除任务。

---

# 事件日志参考

**将每个操作都记录为事件，以获得完整的审计追踪。** 事件存储在云端，即使本地文件丢失也能提供永久备份。

## 重要提示：更新步骤状态（而不仅仅是事件！**

**在开始或完成每个步骤时，必须通过`update-step`更新步骤状态。** 仅记录事件不会更改步骤状态 — 客户通过查看步骤状态来跟踪进度。**

```bash
# When STARTING a step:
python telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "research" "in_progress"
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" step_started "Starting: Research contractors" "research"

# When COMPLETING a step:
python telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "research" "completed"
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" step_completed "Completed: Research contractors" "research"

# When a step FAILS:
python telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "calls" "failed"
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" error "Failed: Could not reach any contractors" "calls"

# To SKIP a step:
python telnyx_api.py update-step "$MISSION_ID" "$RUN_ID" "setup" "skipped"
```

**总是在`log-event`之前调用`update-step`** — 这确保了步骤状态的正确性，即使事件记录失败。

## 重要提示：step_id是必需的**

**step_id是一个必需的参数** — 它将事件与您的计划步骤关联起来，从而能够跟踪哪些活动属于哪个阶段。

```bash
# With step_id (links to plan step)
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "Found contractor" "research" '{"name": "ABC"}'

# Use "-" if event doesn't belong to a specific step
python telnyx_api.py log-event "$MISSION_ID" "$RUN_ID" custom "General note" "-" '{"note": "value"}'
```

`step_id`应与计划中的`step_id`值之一匹配（例如，“research”、“setup”、“calls”、“analyze”）。

| 操作 | 步骤状态更新 | 事件类型 | step_id | 示例摘要 |
|--------|-------------------|------------|---------|-----------------|
| 开始计划步骤 | `update-step ... in_progress` | `step_started` | step_id | “开始：搜索承包商” |
| 完成步骤 | `update-step ... completed` | `step_completed` | step_id | “完成：搜索承包商” |
| 步骤失败 | `update-step ... failed` | `error` | step_id | “失败：无法联系到承包商” |
| 网页搜索 | — | `tool_call` | “research” | “搜索擦窗承包商” |
| 创建助手 | — | `custom` | “setup” | “创建语音助手：ast_123” |
| 安排通话 | — | `custom` | “calls” | “安排与ABC的通话，时间为下午2:30” |
| 通话完成 | — | `custom` | “通话完成，与ABC通话，获得报价$350” |
| 通话失败 | — | `error` | “calls” | “与XYZ的通话未接听，尝试了3次” |
| 做出决定 | — | `message` | “analyze” | “选择ABC和XYZ作为最佳选项” |

---

# 快速参考：所有命令

```bash
# Check setup
python telnyx_api.py check-key

# Missions
python telnyx_api.py create-mission <name> <instructions>
python telnyx_api.py get-mission <mission_id>
python telnyx_api.py list-missions

# Runs
python telnyx_api.py create-run <mission_id> <input_json>
python telnyx_api.py get-run <mission_id> <run_id>
python telnyx_api.py update-run <mission_id> <run_id> <status>
python telnyx_api.py list-runs <mission_id>

# Plan
python telnyx_api.py create-plan <mission_id> <run_id> <steps_json>
python telnyx_api.py get-plan <mission_id> <run_id>
python telnyx_api.py update-step <mission_id> <run_id> <step_id> <status>
# status: pending, in_progress, completed, skipped, failed

# Events (step_id is REQUIRED - use "-" if no specific step)
python telnyx_api.py log-event <mission_id> <run_id> <type> <summary> <step_id> [payload_json]
python telnyx_api.py list-events <mission_id> <run_id>

# Assistants
python telnyx_api.py list-assistants [--name=<filter>] [--page=<n>] [--size=<n>]
python telnyx_api.py create-assistant <name> <instructions> <greeting> [options_json]
python telnyx_api.py get-assistant <assistant_id>
python telnyx_api.py update-assistant <assistant_id> <updates_json>
python telnyx_api.py get-connection-id <assistant_id> [telephony|messaging]

# Phone Numbers
python telnyx_api.py list-phones [--available]
python telnyx_api.py get-available-phone
python telnyx_api.py assign-phone <phone_id> <connection_id> [voice|sms]

# Scheduled Events
python telnyx_api.py schedule-call <assistant_id> <to_phone> <from_phone> <datetime> <mission_id> <run_id> [dynamic_variables_json]
python telnyx_api.py schedule-sms <assistant_id> <to_phone> <from_phone> <datetime> <text> [dynamic_variables_json]
python telnyx_api.py get-event <assistant_id> <event_id>
python telnyx_api.py cancel-scheduled-event <assistant_id> <event_id>
python telnyx_api.py list-events-assistant <assistant_id>

# Insights (conversation results - POLL until status is "completed"!)
python telnyx_api.py get-insights <conversation_id>

# Insight Templates (CRUD)
python telnyx_api.py create-insight <name> <instructions> [options_json]  # options: json_schema, webhook
python telnyx_api.py get-insight <insight_id>
python telnyx_api.py list-insights
python telnyx_api.py update-insight <insight_id> <updates_json>

# Insight Groups
python telnyx_api.py create-insight-group <name> [options_json]  # options: description, webhook
python telnyx_api.py get-insight-group <group_id>
python telnyx_api.py list-insight-groups
python telnyx_api.py update-insight-group <group_id> <updates_json>
python telnyx_api.py assign-insight <group_id> <insight_id>
python telnyx_api.py unassign-insight <group_id> <insight_id>

# Mission Run Agents (linking agents to runs)
python telnyx_api.py link-agent <mission_id> <run_id> <telnyx_agent_id>
python telnyx_api.py list-linked-agents <mission_id> <run_id>
python telnyx_api.py unlink-agent <mission_id> <run_id> <telnyx_agent_id>

# State Management
python telnyx_api.py list-state
python telnyx_api.py get-state <slug>
python telnyx_api.py remove-state <slug>

# Memory (SAVE OFTEN!)
python telnyx_api.py save-memory <slug> <key> <value_json>
python telnyx_api.py get-memory <slug> [key]
python telnyx_api.py append-memory <slug> <key> <item_json>

# High-Level Workflows
python telnyx_api.py init <name> <instructions> <request> [steps_json]
python telnyx_api.py setup-agent <slug> <name> <instructions> <greeting>
python telnyx_api.py complete <slug> <mission_id> <run_id> <summary> [payload_json]
```

---

# 完整示例：擦窗承包商

```bash
# 1. Initialize the mission (creates mission, run, plan, sets to running)
python telnyx_api.py init "Find window washing contractors" \
  "Find contractors in Chicago, call them, negotiate rates, select best two" \
  "Find me window washing contractors in Chicago" \
  '[{"step_id": "research", "description": "Find contractors online", "sequence": 1}, {"step_id": "setup", "description": "Create voice agent", "sequence": 2}, {"step_id": "calls", "description": "Schedule and make calls", "sequence": 3}, {"step_id": "analyze", "description": "Analyze results", "sequence": 4}]'

# Output: Created mission: mis_abc123
#         Created run: run_def456

# 2. Get the mission slug and IDs from state
python telnyx_api.py get-state "find-window-washing-contractors"

# 3. Mark research step as in_progress and start working
python telnyx_api.py update-step "mis_abc123" "run_def456" "research" "in_progress"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_started "Starting: Find contractors online" "research"

# 4. Setup voice agent (creates assistant, links to run, assigns phone number)
python telnyx_api.py update-step "mis_abc123" "run_def456" "setup" "in_progress"
python telnyx_api.py setup-agent "find-window-washing-contractors" \
  "Contractor Caller" \
  "You are calling to get quotes for commercial window washing. Ask about: rates per floor, availability, insurance. Be professional." \
  "Hi, I am calling to inquire about your commercial window washing services. Do you have a moment to discuss rates?"

# Output: Created assistant: ast_xyz789
#         Linked agent ast_xyz789 to run run_def456
#         Found available: +15559876543
#         Assigned phone number 123456

python telnyx_api.py update-step "mis_abc123" "run_def456" "setup" "completed"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_completed "Completed: Voice agent setup" "setup"

# 5. Get agent phone from state
AGENT_PHONE=$(python telnyx_api.py get-state "find-window-washing-contractors" | python -c "import sys,json; print(json.load(sys.stdin).get('agent_phone',''))")
ASSISTANT_ID=$(python telnyx_api.py get-state "find-window-washing-contractors" | python -c "import sys,json; print(json.load(sys.stdin).get('assistant_id',''))")

# 6. After research, SAVE to memory AND log events with step_id (CRITICAL!)
python telnyx_api.py append-memory "find-window-washing-contractors" "contractors_found" '{"name": "ABC Cleaning", "phone": "+13125551234", "source": "web search"}'
python telnyx_api.py log-event "mis_abc123" "run_def456" custom "Found contractor: ABC Cleaning" "research" '{"name": "ABC Cleaning", "phone": "+13125551234"}'

python telnyx_api.py append-memory "find-window-washing-contractors" "contractors_found" '{"name": "XYZ Windows", "phone": "+13125555678", "source": "web search"}'
python telnyx_api.py log-event "mis_abc123" "run_def456" custom "Found contractor: XYZ Windows" "research" '{"name": "XYZ Windows", "phone": "+13125555678"}'

# 7. Complete research step, start calls step
python telnyx_api.py update-step "mis_abc123" "run_def456" "research" "completed"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_completed "Completed: Found 2 contractors" "research"
python telnyx_api.py update-step "mis_abc123" "run_def456" "calls" "in_progress"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_started "Starting: Schedule calls" "calls"

# 8. Schedule calls
python telnyx_api.py schedule-call "$ASSISTANT_ID" "+13125551234" "$AGENT_PHONE" "2024-12-01T15:00:00Z" "$MISSION_ID" "$RUN_ID"

# Output: Scheduled call: evt_abc123

# 9. SAVE scheduled event to memory AND log event with step_id (CRITICAL!)
python telnyx_api.py append-memory "find-window-washing-contractors" "calls_scheduled" '{"event_id": "evt_abc123", "contractor": "ABC Cleaning", "scheduled_for": "2024-12-01T15:00:00Z"}'
python telnyx_api.py log-event "mis_abc123" "run_def456" custom "Scheduled call to ABC Cleaning for 3:00 PM" "calls" '{"scheduled_event_id": "evt_abc123", "contractor": "ABC Cleaning"}'

# 10. Poll for completion (after scheduled time)
python telnyx_api.py get-event "$ASSISTANT_ID" "evt_abc123"

# Output: Status: completed, conversation_id: conv_xyz

# 11. Get insights - POLL UNTIL STATUS IS "completed"
python telnyx_api.py get-insights "conv_xyz"
# Output: Insight status: in_progress
# (wait 10 seconds and retry)

python telnyx_api.py get-insights "conv_xyz"
# Output: Insight status: in_progress
# (wait 10 seconds and retry)

python telnyx_api.py get-insights "conv_xyz"
# Output: Insight: Customer quoted $350 for a 10-story building. Available next week.
# (status is now "completed" - proceed with the insight data)

# 12. SAVE call results to memory AND log event with step_id (CRITICAL!)
python telnyx_api.py save-memory "find-window-washing-contractors" "call_results" '{"ABC Cleaning": {"status": "completed", "conversation_id": "conv_xyz", "quote": 350, "availability": "next week"}}'
python telnyx_api.py log-event "mis_abc123" "run_def456" custom "Call completed: ABC Cleaning quoted $350, available next week" "calls" '{"contractor": "ABC Cleaning", "quote": 350, "conversation_id": "conv_xyz"}'

# 13. Complete calls step, start analyze step
python telnyx_api.py update-step "mis_abc123" "run_def456" "calls" "completed"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_completed "Completed: All calls done" "calls"
python telnyx_api.py update-step "mis_abc123" "run_def456" "analyze" "in_progress"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_started "Starting: Analyze results" "analyze"

# 14. Complete the mission (mark analyze step done first)
python telnyx_api.py update-step "mis_abc123" "run_def456" "analyze" "completed"
python telnyx_api.py log-event "mis_abc123" "run_def456" step_completed "Completed: Analysis done" "analyze"
python telnyx_api.py complete "find-window-washing-contractors" "mis_abc123" "run_def456" \
  "Found 2 best contractors: ABC ($350) and XYZ ($380)" \
  '{"recommended": ["ABC Cleaning", "XYZ Windows"]}'

# Output: Updated run run_def456: succeeded
#         Mission 'find-window-washing-contractors' completed successfully
```

---

# ⚠️ 在创建任何内容之前：查看现有资源

**在创建新的助手、洞察或洞察组之前，始终检查已有的资源。** 重用比重复更好。

### 飞行前检查清单

在每个任务开始时运行这些命令，以清点可用的资源：

```bash
# 1. Search for existing assistants by name — maybe one already fits your use case
python telnyx_api.py list-assistants --name=Weather
python telnyx_api.py list-assistants  # or list all (paginated)
python telnyx_api.py list-assistants --page=2  # next page

# 2. List existing insight templates — reuse structured insights across missions
python telnyx_api.py list-insights

# 3. List existing insight groups — you may only need to add an insight to an existing group
python telnyx_api.py list-insight-groups

# 4. List available phone numbers — check what's already assigned vs free
python telnyx_api.py list-phones --available
```

**所有列表命令都是分页的。** 如果您有很多资源，可以使用`--page=N`进行分页。助手名称过滤器支持子字符串匹配 — 使用它来快速找到相关的助手，而无需滚动页面。**

### 决策流程

#### ⚠️ 重要提示：未经修改地重用

**规则是：如果可以原样使用现有资源，请重用它们。** 不要修改可能被其他任务或用户使用的现有助手、洞察或洞察组。** 修改共享资源（例如，更改助手的指令或洞察的架构）可能会无意中破坏依赖当前配置的工作流程。

**可以安全地未经修改地重用：**
- 指令、工具、语音和设置已经完全符合您需求的现有助手
- 模式/指令已经提取了您所需信息的现有洞察模板
- 始终重用的默认“Summary”洞察
- 已经包含您所需洞察的现有洞察组

**在以下情况下创建新资源而不是重用：**
- 您需要不同的指令、工具、语音或模型 → **创建新的助手**
- 您需要不同的提取模式 → **创建新的洞察模板**
- 您需要不同的洞察组合 → **创建新的洞察组**
- 现有资源“接近但需要调整” → **创建新的，不要修改现有的**

**对于动态上下文（例如，在每次通话中插入“最佳报价”）**，使用**通过安排的事件API传递动态变量**，而不是修改助手。在助手的指令中定义变量占位符（例如，`{{best_quote}}），然后在安排时传递值。这样可以在每次通话中保持助手的不变性。**

1. **助手：**搜索现有的助手。如果有一个完全符合您需求的助手（指令、工具、语音、模型），请重用它。如果它接近但不完全符合，**创建一个新的** — 不要修改现有的：
   ```bash
   python telnyx_api.py list-assistants --name=Weather  # search by name
   python telnyx_api.py get-assistant <id>  # inspect full config before deciding
   # If it fits → reuse as-is
   # If it doesn't fit → create a new assistant instead
   ```

2. **洞察：**像“提取最高温度和降雪概率”这样的结构化洞察可以在许多任务中重复使用。在创建新的洞察之前，请检查`list-insights`。如果有一个具有正确模式的良好洞察，请将其分配给您的组。如果您需要不同的模式，请创建新的洞察模板 — 不要修改现有的。
3. **洞察组：**每个任务创建一个新的组（它们很便宜），但在它们匹配时用现有的洞察模板填充它们。只有当您的数据提取需求确实新的时候才创建新的洞察模板。

**对于动态上下文（例如，在Class 3顺序谈判中，您需要在每次通话中插入“最佳报价”）**，使用**通过安排的事件API传递动态变量**，而不是修改助手。在助手的指令中定义变量占位符（例如，`{{best_quote}}），然后在安排时传递值。这样可以在每次通话中保持助手的不变性。

1. **助手：**搜索现有的助手。如果有一个完全符合您需求的助手（指令、工具、语音、模型），请重用它。如果它接近但不完全符合，**创建一个新的** — 不要修改现有的：
   ```bash
   python telnyx_api.py list-assistants --name=Weather  # search by name
   python telnyx_api.py get-assistant <id>  # inspect full config before deciding
   # If it fits → reuse as-is
   # If it doesn't fit → create a new assistant instead
   ```

2. **洞察：**像“提取最高温度和降雪概率”这样的结构化洞察可以在许多任务中重复使用。在创建新的洞察之前，请检查`list-insights`。如果有一个具有正确模式的良好洞察，请将其分配给您的组。如果您需要不同的模式，创建新的洞察模板 — 不要修改现有的。
3. **洞察组：**每个任务创建一个新的组（它们很便宜），但在它们匹配时用现有的洞察模板填充它们。只有当您的数据提取需求确实新的时候才创建新的洞察模板。

## 任务类别

并非所有任务都相同。在计划之前，确定您的任务属于哪一类 — 这决定了通话是并行进行还是串行进行，状态如何在通话之间流动，以及是否需要人工干预。

## 决策树

```
Does call N depend on results of call N-1?
  YES → Is it negotiation (leveraging previous results)?
    YES → Class 3: Sequential Negotiation
    NO  → Does it have distinct rounds with human approval?
      YES → Class 4: Multi-Round / Follow-up
      NO  → Class 5: Information Gathering → Action
  NO  → Do you need structured scoring/ranking?
    YES → Class 2: Parallel Screening with Rubric
    NO  → Class 1: Parallel Sweep
```

---

## 类别1：并行扫雷

并行分批拨打电话。每个电话都问同一个问题。没有任何电话依赖于另一个电话的结果。收集所有答案，然后进行比较。

### 何时使用
- 对许多目标提出相同的问题（天气、营业时间、可用性、价格）
- 排序无关紧要 — 所有电话都是独立的
- 您需要原始数据收集，而不是评分或排名

### 关键模式
- 所有电话都使用**相同的助手**和相同的指令
- 将所有电话安排在同一批次中（遵守节流限制 — 每隔1-2分钟交错）
- 使用**带有JSON模式的结构化洞察**来提取可比较的数据
- 分析在所有电话完成后进行

### 示例1：天气IVR扫雷

**目标：**拨打10个气象站的电话，提取今天的最高温度，并进行比较。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create IVR assistant with DTMF + structured insight", "sequence": 1},
  {"step_id": "calls", "description": "Schedule calls to all 10 stations", "sequence": 2},
  {"step_id": "poll", "description": "Poll for completion and collect insights", "sequence": 3},
  {"step_id": "analyze", "description": "Compare temperatures, find hottest/coldest", "sequence": 4}
]

# Insight schema
{"type": "object", "properties": {
  "location": {"type": "string"},
  "high_temp_f": {"type": "number"},
  "snow_mentioned": {"type": "boolean"},
  "forecast_summary": {"type": "string"}
}, "required": ["location", "high_temp_f"]}

# Flow:
# 1. Create assistant with send_dtmf tool + insight group
# 2. Schedule all 10 calls in one batch (staggered 1 min apart)
# 3. Cron job polls every 2 min, collects structured insights
# 4. When all done: compare high_temp_f across all results, report hottest city
```

### 示例2：商店营业时间检查

**目标：**拨打10家零售店的电话，确认营业时间。

```bash
# Same pattern: single assistant, all calls in parallel
# Assistant instructions: "You are calling to confirm store hours for [HOLIDAY].
#   Ask: What time do you open and close on [DATE]? Are you open at all?"
# Insight schema:
{"type": "object", "properties": {
  "store_name": {"type": "string"},
  "is_open": {"type": "boolean"},
  "open_time": {"type": "string"},
  "close_time": {"type": "string"},
  "notes": {"type": "string"}
}, "required": ["store_name", "is_open"]}

# Schedule all 10 calls → poll → compare → report table of hours
```

---

## 类别2：带有评分标准的并行筛选

并行分批拨打电话，但每个电话都遵循结构化的评分标准。结果通过结构化洞察自动评分，然后事后排名。

### 何时使用
- 您需要**对许多候选人进行排名或筛选**
- 每个电话都根据相同的标准进行评估（评分卡）
- 评分足够客观，可以定义为模式
- 您需要自动化排名，而不仅仅是原始数据

### 关键模式
- 提前定义**评分标准作为结构化洞察模式** — 包括数字分数、枚举、布尔值
- 洞察模板从对话中自动进行评分
- 在所有电话完成后，根据评分字段对结果进行排序/筛选
- 助手指令应指导对话以涵盖所有评分标准维度

### 示例1：餐厅预订侦察

**目标：**拨打10家餐厅的电话，根据可用性/价格/氛围进行评分，排名前三名。

```bash
# Insight schema (the rubric)
{"type": "object", "properties": {
  "restaurant_name": {"type": "string"},
  "has_availability": {"type": "boolean", "description": "Table available for requested date/time/party size"},
  "availability_score": {"type": "integer", "description": "1-5, 5 = exact time available, 1 = nothing close"},
  "price_range": {"type": "string", "enum": ["$", "$$", "$$$", "$$$$"]},
  "estimated_per_person": {"type": "number"},
  "ambiance_notes": {"type": "string"},
  "ambiance_score": {"type": "integer", "description": "1-5 based on description of atmosphere"},
  "wait_time_minutes": {"type": "number"},
  "overall_score": {"type": "integer", "description": "1-10 overall recommendation"}
}, "required": ["restaurant_name", "has_availability", "availability_score", "price_range", "overall_score"]}

# Assistant instructions:
# "You are calling to check availability for dinner Friday at 7pm, party of 4.
#  Ask about: availability, approximate price per person, dress code/atmosphere,
#  expected wait time. Be conversational and polite."

# Flow:
# 1. Create insight template with rubric schema
# 2. Create assistant with insight group wired up
# 3. Schedule all 10 calls in parallel
# 4. Collect structured insights → sort by overall_score desc → report top 3
```

### 示例2：面试筛选

**目标：**通过电话筛选10位候选人，根据沟通/经验/文化契合度进行评分，排名前三名。

```bash
# Insight schema (the rubric)
{"type": "object", "properties": {
  "candidate_name": {"type": "string"},
  "communication_score": {"type": "integer", "description": "1-5, clarity and professionalism"},
  "experience_years": {"type": "number"},
  "relevant_experience_score": {"type": "integer", "description": "1-5, relevance to the role"},
  "culture_fit_score": {"type": "integer", "description": "1-5, enthusiasm and alignment"},
  "salary_expectation": {"type": "number"},
  "available_start_date": {"type": "string"},
  "red_flags": {"type": "string", "description": "Any concerns noted"},
  "overall_score": {"type": "integer", "description": "1-10 overall recommendation"}
}, "required": ["candidate_name", "communication_score", "relevant_experience_score", "culture_fit_score", "overall_score"]}

# Assistant instructions cover specific screening questions for the role
# All 10 calls run in parallel → rank by overall_score → shortlist top 3
```

## 类别3：顺序谈判

通话必须顺序进行。每个电话的策略都依赖于之前的结果。您正在利用之前的信息来获得更好的结果。

**⚠️ 绝不要并行化这些。** 整个价值来自于顺序信息的优势。

### 何时使用
- 您正在**谈判** — 报价、价格、条款
- “目前最好的报价是X美元，你能超越它吗？”
- 每个电话都需要之前通话的上下文
- 通话顺序是一个战略决策

### 关键模式
- **动态变量：**在安排的事件中使用`dynamic_variables`来根据每次通话注入上下文 — 不需要在通话之间修改助手
- **状态向前传递：** 在内存中跟踪“迄今为止的最佳报价”，并将其作为动态变量传递给下一个通话
- **通话顺序策略：** 从最不可能给出最佳报价的人开始（最弱的手开始）以便建立优势。将最强的候选人留到最后。**另一种方法：从最有可能给出可靠基线的候选人开始**
- **一次一个电话：** 按照（带有动态变量的）顺序安排 → 轮询 → 获取洞察 → 更新状态 → 安排下一个
- **助手保持不变：** 一次定义`{{best_quote}}`和`{{best_company}}`占位符，然后通过安排的事件API在每次通话中传递不同的值

### 示例1：屋顶工人报价

**目标：**依次拨打5个屋顶工人的电话，与之前的最佳报价进行谈判。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create assistant + find roofers", "sequence": 1},
  {"step_id": "call-1", "description": "Call roofer 1 (baseline)", "sequence": 2},
  {"step_id": "call-2", "description": "Call roofer 2 with context", "sequence": 3},
  {"step_id": "call-3", "description": "Call roofer 3 with context", "sequence": 4},
  {"step_id": "call-4", "description": "Call roofer 4 with context", "sequence": 5},
  {"step_id": "call-5", "description": "Call roofer 5 with context", "sequence": 6},
  {"step_id": "analyze", "description": "Select best deal", "sequence": 7}
]

# Flow:
# 1. Create assistant with dynamic variable placeholders in instructions:
#    "Ask for a quote for roof repair on a 2000 sq ft home. Get price, timeline, warranty.
#     {{#if best_quote}}
#     CONTEXT: You have received a quote of {{best_quote}} from {{best_company}}.
#     Mention this if the price seems high. Ask if they can match or beat it.
#     {{/if}}"
#    Set dynamic_variables: {"best_quote": null, "best_company": null}

# 2. Call roofer 1 (no leverage yet — best_quote is null, so that section is skipped)
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID
#    → get insight → save quote ($500)
#    python telnyx_api.py save-memory "<slug>" "best_quote" '{"amount": 500, "company": "Roofer 1"}'

# 3. Call roofer 2 — pass dynamic variables via scheduled event:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID \
#      '{"best_quote": "$500", "best_company": "Roofer 1"}'
#    → get insight → if better ($420), update best_quote

# 4. Call roofer 3 — pass updated context:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID \
#      '{"best_quote": "$420", "best_company": "Roofer 2"}'

# 5. Repeat: schedule with new dynamic vars → poll → insight → update state → next
# 6. After all 5: report best deal with full comparison
```

### 示例2：汽车保险报价

**目标：**拨打4家保险公司的电话，利用每个报价进行下一步谈判。

```bash
# Ordering strategy: Start with the provider you care least about (get a baseline),
# end with your preferred provider (maximum leverage).

# Assistant instructions use dynamic variable placeholders:
#   "You are calling about auto insurance for a 2022 Toyota Camry.
#    {{#if best_quote}}
#    LEVERAGE: The best quote so far is {{best_quote}}/month
#    from {{best_company}}. Mention this and ask them to beat it.
#    {{/if}}"

# Sequential pattern — pass dynamic variables per call:
# Call 1 (baseline): no leverage vars → "What's your rate for [coverage details]?"
# Call 2: {"best_quote": "$180", "best_company": "Geico"}
# Call 3: {"best_quote": "$155", "best_company": "Progressive"}
# Call 4 (preferred): {"best_quote": "$145", "best_company": "StateFarm"}
```

---

## 类别4：多轮/跟进

任务有明确的阶段。第一轮是广泛的外联。结果进行分析，然后由人工进行筛选。

### 何时使用
- 有两个或更多不同的呼叫阶段
- 需要在轮次之间进行人工判断（审批关卡）
- 第二轮针对第一轮的筛选结果

### 关键模式
- 计划有明确的阶段：`round-1-calls`、`round-1-analysis`、`human-approval`、`round-2-calls`
- **人工审批关卡：** 通过Telegram/Slack向人工发送第一轮的结果+建议。等待他们的回复。
- 第二轮的助手可能有**完全不同的指令**

### 示例1：供应商选择

**目标：**根据基本标准筛选10个供应商，通过人工审批筛选前三名。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant + insight rubric", "sequence": 1},
  {"step_id": "round-1-calls", "description": "Screen all 10 vendors", "sequence": 2},
  {"step_id": "round-1-analysis", "description": "Rank and shortlist top 3", "sequence": 3},
  {"step_id": "human-approval", "description": "DM human with top 3, wait for approval", "sequence": 4},
  {"step_id": "round-2-setup", "description": "Create deep-dive assistant with technical questions", "sequence": 5},
  {"step_id": "round-2-calls", "description": "Deep-dive calls with approved vendors", "sequence": 6},
  {"step_id": "final-analysis", "description": "Final recommendation", "sequence": 7}
]

# Round 1 assistant: "Ask about pricing, lead time, minimum order, and general capabilities."
# Round 1 insight rubric: price_score, lead_time_days, meets_minimum, capability_match

# After Round 1 completes:
# → Rank by scores → DM human:
#   "Round 1 complete. Top 3 vendors:
#    1. VendorA — score 8.5, $12/unit, 2-week lead
#    2. VendorB — score 7.8, $14/unit, 1-week lead
#    3. VendorC — score 7.2, $11/unit, 3-week lead
#    Approve these for Round 2? Reply YES or adjust."

# Wait for human response (pause cron or check for reply)

# Round 2 assistant (different!): "Ask detailed technical questions:
#   API integration support? SLA guarantees? Disaster recovery?
#   Reference customers we can contact?"
# Round 2 insight rubric: api_support, sla_score, dr_plan, references_provided
```

### 示例2：候选人招聘

**目标：**通过电话筛选15位候选人（第一轮），筛选出5位（人工审批），进行详细面试（第二轮）。

```bash
# Round 1: Quick 5-minute screen — "Tell me about your background, why this role,
#   salary expectations, availability."
# Insight rubric: communication_score, experience_match, salary_in_range, enthusiasm

# → Rank → DM human with top 5 + scores
# → Human approves (or swaps in someone from position 6-7)

# Round 2: 15-minute deep dive — completely different assistant:
#   "Ask about: specific project experience with [TECH], how they handle conflict,
#    a time they failed and what they learned, questions they have for us."
# Different insight rubric: technical_depth, problem_solving, culture_fit, curiosity

# Track in memory:
python telnyx_api.py save-memory "<slug>" "rounds" '{
  "round_1": {"candidates": [...], "advanced": ["+1555...", "+1555..."]},
  "round_2": {"candidates": [...], "results": [...]}
}'
```

## 类别5：信息收集 → 行动

打电话收集信息，但任务不仅仅是报告 — 它**根据结果采取行动**。一旦找到您需要的信息，就停止搜索并采取行动。

### 何时使用
- 您需要**找到**某些东西（可用性、时间、匹配项），然后**采取行动**（预订它、确认它）
- 提前终止：一旦达到目标，就停止呼叫

### 关键模式
- **提前终止：** 当电话成功时（例如，餐厅有空位）**，停止呼叫。

### 示例1：餐厅预订

**目标：**拨打餐厅的电话，直到找到周五下午4点的空位，然后预订它。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant", "sequence": 1},
  {"step_id": "screen", "description": "Call restaurants to check availability", "sequence": 2},
  {"step_id": "book", "description": "Book at first available restaurant", "sequence": 3}
]

# Flow:
# 1. Create assistant: "Call and ask if they have a table for 4 this Friday at 7pm.
#    If yes, say you'd like to book it under the name [NAME]. Confirm the reservation.
#    If no, ask about Saturday instead, then politely end the call."

# 2. Schedule calls to 5 restaurants (parallel — screening doesn't depend on each other)

# 3. Poll results as they come in:
#    - Restaurant A: no availability → continue
#    - Restaurant B: has availability, BOOKED! → SUCCESS
#    - Cancel/ignore remaining calls (Restaurants C, D, E)
#    - If none of the 5 work: expand to 5 more restaurants (fallback)

# Insight schema:
{"type": "object", "properties": {
  "restaurant_name": {"type": "string"},
  "has_availability": {"type": "boolean"},
  "reservation_confirmed": {"type": "boolean"},
  "reservation_time": {"type": "string"},
  "reservation_name": {"type": "string"},
  "confirmation_number": {"type": "string"},
  "alternative_offered": {"type": "string"}
}, "required": ["restaurant_name", "has_availability", "reservation_confirmed"]}

# Early termination: when reservation_confirmed = true, mission succeeds
```

### 示例2：预约安排

**目标：**拨打牙医办公室的电话，直到找到本周的预约时间。

```bash
# Same pattern as restaurant booking:
# 1. Screen in parallel: "Do you have any openings this week for a cleaning?"
# 2. First office with availability: "I'd like to book that slot for [NAME], DOB [DOB]."
# 3. Stop remaining calls once booked.

# Key difference: may need to provide insurance info, patient details.
# Assistant instructions include all necessary details upfront.

# Fallback: if no office has availability this week, expand search to next week
# or expand to more offices.
```

## 跨类别模式

这些模式适用于多个任务类别。

### 1. 通话之间的动态上下文

使用**通过安排的事件API传递动态变量**，将之前通话的结果注入每个通话中。这保持助手的不变性 — 在指令中定义`{{variable}}占位符，然后通过安排的事件传递不同的值。这对于类别3（顺序谈判）和类别5（行动阶段）至关重要。

```bash
# Assistant instructions use placeholders:
#   "You are calling to get a quote for roof repair on a 2000 sq ft home.
#    {{#if best_quote}}
#    IMPORTANT CONTEXT: Another contractor has quoted {{best_quote}}.
#    If this contractor quotes higher, mention you have a better offer and ask if
#    they can match or beat it. Be professional but firm.
#    {{/if}}"

# After getting a quote of $350 from call 1, pass it as a dynamic variable on call 2:
python telnyx_api.py schedule-call <assistant_id> "+1555..." "+1555..." "<time>" <mission_id> <run_id> '{"best_quote": "$350", "best_company": "ABC Roofing"}'
```

### 2. 人工审批关卡

在轮次之间或采取行动之前，通过Telegram/Slack与人工联系并暂停。

```
# Pattern:
# 1. Cron job detects Round 1 complete
# 2. Formats results summary
# 3. Sends message to human via Telegram/Slack
# 4. Saves state: {"awaiting_approval": true, "approval_summary": "..."}
# 5. Cron continues to poll but takes no action until human responds
# 6. Human replies "approved" or "change X" → cron detects reply → proceeds
```

### 3. 提前终止

当目标达成时，停止不必要的剩余通话。

```bash
# Check for pending events:
python telnyx_api.py list-events-assistant <assistant_id>

# Cancel each pending event:
python telnyx_api.py cancel-scheduled-event <assistant_id> <event_id>
```

### 4. 通话顺序策略

对于顺序谈判（类别3），呼叫顺序很重要：

- **最弱的人先开始：** 从您最不关心的供应商开始。在没有压力的情况下获取基准。使用他们的报价作为优势。
- **最强的最后一个：** 最后使用最有力的供应商。
- **先确定基准：** 或者先从最有可能给出可靠基准的供应商开始。

### 示例1：屋顶工人报价

**目标：**依次拨打5个屋顶工人的电话，与之前的最佳报价进行谈判。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create assistant + find roofers", "sequence": 1},
  {"step_id": "call-1", "description": "Call roofer 1 (baseline)", "sequence": 2},
  {"step_id": "call-2", "description": "Call roofer 2 with context", "sequence": 3},
  {"step_id": "call-3", "description": "Call roofer 3 with context", "sequence": 4},
  {"step_id": "call-4", "description": "Call roofer 4 with context", "sequence": 5},
  {"step_id": "call-5", "description": "Call roofer 5 with context", "sequence": 6},
  {"step_id": "analyze", "description": "Select best deal", "sequence": 7}
]

# Flow:
# 1. Create assistant with dynamic variable placeholders in instructions:
#    "Ask for a quote for roof repair on a 2000 sq ft home. Get price, timeline, warranty.
#     {{#if best_quote}}
#     CONTEXT: You have received a quote of {{best_quote}} from {{best_company}}.
#     Mention this if the price seems high. Ask if they can match or beat it.
#     {{/if}}"
#    Set dynamic_variables: {"best_quote": null, "best_company": null}

# 2. Call roofer 1 (no leverage yet — best_quote is null, so that section is skipped)
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID
#    → get insight → save quote ($500)
#    python telnyx_api.py save-memory "<slug>" "best_quote" '{"amount": 500, "company": "Roofer 1"}'

# 3. Call roofer 2 — pass dynamic variables via scheduled event:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID \
#      '{"best_quote": "$500", "best_company": "Roofer 1"}'
#    → get insight → if better ($420), update best_quote

# 4. Call roofer 3 — pass updated context:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID \
#      '{"best_quote": "$420", "best_company": "Roofer 2"}'

# 5. Repeat: schedule with new dynamic vars → poll → insight → update state → next
# 6. After all 5: report best deal with full comparison
```

### 示例2：汽车保险报价

**目标：**拨打4家保险公司的电话，利用每个报价进行下一步谈判。

```bash
# Ordering strategy: Start with the provider you care least about (get a baseline),
# end with your preferred provider (maximum leverage).

# Assistant instructions use dynamic variable placeholders:
#   "You are calling about auto insurance for a 2022 Toyota Camry.
#    {{#if best_quote}}
#    LEVERAGE: The best quote so far is {{best_quote}}/month
#    from {{best_company}}. Mention this and ask them to beat it.
#    {{/if}}"

# Sequential pattern — pass dynamic variables per call:
# Call 1 (baseline): no leverage vars → "What's your rate for [coverage details]?"
# Call 2: {"best_quote": "$180", "best_company": "Geico"}
# Call 3: {"best_quote": "$155", "best_company": "Progressive"}
# Call 4 (preferred): {"best_quote": "$145", "best_company": "StateFarm"}
```

---

## 类别4：多轮/跟进

任务有不同的阶段。第一轮是广泛的外联。结果进行分析，然后由人工批准筛选名单，第二轮进行深入的通话。

### 何时使用
- 有两个或更多不同的呼叫阶段
- 需要在轮次之间进行人工判断（审批关卡）
- 第二轮针对第一轮的筛选结果

### 关键模式
- 计划有明确的阶段：`round-1-calls`、`round-1-analysis`、`human-approval`、`round-2-calls`
- **人工审批关卡：** 通过Telegram/Slack向人工发送第一轮的结果+建议。等待他们的回复。
- 第二轮的助手可能有**完全不同的指令**

### 示例1：供应商选择

**目标：**根据基本标准筛选10个供应商，通过人工审批筛选前三名。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant + insight rubric", "sequence": 1},
  {"step_id": "round-1-calls", "description": "Screen all 10 vendors", "sequence": 2},
  {"step_id": "round-1-analysis", "description": "Rank and shortlist top 3", "sequence": 3},
  {"step_id": "human-approval", "description": "DM human with top 3, wait for approval", "sequence": 4},
  {"step_id": "round-2-setup", "description": "Create deep-dive assistant with technical questions", "sequence": 5},
  {"step_id": "round-2-calls", "description": "Deep-dive calls with approved vendors", "sequence": 6},
  {"step_id": "final-analysis", "description": "Final recommendation", "sequence": 7}
]

# Round 1 assistant: "Ask about pricing, lead time, minimum order, and general capabilities."
# Round 1 insight rubric: price_score, lead_time_days, meets_minimum, capability_match

# After Round 1 completes:
# → Rank by scores → DM human:
#   "Round 1 complete. Top 3 vendors:
#    1. VendorA — score 8.5, $12/unit, 2-week lead
#    2. VendorB — score 7.8, $14/unit, 1-week lead
#    3. VendorC — score 7.2, $11/unit, 3-week lead
#    Approve these for Round 2? Reply YES or adjust."

# Wait for human response (pause cron or check for reply)

# Round 2 assistant (different!): "Ask detailed technical questions:
#   API integration support? SLA guarantees? Disaster recovery?
#   Reference customers we can contact?"
# Round 2 insight rubric: api_support, sla_score, dr_plan, references_provided
```

### 示例2：候选人招聘

**目标：**通过电话筛选15位候选人（第一轮），筛选出5位（人工审批），进行详细面试（第二轮）。

```bash
# Round 1: Quick 5-minute screen — "Tell me about your background, why this role,
#   salary expectations, availability."
# Insight rubric: communication_score, experience_match, salary_in_range, enthusiasm

# → Rank → DM human with top 5 + scores
# → Human approves (or swaps in someone from position 6-7)

# Round 2: 15-minute deep dive — completely different assistant:
#   "Ask about: specific project experience with [TECH], how they handle conflict,
#    a time they failed and what they learned, questions they have for us."
# Different insight rubric: technical_depth, problem_solving, culture_fit, curiosity

# Track in memory:
python telnyx_api.py save-memory "<slug>" "rounds" '{
  "round_1": {"candidates": [...], "advanced": ["+1555...", "+1555..."]},
  "round_2": {"candidates": [...], "results": [...]}
}'
```

## 类别5：信息收集 → 行动

打电话收集信息，但任务不仅仅是报告 — 它**根据结果采取行动**。一旦找到您需要的信息，就停止搜索并采取行动。

### 何时使用
- 您需要**找到**某些东西（可用性、时间、匹配项），然后**采取行动**（预订它、确认它）**

### 示例1：餐厅预订

**目标：**拨打餐厅的电话，直到找到周五下午4点的空位，然后预订它。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant", "sequence": 1},
  {"step_id": "screen", "description": "Call restaurants to check availability", "sequence": 2},
  {"step_id": "book", "description": "Book at first available restaurant", "sequence": 3}
]

# Flow:
# 1. Create assistant: "Call and ask if they have a table for 4 this Friday at 7pm.
#    If yes, say you'd like to book it under the name [NAME]. Confirm the reservation.
#    If no, ask about Saturday instead, then politely end the call."

# 2. Schedule calls to 5 restaurants (parallel — screening doesn't depend on each other)

# 3. Poll results as they come in:
#    - Restaurant A: no availability → continue
#    - Restaurant B: has availability, BOOKED! → SUCCESS
#    - Cancel/ignore remaining calls (Restaurants C, D, E)
#    - If none of the 5 work: expand to 5 more restaurants (fallback)

# Insight schema:
{"type": "object", "properties": {
  "restaurant_name": {"type": "string"},
  "has_availability": {"type": "boolean"},
  "reservation_confirmed": {"type": "boolean"},
  "reservation_time": {"type": "string"},
  "reservation_name": {"type": "string"},
  "confirmation_number": {"type": "string"},
  "alternative_offered": {"type": "string"}
}, "required": ["restaurant_name", "has_availability", "reservation_confirmed"]}

# Early termination: when reservation_confirmed = true, mission succeeds
```

### 示例2：预约安排

**目标：**拨打牙医办公室的电话，直到找到本周的预约时间。

```bash
# Same pattern as restaurant booking:
# 1. Screen in parallel: "Do you have any openings this week for a cleaning?"
# 2. First office with availability: "I'd like to book that slot for [NAME], DOB [DOB]."
# 3. Stop remaining calls once booked.

# Key difference: may need to provide insurance info, patient details.
# Assistant instructions include all necessary details upfront.

# Fallback: if no office has availability this week, expand search to next week
# or expand to more offices.
```

## 跨类别模式

这些模式适用于多个任务类别。

### 1. 通话之间的动态上下文

使用**通过安排的事件API传递动态变量**，将之前通话的结果注入每个通话中。这保持助手的不变性 — 在指令中定义`{{variable}}占位符，然后通过安排的事件传递不同的值。这对于类别3（顺序谈判）和类别5（行动阶段）至关重要。

```bash
# Assistant instructions use placeholders:
#   "You are calling to get a quote for roof repair on a 2000 sq ft home.
#    {{#if best_quote}}
#    IMPORTANT CONTEXT: Another contractor has quoted {{best_quote}}.
#    If this contractor quotes higher, mention you have a better offer and ask if
#    they can match or beat it. Be professional but firm.
#    {{/if}}"

# After getting a quote of $350 from call 1, pass it as a dynamic variable on call 2:
python telnyx_api.py schedule-call <assistant_id> "+1555..." "+1555..." "<time>" <mission_id> <run_id> '{"best_quote": "$350", "best_company": "ABC Roofing"}'
```

### 2. 人工审批关卡

在轮次之间或采取行动之前，通过Telegram/Slack与人工联系并暂停。

```
# Pattern:
# 1. Cron job detects Round 1 complete
# 2. Formats results summary
# 3. Sends message to human via Telegram/Slack
# 4. Saves state: {"awaiting_approval": true, "approval_summary": "..."}
# 5. Cron continues to poll but takes no action until human responds
# 6. Human replies "approved" or "change X" → cron detects reply → proceeds
```

### 3. 提前终止

当目标达成时，停止不必要的剩余通话。

```bash
# Check for pending events:
python telnyx_api.py list-events-assistant <assistant_id>

# Cancel each pending event:
python telnyx_api.py cancel-scheduled-event <assistant_id> <event_id>
```

### 4. 通话顺序策略

对于顺序谈判（类别3），呼叫顺序很重要：

- **最弱的人先开始：** 从您最不关心的供应商开始。在没有压力的情况下获取基准。使用他们的报价作为优势。
- **最强的最后一个：** 最后使用最有力的供应商。
- **先确定基准：** 或者先从最有可能给出可靠基准的供应商开始。
- **顺序安排：** 先拨打最不可能给出最佳报价的供应商（最弱的人）。

### 示例1：屋顶工人报价

**目标：**依次拨打5个屋顶工人的电话，与之前的最佳报价进行谈判。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create assistant + find roofers", "sequence": 1},
  {"step_id": "call-1", "description": "Call roofer 1 (baseline)", "sequence": 2},
  {"step_id": "call-2", "description": "Call roofer 2 with context", "sequence": 3},
  {"step_id": "call-3", "description": "Call roofer 3 with context", "sequence": 4},
  {"step_id": "call-4", "description": "Call roofer 4 with context", "sequence": 5},
  {"step_id": "call-5", "description": "Call roofer 5 with context", "sequence": 6},
  {"step_id": "analyze", "description": "Select best deal", "sequence": 7}
]

# Flow:
# 1. Create assistant with dynamic variable placeholders in instructions:
#    "Ask for a quote for roof repair on a 2000 sq ft home. Get price, timeline, warranty.
#     {{#if best_quote}}
#     CONTEXT: You have received a quote of {{best_quote}} from {{best_company}}.
#     Mention this if the price seems high. Ask if they can match or beat it.
#     {{/if}}"
#    Set dynamic_variables: {"best_quote": null, "best_company": null}

# 2. Call roofer 1 (no leverage yet — best_quote is null, so that section is skipped)
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID
#    → get insight → save quote ($500)
#    python telnyx_api.py save-memory "<slug>" "best_quote" '{"amount": 500, "company": "Roofer 1"}'

# 3. Call roofer 2 — pass dynamic variables via scheduled event:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID \
#      '{"best_quote": "$500", "best_company": "Roofer 1"}'
#    → get insight → if better ($420), update best_quote

# 4. Call roofer 3 — pass updated context:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID \
#      '{"best_quote": "$420", "best_company": "Roofer 2"}'

# 5. Repeat: schedule with new dynamic vars → poll → insight → update state → next
# 6. After all 5: report best deal with full comparison
```

### 示例2：汽车保险报价

**目标：**拨打4家保险公司的电话，利用每个报价进行下一步谈判。

```bash
# Ordering strategy: Start with the provider you care least about (get a baseline),
# end with your preferred provider (maximum leverage).

# Assistant instructions use dynamic variable placeholders:
#   "You are calling about auto insurance for a 2022 Toyota Camry.
#    {{#if best_quote}}
#    LEVERAGE: The best quote so far is {{best_quote}}/month
#    from {{best_company}}. Mention this and ask them to beat it.
#    {{/if}}"

# Sequential pattern — pass dynamic variables per call:
# Call 1 (baseline): no leverage vars → "What's your rate for [coverage details]?"
# Call 2: {"best_quote": "$180", "best_company": "Geico"}
# Call 3: {"best_quote": "$155", "best_company": "Progressive"}
# Call 4 (preferred): {"best_quote": "$145", "best_company": "StateFarm"}
```

## 类别4：多轮/跟进

任务有不同的阶段。第一轮是广泛的外联。结果进行分析，然后由人工批准筛选名单，第二轮进行深入的通话。

### 何时使用
- 有两个或更多不同的呼叫阶段
- 需要在轮次之间进行人工判断（审批关卡）
- 第二轮针对第一轮的筛选结果

### 关键模式
- 计划有明确的阶段：`round-1-calls`、`round-1-analysis`、`human-approval`、`round-2-calls`
- **人工审批关卡：** 通过Telegram/Slack向人工发送第一轮的结果+建议。等待他们的回复。
- 第二轮的助手可能有**完全不同的指令**

### 示例1：供应商选择

**目标：**根据基本标准筛选10个供应商，通过人工审批筛选前三名。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant + insight rubric", "sequence": 1},
  {"step_id": "round-1-calls", "description": "Screen all 10 vendors", "sequence": 2},
  {"step_id": "round-1-analysis", "description": "Rank and shortlist top 3", "sequence": 3},
  {"step_id": "human-approval", "description": "DM human with top 3, wait for approval", "sequence": 4},
  {"step_id": "round-2-setup", "description": "Create deep-dive assistant with technical questions", "sequence": 5},
  {"step_id": "round-2-calls", "description": "Deep-dive calls with approved vendors", "sequence": 6},
  {"step_id": "final-analysis", "description": "Final recommendation", "sequence": 7}
]

# Round 1 assistant: "Ask about pricing, lead time, minimum order, and general capabilities."
# Round 1 insight rubric: price_score, lead_time_days, meets_minimum, capability_match

# After Round 1 completes:
# → Rank by scores → DM human:
#   "Round 1 complete. Top 3 vendors:
#    1. VendorA — score 8.5, $12/unit, 2-week lead
#    2. VendorB — score 7.8, $14/unit, 1-week lead
#    3. VendorC — score 7.2, $11/unit, 3-week lead
#    Approve these for Round 2? Reply YES or adjust."

# Wait for human response (pause cron or check for reply)

# Round 2 assistant (different!): "Ask detailed technical questions:
#   API integration support? SLA guarantees? Disaster recovery?
#   Reference customers we can contact?"
# Round 2 insight rubric: api_support, sla_score, dr_plan, references_provided
```

### 示例2：候选人招聘

**目标：**通过电话筛选15位候选人（第一轮），筛选出5位（人工审批），进行详细面试（第二轮）。

```bash
# Round 1: Quick 5-minute screen — "Tell me about your background, why this role,
#   salary expectations, availability."
# Insight rubric: communication_score, experience_match, salary_in_range, enthusiasm

# → Rank → DM human with top 5 + scores
# → Human approves (or swaps in someone from position 6-7)

# Round 2: 15-minute deep dive — completely different assistant:
#   "Ask about: specific project experience with [TECH], how they handle conflict,
#    a time they failed and what they learned, questions they have for us."
# Different insight rubric: technical_depth, problem_solving, culture_fit, curiosity

# Track in memory:
python telnyx_api.py save-memory "<slug>" "rounds" '{
  "round_1": {"candidates": [...], "advanced": ["+1555...", "+1555..."]},
  "round_2": {"candidates": [...], "results": [...]}
}'
```

## 类别5：信息收集 → 行动

打电话收集信息，但任务不仅仅是报告 — 它**根据结果采取行动**。一旦找到您需要的信息，就停止搜索并采取行动。

### 何时使用
- 您需要**找到**某些东西（可用性、时间、匹配项），然后**采取行动**（预订它、确认它）

### 示例1：餐厅预订

**目标：**拨打餐厅的电话，直到找到周五下午4点的空位，然后预订它。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant", "sequence": 1},
  {"step_id": "screen", "description": "Call restaurants to check availability", "sequence": 2},
  {"step_id": "book", "description": "Book at first available restaurant", "sequence": 3}
]

# Flow:
# 1. Create assistant: "Call and ask if they have a table for 4 this Friday at 7pm.
#    If yes, say you'd like to book it under the name [NAME]. Confirm the reservation.
#    If no, ask about Saturday instead, then politely end the call."

# 2. Schedule calls to 5 restaurants (parallel — screening doesn't depend on each other)

# 3. Poll results as they come in:
#    - Restaurant A: no availability → continue
#    - Restaurant B: has availability, BOOKED! → SUCCESS
#    - Cancel/ignore remaining calls (Restaurants C, D, E)
#    - If none of the 5 work: expand to 5 more restaurants (fallback)

# Insight schema:
{"type": "object", "properties": {
  "restaurant_name": {"type": "string"},
  "has_availability": {"type": "boolean"},
  "reservation_confirmed": {"type": "boolean"},
  "reservation_time": {"type": "string"},
  "reservation_name": {"type": "string"},
  "confirmation_number": {"type": "string"},
  "alternative_offered": {"type": "string"}
}, "required": ["restaurant_name", "has_availability", "reservation_confirmed"]}

# Early termination: when reservation_confirmed = true, mission succeeds
```

### 示例2：预约安排

**目标：**拨打牙医办公室的电话，直到找到本周的预约时间。

```bash
# Same pattern as restaurant booking:
# 1. Screen in parallel: "Do you have any openings this week for a cleaning?"
# 2. First office with availability: "I'd like to book that slot for [NAME], DOB [DOB]."
# 3. Stop remaining calls once booked.

# Key difference: may need to provide insurance info, patient details.
# Assistant instructions include all necessary details upfront.

# Fallback: if no office has availability this week, expand search to next week
# or expand to more offices.
```

## 跨类别模式

这些模式适用于多个任务类别。

### 1. 通话之间的动态上下文

使用**通过安排的事件API传递动态变量**，将之前通话的结果注入每个通话中。这保持助手的不变性 — 在指令中定义`{{variable}}占位符，然后通过安排的事件传递不同的值。这对于类别3（顺序谈判）和类别5（行动阶段）至关重要。

### 2. 人工审批关卡

在轮次之间或采取行动之前，通过Telegram/Slack与人工联系并暂停。

```
# Pattern:
# 1. Cron job detects Round 1 complete
# 2. Formats results summary
# 3. Sends message to human via Telegram/Slack
# 4. Saves state: {"awaiting_approval": true, "approval_summary": "..."}
# 5. Cron continues to poll but takes no action until human responds
# 6. Human replies "approved" or "change X" → cron detects reply → proceeds
```

### 3. 提前终止

当目标达成时，停止不必要的剩余通话。

```bash
# Check for pending events:
python telnyx_api.py list-events-assistant <assistant_id>

# Cancel each pending event:
python telnyx_api.py cancel-scheduled-event <assistant_id> <event_id>
```

### 4. 通话顺序策略

对于顺序谈判（类别3），呼叫顺序很重要：

- **最弱的人先开始：** 从您最不关心的供应商开始。在没有压力的情况下获取基准。使用他们的报价作为优势。
- **最强的最后一个：** 最后使用最有力的供应商。
- **先确定基准：** 或者先从最有可能给出可靠基准的供应商开始。
- **顺序安排：** 先拨打最不可能给出可靠基准的供应商（最弱的人）。

### 示例1：屋顶工人报价

**目标：**依次拨打5个屋顶工人的电话，与之前的最佳报价进行谈判。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create assistant + find roofers", "sequence": 1},
  {"step_id": "call-1", "description": "Call roofer 1 (baseline)", "sequence": 2},
  {"step_id": "call-2", "description": "Call roofer 2 with context", "sequence": 3},
  {"step_id": "call-3", "description": "Call roofer 3 with context", "sequence": 4},
  {"step_id": "call-4", "description": "Call roofer 4 with context", "sequence": 5},
  {"step_id": "call-5", "description": "Call roofer 5 with context", "sequence": 6},
  {"step_id": "analyze", "description": "Select best deal", "sequence": 7}
]

# Flow:
# 1. Create assistant with dynamic variable placeholders in instructions:
#    "Ask for a quote for roof repair on a 2000 sq ft home. Get price, timeline, warranty.
#     {{#if best_quote}}
#     CONTEXT: You have received a quote of {{best_quote}} from {{best_company}}.
#     Mention this if the price seems high. Ask if they can match or beat it.
#     {{/if}}"
#    Set dynamic_variables: {"best_quote": null, "best_company": null}

# 2. Call roofer 1 (no leverage yet — best_quote is null, so that section is skipped)
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID
#    → get insight → save quote ($500)
#    python telnyx_api.py save-memory "<slug>" "best_quote" '{"amount": 500, "company": "Roofer 1"}'

# 3. Call roofer 2 — pass dynamic variables via scheduled event:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID \
#      '{"best_quote": "$500", "best_company": "Roofer 1"}'
#    → get insight → if better ($420), update best_quote

# 4. Call roofer 3 — pass updated context:
#    python telnyx_api.py schedule-call <id> "+1555..." "+1555..." "<time>" $MISSION_ID $RUN_ID \
#      '{"best_quote": "$420", "best_company": "Roofer 2"}'

# 5. Repeat: schedule with new dynamic vars → poll → insight → update state → next
# 6. After all 5: report best deal with full comparison
```

### 示例2：汽车保险报价

**目标：**拨打4家保险公司的电话，利用每个报价进行下一步谈判。

```bash
# Ordering strategy: Start with the provider you care least about (get a baseline),
# end with your preferred provider (maximum leverage).

# Assistant instructions use dynamic variable placeholders:
#   "You are calling about auto insurance for a 2022 Toyota Camry.
#    {{#if best_quote}}
#    LEVERAGE: The best quote so far is {{best_quote}}/month
#    from {{best_company}}. Mention this and ask them to beat it.
#    {{/if}}"

# Sequential pattern — pass dynamic variables per call:
# Call 1 (baseline): no leverage vars → "What's your rate for [coverage details]?"
# Call 2: {"best_quote": "$180", "best_company": "Geico"}
# Call 3: {"best_quote": "$155", "best_company": "Progressive"}
# Call 4 (preferred): {"best_quote": "$145", "best_company": "StateFarm"}
```

## 类别4：多轮/跟进

任务有不同的阶段。第一轮是广泛的外联。结果进行分析，然后由人工批准筛选名单，第二轮进行深入的通话。

### 何时使用
- 有两个或更多不同的呼叫阶段
- 需要在轮次之间进行人工判断（审批关卡）
- 第二轮针对第一轮的筛选结果

### 关键模式
- 计划有明确的阶段：`round-1-calls`、`round-1-analysis`、`human-approval`、`round-2-calls`
- **人工审批关卡：** 通过Telegram/Slack向人工发送第一轮的结果+建议。等待他们的回复。
- 第二轮的助手可能有**完全不同的指令**

### 示例1：供应商选择

**目标：**根据基本标准筛选10个供应商，通过人工审批筛选前三名。

```bash
# Plan steps
[
  {"step_id": "setup", "description": "Create screening assistant + insight rubric", "sequence": 1},
  {"step_id": "round-1-calls", "description": "Screen all 10 vendors", "sequence": 2},
  {"step_id": "round-1-analysis", "description": "Rank and shortlist top 3", "sequence": 3},
  {"step_id": "human-approval", "description": "DM human with top 3, wait for approval", "sequence": 4},
  {"step_id": "round-2-setup", "description": "Create deep-dive assistant with technical questions", "sequence": 5},
  {"step_id": "round-2-calls", "description": "Deep-dive calls with approved vendors", "sequence": 6},
  {"step_id": "final-analysis", "description": "Final recommendation", "sequence": 7}
]

# Round 1 assistant: "Ask about pricing, lead time, minimum order, and general capabilities."
# Round 1 insight rubric: price_score, lead_time_days, meets_minimum, capability_match

# After Round 1 completes:
# → Rank by scores → DM human:
#   "Round 1 complete. Top 3 vendors:
#    1. VendorA — score 8.5, $12/unit, 2-week lead
#    2. VendorB — score 7.8, $14/unit, 1-week lead
#    3. VendorC — score 7.2, $11/unit, 3-week lead
#    Approve these for Round 2? Reply YES or adjust."

# Wait for human response (pause cron or check for reply)

# Round 2 assistant (different!): "Ask detailed technical questions:
#   API integration support? SLA guarantees? Disaster recovery?
#   Reference customers we can contact?"
# Round 2 insight rubric: api_support, sla_score, dr_plan, references_provided
```

### 示例2：候选人招聘

**目标：**通过电话筛选15位候选人（第一轮），筛选出5位（人工审批），进行详细面试（第二轮）。

```bash
# Round 1: Quick 5-minute screen — "Tell me about your background, why this role,
#   salary expectations, availability."
# Insight rubric: communication_score, experience_match, salary_in_range, enthusiasm

# → Rank → DM human with top 5 + scores
# → Human approves (or swaps in someone from position 6-7)

# Round 2: 15-minute deep dive — completely different assistant:
#   "Ask about: specific project experience with [TECH], how they handle conflict,
#    a time they failed and what they learned, questions they have for us."
# Different insight rubric: technical_depth, problem_solving, culture_fit, curiosity

# Track in memory:
python telnyx_api.py save-memory "<slug>" "rounds" '{
  "round_1": {"candidates": [...], "advanced": ["+1555...", "+1555..."]},
  "round_2": {"candidates": [...], "results": [...]}
}'
```

## 类别5：信息收集 → 行动

打电话收集信息，但任务不仅仅是报告 — 它**根据结果采取行动**。一旦找到您需要的信息，就停止搜索并采取行动。

### 何时使用

### 当您需要**找到**某些东西（可用性、时间、匹配项），然后**采取行动**（预订它、确认它）