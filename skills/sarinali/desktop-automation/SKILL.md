---
name: desktop-control
description: 通过运行在端口8000上的CUA计算机服务器API来控制桌面。
version: 1.0.0
---
# 通过 CUA 服务器控制桌面

此功能允许 OpenClaw 使用 CUA 计算机服务器 API 来控制桌面。

## 先决条件

- CUA 计算机服务器运行在端口 8000 上
- 能够访问 `localhost:8000`（或配置的 `CUA_SERVER_URL`）

## 安装

要使用 OpenClaw 控制主机桌面，您需要在您的机器上安装并运行 CUA 计算机服务器。

### 快速入门（Python SDK）

在主机上安装 CUA 计算机服务器的最简单方法：

```bash
# Install the Computer SDK
pip install cua-computer-sdk

# Start the server (it will control your current desktop)
cua-server start --port 8000

# Or if you need to specify the display (Linux/Unix)
DISPLAY=:0 cua-server start --port 8000

# Verify it's running
curl http://localhost:8000/status
```

### 另一种选择：从源代码安装

如果您 prefer to install from source:

```bash
# Clone the repository
git clone https://github.com/trycua/cua-computer-server
cd cua-computer-server

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m cua_server --port 8000
```

### 作为后台服务运行

为了实现持续的桌面控制，请将其设置为系统服务：

**macOS (launchd):**
```bash
# Create a plist file
cat > ~/Library/LaunchAgents/com.cua.server.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cua.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/cua-server</string>
        <string>start</string>
        <string>--port</string>
        <string>8000</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

# Load the service
launchctl load ~/Library/LaunchAgents/com.cua.server.plist

# Start the service
launchctl start com.cua.server
```

**Linux (systemd):**
```bash
# Create service file
sudo tee /etc/systemd/system/cua-server.service > /dev/null <<EOF
[Unit]
Description=CUA Computer Server
After=network.target

[Service]
Type=simple
User=$USER
Environment="DISPLAY=:0"
Environment="XAUTHORITY=/home/$USER/.Xauthority"
ExecStart=/usr/local/bin/cua-server start --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable cua-server
sudo systemctl start cua-server

# Check status
sudo systemctl status cua-server
```

**Windows (任务调度程序):**
```powershell
# Create a scheduled task to run at startup
$action = New-ScheduledTaskAction -Execute "cua-server.exe" -Argument "start --port 8000"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "CUA Server" -Action $action -Trigger $trigger -Principal $principal -Settings $settings
```

### 配置选项

根据您的需求配置服务器：

```bash
# Basic start with default settings
cua-server start

# Custom port
cua-server start --port 8001

# With authentication token (recommended if exposing to network)
cua-server start --port 8000 --auth-token your-secret-token

# Specify display (Linux/Unix)
DISPLAY=:1 cua-server start --port 8000

# Bind to all interfaces (careful - exposes to network!)
cua-server start --bind 0.0.0.0 --port 8000 --auth-token required-if-exposed
```

### 安全注意事项

⚠️ **重要提示**：出于安全考虑，服务器默认仅监听 `localhost`（127.0.0.1）。这意味着只有您机器上的进程才能连接到它。

- **仅限本地使用（默认设置）**：适用于个人使用 OpenClaw 的情况
- **网络访问**：仅在具有适当防火墙规则和身份验证的情况下使用 `--bind 0.0.0.0`
- **身份验证**：如果服务器可以从网络访问，请始终使用 `--auth-token`

### 验证

安装完成后，验证服务器是否正常工作：

```bash
# Check server status
curl http://localhost:8000/status

# List available commands
curl http://localhost:8000/commands | jq

# Take a test screenshot of your desktop
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "screenshot"}' \
  | jq -r '.result.base64' \
  | base64 -d > test-screenshot.png

# View the screenshot
open test-screenshot.png       # macOS
xdg-open test-screenshot.png   # Linux
start test-screenshot.png      # Windows
```

如果您看到了当前桌面的截图，说明服务器运行正常！

### 故障排除

**端口已被占用：**
```bash
# Check what's using port 8000
lsof -i :8000              # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Solution: Use a different port
cua-server start --port 8001
```

**权限被拒绝（Linux）：**
```bash
# You may need to add your user to the input group for keyboard/mouse control
sudo usermod -a -G input $USER
# Log out and back in for changes to take effect
```

**找不到显示器（Linux）：**
```bash
# Check your display variable
echo $DISPLAY

# Set it explicitly
DISPLAY=:0 cua-server start --port 8000
```

**服务器无响应：**
```bash
# Check if the process is running
ps aux | grep cua-server       # Linux/macOS
tasklist | findstr cua-server  # Windows

# Try running in foreground to see errors
cua-server start --port 8000 --debug
```

## 可用命令

### 截取屏幕截图

捕获当前屏幕：
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "screenshot"}' \
  | jq -r '.result.base64' \
  | base64 -d > screenshot.png
```

### 在指定坐标点击

在特定的 x,y 坐标点击：
```bash
# Click at center of 1280x720 screen
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "left_click", "params": {"x": 640, "y": 360}}'
```

### 右键点击
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "right_click", "params": {"x": 640, "y": 360}}'
```

### 双击
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "double_click", "params": {"x": 640, "y": 360}}'
```

### 输入文本

在当前光标位置输入文本：
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "type_text", "params": {"text": "Hello, World!"}}'
```

### 按下热键

按下键组合：
```bash
# Ctrl+C
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "hotkey", "params": {"keys": ["ctrl", "c"]}}'

# Ctrl+Alt+T (open terminal)
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "hotkey", "params": {"keys": ["ctrl", "alt", "t"]}}'
```

### 按下单个键

按下单个键：
```bash
# Press Enter
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "press_key", "params": {"key": "enter"}}'

# Press Escape
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "press_key", "params": {"key": "escape"}}'
```

### 移动光标

将光标移动到指定位置：
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "move_cursor", "params": {"x": 100, "y": 200}}'
```

### 滚动

向上或向下滚动：
```bash
# Scroll down 3 units
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "scroll_direction", "params": {"direction": "down", "amount": 3}}'

# Scroll up 5 units
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "scroll_direction", "params": {"direction": "up", "amount": 5}}'
```

### 启动应用程序

通过名称启动应用程序：
```bash
# Launch Firefox
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "launch", "params": {"app": "firefox"}}'

# Launch Terminal
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "launch", "params": {"app": "xfce4-terminal"}}'
```

### 打开文件或 URL

使用默认应用程序打开文件或 URL：
```bash
# Open URL
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "open", "params": {"path": "https://example.com"}}'

# Open file
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "open", "params": {"path": "/home/cua/document.txt"}}'
```

### 获取窗口信息

获取当前窗口的 ID：
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_current_window_id"}'
```

### 窗口操作

最大化窗口：
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "maximize_window", "params": {"window_id": "0x1234567"}}'
```

最小化窗口：
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "minimize_window", "params": {"window_id": "0x1234567"}}'
```

## 示例工作流程

### 浏览器导航示例

打开 Firefox 并导航到某个网站：
```bash
# Take initial screenshot
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "screenshot"}' -o initial.json

# Launch Firefox
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "launch", "params": {"app": "firefox"}}'
sleep 3

# Focus address bar (Ctrl+L)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "l"]}}'
sleep 1

# Type URL
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "https://example.com"}}'

# Press Enter
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
sleep 5

# Take final screenshot
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "screenshot"}' -o final.json
```

### 文本编辑器示例

打开文本编辑器并输入内容：
```bash
# Open terminal
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "alt", "t"]}}'
sleep 2

# Type command to open text editor
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "mousepad"}}'
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
sleep 2

# Type some text
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "Hello from OpenClaw!\nThis is automated desktop control."}}'

# Save file (Ctrl+S)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "hotkey", "params": {"keys": ["ctrl", "s"]}}'
sleep 1

# Type filename
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "openclaw-demo.txt"}}'
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "enter"}}'
```

### 填写表单示例

填写网页表单：
```bash
# Assuming browser is open with form visible

# Click on first input field (adjust coordinates)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "left_click", "params": {"x": 400, "y": 300}}'

# Type name
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "John Doe"}}'

# Tab to next field
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "tab"}}'

# Type email
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "john@example.com"}}'

# Tab to next field
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "press_key", "params": {"key": "tab"}}'

# Type message
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "type_text", "params": {"text": "This form was filled automatically by OpenClaw!"}}'

# Submit form (click submit button)
curl -X POST http://localhost:8000/cmd -H "Content-Type: application/json" -d '{"command": "left_click", "params": {"x": 400, "y": 500}}'
```

## 辅助函数

### 检查服务器状态
```bash
curl http://localhost:8000/status
```

### 列出所有可用命令
```bash
curl http://localhost:8000/commands | jq
```

### 获取屏幕尺寸
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_screen_size"}'
```

### 获取光标位置
```bash
curl -X POST http://localhost:8000/cmd \
  -H "Content-Type: application/json" \
  -d '{"command": "get_cursor_position"}'
```

## 环境变量

- `CUA_SERVER_URL`：CUA 服务器的基本 URL（默认：http://localhost:8000）

## 提示

1. **命令执行间隔**：在命令之间添加 `sleep` 以确保用户界面能够及时更新
2. **坐标确认**：屏幕尺寸为 1280x720，中心坐标为 (640, 360)
3. **截图调试**：在操作前后截图以进行验证
4. **使用变量**：将坐标和文本存储在变量中以便重复使用

## OpenClaw 使用示例

一旦加载了此功能，您就可以在 OpenClaw 对话中使用了：

```
User: "Take a screenshot and open Firefox"
OpenClaw: *executes the screenshot and launch firefox commands*

User: "Type 'Hello World' in the current window"
OpenClaw: *executes the type_text command*

User: "Click at the center of the screen"
OpenClaw: *executes click command at 640,360*
```

## 故障排除

1. **连接被拒绝**：确保 CUA 服务器正在端口 8000 上运行
2. **无响应**：检查是否在容器中运行或是否设置了 SSH 隧道
3. **命令无效**：使用 `curl http://localhost:8000/status` 进行验证
4. **坐标错误**：请记住屏幕尺寸为 1280x720，请相应地调整坐标