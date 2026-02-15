---
name: computer-use
description: **全桌面计算机使用方案：适用于无显示器的Linux服务器和VPS**  
该方案通过创建虚拟显示界面（Xvfb + XFCE），实现无需物理显示器即可控制图形用户界面（GUI）应用程序的功能。用户可执行所有标准的操作，包括截图、鼠标点击、键盘输入、滚动以及拖拽等。同时，系统还提供了无闪烁效果的VNC（Virtual Network Computing）连接功能，支持实时远程查看。该方案具有高度的兼容性，适用于任何类型的Linux服务器和大型语言模型（LLM，Large Language Model）。
version: 1.2.0
---

# 计算机使用技巧

针对无头Linux服务器，提供了完整的桌面图形界面（GUI）控制功能。通过创建一个虚拟显示（Xvfb + XFCE），可以在没有物理显示器的情况下在VPS或云实例上运行和控制桌面应用程序。

## 环境配置

- **显示端口**：`:99`
- **分辨率**：1024x768（XGA，推荐使用）
- **桌面环境**：XFCE4（极简版——仅包含xfwm4和面板）

## 快速设置

运行设置脚本以完成所有配置（包括systemd服务及无闪烁效果的VNC连接）：

```bash
./scripts/setup-vnc.sh
```

该脚本会安装以下内容：
- 在`:99`端口上启动Xvfb虚拟显示
- 极简版的XFCE桌面环境（仅包含xfwm4和面板，不包含xfdesktop）
- 带有稳定性优化选项的x11vnc服务器
- 用于浏览器访问的noVNC工具

所有服务会在系统启动时自动启动，并在崩溃后自动重启。

## 常用操作指南

| 操作        | 脚本            | 参数            | 说明                                      |
|-------------|------------------|------------------|-----------------------------------------|
| 截屏        | `screenshot.sh`       |                 | 截取屏幕并转换为base64 PNG格式                   |
| 移动鼠标      | `mouse_move.sh`       | x y             | 将鼠标移动到指定坐标                         |
| 左键点击      | `click.sh`       | x y left         | 在指定坐标处执行左键点击                     |
| 右键点击      | `click.sh`       | x y right         | 在指定坐标处执行右键点击                     |
| 中键点击      | `click.sh`       | x y middle         | 在指定坐标处执行中键点击                     |
| 双击        | `click.sh`       | x y double         | 在指定坐标处执行双击                         |
| 三击        | `click.sh`       | x y triple         | 在指定坐标处执行三击                         |
| 拖动        | `drag.sh`       | x1 y1 x2 y2         | 从起点拖动到终点                         |
| 按下鼠标左键    | `mouse_down.sh`      |                 | 按下鼠标左键                             |
| 释放鼠标左键    | `mouse_up.sh`      |                 | 释放鼠标左键                             |
| 输入文本      | `type_text.sh`       | "text"           | 以50个字符为一段输入文本，每段输入间隔12毫秒           |
| 按键        | `key.sh`       | "combo"           | 按下指定按键（如Return、Ctrl+C、Alt+F4）             |
| 长时间按住按键    | `hold_key.sh`       | "key" seconds       | 按住指定按键指定时间                         |
| 滚动屏幕      | `scroll.sh`       | dir amt [x y]         | 向上/下/左/右滚动屏幕                         |
| 等待        | `wait.sh`       | seconds           | 等待指定时间后截图                         |
| 缩放屏幕      | `zoom.sh`       | x1 y1 x2 y2         | 截取指定区域的屏幕截图                     |

## 使用示例

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

## 工作流程

1. **截屏**——首先查看屏幕内容。
2. **分析**——识别用户界面元素及其坐标。
3. **执行操作**——点击、输入文本、滚动屏幕。
4. **再次截屏**——验证操作结果。
5. **重复上述步骤**。

## 提示

- 屏幕分辨率为1024x768，原点位于屏幕左上角(0,0)。
- 在输入文本框前请先点击以聚焦输入框。
- 在浏览器中，可以使用`Ctrl+End`快速跳转到页面底部。
- 大量文本会分多次输入（每次50个字符），每次输入之间有12毫秒的延迟。
- 长文本会分多次输入，每次输入之间有12毫秒的延迟。

## 实时查看桌面（通过VNC）

可以通过浏览器或VNC客户端实时查看桌面内容。

### 通过浏览器连接

```bash
# SSH tunnel (run on your local machine)
ssh -L 6080:localhost:6080 your-server

# Open in browser
http://localhost:6080/vnc.html
```

### 通过VNC客户端连接

```bash
# SSH tunnel
ssh -L 5900:localhost:5900 your-server

# Connect VNC client to localhost:5900
```

### SSH配置（推荐）

将以下配置添加到`~/.ssh/config`文件中以实现自动隧道连接：

```
Host your-server
  HostName your.server.ip
  User your-user
  LocalForward 6080 127.0.0.1:6080
  LocalForward 5900 127.0.0.1:5900
```

之后只需输入`ssh your-server`，即可通过VNC访问远程服务器。

## 系统服务配置

```bash
# Check status
systemctl status xvfb xfce-minimal x11vnc novnc

# Restart if needed
sudo systemctl restart xvfb xfce-minimal x11vnc novnc
```

### 服务依赖关系

```
xvfb → xfce-minimal → x11vnc → novnc
```

- **xvfb**：负责创建虚拟显示（端口：:99，分辨率：1024x768x24）
- **xfce-minimal**：监控xfwm4和面板的运行状态，并在需要时关闭xfdesktop。
- **x11vnc**：作为VNC服务器，使用`-noxdamage`选项确保显示稳定。
- **novnc**：作为WebSocket代理，通过心跳信号保持连接稳定。

## 打开应用程序

```bash
export DISPLAY=:99
google-chrome --no-sandbox &    # Chrome (recommended)
xfce4-terminal &                # Terminal
thunar &                        # File manager
```

**注意**：在无头服务器上，Firefox和Chromium等浏览器可能存在沙箱限制。建议使用Chrome的deb包进行安装：

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
```

## 手动设置

如果不想使用`setup-vnc.sh`脚本，可以手动进行配置：

```bash
# Install packages
sudo apt install -y xvfb xfce4 xfce4-terminal xdotool scrot imagemagick dbus-x11 x11vnc novnc websockify

# Copy service files
sudo cp systemd/*.service /etc/systemd/system/

# Edit xfce-minimal.service: replace %USER% and %SCRIPT_PATH%
sudo nano /etc/systemd/system/xfce-minimal.service

# Mask xfdesktop (prevents VNC flickering)
sudo mv /usr/bin/xfdesktop /usr/bin/xfdesktop.real
echo -e '#!/bin/bash\nexit 0' | sudo tee /usr/bin/xfdesktop
sudo chmod +x /usr/bin/xfdesktop

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable --now xvfb xfce-minimal x11vnc novnc
```

## 常见问题解决方法

### VNC显示黑屏
- 检查xfwm4是否正在运行：`pgrep xfwm4`
- 重启桌面服务：`sudo systemctl restart xfce-minimal`

### VNC画面闪烁
- 确保xfdesktop已被禁用（检查`/usr/bin/xfdesktop`文件）。
- xfdesktop可能导致Xvfb在显示过程中出现闪烁现象。

### VNC连接频繁断开
- 确保noVNC配置中使用了`--heartbeat 30`选项。
- 检查x11vnc是否使用了`-noxdamage`选项。

### x11vnc崩溃（SIGSEGV错误）
- 尝试添加`-noxdamage -noxfixes`选项。
- `DAMAGE`扩展程序可能会导致Xvfb崩溃。

## 必需安装的软件

通过`setup-vnc.sh`脚本可以自动安装所有必需的软件：  
```bash
xvfb xfce4 xfce4-terminal xdotool scrot imagemagick dbus-x11 x11vnc novnc websockify
```