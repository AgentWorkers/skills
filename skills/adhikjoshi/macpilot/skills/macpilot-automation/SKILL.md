---
name: macpilot-automation
description: 使用 MacPilot CLI 的 macOS 核心自动化技能：通过 `macpilot` 命令，Claude Code 可以控制应用程序、输入文本、点击元素、运行 shell 命令，并在 macOS 上实现工作流程的自动化。
---
# MacPilot自动化

使用`macpilot`命令行工具（CLI）来自动化macOS的操作。MacPilot提供了100多个命令，用于控制鼠标、键盘、应用程序、窗口、用户界面（UI）、剪贴板、对话框、shell以及系统设置。所有命令都支持`--json`选项，以便输出结构化的数据。

## 使用场景

当用户需要以下操作时，可以使用此功能：
- 自动化macOS任务（如打开应用程序、点击按钮、输入文本、导航菜单）
- 以编程方式控制鼠标和键盘
- 通过辅助功能API与正在运行的应用程序交互
- 将多个自动化步骤组合成工作流程
- 运行shell命令或与终端交互
- 管理剪贴板、通知、音频和显示设置

## 先决条件

MacPilot必须已安装到`/Applications/MacPilot.app`目录下，并在`/usr/local/bin/macpilot`或`~/bin/macpilot`目录中创建一个符号链接。该应用程序需要在系统设置 > 隐私与安全 > 辅助功能中启用相应的权限。

## 核心命令参考

### 鼠标控制
```bash
macpilot click <x> <y>              # Left click at coordinates
macpilot doubleclick <x> <y>        # Double click
macpilot rightclick <x> <y>         # Right click
macpilot move <x> <y>               # Move cursor
macpilot drag <x1> <y1> <x2> <y2>  # Drag from point to point
macpilot scroll <up|down|left|right> [amount]  # Scroll (default: 3)
macpilot mouse-position --json      # Get current cursor position
```

### 键盘控制
```bash
macpilot keyboard type "Hello World"           # Type text
macpilot keyboard key cmd+c                    # Press shortcut
macpilot keyboard key enter                    # Press single key
macpilot chain "type:hello" "key:tab" "type:world"  # Chain actions
```
修饰键：`cmd`、`shift`、`alt`、`ctrl`、`fn`
特殊键：`enter`、`tab`、`space`、`escape`、`delete`、`f1`-`f12`、`up`、`down`、`left`、`right`

### 应用程序管理
```bash
macpilot app open "Safari"          # Open/launch app
macpilot app focus "Safari"         # Bring app to front
macpilot app frontmost --json       # Get frontmost app
macpilot app list --json            # List running apps
macpilot app quit "Safari"          # Quit app
macpilot app quit "Safari" --force  # Force quit
macpilot app hide "Safari"          # Hide app
```

### 菜单交互
```bash
macpilot menu click File Open --app Safari      # Click menu item
macpilot menu list --app Safari --json           # List all menus
macpilot menu list --app Safari --menu File      # List specific menu
```

### 剪贴板
```bash
macpilot clipboard get --json              # Read clipboard text
macpilot clipboard set "text"              # Set clipboard text
macpilot clipboard image photo.png         # Copy image to clipboard
macpilot clipboard info --json             # Content type, size, preview
macpilot clipboard types --json            # List all UTI types
macpilot clipboard clear --json            # Clear clipboard
macpilot clipboard paste --json            # Simulate Cmd+V
macpilot clipboard copy file.txt --json    # Copy file(s) to clipboard
macpilot clipboard save /tmp/out.png       # Save clipboard content to file

# Clipboard history (background daemon, max 50 items)
macpilot clipboard history start --json    # Start tracking
macpilot clipboard history stop --json     # Stop tracking
macpilot clipboard history list --json     # Show history
macpilot clipboard history search "text"   # Search history
macpilot clipboard history clear --json    # Delete history
```

### Shell命令
```bash
macpilot shell run "ls -la"                # Run command, get output
macpilot shell interactive "top"           # Open in Terminal
macpilot shell type "git status"           # Type into active terminal
macpilot shell paste "long command here"   # Paste via clipboard
```

### 系统控制
```bash
macpilot audio volume get --json           # Get volume (0-100)
macpilot audio volume set 50               # Set volume
macpilot audio volume mute                 # Mute
macpilot display brightness set 75         # Set brightness
macpilot appearance dark                   # Dark mode
macpilot appearance light                  # Light mode
macpilot notification send "Title" "Body"  # System notification
macpilot notification list --json          # List visible notifications
macpilot notification click --title "match" # Click notification by title
macpilot notification dismiss --json       # Dismiss top notification
macpilot notification dismiss --all        # Dismiss all notifications
macpilot system info --json                # System info
macpilot network wifi-name --json          # Wi-Fi name
macpilot network ip --json                 # IP address
```

### 等待与同步
```bash
macpilot wait seconds 2                          # Sleep 2 seconds
macpilot wait element "Save" --app TextEdit       # Wait for UI element
macpilot wait window "Untitled" --timeout 10      # Wait for window
macpilot watch events --duration 5 --json         # Monitor events
```

### 空间与 Dock
```bash
macpilot space list --json                  # List spaces
macpilot space switch right                 # Switch space
macpilot dock hide                          # Auto-hide dock
macpilot dock show                          # Always show dock
```

## 重要规则

1. **交互前务必聚焦应用程序**：在执行点击、输入或菜单操作之前，必须先使用`macpilot app focus "AppName"`命令聚焦应用程序。首次点击可能会被窗口激活所占用——请先点击应用程序的内容区域，然后再点击目标元素。
2. **使用`--json`进行数据解析**：当需要以编程方式解析输出时，务必添加`--json`选项。
3. **使用`ui find-text`获取坐标**：如果要点击某个特定元素，首先使用`macpilot ui find-text "label" --app AppName --json`获取其坐标，然后在该位置进行点击。
4. **使用`macpilot chain`组合复杂操作**：对于多步骤的键盘操作，建议使用`macpilot chain`而不是多个单独的命令。
5. **通过键盘设置文本字段值**：当焦点不确定时，使用`macpilot ui set-value`设置文本字段的值比直接键盘输入更可靠。
6. **等待元素加载**：在与尚未完全显示的UI元素交互之前，使用`macpilot wait element`确保元素已经加载完成。

## 示例工作流程

### 在Safari中打开URL
```bash
macpilot app open Safari
macpilot wait window Safari --timeout 5
macpilot app focus Safari
macpilot keyboard key cmd+l
macpilot keyboard type "https://example.com"
macpilot keyboard key enter
```

### 将文本从一个应用程序复制到另一个应用程序
```bash
macpilot app focus "TextEdit"
macpilot keyboard key cmd+a
macpilot keyboard key cmd+c
macpilot app focus "Notes"
macpilot keyboard key cmd+v
```

### 在TextEdit中创建新文件
```bash
macpilot app open TextEdit
macpilot wait window TextEdit --timeout 5
macpilot keyboard type "Hello from MacPilot!"
macpilot keyboard key cmd+s
macpilot wait seconds 1
macpilot dialog navigate "/Users/me/Desktop"
macpilot dialog set-field "myfile.txt"
macpilot dialog click-button "Save"
```