---
name: context-recovery
description: 在会话压缩后，或者当需要继续会话但上下文信息丢失时，能够自动恢复工作状态。该功能支持 Discord、Slack、Telegram、Signal 以及其他受支持的聊天平台。
metadata: {"clawdbot":{"emoji":"🔄"}}
---

# 上下文恢复

在会话被压缩后，或者当需要继续对话但上下文缺失时，系统会自动恢复可用的工作上下文。该功能支持 Discord、Slack、Telegram、Signal 等平台。

**使用场景**：会话开始时上下文被截断；用户在没有提供详细信息的情况下提及之前的工作；或者出现会话压缩的提示。

---

## 触发条件

### 自动触发条件
- 会话以 `<summary>` 标签开头（检测到会话被压缩）
- 用户消息中包含会话压缩的提示信息，例如：“Summary unavailable”（摘要不可用）、“context limits”（上下文限制）或“truncated”（内容被截断）

### 手动触发条件
- 用户发送“continue”（继续）、“did this happen?”（发生了什么？）、“where were we?”（我们刚才在讨论什么？）或“what was I working on?”（我在做什么？）
- 用户提及“the project”（项目）、“the PR”（合并请求）、“the branch”（分支）或“the issue”（问题），但没有明确具体指代
- 用户表示之前有工作内容，但上下文不明确
- 用户询问“do you remember...?”（你记得吗？）或“we were working on...”（我们之前在讨论什么？）

---

## 执行流程

### 第一步：检测当前使用的通道

从运行时上下文中提取以下信息：
- `channel`：Discord、Slack、Telegram、Signal 等平台的通道名称
- `channelId`：具体的通道/对话 ID
- `threadId`：对于分层的对话（如 Slack 和 Discord 的线程），需要获取线程 ID

### 第二步：获取通道历史记录（自适应深度）

**初始获取：**
```
message:read
  channel: <detected-channel>
  channelId: <detected-channel-id>
  limit: 50
```

**自适应扩展逻辑：**
1. 从返回的消息中解析时间戳
2. 计算时间跨度：`newest_timestamp - oldest_timestamp`
3. 如果时间跨度小于 2 小时且消息数量小于等于限制值（`limit`）：
   - 再获取 50 条消息（如果平台支持 `before` 参数，则使用该参数）
   - 重复此步骤，直到时间跨度大于等于 2 小时或总消息数量大于等于 100 条
4. 最大获取 100 条消息（受令牌预算限制）

**针对分层对话的恢复机制（Slack/Discord）：**
```
# If threadId is present, fetch thread messages first
message:read
  channel: <detected-channel>
  threadId: <thread-id>
  limit: 50

# Then fetch parent channel for broader context
message:read
  channel: <detected-channel>
  channelId: <parent-channel-id>
  limit: 30
```

**解析内容：**
- 用户最近提出的请求
- 辅助系统最近的回复内容
- URL、文件路径、分支名称、合并请求（PR）编号
- 未完成的操作（用户提出但未完成的任务）
- 项目标识符和工作目录

### 第三步：获取会话日志（如果可用）

```bash
# Find most recent session files for this agent
SESSION_DIR=$(ls -d ~/.clawdbot-*/agents/*/sessions 2>/dev/null | head -1)
SESSIONS=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -3)

for SESSION in $SESSIONS; do
  echo "=== Session: $SESSION ==="
  
  # Extract user requests
  jq -r 'select(.message.role == "user") | .message.content[0].text // empty' "$SESSION" | tail -20
  
  # Extract assistant actions (look for tool calls and responses)
  jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text // empty' "$SESSION" | tail -50
done
```

### 第四步：检查共享内存中的信息

```bash
# Extract keywords from channel history (project names, PR numbers, branch names)
# Search memory for relevant entries
grep -ri "<keyword>" ~/clawd-*/memory/ 2>/dev/null | head -10

# Check for recent daily logs
ls -t ~/clawd-*/memory/202*.md 2>/dev/null | head -3 | xargs grep -l "<keyword>" 2>/dev/null
```

### 第五步：合成上下文

整理并生成结构化的摘要：

```markdown
## Recovered Context

**Channel:** #<channel-name> (<platform>)
**Time Range:** <oldest-message> to <newest-message>
**Messages Analyzed:** <count>

### Active Project/Task
- **Repository:** <repo-name>
- **Branch:** <branch-name>
- **PR:** #<number> — <title>

### Recent Work Timeline
1. [<timestamp>] <action/request>
2. [<timestamp>] <action/request>
3. [<timestamp>] <action/request>

### Pending/Incomplete Actions
- ⏳ "<quoted incomplete action>"
- ⏳ "<another incomplete item>"

### Key References
| Type | Value |
|------|-------|
| PR | #<number> |
| Branch | <name> |
| Files | <paths> |
| URLs | <links> |

### Last User Request
> "<quoted request that may not have been completed>"

### Confidence Level
- Channel context: <high/medium/low>
- Session logs: <available/partial/unavailable>
- Memory entries: <found/none>
```

### 第六步：缓存恢复的上下文

将恢复的上下文保存到内存中，以供后续使用：

```bash
# Write to daily memory file
MEMORY_FILE=~/clawd-*/memory/$(date +%Y-%m-%d).md

cat >> "$MEMORY_FILE" << EOF

## Context Recovery — $(date +%H:%M)

**Channel:** #<channel-name>
**Recovered context for:** <project/task summary>

### Key State
- <bullet points of critical context>

### Pending Items
- <incomplete actions>

EOF
```

这样可以在未来的会话压缩中保留上下文信息。

### 第七步：展示恢复的上下文

展示恢复的上下文，并提示用户：
> “上下文已恢复。您上次的请求是 [X]。该操作 [已完成/未完成]。您是否希望 [继续/重试/进一步说明]？”

---

## 各平台特定说明

### Discord
- 使用来自传入消息元数据的 `channelId`
- 公会通道可以访问完整的会话历史记录
- 对于分层对话，需要检查消息元数据中的 `threadId`
- 私人消息（DM）的历史记录可能有限

### Slack
- 使用 `channel` 参数和 Slack 通道 ID
- 分层对话的上下文需要 `threadId`，请务必先检查该信息
- 通过父通道可以获取完整的对话上下文
- 可能需要工作区级别的权限才能访问全部历史记录

### Telegram / Signal / 其他平台
- 使用相同的 `message:read` 接口
- 不同平台的历史记录深度可能有所不同
- 组内对话和私信的上下文可能存在差异

---

## 限制条件
- **强制要求**：在回复“数据不足”或询问补充信息之前，必须先执行上述恢复流程
- 自适应扩展深度：初始获取 50 条消息，最多扩展到 100 条
- 时间目标：尽可能捕获至少 2 小时的会话内容
- 会话日志的获取范围：最多获取最近 3 个会话的日志文件
- 内存缓存：将恢复的上下文追加到每日日志文件中，避免覆盖原有内容
- 如果恢复失败，需说明尝试了哪些操作以及哪些数据源无法获取

---

## 自动触发机制的检测

在会话开始时，系统会扫描是否存在会话压缩的提示信息：

```python
# Pseudocode for trigger detection
if message contains "<summary>":
    trigger_context_recovery()
elif message contains any of ["Summary unavailable", "context limits", "truncated", "compacted"]:
    trigger_context_recovery()
elif message matches continuation_patterns:
    # "continue", "where were we", "did this happen", etc.
    trigger_context_recovery()
```

**无需等待用户提问**——如果检测到会话被压缩，系统会主动恢复上下文并展示给用户。

---

## 示例

**场景**：会话开始时显示了压缩提示

```
User message: "<summary>Summary unavailable due to context limits...</summary>"
User message: "did this happen?"
```

**辅助系统的处理流程：**
1. 通过 `<summary>` 标签检测到会话被压缩
2. 发送请求：`message:read channel=discord channelId=1460342116516364533 limit=50`
3. 计算时间跨度：2.5 小时（足够的时间范围，无需进一步扩展）
4. 解析消息，找到用户最后的请求：“现在我来提取与 PR #137（Skills & Agents System）相关的编排决策…”
5. 检查会话日志，提取用户最近的请求内容
6. 将上下文摘要保存到 `memory/YYYY-MM-DD.md` 文件中
7. 回复用户：
> “上下文已恢复。您上次的请求是提取与 PR #137 相关的编排决策。由于上下文被截断，该操作未能完成。
>
> **恢复的上下文信息：**
> - PR #137：包含 15,053 个新增内容，涉及 91 个文件，存在合并冲突
> - 相关文件位置：`content/spec-skills-agents-system.md`（2,067 行）
> - 会话文件位置：`~/.clawdbot-duke-leto/archive/nexus-sessions/`（96 个文件）
>
> 您是否希望继续执行提取操作？**