---
name: soulforge
description: "通过一个持久的后台守护进程，可以从 YAML 定义中将多步骤的编码工作流程调度到 Claude Code CLI 或 Codex CLI。适用于以下场景：  
(1) 实现端到端的功能开发流程（规划 → 实现 → 验证 → 提交 Pull Request）；  
(2) 在您进行其他工作时，将编码任务委托给后台自动执行；  
(3) 运行需要人工审核的检查点的开发工作流程；  
(4) 自动化功能分支的创建、实现以及 Pull Request 的提交。  
需要使用 @ghostwater/soulforge 这个 npm 包。"
repository: "https://github.com/ghostwater-ai/soulforge"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires":
          {
            "bins": ["soulforge", "claude", "gh"],
            "env": ["GITHUB_TOKEN or gh auth login"],
            "optional_bins": ["codex"],
          },
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

Soulforge 是一个基于守护进程的工作流引擎，它将编码任务分配给 Claude Code CLI 或 Codex CLI，并在各个阶段设置人工审核的检查点。

## 安全性与数据流

### 该工具对外发送的数据：
- **模型 CLI（claude/codex）：** 仓库内容和提示会被发送到配置的模型提供者（Anthropic、OpenAI）。仅在你同意数据暴露的情况下，这些数据才会被发送。
- **回调：** 运行元数据（运行 ID、任务描述、步骤状态）会被发送到你通过 `--callback-url` 配置的 URL。切勿将回调指向不受控制的端点。避免在回调头部或正文模板中包含敏感信息。
- **GitHub：** 通过 `gh pr create` 命令创建 Pull Request (PR)，这需要使用已认证的 GitHub CLI。Soulforge 会在配置的仓库中执行推送操作并创建 PR。

### 所需凭证：
- 使用 `gh` CLI 创建 PR 时，必须先进行身份验证（`gh auth login`）。
- 必须安装并配置 Claude Code 或 Codex CLI，并设置 API 密钥。
- 回调 URL 和认证令牌由用户提供，请确保它们指向可信的本地端点。

## 快速入门

```bash
npm install -g @ghostwater/soulforge
soulforge daemon start
```

## 运行工作流

Soulforge 的主要命令是 `run-workflow`。目前只有一个内置的工作流：`feature-dev`。

### 工作流流程（以 `feature-dev` 为例）：
1. **plan**（claude-code, opus）：将任务分解为有序的用户故事。
2. **review-plan**（self）：暂停以等待人工审批；如果被拒绝，流程会返回到 `plan` 阶段并显示反馈。
3. **implement**（claude-code, opus）：循环执行每个用户故事，并逐一进行验证。
4. **verify**（claude-code, opus）：检查每个故事是否符合验收标准。
5. **test**（claude-code, opus）：运行集成测试或端到端测试。
6. **pr**（claude-code, opus）：通过 `gh pr create` 创建 PR。
7. **final-review**（self）：暂停以等待最终的人工审核。

### 默认配置（feature-dev）：
| 设置 | 默认值 | 可覆盖值 |
|---------|---------|----------|
| 执行器 | `claude-code` | 在工作流 YAML 中指定 |
| 模型 | `opus`（自动选择最新版本） | 在工作流 YAML 中指定 |
| 超时时间 | 每个步骤 600 秒 | 在工作流 YAML 中指定 |
| 最大重试次数 | 2 | 在工作流 YAML 中指定 |
| 工作目录（worktree） | 自动创建 | 可使用 `--no-worktree` 或 `--workdir` 选项覆盖 |
| 分支名称 | `soulforge/<short-run-id>` | 可使用 `--branch <name>` 选项覆盖 |

### Git 工作目录（worktree）的行为：
- 当 `--var repo=<path>` 指定一个 Git 仓库时，Soulforge 会**自动创建一个工作目录**：
  - **裸目录+工作目录布局**（`.bare/` + `main/`）：工作目录会创建在 `worktrees/` 目录下。
  - **标准的 `.git` 目录布局**：工作目录会创建在仓库内的 `worktrees/` 目录中。
  - 如果不是 Git 仓库，Soulforge 会报错（此时请使用 `--workdir` 选项）。

### 覆盖工作目录的行为：
- `--workdir /some/path`：使用现有的目录，不执行任何 Git 操作。
- `--no-worktree`：直接在仓库中进行操作，不创建工作目录。
- `--branch my-branch`：自定义分支名称，替代默认的 `soulforge/<id>`。

`--workdir` 和 `--var repo=` 是互斥的。

## 检查点（approve/reject）：
当步骤的执行器设置为 `self` 时，流程会暂停并等待用户输入。

### 拒绝操作后的处理：
如果某个检查点设置了 `on_reject.reset_to`（例如，`review-plan` → `plan`），拒绝操作会将流程重置到该步骤。你的拒绝理由会以 `{{rejection_feedback}}` 的形式传递给该步骤的下一次执行。

如果没有设置 `on_reject`，系统会重新尝试执行相同的步骤。

## 监控

```bash
soulforge status                # active runs overview
soulforge status <query>        # filter by run ID prefix or task substring
soulforge runs                  # all runs (including completed)
soulforge events --run <id>     # event log for a run
soulforge events --follow       # stream all events
soulforge logs 50               # last 50 daemon log lines
```

## 生命周期命令

```bash
soulforge cancel <run-id>       # kill a running workflow
soulforge resume <run-id>       # retry a failed run from the failed step
soulforge daemon start          # start daemon (background)
soulforge daemon start -f       # start daemon (foreground, for debugging)
soulforge daemon stop           # stop daemon
soulforge daemon status         # check if daemon is running
```

### 回调（与框架无关）：
Soulforge 可以在运行或步骤发生事件时向任何 URL 发送请求。Soulforge 不了解接收回调的服务器的具体实现，回调的路由由调用者自行处理。
`--callback-url` 是必填参数。使用 `--no-callback` 可以完全禁用所有回调（包括运行完成的通知）。

### 回调中的模板变量：
`--callback-body` 中包含以下变量：`{{run_id}}`, `{{status}}`, `{{task}}`, `{{step_id}}`, `{{step_status}}`。

### 每个步骤的回调触发条件：
工作流步骤可以通过 `notify` 字段指定哪些事件会触发回调。

```yaml
steps:
  - id: implement
    executor: claude-code
    notify: [on_complete, on_fail]   # callback on complete or failure
    input: "Implement the feature"

  - id: review
    executor: self
    # self executor defaults to [on_waiting] — always notifies on checkpoint
    input: "Review the implementation"
```

### 默认通知行为：
对于未指定回调触发条件的步骤，工作流会使用全局的默认通知行为（`on_complete`, `on_waiting`, `on_fail`）。

### 自动执行步骤（检查点）：
如果步骤未指定回调触发条件，系统会自动使用 `[on_waiting]` 作为默认通知方式。这意味着检查点总是会触发通知。

## 规范：使用 GitHub 问题来定义工作流规范：
详细的工作流规范应编写成 GitHub 问题，并在工作流任务中引用这些问题。

```bash
soulforge run feature-dev \
  "Fix GitHub issue #5: https://github.com/org/repo/issues/5 — implement reject loopback" \
  --var repo=/path/to/project
```

执行器会读取问题的 URL 并据此执行相应的操作。这样可以避免规范文件被孤立或丢失。

## 先决条件：
- 安装 `soulforge` CLI：`npm install -g @ghostwater/soulforge`
- 安装 `claude` CLI（用于执行代码任务）
- 使用已认证的 GitHub CLI（`gh auth login`）来创建 PR
- 需要 Git 来管理工作目录和分支

## 工作流格式：
有关完整的 YAML 架构、模板变量、循环步骤以及如何编写自定义工作流的详细信息，请参阅 [references/workflow-format.md](references/workflow-format.md)。