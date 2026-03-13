---
name: cmux
description: "通过 `cmux` 终端多路复用器的 Unix 套接字 API 来对其进行控制。适用于以下场景：  
(1) 列出、创建、选择或关闭工作区；  
(2) 分割窗口并管理显示界面；  
(3) 向终端发送文本或按键信息；  
(4) 创建通知；  
(5) 设置侧边栏状态、进度条或日志记录；  
(6) 查询系统状态。  
需要使用 `cmux` 命令行工具（CLI）或位于 `/tmp/cmux.sock` 的 Unix 套接字。"
---
# cmux

通过其 Unix 套接字 API 或 CLI 以编程方式控制 cmux 终端多路复用器。

## 套接字连接

```bash
SOCKET_PATH="${CMUX_SOCKET_PATH:-/tmp/cmux.sock}"
```

发送 JSON-RPC 请求：
```json
{"id":"req-1","method":"workspace.list","params":{}}
```

## CLI 快速参考

```bash
# Output as JSON
cmux --json <command>

# Target specific workspace/surface
cmux --workspace <id> --surface <id> <command>
```

## 工作区

| 操作 | CLI | 套接字方法 |
|--------|-----|---------------|
| 列出所有工作区 | `cmux list-workspaces` | `workspace.list` |
| 创建新工作区 | `cmux new-workspace` | `workspace.create` |
| 选择工作区 | `cmux select-workspace --workspace <id>` | `workspace.select` |
| 获取当前工作区 | `cmux current-workspace` | `workspace.current` |
| 关闭工作区 | `cmux close-workspace --workspace <id>` | `workspace.close` |

## 分割屏幕与显示区域

| 操作 | CLI | 套接字方法 |
|--------|-----|---------------|
| 创建新的分割屏幕 | `cmux new-split <方向>` | `surface.split` (方向: 左/右/上/下) |
| 列出显示区域 | `cmux list-surfaces` | `surface.list` |
| 焦点切换到显示区域 | `cmux focus-surface --surface <id>` | `surface.focus` |

## 输入操作

| 操作 | CLI | 套接字方法 |
|--------|-----|---------------|
| 发送文本 | `cmux send "echo hello"` | `surface.send_text` |
| 发送按键信号 | `cmux send-key enter` | `surface.send_key` |
| 向指定显示区域发送命令 | `cmux send-surface --surface <id> "cmd"` | `surface.send_text` (需要指定显示区域 ID) |

支持的按键：`enter`, `tab`, `escape`, `backspace`, `delete`, `up`, `down`, `left`, `right`

## 通知

```bash
cmux notify --title "Title" --body "Body"
# Socket: notification.create
```

## 侧边栏元数据

| 操作 | CLI | 套接字方法 |
|--------|-----|---------------|
| 设置状态 | `cmux set-status <键> <值>` | (仅限通过套接字操作) |
| 清除状态 | `cmux clear-status <键>` | (仅限通过套接字操作) |
| 设置进度条状态 | `cmux set-progress 0.5 --label "Building..."` | (仅限通过套接字操作) |
| 清除进度条 | `cmux clear-progress` | (仅限通过套接字操作) |
| 记录日志 | `cmux log "消息" --level error` | (仅限通过套接字操作) |
| 清除日志 | `cmux clear-log` | (仅限通过套接字操作) |

## 系统信息

| 操作 | CLI | 套接字方法 |
|--------|-----|---------------|
| 发送 Ping 请求 | `cmux ping` | `system.ping` |
| 查看系统功能 | `cmux capabilities` | `system.capabilities` |
| 识别当前上下文 | `cmux identify` | `system.identify` |

## Python 客户端

```python
import json
import os
import socket

SOCKET_PATH = os.environ.get("CMUX_SOCKET_PATH", "/tmp/cmux.sock")

def rpc(method, params=None, req_id=1):
    payload = {"id": req_id, "method": method, "params": params or {}}
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(SOCKET_PATH)
        sock.sendall(json.dumps(payload).encode("utf-8") + b"\n")
        return json.loads(sock.recv(65536).decode("utf-8"))

# List workspaces
print(rpc("workspace.list", req_id="ws"))

# Send notification
print(rpc("notification.create", {"title": "Hello", "body": "From Python!"}))
```

## Shell 辅助工具

```bash
cmux_cmd() {
    SOCK="${CMUX_SOCKET_PATH:-/tmp/cmux.sock}"
    printf "%s\n" "$1" | nc -U "$SOCK"
}

cmux_cmd '{"id":"ws","method":"workspace.list","params":{}}'
```

## 检查 cmux 是否可用

```bash
[ -S "${CMUX_SOCKET_PATH:-/tmp/cmux.sock}" ] && echo "cmux socket available"
command -v cmux &>/dev/null && echo "cmux CLI available"
```