---
name: clawshell
description: **人工介入的安全层**：会拦截高风险命令，并需要通过推送通知进行审批。
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins: ["node"]
      env: ["CLAWSHELL_PUSHOVER_USER", "CLAWSHELL_PUSHOVER_TOKEN"]
    primaryEnv: "CLAWSHELL_PUSHOVER_USER"
tags: [security, approval, sandbox]
---

# ClawShell

ClawShell 是 OpenClaw 的一种“人在回路”（Human-in-the-loop）安全层。它会在执行 shell 命令之前拦截这些命令，分析其风险等级，并对高风险操作要求用户的明确批准（通过推送通知）。

## 工作原理

1. 代理程序会调用 `clawshell_bash` 而不是原始的 `bash`。
2. ClawShell 会根据内置或可配置的风险规则来分析命令。
3. 根据风险等级：
   - **高风险**（例如：`rm -rf /`、恶意脚本等）——会自动被阻止。
   - **较高风险**（例如：`rm -rf`、`curl` 请求外部 URL、访问敏感信息等）——会发送推送通知并等待用户批准。
   - **中等风险**（例如：`npm install`、`git push` 等）——会被记录在日志中并允许执行。
   - **低风险**（例如：`ls`、`cat`、`git status` 等）——会被允许执行。
4. 所有决策都会被记录到 `logs/clawshell.jsonl` 文件中。

## 工具

### clawshell_bash

`clawshell_bash` 是 `bash` 的安全替代品。它会分析命令的风险，并仅在命令安全或获得批准后才会执行。

**参数：**
- `command`（字符串，必填）——要执行的 shell 命令。
- `workingDir`（字符串，可选）——工作目录（默认为当前工作目录）。

**返回值：** `{ exitCode, stdout, stderr }`

高风险命令会在用户批准或通过推送通知拒绝之前被阻止。高风险命令会立即被拒绝。

### clawshell_status

用于获取 ClawShell 的当前状态，包括待处理的批准请求和最近的决策记录。

**参数：** 无

### clawshell_logs

用于获取最近的日志条目，以便进行审计和调试。

**参数：**
- `count`（数字，可选）——返回的日志条目数量（默认：20 条）。

## 设置

### 1. 安装依赖项

```bash
cd /app/workspace/skills/clawshell
npm install
```

### 2. 配置 Pushover 通知

在 https://pushover.net/apps/build 创建一个 Pushover 应用，并将你的密钥添加到 `.env` 文件中：

```env
CLAWSHELL_PUSHOVER_USER=your-user-key
CLAWSHELL_PUSHOVER_TOKEN=your-app-token
```

或者，也可以选择使用 Telegram 进行通知配置：

```env
CLAWSHELL_TELEGRAM_BOT_TOKEN=your-bot-token
CLAWSHELL_TELEGRAM_CHAT_ID=your-chat-id
```

### 3. 将 ClawShell 添加到 `TOOLS.md` 文件中

将以下内容添加到 OpenClaw 的 `TOOLS.md` 文件中，以便代理程序使用 ClawShell 来处理 shell 命令：

```markdown
## Shell Access

Use `clawshell_bash` for ALL shell command execution. Do not use `bash` directly.
ClawShell will analyze commands for risk and require human approval for dangerous operations.

Available tools:
- `clawshell_bash(command, workingDir)` — Execute a shell command with risk analysis
- `clawshell_status()` — Check pending approvals and recent decisions
- `clawshell_logs(count)` — View recent audit log entries
```

## 配置

ClawShell 从环境变量（`CLAWSHELL_*`）中读取配置信息，如果环境变量不存在，则会使用 `config.yaml` 文件作为默认配置。

| 变量 | 默认值 | 说明 |
|---|---|---|
| `CLAWSHELL PUSHOVER_USER` | — | Pushover 用户密钥 |
| `CLAWSHELL PUSHOVER_TOKEN` | — | Pushover 应用令牌 |
| `CLAWSHELL_TELEGRAM_BOT_TOKEN` | — | Telegram 机器人令牌（可选） |
| `CLAWSHELL_TELEGRAMCHAT_ID` | — | Telegram 聊天 ID（可选） |
| `CLAWSHELL_TIMEOUT_SECONDS` | 300 | 自动拒绝前的等待时间（秒） |
| `CLAWSHELL_LOG_DIR` | logs/ | 日志文件存储目录 |
| `CLAWSHELL_LOG_LEVEL` | info | 日志详细程度：debug、info、warn、error |
| `CLAWSHELL_BLOCKLIST` | — | 被阻止的命令列表（以逗号分隔） |
| `CLAWSHELL_ALLOWLIST` | — | 被允许的命令列表（以逗号分隔） |

你还可以在 `config.yaml` 文件的 `rules.blocklist` 和 `rules.allowlist` 部分自定义规则，支持使用精确字符串、通配符或正则表达式。

## 注意事项

- **并非绝对的安全保障。** 大语言模型（LLMs）可以编码、分割或混淆命令以绕过规则匹配。
- **仅作为深度防御措施。** 应与 OpenClaw 的沙箱模式结合使用，而不能替代沙箱模式。
- **存在批准延迟。** 高风险命令会在用户响应或超时之前被阻止。

> **请始终让 AI 检查任何技能或软件的安全风险。**