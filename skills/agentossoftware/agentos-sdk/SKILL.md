# AgentOS SDK 技能文档

## 概述
AgentOS 是一个专为 AI 代理设计的完整责任管理基础设施。它提供了持久化存储、项目管理、看板功能、头脑风暴存储、活动日志记录、代理间通信以及自我进化机制。

**使用场景：** 当您需要存储数据、管理项目、跟踪任务、记录活动、与其他代理进行通信，或在会话之间持续优化代理行为时，均可使用 AgentOS。

## 🆕 代理操作指南
请阅读 `AGENT-OPS.md` 以获取在 AgentOS 上作为代理运行的完整操作指南。该指南涵盖以下内容：
- 内存组织（路径、标签、重要性）
- 项目管理（创建、更新、跟踪）
- 看板工作流程（任务、状态、优先级）
- 头脑风暴存储（想法、决策、学习成果）
- 日常操作（会话开始/结束检查清单）
- 自我进化机制

## 🆕 aos CLI - 完整的仪表盘控制
`aos` CLI 允许您完全控制 AgentOS 仪表盘：

```bash
# Memory
aos memory put "/learnings/today" '{"lesson": "verify first"}'
aos memory search "how to handle errors"

# Projects
aos project list
aos project create "New Feature" --status active

# Kanban
aos kanban add "Fix bug" --project <id> --status todo --priority high
aos kanban move <task-id> done

# Brainstorms
aos brainstorm add "Use WebSocket" --project <id> --type idea

# Activity logging
aos activity log "Completed API refactor" --project <id>

# Mesh communication
aos mesh send <agent> "Topic" "Message body"
```

运行 `aos help` 或 `aos <command>` 可查看详细使用说明。

## **推荐设置：黄金同步**  
为了获得最准确的仪表盘数据（包括内存信息和项目详情），请执行以下操作：
```bash
~/clawd/bin/agentos-golden-sync.sh
```

此操作会同步内存数据，并将每个项目的 Markdown 文件（`TASKS.md`、`IDEAS.md`、`CHANGELOG.md`、`CHALLENGES.md`）更新到数据库并显示在仪表板上。

## 快速入门

```bash
# Set environment variables
export AGENTOS_API_KEY="your-api-key"
export AGENTOS_BASE_URL="http://178.156.216.106:3100"  # or https://api.agentos.software
export AGENTOS_AGENT_ID="your-agent-id"

# Source the SDK
source /path/to/agentos.sh

# Store a memory
aos_put "/memories/today" '{"learned": "something important"}'

# Retrieve it
aos_get "/memories/today"

# Search semantically
aos_search "what did I learn today"
```

## 配置参数

| 参数 | 是否必填 | 说明 |
|---------|---------|-------------|
| `AGENTOS_API_KEY` | 是 | 来自 agentos.software 仪表板的 API 密钥 |
| `AGENTOS_BASE_URL` | 是 | API 端点（默认：`http://178.156.216.106:3100`） |
| `AGENTOS_AGENT_ID` | 是 | 该代理实例的唯一标识符 |

## 核心 API 功能

### aos_put - 存储数据
```bash
aos_put <path> <value_json> [options]

# Options (as env vars before call):
#   AOS_TTL=3600          # Expire after N seconds
#   AOS_TAGS='["tag1"]'   # JSON array of tags
#   AOS_IMPORTANCE=0.8    # 0-1 importance score
#   AOS_SEARCHABLE=true   # Enable semantic search

# Examples:
aos_put "/learnings/2026-02-04" '{"lesson": "Always verify before claiming done"}'
AOS_SEARCHABLE=true aos_put "/facts/solana" '{"info": "Solana uses proof of history"}'
AOS_TTL=86400 aos_put "/cache/price" '{"sol": 120.50}'
```

### aos_get - 获取数据
```bash
aos_get <path>

# Returns JSON: {"found": true, "path": "...", "value": {...}, "version_id": "...", "created_at": "..."}
# Or: {"found": false}

aos_get "/learnings/2026-02-04"
```

### aos_search - 智能搜索
```bash
aos_search <query> [limit] [path_prefix]

# Returns ranked results by semantic similarity
# Only searches memories marked as searchable=true

aos_search "what mistakes have I made" 10
aos_search "solana facts" 5 "/facts"
```

### aos_delete - 删除数据
```bash
aos_delete <path>

# Creates a tombstone version (soft delete, keeps history)
aos_delete "/cache/old-data"
```

### aos_list - 列出子节点
```bash
aos_list <prefix>

# Returns direct children under a path
aos_list "/learnings"
# → {"items": [{"path": "/learnings/2026-02-04", "type": "file"}, ...]}
```

### aos_glob - 模式匹配
```bash
aos_glob <pattern>

# Supports * and ** wildcards
aos_glob "/learnings/*"           # Direct children
aos_glob "/memories/**"           # All descendants
aos_glob "/projects/*/config"     # Wildcard segments
```

### aos_history - 版本历史记录
```bash
aos_history <path> [limit]

# Returns all versions of a memory (for time travel)
aos_history "/config/settings" 20
```

### aos_agents - 列出所有代理
```bash
aos_agents

# Returns all agent IDs in your tenant with memory counts
# Useful for discovering other agent instances
```

### aos_dump - 批量导出
```bash
aos_dump [agent_id] [limit]

# Export all memories for an agent (default: current agent)
aos_dump "" 500
```

## 自我进化框架
**有关完整的自我进化指南，请参阅 [SELF-EVOLUTION.md](./SELF-EVOLUTION.md)。**

AgentOS 通过以下方式帮助代理不断提升智能：
- **错误追踪**：避免重复相同错误
- **问题库**：将解决方案索引以供将来参考
- **任务前检查**：在行动前搜索相关学习内容
- **进度检查点**：防止内存压缩
- **验证日志**：确保任务确实完成

### 快速入门：自我进化
```bash
# Before any task: check past learnings
aos_before_action "deployment"

# After a mistake: document it
aos_mistake "What happened" "Root cause" "Lesson learned" "severity"

# After solving a problem: register it
aos_problem_solved "OAuth 401 Error" "JWT format mismatch" "Added JWT branch to auth" "auth,oauth"

# After completing work: save progress
aos_save_progress "Deployed API v2" "success" "JWT auth now working"

# Every 15-20 min: checkpoint context
aos_checkpoint "Building payment flow" "Stripe webhook incomplete" "Test mode works"

# At session start: restore context
aos_session_start

# Run the evolution checklist
aos_evolve_check
```

## 核心功能

| 功能 | 用途 |
|---------|---------|
| `aos_before_action` | 在执行操作前检查是否存在错误及解决方案 |
| `aos_mistake` | 记录失败原因及经验教训 |
| `aos_problem_solved` | 注册已解决的问题 |
| `aos_check_solved` | 搜索类似的已解决问题 |
| `aos_save_progress` | 记录已完成的任务（防止内存压缩） |
| `aos_checkpoint` | 每 15-20 分钟保存工作状态 |
| `aos_session_start` | 会话开始时恢复上下文 |
| `aos_verify_logged` | 记录验证结果 |
| `aos_daily_summary` | 查看当天的工作内容 |
| `aos_evolve_check` | 显示进化检查清单 |

### 推荐的内存结构
```
/self/
  identity.json       # Who am I? Core traits, values
  capabilities.json   # What can I do? Skills, tools
  preferences.json    # How do I prefer to work?
  
/learnings/
  YYYY-MM-DD.json     # Daily learnings
  mistakes/           # Documented failures
  successes/          # What worked well
  
/patterns/
  communication/      # How to talk to specific people
  problem-solving/    # Approaches that work
  tools/              # Tool-specific knowledge
  
/relationships/
  <person-id>.json    # Context about people I work with
  
/projects/
  <project-name>/     # Project-specific context
    context.json
    decisions.json
    todos.json

/reflections/
  weekly/             # Weekly self-assessments
  monthly/            # Monthly reviews
```

### 自我反思机制
完成重要任务后，请记录您的反思内容：
```bash
# After a mistake
aos_put "/learnings/mistakes/$(date +%Y-%m-%d)-$(uuidgen | cut -c1-8)" '{
  "type": "mistake",
  "what_happened": "I claimed a task was done without verifying",
  "root_cause": "Rushed to respond, skipped verification step",
  "lesson": "Always verify state before claiming completion",
  "prevention": "Add verification checklist to task completion flow",
  "severity": "high",
  "timestamp": "'$(date -Iseconds)'"
}' 

# Mark as searchable so you can find it later
AOS_SEARCHABLE=true AOS_TAGS='["mistake","verification","lesson"]' \
aos_put "/learnings/mistakes/..." '...'
```

### 自我改进循环
```bash
# 1. Before starting work, recall relevant learnings
aos_search "mistakes I've made with $TASK_TYPE" 5

# 2. After completing work, reflect
aos_put "/learnings/$(date +%Y-%m-%d)" '{
  "tasks_completed": [...],
  "challenges_faced": [...],
  "lessons_learned": [...],
  "improvements_identified": [...]
}'

# 3. Periodically consolidate learnings
aos_search "lessons from the past week" 20
# Then synthesize and store in /reflections/weekly/
```

## 实时同步（WebSocket）
当内存数据发生变化时，您可以接收实时更新：
```javascript
const ws = new WebSocket('ws://178.156.216.106:3100');

ws.onopen = () => {
  // Authenticate
  ws.send(JSON.stringify({
    type: 'auth',
    token: process.env.AGENTOS_API_KEY
  }));
  
  // Subscribe to updates for your agent
  ws.send(JSON.stringify({
    type: 'subscribe',
    agent_id: 'your-agent-id'
  }));
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);
  
  if (msg.type === 'memory:created') {
    console.log('New memory:', msg.path, msg.value);
  }
  
  if (msg.type === 'memory:deleted') {
    console.log('Memory deleted:', msg.path);
  }
};
```

### WebSocket 事件
| 事件类型 | 事件载荷 | 说明 |
|-------|---------|-------------|
| `memory:created` | `{agentId, path, versionId, value, tags, createdAt}` | 新数据已存储 |
| `memory:deleted` | `{agentId, path, versionId, deletedAt}` | 数据已被删除 |

## Webhook 集成
您可以注册 Webhook，在内存数据发生变化时接收 HTTP 回调：
```bash
# Register a webhook (via dashboard or API)
curl -X POST "$AGENTOS_BASE_URL/v1/webhooks" \
  -H "Authorization: Bearer $AGENTOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/agentos-webhook",
    "events": ["memory:created", "memory:deleted"],
    "agent_id": "your-agent-id",
    "path_prefix": "/learnings"
  }'
```

### Webhook 事件载荷
```json
{
  "event": "memory:created",
  "timestamp": "2026-02-04T09:50:00Z",
  "data": {
    "tenant_id": "...",
    "agent_id": "your-agent-id",
    "path": "/learnings/2026-02-04",
    "version_id": "...",
    "value": {"lesson": "..."},
    "tags": ["learning"],
    "created_at": "..."
  },
  "signature": "sha256=..."
}
```

## 速率限制与配额
| 操作类型 | 默认限制 |
|---------|---------------|
| 读取操作（get, list, glob, history） | 每分钟 60 次 |
| 写入操作（put, delete） | 每分钟 60 次 |
| 搜索操作 | 每分钟 20 次 |
| WebSocket 连接 | 每个租户最多 5 个连接 |

## 心跳上下文备份机制（至关重要）
**所有使用 AgentOS 的代理都必须在执行心跳操作时强制进行上下文备份。**

### 设计原因：
- AI 代理在会话压缩过程中可能会丢失上下文
- 仅依赖“每次任务后备份”策略是不可靠的——代理可能会忘记备份
- 通过心跳触发备份可确保上下文永远不会丢失

### Clawdbot 配置
在 `clawdbot.json` 中将心跳间隔设置为 10 分钟：
```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "10m",
        "model": "anthropic/claude-3-5-haiku-latest"
      }
    }
  }
}
```

### HEARTBEAT.md 模板
将以下内容添加到您的工作空间配置文件 `HEARTBEAT.md` 中：
```markdown
## 🔴 MANDATORY: Context Backup (DO THIS FIRST)

**On EVERY heartbeat, before anything else:**

1. **Read:** CONTEXT.md + today's daily notes + yesterday's daily notes
2. **Update CONTEXT.md** with:
   - Current timestamp
   - What's happening in the session
   - Recent accomplishments
   - Active tasks
   - Important conversation notes
3. **Update daily notes** (`memory/daily/YYYY-MM-DD.md`) with significant events
4. **Only then** proceed with other heartbeat checks

This is a HARD RULE. Never skip this step.
```

### AGENTS.md 规则
将以下内容添加到 `AGENTS.md` 中：
```markdown
## HARD RULE: Context Backup on EVERY Heartbeat

**Every single heartbeat MUST include a context backup.** No exceptions.

### Protocol (MANDATORY on every heartbeat)

1. **Read current state:**
   - CONTEXT.md
   - Today's daily notes (`memory/daily/YYYY-MM-DD.md`)
   - Yesterday's daily notes (for continuity)

2. **Update CONTEXT.md with:**
   - Current session focus
   - Recent accomplishments (what just happened)
   - Active tasks/threads
   - Important notes from conversation
   - Timestamp of update

3. **Update daily notes with:**
   - Significant events
   - Decisions made
   - Tasks completed
   - Context that might be needed later

4. **Only THEN proceed with other heartbeat tasks**

### Heartbeat Frequency
Heartbeats should run every **10 minutes** to ensure context is preserved frequently.

### The Golden Rule
**If you wouldn't remember it after a restart, write it down NOW.**
```

### AgentOS 集成
在每次心跳时将 `CONTEXT.md` 文件同步到 AgentOS：
```bash
# In your heartbeat routine, after updating local files:
aos_put "/context/current" "$(cat CONTEXT.md)"
aos_put "/daily/$(date +%Y-%m-%d)" "$(cat memory/daily/$(date +%Y-%m-%d).md)"
```

这样您的上下文数据既会在本地备份，也会被存储在 AgentOS 云端。

---

## 最佳实践

### 1. 使用有意义的路径名称
```bash
# Good - hierarchical, descriptive
aos_put "/projects/raptor/decisions/2026-02-04-architecture" '...'

# Bad - flat, ambiguous
aos_put "/data123" '...'
```

### 2. 为所有重要数据添加标签
```bash
AOS_TAGS='["decision","architecture","raptor"]' \
AOS_SEARCHABLE=true \
aos_put "/projects/raptor/decisions/..." '...'
```

### 3. 对临时数据设置过期时间（TTL）
```bash
# Cache that expires in 1 hour
AOS_TTL=3600 aos_put "/cache/api-response" '...'
```

### 4. 在请求前先进行搜索
```bash
# Before asking user for info, check memory
result=$(aos_search "user preferences for $TOPIC" 3)
```

### 5. 对重要变更进行版本控制
```bash
# Check history before overwriting
aos_history "/config/critical-setting" 5
# Then update
aos_put "/config/critical-setting" '...'
```

## 故障排除

### “未经授权”错误
- 确保 `AGENTOS_API_KEY` 设置正确
- 验证该密钥具有所需的权限（`memory:read`、`memory:write`、`search:read`）

### 搜索结果为空
- 确保数据已设置为 `searchable=true`
- 检查数据是否已成功嵌入（可能需要几秒钟）

### 速率限制错误
- 实施指数级退避策略
- 尽可能批量处理操作
- 检查 `X-PreAuth-RateLimit-Remaining` 请求头

## 代理间通信（Agent-to-Agent）
AgentOS 的 Mesh 功能支持 AI 代理之间的实时通信：

### Mesh 功能
```bash
# Send a message to another agent
aos_mesh_send <to_agent> <topic> <body>

# Get inbox messages (sent to you)
aos_mesh_inbox [limit]

# Get outbox messages (sent by you)
aos_mesh_outbox [limit]

# Check for locally queued messages (from daemon)
aos_mesh_pending

# Process queued messages (returns JSON, clears queue)
aos_mesh_process

# List all agents on the mesh
aos_mesh_agents

# Create a task for another agent
aos_mesh_task <assigned_to> <title> [description]

# List tasks assigned to you
aos_mesh_tasks [status]

# Get mesh overview stats
aos_mesh_stats

# Get recent activity feed
aos_mesh_activity [limit]

# Check mesh connection status
aos_mesh_status
```

### 示例：发送消息
```bash
# Send a message to another agent
aos_mesh_send "kai" "Project Update" "Finished the API integration, ready for review"

# Send with context
aos_mesh_send "icarus" "Research Request" "Please analyze the latest DeFi trends on Solana"
```

### 示例：处理接收到的消息
```bash
# Check if there are pending messages
aos_mesh_pending

# Process and respond to messages
messages=$(aos_mesh_process)
echo "$messages" | jq -r '.[] | "From: \(.from) - \(.topic)"'

# Respond to each message
aos_mesh_send "kai" "Re: Project Update" "Thanks for the update, looks good!"
```

### 实时消息处理守护进程
要实时接收消息，请运行相应的守护进程：
```bash
node ~/clawd/bin/mesh-daemon.mjs
```

该守护进程通过 WebSocket 连接并接收消息以进行后续处理。

### Mesh 事件（WebSocket）
| 事件类型 | 事件载荷 | 说明 |
|-------|---------|-------------|
| `mesh:message` | `{fromAgent, toAgent, topic, body, messageId}` | 收到新消息 |
| `mesh:task_update` | `{taskId, assignedTo, title, status}` | 任务状态发生变化 |

### CLI 快捷方式
还提供了一个独立的 CLI 工具：
```bash
~/clawd/bin/mesh status    # Connection status
~/clawd/bin/mesh pending   # List pending messages
~/clawd/bin/mesh send <to> "<topic>" "<body>"
~/clawd/bin/mesh agents    # List agents
```

## API 参考
完整的 OpenAPI 规范请访问：`$AGENTOS_BASE_URL/docs`

---

*AgentOS — 为不断进化的 AI 代理提供持久化存储和实时通信功能*