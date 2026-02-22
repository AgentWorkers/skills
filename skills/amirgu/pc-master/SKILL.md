---
name: pc-master
description: 通过 WSL2 来控制 Windows 电脑。当用户需要打开/关闭应用程序、管理进程、截图、控制窗口、管理 Windows 系统下的文件（C:\ 目录中的文件）、自动化任务，或执行任何需要与 Windows 主机交互的操作时（例如“打开 Chrome 浏览器”、“关闭 Spotify 应用程序”、“截图”、“列出正在运行的应用程序”、“移动 Windows 系统下的文件”等），都可以使用该功能。
---
# PC Master — 通过 WSL2 控制 Windows 应用程序

所有 Windows 可执行文件都可以通过 `/mnt/c/Windows/System32/` 路径访问。可以直接在 bash 中调用这些文件。

## 先决条件

WSL2 的互操作性必须正常工作。如果 `.exe` 文件在调用时出现 `UtilAcceptVsock` 错误，请让用户在 Windows 中运行 `wsl --shutdown`，然后重新启动 WSL。

## 核心命令

### 进程管理
```bash
# List all processes
/mnt/c/Windows/System32/tasklist.exe

# Filter by name
/mnt/c/Windows/System32/tasklist.exe /FI "IMAGENAME eq chrome.exe"

# Kill by name
/mnt/c/Windows/System32/taskkill.exe /F /IM chrome.exe

# Kill by PID
/mnt/c/Windows/System32/taskkill.exe /F /PID 1234
```

### 启动应用程序
```bash
# Open a URL in default browser
/mnt/c/Windows/System32/cmd.exe /c "start https://google.com"

# Open an app by name
/mnt/c/Windows/System32/cmd.exe /c "start chrome"
/mnt/c/Windows/System32/cmd.exe /c "start spotify"
/mnt/c/Windows/System32/cmd.exe /c "start notepad"

# Open a file with its default app
/mnt/c/Windows/System32/cmd.exe /c "start C:\\Users\\User\\file.pdf"

# Launch full path
/mnt/c/Windows/System32/cmd.exe /c "start \"\" \"C:\\Program Files\\App\\app.exe\""
```

> ⚠️ `cmd.exe /c start` 必须从 Windows 路径中执行。如果当前工作目录（cwd）是一个 UNC 路径（即 WSL 路径），请使用 `/mnt/c/Windows/System32/cmd.exe /c "cd /d C:\ && start ..."`。

### PowerShell（高级用法）
```bash
PS=/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe

# Run a command
$PS -NonInteractive -Command "Get-Process | Select-Object -First 10"

# Get window titles
$PS -NonInteractive -Command "Get-Process | Where-Object {$_.MainWindowTitle} | Select-Object Name, MainWindowTitle"

# Set volume
$PS -NonInteractive -Command "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"
```

### 截图
```bash
# Take a screenshot and save to Windows desktop
PS=/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe
$PS -NonInteractive -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Screen]::PrimaryScreen | ForEach-Object { \$bmp = New-Object System.Drawing.Bitmap(\$_.Bounds.Width, \$_.Bounds.Height); \$g = [System.Drawing.Graphics]::FromImage(\$bmp); \$g.CopyFromScreen(\$_.Bounds.Location, [System.Drawing.Point]::Empty, \$_.Bounds.Size); \$bmp.Save('C:\\screenshot.png') }"
```

### 文件系统（Windows 路径）
```bash
# Windows C:\ is at /mnt/c/ in WSL
ls /mnt/c/Users/
cat /mnt/c/Users/Username/Desktop/file.txt
cp /mnt/c/Users/Username/Downloads/file.zip /mnt/c/Users/Username/Desktop/

# Find Windows username
ls /mnt/c/Users/ | grep -v "Public\|Default\|All Users"
```

### 系统信息
```bash
# Windows version
/mnt/c/Windows/System32/cmd.exe /c "ver"

# Disk usage
/mnt/c/Windows/System32/cmd.exe /c "wmic logicaldisk get size,freespace,caption"

# Network info
/mnt/c/Windows/System32/ipconfig.exe
```

## 常用操作

**关闭并重新打开应用程序：**
```bash
/mnt/c/Windows/System32/taskkill.exe /F /IM chrome.exe
sleep 2
/mnt/c/Windows/System32/cmd.exe /c "start chrome"
```

**检查应用程序是否正在运行：**
```bash
/mnt/c/Windows/System32/tasklist.exe /FI "IMAGENAME eq spotify.exe" | grep -i spotify && echo "Running" || echo "Not running"
```

**打开特定网站：**
```bash
/mnt/c/Windows/System32/cmd.exe /c "start https://www.google.com"
```

## 注意事项：
- 输出内容可能包含乱码（因为 Windows 的编码格式与 UTF-8 不同），但这属于正常现象，内容仍然可以正常阅读。
- 通过 `start` 命令启动的一些图形界面（GUI）应用程序可能不会产生输出，这是预期中的行为。
- 对于交互式的 PowerShell 脚本，建议将输出内容写入临时文件中后再读取，而不是直接捕获标准输出（stdout）。
- 有关常见应用程序的可执行文件名称，请参阅 `references/windows-apps.md`。