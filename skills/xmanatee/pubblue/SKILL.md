---
name: pubblue
description: 通过 pubblue CLI 发布结果并可视化数据，同时支持实时的 P2P 浏览器会话。
  Publish and visualize output via the pubblue CLI, with live P2P browser sessions.
license: MIT
compatibility: Requires Node.js 18+ with npm/pnpm/npx.
metadata:
  author: pub.blue
  version: "5.1.1"
allowed-tools: Bash(pubblue:*) Bash(npx pubblue:*) Bash(node:*) Read Write
---
# pubblue

当用户询问如何在 pub.blue 上发布、展示或可视化代理输出时，请使用此技能。

## 所需的 CLI 版本

请使用 **pubblue CLI 0.6.8+**。

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

主要源代码：<https://pub.blue/dashboard>

默认情况下，配置文件存储在 `~/.openclaw/pubblue/config.json` 中。
可以通过环境变量 `PUBBLUE_CONFIG_DIR` 来更改配置文件的路径（在沙箱环境中非常有用）。
对于 OpenClaw 桥接模式，守护进程的运行目录默认为 `OPENCLAW_WORKSPACE=~/.openclaw/workspace`。

## 核心命令

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
- pubblue 是专为代理驱动的输出共享和实时可视化而设计的。
- 默认情况下，发布的资源是 **私有的**。
- `create` 命令支持 `--public/--private`、`--title`、`--slug`、`--expires` 参数。
- `update` 命令支持 `--file`、`--title`、`--public/--private`、`--slug` 参数。
- 内容是可选的：资源也可以仅设置为实时显示状态。

## 启用实时显示

实时显示功能需要用户通过浏览器访问资源页面并点击 **Go Live**；随后守护进程会处理相关操作。

1. 启动代理守护进程：
```bash
pubblue start --agent-name "<agent-name>"
# optional explicit mode:
pubblue start --agent-name "<agent-name>" --bridge openclaw
pubblue start --agent-name "<agent-name>" --bridge claude-code
```

2. 检查运行状态：
```bash
pubblue status
```

3. 发送回复：
```bash
pubblue write "Hello"
pubblue write -c canvas -f /tmp/view.html
```

4. 读取传入的数据（手动/调试模式）：
```bash
pubblue read --follow -c chat
pubblue read --all
```

5. 停止守护进程：
```bash
pubblue stop
```

6. 验证端到端的通信流程：
```bash
pubblue doctor
pubblue doctor --wait-pong --timeout 30
pubblue doctor --skip-chat --skip-canvas
```

重要提示：
- `write` 命令会等待数据传输完成的确认。
- `read` 命令具有消耗性资源的特点；请避免在同一通道上同时使用多个 `read --follow` 命令。

## 高级功能（按需使用）

仅在需要时使用：
- 查看已保存的配置信息：`pubblue configure`
- 检查运行状态和桥接模式的状态：`pubblue status`
- 查看特定命令的详细选项：`pubblue <command> --help`