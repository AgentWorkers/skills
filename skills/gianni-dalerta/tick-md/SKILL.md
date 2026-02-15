# 多代理协调系统（Tick Multi-Agent Coordination）

通过结构化的Markdown文件来协调人类代理和AI代理之间的工作。用户可以自然地与你交互，而你则负责在TICK.md文件中透明地管理各项任务。

## 安装

**前提条件**：你的环境中已经安装并配置好了Tick命令行工具（CLI）和MCP服务器。

**首次设置？** 请参阅`INSTALL.md`以获取针对特定编辑器的安装说明。

**快速检查**：
```bash
# Verify CLI is available
tick --version

# Check if TICK.md exists in project
ls TICK.md

# If not, initialize
tick init
```

## 核心概念

**Tick协议**：基于Git的任务协调机制，通过TICK.md文件实现：
- **人类可读**：使用标准Markdown格式，并结合YAML格式
- **机器可解析**：结构化的数据格式，便于工具处理
- **Git支持**：具备完整的版本控制和审计追踪功能
- **本地优先**：无需依赖云服务

## 快速入门

### 检查Tick是否已初始化
```bash
ls TICK.md
```

### 如果未初始化
```bash
tick init
```

### 获取当前状态
```bash
tick status
```

## 常见工作流程

### 1. 用户请求你执行某项任务

**用户**：“你能重构认证系统吗？”

**你的操作**：
```bash
# 1. Create task
tick add "Refactor authentication system" --priority high --tags backend,security

# 2. Register yourself (first time only)
tick agent register @your-name --type bot --roles "engineer,refactoring"

# 3. Claim the task
tick claim TASK-XXX @your-name

# 4. Work on it (do the actual work)

# 5. Add progress comments
tick comment TASK-XXX @your-name --note "Analyzing current auth flow"
tick comment TASK-XXX @your-name --note "Refactored to use JWT tokens"

# 6. Mark complete
tick done TASK-XXX @your-name
```

### 2. 用户询问项目进度

**用户**：“我们正在处理哪些任务？”

```bash
# Get comprehensive status
tick status

# Or filter and list tasks
tick list --status in_progress
tick list --claimed-by @bot-name
```

**为用户自然地总结任务进度。**

### 3. 与其他代理协调

**用户**：“其他代理完成任务了吗？”

```bash
# Check overall status
tick status

# List agents and their work
tick agent list --verbose

# Validate the project
tick validate
```

### 4. 分解复杂任务

**用户**：“需要制作一个包含图表和数据导出的用户仪表板。”

**你的操作**：
```bash
# Create parent task
tick add "Build user dashboard" --priority high --tags frontend

# Create subtasks with dependencies
tick add "Design dashboard layout" --priority high --tags frontend,design
tick add "Implement data charts" --priority medium --tags frontend,charts --depends-on TASK-XXX
tick add "Add CSV export" --priority low --tags frontend,export --depends-on TASK-XXX

# Visualize dependencies
tick graph
```

## 命令参考

### 项目管理
```bash
tick init                          # Initialize new project
tick status                        # View project overview
tick list                          # List tasks with filters
tick graph                         # Visualize dependencies
tick watch                         # Monitor changes in real-time
tick validate                      # Check for errors
tick sync --push                   # Commit and push to git
```

### 任务操作
```bash
tick add "Task title" \
  --priority high \                # urgent|high|medium|low
  --tags backend,api \             # Comma-separated tags
  --assigned-to @agent \           # Assign to agent
  --depends-on TASK-001 \          # Dependencies
  --estimated-hours 4              # Time estimate

tick claim TASK-001 @agent         # Claim task (sets in_progress)
tick release TASK-001 @agent       # Release task (back to todo)
tick done TASK-001 @agent          # Complete task
tick reopen TASK-001 @agent        # Reopen completed task
tick delete TASK-001               # Delete a task
tick comment TASK-001 @agent \     # Add note
  --note "Progress update"
tick edit TASK-001 \               # Direct field edit
  --title "New title" \
  --priority high \
  --status in_progress
```

### 修正与恢复
```bash
tick reopen TASK-001 @agent        # Reopen completed task
tick reopen TASK-001 @agent \      # Reopen and re-block dependents
  --re-block

tick delete TASK-001               # Delete task, cleans up deps
tick delete TASK-001 --force       # Delete even if has dependents

tick edit TASK-001 --title "X"     # Change title
tick edit TASK-001 --priority high # Change priority
tick edit TASK-001 --status todo   # Change status directly
tick edit TASK-001 --tags a,b,c    # Replace tags
tick edit TASK-001 --add-tag new   # Add tag
tick edit TASK-001 --remove-tag old # Remove tag
tick edit TASK-001 \               # Edit dependencies
  --depends-on TASK-002,TASK-003

tick undo                          # Undo last tick operation
tick undo --dry-run                # Preview what would be undone
```

### 批量操作
```bash
tick import tasks.yaml             # Import tasks from YAML file
tick import - < tasks.yaml         # Import from stdin
tick import tasks.yaml --dry-run   # Preview import

tick batch start                   # Begin batch mode (no auto-commit)
tick batch status                  # Check batch status
tick batch commit                  # Commit all batched changes
tick batch abort                   # Discard batched changes
```

### 高级任务列表
```bash
tick list                          # All tasks, grouped by status
tick list --status blocked         # Only blocked tasks
tick list --priority urgent        # High-priority tasks
tick list --assigned-to @alice     # Tasks for specific agent
tick list --tag backend            # Tasks with tag
tick list --json                   # JSON output for scripts
```

### 依赖关系可视化
```bash
tick graph                         # ASCII dependency tree
tick graph --format mermaid        # Mermaid flowchart
tick graph --show-done             # Include completed tasks
```

### 实时监控
```bash
tick watch                         # Watch for changes
tick watch --interval 10           # Custom polling interval
tick watch --filter in_progress    # Only show specific status
```

### 代理管理
```bash
tick agent register @name \        # Register new agent
  --type bot \                     # human|bot
  --roles "dev,qa" \               # Comma-separated roles
  --status idle                    # working|idle|offline

tick agent list                    # List all agents
tick agent list --verbose          # Detailed info
tick agent list --type bot         # Filter by type
tick agent list --status working   # Filter by status
```

## MCP工具（替代CLI）

如果使用Model Context Protocol，可以使用以下工具代替CLI命令：

### 状态与检查
- `tick_status`：获取项目状态（代理、任务、进度）
- `tick_validate`：验证TICK.md文件的结构
- `tick_agent_list`：列出代理列表（可选过滤条件）

### 任务管理
- `tick_add`：创建新任务
- `tick_claim`：将任务分配给代理
- `tick_release`：释放被代理占用的任务
- `tick_done`：完成任务（自动解除依赖关系）
- `tick_comment`：为任务添加备注

### 修正与恢复
- `tick_reopen`：重新打开已完成的任务
- `tick_delete`：删除任务
- `tick_edit`：直接编辑任务字段（绕过状态机）
- `tick_undo`：撤销上一次操作

### 代理管理
- `tick_agent_register`：注册新代理

**MCP示例**：
```javascript
// Create task via MCP
await tick_add({
  title: "Refactor authentication",
  priority: "high",
  tags: ["backend", "security"],
  assignedTo: "@bot-name"
})

// Claim it
await tick_claim({
  taskId: "TASK-023",
  agent: "@bot-name"
})
```

## 最佳实践

### 1. 首先进行自然对话

✅ **正确做法**：用户提出请求时，你自动创建相应任务。
❌ **错误做法**：让用户手动创建任务。

### 2. 始终使用代理的名称

**注册一次后**：
```bash
tick agent register @your-bot-name --type bot --roles "engineer"
```

**之后始终一致地使用该名称**：
```bash
tick claim TASK-001 @your-bot-name
tick done TASK-001 @your-bot-name
```

### 3. 在评论中提供上下文信息

```bash
# ✅ Good - explains what and why
tick comment TASK-005 @bot --note "Switched from REST to GraphQL for better type safety and reduced over-fetching"

# ❌ Bad - too vague
tick comment TASK-005 @bot --note "Updated API"
```

### 4. 分解大型任务

将复杂任务拆分为包含依赖关系的子任务：
```bash
tick add "Set up CI/CD pipeline" --priority high
tick add "Configure GitHub Actions" --depends-on TASK-010
tick add "Add deployment scripts" --depends-on TASK-011
tick add "Set up staging environment" --depends-on TASK-011
```

### 5. 在分配任务前检查状态

```bash
# Make sure task exists and isn't claimed
tick status

# Then claim
tick claim TASK-XXX @your-name
```

## 理解TICK.md文件的结构

该文件包含三个部分：

1. **前置内容**（YAML）：项目元数据
2. **代理列表**（Markdown）：哪些代理正在处理哪些任务
3. **任务块**（YAML + Markdown）：包含任务详情和历史记录的详细信息

**示例**：
```markdown
---
project: my-app
schema_version: "1.0"
next_id: 5
---

# Agents

| Name | Type | Roles | Status | Working On |
|------|------|-------|--------|------------|
| @alice | human | owner | working | TASK-003 |
| @bot | bot | engineer | idle | - |

# Tasks

\```yaml
id: TASK-001
title: 构建认证系统
status: done
priority: high
claimed_by: null
# ... 其他字段
history:
  - ts: 2026-02-07T10:00:00Z
    who: @bot
    action: created
  - ts: 2026-02-07T14:00:00Z
    who: @bot
    action: done
\```

Implemented JWT-based authentication with token refresh...
```

## 高级功能

### 自动解除依赖关系

当你完成任务后，相关依赖任务会自动解除阻塞：
```bash
# TASK-002 depends on TASK-001
# TASK-002 status: blocked

tick done TASK-001 @bot
# TASK-002 automatically changes to: todo
```

### 检测循环依赖关系

系统会自动检测并处理循环依赖关系：
```bash
tick validate
# Error: Circular dependency detected: TASK-001 → TASK-002 → TASK-003 → TASK-001
```

### 智能提交信息

提交代码时使用描述性信息，便于理解变更内容：
```bash
tick sync --push
# Automatically generates: "feat: complete TASK-001, TASK-002; update TASK-003"
```

### 重新打开已完成的任务

如果任务被错误地标记为已完成，可以重新打开它：
```bash
tick reopen TASK-001 @bot
# Sets status back to in_progress, records in history

tick reopen TASK-001 @bot --re-block
# Also re-blocks any tasks that depend on this one
```

### 修正错误

及时发现并修正错误：
```bash
# Undo the last tick operation
tick undo

# Preview what would be undone first
tick undo --dry-run

# Direct field edits (bypasses state machine)
tick edit TASK-001 --status todo --priority urgent
```

### 批量操作

对于多个更改，可以一次性提交：
```bash
tick batch start
# Now make multiple changes...
tick add "Task 1" --priority high
tick add "Task 2" --priority medium
tick claim TASK-001 @bot
# ...
tick batch commit   # Single commit for all changes
# Or: tick batch abort  # Discard all changes
```

### 实时监控

系统提供实时任务状态监控功能：
```bash
tick watch
# [10:23:45] ✓ Added: TASK-015 - Implement user search
# [10:24:12] 🔒 TASK-015 claimed by @bot
# [10:26:33] ⟳ TASK-015: in_progress → done
```

## 快速参考卡

```
Workflow:      init → add → claim → work → comment → done → sync
Essential:     status | add | claim | done | list | graph
Corrections:   reopen | delete | edit | undo
Bulk:          import | batch start/commit/abort
Coordination:  agent register | agent list | validate | watch
Git:           sync --pull | sync --push
```

## 关键提示

1. **用户与你交互，而不是直接与Tick系统交互**
2. **你负责透明地维护TICK.md文件的内容**
3. **仪表板仅用于查看信息，而非主要交互工具**
4. **始终一致地使用代理的名称**
5. **经常添加评论以展示任务进度**
6. **同步前务必验证文件内容**
7. **在分配任务前检查任务状态**
8. **将复杂任务分解为子任务**

## 资源

- **GitHub仓库**：https://github.com/your-org/tick-md
- **文档**：https://tick-md.dev/docs
- **CLI包（npm）**：https://npmjs.com/package/tick-md
- **MCP服务器包（npm）**：https://npmjs.com/package/tick-mcp-server

## 许可证

MIT许可证