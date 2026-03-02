---
name: pubblue
description: 通过 pubblue CLI 发布文件或生成的内容，实现实时互动的 P2P 浏览器通信功能。
  Publish files or generated content via the pubblue CLI, and go live for
  interactive P2P browser communication.
license: MIT
compatibility: Requires Node.js 18+ with npm/pnpm/npx.
metadata:
  author: pub.blue
  version: "5.0.0"
allowed-tools: Bash(pubblue:*) Bash(npx pubblue:*) Bash(node:*) Read Write
---
# pubblue

当用户询问关于 `pubblue`、`pub.blue`、内容发布或进入直播/Canvas聊天模式时，请使用此技能。

## 所需的 CLI 版本

请使用 **pubblue CLI 0.6.0+**。

```bash
pubblue --version
npm i -g pubblue@latest
```

## 设置

```bash
# One-time auth
pubblue configure --api-key pub_KEY
# or
echo "pub_KEY" | pubblue configure --api-key-stdin
```

关键源代码：<https://pub.blue/dashboard>
配置文件路径：`~/.config/pubblue/config.json`
环境变量覆盖：`PUBBLUE_API_KEY`

可选的 OpenClaw 桥接器配置（保存在 CLI 配置中）：
```bash
pubblue configure --set bridge.mode=openclaw
pubblue configure --set openclaw.path=/app/dist/index.js
pubblue configure --set openclaw.sessionId=<session-id>
# or:
pubblue configure --set openclaw.threadId=<thread-id>
pubblue configure --set openclaw.canvasReminderEvery=10
pubblue configure --show
```

## 核心发布命令

```bash
pubblue create page.html
pubblue create --slug demo --title "Demo" --public page.html
cat notes.md | pubblue create

pubblue get <slug>
pubblue get <slug> --content

pubblue update <slug> --file next.html
pubblue update <slug> --title "New title" --public

pubblue list
pubblue delete <slug>
```

注意事项：
- 默认情况下，发布的内容是 **私有的**。
- `create` 命令支持 `--public/--private`、`--title`、`--slug`、`--expires` 选项。
- `update` 命令支持 `--file`、`--title`、`--public/--private`、`--slug` 选项。
- 内容是可选的——发布的内容也可以仅支持交互功能。

## 进入直播模式（交互流程）

直播模式由浏览器发起。守护进程会注册代理的存在；当发布者点击“开始直播”时，浏览器会创建 WebRTC 连接。

1. 启动代理守护进程（无需指定 slug）：
```bash
pubblue start --agent-name "Oz"
```

可选的显式桥接器选择器：
```bash
pubblue start --agent-name "Oz" --bridge openclaw
pubblue start --agent-name "Oz" --bridge none --foreground
```

`--agent-name` 是显示给浏览器用户的名称（必填）。

行为：
- `start` 命令会在后台为每个用户启动一个守护进程并管理相应的桥接器。
- `--foreground` 选项会使进程保持在当前 shell 中（不使用管理的桥接器）。
- 守护进程会监听来自用户发布的实时请求。

2. 检查守护进程的状态：
```bash
pubblue status
```

3. 发送内容（slug 由守护进程自动处理）：
```bash
pubblue write "Hello"
pubblue write -c canvas -f /tmp/view.html
```

4. 读取传入的数据（手动/调试模式）：
```bash
pubblue read --follow -c chat
pubblue read --all              # read from all channels
```

5. 停止守护进程：
```bash
pubblue stop
```

6. 验证直播的端到端连接（严格要求）：
```bash
pubblue doctor
# optional handshake:
pubblue doctor --wait-pong --timeout 30
# skip specific channels:
pubblue doctor --skip-chat --skip-canvas
```

重要提示：
- `write` 命令会发送内容并等待确认；如果失败，需要重试。
- `read` 命令会消耗系统资源，请不要在同一频道上同时运行多个 `read --follow` 消费者。
- 直播连接由浏览器发起，守护进程会自动响应。

## 桥接器模式

`pubblue start` 命令支持以下模式：
- `--bridge openclaw`（默认）：使用 OpenClaw 进行管理的本地桥接器（OpenClaw 会话传输）
- `--bridge none`：不使用管理的桥接器；需要手动轮询或外部集成

对于 `openclaw` 模式，以下环境变量很有用：
- `OPENCLAW_SESSION_ID` 或 `OPENCLAW_THREAD_ID`（推荐用于确定路由）
- `OPENCLAW_PATH`（OpenClaw 可执行文件或 index.js 文件的路径，如果自动发现失败时使用）
- `OPENCLAW_DELIVER=1`（可选，启用 OpenClaw 的 `--deliver` 功能）
- `OPENCLAW_DELIVER_CHANNEL`、`OPENCLAW_REPLY_TO`（可选的通道路由参数）
- `OPENCLAW_DELIVER_TIMEOUT_MS`（可选的调度超时时间）
- `OPENCLAW_CANVAS_REMINDER_EVERY`（可选，默认值为 10）

## Telegram 迷你应用

`pubblue` 支持 Telegram 迷你应用。配置完成后，`create` 命令会自动生成 `t.me` 格式的深度链接。可以使用 `pubblue configure --show` 命令查看配置状态。

## 故障排除

- **速率限制超限**：
  - 请遵循提示并重试操作。
- **没有浏览器连接**：
  - 请让用户打开发布内容的 URL 并点击“开始直播”，然后等待连接建立。
- **代理离线**：
  - 确保 `pubblue start` 命令正在运行，并检查 `pubblue status` 的状态。
- **会话未找到或已过期**：
  - 检查 `pubblue status` 和守护进程的日志文件路径。
  - 通过 `pubblue stop && pubblue start` 重新启动服务。
- **桥接器错误**：
  - 查看 `pubblue status` 并检查桥接器的状态和日志文件。