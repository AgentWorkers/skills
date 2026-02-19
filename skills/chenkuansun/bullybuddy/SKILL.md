---
name: bullybuddy
description: **BullyBuddy** — 一个用于管理 Claude Code 会话的 CLI 工具。通过 `/bullybuddy` 命令可以创建、列出、发送输入、终止以及监控多个 Claude Code 会话。该工具会自动从 `~/.bullybuddy/connection.json` 文件中读取认证令牌。
user-invocable: true
command-dispatch: tool
command-tool: exec
command-arg-mode: raw
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "homepage": "https://github.com/ChenKuanSun/openclaw-bullybuddy",
        "requires": { "bins": ["bullybuddy", "claude", "jq", "curl"] },
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
# BullyBuddy

BullyBuddy负责创建和管理多个Claude Code的CLI会话。它支持两种后端技术：**tmux**（默认选项，会话在服务器重启后仍可保留）或**node-pty**（备用方案）。同时提供REST API、WebSocket流式传输以及Web仪表板功能。

## 设置

1. 全局安装该软件包：

```bash
npm install -g openclaw-bullybuddy
```

2. 启动服务器：

```bash
bullybuddy server
```

服务器启动时，连接信息会自动保存到`~/.bullybuddy/connection.json`文件中。`/bullybuddy`命令会自动读取该文件，无需设置环境变量。

若需远程访问，请使用`bullybuddy server --tunnel`命令。隧道URL可以通过`/bullybuddy url`获取。

## /bullybuddy命令行接口

```
/bullybuddy status          - Server status & session summary
/bullybuddy list            - List all sessions
/bullybuddy spawn [cwd] [task] [group] - Create new session
/bullybuddy send <id> <text> - Send input to session
/bullybuddy output <id> [lines] - Show session output/transcript
/bullybuddy kill <id>       - Terminate session
/bullybuddy url             - Show dashboard URL (local + tunnel)
/bullybuddy audit [limit]   - View audit log
/bullybuddy transcript <id> [limit] - View conversation transcript
/bullybuddy help            - Show help
```

## 安全注意事项

- 认证令牌赋予了对所有Claude Code会话的**完全控制权**，包括发送任意输入内容。请将其视为敏感信息并严格保密。
- `/bullybuddy url`命令会输出包含令牌的仪表板URL，切勿公开分享或记录该URL。
- 使用`--tunnel`选项时，仪表板和API会通过Cloudflare临时URL暴露在互联网上。任何持有令牌的人都可以远程访问所有会话。
- 创建的会话将以用户的本地权限运行Claude Code。如果启用了`--dangerously-skip-permissions`选项，Claude可以无需确认即可执行任何命令。

## 认证机制

每次服务器启动时都会生成一个随机令牌，并将其保存到`~/.bullybuddy/connection.json`文件中（权限设置为0600）。CLI和`/bullybuddy`会自动检测到该令牌。对于仪表板，令牌会包含在启动时显示的URL中。服务器正常关闭后，连接信息文件会被删除。

## API概述

所有API接口都需要通过`Authorization: Bearer <token>`头部或`?token=`查询参数传递令牌。所有响应格式为`{ ok: boolean, data?: T, error?: string }`。

| 方法      | API接口        | 功能描述                |
|---------|---------------|----------------------|
| `GET`     | `/health`        | 获取服务器状态              |
| `GET`     | `/api/sessions`     | 列出会话（可按组筛选）           |
| `POST`     | `/api/sessions`     | 创建新会话                |
| `GET`     | `/api/sessions/:id`     | 查看会话详情及指标            |
| `DELETE`     | `/api/sessions/:id`     | 删除指定会话                |
| `POST`     | `/api/sessions/:id/input` | 向PTY发送输入              |
| `POST`     | `/api/sessions/:id/resize` | 调整PTY窗口大小            |
| `POST`     | `/api/sessions/:id/task` | 设置会话任务元数据            |
| `POST`     | `/api/sessions/:id/mute` | 静音会话通知              |
| `POST`     | `/api/sessions/:id/unmute` | 取消会话通知静音            |
| `GET`     | `/api/groups`     | 获取会话分组信息            |
| `GET`     | `/api/summary`     | 获取整体状态统计            |
| `GET`     | `/api/browse`     | 浏览目录（默认禁用）            |
| `GET`     | `/api/audit`     | 查看审计日志              |
| `GET`     | `/api/sessions/:id/transcript` | 获取会话对话记录           |

### 创建会话的请求数据

```json
{
  "name": "worker-1",
  "group": "myproject",
  "cwd": "/path/to/repo",
  "task": "Implement feature X",
  "args": ["--verbose"],
  "cols": 120,
  "rows": 40,
  "skipPermissions": false
}
```

所有字段均为可选。如果提供了`task`参数，该参数会自动作为输入发送给Claude。

**注意：**发送输入内容时，请使用`\r`（回车符）作为结束标志，而非`\n`。

## WebSocket协议

连接地址为`ws://<host>:<port>/ws?token=<token>`。

### 客户端消息类型及参数

| 类型    | 参数            | 描述                        |
|---------|-----------------|---------------------------|
| `subscribe` | `sessionId`, `cols?`, `rows?` | 订阅会话输出                    |
| `unsubscribe` | `sessionId`         | 停止接收会话输出                    |
| `input`    | `sessionId`, `data`      | 向PTY发送按键输入                |
| `resize`   | `sessionId`, `cols`, `rows`    | 调整PTY窗口大小                  |

### 服务器消息类型及参数

| 类型    | 参数            | 描述                        |
|---------|-----------------|---------------------------|
| `sessions` | `sessions[]`       | 所有会话列表                    |
| `output`   | `sessionId`, `data`      | 终端输出数据块                    |
| `scrollback` | `sessionId`, `data`      | 订阅时使用的缓冲回滚功能                |
| `session:created` | `session`       | 新会话创建                    |
| `session:exited` | `sessionId`, `exitCode`     | 会话终止                    |
| `session:stateChanged` | `sessionId`, `detailedState` | 会话状态变化                    |
| `error`    | `message`       | 发生错误（例如：无效输入）                |

## 状态检测

BullyBuddy通过分析PTY的原始输出来实时检测Claude Code的运行状态。

| `detailedState` | 含义                        |
|-----------------|-------------------------|
| `starting` | 会话刚创建，Claude正在加载            |
| `working` | Claude正在处理或编辑内容              |
| `permission_needed` | Claude等待用户授权                |
| `idle`    | Claude处于空闲状态，可接收输入             |
| `compacting` | 正在压缩对话历史记录                |
| `error`    | 输出中检测到错误                    |

状态变化会通过WebSocket发送，并在`GET /api/summary`接口中显示。

## 与OpenClaw的集成

定期调用`GET /api/summary`接口可查看所有会话的状态。`sessionsNeedingAttention`字段会列出处于`permission_needed`或`error`状态的会话ID。

## 远程访问

使用`--tunnel`选项启动服务器，系统会自动生成Cloudflare临时URL：

```bash
bullybuddy server --tunnel
```

隧道URL会在启动时显示，并保存到`~/.bullybuddy/connection.json`文件中。可以使用`bullybuddy url`或`/bullybuddy url`随时获取该URL。

## CLI命令

```bash
bullybuddy server                          # Start server
bullybuddy server --tunnel                 # Start with Cloudflare tunnel
bullybuddy url                             # Show dashboard URL (local + tunnel)
bullybuddy spawn --name worker --group proj  # Spawn session
bullybuddy list --json                     # List sessions
bullybuddy send <id> "Fix the bug"         # Send input
bullybuddy attach <id>                     # Interactive terminal
bullybuddy kill <id>                       # Kill session
bullybuddy groups                          # List groups
bullybuddy open                            # Open dashboard
```

## 脚本执行方式

当脚本被调用时，会执行以下操作：  
```bash
{baseDir}/scripts/bullybuddy.sh $ARGUMENTS
```