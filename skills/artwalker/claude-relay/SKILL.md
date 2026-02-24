---
name: claude-relay
description: 通过 tmux 在多个项目中使用 Claude Code 的中继操作器。可以启动/继续持久的 Claude Code 终端会话、发送提示信息、读取输出结果，并根据项目名称或路径来管理后台会话。
metadata: {"openclaw":{"emoji":"🔄","requires":{"bins":["tmux","claude"]}}}
---
# Claude Relay

通过 tmux 将 Claude Code 作为持久的终端协作工具来使用。

## 该技能的用途：
- 在项目目录中启动 Claude Code 会话
- 向正在运行的 Claude 会话发送指令
- 查看 Claude 的输出结果
- 管理多个并发的项目会话

## 脚本使用：
所有操作均使用 `scripts/relay.sh` 脚本执行。建议使用脚本化的方式，以确保行为的一致性和可预测性。

## 项目路径查找规则：
脚本按以下顺序查找项目路径：
1. 绝对路径（如果存在）
2. 来自 `skills` 目录中 `projects.map` 文件的别名（格式：`name=/abs/path`）
3. `CLAUDE_RELAY_ROOT/<name>` 的精确匹配
4. 在 `$CLAUDE_RELAY_ROOT` 目录下按文件夹名称查找（最大搜索深度为 2 层）
5. 如果未指定路径，则重用上一个项目会话

如果找到多个匹配项，系统会请求用户进行选择。

## 标准工作流程：
1. 启动或重用目标项目的会话：
   - `scripts/relay.sh start <project-or-path>`
2. 向项目会话发送指令：
   - `scripts/relay.sh send <project-or-path> "<instruction>"`
3. 查看输出结果：
   - `scripts/relay.sh tail <project-or-path> [lines]`
4. 重复发送指令或查看输出的操作
5. 根据用户指令停止会话：
   - `scripts/relay.sh stop <project-or-path>`

## 会话命名规则：
会话名称具有唯一性，格式为 `cc_<project_basename_sanitized>`，其中 `project_basename` 是项目名称，`sanitized` 是对项目名称的简化处理。

## 快速命令：
```bash
scripts/relay.sh start myproject
scripts/relay.sh send myproject "fix the failing tests"
scripts/relay.sh tail myproject 80
scripts/relay.sh status
scripts/relay.sh stop myproject
```

## 环境变量：
| 变量          | 默认值         | 说明                          |
|----------------|----------------|-------------------------------------------|
| `CLAUDE_RELAY_ROOT` | `$HOME/projects` | 用于查找项目路径的根目录                 |
| `CLAUDE_RELAY_MAP` | `<skill-dir>/projects.map` | 包含项目别名映射的文件路径                |
| `CLAUDE_BIN` | `claude`       | Claude Code 命令行工具的路径                   |
| `RELAY_WAIT` | `6`          | 发送指令后等待输出结果的秒数                   |

## 设置步骤：
1. 安装此技能
2. 在 `skills` 目录下创建 `projects.map` 文件（参考示例文件 `projects.map.example`）
3. 确保 `tmux` 和 `claude` 已安装，并且它们的路径已添加到系统的 `PATH` 环境变量中

## 注意事项：
- 该技能主要用于项目间的数据传输和会话管理，不涉及复杂的代码推理功能。
- 对于需要深入设计或代码审查的任务，请在使用此技能前选择更合适的工具或模型。