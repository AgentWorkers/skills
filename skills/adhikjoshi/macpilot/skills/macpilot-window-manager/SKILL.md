---
name: macpilot-window-manager
description: 使用 MacPilot 管理 macOS 的窗口。可以执行以下操作：列出窗口、移动窗口、调整窗口大小、将窗口固定在屏幕边缘、最小化窗口、将窗口全屏显示以及重新排列窗口的位置。该工具支持多显示器显示和“Spaces”功能（即多个桌面布局）。
---
# MacPilot 窗口管理器

使用 MacPilot 来控制 macOS 上的应用程序窗口——可以列出窗口、移动窗口、调整窗口大小、将窗口吸附到指定位置、最小化窗口、全屏显示，以及在不同的工作空间（Spaces）和显示器（Displays）之间管理窗口。

## 使用场景

在以下情况下可以使用此功能：
- 需要排列或整理应用程序窗口
- 需要将窗口移动到特定位置或调整窗口大小
- 需要将窗口吸附到屏幕的半边或角落
- 需要查看当前打开的所有窗口
- 需要聚焦某个窗口或将其置于前台
- 需要在多个工作空间或显示器之间管理窗口
- 需要保存和恢复窗口布局

## 窗口操作命令

### 列出所有窗口
```bash
macpilot window list --json                        # All visible windows
macpilot window list --app "Safari" --json         # Windows for specific app
macpilot window list --all-spaces --json           # Include all Spaces
```

### 聚焦窗口
```bash
macpilot window focus "Safari" --json                          # Focus app's main window
macpilot window focus "Safari" --title "GitHub" --json         # Focus by title substring
```

### 创建新窗口
```bash
macpilot window new "Safari" --json                # Open new window in app
```

### 移动窗口
```bash
macpilot window move "Safari" 100 50 --json        # Move to x=100, y=50
```

### 调整窗口大小
```bash
macpilot window resize "Safari" 1200 800 --json    # Set width=1200, height=800
```

### 关闭窗口
```bash
macpilot window close --app "Safari" --json        # Close frontmost window
```

### 最小化/全屏显示
```bash
macpilot window minimize "Safari" --json           # Minimize to Dock
macpilot window fullscreen "Safari" --json         # Toggle fullscreen
```

### 将窗口吸附到指定位置
```bash
macpilot window snap "Safari" left --json          # Left half of screen
macpilot window snap "Safari" right --json         # Right half of screen
macpilot window snap "Safari" top-left --json      # Top-left quarter
macpilot window snap "Safari" top-right --json     # Top-right quarter
macpilot window snap "Safari" bottom-left --json   # Bottom-left quarter
macpilot window snap "Safari" bottom-right --json  # Bottom-right quarter
macpilot window snap "Safari" center --json        # Center of screen
macpilot window snap "Safari" maximize --json      # Fill entire screen
```

### 保存/恢复窗口布局
```bash
macpilot window restore --save --json              # Save all window positions
macpilot window restore --json                     # Restore saved positions
macpilot window restore --save --app "Safari"      # Save specific app only
```

## 工作空间（Spaces）与显示器（Displays）

```bash
macpilot space list --json                         # List all Spaces
macpilot space switch left --json                  # Switch to left Space
macpilot space switch right --json                 # Switch to right Space
macpilot space switch 2 --json                     # Switch to Space 2
macpilot space bring --app "Slack" --json          # Bring app to current Space
```

## 常用工作流程

### 并排布局
```bash
macpilot window snap "Safari" left
macpilot window snap "VS Code" right
```

### 四窗口布局（4 个应用程序）
```bash
macpilot window snap "Safari" top-left
macpilot window snap "Terminal" top-right
macpilot window snap "Finder" bottom-left
macpilot window snap "Notes" bottom-right
```

### 演示模式设置
```bash
# Maximize the presentation app
macpilot window snap "Keynote" maximize
# Or go fullscreen
macpilot window fullscreen "Keynote"
```

### 开发环境布局
```bash
# Editor on left 60%, terminal on right 40%
macpilot window move "VS Code" 0 25
macpilot window resize "VS Code" 1152 775
macpilot window move "Terminal" 1152 25
macpilot window resize "Terminal" 768 775
```

### 收集所有窗口
```bash
# Bring scattered windows back to current Space
macpilot space bring --app "Safari"
macpilot space bring --app "Terminal"
macpilot space bring --app "Finder"
```

### 保存和恢复工作区设置
```bash
# Before a meeting - save your layout
macpilot window restore --save

# After the meeting - restore it
macpilot window restore
```

## 提示：

- 在重新排列窗口之前，可以使用 `window list --json` 命令查看窗口的当前位置和大小
- `snap` 命令会根据窗口当前所在的显示器来执行吸附操作
- 当多个窗口存在时，建议使用 `window focus` 而不是 `app focus`
- 使用 `display-info --json` 命令获取屏幕尺寸以进行精确的位置调整
- 坐标系以左上角为原点（0,0 表示主显示器的左上角）
- 在多显示器设置中，次级显示器的 x 坐标可能是负数（表示位于主显示器左侧），或者 x 坐标大于主显示器的宽度（表示位于主显示器右侧）