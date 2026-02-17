---
name: agent-autonomy-primitives
description: 使用 ClawVault 的基本组件（任务、项目、内存类型、模板、心跳机制）来构建长时间运行的自主代理循环。这些组件适用于设置代理的自主性、创建基于任务的执行循环、自定义基本组件的架构、连接基于心跳的工作队列，以及训练代理管理自身的待办事项列表。此外，它们还适用于将基本组件适配到现有的代理系统中，或通过共享的存储库来设计多代理协作方案。
---
# 代理自主性基础组件

通过五个可组合的基础组件，你可以将任何AI代理转变为一个能够自我导向的工作者：**类型化内存**、**任务文件**、**项目分组**、**模板架构**和**心跳循环**。

## 先决条件

```bash
npm install -g clawvault
clawvault init
```

## 这五个基础组件

### 1. 类型化内存

每种内存都有一个类型。类型决定了它存储的位置以及获取的方式。

| 类型 | 目录          | 使用场景        |
|------|--------------|-------------------|
| `decision` | `decisions/`     | 记录带有理由的决策            |
| `lesson` | `lessons/`     | 从经验中学习到的内容           |
| `person` | `people/`     | 联系信息、关系上下文           |
| `commitment` | `commitments/`     | 承诺事项、应交付的成果         |
| `preference` | `preferences/`     | 个人的工作偏好             |
| `fact` | `inbox/`     | 需要稍后处理的原始信息           |
| `project` | `projects/`     | 包含目标和状态的工作流           |

**规则：** 如果你知道数据的类型，就使用相应的命令来存储它。将所有内容都存储在日常笔记中会使得后续的检索变得困难。

### 2. 任务组件

任务是一个包含YAML前置信息的Markdown文件，存储在`tasks/`目录下：

```yaml
---
status: open
priority: high
owner: your-agent-name
project: my-project
due: 2026-03-01
tags: [infrastructure, deploy]
estimate: 2h
---
# Deploy API to production

## Context
Server provisioned. Need Dockerfile fix.

## Next Steps
- Fix binding to 0.0.0.0
- Add health endpoint
- Push and verify
```

**创建任务：**  
```bash
clawvault task add "Deploy API to production" \
  --priority high \
  --owner my-agent \
  --project my-project \
  --due 2026-03-01 \
  --tags "infrastructure,deploy"
```

**更新任务状态：**  
```bash
clawvault task update deploy-api-to-production --status in-progress
clawvault task done deploy-api-to-production --reason "Deployed, health check passing"
```

**状态：** `open` → `in-progress` → `done`（或`blocked`）  
**优先级：** `critical` > `high` > `medium` > `low`

### 3. 项目分组

项目通过元数据将相关任务组织在一起：

```bash
clawvault project add "Outbound Engine" \
  --owner pedro \
  --client versatly \
  --tags "gtm,sales" \
  --deadline 2026-03-15
```

任务通过`project`字段引用项目。可以通过项目来筛选任务：  
```bash
clawvault task list --project outbound-engine
```

### 4. 模板架构

模板是YAML格式的定义文件，用于规定每个基础组件中应包含哪些字段。它们存储在`templates/`目录下。

有关完整的自定义指南，请参阅[references/template-customization.md](references/template-customization.md)。

**关键点：**  
- 模板可以覆盖内置的字段结构——将`task.md`文件放入`templates/`目录即可更改字段结构  
- 通过编辑模板可以添加新的字段（例如`sprint`、`effort`、`client`）  
- 可以删除不需要的字段  
- 可以修改默认值（例如，默认优先级为`high`）  
- 验证功能仅提供提示，不会阻止任务的执行  

### 5. 心跳循环

心跳循环是实现代理自主性的关键机制。你需要将其集成到代理的定期唤醒周期中。

**每个心跳周期（例如，每30分钟）：**  
```
1. clawvault task list --owner <agent-name> --status open
2. Sort by: priority (critical first), then due date (soonest first)
3. Pick the highest-impact task executable RIGHT NOW
4. Execute it
5. On completion: clawvault task done <slug> --reason "what was done"
6. On blocker: clawvault task update <slug> --status blocked --blocked-by "reason"
7. If new work discovered: clawvault task add "new task" --priority <p> --project <proj>
8. If lesson learned: clawvault remember lesson "what happened"
9. Go back to sleep
```

**针对OpenClaw代理的实现：**  
在`HEARTBEAT.md`文件中添加相关代码：  
```markdown
## Task-Driven Autonomy

Every heartbeat:
1. `clawvault task list --owner <your-name> --status open` → your work queue
2. Sort by priority + due date
3. Pick highest-impact task you can execute NOW
4. Work it. Update status. Mark done. Report.
5. Check for tasks due within 24h — those get priority
```

对于基于Cron的任务调度器，可以安排一个定期执行的作业：  
```
Schedule: every 30 minutes
Action: Read task queue, pick highest priority, execute, report
```

## 组合基础组件以实现自主性

真正的力量在于组件的组合，而非单一组件本身：

```
Wake → Read memory → Check tasks → Execute → Learn → Update memory → Sleep
         ↑                                      |
         └──────────────────────────────────────┘
```

每个周期中，各个组件会相互协作：  
- **内存**为任务执行提供上下文（决策、经验教训、个人偏好影响工作方式）  
- **任务执行**会产生新的数据（学习到的内容、做出的决策、创建的承诺）  
- **经验教训**会优化未来的执行过程（避免重复错误）  
- **Wiki链接`（`[[entity-name]]`）帮助构建跨所有文件的知识图谱**  
- **项目**为代理的工作提供明确的边界，防止其偏离目标  

## 根据你的环境进行调整

有关如何将这些组件集成到现有代理框架（如OpenClaw、LangChain、CrewAI或自定义系统）中的详细指导，请参阅[references/adaptation-guide.md]：  
- 如何将组件集成到现有系统中  
- 选择需要采用哪些组件（从最基本的开始，根据需求逐步扩展）  
- 如何通过共享的数据库实现多代理协作  
- 如何从其他内存系统迁移数据  

## 快速入门：5分钟内实现自主性  

```bash
# 1. Install and init
npm install -g clawvault
clawvault init

# 2. Create your first project
clawvault project add "My Project" --owner my-agent

# 3. Create tasks
clawvault task add "Set up monitoring" --priority high --owner my-agent --project my-project
clawvault task add "Write API docs" --priority medium --owner my-agent --project my-project

# 4. Wire into heartbeat (add to HEARTBEAT.md or cron)
# "Every 30min: clawvault task list --owner my-agent --status open, pick top task, execute"

# 5. Start working
clawvault task update set-up-monitoring --status in-progress
# ... do the work ...
clawvault task done set-up-monitoring --reason "Prometheus + Grafana configured"
clawvault remember lesson "UptimeRobot free tier only checks every 5min" --content "Use Better Stack for <1min checks"
```

## 应避免的做法  

| 不要这样做 | 应该这样做 |
|---------|-------------|
| 将所有内容存储在一个大型内存文件中 | 使用类型化内存（`decisions/`、`lessons/`、`people/`等） |
| 创建没有所有者或项目信息的任务 | 必须为每个任务指定`--owner`和`--project`字段 |
| 询问“我应该做什么？” | 查看任务队列并做出决策 |
| 学到经验后忘记记录 | 使用`clawvault remember lesson`立即保存记录 |
| 跳过标记任务为“已完成”的步骤 | 必须使用`task done --reason`来记录任务状态 |
| 为模糊的想法创建任务 | 先将想法放入`backlog/`，准备就绪后再转移到`tasks/` |
| 不断修改模板架构 | 尽早稳定模板结构——字段名称的更改可能会破坏现有文件 |

## Obsidian集成

由于所有数据都采用Markdown格式并带有YAML前置信息，Obsidian可以将代理的工作空间呈现为人类可读的界面：  
- **看板**：在Obsidian Bases中打开`all-tasks.base`文件，可以在不同状态之间拖动任务  
- **阻塞状态视图**：`blocked.base`显示需要人工处理的任务  
- **按所有者分类**：`by-owner.base`显示每个代理正在处理的任务  
- **按项目分类**：`by-project.base`按工作流展示任务  

同一个文件既是代理的数据结构，也是人类的用户界面。无需额外的同步层。