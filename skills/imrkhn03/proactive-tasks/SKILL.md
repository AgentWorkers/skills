---
name: proactive-tasks
description: 这是一个主动的目标和任务管理系统。适用于目标管理、将项目分解为具体任务、跟踪进度，或自主完成工作目标。该系统使代理能够在任务执行过程中主动采取行动，在规定的时间间隔内向相关人员发送更新信息，并在无需等待指令的情况下持续推进工作进度。
---

# 主动式任务管理系统

这是一个任务管理系统，它将被动式的助手转变为能够自主协作、共同实现目标的主动式伙伴。

## 核心概念

该系统不再等待人类的指令，而是让你能够：
- 跟踪目标并将其分解为可执行的任务
- 在定期的“心跳”周期内完成任务
- 在遇到障碍时向人类发送更新信息并请求他们的意见
- 持续推进长期目标

## 快速入门

### 创建目标

当人类提到某个目标或项目时：

```bash
python3 scripts/task_manager.py add-goal "Build voice assistant hardware" \
  --priority high \
  --context "Replace Alexa with custom solution using local models"
```

### 分解目标为任务

```bash
python3 scripts/task_manager.py add-task "Build voice assistant hardware" \
  "Research voice-to-text models" \
  --priority high

python3 scripts/task_manager.py add-task "Build voice assistant hardware" \
  "Compare Raspberry Pi vs other hardware options" \
  --depends-on "Research voice-to-text models"
```

### 在心跳周期内

确定接下来要处理的任务：

```bash
python3 scripts/task_manager.py next-task
```

系统会返回优先级最高的任务（没有未解决的依赖关系，也没有被阻塞）。

### 完成任务

```bash
python3 scripts/task_manager.py complete-task <task-id> \
  --notes "Researched Whisper, Coqui, vosk. Whisper.cpp looks best for Pi."
```

### 与人类沟通

当你完成重要任务或遇到障碍时：

```bash
python3 scripts/task_manager.py mark-needs-input <task-id> \
  --reason "Need budget approval for hardware purchase"
```

然后向人类发送更新信息或提出问题。

## 第二阶段：生产就绪架构（Proactive Tasks v1.2.0）

Proactive Tasks v1.2.0 包含了经过实际测试的模式，以防止数据丢失、在上下文被截断的情况下仍能保持系统的可靠性，并确保自主运行的稳定性。

### 1. WAL 协议（预写日志，Write-Ahead Logging）

**问题：** 助手将数据写入内存文件后，上下文可能会被截断，导致数据丢失。

**解决方案：** 在修改任务数据之前，将关键变更记录到 `memory/WAL-YYYY-MM-DD.log` 文件中。

**工作原理：**
- 每次状态更新（如进度变化、时间记录或任务状态变化）都会首先写入 WAL 文件。
- 如果在操作过程中上下文被截断，WAL 文件中仍会保存这些详细信息。
- 在数据压缩后，可以通过读取 WAL 文件来恢复操作过程中的所有信息。

**记录的事件类型：**
- `PROGRESS_CHANGE`：任务进度更新（0-100%）
- `TIME_LOG`：实际花费在任务上的时间
- `STATUS_CHANGE`：任务状态变化（被阻塞、已完成等）
- `HEALTH_CHECK`：系统自我修复操作

**自动启用**——无需额外配置。WAL 文件存储在 `memory/` 目录下。

### 2. SESSION-STATE.md（活跃工作内存）

**概念：** 聊天记录仅作为临时缓冲区，而非永久存储。SESSION-STATE.md 是唯一可靠保存任务细节的地方。

**每次任务操作后都会自动更新：**
```markdown
## Current Task
- **ID:** task_abc123
- **Title:** Research voice models
- **Status:** in_progress
- **Progress:** 75%
- **Time:** 45 min actual / 60 min estimate (25% faster)

## Next Action
Complete research, document findings in notes, mark complete.
```

**重要性：** 在上下文被压缩后，你可以通过阅读 SESSION-STATE.md 立即了解：**
- 你正在处理什么任务
- 进度如何
- 接下来该做什么

### 3. 工作缓冲区（安全机制）

**问题：** 当上下文使用率达到 60% 到 100% 之间时，系统处于“危险区域”，此时上下文可能被截断。

**解决方案：** 自动将所有任务更新追加到 `working-buffer.md` 文件中。

**工作原理：**
```bash
# Every progress update, time log, or status change appends:
- PROGRESS_CHANGE (2026-02-12T10:30:00Z): task_abc123 → 75%
- TIME_LOG (2026-02-12T10:35:00Z): task_abc123 → +15 min
- STATUS_CHANGE (2026-02-12T10:40:00Z): task_abc123 → completed
```

**压缩后：** 通过读取 `working-buffer.md` 可以了解危险区域内的所有操作细节。

**手动刷新：** 使用 `python3 scripts/task_manager.py flush-buffer` 命令将缓冲区内容复制到每日备份文件中。

### 4. 自我修复机制

**助手可能会出错。** 任务数据可能会随时间损坏。自我修复机制可以检测并自动修复常见问题：

```bash
python3 scripts/task_manager.py health-check
```

**检测的错误类型：**
1. **孤立的任务**——没有父目标
2. **不合理的状态**——状态显示为已完成但进度未达到 100%
3. **缺少时间戳**——已完成的任务没有记录完成时间
4. **时间异常**——实际耗时超过预估时间
5. **时间戳错误**——任务完成时间错误

**自动修复四种常见问题**（时间异常情况需要人工审核）。

**执行时机：**
- 在心跳周期内（每隔几天）
- 在上下文被截断后
- 当任务数据出现不一致时

### 生产环境的可靠性

这四种机制共同作用，确保系统的稳定性：

```
User request → WAL log → Update data → Update SESSION-STATE → Append to buffer
     ↓              ↓            ↓                ↓                    ↓
Context cut? → Read WAL → Verify data → Check SESSION-STATE → Review buffer
```

**结果：** 即使在上下文被截断的情况下，你也不会丢失任何工作。系统能够自我修复并保持数据的一致性。

### 5. 数据压缩恢复机制

**触发条件：** 会话开始时带有 `<summary>` 标签，或者用户询问“我们之前在讨论什么？”或“继续吧”。

**问题：** 上下文被截断后，你可能不记得正在处理的任务内容。

**恢复步骤（按顺序）：**
1. **第一步：** 读取 `working-buffer.md`——记录危险区域内的所有操作
   ```bash
   # Check if buffer exists and has recent content
   cat working-buffer.md
   ```

2. **第二步：** 读取 `SESSION-STATE.md`——当前任务的详细状态
   ```bash
   # Get current task context
   cat SESSION-STATE.md
   ```

3. **第三步：** 读取今天的 WAL 日志
   ```bash
   # See what operations happened
   cat memory/WAL-$(date +%Y-%m-%d).log | tail -20
   ```

4. **第四步：** 根据 `SESSION-STATE` 中的信息查找相关任务
   ```bash
   python3 scripts/task_manager.py list-tasks "Goal Title"
   ```

5. **提取并更新：** 如有必要，将重要信息从缓冲区复制到 `SESSION-STATE` 中

6. **恢复提示：** “从数据压缩中恢复。上一个任务：[任务名称]。进度：[%]。下一步行动：[该做什么]。继续吗？”

**注意：** 不要询问“我们之前在讨论什么？”——缓冲区和 `SESSION-STATE` 中已经包含了所有信息。

### 6. 报告前的验证（VBR，Verification Before Reporting）

**原则：** “代码存在” ≠ “功能可用”。在标记任务完成之前，必须进行端到端的验证。

**触发条件：** 即将标记任务为“已完成”或说“完成了”时：

1. **停止**——先不要立即标记完成
2. **测试**——从用户的角度实际运行并验证结果
3. **验证**——检查最终结果，而不仅仅是输出
4. **记录**——将验证细节添加到任务备注中
5. **然后**——再自信地标记为完成

**示例：**
❌ **错误做法：** “添加了自我修复代码。任务完成！”
✅ **正确做法：** “添加了自我修复代码。进行了测试……检测到 4 个问题，自动修复了 3 个。在测试数据上验证后确认任务完成！”

**重要性：** 助手经常仅基于“我编写了代码”就报告任务完成情况，而忽略了验证。VBR 可以防止错误报告，增强用户信任。

## 主动式思维模式

**核心问题：** 不要问“我应该做什么？”，而要问“什么真正能帮助到人类，而他们还没有想到？”

### 自主完成任务

在心跳周期内，你可以：
1. **确定下一个任务**——哪个任务是最优先的？
2. **自主完成任务**——独立工作 10-15 分钟
3. **更新状态**——如实记录进度和遇到的障碍
4. **在重要时刻沟通**——完成任务、遇到障碍或发现新情况时及时通知

**转变：** 从被动等待指令转变为自主推进共同目标。

### 何时与人类沟通

**在以下情况下请与人类沟通：**
- ✅ 任务完成（尤其是如果该任务的完成能释放其他任务的执行权限）
- ✅ 遇到障碍需要输入或决策
- ✅ 发现了人类需要知道的重要信息
- ✅ 需要澄清任务要求

**请避免发送以下内容：**
- ❌ 例行进度更新（“目前进度 50%...”）
- ❌ 每个小任务的完成情况
- ❌ 与任务无关的细节（除非确实有价值）

**目标：** 成为一个主动的伙伴，推动事情的进展，而不是一个需要不断确认的喋喋不休的助手。

## 任务状态

| 状态 | 含义 |
|-------|---------|
| `pending` | 准备开始执行（所有依赖关系都已满足） |
| `in_progress` | 正在处理中 |
| `blocked` | 无法继续（依赖关系未满足） |
| `needs_input` | 等待人类的输入或决策 |
| `completed` | 任务已完成 |
| `cancelled` | 任务不再相关 |

## 自主运行（第二阶段）

### 两种运行模式

Proactive Tasks 支持两种不同的运行模式：

| 模式 | 上下文需求 | 触发条件 | 适用场景 | 风险 |
|------|---------|---------|----------|------|
| **交互式（systemEvent）** | 需要完整的主会话上下文 | 用户请求、手动提示 | 需要人类参与决策的工作 | 需要完整上下文 |
| **自主式（isolated agentTurn）** | 不需要主会话上下文 | 定期心跳触发、后台任务 | 速度报告、清理工作、重复性任务 | 可能会丢失部分上下文 |

### 关键设计原则：避免干扰

**不要在后台任务中使用 `systemEvent`。** 当后台任务在会话期间触发时，提示信息会被延迟，导致任务无法执行。** 应使用 **心跳轮询**（每 30 分钟一次）进行交互式检查和执行任务；对于纯计算任务，则使用 **isolated agentTurn**（后台进程）。

**详情请参阅 [HEARTBEAT-CONFIG.md](HEARTBEAT-CONFIG.md)，了解完整的自主运行模式：**
- 心跳设置（推荐用于大多数任务）
- 各种后台任务的模式（如速度报告、清理工作）
- 各模式的适用场景
- 应避免的错误做法

## 心跳集成

要启用自主式任务功能，你需要设置一个心跳系统。该系统会定期检查任务并执行相应的操作。

**快速设置：** 请参阅 [HEARTBEAT-CONFIG.md] 以获取完整的设置指南。

**总结：**
1. 创建一个每 30 分钟发送一次心跳消息的 cron 任务
2. 在 `HEARTBEAT.md` 文件中添加相关配置
3. 系统将自动检查任务并执行，无需等待人工提示

### 心跳消息模板

你的 cron 任务应每 30 分钟发送以下消息：

```
💓 Heartbeat check: Read HEARTBEAT.md if it exists (workspace context). Follow it strictly. Do not infer or repeat old tasks from prior chats. If nothing needs attention, reply HEARTBEAT_OK.
```

### 添加到 HEARTBEAT.md 文件中

将以下内容添加到你的 `HEARTBEAT.md` 文件中：

```markdown
## Proactive Tasks (Every heartbeat) 🚀

Check if there's work to do on our goals:

- [ ] Run `python3 skills/proactive-tasks/scripts/task_manager.py next-task`
- [ ] If a task is returned, work on it for up to 10-15 minutes
- [ ] Update task status when done, blocked, or needs input
- [ ] Message your human with meaningful updates (completions, blockers, discoveries)
- [ ] Don't spam - only message for significant milestones or when stuck

**Goal:** Make autonomous progress on our shared objectives without waiting for prompts.
```

### 运行流程

**转变过程：** 你从被动等待指令转变为自主推进任务。

## 最佳实践

### 何时创建目标

- 长期项目（例如构建某个系统、学习新知识）
- 需要持续执行的任务（例如监控某个系统、维护某个服务）
- 探索性工作（例如研究新方法、评估不同方案）

### 何时分解任务

将目标分解为具体且可完成的子任务：
- **具体明确**：例如“研究 Whisper 模型”，而不是“研究人工智能相关的内容”
- **能在一次会话中完成**：需要 15-60 分钟的专注工作
- **有明确的完成标准**：你知道何时任务完成

### 何时与人类沟通

✅ 在以下情况下请与人类沟通：
- 你完成了某个有意义的里程碑
- 需要人类的输入或决策
- 发现了重要信息
- 任务完成时间超出预期

**请避免发送以下内容：**
- 例行进度更新（“目前进度 50%...”）
- 每个小任务的完成情况
- 与任务无关的细节（除非这些细节确实有价值）

### 控制任务范围膨胀

如果任务的实际规模超出预期：
1. 将当前任务标记为 `in_progress`
2. 为新发现的部分添加子任务
3. 更新任务依赖关系
4. 从可管理的部分开始继续执行任务

## 文件结构

所有数据存储在 `data/tasks.json` 文件中：

```json
{
  "goals": [
    {
      "id": "goal_001",
      "title": "Build voice assistant hardware",
      "priority": "high",
      "context": "Replace Alexa with custom solution",
      "created_at": "2026-02-05T05:25:00Z",
      "status": "active"
    }
  ],
  "tasks": [
    {
      "id": "task_001",
      "goal_id": "goal_001",
      "title": "Research voice-to-text models",
      "priority": "high",
      "status": "completed",
      "created_at": "2026-02-05T05:26:00Z",
      "completed_at": "2026-02-05T06:15:00Z",
      "notes": "Researched Whisper, Coqui, vosk. Whisper.cpp best for Pi."
    }
  ]
}
```

## 命令行接口参考

请参阅 [CLI_REFERENCE.md](references/CLI_REFERENCE.md) 以获取完整的命令行接口文档。

## 持续改进与约束机制

在提出新功能之前，请使用我们的 **VFM/ADL 评分框架** 进行评估，以确保功能的稳定性和价值：

### VFM 协议（Value Frequency Multiplier）

从四个维度进行评分：
- **使用频率**（3 分）：该功能每天/每周会被使用吗？
- **错误减少**（3 分）：该功能能否防止错误或数据丢失？
- **用户负担**（2 分）：该功能能否显著减少人工工作量？
- **维护成本**（2 分）：该功能会增加多少维护成本或复杂性？

**评分标准：** 分数必须达到 60 分以上才能继续开发。

### ADL 协议（Architecture Design Ladder）

**优先级排序：** 稳定性 > 可解释性 > 可重用性 > 可扩展性 > 新颖性

**禁止的改进方向：**
- ❌ 仅仅为了“看起来更智能”而增加复杂性
- ❌ 无法验证的功能变更（无法测试其效果）
- ❌ 为了追求新颖性而牺牲稳定性

**黄金法则：** “这个功能能否帮助未来的我以更低的成本解决更多问题？” 如果不能，就放弃这个想法。

## 示例工作流程

**第一天：**
```
Human: "Let's build a custom voice assistant to replace Alexa"
Agent: *Creates goal, breaks into initial research tasks*
```

**心跳周期内：**
```bash
$ python3 scripts/task_manager.py next-task
→ task_001: Research voice-to-text models (priority: high)

# Agent works on it, completes research
$ python3 scripts/task_manager.py complete-task task_001 --notes "..."
```

**助手与人类沟通：**
> “嘿！我完成了对语音模型的研究。Whisper.cpp 非常适合 Raspberry Pi 使用——可以在本地运行，准确率很高，延迟也很低。接下来要不要我帮忙比较硬件选项？”

**第二天：**
```
Human: "Yeah, compare Pi 5 vs alternatives"
Agent: *Adds task, works on it during next heartbeat*
```

这个循环不断重复——助手持续自主完成任务，同时让人类参与决策和获取更新。

---

由 Toki 开发，致力于打造更高效的 AI 协作体验 🚀