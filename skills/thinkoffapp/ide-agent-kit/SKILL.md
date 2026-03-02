---
name: ide-agent-kit
description: 文件系统消息总线（Filesystem Message Bus）和Webhook中继（Webhook Relay）用于多代理集成开发环境（IDE）的协调。当代理需要共享事件、轮询Ant Farm房间、接收GitHub/GitLab的Webhook通知、在不同会话间协调任务或运行定时作业时，这些功能非常有用。系统默认优先使用本地通信方式（即不依赖网络），并在以下情况下触发相应的操作：代理间通信、Webhook事件被接收、房间状态被轮询、定时任务被执行（通过cron调度），或tmux命令被运行。
version: 0.4.0
metadata:
  openclaw:
    requires:
      bins: [node]
      env: []
    homepage: https://github.com/ThinkOffApp/ide-agent-kit
    install:
      - kind: node
        package: ide-agent-kit
        bins: [ide-agent-kit]
---
# IDE Agent Kit

通过 OpenClaw，将您的 IDE 编码代理连接到实时团队中。该工具支持基于文件系统的消息传递机制、房间轮询、自动化规则以及多模型代理协调功能，且完全无需依赖任何外部服务。

## 安全模型

该工具分为两个层级：

**基础层（仅限本地使用，无需凭证）：**
- 本地文件系统队列和接收日志：代理在工作目录中读写文件。
- `init`、`receipt tail`、`memory`（本地后端）：不使用网络，也不存储任何敏感信息。
- `serve` 默认仅绑定到 `127.0.0.1`，用于接收 Webhook 并将数据写入本地队列。

**高级层（需要明确启用及提供凭证）：**
- `sessions`、`gateway`：与 OpenClaw 代理服务器通信（需要配置 `openclaw.token`）。
- `poll`：连接到 Ant Farm 房间以实现跨机器协作（需要 `--api-key` 参数）。
- `emit`、`hooks create`：将数据发送到用户指定的外部 URL。
- `tmux run`、`exec`：执行 shell 命令（仅允许执行配置文件中列出的命令）。

所有高级功能均需通过配置才能启用。默认的 `init` 配置文件中，凭证字段为空，允许执行的命令也非常有限。

### 网络行为

| 命令        | 出站连接                | 入站连接                |
|-------------|-------------------|---------------------|
| `init`, `receipt tail`, `memory` (local) | 无                    | 无                    |
| `serve`       | 仅绑定到 localhost:8787         | （可配置）                |
| `poll`       | 连接到 Ant Farm API (HTTPS)       | 无                    |
| `sessions`, `gateway` | 默认绑定到 OpenClaw 代理服务器 | 无                    |
| `emit`       | 用户指定的 URL             | 无                    |
| `hooks create` | 用户指定的 webhook URL         | 无                    |

### 命令执行

`tmux run` 和 `exec` 仅会执行配置文件中 `tmux.allow` 列出的命令。默认允许执行的命令包括：`npm test`、`npm run build`、`pytest`、`git status`、`git diff`。未列出的命令将被拒绝执行。

执行命令前，系统会先通过 `exec request` 过程进行人工审核或代理处理。

## 快速入门

```bash
npm install -g ide-agent-kit
ide-agent-kit init --ide claude-code
```

创建一个名为 `ide-agent-kit.json` 的配置文件。所有凭证字段均为空。在配置完成之前，该工具不会与任何服务器建立连接。

## 连接方式

共有四种连接模式，可以自由组合使用。默认情况下，仅启用第一种模式（本地文件系统模式）。

### 1. 本地文件系统模式（默认）

同一台机器上的代理通过共享的队列目录和接收日志进行通信。无需网络连接或 API 密钥。

- 队列文件：`./ide-agent-queue.jsonl`
- 接收日志文件：`./ide-agent-receipts.jsonl`

### 2. Webhook 中继服务器（可选）

接收来自 GitHub/GitLab 的 Webhook 并将其写入本地事件队列。

```bash
ide-agent-kit serve [--config <path>]
```

默认情况下，该模块绑定到 `127.0.0.1:8787`。需在配置文件中设置 `github.webhook_secret` 以验证 Webhook 签名。该模块不进行出站连接。

### 3. Ant Farm 房间轮询（可选）

用于实现跨机器间的协作。

```bash
ide-agent-kit poll --rooms <room1,room2> --api-key <key> --handle <@handle> [--interval <sec>]
```

**要求：** 需要 `--api-key` 参数（Ant Farm API 密钥）。该功能会限制请求频率，默认间隔为 120 秒。

### 4. GitHub 事件（可选）

当 `serve` 模块运行时，可以将 GitHub 的 Webhook 事件转发到本地队列。该功能可将 PR/Issue/CI 事件转换为本地事件。

**要求：** 需要在配置文件中设置 `github.webhook_secret` 以验证传入的 Webhook 签名。

## 命令列表

### 基础层（仅限本地使用，无需凭证）

| 命令            | 功能                        |
|-----------------|---------------------------|
| `init [--ide <name>] [--profile <balanced\|low-friction>] | 生成初始配置文件                |
| `receipt tail [--n <count>]     | 打印最近的 N 条接收记录             |
| `watch [--config <path>]      | 监控事件队列，并在新事件发生时通知 IDE 会话     |
| `serve [--config <path>]      | 启动 Webhook 中继服务器（仅限本地）         |
| `memory list\|get\|set\|search`   | 管理代理的内存状态                 |
| `keepalive start\|stop\|status` | 防止 macOS 系统进入睡眠状态           |

### 高级层（需要凭证或明确配置）

| 命令            | 必需的参数                | 功能                        |
|-----------------|---------------------------|---------------------------|
| `sessions send --agent <id> --message <text>` | 通过代理服务器发送消息                |
| `sessions spawn --task <text>` | 创建新的代理会话                   |
| `sessions list\|history\|status` | 查询代理会话状态                   |
| `gateway trigger\|health\|agents` | 操作代理服务器                   |
| `poll --rooms <r> --api-key <k> --handle <h>` | 通过 Ant Farm API 查询房间状态           |
| `emit --to <url> --json <file>` | 将事件数据发送到指定 URL                |
| `hooks create --webhook-url <url>` | 创建 Webhook 转发器                   |
| `tmux run --cmd <command>` | 仅允许执行指定命令                | 在 tmux 中执行命令并记录接收结果       |
| `exec request\|resolve\|list` | 执行命令前需人工审核                |
| `cron add\|list\|remove\|run\|status` | 管理定时任务                     |

## 配置文件说明

配置文件由 `ide-agent-kit init` 生成。所有凭证字段默认为空。

| 参数            | 用途                          | 默认值                        |
|-----------------|---------------------------|---------------------------|
| `listen.host`       | Webhook 服务器绑定地址             | `127.0.0.1`                    |
| `listen.port`       | Webhook 服务器端口                 | `8787`                        |
| `tmux.allow`       | 允许执行的 shell 命令                | `[npm test, npm run build, pytest, git status, git diff]` |
| `openclaw.token`     | 代理服务器认证密钥（高级功能）            | 空                          |
| `github.webhook_secret` | 用于验证 GitHub Webhook 签名           | 空                          |

## 数据访问权限

| 文件路径          | 访问权限                | 用途                          |
|-----------------|---------------------------|-----------------------------------|
| `ide-agent-receipts.jsonl` | 只读                         | 所有代理操作的审计日志                   |
| `ide-agent-queue.jsonl` | 读写                         | 事件队列                         |
| `ide-agent-kit.json`    | 读                         | 运行时配置文件（可能包含敏感信息）             |
| `memory/`         | 读写                         | 本地代理内存文件                     |

## 项目信息与验证方式

- **npm 包来源：** https://www.npmjs.com/package/ide-agent-kit
- **代码仓库：** https://github.com/ThinkOffApp/ide-agent-kit
- **维护者：** petruspennanen (npm)、ThinkOffApp (GitHub)
- **许可证：** AGPL-3.0

该 npm 包不包含安装脚本（`preinstall`/`postinstall`）。所有代码均采用纯 ESM JavaScript 编写。安装前建议使用 `npm pack --dry-run` 进行验证。