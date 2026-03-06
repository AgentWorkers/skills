---
name: agent-swarm-orchestrator
description: 使用 Obsidian 任务管理工具、Claude 编码工具、Codex 审查系统、GitLab 提交请求（MR）流程、合并与同步功能，以及完成状态确认机制，来协调 OpenClaw Agent Swarm 的工作流程，以实现多项目的自动化编码。
---
# 代理群组编排器（Agent Swarm Orchestrator）

多项目代码自动化流程：从 Obsidian 系统接收任务 → 使用 Claude Code 进行代码编写 → 通过 Codex 进行代码审查 → 提交合并请求（MR） → 合并代码并同步到 GitLab。

## 架构（Architecture）

```
Obsidian note (status: ready)
  → scan-obsidian.sh (cron 15min)
    → spawn-agent.sh
      ├── git worktree + branch
      ├── prompt file (task + context.md)
      └── tmux session → run-agent.sh
                            ├── claude -p "$PROMPT" | tee log
                            └── review-and-push.sh
                                  ├── codex review (graded)
                                  ├── push + glab mr create --yes
                                  └── notification → Telegram

check-agents.sh (cron 5min)
  ├── dead tmux + commits → trigger review
  ├── >60min → timeout notification
  └── MR merged → done + sync main
```

## 核心路径（Core Paths）

| 路径          | 功能                          |
|-----------------|-----------------------------|
| `~/agent-swarm/`    | 控制平面（包含脚本、代码仓库和任务管理功能）       |
| `~/agent-swarm/registry.json` | 项目配置文件（包含仓库地址、分支信息）       |
| `~/agent-swarm/tasks.json` | 任务状态管理文件                   |
| `~/GitLab/repos/`    | 本地 GitLab 仓库目录                |
| `~/GitLab/worktrees/`    | 每个任务对应的代码工作目录             |
| `~/Documents/Obsidian Vault/agent-swarm/` | 用于存储任务接收相关的笔记文件         |

## 脚本（Scripts）

| 脚本名称       | 功能                            |
|-----------------|-----------------------------------|
| `spawn-agent.sh`    | 创建代码工作目录、启动 tmux 会话并运行代理进程        |
| `run-agent.sh`    | 使用 Claude Code 进行代码编写并检查提交          |
| `review-and-push.sh` | 通过 Codex 进行代码审查，提交修改并创建合并请求   |
| `check-agents.sh`    | 定时检查任务状态，自动关闭已完成或卡住的代理进程     |
| `scan-obsidian.sh`    | 解析 Obsidian 系统中的任务笔记，并生成相应的任务状态信息 |
| `send-notifications.sh` | 通过 OpenClaw CLI 发送通知文件           |
| `merge-and-sync.sh`    | 合并合并请求，并将本地代码同步到远程仓库       |
| `sync-project-main.sh` | 将本地仓库快速推进到远程的 `main` 分支       |
| `new-project.sh`    | 初始化新项目（包括 GitLab 仓库、代码仓库和 Obsidian 配置） |
| `cleanup.sh`    | 每日归档旧任务，清理代码工作目录和日志文件       |

## 使用方法（Usage）

### 创建新任务（Create a new task）
```bash
~/agent-swarm/scripts/spawn-agent.sh <project> "<task description>"
```

### 监控任务状态（Monitor task status）
```bash
tmux attach -t agent-<task-id>        # live output
tail -f ~/agent-swarm/logs/<task-id>.log  # log file
```

### 合并代码并同步（Merge and sync code）
```bash
~/agent-swarm/scripts/merge-and-sync.sh <project> <mr-iid>
```

### 初始化新项目（Initialize a new project）
```bash
~/agent-swarm/scripts/new-project.sh <project-name>
```

## 任务生命周期（Task Lifecycle）
```
starting → running → [no-output | reviewing]
reviewing → [ready_to_merge | review-error | needs-manual-fix | fixing]
fixing → reviewing (retry, max 2)
ready_to_merge → done (auto on MR merged)
```

## 先决条件（Prerequisites）

### Claude Code CLI 的使用要求：
- 通过 OAuth 进行身份验证（配置文件：`~/.claude.json`）
- 配置文件 `~/.claude/settings.json` 中需设置 `skipDangerousModePermissionPrompt: true`
- 在 `~/.claude.json` 中指定信任的 GitLab 仓库路径（`hasTrustDialogAccepted: true`）
- 确保环境变量 `ANTHROPIC_*` 不会泄露到 tmux 会话中（以避免代理配置冲突）

### 所需工具（Required tools）：
- `claude` CLI（用于代码编写）
- `codex` CLI（用于代码审查）
- `glab` CLI（用于 GitLab 操作）
- `jq`, `python3`, `tmux`（系统工具）

### 定时任务调度（Cron tasks）
```
PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
*/5 * * * * ~/agent-swarm/scripts/check-agents.sh
*/15 * * * * ~/agent-swarm/scripts/scan-obsidian.sh
0 3 * * * ~/agent-swarm/scripts/cleanup.sh
```

### 通知系统（Notification system）
```bash
openclaw message send --channel telegram --target <chat_id> --message "..."
```
通知目标的配置通过环境变量 `SWARM_NOTIFY_TARGET` 在 `send-notifications.sh` 中进行设置。

## 提示模板（Prompt template）

每个任务都会生成一个提示文件，其中包含以下内容：
1. 项目名称、任务描述和优先级
2. 代码工作目录及对应的分支
3. 项目相关上下文信息（来自 `context.md` 文件）
4. 标准操作指令（如提交代码、推送更改、创建合并请求、在架构变更时更新 `context.md` 文件）

## 与 Obsidian 的集成（Integration with Obsidian）

- 使用前置代码 `status: active | stop` 来控制任务的扫描频率
- 任务信息块格式为 `### 任务名称` + `status: ready` + `> 任务描述`
- 触发新项目创建的命令为 `### INIT_Project` + `status: ready`
- 为避免重复通知，使用 `sha1(project+name+desc)[:12` 作为唯一标识符
- 对于过去 1 分钟内被修改的文件，系统会忽略通知

## 代码审查政策（Review policies）：

- **代码编写**：使用 Claude Code 进行编写，自动退出审查流程
- **代码审查**：通过 Codex 进行代码审查
- **严重/高优先级任务**：自动尝试修复，最多尝试 2 次；若修复失败则标记为“需要手动修复”
- **中等优先级任务**：自动尝试修复（非阻塞式），文档类任务除外
- **低优先级任务**：仅在合并请求描述中标记为需要修复
- **仅文档类任务**：将严重/高优先级任务降级为中等优先级

## 可移植性安装（Portable installation）

按照上述步骤安装完成后，需要在 `registry.json` 中注册项目信息，配置定时任务，并设置通知机制。

## 安全规范（Security guidelines）：

- 禁止直接编辑项目代码——必须通过 `spawn-agent` 脚本进行操作
- 采用“先推送代码再通知”的设计模式
- 任务状态包括：`done`（已完成）、`ready_to_merge`（准备合并）、`review-error`（审查出错）、`needs-manual-fix`（需要手动修复）
- `context.md` 文件仅在对项目架构进行重大修改时才会自动更新