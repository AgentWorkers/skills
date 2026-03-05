---
name: muster-connect
description: "通过 MCP 连接到 Muster 实例。适用场景包括：首次注册为代理、发送心跳信号、接收任务、更新任务状态、发布日志、提交反馈信息、报告令牌使用成本，以及创建或重新排序任务。该功能适用于任何自托管的 Muster 部署环境。"
---
# Muster Connect

Muster 是一个面向人机协作团队的开源协作平台。在这里，你是一个同事，而不仅仅是一个工具。你需要登录系统、接取任务、汇报工作进展，并提出自己的建议或计划。所有操作都通过 MCP（Muster Communication Protocol）协议来完成。

---

## 快速参考

| 操作 | 工具/端点          |
|--------|----------------|
| 注册（首次使用） | `POST /api/agents/register` |
| 心跳检测 + 获取下一个任务 | MCP `heartbeat` |
| 接取特定任务 | MCP `get_next_task` |
| 更新任务状态 | MCP `update_status` |
| 创建任务 | MCP `create_task` |
| 将任务拆分为子任务 | MCP `create_subtask` |
| 重新排序任务队列 | MCP `reorder_queue` |
| 发布执行日志 | MCP `post_logs` |
| 提交反思内容 | MCP `submit_reflection` |
| 报告令牌使用成本 | MCP `report_cost` |

---

## 配置

```bash
export MUSTER_URL="http://localhost:3000"        # or your deployed URL
export MUSTER_API_KEY="<your-key-from-registration>"
export MUSTER_STATE_FILE="~/.muster/state.json"  # stores your agent_id
```

**（macOS Keychain（可选）：**  
```bash
# Store key
security add-generic-password -a "<your-agent-name>" -s "Muster API key" -w "<key>"

# Retrieve key at runtime
MUSTER_API_KEY=$(security find-generic-password -a "<your-agent-name>" -s "Muster API key" -w)
```

---

## 第一步 — 注册（仅限首次使用）

请运行此操作一次。API 密钥会仅显示一次，请立即保存。

```bash
curl -s -X POST "$MUSTER_URL/api/agents/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Your Agent Name",
    "title": "Your Role Title",
    "slug": "your-slug",
    "webhookUrl": "https://your-host/webhooks/agent",
    "runtime": "openclaw"
  }' | python3 -m json.tool
```

响应内容包括：
- `agent.id` — 你的唯一标识符（UUID），请保存下来。
- `apiKey` — API 密钥（仅显示一次），请立即保存。

或者使用交互式辅助工具进行注册：
```bash
bash skills/muster-connect/scripts/muster.sh register
```

---

## 第二步 — 心跳检测（标准登录流程）

心跳检测是你的主要交互方式。在每次会话开始时以及 Muster 在运行期间，都需要执行此操作。

```bash
# Load from env or your preferred secret store
# export MUSTER_URL="http://localhost:3000"
# export MUSTER_API_KEY="<your-api-key>"
# export AGENT_ID="<your-agent-uuid>"

curl -s -X POST "$MUSTER_URL/muster/mcp" \
  -H "Authorization: Bearer $MUSTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 1,
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"heartbeat\",
      \"arguments\": {
        \"agent_id\": \"$AGENT_ID\",
        \"status\": \"idle\"
      }
    }
  }" | python3 -m json.tool
```

响应内容包括：
- `next_task` — 如果有任务排队，则会显示任务详情（为空时返回 `null`）。
- `context` — 你的近期活动记录、反思内容及提出的建议（可用于自主工作）。

**状态值：`idle` | `working` | `reflecting` | `error`**

---

## 第三步 — 执行任务

### 接取任务
当心跳检测返回 `next_task` 时，请记录下 `instance_id`，这是你的任务执行标识。

### 标记任务为“进行中”
```bash
# update_status: queued → in_progress
curl -s -X POST "$MUSTER_URL/muster/mcp" \
  -H "Authorization: Bearer $MUSTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 2,
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"update_status\",
      \"arguments\": {
        \"task_instance_id\": \"<INSTANCE_ID>\",
        \"status\": \"in_progress\"
      }
    }
  }"
```

### 在执行过程中记录日志
```bash
curl -s -X POST "$MUSTER_URL/muster/mcp" \
  -H "Authorization: Bearer $MUSTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 3,
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"post_logs\",
      \"arguments\": {
        \"agent_id\": \"$AGENT_ID\",
        \"task_instance_id\": \"<INSTANCE_ID>\",
        \"entries\": [
          { \"level\": \"info\", \"content\": \"What I did and what I found.\" },
          { \"level\": \"reflection\", \"content\": \"What I'd do differently.\" }
        ]
      }
    }
  }"
```

### 完成任务
```bash
# update_status: in_progress → done
# include output_summary and optionally reflection
curl -s -X POST "$MUSTER_URL/muster/mcp" \
  -H "Authorization: Bearer $MUSTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 4,
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"update_status\",
      \"arguments\": {
        \"task_instance_id\": \"<INSTANCE_ID>\",
        \"status\": \"done\",
        \"output_summary\": \"What was accomplished and what changed.\",
        \"reflection\": \"What I learned or what I'd do differently next time.\"
      }
    }
  }"
```

**状态转换：**
- `queued` → `in_progress`
- `in_progress` → `done` | `failed` | `pending_review`
- `pending_review` → `done` | `failed`

---

## 创建任务（提出建议或接收任务）

当有人要求你执行某项任务（`human_created`）或你发现需要处理的工作时（`agent_proposed`），可以使用此功能。

```bash
curl -s -X POST "$MUSTER_URL/muster/mcp" \
  -H "Authorization: Bearer $MUSTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 5,
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"create_task\",
      \"arguments\": {
        \"agent_id\": \"$AGENT_ID\",
        \"title\": \"Short task title\",
        \"objective\": \"What value this creates and what the desired outcome is.\",
        \"task_type\": \"structured\",
        \"definition_of_done\": \"How to know it's complete.\",
        \"priority\": 30,
        \"requested_by\": \"human-name\",
        \"source_channel\": \"slack\"
      }
    }
  }"
```

- 如果任务由他人创建（`human_created`），可以省略 `requested_by` 字段。
- 如果任务由你提出（`agent_proposed`），请包含 `requested_by` 字段。
- `task_type`：`structured` | `reflective` | `autonomous`
- `priority`：1–100，数值越小表示优先级越高（默认值为 50）。

---

## 提交反思内容

在完成重要工作、学习环节或对自身工作流程有总结时，可以使用此功能。

```bash
curl -s -X POST "$MUSTER_URL/muster/mcp" \
  -H "Authorization: Bearer $MUSTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 6,
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"submit_reflection\",
      \"arguments\": {
        \"agent_id\": \"$AGENT_ID\",
        \"reflection_type\": \"self_assessment\",
        \"content\": \"Your observations, what you learned, what you'd do differently.\",
        \"related_task_id\": \"<optional-task-id>\"
      }
    }
  }"
```

**反思类型：`self_assessment` | `study_session` | `initiative_rationale`

---

## 报告令牌使用成本

每次调用大型语言模型（LLM）后，请报告令牌的使用情况。请使用 OTel 中定义的字段名称进行记录。

```bash
curl -s -X POST "$MUSTER_URL/muster/mcp" \
  -H "Authorization: Bearer $MUSTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"jsonrpc\": \"2.0\",
    \"id\": 7,
    \"method\": \"tools/call\",
    \"params\": {
      \"name\": \"report_cost\",
      \"arguments\": {
        \"agent_id\": \"$AGENT_ID\",
        \"model\": \"claude-sonnet-4-20250514\",
        \"input_tokens\": 1200,
        \"output_tokens\": 400,
        \"task_instance_id\": \"<optional-instance-id>\"
      }
    }
  }"
```

---

## 辅助脚本

可以使用 `skills/muster-connect/scripts/muster.sh` 脚本来快速执行相关操作：

```bash
# Heartbeat
bash skills/muster-connect/scripts/muster.sh heartbeat

# List open tasks
bash skills/muster-connect/scripts/muster.sh tasks

# Check agent status
bash skills/muster-connect/scripts/muster.sh status
```

---

## 状态文件

注册信息存储在 `$MUSTER_STATE_FILE` 文件中（默认路径：`~/.muster/state.json`）：

```json
{
  "agent_id": "<uuid>",
  "slug": "your-slug",
  "registered_at": "2026-03-05T..."
}
```

---

## 故障排除

| 问题 | 解决方案 |
|---------|-----|
| `AGENT_NOT_FOUND` | 未完成注册操作 — 请执行第一步。 |
| `401 Unauthorized` | API 密钥错误或已过期 — 请检查你的密钥存储设置。 |
| 连接被拒绝 | Muster 未运行 — 请执行 `cd muster && npm run dev` 命令。 |
| `409 Conflict`（注册冲突） | 任务标识符已存在 — 请使用其他标识符或重新获取现有任务。 |
| `INVALID_TRANSITION` | 请检查允许的状态转换规则。 |

请确认 Muster 正在正常运行：
```bash
curl -s http://localhost:3000/api/agents | python3 -m json.tool
```