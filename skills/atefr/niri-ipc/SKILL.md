---
name: niri-ipc
description: 在 Linux 上，可以通过 Niri Wayland 组合器的 IPC（`niri msg --json` / `$NIRI_SOCKET`）来对其进行控制。当需要查询 Niri 的状态（输出、工作区、当前聚焦的窗口）或执行某些操作（聚焦/移动/关闭窗口、切换工作区、运行命令、重新加载配置）时，可以使用该方式。这些操作可以在运行于 Niri 会话中的 OpenClaw 代理上完成。
---

# Niri IPC

您可以通过 `niri msg` CLI（推荐方式）或向 `$NIRI SOCKET` 发送 JSON 请求来使用 Niri IPC。

本技能的前提条件如下：
- 您正在运行 Niri 的 Linux 系统上。
- `$NIRI SOCKET` 已被正确设置（通常在 Niri 会话中已经设置好）。

## 快速入门（推荐）

使用随附的帮助脚本（该脚本是对 `niri msg --json` 的封装）：

```bash
./skills/niri-ipc/scripts/niri.py version
./skills/niri-ipc/scripts/niri.py outputs
./skills/niri-ipc/scripts/niri.py workspaces
./skills/niri-ipc/scripts/niri.py windows
./skills/niri-ipc/scripts/niri.py focused-window
```

## 更深入的控制

### 1) 高级辅助工具（窗口匹配）

当您需要根据窗口的 **标题** 或 **应用 ID** 来查找窗口时，可以使用 `scripts/niri_ctl.py`：

```bash
# List windows (optionally filtered)
./skills/niri-ipc/scripts/niri_ctl.py list-windows --query firefox

# Focus a window by substring match
./skills/niri-ipc/scripts/niri_ctl.py focus firefox

# Close a matched window (focus then close)
./skills/niri-ipc/scripts/niri_ctl.py close firefox

# Move a matched window to a workspace (by index or by name)
./skills/niri-ipc/scripts/niri_ctl.py move-to-workspace firefox 3
./skills/niri-ipc/scripts/niri_ctl.py move-to-workspace firefox web

# Focus a workspace by index or name
./skills/niri-ipc/scripts/niri_ctl.py focus-workspace 2
./skills/niri-ipc/scripts/niri_ctl.py focus-workspace web
```

### 2) 完整的 IPC 访问（原始套接字）

使用 `scripts/niri_socket.py` 直接与 `$NIRI SOCKET` 通信（数据格式为以换行符分隔的 JSON）：

```bash
# Send a simple request (JSON string)
./skills/niri-ipc/scripts/niri_socket.py raw '"FocusedWindow"'

# Batch requests: one JSON request per line on stdin
printf '%s\n' '"FocusedWindow"' '"Workspaces"' | ./skills/niri-ipc/scripts/niri_socket.py stdin

# Event stream (prints JSON events until interrupted)
./skills/niri-ipc/scripts/niri_socket.py event-stream
```

### 操作

通过 Niri 执行各种操作：

```bash
# Focus workspace by index
./skills/niri-ipc/scripts/niri.py action focus-workspace 2

# Move focused window to workspace
./skills/niri-ipc/scripts/niri.py action move-window-to-workspace 3

# Focus a window by id
./skills/niri-ipc/scripts/niri.py action focus-window 123

# Close focused window
./skills/niri-ipc/scripts/niri.py action close-window

# Reload niri config
./skills/niri-ipc/scripts/niri.py action load-config-file

# Spawn (no shell)
./skills/niri-ipc/scripts/niri.py action spawn -- alacritty

# Spawn through shell
./skills/niri-ipc/scripts/niri.py action spawn-sh -- 'notify-send hello'
```

### 输出配置

使用封装后的 `niri msg output ...` 命令来配置输出格式：

```bash
./skills/niri-ipc/scripts/niri.py output --help
```

## 直接使用 `niri msg`

如果您不需要辅助脚本，可以直接调用 `niri msg`：

```bash
niri msg --json windows
niri msg --json action focus-workspace 2
```

提示：如果在升级后出现 `niri msg` 解析错误，请重启 compositor（因为新的 `niri msg` 可能与旧的 compositor 不兼容）。

## 事件流

Niri 可以提供事件流，适用于状态栏或后台进程：

```bash
# Raw JSON event lines (runs until interrupted)
./skills/niri-ipc/scripts/niri.py event-stream

# Just a few lines for a quick test
./skills/niri-ipc/scripts/niri.py event-stream --lines 5
```

## 故障排除

- 如果命令执行失败并显示 “NIRI SOCKET 未设置” 的错误，请确保您在 Niri 会话中操作，或者手动输出 `$NIRI SOCKET` 的路径。
- 如果您需要了解套接字协议的详细信息，请阅读 `./skills/niri-ipc/references/ipc.md`。
- 如果您的自动化需求较为复杂（例如根据窗口标题或应用 ID 来选择窗口），请先查询所有窗口的信息，然后再根据窗口 ID 执行相应的操作。