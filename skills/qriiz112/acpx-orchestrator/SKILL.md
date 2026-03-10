---
name: acpx
description: 增强型终端AI代理编排器，支持并行执行、健康检查以及工作流预设功能。
metadata: {"version": "4.0.0", "author": "qriiz112", "email": "christianovianto@gmail.com", "license": "MIT"}
requires: {"bins": ["acpx"], "optional": ["opencode", "pi", "kimi", "kilo", "codex", "claude"]}
---
# acpx v4.0 - 代理编排器

这是一个增强了的 CLI 工具，基于 acpx 构建，新增了编排功能，包括并行执行、健康检查以及工作流管理。

## 快速入门

```bash
# Discover agents
acpx discover

# Health check
acpx health

# Run single agent
acpx run opencode "Fix bug"

# Run workflow
acpx workflow review
```

## 命令

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `discover` | 列出已安装的代理 | `acpx discover` |
| `health` | 检查所有代理的状态 | `acpx health` |
| `run` | 运行单个代理 | `acpx run opencode "task"` |
| `parallel` | 从文件中并行运行代理任务 | `acpx parallel tasks.txt` |
| `batch` | 从文件中顺序运行代理任务 | `acpx batch tasks.txt` |
| `watch` | 监控代理的状态 | `acpx watch opencode` |
| `kill` | 终止代理会话 | `acpx kill opencode` |
| `workflow` | 运行预定义的工作流 | `acpx workflow review` |
| `json` | 以 JSON 格式输出结果 | `acpx json opencode "task" \| jq` |
| `exec` | 直接执行命令 | `acpx exec opencode "task"` |

## 工作流

| 工作流 | 描述 |
|----------|-------------|
| `review` | 代码审查，并以 JSON 格式输出结果 |
| `refactor` | 安全地进行代码重构（显示差异） |
| `test` | 生成 PyTest 测试用例 |
| `debug` | 深度调试（超时时间为 600 秒） |

## 批量文件格式

```bash
# tasks.txt
opencode exec 'Fix auth.py'
pi exec 'Create tests'
kimi --print --yolo --prompt 'Review changes'
```

## 通过 OpenClaw 启动

```javascript
// Health check
sessions_spawn(
  task="acpx health",
  label="health-check",
  runtime="subagent",
  mode="run"
)

// Run workflow
sessions_spawn(
  task="acpx workflow review",
  label="review",
  runtime="subagent",
  mode="run"
)

// Parallel tasks
sessions_spawn(
  task="acpx parallel tasks.txt",
  label="parallel-jobs",
  runtime="subagent",
  mode="run"
)

// JSON output
sessions_spawn(
  task="acpx json opencode 'List functions'",
  label="json-task",
  runtime="subagent",
  mode="run"
)
```

## 辅助脚本

- `acpx` - 主要的代理编排器 CLI 工具 |
- `acpx-batch` - 传统的顺序执行工具 |
- `acpx-workflow` - 传统的预定义工作流工具 |
- `acpx-discover` - 传统的代理发现工具 |

## 更新日志

- **v4.0.0**：增强了代理编排功能（支持并行执行、健康检查、工作流以及 JSON 输出） |
- **v3.1.0**：提供了简单的 CLI 接口 |
- **v3.0.0**：实现了通用的自动代理发现功能 |
- **v2.0.0**：支持异步多代理执行模式 |
- **v1.0.0**：最初的代理编排工具版本 |