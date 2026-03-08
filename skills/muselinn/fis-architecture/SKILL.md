---
name: fis-architecture
description: 使用 JSON 票据和 A2A 协调机制来编排多代理工作流程。适用于在 CyberMao（主代理）与 Worker 代理（工程师/研究员/撰稿人）之间分配任务的情况。
metadata:
  openclaw:
    emoji: 🏗️
    always: false
homepage: https://github.com/linn/fis-architecture
---
# FIS Architecture 3.2 Pro

这是一个多代理工作流框架，用于实现**CyberMao（主节点）**与**Worker（工作节点）**之间的协作，通过JSON工单和Discord论坛帖子进行沟通。

---

## 适用场景

**在以下情况下使用FIS：**
- 当CyberMao需要将复杂任务委托给专门的Worker时
- 任务需要特定的领域知识（如编码、研究或写作）
- 需要在多个会话中跟踪任务进度
- 多步骤工作流需要代理之间的协同

**代理角色：**
| 角色 | 代理ID | 专长 |
|------|----------|-----------|
| **架构师** | `main` | 协调、任务分配、用户沟通 |
| **编码** | `engineer` | Python编程、gprMax工具使用、算法开发、数据分析 |
| **研究** | `researcher` | 理论研究、文献查阅、仿真规划 |
| **写作** | `writer` | 文档编写、LaTeX格式处理、数据可视化 |

---

## Discord机器人权限要求

每个代理的Discord机器人必须在Discord服务器中配置以下权限。否则，创建帖子和发送消息的操作将会失败。

**必需的机器人权限：**
- **发送消息** — 在频道和帖子中回复
- **在帖子中发送消息** — 在论坛帖子内发布内容
- **创建公开帖子** — 程序化创建新的论坛帖子
- **读取消息历史** — 读取帖子上下文
- **嵌入链接** — 在报告中嵌入链接
- **上传文件** — 上传交付成果

**配置方法：**
1. 进入Discord服务器设置 → 角色管理
2. 为每个机器人角色（CyberMao、Researcher、Engineer、Writer）启用上述权限
3. 确保每个论坛频道都授予相关机器人角色这些权限

**验证方法：**
```json
{ "action": "threadCreate", "channelId": "<forum_channel_id>", "name": "Permission Test" }
```
如果机器人缺少这些权限，`discord`工具会返回错误信息。

---

## 工具配置

| 工具 | 用途 | 路径 |
|------|---------|------|
| `fis_lifecycle_pro.py` | 管理工单的生命周期（创建/更新/完成/列表） | `scripts/fis_lifecycle_pro.py` |
| `fis_coordinator.py` | 生成任务委托模板（仅限CyberMao使用） | `scripts/fis_coordinator.py` |
| `fis_worker_toolkit.py` | 创建子代理、生成报告（仅限Worker使用） | `scripts/fis_worker_toolkit.py` |

**Python环境要求：** 需要Python 3.8及以上版本，并且仅使用标准库（无需外部依赖）。

---

## 核心工作流程

### 第1步：CyberMao委托任务

```bash
# Generate ticket + Thread template + A2A command
python3 scripts/fis_coordinator.py delegate \
  --agent engineer \
  --task "Implement GPR signal filter" \
  --forum coding
```

**输出：**
- 工单ID：`TASK_YYYYMMDD_XXX_AGENT`
- 帖子模板内容
- 用于通知Worker的`sessions_send`命令

### 第2步：CyberMao创建论坛帖子

使用`discord`工具在相应的论坛频道中创建一个帖子：

```json
{
  "action": "threadCreate",
  "channelId": "<forum_channel_id>",
  "name": "TASK_xxx: Implement GPR signal filter"
}
```

系统会返回新的帖子ID，然后使用该ID通知Worker：

```bash
python3 scripts/fis_coordinator.py notify \
  --ticket-id TASK_xxx \
  --thread-id <new_thread_id>
```

执行`sessions_send`命令以通知Worker。

### 第3步：Worker执行任务

```bash
# Check ticket
python3 scripts/fis_lifecycle_pro.py list

# Update status
python3 scripts/fis_lifecycle_pro.py status \
  --ticket-id TASK_xxx --status doing

# Optional: Spawn sub-agent for complex sub-tasks
python3 scripts/fis_worker_toolkit.py spawn \
  --parent-ticket TASK_xxx \
  --subtask "Analyze algorithm complexity"
```

Worker使用`discord`工具在论坛帖子中回复：

```json
{
  "action": "threadReply",
  "channelId": "<thread_id>",
  "content": "Task received. Starting execution."
}
```

### 第4步：Worker完成任务并报告

```bash
# Generate completion report
python3 scripts/fis_worker_toolkit.py report \
  --parent-ticket TASK_xxx \
  --summary "Successfully implemented GPR filter" \
  --deliverables filter.py test_results.json
```

执行`sessions_send`命令以通知CyberMao。

### 第5步：CyberMao完成任务

```bash
# View report
python3 scripts/fis_coordinator.py report --ticket-id TASK_xxx

# Mark complete
python3 scripts/fis_lifecycle_pro.py complete --ticket-id TASK_xxx
```

将帖子归档，并在#daily-chat频道中向用户报告任务完成情况。

---

## 架构原理

**关键原则：**
1. **双向通信** — CyberMao通过`sessions_send`命令与Worker交互，Worker完成任务后进行反馈
2. **工单跟踪** — 所有任务都通过`fis-hub/`目录下的JSON工单进行管理
3. **程序化创建帖子** — CyberMao通过`discord`工具的`threadCreate`功能创建论坛帖子
4. **子代理在后台运行** — 使用`mode="run"`模式启动子代理，不会创建新的帖子

---

## 命令参考

### `fis_lifecycle_pro.py`

```bash
# Create ticket
python3 scripts/fis_lifecycle_pro.py create \
  --agent engineer --task "Description" --channel-type coding

# Update status (todo/doing/done)
python3 scripts/fis_lifecycle_pro.py status \
  --ticket-id TASK_xxx --status doing --note "Progress update"

# Mark complete
python3 scripts/fis_lifecycle_pro.py complete --ticket-id TASK_xxx

# List active tickets
python3 scripts/fis_lifecycle_pro.py list

# Archive old tickets
python3 scripts/fis_lifecycle_pro.py archive
```

### `fis_coordinator.py`（仅限CyberMao使用）

```bash
# Delegate and generate templates
python3 scripts/fis_coordinator.py delegate \
  --agent researcher --task "GPR theory analysis" --forum theory

# Notify Worker after Thread is created
python3 scripts/fis_coordinator.py notify \
  --ticket-id TASK_xxx --thread-id <discord_thread_id>

# View detailed report
python3 scripts/fis_coordinator.py report --ticket-id TASK_xxx
```

### `fis_worker_toolkit.py`（仅限Worker使用）

```bash
# Spawn sub-agent (background, no Thread)
python3 scripts/fis_worker_toolkit.py spawn \
  --parent-ticket TASK_xxx --subtask "Complex sub-task description"

# Generate completion report
python3 scripts/fis_worker_toolkit.py report \
  --parent-ticket TASK_xxx \
  --summary "Completion summary" \
  --deliverables file1.py file2.json
```

---

## 论坛频道映射

| 类别 | 论坛频道 | 执行任务的Worker | 使用的工具标志 |
|----------|--------------|--------|-----------|
| 研究 | 🔬-theory-derivation | @Researcher | `--forum theory` |
| 研究 | 📊-gpr-simulation | @Researcher | `--forum simulation` |
| 开发 | 💻-coding | @Engineer | `--forum coding` |
| 写作 | 📝-drafts | @Writer | `--forum drafts` |

---

## 错误处理

**如果工单创建失败：**
- 检查Python版本：`python3 --version`（需3.8及以上）
- 确认`fis-hub/`目录存在且可写入
- 检查磁盘空间是否充足

**如果帖子创建失败：**
- 确认机器人具有在目标论坛频道中创建公开帖子的权限
- 检查`channelId`是否指向论坛频道（而非普通文本频道）
- 确认机器人是服务器的成员并具有正确的角色权限

**如果双向通信失败：**
- 检查`openclaw.json`文件中是否设置了`agentToAgent.enabled: true`
- 确认Worker的代理ID在允许列表中
- 检查Worker的会话是否处于活动状态

**如果子代理创建失败：**
- 确保使用了`mode="run"`模式（而非`mode="session"`）
- 检查任务描述是否清晰明确

---

## 质量标准
1. **每个任务对应一个工单** — 工单ID不可重复使用
2. **必须更新状态** — Worker必须更新任务状态（待办 → 进行中 → 完成）
3. **每个任务对应一个帖子** — 每个任务都会在论坛中创建一个专属帖子
4. **双向确认** — 必须通过`sessions_send`命令确认接收任务
5. **任务完成后归档帖子** — 完成任务后归档相关帖子

---

## 配置要求

配置文件位于`~/.openclaw/openclaw.json`中：

```json
{
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["main", "researcher", "engineer", "writer"]
    }
  }
}
```

---

## 测试

### 快速双向通信测试

```python
# Test connectivity
sessions_send(sessionKey="engineer", message="A2A test")
```

### 帖子创建测试

```json
{ "action": "threadCreate", "channelId": "<forum_channel_id>", "name": "FIS Test Thread" }
```

### 完整工作流测试

```bash
# 1. Create task
python3 scripts/fis_coordinator.py delegate \
  --agent researcher --task "Test task" --forum theory

# 2. Create Forum Thread via discord tool threadCreate

# 3. Notify Worker with Thread ID
python3 scripts/fis_coordinator.py notify \
  --ticket-id TASK_xxx --thread-id <thread_id>

# 4. Execute A2A command

# 5. Complete
python3 scripts/fis_lifecycle_pro.py complete --ticket-id TASK_xxx
```

---

*FIS 3.2 Pro | 多代理工作流框架*