---
name: ask-claude
description: 将任务委托给 Claude Code CLI，并立即在聊天中反馈结果。该工具支持持久会话功能——Claude Code 会记住同一工作目录下的先前上下文。当用户请求运行 Claude、委托编码任务、继续之前的 Claude 会话，或执行任何能够利用 Claude Code 工具（如文件编辑、代码分析、Bash 命令等）的任务时，均可使用该工具。请务必以同步方式运行该工具，并在回复中始终包含执行结果。
metadata:
  {
    "openclaw": {
      "emoji": "🤖",
      "requires": { "anyBins": ["claude"] }
    }
  }
---
# 使用 Claude — 执行任务并报告结果（支持持久化会话）

## 两种模式

### 新会话（默认模式）
适用于开始新任务或讨论新主题时。

```bash
OUTPUT=$(/home/xmanel/.openclaw/workspace/run-claude.sh "prompt" "/workdir")
echo "$OUTPUT"
```

### 继续会话（--continue）
当用户希望在相同的工作目录中继续之前的 Claude 任务时使用。
Claude 会记住之前的所有操作：读取的文件、所做的编辑以及收集到的上下文信息。

```bash
OUTPUT=$(/home/xmanel/.openclaw/workspace/run-claude.sh --continue "prompt" "/workdir")
echo "$OUTPUT"
```

## 何时使用 `--continue`
当用户说出以下内容时，可以使用 `--continue`：
- “现在修复你发现的问题”
- “继续”
- “X 文件怎么样了？”
- “对……也做同样的操作”
- “那么现在呢？”
- “好的，关于……的错误呢？”
- 任何明确提到 Claude 最近所做操作的内容

在以下情况下，应使用 **新会话**：
- 开始一个不相关的任务
- 用户要求“从头开始”或“新任务”
- 使用不同的工作目录/项目

## 会话存储
Claude 会将会话信息按目录存储在 `~/.claude/projects/` 目录下。
只要使用相同的工作目录，`--continue` 就会从上次停止的地方继续执行——
相同的文件上下文、相同的对话记录以及相同的编辑内容。

## 直接命令（替代使用包装器）
```bash
# New session
OUTPUT=$(cd /workdir && env -u CLAUDECODE claude --permission-mode bypassPermissions --print "task" 2>&1)

# Continue session
OUTPUT=$(cd /workdir && env -u CLAUDECODE claude --permission-mode bypassPermissions --print --continue "task" 2>&1)
```

## 常见的工作目录
| 用途             | 工作目录                                                    |
| ---------------------- | ------------------------------------------------------ |
| 通用脚本           | `/home/xmanel/.openclaw/workspace`                     |
| 交易相关           | `/home/xmanel/.openclaw/workspace/hyperliquid`         |

## 收到结果后
- 用 1-3 行总结 Claude 的操作或发现的内容
- 提及创建或修改的文件
- 如果出现错误：分析问题并提供建议的解决方法
- 如果输出内容较长：可按需提供完整输出