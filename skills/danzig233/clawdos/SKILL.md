---
name: clawdos
description: "通过Clawdos API实现Windows自动化：支持屏幕截图、鼠标/键盘操作、窗口管理、文件系统操作以及shell命令执行。也可通过Python脚本以独立CLI（命令行界面）的形式进行操作。适用于用户需要远程控制或检查Windows主机的情况。"
license: "MIT"
metadata:
  openclaw:
    version: "2.1.1"
    display_name: "Windows Execution Interface for OpenClaw"
    author: "DANZIG MOE"
    emoji: "🐾"
    python_requires: ">=3.10"
    dependencies:
      - "requests>=2.28.0"
    requires:
      env:
        - "CLAWDOS_BASE_URL"
        - "CLAWDOS_API_KEY"
        - "CLAWDOS_TIMEOUT"
        - "CLAWDOS_FS_ROOT_ID"
    primaryEnv: "CLAWDOS_API_KEY"
    config_schema:
      base_url:
        type: "string"
        default: "http://127.0.0.1:17171"
        description: "Clawdos Windows host service address"
      api_key:
        type: "string"
        required: true
        description: "Clawdos API key"
      timeout:
        type: "integer"
        default: 30
        description: "Request timeout in seconds"
      fs_root_id:
        type: "string"
        description: "Sandbox root directory ID for file system operations"
---
# Clawdos

## 概述

该技能提供了一个基于 CLI 的接口，用于调用 Clawdos 的 REST API，允许您通过 Shell 命令从 OpenClaw 安全地操作 Windows 机器。无需加载额外的工具，只需使用 `exec` 命令来执行独立的 Python 脚本 `scripts/clawdos.py` 即可。

### ⚠️ 安全性与沙箱机制

**文件系统沙箱保护：**
- 所有文件系统操作（`fs_list`、`fs_read`、`fs_write`、`fs_delete`、`fs_move`）都被限制在 Windows 主机的沙箱根目录内执行。
- 沙箱根目录由 `CLAWDOS_FS_ROOT_ID` 环境变量配置，并在服务器端进行强制执行。
- Clawdos 服务会阻止访问沙箱目录之外的文件。任何尝试遍历路径的操作（例如 `../../../`）都会被阻止。
- 这种隔离机制确保了技能操作不会意外或故意访问敏感的系统文件、用户文档或配置文件。

**网络隔离：**
- Clawdos 服务仅与配置的 `CLAWDOS_BASE_URL` 进行通信，不会建立未经授权的外部连接。
- 所有的 API 调用都通过 `CLAWDOS_API_KEY` 进行身份验证，并在适用的情况下通过 HTTPS 加密传输。

### ⚠️ 权限与功能警告

该技能提供了强大的 Windows 自动化功能。用户必须明确了解并授权以下操作：

1. **Shell 命令执行**（`shell_exec`）：
   - 可以在 Windows 主机上执行任意的 PowerShell 或 cmd 命令。
   - 即使在沙箱内，这些命令也可能修改系统状态、安装软件或更改配置。
   - **仅允许来自可信来源并经过用户明确授权的使用。**

2. **文件删除**（`fs_delete`）：
   - 会永久删除沙箱内的文件和目录。
   - 一旦删除，文件无法恢复。
   - **请务必谨慎操作；在执行前确认删除意图。**

3. **文件上传/下载**（`--file`、`--out`）：
   - 该脚本可以从本地文件系统读取文件并上传到 Windows 主机（在沙箱内）。
   - 也可以从 Windows 主机下载文件到代理系统。
   **请勿对敏感文件或不可信的远程系统使用此功能。**

4. **屏幕/窗口监控**：
   - 可以观察活动中的 GUI 内容（`screen_capture`、`window_list`、`window_focus`）。
   - 如果屏幕上显示了敏感信息，这些信息可能会被捕获。

### ⚠️ 使用要求
**该技能需要您的 Windows 主机上运行相应的服务器程序。**请确保 Windows 主机上正在运行 `danzig233/clawdos`。连接参数（`CLAWDOS_BASE_URL` 和 `CLAWDOS_API_KEY`）必须通过 OpenClaw 的技能配置界面或环境变量进行配置，具体配置方法请参考本文件的元数据。

## 使用方法

您可以通过使用 `exec` 命令运行 `scripts/clawdos.py` 脚本来与 Clawdos 进行交互。脚本会自动获取 OpenClaw 注入的 `CLAWDOS_BASE_URL` 和 `CLAWDOS_API_KEY` 环境变量。

**基本语法：**
```bash
python3 ~/.nvm/versions/node/v22.22.1/lib/node_modules/openclaw/skills/clawdos/scripts/clawdos.py <action> --args '{"key":"value"}'
```

### 可用的操作

#### 1. 视觉导航与系统检查
- `health`：检查服务状态。
- `get_env`：获取屏幕分辨率、DPI 比率和当前活动窗口。
- `window_list`：列出所有打开的窗口。
- `window_focus`：聚焦某个窗口。参数：`{"titleContains": "..."}` 或 `{"processName": "..."}`
- `screen_capture`：截取屏幕截图。使用 `--out path/to/save.png` 可以将截图保存为图片文件。参数：`{"format": "png", "quality": 80}`

#### 2. 精确输入（鼠标与键盘）
*（尽可能优先使用键盘/Shell，以避免视觉估计错误）*
- `click`：点击鼠标。参数：`{"x": 100, "y": 200, "button": "left"}`
- `move`：移动鼠标光标。参数：`{"x": 100, "y": 200}``
- `drag`：拖动鼠标。参数：`{"fromX": 100, "fromY": 200, "toX": 300, "toY": 400}``
- `keys`：按指定组合键。参数：`{"combo": ["ctrl", "c"]`
- `type_text`：输入文本。参数：`{"text": "hello"}`
- `scroll`：滚动鼠标滚轮。参数：`{"amount": -500}``
- `batch`：顺序执行多个输入操作。参数：`{"actions": [...]}`

#### 3. 文件与系统操作
- `fs_list`：列出目录内容。参数：`{"path": "/"}`
- `fs_read`：读取文件内容（将原始内容输出到标准输出）。使用 `--out path/to/save.bin` 可以将文件保存为二进制文件。参数：`{"path": "/hello.txt"}`
- `fs_write`：写入文件内容。参数：`{"path": "/hello.txt", "content": "hello world"}`。或者使用 `--file path/to/local.bin` 上传本地二进制文件。
- `fs_mkdir`：创建目录。参数：`{"path": "/newdir"}`
- `fs_delete`：删除文件或目录。参数：`{"path": "/newdir", "recursive": true}``
- `fs_move`：移动或重命名文件/目录。参数：`{"from": "/src", "to": "/dst"}`
- `shell_exec`：在 Windows 主机上运行 Shell 命令。参数：`{"command": "dir", "args": ["/w"], "workingDir": ""}`

### 操作最佳实践
- **优先使用键盘与 Shell**：为了减少因视觉坐标估计导致的错误，尽可能优先使用键盘快捷键（`key_combo`、`type_text`）或 Shell 命令（`shell_exec`），而不是鼠标操作。
- **有针对性的鼠标操作**：仅将精确的鼠标操作（`mouse_click`、`mouse_move`、`mouse_drag`）用于必要的 UI 操作（例如点击网页上的特定按钮、导航软件界面或聚焦输入框）。
- **滚动**：使用 `mouse.scroll` 可以安全地浏览长页面或文档。

### 安全最佳实践
- **验证文件路径**：始终确认目标路径位于指定的沙箱目录内。虽然服务器会进行隔离，但在脚本中仍需再次检查路径。
- **审核 Shell 命令**：在执行 `shell_exec` 命令之前，请仔细检查命令内容。避免从不可信的来源执行命令。
- **文件传输限制**：仅上传/下载您信任的文件。切勿使用 `--file` 传输包含敏感信息或系统文件的文件。
- **减少屏幕截图**：如果屏幕上可能显示敏感信息（如密码、令牌或个人数据），请避免截图。
- **明确确认删除操作**：在执行 `fs_delete` 之前，请仔细确认目标路径。删除的文件无法恢复。

## 示例

**聚焦 MS Edge 并输入文本：**
```bash
python3 scripts/clawdos.py window_focus --args '{"processName": "msedge"}'
python3 scripts/clawdos.py type_text --args '{"text": "https://openclaw.ai\n"}'
```

**截取屏幕截图并保存到本地：**
```bash
python3 scripts/clawdos.py screen_capture --out /tmp/windows_screen.png --args '{"format":"png"}'
```

**从 Windows 读取文件内容：**
```bash
python3 scripts/clawdos.py fs_read --args '{"path": "logs/app.log"}'
```

**在 Windows 上执行 PowerShell 命令：**
```bash
python3 scripts/clawdos.py shell_exec --args '{"command": "powershell", "args": ["-Command", "Get-Process"]}'
```