---
name: task-system
displayName: Task System
description: 这是一个完整的任务跟踪系统，支持使用 SQLite 数据库进行数据持久化存储、自动任务创建、任务状态通知、心跳监测以及卡住任务的恢复功能。该系统替代了原有的 `task-queue-heartbeat`、`auto-track` 和 `notification` 工具，可用于满足所有的任务管理需求。
version: 1.0.0
author: Santosh
license: MIT
install: ./install.sh
---

# 任务管理系统

这是一个用于管理任务完整生命周期的技能工具。

## 安装

```bash
./install.sh
```

或者手动将其添加到 PATH 环境变量中：
```bash
export PATH="$HOME/.openclaw/agents/main/workspace/skills/task-system/scripts:$PATH"
```

## 快速命令

```bash
# Create task
task-system.sh create "Your request here"

# Update heartbeat
task-system.sh heartbeat $TASK_ID

# Mark complete
task-system.sh complete $TASK_ID "Optional notes"

# Check stuck
task-system.sh stuck

# Daily status
task-system.sh status
```

## 数据库架构

```sql
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  request_text TEXT NOT NULL,
  status TEXT DEFAULT 'pending',
  priority INTEGER DEFAULT 5,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  started_at DATETIME,
  completed_at DATETIME,
  last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
  notes TEXT
);

-- Key indexes
CREATE INDEX IF NOT EXISTS idx_tasks_status_updated ON tasks(status, last_updated);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority ASC);
```

## 脚本

请查看 `scripts/` 目录：
- `task-system.sh` — 主要命令行工具（用于创建任务、检查任务状态、标记任务完成、处理卡住的任务等）
- `create-task.sh` — 创建新任务
- `heartbeat.sh` — 更新任务的最后更新时间
- `complete-task.sh` — 标记任务为已完成
- `stuck-check.sh` — 查找卡住的任务