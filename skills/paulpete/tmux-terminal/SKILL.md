---
name: tmux-terminal
description: 通过 tmux 实现交互式终端控制，适用于 TUI 应用程序、命令提示符（prompt）以及需要长时间运行的 CLI 工作流程。
hats: [developer, qa_tester]
---

# tmux-terminal

## 概述

tmux 是一个用于管理交互式终端会话的工具，支持多种 TUI（图形用户界面）工作流程，例如 `ralph-tui`。通过 tmux，您可以发送按键、捕获屏幕输出，并在会话的不同阶段保持进程的运行状态。

## 使用场景

- 测试 `ralph-tui` 或任何需要交互式命令行界面的应用程序
- 管理长时间运行的进程（如 Web 服务器、循环程序）
- 捕获终端输出以用于质量保证报告
- 与需要重新绘制屏幕的应用程序进行交互

## 先决条件

- 已安装 tmux（macOS 上已预装）

验证安装：
```bash
tmux -V
```

## 核心命令

- 创建一个分离的会话：
```bash
tmux new-session -d -s <name>
```

- 发送命令（按下 Enter 键执行命令）：
```bash
tmux send-keys -t <name> "<command>" Enter
```

- 捕获屏幕输出：
```bash
tmux capture-pane -t <name> -p
```

- 完成后终止会话：
```bash
tmux kill-session -t <name>
```

## 特殊按键

使用 `send-keys` 命令来发送特定的按键：
- `Enter`
- `C-c`（Ctrl+C）
- `C-d`（Ctrl-D）
- `Tab`
- `Escape`
- `Up`、`Down`、`Left`、`Right`

示例：
```bash
tmux send-keys -t <name> Up
tmux send-keys -t <name> C-c
```

## TUI（图形用户界面）交互模式

- **启动 ralph-tui**：
```bash
tmux new-session -d -s ralph-tui
tmux send-keys -t ralph-tui "cargo run -p ralph-tui" Enter
```

- **在 TUI 界面中导航**：
```bash
tmux send-keys -t ralph-tui Down
tmux send-keys -t ralph-tui Enter
```

- **捕获并解析屏幕内容**：
```bash
tmux capture-pane -t ralph-tui -p -S -200
```

- 使用 `-S -200` 命令在屏幕显示混乱时捕获最后 200 行内容。

## 长时间运行进程的管理

- 在 tmux 会话中启动服务器或循环程序，以确保它们持续运行。
- 使用 `capture-pane` 命令检查进程状态（查找 “listening” 或 “ready” 等提示信息）。
- 使用 `C-c` 终止会话，然后使用 `kill-session` 来彻底结束进程。

示例：
```bash
tmux new-session -d -s ralph-web
tmux send-keys -t ralph-web "cargo run -p ralph-cli -- web" Enter
tmux capture-pane -t ralph-web -p | rg -n "listening|ready"
tmux send-keys -t ralph-web C-c
tmux kill-session -t ralph-web
```

## 注意事项

- 会话名称应简短且唯一。
- 始终及时清理会话，以避免后台进程泄露。
- 如果捕获到的输出为空，请稍等片刻后再尝试捕获。