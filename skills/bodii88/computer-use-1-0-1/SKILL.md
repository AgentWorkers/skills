---
name: computer-use
description: **全桌面计算机使用方案：适用于无显示器的Linux服务器和VPS**  
该方案通过创建一个虚拟显示环境（Xvfb + XFCE），实现无需物理显示器即可控制图形用户界面（GUI）应用程序的功能。用户可以执行所有标准的操作，包括截图、鼠标点击、键盘输入、滚动以及拖拽等。该方案具有高度的通用性，适用于任何类型的自然语言模型（LLM），且不依赖于具体的模型架构。
---

# 计算机使用技巧

对于无显示器的 Linux 服务器，可以完全通过图形用户界面（GUI）进行控制。系统会创建一个虚拟显示界面（Xvfb + XFCE），这样你就可以在没有物理显示器的情况下，在虚拟私有服务器（VPS）或云服务器上运行和控制桌面应用程序。

## 环境配置

- **显示端口**：`:99`
- **分辨率**：1024x768（XGA，推荐使用）
- **桌面环境**：XFCE4

## 快速入门

```bash
export DISPLAY=:99

# Take screenshot
./scripts/screenshot.sh

# Click at coordinates
./scripts/click.sh 512 384 left

# Type text
./scripts/type_text.sh "Hello world"

# Press key combo
./scripts/key.sh "ctrl+s"

# Scroll down
./scripts/scroll.sh down 5
```

## 操作参考

| 操作 | 脚本 | 参数 | 描述 |
|--------|--------|-----------|-------------|
| 截屏 | `screenshot.sh` | — | 截取屏幕并转换为 base64 格式的 PNG 图片 |
| 获取鼠标位置 | `cursor_position.sh` | — | 获取当前鼠标的位置（X, Y 坐标） |
| 移动鼠标 | `mouse_move.sh` | x y | 将鼠标移动到指定的坐标 |
| 左键点击 | `click.sh` | x y left | 在指定的坐标处左键点击 |
| 右键点击 | `click.sh` | x y right | 在指定的坐标处右键点击 |
| 中键点击 | `click.sh` | x y middle | 在指定的坐标处中键点击 |
| 双击 | `click.sh` | x y double | 双击 |
| 三击 | `click.sh` | x y triple | 三击（用于选择文本行） |
| 拖动 | `drag.sh` | x1 y1 x2 y2 | 从起点拖动到终点 |
| 按下鼠标左键 | `mouse_down.sh` | — | 按下鼠标左键 |
| 释放鼠标左键 | `mouse_up.sh` | — | 释放鼠标左键 |
| 输入文本 | `type_text.sh` | "text" | 逐段输入文本（每次输入 50 个字符，间隔 12 毫秒） |
| 按键 | `key.sh` | "combo" | 按下指定的键（如 Return、Ctrl+C、Alt+F4） |
| 长时间按住键 | `hold_key.sh` | "key" seconds | 按住指定的键指定时间 |
| 滚动屏幕 | `scroll.sh` | dir amt [x y] | 向上/下/左/右滚动屏幕 |
| 等待 | `wait.sh` | seconds | 等待指定时间后截图 |
| 缩放屏幕 | `zoom.sh` | x1 y1 x2 y2 | 截取指定区域的屏幕截图 |

## 工作流程

1. **截图**：首先查看屏幕内容。
2. **分析**：识别用户界面元素及其坐标。
3. **执行操作**：进行点击、输入文本或滚动等操作。
4. **再次截图**：验证操作结果。
5. **重复上述步骤**。

## 使用技巧

- 屏幕分辨率为 1024x768，原点位于屏幕的左上角（0,0）。
- 在输入文本框前，请先点击以聚焦输入框。
- 在浏览器中，可以使用 `Ctrl+End` 键跳转到页面底部。
- 大部分操作会在 2 秒后自动截图。
- 长文本会分多次输入（每次 50 个字符），每次输入之间有 12 毫秒的延迟。

## 系统服务

```bash
# Services auto-start on boot
sudo systemctl status virtual-desktop   # Xvfb on :99
sudo systemctl status xfce-desktop      # XFCE session

# Manual restart if needed
sudo systemctl restart virtual-desktop xfce-desktop
```

## 打开应用程序

```bash
export DISPLAY=:99
chromium-browser --no-sandbox &    # Web browser
xfce4-terminal &                   # Terminal
thunar &                           # File manager
```

## 所需系统软件

需要安装的系统软件包（安装一次即可）：
```bash
sudo apt install -y xvfb xfce4 xfce4-terminal xdotool scrot imagemagick dbus-x11 chromium-browser
```