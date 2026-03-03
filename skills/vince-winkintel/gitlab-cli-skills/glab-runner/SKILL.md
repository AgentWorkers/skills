---
name: glab-runner
description: 管理 GitLab 的持续集成/持续部署（CI/CD）运行器：可以在项目、组或实例级别列出、暂停或删除这些运行器。适用于查看运行器状态、临时暂停某个运行器，或移除不再使用的运行器。相关操作包括：查看运行器信息、暂停运行器、删除运行器等。
---
# glab runner

用于通过命令行管理 GitLab 的持续集成/持续部署（CI/CD）运行器。

> **新增于 glab v1.87.0**

## 快速入门

```bash
# List runners for current project
glab runner list

# Pause a runner
glab runner pause <runner-id>

# Delete a runner
glab runner delete <runner-id>
```

## 常见工作流程

### 列出所有运行器

```bash
# List all runners for current project
glab runner list

# List for a specific project
glab runner list --repo owner/project

# List all runners (instance-level, admin only)
glab runner list --all

# Output as JSON
glab runner list --output json

# Paginate
glab runner list --page 2 --per-page 50
```

**示例 JSON 输出解析：**
```bash
# Find all paused runners
glab runner list --output json | python3 -c "
import sys, json
runners = json.load(sys.stdin)
paused = [r for r in runners if r.get('paused')]
for r in paused:
    print(f\"{r['id']}: {r.get('description','(no description)')} — {r.get('status')}\")
"
```

### 暂停运行器

暂停运行器可以阻止其接收新的任务，但不会将其从系统中删除。

```bash
# Pause runner 123
glab runner pause 123

# Pause in a specific project context
glab runner pause 123 --repo owner/project
```

**何时需要暂停运行器：**
- 维护窗口期间（进行更新、重启等操作）
- 调查出现故障的运行器
- 临时减少运行器数量
- 在退役运行器之前（先确认没有任务正在运行）

### 删除运行器

```bash
# Delete with confirmation prompt
glab runner delete 123

# Delete without confirmation
glab runner delete 123 --force

# Delete in a specific project context
glab runner delete 123 --repo owner/project
```

**⚠️ 删除操作是不可逆的。** 如果不确定，请先暂停运行器。

## 决策树：暂停 vs 删除

```
Do you need the runner gone permanently?
├─ No → Pause it (recoverable)
└─ Yes → Is it actively running jobs?
          ├─ Yes → Pause first, wait for jobs to finish, then delete
          └─ No → Delete with --force
```

## 运行器状态参考

| 状态 | 含义 |
|---|---|
| `online` | 已连接并准备好接收任务 |
| `offline` | 未连接（请检查运行器进程） |
| `paused` | 已连接但不接收新任务 |
| `stale` | 过去 3 个月内无任何活动 |

## 故障排除

**“runner: command not found”**：
- 需要使用 glab v1.87.0 或更高版本。请使用 `glab version` 命令检查版本信息。

**在实例级别运行器上出现 “Permission denied” 错误**：
- 实例级别的运行器管理需要 GitLab 管理员权限。
- 项目级别的运行器可以由项目维护者管理。

**运行器无法被暂停**：
- 使用 `glab runner list` 命令确认运行器 ID。
- 检查权限（至少需要具有项目维护者权限）。

**暂停后运行器仍显示为 “online” 状态**：
- 运行器进程仍在主机上运行，只是无法接收新任务。
- 这是正常现象。要完全停止运行器，需要通过 SSH 连接到主机并终止该进程。

**无法删除运行器**：
- 运行器可能是共享的或属于组级别（需要更高权限）。
- 检查该运行器是否被分配给了多个项目；如果需要删除某个运行器，可能需要从项目级别进行操作，而非实例级别。

## 相关技能

- `glab-runner-controller` — 管理运行器控制器和调度流程（仅限管理员使用，处于实验阶段）
- `glab-ci` — 查看和管理 CI/CD 流程及任务
- `glab-job` — 为单个任务重试、取消或查看日志

## 命令参考

```
glab runner <command> [--flags]

Commands:
  list    Get a list of runners available to the user
  pause   Pause a runner
  delete  Delete a runner

Flags (list):
  --all          List all runners (instance-level, admin only)
  --output       Format output as: text, json
  --page         Page number
  --per-page     Number of items per page
  --repo         Select a repository
  -h, --help     Show help

Flags (pause / delete):
  --force        Skip confirmation prompt (delete only)
  --repo         Select a repository
  -h, --help     Show help
```