---
name: soulforge
description: "通过一个持久的后台守护进程，可以从 YAML 定义中将多步骤的编码工作流程调度到 Claude Code CLI 或 Codex CLI 中执行。适用场景包括：  
(1) 实现端到端的功能开发流程（规划 → 实现 → 验证 → 提交 Pull Request）；  
(2) 将编码任务委托到后台执行，同时您可以继续处理其他工作；  
(3) 运行需要人工审核的检查点的开发工作流程；  
(4) 自动化功能分支的创建、实现以及 Pull Request 的提交。  
该功能需要依赖 @ghostwater/soulforge 这个 npm 包。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["soulforge", "claude", "gh"], "env": [] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": "@ghostwater/soulforge",
              "global": true,
              "bins": ["soulforge"],
              "label": "Install Soulforge CLI (npm)",
            },
          ],
      },
  }
---
# Soulforge

Soulforge 是一个基于守护进程的工作流引擎，它将编码任务分配给执行器（如 Claude Code 或 Codex），并在需要人工审核的节点暂停执行。

## 安装与启动

```bash
npm install -g @ghostwater/soulforge
soulforge daemon start
```

如果守护进程尚未运行，执行 `soulforge run` 命令即可自动启动它。

## 快速入门

```bash
# Run a feature-dev workflow
soulforge run feature-dev "Add user authentication with JWT tokens" \
  --workdir /path/to/project

# Run a bugfix workflow
soulforge run bugfix "Fix race condition in session handler" \
  --workdir /path/to/project \
  --var build_cmd="npm run build" \
  --var test_cmd="npm test"
```

`--workdir` 参数是**必需的**，它必须指向一个现有的目录。Soulforge 会自动从这个目录创建一个 Git 工作区（worktree）。

> ⚠️ `--var repo=` 参数已不再支持，请使用 `--workdir` 代替。

## 内置工作流

| 工作流 | 步骤 | 功能 |
|----------|-------|-------------|
| `feature-dev` | 规划 → 审核 → 实现 → 验证 → 测试 → 提交 PR → 代码审核 → 审核关卡 → 最终审核 | 包含故事分解的完整功能开发流程 |
| `bugfix` | 诊断 → 审核诊断 → 修复 → 验证 → 提交 PR → 代码审核 → 审核关卡 → 最终审核 | 首先修复失败测试的缺陷修复流程 |

这两种工作流默认使用 `codex-cli` 作为执行器，并采用 `gpt-5.3-codex` 模型。

## 关键命令

| 命令 | 功能 |
|---------|-------------|
| `soulforge run <工作流> "<任务>" [参数]"` | 启动一个工作流 |
| `soulforge status [<查询>]` | 检查工作流状态（通过 ID 或任务字符串查询） |
| `soulforge runs` | 列出所有正在运行的工作流 |
| `soulforge approve <运行ID> [--消息 "..."]` | 批准某个工作流节点 |
| `soulforge reject <运行ID> --原因 "…"` | 拒绝某个工作流节点并给出反馈（回滚到之前的步骤） |
| `soulforge complete --运行ID <ID> --步骤ID <ID> --数据 '<json>'` | 完成某个步骤（输出结构化数据） |
| `soulforge cancel <运行ID>` | 取消正在运行的工作流 |
| `soulforge resume <运行ID>` | 恢复失败的工作流 |
| `soulforge events [--运行 <ID>] [--跟随]` | 流式查看工作流事件 |
| `soulforge logs [<行>]` | 显示守护进程日志 |
| `soulforge daemon start/stop/status` | 管理守护进程 |
| `soulforge workflow list` | 列出可用的工作流 |
| `soulforge workflow show <名称>` | 显示某个工作流的 YAML 详情 |
| `soulforge workflow create <名称> [--来自 <模板>]` | 创建自定义工作流 |

## 运行参数

- `--workdir <路径>` — **必需**，指定项目目录（必须存在）
- `--var key=value` — 传递变量（例如 `build_cmd`、`test_cmd`）
- `--keep-worktree` — 在工作流完成后保留工作区的元数据和文件
- `--executor <名称>` — 为所有代码步骤指定执行器（例如 `codex-cli`、`claude-code`）
- `--model <名称>` — 为所有代码步骤指定模型（例如 `gpt-5.3-codex`、`opus`）
- `--callback-exec <命令>` | 用于步骤通知的 shell 命令回调（详见回调部分）
- `--no-callback` | 不使用任何回调

⚠️ `<任务>` 参数是一个**位置参数**，必须紧跟在工作流名称之后：

```bash
soulforge run feature-dev "Your task here" --workdir /path/to/project
```

## 回调机制

Soulforge 支持两种步骤通知回调机制：

### OpenClaw CLI 回调

```bash
soulforge run feature-dev "Add caching layer" \
  --workdir /path/to/project \
  --callback-exec 'openclaw agent --session-key "agent:myagent:slack:channel:c0123abc" --message "Soulforge run {{run_id}} step {{step_id}} status: {{step_status}}" --deliver'
```

自动将回调路由到正确的 OpenClaw 代理会话——无需额外的令牌或 HTTP 配置。

> **注意：** `--session-key` 参数需要使用 `ghostwater-ai/openclaw` 分支（该分支尚未合并到上游代码库中）。从 2026.2.26 版本开始支持。

### 模板变量

- `{{run_id}}` — 运行 ID
- `{{status}}` — 运行状态
- `{{task}}` — 原始任务字符串
- `{{step_id}}` — 当前步骤 ID
- `{{step_status}}` — 当前步骤状态

### 单步通知控制

步骤可以通过 `notify` 参数指定回调触发时机：
- `on_complete` — 步骤成功完成
- `on_waiting` — 步骤等待人工审核
- `on_fail` — 步骤失败

默认情况下，所有使用 `executor: self` 的步骤都会触发 `on_waiting` 回调。

## 审核关卡工作流

使用 `executor: self` 的步骤会在需要人工审核时暂停执行：

```bash
# Check what's waiting
soulforge status

# Approve a checkpoint (optionally with context)
soulforge approve <run-id> --message "Looks good, proceed"

# Reject with feedback (rewinds to the step defined in on_reject.reset_to)
soulforge reject <run-id> --reason "Stories are too granular, combine 3 and 4"
```

两种工作流中的审核关卡步骤都会使用 `gate` 类型进行条件路由：
- **pass** → 继续进入最终审核
- **fix** → 重新进入审核-修复-代码审核-审核关卡循环（最多 5 次）

## 执行器覆盖

可以指定执行代码步骤的 CLI：

```bash
# Use Claude Code instead of Codex
soulforge run feature-dev "Refactor auth module" \
  --workdir /path/to/project \
  --executor claude-code \
  --model opus
```

可用的执行器包括：`claude-code`、`codex-cli`、`codex`（旧版本）。此设置仅适用于代码步骤；使用 `executor: self` 的步骤（如审核关卡）不会被覆盖。

## 结构化步骤输出

使用 `output_schema` 的步骤会通过 `soulforge complete` 命令完成步骤输出，而不是直接使用标准输出（stdout）：

1. 运行器会自动将完成指令插入执行器的提示界面
2. 执行器调用 `soulforge complete --运行ID <ID> --步骤ID <ID> --数据 '<json>'`
3. 数据会根据预定义的格式进行验证
4. 如果执行器在未调用 `complete` 之前退出，运行器会尝试重新启动会话（最多尝试 3 次）

## Git 工作区行为

当 `--workdir` 指向一个 Git 仓库时：
- **Bare+worktree 布局**（`.bare/` + `main/`）：在 `worktrees/` 目录下创建工作区
- **标准 `.git` 布局**：在仓库内的 `worktrees/` 目录下创建工作区
- **非 Git 仓库**：直接在当前目录下操作

## 最佳实践（运营经验）

### 任务字符串
- **务必具体明确。** 如果没有限制，任务数量可能会膨胀到 10-12 个。请包含以下信息：
  - 尽可能提供具体的文件路径
  - 限制任务数量（例如“最多 3 个任务”）
  - **不要包含无关代码的修改或文档编写任务**
- 参考 GitHub 问题获取详细规范：`例如：“实现 https://github.com/org/repo/issues/42``

### 工作流管理
- **每台机器上运行一个守护进程**。来自不同安装路径的多个守护进程进程可能会共享同一个数据库，从而导致冲突。可以使用 `pgrep -af "soulforge.*daemon-entry"` 来终止异常进程。
- **检查守护进程状态**：`soulforge daemon status` 命令可以显示上次检查的时间——如果显示“may be hung”，则表示已超过 5 分钟未进行任何操作。
- **取消的工作流可能会留下未完成的步骤**。请使用 `soulforge cancel <运行ID>` 显式终止这些步骤；如果步骤卡住，需要重启守护进程。

### 审核关卡工作流
- 代码审核 → 审核关卡 → 修复的流程会将发现的问题以 PR 评论的形式提交（作为审计记录）
- 审核关卡的判断标准：修复与任务相关的问题；将范围扩展的问题单独提交为新问题
- 审核关卡的执行器为 `executor: self`——由调用者（即你）来处理判断

### 构建/测试流程
- 工作流会指示执行器从 `AGENTS.md` 和仓库脚本中获取任务信息
- 对于缺陷修复工作流，请明确指定 `--var build_cmd=` 和 `--var test_cmd=` 参数以确保可靠性
- 特色开发工作流依赖于 `AGENTS.md` 文件中的任务信息——请确保目标仓库中包含该文件

## 先决条件

- **`soulforge` CLI**：`npm install -g @ghostwater/soulforge`
- **`codex` CLI` 或 `claude` CLI`：用于执行代码的执行器（需要使用相应的模型进行认证）
- **`gh` CLI`：用于创建 PR（需要通过 `gh auth login` 进行认证）
- **Git**：用于创建工作区和分支管理

### 凭据要求

Soulforge 本身不需要 API 密钥或令牌。所有认证操作均由相应的 CLI 处理：
- **GitHub**：使用 `gh auth login` 进行认证（用于创建 PR、提交问题、编写代码审核评论）
- **Claude Code**：需要 Anthropic API 密钥或 OAuth（由 `claude` CLI 管理）
- **Codex CLI**：需要 OpenAI API 密钥或 OAuth（由 `codex` CLI 管理）

Soulforge 不需要设置任何环境变量——它将所有认证操作委托给底层的 CLI 工具。

## 环境变量

- `SOULFORGE_DATA_DIR` — 数据目录的路径（默认值：`~/.soulforge`）

## 工作流格式参考

有关完整的 YAML 格式、步骤类型、关卡路由、循环配置和模板变量的详细信息，请参阅 [references/workflow-format.md]。