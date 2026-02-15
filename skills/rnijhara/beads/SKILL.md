---
name: beads
description: 这是一个基于 Git 的问题跟踪工具，专为 AI 代理设计。它可用于管理任务、依赖关系以及多步骤工作流程。该工具会在任务跟踪、问题管理、依赖关系图、待处理工作队列，或者当出现 “beads”/“bd” CLI 命令时触发相应的操作。
metadata:
  openclaw:
    emoji: 📿
    requires:
      bins: [bd]
    install:
      - id: brew
        kind: brew
        formula: beads
        bins: [bd]
        label: Install beads (brew)
      - id: npm
        kind: npm
        package: "@beads/bd"
        bins: [bd]
        label: Install beads (npm)
---

# Beads

这是一个用于AI代理的分布式、基于Git的图形问题跟踪工具。它使用JSONL格式存储任务信息，取代了传统的Markdown格式。

## 快速入门

```bash
# Initialize (non-interactive for agents)
bd init --quiet

# Check ready work
bd ready --json

# Create a task
bd create "Complete task X" -p 1 --json

# View task
bd show bd-a1b2 --json
```

## 核心工作流程

1. `bd ready --json` — 查找未阻塞的任务
2. `bd update <id> --status in_progress` — 接受任务
3. 完成任务
4. `bd close <id> --reason "Done"` — 任务完成
5. `bd sync` — 在结束会话前强制同步数据

## 对代理至关重要的规则：

- **始终使用`--json`选项** 以生成机器可读的输出
- **切勿使用`bd edit`** — 该命令会打开编辑器，代理无法使用
- **改用`bd update`命令**，例如：`bd update <id> --title "新标题" --description "新描述"`
- **在会话结束时运行`bd sync`**，将更改同步到Git仓库

## 命令

### 初始化

```bash
bd init --quiet              # Non-interactive, auto-installs hooks
bd init --prefix myproj      # Custom ID prefix
bd init --stealth            # Local only, don't commit .beads/
bd init --contributor        # Fork workflow (separate planning repo)
```

### 创建问题

```bash
bd create "Title" -p 1 --json                    # Priority 1 (0=critical, 3=low)
bd create "Title" -t epic -p 0 --json            # Create epic
bd create "Subtask" -p 1 --json                  # Under epic: bd-a3f8.1, .2, .3
bd create "Found issue" --deps discovered-from:bd-a1b2 --json
```

问题类型：`task`（任务）、`bug`（错误）、`feature`（功能需求）、`epic`（大型项目）
优先级：`0`（P0/紧急）到`3`（P3/低优先级）

### 查询问题

```bash
bd ready --json                    # Unblocked tasks (the work queue)
bd ready --priority 0 --json       # Only P0s
bd ready --assignee agent-1 --json # Assigned to specific agent

bd list --json                     # All issues
bd list --status open --json       # Open issues
bd list --priority 1 --json        # P1 issues

bd show bd-a1b2 --json             # Issue details + audit trail
bd blocked --json                  # Issues waiting on dependencies
bd stats --json                    # Statistics
```

### 更新问题

```bash
bd update bd-a1b2 --status in_progress --json
bd update bd-a1b2 --title "New title" --json
bd update bd-a1b2 --description "Details" --json
bd update bd-a1b2 --priority 0 --json
bd update bd-a1b2 --assignee agent-1 --json
bd update bd-a1b2 --design "Design notes" --json
bd update bd-a1b2 --notes "Additional notes" --json
```

问题状态：`open`（开放）、`in_progress`（进行中）、`blocked`（阻塞）、`closed`（已完成）

### 关闭问题

```bash
bd close bd-a1b2 --reason "Completed" --json
bd close bd-a1b2 bd-b2c3 --reason "Batch close" --json
```

### 依赖关系

```bash
bd dep add bd-child bd-parent      # child blocked by parent
bd dep add bd-a1b2 bd-b2c3 --type related    # Related link
bd dep add bd-a1b2 bd-epic --type parent     # Parent-child

bd dep tree bd-a1b2                # Visualize dependency tree
bd dep remove bd-child bd-parent   # Remove dependency
bd dep cycles                      # Detect circular deps
```

依赖类型：`blocks`（默认）、`related`（相关）、`parent`（父任务）、`discovered-from`（从哪个任务派生）

### Git同步

```bash
bd sync                    # Export → commit → pull → import → push
bd hooks install           # Install git hooks for auto-sync
```

该工具会以30秒的延迟自动同步数据。可以使用`bd sync`命令强制立即同步。

### 维护

```bash
bd admin compact --dry-run --json   # Preview compaction
bd admin compact --days 90          # Compact issues closed >90 days
bd doctor                           # Check database health
```

## 分层ID（大型项目）

```bash
bd create "Project Alpha" -t epic -p 1 --json   # Returns: bd-a3f8
bd create "Phase 1" -p 1 --json                 # Returns: bd-a3f8.1
bd create "Research" -p 1 --json                # Returns: bd-a3f8.2
bd create "Review" -p 1 --json                  # Returns: bd-a3f8.3
```

问题ID最多可包含3个层级，例如：`bd-a3f8` → `bd-a3f8.1` → `bd-a3f8.1.1`

## 多代理协调

```bash
# Agent claims work
bd update bd-a1b2 --status in_progress --assignee agent-1 --json

# Query assigned work
bd ready --assignee agent-1 --json

# Track discovered work
bd create "Found issue" --deps discovered-from:bd-a1b2 --json
```

## 提交规范（可选）

对于使用Git进行版本控制的项目，请在提交信息中包含问题ID，以便追踪问题进度：

```bash
git commit -m "Complete research phase (bd-a1b2)"
```

## 会话结束前的检查事项

在结束会话之前，请确保完成以下操作：

```bash
bd sync                    # Flush all changes
bd ready --json            # Show next work for handoff
```