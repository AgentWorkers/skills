---
name: oneshot-ship
description: 使用 `oneshot CLI` 自动提交代码：该工具通过一个命令完成代码的规划、执行、审查以及提交 PR 的整个流程。支持通过 SSH 连接远程服务器，也支持在本地运行。适用于用户希望自动提交代码更改、自动化 PR 流程，或结合 Claude 和 Codex 使用自主编码流程的场景。
license: MIT
metadata:
  author: ADWilkinson
  version: "0.0.1"
  repository: "https://github.com/ADWilkinson/oneshot-cli"
compatibility: Requires Bun, Claude Code CLI, Codex CLI, and GitHub CLI. SSH access to a server optional (can run locally with --local)
---
# oneshot CLI

使用单个命令即可完成代码的提交。oneshot CLI 会自动执行整个流程：计划（Claude）→ 执行（Codex）→ 审查（Codex）→ 提交 Pull Request（PR）（Claude）。该工具可以通过 SSH 连接到远程服务器，也可以通过 `--local` 选项在本地运行。

## 适用场景

- 用户希望无需手动编写代码即可将代码更改提交到仓库。
- 用户希望自动化计划、执行、审查和提交 Pull Request 的工作流程。
- 用户提到“oneshot”或“oneshot CLI”，或者希望实现自动化的代码提交功能。
- 用户希望将编码任务委托给远程服务器或在本地执行。

## 安装

```bash
bun install -g oneshot-ship
```

## 配置

运行 `oneshot init` 命令来配置 SSH 主机、工作区路径、API 密钥以及模型偏好设置。配置信息会保存在 `~/.oneshot/config.json` 文件中。

服务器上的仓库应按照 `<org>/<repo>` 的结构组织在工作区路径下：

```
~/projects/
  my-org/my-app/
  my-org/my-api/
```

### 服务器要求

- [Bun](https://bun.sh)
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- [Codex CLI](https://github.com/openai/codex)
- [GitHub CLI](https://cli.github.com)（已登录）
- 环境变量中需设置 `ANTHROPIC_API_KEY` 和 `OPENAI_API_KEY`。

## 使用方法

### 基本用法

```bash
oneshot <repo> "<task>"
```

### 结合 Linear 票务系统使用

```bash
oneshot <repo> <linear-url>
```

该工具会获取相关票务信息，并在创建 Pull Request 后更新其状态。

### 本地模式

```bash
oneshot <repo> "<task>" --local
```

直接在当前机器上运行整个流程，无需通过 SSH 连接到服务器。需要本地安装 Claude Code CLI、Codex CLI 和 GitHub CLI。

### 后台模式

```bash
oneshot <repo> "<task>" --bg
```

以后台模式运行流程（仅支持 SSH 连接）。

### 干运行

```bash
oneshot <repo> --dry-run
```

仅验证仓库是否存在，而不实际执行流程。

### 更改使用模型

```bash
oneshot <repo> "<task>" --model sonnet
```

## 流程步骤

1. **验证**：检查仓库是否存在，并从远程仓库获取最新代码。
2. **创建工作区**：从 `origin/main` 创建一个临时的 Git 工作区，并自动检测并安装依赖项（bun/pnpm/yarn/npm）。
3. **计划**：Claude 读取代码库及 `CLAUDE.md` 中的规范，生成执行计划。
4. **执行**：Codex 根据计划执行代码。
5. **审查**：Codex 自动检查代码中的错误、类型问题及安全漏洞。
6. **提交 Pull Request**：Claude 创建新分支、提交代码并打开 Pull Request。

每次运行后，临时工作区都会被清理干净。

## 配置文件

`~/.oneshot/config.json`：

```json
{
  "host": "user@100.x.x.x",
  "basePath": "~/projects",
  "anthropicApiKey": "sk-ant-...",
  "linearApiKey": "lin_api_...",
  "claude": { "model": "opus", "timeoutMinutes": 180 },
  "codex": { "model": "gpt-5.3-codex", "reasoningEffort": "xhigh", "timeoutMinutes": 180 },
  "stepTimeouts": {
    "planMinutes": 20,
    "executeMinutes": 60,
    "reviewMinutes": 20,
    "prMinutes": 20
  }
}
```

只需配置 `host` 参数，其他参数均使用默认值。

## 常用参数

| 参数 | 缩写 | 说明 |
|------|-------|-------------|
| `--model` | `-m` | 更改使用的 Claude 模型 |
| `--dry-run` | `-d` | 仅进行验证 |
| `--local` | | 在本地运行，而非通过 SSH |
| `--bg` | | 以后台模式运行（仅支持 SSH） |
| `--help` | `-h` | 显示帮助信息 |
| `--version` | `-v` | 显示版本信息 |

## 自定义设置

- 在任意仓库根目录下放置 `CLAUDE.md` 文件，以强制使用指定的代码规范；oneshot 会将其作为上下文传递给 Claude 和 Codex。
- 通过编辑 `prompts/plan.txt`、`execute.txt`、`review.txt`、`pr.txt` 文件来自定义流程行为。

## 使用建议

- 对于耗时较长的任务，使用 `--bg` 选项以方便后台运行。
- 当使用 Linear 票务系统时，该工具会自动将票务状态更新为“待审查”并添加相应的 Pull Request 评论。
- 每个步骤都设置了超时时间（默认值：计划 20 分钟、执行 60 分钟、审查 20 分钟、提交 Pull Request 20 分钟）。
- oneshot CLI 会为每个任务创建独立的工作区，确保主分支不受影响。