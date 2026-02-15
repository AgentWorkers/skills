---
name: research-tracker
description: 使用基于 SQLite 的状态跟踪系统来管理自主 AI 研究代理。适用于创建长时间运行的研究子代理、跟踪多步骤调查过程、协调代理之间的协作以及监控后台工作。触发条件包括：研究项目的启动、子代理之间的协作、自主调查的进行、进度跟踪以及代理的运行状态监控。
---

# 研究跟踪器（Research Tracker）

这是一个命令行工具（CLI），用于管理具有只写状态（append-only）、指令队列以及监控功能的自主研究代理（research agents）。

## 先决条件

```bash
brew tap 1645labs/tap
brew install julians-research-tracker
```

或者：`go install github.com/1645labs/julians-research-tracker/cmd/research@latest`

## 快速入门

### 启动一个研究项目
```bash
research init market-q1 --name "Q1 Market Analysis" --objective "Analyze competitor pricing and positioning"
```

### 作为研究代理——记录进度
```bash
export RESEARCH_SESSION_ID="$SESSION_KEY"  # Track which agent is writing

research log market-q1 STEP_BEGIN --step 1 --payload '{"task":"gather sources"}'
# ... do work ...
research log market-q1 STEP_COMPLETE --step 1
research heartbeat market-q1
```

### 检查状态（从主会话或心跳信号中）
```bash
research status market-q1 --json
research context market-q1 --last 5  # Truncated context for prompts
```

### 向正在运行的代理发送指令
```bash
research instruct market-q1 "Focus on enterprise segment" --priority URGENT
research stop-signal market-q1  # Request graceful stop
```

### 代理检查是否有新指令
```bash
research pending market-q1 --json
research ack market-q1 --all  # Acknowledge after processing
research check-stop market-q1  # Exit 0 = stop, Exit 1 = continue
```

## 命令参考

| 命令 | 功能 |
|---------|---------|
| `init <id> -o "..."` | 创建一个带有目标的研究项目 |
| `list [--status active\|done\|all]` | 列出所有项目（包括 `needs_attention` 标志） |
| `show <id>` | 查看项目详情及最近事件 |
| `stop <id>` | 停止项目，并发送 STOP 指令 |
| `archive <id>` | 将已完成的项目归档 |
| `log <id> <event> [--step N]` | 记录事件（如 STEP_BEGIN、CHECKPOINT、BLOCKED 等） |
| `heartbeat <id>` | 更新代理的活跃时间戳 |
| `block <id> --reason "..."` | 将代理标记为“被阻塞状态”，需要输入 |
| `complete <id>` | 将代理标记为“已完成” |
| `status <id> [--json]` | 查看当前项目状态 |
| `context <id> [--last N]` | 提供代理提示所需的简短上下文信息 |
| `instruct <id> "text"` | 向代理发送指令 |
| `pending <id>` | 列出未处理的指令 |
| `ack <id> [--all]` | 回应所有指令 |
| `check-stop <id>` | 返回退出代码：0=停止，1=继续 |
| `audit <id> --verdict pass\|drift` | 记录审计结果 |

## 事件类型

`STARTED`、`STEP_BEGIN`、`STEP COMPLETE`、`CHECKPOINT`、`BLOCKED`、`UNBLOCKED`、`AUDIT_PASS`、`AUDIT_DRIFT`、`HEARTBEAT`、`DONE`、`STOPPED`、`TIMEOUT`

## 集成模式

### 启动一个研究代理
```
1. research init <project> --objective "..."
2. sessions_spawn with task including:
   - Project ID and objective
   - Instructions to use research CLI for state
   - Check stop signal before each step
   - Log progress with heartbeat
3. Heartbeat monitors: research list --json | check needs_attention
4. Send instructions via: research instruct <project> "..."
```

### 代理的运行循环（在已启动的代理中）
```bash
while research check-stop $PROJECT; [ $? -eq 1 ]; do
  research pending $PROJECT --json  # Check instructions
  research log $PROJECT STEP_BEGIN --step $STEP
  # ... do work ...
  research log $PROJECT STEP_COMPLETE --step $STEP
  research heartbeat $PROJECT
  STEP=$((STEP + 1))
done
research complete $PROJECT
```

## 注意力检测（Attention Detection）

当满足以下条件时，`research list --json` 的输出中会包含 `needs_attention: true` 标志：
- 最后一个事件为 `BLOCKED`（被阻塞状态）
- 有未处理的紧急（URGENT）或 STOP 指令
- 心跳信号过期（距离上次心跳事件已超过 5 分钟）
- 最近的审计结果为 `AUDIT_DRIFT`（审计结果异常）

## 数据库

使用 SQLite 数据库（文件路径：`~/.config/research-tracker/research.db`），采用 WAL 模式（仅追加数据，不覆盖原有数据）。

安装完成后运行 `research db migrate` 命令进行数据库迁移。首次使用时数据库结构会自动迁移。