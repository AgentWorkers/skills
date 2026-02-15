---
name: bb
description: **BullyBuddy** – 通过斜杠（/）命令来控制 Claude Code 会话。使用 `/bb` 命令可以管理多个 Claude Code 实例。支持的命令包括：`status`（状态查询）、`list`（列表显示）、`spawn`（创建新实例）、`send`（发送数据）、`output`（输出结果）、`kill`（终止实例）、`audit`（审计日志）、`transcript`（会话记录）。
user-invocable: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["bullybuddy", "claude"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "openclaw-bullybuddy",
              "bins": ["bullybuddy"],
            },
          ],
      },
  }
---

# BullyBuddy 的 `/bb` 命令

您可以通过 `/bb` 命令直接控制 BullyBuddy Claude 代码会话管理器。

## 设置

1. 安装 BullyBuddy：

```bash
npm install -g openclaw-bullybuddy
```

2. 启动服务器：

```bash
bullybuddy server
```

服务器启动时，连接信息会自动保存到 `~/.bullybuddy/connection.json` 文件中。`/bb` 命令会自动读取该文件，无需设置环境变量。

如需远程访问，请使用 `bullybuddy server --tunnel` 命令。隧道地址可以通过 `/bb url` 查看。

## 使用方法

```
/bb status          - Server status & session summary
/bb list            - List all sessions
/bb spawn [cwd] [task] [group] - Create new session
/bb send <id> <text> - Send input to session
/bb output <id> [lines] - Show session output/transcript
/bb kill <id>       - Terminate session
/bb url             - Show dashboard URL (local + tunnel)
/bb audit [limit]   - View audit log
/bb transcript <id> [limit] - View conversation transcript
/bb help            - Show help
```

## 示例

```
/bb status
/bb list
/bb spawn /home/user/project "Fix the login bug"
/bb send abc123 "yes"
/bb output abc123
/bb kill abc123
```

## 脚本

当执行 `/bb` 命令时，系统会运行相应的脚本：
```bash
{baseDir}/scripts/bb.sh $ARGUMENTS
```