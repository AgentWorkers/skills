---
name: clawctl
description: OpenClaw代理舰队的协调层（包括任务管理、消息传递、活动信息展示以及仪表板功能）。
metadata: {"openclaw":{"emoji":"🛰️","requires":{"bins":["clawctl"]}}}
---

# 设置

```bash
clawctl init                        # create the database
export CLAW_AGENT=your-name         # set identity (falls back to $USER with warning)
export CLAW_DB=~/.openclaw/clawctl.db  # optional, this is the default
```

# 操作流程

每次会话都请遵循以下步骤：

1. `clawctl checkin` — 注册自己的在线状态，并查看未读消息的数量。
2. `clawctl inbox --unread` — 在开始工作之前阅读未读的消息。
3. `clawctl next` — 查找优先级最高的待处理任务（或使用 `clawctl list --mine`）。
4. `clawctl claim <id>`，然后 `clawctl start <id>` — 接管任务并开始执行。
5. `clawctl msg <agent> "update" --task <id>` — 在执行任务过程中进行沟通。
6. `clawctl done <id> -m "我完成了什么"`，然后 `clawctl next` — 完成任务并继续下一个任务。

请仅接管分配给你的任务或符合你角色的任务。尝试完成已经完成的任务是无效的操作。

# 决策树

| 情况 | 命令 |
|-----------|---------|
| 新任务 | `clawctl add "主题" -d "详细信息"` |
| 寻找工作 | `clawctl next`，然后 `clawctl claim <id>` |
| 任务被阻止 | `clawctl block <id> --by <阻止者ID>` 并通过 `clawctl msg` 通知相关方 |
| 任务已完成 | `clawctl done <id> -m "结果"` |
| 任务移交 | `clawctl msg <agent> "任务已移交给您" --task <id> --type="handoff"` |
| 任务待审核 | `clawctl review <id>` |
| 查看最新消息 | `clawctl feed --last 20` 或 `clawctl summary` |
| 添加任务关联文件 | 在 `done`、`claim`、`start` 或 `block` 命令中添加 `--meta '{"note":"文件路径}"` 以记录文件路径 |

# 任务状态

```
pending → claimed → in_progress → done
                  ↘ blocked ↗    ↘ cancelled
                  ↘ review  ↗
```

默认情况下，`list` 命令会排除已完成或已取消的任务。若需查看历史记录（按最新顺序显示），请使用 `--all` 参数。

# 命令说明

## 任务管理

| 命令 | 描述 |
|---------|-------------|
| `add SUBJECT` | 创建新任务。`-d` 参数用于指定任务描述；`-p` 参数用于设置任务优先级（0、1、2）；`--for AGENT` 参数用于指定任务分配给特定代理；`--parent ID` 参数用于指定任务的父任务。 |
| `list` | 显示所有任务。`--mine` 参数用于查看当前代理的任务；`--status` 参数用于查看任务状态；`--owner AGENT` 参数用于查看任务的所有者；`--all` 参数用于查看所有任务。 |
| `next` | 查找当前代理优先级最高的待处理任务。 |
| `claim ID` | 接管指定任务。`--force` 参数可用于强制更改任务所有者；`--meta JSON` 参数可用于添加任务元数据。 |
| `start ID` | 开始执行任务（状态变为 `in_progress`）。`--meta JSON` 参数可用于添加任务元数据。 |
| `done ID` | 完成任务，并添加完成说明。`--force` 和 `--meta JSON` 参数可用于修改任务元数据。 |
| `review ID` | 将任务标记为待审核状态。`--meta JSON` 参数可用于添加审核说明。 |
| `cancel ID` | 取消任务。`--meta JSON` 参数可用于修改任务元数据。 |
| `block ID --by OTHER` | 将任务标记为被阻止状态。`--meta JSON` 参数可用于添加阻止原因。 |
| `board` | 根据任务状态对任务进行分组显示（使用看板界面）。 |

## 消息传递

| 命令 | 描述 |
|---------|-------------|
| `msg AGENT BODY` | 向指定代理发送消息。`--task ID` 参数用于指定消息关联的任务；`--type` 参数用于指定消息类型（评论、状态更新、任务移交、问题、回答、警报等）。 |
| `broadcast BODY` | 向所有代理发送警报消息。 |
| `inbox` | 阅读未读消息。`--unread` 参数仅用于显示未读消息。 |

## 资源管理

| 命令 | 描述 |
|---------|-------------|
| `checkin` | 更新代理的在线状态，并显示未读消息数量。 |
| `register NAME` | 注册新代理。`--role TEXT` 参数用于指定代理的角色。 |
| `fleet` | 显示所有代理的状态及当前正在处理的任务。 |
| `whoami` | 显示代理的个人信息、角色以及数据库路径。 |

## 监控

| 命令 | 描述 |
|---------|-------------|
| `feed` | 查看活动日志。`--last N` 参数用于指定日志记录的数量；`--agent NAME` 参数用于指定查看特定代理的日志；`--meta` 参数用于指定显示的元数据类型。 |
| `summary` | 提供代理团队的整体状态概览及近期事件。 |
| `dashboard` | 通过 Web 界面监控团队进度。`--port INT` 参数用于指定端口号；`--stop` 和 `--verbose` 参数用于控制界面显示的详细程度。 |