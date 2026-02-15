---
name: clawdo
version: 1.1.4
author: LePetitPince <lepetitpince@proton.me>
homepage: https://github.com/LePetitPince/clawdo
description: "AI代理的待办事项列表和任务管理工具：支持自主添加、跟踪和完成任务；代理可以提出任务建议，由人类进行审批。该工具支持按心跳间隔、定时任务（cron）或对话方式触发任务执行；采用持久的SQLite数据库进行数据存储，并以结构化的JSON格式输出结果。"
tags:
  - todo
  - task-queue
  - task-management
  - agent-tools
  - productivity
  - heartbeat
  - workflow
  - autonomous
keywords:
  - todo list
  - task queue
  - todo
  - tasks
  - agent tasks
  - persistent tasks
  - heartbeat tasks
  - agent todo
  - task management
  - agent workflow
  - autonomous execution
  - agent collaboration
categories:
  - productivity
  - agent-tools
  - workflow
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["clawdo"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "clawdo",
              "bins": ["clawdo"],
              "label": "Install clawdo (npm global)",
            },
          ],
      },
  }
---

# 🦞 clawdo — 专为AI代理设计的待办事项列表工具

您的AI代理拥有内存文件、定时任务（cron jobs）以及聊天功能，但却缺乏一个待办事项列表。  
无法简单地通过指令来安排任务，比如“等有空的时候处理这个任务”或“在UTC时间14:00执行这个任务”，更无法在当前对话中立即执行某个任务。唯一的方法就是……记住要去做这件事，并在空闲时处理它。这就是clawdo的作用。

## 安装

```bash
clawhub install clawdo    # installs skill + docs into your workspace
npm install -g clawdo     # install the CLI binary
```

**系统要求：** Node.js ≥ 18

## 快速入门

```bash
# Capture a task
clawdo add "update dependencies" --urgency soon

# Agent checks its queue (heartbeat, cron, conversation — wherever)
clawdo inbox --format json

# Agent works it
clawdo start a3f2
clawdo done a3f2 --json
```

使用命令 `add` 添加任务，任务会进入“收件箱”（inbox），然后通过 `start` 命令开始执行，执行完成后状态会变为 `done`。所有任务的数据都存储在SQLite数据库中。每个命令都支持 `--json` 选项，这样代理就能解析结构化的数据，而不仅仅是终端输出。

## 适用场景

clawdo适用于所有需要管理任务的场景：

- **心跳循环（Heartbeat loops）**：“我的任务队列里有什么任务？在检查间隔期间处理它们吧。”  
- **定时任务（Cron jobs）**：“每小时处理一个任务。”  
- **对话记录**：“J提到需要修复认证模块，让我记录下来。”  
- **管道与子代理（Pipes and sub-agents）**：无需交互式提示，适用于非文本终端环境。

### 心跳循环集成示例

```bash
# In HEARTBEAT.md — runs every ~30 minutes
TASKS=$(clawdo inbox --format json)
AUTO=$(echo "$TASKS" | jq '.autoReady | length')

if [ "$AUTO" -gt 0 ]; then
  TASK=$(clawdo next --auto --json | jq -r '.task.id')
  clawdo start "$TASK" --json
  # ... do the work ...
  clawdo done "$TASK" --json
fi
```

## 权限等级

任务可以被标记不同的权限等级，以控制代理在无人监督下的操作权限：

| 权限等级 | 时间限制 | 含义 |
|---------|---------|--------|
| **auto**   | 10分钟   | 代理自动执行任务（例如修正拼写错误、运行测试）。 |
| **auto-notify** | 30分钟   | 代理执行任务后通知人类。 |
| **collab**   | 无时间限制 | 需要人类参与的任务（复杂、高风险或含义模糊的任务）。 |

默认权限等级为 `collab`（最安全级别）。

**重要规则：** 权限等级是固定不变的，代理无法自行更改。如果代理连续三次失败，其权限等级会降级为 `collab`。权限等级只能降级，不能升级。  
**任务提案由代理提出，人类批准。** 所有任务最初都处于“proposed”（待批准）状态，人类需要通过 `clawdo confirm <id>` 来确认任务是否执行。

## 使用方法

### 对于人类用户

```bash
# Add tasks — inline metadata parsing
clawdo add "deploy new API +backend auto-notify now"
#           └── text ──────┘ └project┘ └─level──┘ └urg┘

# View
clawdo list                       # active tasks
clawdo list --status proposed     # agent suggestions
clawdo next                       # highest priority

# Review agent proposals
clawdo confirm <id>               # approve
clawdo reject <id>                # reject

# Work
clawdo start <id>
clawdo done <id>
clawdo done abc,def,ghi           # complete several
```

### 对于AI代理

```bash
# Check inbox (structured)
clawdo inbox --format json

# Propose work
clawdo propose "add input validation" --level auto --json

# Execute
TASK=$(clawdo next --auto --json | jq -r '.task.id // empty')
if [ -n "$TASK" ]; then
  clawdo start "$TASK" --json
  # ... do the work ...
  clawdo done "$TASK" --json
fi
```

任务的状态会在“收件箱”中显示为：`autoReady`、`autoNotifyReady`、`urgent`、`overdue`、`proposed`、`stale`、`blocked`。

## 内联语法

- `+word` → 项目（Project）  
- `@word` → 任务上下文（Context）  
- `auto` / `auto-notify` / `collab` → 权限等级  
- `now` / `soon` / `whenever` / `someday` → 任务紧急程度  
- `due:YYYY-MM-DD` → 任务截止日期  

## 安全性特性

- **权限不可升级**：代理无法提升自己的权限等级。  
- **任务提案限制**：同一时间最多只能有5个待处理任务，每个任务之间有60秒的冷却时间。  
- **输入安全防护**：对用户输入进行清理处理，使用参数化SQL语句。  
- **审计追踪**：所有状态变更都会被记录到只读日志中。  
- **安全ID生成**：使用 `crypto.randomInt()` 生成随机ID，避免算法偏见。  

## 资源信息

- **GitHub仓库：** https://github.com/LePetitPince/clawdo  
- **npm包：** https://www.npmjs.com/package/clawdo  
- **完整文档：** `clawdo --help`  

## 许可证

MIT许可证