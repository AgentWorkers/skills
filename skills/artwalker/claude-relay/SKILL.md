---
name: claude-relay
description: 通过 tmux 在多个项目中使用 Claude Code 的中继操作符。当用户需要启动/继续 Claude Code 终端会话、发送提示信息、读取输出内容，或按项目名称/路径管理后台运行的 Claude 会话时，可以使用该功能。
metadata: {"openclaw":{"emoji":"🔄","requires":{"bins":["tmux","claude"]}}}
---
# Claude Relay

通过 tmux 将 Claude Code 作为持久的终端协作工具来使用。

## 脚本

所有操作都通过 `scripts/relay.sh` 脚本执行。不带参数运行该脚本可查看使用说明。

```bash
scripts/relay.sh <action> [project] [args...]
```

**可用命令**：`start`、`send`、`tail`、`stop`、`status`、`session`

## 工作流程

1. 启动会话：`scripts/relay.sh start <project>`
2. 发送指令：`scripts/relay.sh send <project> "<text>"`
3. 读取输出：`scripts/relay.sh tail <project> [lines]`
4. 根据需要重复发送指令或查看输出。
5. 完成后停止会话：`scripts/relay.sh stop <project>`

## 项目路径解析

脚本会按以下顺序解析 `<project>`：

1. 绝对路径（如果目录存在）
2. 从 `projects.map` 文件中查找别名（格式：`name=/abs/path`）
3. 直接匹配 `$CLAUDE_RELAY_ROOT/<name>`
4. 在 `$CLAUDE_RELAY_ROOT` 目录下按文件夹名称查找（最大搜索深度为 2 层）
5. 如果未指定路径，则使用上一个项目。

如果找到多个匹配项，脚本会显示所有候选项目，并提示用户确认具体要使用的项目。

## 会话命名规则

会话名称为 `cc_<basename_sanitized>`，每个项目对应一个 tmux 会话。

## 错误处理

- **未安装 tmux**：脚本以代码 2 退出，并显示“缺少依赖项”的错误信息。
- **找不到 Claude 可执行文件**：同样以代码 2 退出。请检查 `CLAUDE_BIN` 环境变量或默认路径。
- **会话未运行**（在已停止的会话中尝试发送指令或查看输出）：脚本以代码 6 退出。请先重新启动会话。
- **项目未找到**：脚本以代码 4 退出。请检查 `projects.map` 文件或项目路径。
- **Claude 进程挂起**：虽然 `tail` 命令仍能执行，但输出可能异常。此时请使用 `stop` 命令停止会话并重新启动。

## 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `CLAUDE_RELAY_ROOT` | `$HOME/projects` | 用于查找项目的根目录 |
| `CLAUDERELAY_MAP` | `<skill-dir>/projects.map` | 项目别名映射文件的路径 |
| `CLAUDE_BIN` | `claude`（从 `PATH` 变量中获取） | Claude Code 的命令行工具二进制文件路径 |
| `RELAY_WAIT` | `6` | 发送指令后等待输出显示的秒数 |

## 设置步骤

1. 安装此技能。
2. 在技能目录下创建一个 `projects.map` 文件（参考 `projects.map.example` 示例）。
3. 确保 `tmux` 和 `claude` 已安装，并且它们的路径已添加到系统的 `PATH` 环境变量中。

## 注意事项

- 该技能主要用于数据传输和任务协调，不涉及复杂的代码推理功能。