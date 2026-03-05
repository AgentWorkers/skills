---
name: codex-bridge
description: 将编码任务通过后台执行的方式发送到本地的 OpenAI Codex CLI，并进行状态监控。同时，可以针对相关问题提供明确的解答。适用于需要在命令行上将脚本编写、代码编辑、代码重构或多步骤编码工作委托给 Codex 的场景。
metadata:
  openclaw:
    emoji: "🧰"
    requires:
      bins: ["python3", "codex"]
---
# Codex Bridge

该功能允许将 OpenClaw 的编码任务委托给本地的 `codex` CLI 并异步管理这些任务。通过这个功能，OpenClaw 可以：

- 分发任务
- 查看任务状态及最新输出结果
- 转发需要澄清的问题
- 发送回答
- 收集最终结果

## 使用场景

- 编写脚本（Python、Bash 等）
- 在现有项目中实现或重构代码
- 在后台运行涉及多个文件的编码任务
- 在保持 OpenClaw 可响应性的同时委托编码工作
- 处理在运行过程中可能需要澄清问题的任务

## 不适用场景

- 用于快速查询事实性信息或获取简单解释
- 需要 OpenClaw 直接编写的小段代码
- 非编码类任务
- 不需要调用本地编码代理/CLI 的任务

## 分发任务

```bash
~/.openclaw/skills/codex-bridge/codex-bridge-dispatch.sh \
  --task-id <descriptive-name> \
  --workdir <project-directory> \
  --prompt "<detailed coding task>"
```

### 提示编写

提示中应包含以下内容：
- 需要构建或修复的内容
- 已知的文件路径（如果有的话）
- 预期的行为或输出结果
- 优先使用的语言/框架
- 任何限制条件（如测试要求、代码风格规范、不允许添加新的依赖项等）

示例：

```bash
~/.openclaw/skills/codex-bridge/codex-bridge-dispatch.sh \
  --task-id scripts-csv-parser \
  --workdir ~/projects/data-tools \
  --prompt "Create parse_orders.py. Read orders CSV, keep shipped rows, group by customer_id, and write summary CSV with columns customer_id, order_count, total_amount. Use pandas. Add basic CLI args and error handling."
```

## 查看任务状态

```bash
~/.openclaw/skills/codex-bridge/codex-bridge-status.sh --task-id <id>
```

常见的状态查询命令：

```bash
~/.openclaw/skills/codex-bridge/codex-bridge-status.sh --list
~/.openclaw/skills/codex-bridge/codex-bridge-status.sh --task-id <id> --output
~/.openclaw/skills/codex-bridge/codex-bridge-status.sh --task-id <id> --question
~/.openclaw/skills/codex-bridge/codex-bridge-status.sh --task-id <id> --result
~/.openclaw/skills/codex-bridge/codex-bridge-status.sh --task-id <id> --log
```

## 回答需要澄清的问题

当任务状态为 `waiting_for_answer` 时，读取待回答的问题并发送回复：

```bash
~/.openclaw/skills/codex-bridge/codex-bridge-status.sh --task-id <id> --question
~/.openclaw/skills/codex-bridge/codex-bridge-answer.sh --task-id <id> --answer "<answer text>"
```

在收到回复后，系统会恢复之前的 Codex 会话。

## 工作流程

1. 使用明确的提示分发任务。
2. 报告任务 ID。
3. 定期检查任务状态及输出结果。
4. 如果任务状态变为 `waiting_for_answer`，读取相关问题并转告用户，然后使用 `--answer` 命令发送回复。
5. 当任务状态变为 `complete` 时，读取 `--result` 并总结任务结果。
6. 如果任务状态为 `error`，查看 `--log` 和 `--output` 文件以获取详细错误信息。

## 注意事项与限制

- 该功能依赖于本地的 `codex` CLI（`codex exec` 和 `codex exec resume` 命令）。
- 需要澄清的问题通过提示中的文本标记协议进行传递。
- 任务状态信息存储在 `~/.codex-bridge/tasks/<task-id>/` 目录下。
- 命令在指定的 `--workdir` 目录下通过 Codex 运行。
- 对于无人值守的运行任务，系统会在等待 10 分钟无响应后自动超时，并采用默认的补救措施继续执行。