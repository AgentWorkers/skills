---
name: computer-use
description: **全桌面计算机用于无头Linux服务器**：通过`Xvfb`和`XFCE`虚拟桌面结合`xdotool`实现自动化操作（包括点击、输入、滚动、截图、拖拽等17种动作）。与`OpenClaw`的浏览器工具不同，该方案在`X11`层面上运行，因此网站无法检测到这些自动化操作。同时支持使用`VNC`进行实时查看。
version: 1.2.1
---
# 计算机使用技巧

**无头Linux服务器的全桌面GUI控制**：通过创建虚拟显示（Xvfb + XFCE），您可以在没有物理显示器的VPS或云实例上运行和控制桌面应用程序。

## 环境配置

- **显示端口**：`:99`
- **分辨率**：1024x768（XGA，推荐使用）
- **桌面环境**：XFCE4（极简版——仅包含xfwm4和面板）

## 快速设置

运行设置脚本以安装所有所需组件（systemd服务、无闪烁效果的VNC客户端）：

```bash
./scripts/setup-vnc.sh
```

该脚本会安装以下内容：
- 在`:99`端口上创建Xvfb虚拟显示
- 极简版的XFCE桌面（仅包含xfwm4和面板，不包含xfdesktop）
- 带有稳定性选项的x11vnc客户端
- 用于浏览器访问的无VNC客户端（noVNC）

所有服务会在系统启动时自动启动，并在崩溃后自动重启。

## 操作参考

| 操作 | 脚本 | 参数 | 说明 |
|--------|--------|-----------|-------------|
| 截图 | `screenshot.sh` | — | 截取屏幕并转换为base64 PNG格式 |
| 移动鼠标 | `mouse_move.sh` | x y | 将鼠标移动到指定坐标 |
| 左键点击 | `click.sh` | x y left | 在指定坐标处左键点击 |
| 右键点击 | `click.sh` | x y right | 在指定坐标处右键点击 |
| 中键点击 | `click.sh` | x y middle | 在指定坐标处中键点击 |
| 双击 | `click.sh` | x y double | 双击 |
| 三击 | `click.sh` | x y triple | 三击（用于选择文本行） |
| 拖动 | `drag.sh` | x1 y1 x2 y2 | 从起点拖动到终点 |
| 按下鼠标左键 | `mouse_down.sh` | — | 按下鼠标左键 |
| 释放鼠标左键 | `mouse_up.sh` | — | 释放鼠标左键 |
| 输入文本 | `type_text.sh` | "text" | 以50个字符为单位输入文本（每次输入间隔12毫秒） |
| 按键 | `key.sh` | "combo" | 按下指定键（如Return、Ctrl+C、Alt+F4） |
| 长时间按住键 | `hold_key.sh` | "key" seconds | 按住指定键指定的时间 |
| 滚动屏幕 | `scroll.sh` | dir amt [x y] | 向上/下/左/右滚动屏幕 |
| 等待 | `wait.sh` | seconds | 等待指定时间后截图 |
| 缩放屏幕 | `zoom.sh` | x1 y1 x2 y2 | 截取指定区域的屏幕截图 |

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

1. **截图**：首先查看屏幕内容。
2. **分析**：识别用户界面元素及其坐标。
3. **操作**：执行点击、输入、滚动等操作。
4. **再次截图**：验证操作结果。
5. **重复上述步骤**。

## 提示

- 屏幕分辨率为1024x768，原点位于左上角（0,0）。
- 在输入文本框前请先点击以聚焦输入框。
- 在浏览器中，可以使用`Ctrl+End`快速跳到页面底部。
- 大量文本会分批输入（每次50个字符），每次输入之间有12毫秒的延迟。
- 长文本会分批处理，每次输入之间有12毫秒的延迟。

## 实时查看桌面（通过VNC）

您可以通过浏览器或VNC客户端实时查看桌面内容。

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

之后，只需执行`ssh your-server`即可使用VNC客户端连接。

## 系统服务

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

- **xvfb**：创建虚拟显示（端口：:99，分辨率：1024x768x24）
- **xfce-minimal**：负责运行xfwm4和面板，会自动关闭xfdesktop。
- **x11vnc**：提供稳定的VNC服务（使用`-noxdamage`选项）。
- **noVNC**：作为WebSocket代理，用于保持连接的稳定性。

## 打开应用程序

```bash
export DISPLAY=:99

# Chrome — only use --no-sandbox if the kernel lacks user namespace support.
# Check: cat /proc/sys/kernel/unprivileged_userns_clone
#   1 = sandbox works, do NOT use --no-sandbox
#   0 = sandbox fails, --no-sandbox required as fallback
# Using --no-sandbox when unnecessary causes instability and crashes.
if [ "$(cat /proc/sys/kernel/unprivileged_userns_clone 2>/dev/null)" = "0" ]; then
    google-chrome --no-sandbox &
else
    google-chrome &
fi

xfce4-terminal &                # Terminal
thunar &                        # File manager
```

**注意**：在无头服务器上，Firefox和Chromium等浏览器可能存在沙箱限制。建议使用Chrome的`.deb`包。

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f
```

## 手动设置

如果您不希望使用`setup-vnc.sh`脚本，可以手动进行配置：

```bash
# Install packages
sudo apt install -y xvfb xfce4 xfce4-terminal xdotool scrot imagemagick dbus-x11 x11vnc novnc websockify

# Run the setup script (generates systemd services, masks xfdesktop, starts everything)
./scripts/setup-vnc.sh
```

如果您希望完全手动配置系统，`setup-vnc.sh`脚本会自动生成所有必要的systemd服务文件。请仔细阅读该脚本以了解具体的服务配置细节。

## 故障排除

### VNC显示黑屏
- 检查xfwm4是否正在运行：`pgrep xfwm4`
- 重启桌面环境：`sudo systemctl restart xfce-minimal`

### VNC画面闪烁
- 确保xfdesktop被禁用（检查`/usr/bin/xfdesktop`文件）。
- xfdesktop可能导致Xvfb显示画面闪烁（因为其绘制过程会导致画面刷新）。

### VNC连接频繁中断
- 确保noVNC客户端使用了`--heartbeat 30`选项。
- 检查x11vnc客户端是否使用了`-noxdamage`选项。

### x11vnc崩溃（出现SIGSEGV错误）
- 添加`-noxdamage -noxfixes`选项以解决崩溃问题。
- `DAMAGE`扩展程序可能会导致Xvfb出现崩溃。

## 所需软件

通过`setup-vnc.sh`脚本可以安装所有必要的软件：```bash
xvfb xfce4 xfce4-terminal xdotool scrot imagemagick dbus-x11 x11vnc novnc websockify
```