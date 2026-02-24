---
name: soulforge
description: "通过一个持久的后台守护进程，可以从 YAML 定义中将多步骤的编码工作流程调度到 Claude Code CLI 或 Codex CLI。适用场景包括：(1) 从头到尾实现一个功能；(2) 运行包含人工检查点的错误修复工作流程；(3) 在后台委托编码任务；(4) 管理自定义工作流程（如列出、显示或创建工作流程）。该功能需要依赖 @ghostwater/soulforge 库。"
repository: "https://github.com/ghostwater-ai/soulforge"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires":
          {
            "bins": ["soulforge", "gh"],
            "env": ["GITHUB_TOKEN or gh auth login"],
            "optional_bins": ["claude", "codex"],
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

这是一个基于守护进程的工作流引擎，用于管理编码工作流程，并支持可选的人工检查点（ checkpoints）。

## 主要更新（当前功能）

- 使用 `--workdir` 参数是运行 `soulforge` 的必要条件。
- 内置的工作流包括：`feature-dev` 和 `bugfix`。
- 可以通过以下命令自定义工作流管理：
  - `soulforge workflow list`：列出所有工作流
  - `soulforge workflow show <name>`：查看指定工作流的详细信息
  - `soulforge workflow create <name> [--from <template>] [--force]`：创建新的工作流
- 工作流的执行支持内置工作流、自定义工作流以及路径回退机制。
- 结构化输出步骤采用基于模式的自动补全功能（`soulforge complete`），该功能会注入相应的补全指令。
- 旧的基于文本的“预期结果”（expects）检查机制已被弃用/从运行时行为中移除。
- 修复 bug 的 PR 步骤具有幂等性（如果已经存在相应的 PR，则会重用该 PR）。

## 快速入门

```bash
npm install -g @ghostwater/soulforge
soulforge daemon start
```

## 运行工作流

```bash
soulforge run feature-dev "Implement issue #123" --workdir /path/to/repo
```

**常用选项：**

```bash
--executor codex-cli|claude-code
--model <model-name>
--callback-url <url>
--callback-exec '<shell command>'
--no-callback
```

## 检查点（Checkpoints）

```bash
soulforge status
soulforge approve <run-id>
soulforge reject <run-id> --reason "..."
```

## 自定义工作流（Custom Workflows）

自定义工作流存储在 `~/.soulforge/workflows/` 目录下。

## 结构化补全机制（Structured Completion）

对于结构化步骤，Soulforge 会注入相应的补全指令。这些指令需要满足步骤的 `output_schema` 规范。

## 监控与生命周期管理（Monitoring & Lifecycle）

```bash
soulforge status [query]
soulforge runs
soulforge events --run <id>
soulforge logs 100

soulforge cancel <run-id>
soulforge resume <run-id>

soulforge daemon start
soulforge daemon stop
soulforge daemon status
```

## 安全性 / 外部影响（Security / External Effects）

- 编码执行器可以将仓库内容发送给模型提供者（model providers）。
- 使用 `gh` 命令来处理 Pull Request（PR）操作。
- 回调端点（callback endpoints）会接收您配置的运行/步骤元数据。

**仅在与您信任的仓库/端点上运行该工具。**

## 参考资料

- 工作流格式规范：[references/workflow-format.md](references/workflow-format.md)