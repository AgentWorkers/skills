---
name: desktop-control
description: 在 Windows 上控制桌面应用程序：可以启动、关闭、切换窗口的焦点、调整窗口大小、移动窗口、模拟键盘/鼠标输入、管理进程、控制 VSCode、读取剪贴板内容以及捕获屏幕信息。当用户需要与正在运行的程序交互、切换窗口、输入文本、使用快捷键、在 VSCode 中打开文件、管理正在运行的进程或获取系统显示信息时，可以使用这些功能。
---

# 桌面控制——全面的 Windows 应用程序控制功能

## 仅限发布的说明（ClawHub）
此发布包包含 `.ps1.txt` 格式的脚本，因为 ClawHub 仅接受文本文件。  
下载后，请将每个 `.ps1.txt` 文件重命名为 `.ps1`，并将其放入 `scripts/` 文件夹中，以便使用该功能。

您可以通过 PowerShell 脚本来控制这台 Windows 机器上的任何桌面应用程序：启动程序、管理窗口、模拟输入、控制 VSCode 以及监控进程。

## 关键提示：脚本的位置  
所有脚本都位于该功能文件夹的相对路径下：  
```
SKILL_DIR = ~/.openclaw/workspace/skills/desktop-control/scripts
```

运行脚本时，请始终使用完整路径：  
```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/<script>.ps1" -Action <action> [params]
```

## 重要安全规则：  
1. **关闭窗口前**——询问用户是否有关未保存的数据。  
2. **终止进程前**——除非用户明确要求，否则务必先确认。  
3. **发送输入前**——确保目标窗口已处于焦点状态。  
4. **剪贴板操作**——在覆盖剪贴板内容时请提醒用户。  

---

## 功能参考：  

### 1. 窗口管理 (`app-control.ps1`)  
- 管理应用程序窗口：启动、关闭、切换焦点、调整大小、移动、固定窗口位置。  
  - **列出所有可见窗口**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action list-windows
```  
    返回信息：进程 ID (PID)、窗口标题、位置 (X, Y)、大小 (宽度 × 高度)、状态 (正常/最小化/最大化)  
  - **启动应用程序**  
    ```powershell
# By name (searches PATH and common locations)
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action launch -Target "notepad"

# By full path
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action launch -Target "C:\Program Files\MyApp\app.exe"

# With arguments
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action launch -Target "code" -Arguments "C:\Users\ibach\project"
```  
  - **切换窗口焦点**  
    ```powershell
# By window title (partial match)
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action focus -Target "Visual Studio Code"

# By PID
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action focus -ProcId 12345
```  
  - **优雅地关闭窗口**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action close -Target "Notepad"
```  
  - **最小化/最大化/恢复窗口**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action minimize -Target "Visual Studio Code"
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action maximize -Target "Visual Studio Code"
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action restore -Target "Visual Studio Code"
```  
  - **移动窗口**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action move -Target "Notepad" -X 100 -Y 200
```  
  - **调整窗口大小**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action resize -Target "Notepad" -Width 800 -Height 600
```  
  - **将窗口固定到屏幕一半**  
    ```powershell
# Options: left, right, top, bottom, topleft, topright, bottomleft, bottomright
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/app-control.ps1" -Action snap -Target "Notepad" -Position left
```  

---

### 2. 输入模拟 (`input-sim.ps1`)  
- 模拟键盘和鼠标输入到任何应用程序中。  
  **重要提示**：在发送输入前，请使用 `app-control.ps1 -Action focus` 先将目标窗口切换到焦点状态。  
  - **输入文本**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action type-text -Text "Hello, World!"
```  
  - **发送键盘快捷键**  
    ```powershell
# Common shortcuts: Ctrl+S, Ctrl+C, Ctrl+V, Ctrl+Z, Alt+F4, Ctrl+Shift+P, Win+D
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action send-keys -Keys "Ctrl+S"
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action send-keys -Keys "Ctrl+Shift+P"
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action send-keys -Keys "Alt+Tab"
```  
  - **发送特殊按键**  
    ```powershell
# Keys: Enter, Tab, Escape, Backspace, Delete, Up, Down, Left, Right, Home, End, PageUp, PageDown, F1-F12
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action send-keys -Keys "Enter"
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action send-keys -Keys "F5"
```  
  - **在指定坐标点击鼠标**  
    ```powershell
# Left click
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action mouse-click -X 500 -Y 300

# Right click
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action mouse-click -X 500 -Y 300 -Button right

# Double click
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action mouse-click -X 500 -Y 300 -DoubleClick
```  
  - **移动鼠标**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action mouse-move -X 500 -Y 300
```  
  - **滚动屏幕**  
    ```powershell
# Scroll up (positive) or down (negative)
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action mouse-scroll -Clicks 3
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/input-sim.ps1" -Action mouse-scroll -Clicks -3
```  

---

### 3. VSCode 控制 (`vscode-control.ps1`)  
- 通过 `code` CLI 和扩展程序来控制 Visual Studio Code。  
  - **打开文件**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action open-file -Path "C:\Users\ibach\project\main.py"
```  
  - **在指定行打开文件**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action goto -Path "C:\Users\ibach\project\main.py" -Line 42
```  
  - **打开文件夹/工作区**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action open-folder -Path "C:\Users\ibach\project"
```  
  - **打开差异视图**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action open-diff -Path "file1.py" -Path2 "file2.py"
```  
  - **列出已安装的扩展程序**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action list-extensions
```  
  - **安装扩展程序**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action install-extension -ExtensionId "ms-python.python"
```  
  - **卸载扩展程序**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action uninstall-extension -ExtensionId "ms-python.python"
```  
  - **在 VSCode 中打开新终端**  
    ```powershell
# This focuses VSCode and sends Ctrl+` to toggle terminal
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action new-terminal
```  
  - **打开 VSCode 命令面板**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action command-palette
```  
  - **按名称运行 VSCode 命令**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/vscode-control.ps1" -Action run-command -Command "workbench.action.toggleSidebarVisibility"
```  

---

### 4. 进程管理 (`process-manager.ps1`)  
- 监控和管理正在运行的进程。  
  - **列出所有进程**  
    ```powershell
# All processes
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/process-manager.ps1" -Action list

# Filter by name
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/process-manager.ps1" -Action list -Name "code"

# Top N by memory
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/process-manager.ps1" -Action list -SortBy memory -Top 10
```  
  - **获取进程详细信息**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/process-manager.ps1" -Action info -ProcId 12345
```  
  - **启动新进程**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/process-manager.ps1" -Action start -Path "notepad.exe" -Arguments "C:\file.txt"
```  
  - **终止进程（请先确认用户意愿）**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/process-manager.ps1" -Action kill -ProcId 12345
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/process-manager.ps1" -Action kill -Name "notepad"
```  
  - **监控进程资源使用情况**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/process-manager.ps1" -Action monitor -ProcId 12345 -Duration 10
```  

---

### 5. 屏幕与系统信息 (`screen-info.ps1`)  
- 获取显示信息、窗口详情、剪贴板内容以及截图。  
  - **列出所有显示器/监视器**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/screen-info.ps1" -Action displays
```  
  - **获取活动（焦点）窗口的信息**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/screen-info.ps1" -Action active-window
```  
  - **获取窗口详细信息**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/screen-info.ps1" -Action window-info -Target "Visual Studio Code"
```  
  - **截取屏幕截图**  
    ```powershell
# Full screen
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/screen-info.ps1" -Action screenshot -OutputPath "$HOME/screenshot.png"

# Specific window
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/screen-info.ps1" -Action screenshot -Target "Notepad" -OutputPath "$HOME/notepad-screenshot.png"
```  
  - **读取剪贴板内容**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/screen-info.ps1" -Action clipboard-get
```  
  - **设置剪贴板文本**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/screen-info.ps1" -Action clipboard-set -Text "Text to copy"
```  
  - **获取系统信息（运行时间、操作系统、分辨率）**  
    ```powershell
powershell -ExecutionPolicy Bypass -File "$HOME/.openclaw/workspace/skills/desktop-control/scripts/screen-info.ps1" -Action system-info
```  

---

## 常见操作流程：  
- 在 VSCode 中打开文件并跳转到指定行。  
- 在指定应用程序中输入内容。  
- 保存当前应用程序中的文档。  
- 将两个窗口并排排列。  
- 强制关闭卡住的应用程序。  
- 截取特定窗口的截图。  

---

## 错误处理：  
- 如果脚本返回退出代码 0，则表示成功。  
- 如果脚本返回退出代码 1，则表示出现错误（请查看 stderr 输出以获取详细信息）。  
- 如果找不到某个窗口，请先使用 `list-windows` 命令获取其准确标题。  
- 如果找不到 `code` CLI，可能是因为 VSCode 未添加到系统路径中；请尝试先启动 VSCode。  

## 故障排除：  
- **“找不到窗口”**——使用 `list-windows` 命令查看窗口的准确标题，然后进行更精确的匹配。  
- **“访问被拒绝”**——某些系统进程需要管理员权限，请告知用户。  
- **输入操作无效**——确保目标窗口处于焦点状态且处于前台。  
- **VSCode CLI 未找到**——尝试先运行 `code --version` 命令；如果仍未找到，请从“开始菜单”中启动 VSCode。