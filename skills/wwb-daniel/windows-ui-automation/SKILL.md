---
name: windows-ui-automation
description: 使用 PowerShell 自动化 Windows 图形用户界面（GUI）操作（鼠标、键盘、窗口）。当用户需要在桌面上模拟用户输入时，例如移动光标、点击按钮、在非网页应用程序中输入文本或管理窗口状态，可以使用此方法。
---

# Windows UI Automation

通过编程方式控制 Windows 桌面环境。

## 核心功能

- **鼠标**：移动鼠标、点击（左键/右键/双击）、拖动。
- **键盘**：输入文本、按下特殊键（Enter、Tab、Alt 等）。
- **窗口**：查找窗口、将窗口置于焦点、最小化/最大化以及截图。

## 使用指南

### 鼠标控制

使用提供的 PowerShell 脚本 `mouse_control.ps1.txt`：

```powershell
# Move to X, Y
powershell -File skills/windows-ui-automation/mouse_control.ps1.txt -Action move -X 500 -Y 500

# Click at current position
powershell -File skills/windows-ui-automation/mouse_control.ps1.txt -Action click

# Right click
powershell -File skills/windows-ui-automation/mouse_control.ps1.txt -Action rightclick
```

### 键盘控制

使用 `keyboard_control.ps1.txt`：

```powershell
# Type text
powershell -File skills/windows-ui-automation/keyboard_control.ps1.txt -Text "Hello World"

# Press Enter
powershell -File skills/windows-ui-automation/keyboard_control.ps1.txt -Key "{ENTER}"
```

### 窗口管理

通过窗口标题将窗口置于焦点：
```powershell
$wshell = New-Object -ComObject WScript.Shell; $wshell.AppActivate("Notepad")
```

## 最佳实践

1. **安全性**：始终缓慢移动鼠标，或在操作之间添加延迟。
2. **验证**：在执行复杂的 UI 操作前后截图，以确认操作结果。
3. **坐标**：请注意，坐标 (0,0) 位于主显示器的左上角。