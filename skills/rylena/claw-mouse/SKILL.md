---
name: claw-mouse
description: 通过使用 `xdotool` 和 `scrot`，可以通过截图、移动鼠标、点击以及输入文本来控制 Linux X11 桌面。
homepage: https://github.com/rylena/claw-mouse
metadata:
  openclaw:
    requires:
      bins: [python3, xdotool, scrot]
---
# claw-mouse

该工具为 Linux 的 X11 环境提供了一个小巧的、可脚本化的桌面 GUI 控制辅助工具。它主要用于自动化执行以下操作：
1) 截取屏幕截图
2) 确定点击位置
3) 移动鼠标、点击或输入文本
4) 重复上述操作

该工具内部使用了以下工具来实现这些功能：
- `scrot`：用于截取屏幕截图
- `xdotool`：用于控制鼠标、键盘和窗口

## 文件结构

- `desktopctl.py`：命令行脚本（CLI）

## 系统要求

- 运行 X11 的 Linux 系统（不支持仅使用 Wayland 的系统）
- Python 3
- `xdotool` 工具
- `scrot` 工具

### Ubuntu/Debian 系统的依赖安装

```bash
sudo apt-get update
sudo apt-get install -y xdotool scrot
```

## 使用方法

从该工具的目录中，执行以下命令来使用该工具：

```bash
python3 desktopctl.py screenshot
python3 desktopctl.py click 500 300
python3 desktopctl.py type "hello"
python3 desktopctl.py key ctrl+l
python3 desktopctl.py windows
python3 desktopctl.py activate "Chromium"
```

### DISPLAY 和 XAUTHORITY 设置

如果你在通过守护进程或无头 shell 运行该工具，且 `DISPLAY` 环境变量未设置，请按照以下方式配置：

```bash
DISPLAY=:0 XAUTHORITY=$HOME/.Xauthority python3 desktopctl.py screenshot
```

或者，你也可以通过命令行参数来指定 `DISPLAY` 和 `XAUTHORITY` 的值：

```bash
python3 desktopctl.py --display :0 --xauthority $HOME/.Xauthority screenshot
```

## 安全提示

该工具会直接在你的实际桌面会话中进行操作（包括点击和输入）。请谨慎使用。

## 更新记录

- 0.1.0：初始版本发布。