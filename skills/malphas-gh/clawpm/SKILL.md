---
name: clawpm
description: 多项目任务与研究管理工具（基于JSON的命令行界面）
user-invocable: true
metadata: { "openclaw": { "requires": { "bins": ["clawpm"] }, "emoji": "📋", "install": [{ "id": "uv", "kind": "uv", "package": "git+https://github.com/malphas-gh/clawpm", "bins": ["clawpm"], "label": "Install clawpm (uv)" }] } }
---

# ClawPM 技能

**多项目任务管理**：所有命令默认输出 JSON 格式的数据；使用 `-f text` 可以获得人类可读的输出。

## 首次设置

```bash
clawpm setup               # Creates ~/clawpm/ with portfolio.toml, projects/, work_log.jsonl
clawpm setup --check       # Verify installation
```

可以通过 `CLAWPM_PORTFOLIO` 环境变量来覆盖项目文件夹的位置。

## 创建项目

项目是由包含 `.project/` 文件夹的目录组成的。这些目录不需要是 Git 仓库。

### 在任意目录下初始化项目

```bash
cd /path/to/my-project
clawpm project init                    # Auto-detects ID/name from directory
clawpm project init --id myproj        # Custom ID
```

### 通过 Git 克隆自动初始化

位于 `~/clawpm/projects/` 目录下的 Git 仓库在首次使用时会自动初始化：

```bash
git clone git@github.com:user/repo.git ~/clawpm/projects/repo
cd ~/clawpm/projects/repo
clawpm add "First task"    # Auto-initializes .project/, then adds task
```

### 发现未跟踪的 Git 仓库

```bash
clawpm projects list --all   # Shows tracked + untracked git repos
```

## 快速入门

```bash
# From a project directory (auto-detected):
clawpm status              # See project status
clawpm next                # Get next task
clawpm start 42            # Start task (short ID works)
clawpm done 42             # Mark done

# Or set a project context:
clawpm use my-project
clawpm status              # Now uses my-project
```

## 顶级命令（快捷方式）

| 命令 | 等效命令 | 描述 |
|---------|------------|-------------|
| `clawpm add "标题"` | `clawpm tasks add -t "标题"` | 快速添加任务 |
| `clawpm add "标题" -b "描述"` | `clawpm tasks add -t "标题" -b "描述"` | 添加带有描述的任务 |
| `clawpm add "标题" --parent 25` | | 添加子任务 |
| `clawpm done 42` | `clawpm tasks state 42 done` | 标记任务为已完成 |
| `clawpm start 42` | `clawpm tasks state 42 progress` | 开始执行任务 |
| `clawpm block 42` | `clawpm tasks state 42 blocked` | 标记任务为被阻塞 |
| `clawpm next` | `clawpm projects next` | 获取下一个任务 |
| `clawpm status` | | 项目概览 |
| `clawpm context` | | 完整的代理上下文信息 |
| `clawpm use <id>` | | 设置项目上下文 |

## 项目自动检测

ClawPM 会按以下优先级自动检测你的项目：
1. **子命令标志**：`clawpm tasks list --project clawpm`
2. **全局标志**：`clawpm --project clawpm status`
3. **当前目录**：向上查找 `.project/settings.toml` 文件
4. **自动初始化**：如果位于 `project_roots` 下的未跟踪 Git 仓库中，会自动初始化
5. **上下文**：之前通过 `clawpm use <project>` 设置的上下文

## 任务 ID 的简化表示

你可以只使用任务 ID 的数字部分：
- `42` → `CLAWP-042`（前缀来自项目 ID）
- `CLAWP-042` → `CLAWP-042`（完整的 ID 也可以）

## 子任务

```bash
clawpm add "Subtask" --parent 25   # Creates subtask (auto-splits parent if needed)
clawpm tasks split 25              # Manually convert task to parent directory

clawpm done 25             # Fails if subtasks not done
clawpm done 25 --force     # Override and complete anyway
```

子任务的状态会随父任务的状态变化而变化（例如，当父任务状态变为“已完成”或“被阻塞”时，子任务所在的目录也会相应变化）。

## 代理上下文（恢复工作）

通过一个命令获取恢复工作所需的所有信息：

```bash
clawpm context             # Full context for current project
clawpm context -p myproj   # Specific project
```

返回的 JSON 包含：项目信息、正在进行/下一个任务、阻塞原因、最近的工作日志、Git 状态以及未解决的问题。

## 工作流程示例

```bash
clawpm context             # Get full context
clawpm start 42            # Mark in progress (auto-logs)
# ... do work ...
git add . && git commit -m "feat: ..."
clawpm done 42 --note "Completed"       # Auto-logs with files_changed
clawpm log commit                        # Also log the git commits themselves
```

遇到阻碍时：

```bash
clawpm block 42 --note "Need API credentials"
```

## 完整命令参考

### 项目
```bash
clawpm projects list [--all]            # List projects (--all includes untracked repos)
clawpm projects next                    # Next task across all projects
clawpm project context [project]        # Full project context
clawpm project init                     # Initialize project in current dir
```

### 任务
```bash
clawpm tasks                            # List tasks (default: open+progress+blocked)
clawpm tasks list [-s open|done|blocked|progress|all] [--flat]
clawpm tasks show <id>                  # Task details
clawpm tasks add -t "Title" [--priority 3] [--complexity m] [--parent <id>] [-b "body"]
clawpm tasks edit <id> [--title "..."] [--priority N] [--complexity s|m|l|xl] [--body "..."]
clawpm tasks state <id> open|progress|done|blocked [--note "..."] [--force]
clawpm tasks split <id>                 # Convert to parent directory for subtasks
```

### 工作日志
```bash
clawpm log add --task <id> --action progress --summary "What I did"
clawpm log tail [--limit 10]            # Recent entries (auto-filtered to current project)
clawpm log tail --all                   # Recent entries across all projects
clawpm log tail --follow                # Live tail (like tail -f)
clawpm log last                         # Most recent entry (auto-filtered to current project)
clawpm log last --all                   # Most recent entry across all projects
clawpm log commit [-n 10]               # Log recent git commits to work log
clawpm log commit --dry-run             # Preview without logging
clawpm log commit --task <id>           # Associate commits with a task
```

**注意**：任务状态的变化（开始/完成/被阻塞）会通过 `git files_changed` 事件自动记录到工作日志中。

### 研究
```bash
clawpm research list
clawpm research add --type investigation --title "Question"
clawpm research link --id <research_id> --session-key <key>
```

### 问题
```bash
clawpm issues add --type bug --severity high --actual "What happened"
clawpm issues list [--open]             # Open issues only
```

### 会议记录提取
```bash
clawpm sessions extract                # Extract OpenClaw sessions with clawpm calls
clawpm sessions extract --force        # Re-extract all (overwrite existing)
clawpm sessions list                   # List extracted sessions with stats
clawpm sessions list --processed       # List already-processed sessions
clawpm sessions process <id-prefix>    # Move session to processed/
clawpm sessions process --all          # Move all extracted to processed/
```

### 管理员功能
```bash
clawpm setup               # Create portfolio (first-time)
clawpm setup --check       # Verify installation
clawpm status              # Project overview
clawpm context             # Full agent context
clawpm doctor              # Health check
clawpm use [project]       # Set/show project context
clawpm use --clear         # Clear context
```

## 工作日志操作

- `start` - 开始工作（会自动记录在 `clawpm start` 中）
- `progress` - 进展中
- `done` - 完成（会自动记录在 `clawpm done` 中）
- `blocked` - 遇到阻碍（会自动记录在 `clawpm block` 中）
- `commit` - 提交 Git 代码（通过 `clawpm log commit` 记录）
- `pause` - 切换任务
- `research` - 研究笔记
- `note` - 一般性观察

## 任务状态与文件位置

| 状态 | 文件路径 | 含义 |
|-------|--------------|---------|
| open | `tasks/CLAWP-042.md` | 可以开始工作 |
| progress | `tasks/CLAWP-042.progress.md` | 正在处理中 |
| done | `tasks/done/CLAWP-042.md` | 已完成 |
| blocked | `tasks/blocked/CLAWP-042.md` | 等待处理 |

## 提示

- **命令标志的使用顺序**：`clawpm [全局标志] <命令> [命令标志>`（例如：`clawpm -f text tasks list -s open`）
- **输出格式**：所有命令默认输出 JSON；使用 `-f text` 可以获得人类可读的格式
- **每次调用一个命令**：不要使用 `&&` 连接多个 `clawpm` 命令——请分别执行它们
- **项目文件夹的默认位置**：`~/clawpm`；可以通过 `CLAWPM_PORTFOLIO` 环境变量进行覆盖
- **额外的项目文件夹**：可以通过设置 `CLAWPMPROJECT_ROOTS`（用冒号分隔）或在 `portfolio.toml` 中添加到 `project_roots` 列表中
- **工作日志**：日志文件仅可追加，存储在 `<portfolio>/work_log.jsonl` 中

## 故障排除

```bash
clawpm doctor              # Check for issues
clawpm setup --check       # Verify installation
clawpm log tail            # See recent activity
```