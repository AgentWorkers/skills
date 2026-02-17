---
name: soulforge
description: "通过一个持续运行的后台守护进程，可以将多步骤的编码工作流程从 YAML 定义中调度到 Claude Code CLI 或 Codex CLI。适用场景包括：  
(1) 实现端到端的功能开发流程（计划 → 实现 → 验证 → 提交 Pull Request）；  
(2) 在您进行其他工作时，将编码任务委托给后台自动执行；  
(3) 运行需要人工审核的检查点的开发工作流程；  
(4) 自动化功能分支的创建、实现以及 Pull Request 的提交。  
该功能需要依赖 @ghostwater/soulforge 这个 npm 包。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "bins": ["soulforge", "claude", "gh", "git"], "env": [] },
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

Soulforge 是一个基于守护进程的工作流引擎，它将编码步骤分配给执行器（如 Claude Code 或 Codex），并在需要人工审核的节点暂停执行流程。

## 安装与启动

```bash
npm install -g @ghostwater/soulforge
soulforge daemon start
```

## 核心工作流流程

```bash
# Run a feature-dev workflow against a repo
soulforge run feature-dev "Add user authentication with JWT tokens" \
  --var repo=/path/to/project \
  --var build_cmd="npm run build" \
  --var test_cmd="npm test"
```

Soulforge 会自动创建一个 Git 工作区（worktree），然后按照以下顺序执行任务：**计划 → 审核 → 实现 → 验证 → 测试 → 提交代码请求（PR）→ 最终审核**。

使用执行器 `self` 的步骤会在需要人工批准时暂停：

```bash
soulforge approve <run-id>              # approve checkpoint
soulforge reject <run-id> --reason "…"  # reject with feedback
```

## 关键命令

| 命令 | 功能 |
|---------|-------------|
| `soulforge run <workflow> "<task>" [flags]` | 启动一个工作流 |
| `soulforge status [<query>]` | 检查工作流状态（通过 ID 或任务名称查询） |
| `soulforge runs` | 列出所有正在运行的工作流 |
| `soulforge approve <run-id>` | 批准某个工作流节点 |
| `soulforge reject <run-id> --reason "…"` | 拒绝某个工作流节点 |
| `soulforge cancel <run-id>` | 取消正在运行的工作流 |
| `soulforge resume <run-id>` | 恢复失败的工作流 |
| `soulforge events [--run <id>] [--follow]` | 流式查看工作流事件 |
| `soulforge logs [<lines>]` | 查看守护进程日志 |
| `soulforge daemon start/stop/status` | 管理守护进程 |

## 运行参数

- `--var key=value` — 传递变量（例如 `repo`、`build_cmd`、`test_cmd`）
- `--workdir <path>` — 使用指定的目录而不是自动创建工作区 |
- `--no-worktree` — 直接在 Git 仓库中操作（不创建工作区） |
- `--branch <name>` — 自定义分支名称（默认值：根据任务名称自动生成） |
- `--callback-url <url>` | 在工作流完成时发送 POST 请求到指定 URL （详见下文关于回调的部分） |
- `--callback-headers <json>` | 回调请求的头部信息 |
- `--callback-body <json>` | 回调请求的正文模板，其中包含 `{{run_id}}`、`{{status}}`、`{{task}}` 等占位符 |

## 回调机制

Soulforge 支持与具体框架无关的回调机制。工作流完成时，它会将数据发送到您配置的 URL：

```bash
soulforge run feature-dev "Add caching layer" \
  --var repo=/path/to/project \
  --callback-url "http://127.0.0.1:18789/hooks/agent" \
  --callback-headers '{"Authorization":"Bearer <token>","Content-Type":"application/json"}' \
  --callback-body '{"message":"Soulforge run {{run_id}} finished: {{status}}. Task: {{task}}","sessionKey":"<your-session-key>"}'
```

回调系统的实现细节对 Soulforge 是不可知的——Soulforge 不知道数据会被发送到哪里，具体的路由由调用方负责处理。

## 先决条件

使用 Soulforge 需要以下工具：
- **`soulforge` CLI** — 通过 `npm install -g @ghostwater/soulforge` 全局安装（[源代码](https://github.com/ghostwater-ai/soulforge)，维护者：`@ghostwater`）
- **`claude` CLI** 或 **`codex` CLI** — 实际执行代码的执行器 |
- **`gh` CLI** — 用于创建代码提交请求（PR） |
- **`git` — 用于创建工作区和分支管理 |

凭据由相应的执行器 CLI 管理，而非 Soulforge。

## 安全注意事项

- **回调功能是可选的** — Soulforge 仅会向您通过 `--callback-url` 指定的 URL 发送数据。除非您信任接收方，否则不要在 `--callback-headers` 或 `--callback-body` 中包含任何敏感信息。建议使用本地地址或内部 URL。
- **守护进程的权限范围** — 守护进程可以使用执行器所拥有的凭据来修改仓库和调用其他 CLI。请先在非敏感仓库上进行测试。
- **权限控制** — 确保 `gh`、`claude`/`codex` 的权限设置仅限于执行所需的最小范围。

## 工作流格式

有关完整的 YAML 格式及如何编写自定义工作流的详细信息，请参考 [references/workflow-format.md](references/workflow-format.md)。

## 规范编写方式

请将工作流的具体规范以 GitHub 问题的形式编写，并在任务字符串中引用该问题的链接：

```bash
soulforge run feature-dev "Find the full task https://github.com/org/repo/issues/42" \
  --var repo=/path/to/project
```

执行器会读取问题的链接并据此执行相应的操作。

## Git 工作区行为

默认情况下，当 `--var repo=<path>` 指定一个 Git 仓库时：
- **Bare+worktree 架构**：在 `worktrees/` 目录下创建工作区（格式为 `.bare/` + `main/`）
- **标准 `.git` 架构**：在仓库内的 `worktrees/` 目录下创建工作区
- **如果未指定 Git 仓库**：直接在仓库内进行操作（不执行 Git 操作）

您可以通过 `--workdir`（使用指定目录）或 `--no-worktree`（直接在仓库中操作）来修改这些行为。