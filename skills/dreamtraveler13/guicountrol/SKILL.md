---
name: linux-gui-control
description: "使用 xdotool、wmctrl 和 dogtail 来控制 Linux 桌面图形用户界面（GUI）。当您需要与非浏览器应用程序交互、模拟鼠标/键盘输入、管理窗口或检查 X11/GNOME 系统下应用程序的 UI 结构时，这些工具非常实用。支持的功能包括：  
(1) 在应用程序中点击或输入内容；  
(2) 调整窗口大小或移动窗口；  
(3) 从应用程序中提取基于文本的 UI 信息（适用于视障用户）；  
(4) 截取屏幕截图以供视觉分析。"
---

# Linux GUI 控制

本技能提供了用于自动化操作 Linux 桌面环境的工具和流程。

## 快速入门

### 1. 确定目标窗口
使用 `wmctrl` 来查找您想要控制的窗口的精确名称。
```bash
wmctrl -l
```

### 2. 检查 UI 层次结构
对于支持无障碍功能的应用程序（GNOME 应用程序、使用 `--force-renderer-accessibility` 参数的 Electron 应用程序），可以使用检查脚本来获取按钮名称，而无需截图。
```bash
python3 scripts/inspect_ui.py "<app_name>"
```

### 3. 执行操作
通过辅助脚本使用 `xdotool` 来执行常见的操作。
```bash
# Activate window
./scripts/gui_action.sh activate "<window_name>"

# Click coordinates
./scripts/gui_action.sh click 500 500

# Type text
./scripts/gui_action.sh type "Hello World"

# Press a key
./scripts/gui_action.sh key "Return"
```

## 工作流程

### 通过文本界面操作应用程序
1. 使用 `wmctrl -l` 列出所有窗口。
2. 激活目标窗口。
3. 运行 `scripts/inspect_ui.py` 以获取按钮和输入元素的列表。
4. 使用 `xdotool key Tab` 和 `Return` 来导航；如果知道坐标，也可以直接使用 `click` 命令。
5. 如果基于文本的检查失败，可以切换到截图方式并使用视觉辅助工具进行操作。

### 强制启用 Electron 应用程序的无障碍功能
许多现代应用程序（如 VS Code、Discord、Cider、Chrome）需要设置特定的标志才能显示其 UI 树结构：
```bash
pkill <app>
nohup <app> --force-renderer-accessibility > /dev/null 2>&1 &
```

## 工具参考

- **wmctrl**：窗口管理工具（列出、激活、移动、调整大小）。
- **xdotool**：输入模拟工具（点击、输入、按键、鼠标移动）。
- **dogtail**：通过 AT-SPI（无障碍总线）提取 UI 树结构。
- **scrot**：轻量级的截图工具。