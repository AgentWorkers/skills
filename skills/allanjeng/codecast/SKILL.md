---
name: codecast
description: 通过 Webhook 将 Stream 编码代理会话（如 Claude Code、Codex、Gemini CLI 等）实时传输到 Discord 频道。适用于在调用编码代理时，需要实现透明、可观察的开发会话场景——避免出现“黑箱”现象。该工具能够将 Claude Code 生成的 stream-json 输出解析为格式规范的 Discord 消息，其中包含工具调用、文件操作、bash 命令及执行结果，且完全不消耗任何 AI 许可证（AI tokens）。适用于需要“将输出内容流式传输到 Discord”、“中继代理输出”或“使开发会话可见”的场景。
metadata: {"openclaw":{"emoji":"🎬","requires":{"anyBins":["unbuffer","python3"]}}}
---

# Codecast

这是一个用于将实时编码会话直播到 Discord 的工具。它提供了透明化的操作界面，让您能够看到所有的工具调用、文件写入操作以及 Bash 命令的执行过程，且完全不消耗任何 AI 令牌。

## 工作原理

```
┌──────────┐  stream-json  ┌──────────────┐  platform  ┌──────────┐
│ Claude   │ ────────────→ │ parse-stream │ ────────→ │ Discord  │
│ Code -p  │               │ .py          │           │ #channel │
└──────────┘               └──────────────┘           └──────────┘
┌──────────┐    --json     │              │           │          │
│ Codex    │ ────────────→ │  (auto-      │ ────────→ │          │
│ exec     │               │   detected)  │           │          │
└──────────┘               └──────────────┘           └──────────┘
```

- Claude Code 以 `-p`（打印）模式运行，并使用 `--output-format stream-json --verbose` 参数来输出格式化的 JSON 数据。
- Codex 使用 `--json` 参数生成结构化的 JSONL 格式事件数据。
- `parse-stream.py` 负责读取 JSON 数据，自动识别代理的通信格式，并通过平台适配器将格式化后的消息发送出去。
- 平台适配器（目前支持 Discord）负责处理消息的发送和线程管理。
- `unbuffer` 工具用于防止 Claude Code 的标准输出被缓冲（仅适用于 Claude Code）。
- 非 Claude/非 Codex 代理则直接以原始的 ANSI 格式输出数据。
- 通过 `-r` 参数可以配置每 60 秒的发送频率上限，以避免 webhook 被限制。
- 系统会在启动时清理超过 7 天旧的中间输出目录。

## 首次设置

安装该工具后，请按照以下步骤进行配置：

### 1. 使脚本可执行

```bash
chmod +x {baseDir}/scripts/dev-relay.sh {baseDir}/scripts/parse-stream.py
```

### 2. 创建 Discord Webhook

在目标 Discord 频道中通过 Discord API 或服务器设置 → 集成 → Webhook 功能来创建一个 webhook。

**如果您的机器人具有 MANAGE_WEBHOOKS 权限：**
```bash
curl -s -X POST "https://discord.com/api/v10/channels/<CHANNEL_ID>/webhooks" \
  -H "Authorization: Bot <BOT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Codecast"}'
```

保存 webhook 的 URL：
```bash
echo "https://discord.com/api/webhooks/<ID>/<TOKEN>" > {baseDir}/scripts/.webhook-url
chmod 600 {baseDir}/scripts/.webhook-url
```

### 3. （仅适用于 Claude Code）跳过权限验证步骤

如果 `~/.claude/settings.json` 文件不存在，请创建它：
```json
{
  "permissions": {
    "defaultMode": "bypassPermissions",
    "allow": ["*"]
  }
}
```

### 4. 安装 `unbuffer` 工具

```bash
brew install expect    # macOS
apt install expect     # Linux
```

### 5. 机器人令牌（可选，用于 --thread 模式）

**建议使用 macOS 的 Keychain 存储令牌（避免将令牌以明文形式保存在磁盘上）**
```bash
security add-generic-password -s discord-bot-token -a codecast -w YOUR_BOT_TOKEN
```

在运行 Codecast 之前，请先导出令牌：
```bash
export CODECAST_BOT_TOKEN=$(security find-generic-password -s discord-bot-token -a codecast -w)
```

**备用方案：使用文件存储令牌**
```bash
echo "YOUR_BOT_TOKEN" > {baseDir}/scripts/.bot-token
chmod 600 {baseDir}/scripts/.bot-token
```

### 6. 验证设置

```bash
bash {baseDir}/scripts/test-smoke.sh
```

系统会检查 webhook 是否可以正常访问、所需的可执行文件是否齐全、脚本的权限是否正确设置，以及平台适配器是否能够正常加载。

## 使用方法

安装完成后，请执行以下命令使脚本可执行：
```bash
chmod +x {baseDir}/scripts/dev-relay.sh {baseDir}/scripts/parse-stream.py
```

### 推荐使用 OpenClaw

**⚠️ 必须使用 `nohup` 命令来运行 Codecast，因为 `exec background:true` 会导致长时间运行的会话被强制终止。** 详情请参考 [代理集成文档](#agent-integration)。

```bash
exec command:"nohup {baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Build a REST API for todos. When finished, run: openclaw system event --text \"Done: built REST API\" --mode now' > /tmp/codecast.log 2>&1 & echo PID:\$!"
```

### 直接使用方法

```bash
bash {baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Build auth module. When finished, run: openclaw system event --text "Done: auth module built" --mode now'
```

### 常用选项

| 标志 | 描述 | 默认值 |
|------|------------|---------|
| `-w <目录>` | 工作目录 | 当前目录 |
| `-t <秒>` | 超时时间 | 1800 秒（30 分钟） |
| `-h <秒>` | 挂起阈值 | 120 秒 |
| `-i <秒>` | 发送间隔 | 10 秒 |
| `-n <名称>` | 代理显示名称 | 自动检测 |
| `-r <数量>` | 每 60 秒的发送次数上限 | 25 次 |
| `-P <平台>` | 聊天平台 | discord |
| `--thread` | 将消息发送到 Discord 的特定线程 | 关闭 |
| `--skip-reads` | 隐藏读取工具相关的事件 | 关闭 |
| `--resume <目录>` | 从中间输出目录重新开始会话 | 不适用 |
| `--review <URL>` | PR 评审模式 | 不适用 |
| `--parallel <文件>` | 并行任务模式 | 不适用 |

### 线程模式

所有消息会被发送到同一个 Discord 线程中，以保持聊天记录的整洁：
```bash
bash {baseDir}/scripts/dev-relay.sh --thread -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Refactor auth'
```

### 会话恢复

您可以重新开始之前的会话（例如，将会话内容发送到另一个频道或在新 webhook 设置后继续）：
```bash
bash {baseDir}/scripts/dev-relay.sh --resume /tmp/dev-relay.XXXXXX
```

会话开始时会显示中间输出目录的路径（例如：`📂 Relay: /tmp/dev-relay.XXXXXX`）。

### Codex 的结构化输出

Codex 的命令行界面支持使用 `--json` 参数生成结构化的 JSONL 数据。`parse-stream.py` 会自动解析这些数据，并生成与 Claude Code 相同格式的 Discord 输出：

```bash
bash {baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- codex exec --json --full-auto 'Fix all test failures. When finished, run: openclaw system event --text "Done: tests fixed" --mode now'
```

解析器会从第一个 JSON 数据中自动识别输出格式，因此无需额外设置。

### PR 评审模式

您可以使用 Codecast 与 Pull Request 评审流程结合，将评审过程实时直播到 Discord：

```bash
bash {baseDir}/scripts/dev-relay.sh --review https://github.com/owner/repo/pull/123
```

具体操作包括：
1. 将仓库克隆到一个临时目录。
2. 检出 PR 分支。
3. 运行代码评审工具并显示评审结果。
4. 如有需要，可以将评审结果作为 GitHub PR 评论发送。

**评审模式的额外选项**（在提供 PR URL 之前使用）：

| 标志 | 描述 | 默认值 |
|------|------------|---------|
| `-a <代理>` | 使用的代理（claude 或 codex） | claude |
| `-p <提示语>` | 自定义评审提示语 | 标准的代码评审提示语 |
| `-c` | 将评审结果作为 GitHub PR 评论发送 | 关闭 |

**示例：**
```bash
# Review with default Claude Code agent
bash {baseDir}/scripts/dev-relay.sh --review https://github.com/owner/repo/pull/123

# Review with Codex, post comment, in a thread
bash {baseDir}/scripts/dev-relay.sh --thread --review https://github.com/owner/repo/pull/123 -- -a codex -c

# Custom review prompt
bash {baseDir}/scripts/dev-relay.sh --review https://github.com/owner/repo/pull/123 -- -p "Focus on security vulnerabilities and SQL injection"
```

评审工具会将评审结果保存到 `/tmp/pr-review-<编号>.md` 文件中。使用 `-c` 选项后，评审结果会以 GitHub PR 评论的形式显示。

### 并行任务模式

您可以同时运行多个 Codecast 会话：

```bash
bash {baseDir}/scripts/dev-relay.sh --parallel tasks.txt
```

**任务配置文件格式**（每行一个任务）：
```
~/projects/api | Build user authentication endpoint
~/projects/web | Add dark mode toggle to settings page
~/projects/docs | Update API documentation for v3
```

每个任务都会在 Discord 中创建一个独立的线程和输出目录。所有任务完成后会显示一个总结信息。

**并行模式的额外选项：**

| 标志 | 描述 | 默认值 |
|------|------------|---------|
| `-a <代理>` | 使用的代理（claude 或 codex） | claude |
| `--worktree` | 使用每个目录的 Git 工作树 | 关闭 |
| `--skip-reads` | 隐藏读取操作相关的事件 | 关闭 |
| `-r <数量>` | 每个任务的发送频率上限 | 25 次 |
| `-t <秒>` | 每个任务的超时时间 | 1800 秒 |

**示例：**
```bash
bash {baseDir}/scripts/dev-relay.sh --parallel tasks.txt -- -a codex --worktree
```

以 `#` 开头的行会被忽略。每个任务会自动开启线程以区分不同的任务。

### Discord 桥接功能（交互式）

您可以运行一个辅助进程，将 Discord 的消息转发到正在运行的 Codecast 会话中：

```bash
python3 {baseDir}/scripts/discord-bridge.py --channel CHANNEL_ID --users USER_ID1,USER_ID2
```

**在 Discord 中使用的命令：**

| 命令 | 功能 |
|---------|------------|
| `!status` | 显示正在运行的 Codecast 会话 |
| `!kill <PID>` | 终止一个会话 |
| `!log [PID]` | 显示最近的输出（仅当有会话时需要提供 PID） |
| `!send [PID] <消息>` | 将消息发送到代理的标准输入 |
| *(纯文本)* | 如果只有一个会话正在运行，这些命令会自动执行 |

**环境变量：**

| 变量 | 描述 |
|----------|------------|
| `BRIDGE_CHANNEL_ID` | 需要监控的 Discord 频道 |
| `BRIDGE_ALLOWED_USERS` | 允许访问的 Discord 用户 ID（用逗号分隔） |

**所需软件：** `websocket-client` Python 包（通过 `pip install websocket-client` 安装）以及具有 `MESSAGE_CONTENT` 意图的 Discord 机器人令牌。

## Discord 上显示的内容

- **对于 Claude Code（stream-json 模式）：**
  - 模型相关信息
  - 文件写入操作（包含行数和内容预览）
  - 文件编辑操作
  - Bash 命令
  - Bash 命令的输出（截断为 800 个字符）
  - 文件读取操作（使用 `--skip-reads` 可以隐藏）
  - Web 搜索功能
  - 助手提供的帮助信息
  - 完成任务的总结信息（包括轮次、耗时、成本和会话统计）

- **对于 Codex（--json 模式）：**
  - 会话的线程 ID
  - 命令的执行记录
  - 命令的输出（截断为 800 个字符）
  - 文件的创建/修改操作
  - 推理过程的详细记录
  - Web 搜索结果
  - MCP 工具的调用记录
  - 代理的提示信息
  - 每轮次的令牌使用情况
  - 会话的总结信息（包括成本和统计）

- **对于其他代理（原始输出模式）：**
  - 以代码块的形式显示输出内容（包含 ANSI 格式的转换）
  - 挂起操作的警告信息
  - 任务完成的提示信息

## 总结

每个会话结束时都会显示一个总结信息，包括：
- 创建和修改的文件列表（包含文件数量）
- 执行的 Bash 命令
- 工具的使用情况
- 总成本

## 架构概述

```
scripts/
├── dev-relay.sh          # Shell entry point, flag parsing, process management
├── parse-stream.py       # Multi-agent JSON stream parser (Claude + Codex)
├── review-pr.sh          # PR review mode (--review)
├── parallel-tasks.sh     # Parallel worktree tasks (--parallel)
├── discord-bridge.py     # Discord → stdin bridge (companion process)
├── test-smoke.sh         # Pre-flight validation (webhook, deps, permissions)
├── strip-ansi.sh         # ANSI escape code stripper
├── .webhook-url          # Discord webhook URL (gitignored)
└── platforms/
    ├── __init__.py       # Platform adapter loader
    └── discord.py        # Discord webhook + thread support
```

## 提示语模板

请确保在代理的提示语中添加完成任务的提示信息。这样当代理完成任务时，OpenClaw 会立即响应，而无需等待下一次心跳信号。

```
<your task description here>

When completely finished, run: openclaw system event --text "Done: <brief summary>" --mode now
```

**完整示例：**
```bash
exec command:"nohup {baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Refactor the auth module to use JWT tokens. Add tests. When completely finished, run: openclaw system event --text \"Done: refactored auth to JWT with tests\" --mode now' > /tmp/codecast.log 2>&1 & echo PID:\$!"
```

## 支持的代理类型

| 代理类型 | 输出格式 | 支持情况 |
|-------|------------|--------|
| Claude Code | stream-json（已解析） | 完全支持 |
| Codex | --json JSONL（已解析） | 完全支持 |
| Codex（未使用 --json） | 原始 ANSI 格式 | 基本支持 |
| Gemini CLI | 原始 ANSI 格式 | 基本支持 |
| 任何命令行工具 | 原始 ANSI 格式 | 基本支持 |

## 交互式输入

在会话进行中，您可以将用户的输入转发给代理：
- 从 OpenClaw 发送输入的格式：`process:submitsessionId:<ID> data:"您的消息"``
- 会话相关信息会被保存在 `/tmp/dev-relay-sessions/<PID>.json` 文件中（每个并发会话对应一个文件）。

## 代理集成

当 AI 代理（如 OpenClaw）通过编程方式调用 Codecast 时，请注意：
**⚠️ 对于 Codecast 会话，切勿使用 `exec background:true`。** OpenClaw 的后台执行机制适用于短时间运行的任务（如构建、测试）。对于长时间运行的任务（如 Claude Code 会话），系统会在代理轮次结束后约 15-20 秒内强制终止该进程。这是 OpenClaw 的设计特性——它采用轮询方式运行，而不是连续执行。详情请参考 [社区讨论](https://www.answeroverflow.com/m/1469280591886286899)。

**建议使用 `nohup` 命令：**
```bash
nohup {baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Your task here' > /tmp/codecast.log 2>&1 &
```

**完成任务后的通知：**
- `dev-relay.sh` 在程序退出时会调用 `openclaw gateway wake` 来触发心跳信号。
- 在代理的提示语中添加以下内容：`任务完成后，请运行：openclaw system event --text 'Done: [总结内容]' --mode now`。
- 监控 `/tmp/dev-relay-sessions/<PID>.json` 文件——会话结束后该文件会被自动删除。
- 使用 `ps -p <PID>` 命令检查进程的状态。

> **警告：** 如果在 OpenClaw 重启期间使用 `exec background:true`，会话数据将会丢失。
> *在会话进行中，代理不得运行 `config.patch` 命令，因为这会导致重启并终止后台进程。*

**会话结束后的处理流程：**
会话结束后，调用方应：
1. 查看 `#dev-session` 或 `process:log` 文件以了解构建的结果。
2. 验证最终结果是否正常（通过运行相关工具并检查输出）。
3. 将结果告知用户。

**完成通知：**
请在代理的提示语中添加以下内容，以便用户能够立即收到完成通知：
```
When completely finished, run: openclaw system event --text 'Done: [summary]' --mode now
```

**示例（OpenClaw 代理调用 Codecast 的情况）：**
```bash
# Step 1: Launch via nohup (decoupled from agent turn lifecycle)
exec command:"nohup {baseDir}/scripts/dev-relay.sh -w ~/projects/myapp -- claude -p --dangerously-skip-permissions --output-format stream-json --verbose 'Build auth module. When finished, run: openclaw system event --text \"Done: auth module built\" --mode now' > /tmp/codecast.log 2>&1 & echo PID:$!"
# Step 2: Note the PID from output, monitor via ps or wait for wake event
```

## 会话跟踪**

- **活跃会话信息：** `/tmp/dev-relay-sessions/<PID>.json` 文件（每个并发会话对应一个文件），其中包含 PID、代理名称、开始时间以及用于转发输入的目录路径。该文件会在会话结束后自动删除。
- **原始事件日志：** 输出目录位于 `/tmp/dev-relay.XXXXXX`（会在会话开始时显示路径），其中保存了所有原始事件数据，可用于后续的会话恢复。系统会在启动时自动清理超过 7 天的旧日志文件。

## 环境变量

| 变量 | 描述 | 默认值 |
|----------|------------|---------|
| `CODECAST_BOT_TOKEN` | 用于 `--thread` 模式和桥接功能的 Discord 机器人令牌 | 如果未设置，则使用 `.bot-token` 文件 |
| `CODECAST_RATE_LIMIT` | 每 60 秒的最大发送次数 | 25 次 |
| `BRIDGE_CHANNEL_ID` | 需要监控的 Discord 频道 | 所有频道 |
| `BRIDGE_ALLOWED_USERS` | 允许访问的 Discord 用户 ID（用逗号分隔） | 所有用户 |

## 故障排除**

| 错误现象 | 原因 | 解决方法 |
|---------|-------|-----|
| 输出内容混乱或为空 | 未正确分配 PTY（伪终端） | 在执行命令时设置 `pty:true`。如果直接使用 Codecast，请确保已安装 `unbuffer` 工具。 |
| 代理似乎卡住 | 代理的空闲时间超过设定阈值 | 查看 `process:log` 文件以获取代理状态。可以使用 `-h <秒>` 参数调整挂起阈值。 |
| Webhook 被限制 | 在指定时间内发送了过多消息 | 无需手动操作——系统会自动分批发送消息。如果问题持续存在，可以使用 `-r 15` 参数降低发送频率。 |
| 无法收到 Discord 消息 | Webhook URL 错误或丢失 | 运行 `/{baseDir}/scripts/test-smoke.sh` 命令来验证设置是否正确。 |

## 完成通知

任务完成后，中间输出进程会调用 `openclaw gateway wake` 来立即通知 OpenClaw。