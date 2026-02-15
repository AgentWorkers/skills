---
name: bullybuddy
description: **BullyBuddy** – 用于管理 Claude 代码会话的工具。支持以下命令：  
`status`：查看会话状态  
`list`：列出所有会话  
`spawn`：创建新的会话  
`send`：向会话发送数据  
`output`：查看会话输出  
`kill`：终止会话  
`audit`：审计会话记录  
`transcript`：获取会话的文字记录
metadata: { "openclaw": { "emoji": "🦞", "always": true } }
---

# BullyBuddy

您可以通过 `/bullybuddy` 或 `/skill bullybuddy` 命令来控制 BullyBuddy Claude 代码会话管理器。

## 使用方法

使用以下子命令运行脚本：

```bash
{baseDir}/scripts/bb.sh <command> [args...]
```

必须设置环境变量 `BB_URL` 和 `BB_TOKEN`。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `help` | 显示帮助信息 |
| `status` | 查看服务器状态 |
| `list` | 列出所有会话 |
| `spawn [cwd] [task]` | 创建一个新的会话 |
| `send <id> <text>` | 向指定会话发送文本信息 |
| `output <id>` | 查看指定会话的输出内容 |
| `kill <id>` | 结束指定会话 |
| `audit [n]` | 审计日志 |
| `transcript <id>` | 查看会话的文字记录 |

## 示例

```
/bullybuddy status
/bullybuddy list
/bullybuddy spawn ~/project "Fix bug"
/bullybuddy send abc123 yes
/bullybuddy kill abc123
```