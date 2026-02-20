# a6-agent-orchestrator-pro

> 一款功能齐全的代理编排器，具备注册表、任务队列、工作流引擎、权限管理、成本控制、ClickUp集成以及项目隔离等功能。

## 主要特性

- **代理注册表** — 可以注册代理，并设置其使用的模型、系统提示语以及权限范围。
- **权限管理** — 为每个代理指定允许使用的工具、可访问的文件路径、是否可以发送外部通信以及运行时间限制。
- **任务队列** — 基于优先级的任务队列，会自动将任务分配给合适的代理。
- **项目隔离** — 可以按项目对任务进行标记，并根据项目过滤和限制代理的操作范围。
- **预算控制** — 提供每日/每月的支出限额，并在超出限额时发出警告。
- **ClickUp集成** — 支持与ClickUp的双向数据同步（从ClickUp获取任务，将完成结果推送回ClickUp）。
- **工作流引擎** — 支持包含依赖关系的多步骤工作流，并具备错误处理机制。
- **仪表板** — 会自动生成HEARTBEAT.md文件，提供系统的完整概览。
- **健康检查** — 提供简洁的一行代码来检查系统运行状态。
- **报告** — 提供包含项目详细信息和成本统计的汇总报告。

## 系统要求

- Python 3.10及以上版本
- 内置SQLite数据库
- 需要OpenClaw工作空间，且该工作空间中必须存在`.data/sqlite/`目录
- （可选）ClickUp API令牌（用于与ClickUp进行数据同步）

## 快速入门

```bash
PY=~/.openclaw/workspace/.venv/bin/python3

# Initialize schema and seed default agents
$PY scripts/agent_orchestrator.py --init

# Register an agent with permissions
$PY scripts/agent_orchestrator.py register security-scanner claude-sonnet-4 \
  "Security scanning specialist" \
  --allowed-tools "web_search,read" \
  --allowed-paths "/workspace/tools,/workspace/skills" \
  --max-runtime 120

# Queue a task with project tag
$PY scripts/agent_orchestrator.py queue "Research competitor pricing" --type research --priority 2 --project mlm

# Set budget limits
$PY scripts/agent_orchestrator.py budget set --daily 5.00 --monthly 100.00

# Check status
$PY scripts/agent_orchestrator.py status

# Run next task (checks budget before spawning)
$PY scripts/agent_orchestrator.py run-next
```

## 命令说明

### 代理管理
| 命令 | 功能说明 |
|---------|-------------|
| `register <name> <model> <prompt> [--allowed-tools] [--allowed-paths] [--can-send-external] [--max-runtime]` | 注册代理并设置其权限 |
| `list` | 列出所有代理及其权限信息 |
| `list --project <name>` | 按项目筛选并列出任务 |
| `assign <task_type> <agent_name>` | 将任务类型分配给指定的代理 |

### 任务队列
| 命令 | 功能说明 |
|---------|-------------|
| `queue <description> [--type] [--priority] [--project]` | 将任务加入队列 |
| `run-next` | 运行队列中优先级最高的任务（会检查预算是否超出限制） |
| `auto-route [--execute] [--force]` | 自动为未分配代理的任务分配执行者 |
| `status` | 显示代理数量、队列状态及预算使用情况 |

### 预算控制
| 命令 | 功能说明 |
|---------|-------------|
| `budget set --daily <*> --monthly <$>` | 设置每日/每月的支出限额 |
| `budget status` | 显示当前支出与限额的对比情况 |
| `budget alert` | 当支出接近限额（80%以上）时发出警告 |
| `budget log <amount> [--agent] [--desc]` | 记录支出明细 |

### ClickUp集成
| 命令 | 功能说明 |
| `sync-clickup` | 从ClickUp文件夹中获取任务信息 |
| `update-clickup` | 将任务完成结果推送回ClickUp |

### 监控
| 命令 | 功能说明 |
| `dashboard` | 查看完整的系统仪表板（HEARTBEAT.md格式） |
| `heartbeat` | 提供简短的系统运行状态检查 |
| `report` | 提供包含项目详细信息和成本统计的汇总报告 |
| `history [--limit N]` | 查看任务执行历史记录 |

## 权限管理

每个代理的配置包括：
- **allowed_tools** — 代理允许使用的工具名称（以JSON数组形式）
- **allowed_paths** — 代理可以访问的文件路径（以JSON数组形式）
- **can_send_external** — 代理是否可以发送电子邮件或消息
- **max_runtime_seconds** — 代理的运行超时时间

这些权限会在代理启动时通过`run-next`命令注入其系统提示语中，从而实现由模型强制执行的安全控制。

## 项目隔离

任务可以按照项目名称进行标记：
```bash
$PY scripts/agent_orchestrator.py queue "Build landing page" --type build_skill --project mlm
$PY scripts/agent_orchestrator.py list --project mlm
```

当代理被分配执行带有项目标签的任务时，其系统提示语中会包含与该项目相关的操作指南，以限制代理的操作范围。

## 成本控制

预算限制可以防止无节制的支出：
```bash
$PY scripts/agent_orchestrator.py budget set --daily 5.00 --monthly 100.00
$PY scripts/agent_orchestrator.py budget log 0.15 --agent researcher --desc "Deep research on X"
$PY scripts/agent_orchestrator.py budget alert
```

`run-next`命令在启动代理之前会检查预算，如果超出限额则会拒绝执行任务。

## 数据库

使用SQLite数据库（文件路径：`.data/sqlite/agxntsix.db`），其中包含以下表格：
- `agents` — 代理注册表及权限信息
- `task_queue` — 带有项目标签的任务队列
- `execution_log` — 任务执行历史记录
- `budget_config` — 预算限制信息
- `daily_spend` — 日常支出记录
- `workflow_definitions` / `workflow_steps` / `workflow_runs` — 工作流相关数据
- `agent_taskMappings` — 任务类型与代理的映射关系
- `agent_configs` — 代理的配置信息（键值对形式）

## 架构设计

```
User/Cron → Queue Task → Auto-Route → Budget Check → Spawn Agent (with permissions)
                                                          ↓
                                              Permission-scoped system prompt
                                              Project-isolated context
                                              Runtime-limited execution
                                                          ↓
                                              Log result → Update ClickUp → Dashboard
```

---

**由Agent Six（a6）开发**

🌐 [agxntsix.ai](https://agxntsix.ai)
💼 [LinkedIn](https://linkedin.com/in/agxntsix)
🎥 [YouTube](https://youtube.com/@agxntsix)
🐙 [GitHub](https://github.com/agxntsix)
📅 [预约咨询](https://cal.com/agxntsix)