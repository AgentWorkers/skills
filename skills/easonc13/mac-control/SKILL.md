---
name: mac-control
description: 使用 cliclick 和 AppleScript 通过鼠标/键盘自动化来控制 Mac。它可以用于点击 UI 元素、截取屏幕截图、获取窗口边界、处理 Retina 显示屏上的坐标缩放，以及自动化各种 UI 操作，例如点击 Chrome 扩展程序图标、关闭对话框或工具栏按钮。
---
# Mac 控制

使用 clicclick（鼠标/键盘）和系统工具自动化 Mac 用户界面交互。

## 工具

- **clicclick**：`/opt/homebrew/bin/clicclick` - 鼠标/键盘控制工具
- **screencapture**：内置的截图工具
- **magick**：用于图像分析的 ImageMagick 工具
- **osascript**：用于获取窗口信息的 AppleScript

## 坐标系统（Eason 的 Mac Mini）

**当前设置**：1920x1080 的显示器，**1:1 缩放**（无需转换！）

- 截图坐标 = clicclick 获取的坐标
- 如果截图中元素的坐标为 (800, 500)，则在 (800, 500) 点点击

### 对于 Retina 显示器（2x 缩放）

如果截图的分辨率是实际分辨率的 2 倍：
```bash
# Convert: cliclick_coords = screenshot_coords / 2
cliclick c:$((screenshot_x / 2)),$((screenshot_y / 2))
```

### 校准脚本

运行以下脚本以验证缩放因子：
```bash
/Users/eason/clawd/scripts/calibrate-cursor.sh
```

## clicclick 命令

```bash
# Click at coordinates
/opt/homebrew/bin/cliclick c:500,300

# Move mouse (no click) - Note: may not visually update cursor
/opt/homebrew/bin/cliclick m:500,300

# Double-click
/opt/homebrew/bin/cliclick dc:500,300

# Right-click
/opt/homebrew/bin/cliclick rc:500,300

# Click and drag
/opt/homebrew/bin/cliclick dd:100,100 du:200,200

# Type text
/opt/homebrew/bin/cliclick t:"hello world"

# Press key (Return, Escape, Tab, etc.)
/opt/homebrew/bin/cliclick kp:return
/opt/homebrew/bin/cliclick kp:escape

# Key with modifier (cmd+w to close window)
/opt/homebrew/bin/cliclick kd:cmd t:w ku:cmd

# Get current mouse position
/opt/homebrew/bin/cliclick p

# Wait before action (ms)
/opt/homebrew/bin/cliclick -w 100 c:500,300
```

## 截图

```bash
# Full screen (silent)
/usr/sbin/screencapture -x /tmp/screenshot.png

# With cursor (may not work for custom cursor colors)
/usr/sbin/screencapture -C -x /tmp/screenshot.png

# Interactive region selection
screencapture -i region.png

# Delayed capture
screencapture -T 3 -x delayed.png  # 3 second delay
```

## 工作流程：截图 → 分析 → 点击

**可靠点击的最佳实践**：

1. **截取屏幕截图**
   ```bash
   /usr/sbin/screencapture -x /tmp/screen.png
   ```

2. **查看截图**（使用相关工具）以找到目标坐标

3. **在相应坐标处点击**（在 1920x1080 的显示器上保持 1:1 缩放）
   ```bash
   /opt/homebrew/bin/cliclick c:X,Y
   ```

4. **通过再次截图来验证点击是否成功**

### 示例：点击按钮

```bash
# 1. Screenshot
/usr/sbin/screencapture -x /tmp/before.png

# 2. View image, find button at (850, 450)
# (Use Read tool on /tmp/before.png)

# 3. Click
/opt/homebrew/bin/cliclick c:850,450

# 4. Verify
/usr/sbin/screencapture -x /tmp/after.png
```

## 窗口边界

```bash
# Get Chrome window bounds
osascript -e 'tell application "Google Chrome" to get bounds of front window'
# Returns: 0, 38, 1920, 1080  (left, top, right, bottom)
```

## 常见操作模式

### Chrome 扩展程序图标（Browser Relay）

使用 AppleScript 来查找按钮的精确位置：
```bash
# Find Clawdbot extension button position
osascript -e '
tell application "System Events"
    tell process "Google Chrome"
        set toolbarGroup to group 2 of group 3 of toolbar 1 of group 1 of group 1 of group 1 of group 1 of group 1 of window 1
        set allButtons to every pop up button of toolbarGroup
        repeat with btn in allButtons
            if description of btn contains "Clawdbot" then
                return position of btn & size of btn
            end if
        end repeat
    end tell
end tell
'
# Output: 1755, 71, 34, 34 (x, y, width, height)

# Click center of button
# center_x = x + width/2 = 1755 + 17 = 1772
# center_y = y + height/2 = 71 + 17 = 88
/opt/homebrew/bin/cliclick c:1772,88
```

### 通过颜色检测进行点击

如果你需要找到特定颜色的元素：
```bash
# Find red (#FF0000) pixels in screenshot
magick /tmp/screen.png txt:- | grep "#FF0000" | head -5

# Calculate center of colored region
magick /tmp/screen.png txt:- | grep "#FF0000" | awk -F'[,:]' '
  BEGIN{sx=0;sy=0;c=0}
  {sx+=$1;sy+=$2;c++}
  END{printf "Center: (%d, %d)\n", sx/c, sy/c}'
```

### 点击对话框按钮

1. 截取对话框的屏幕截图
2. 直观地找到按钮的位置
3. 在 1920x1080 的显示器上点击该位置
   ```bash
# Example: Click "OK" button at (960, 540)
/opt/homebrew/bin/cliclick c:960,540
```

### 在文本字段中输入文本

```bash
# Click to focus, then type
/opt/homebrew/bin/cliclick c:500,300
sleep 0.2
/opt/homebrew/bin/cliclick t:"Hello world"
/opt/homebrew/bin/cliclick kp:return
```

## 辅助脚本

这些脚本位于 `/Users/eason/clawd/scripts/` 目录下：

- `calibrate-cursor.sh`：校准坐标缩放
- `click-at-visual.sh`：根据截图坐标进行点击
- `get-cursor-pos.sh`：获取当前光标位置
- `attach-browser-relay.sh`：自动触发 Browser Relay 扩展程序的点击功能

## 当点击失败时使用键盘导航

**Google OAuth 和受保护的页面会阻止合成鼠标点击！** 使用键盘进行导航：
```bash
# Tab to navigate between elements
osascript -e 'tell application "System Events" to keystroke tab'

# Shift+Tab to go backwards
osascript -e 'tell application "System Events" to key code 48 using shift down'

# Enter to activate focused element
osascript -e 'tell application "System Events" to keystroke return'

# Full workflow: Tab 3 times then Enter
osascript -e '
tell application "System Events"
    keystroke tab
    delay 0.15
    keystroke tab
    delay 0.15
    keystroke tab
    delay 0.15
    keystroke return
end tell
'
```

**何时使用键盘而不是鼠标**：
- Google OAuth 或登录页面（具有反自动化保护机制）
- 引起焦点捕获的弹出对话框
- 在验证后仍然无法通过鼠标点击成功的情况

## Chrome Browser Relay 与多个窗口

**问题**：Browser Relay 可能会列出多个 Chrome 窗口中的标签页，导致无法在目标标签页上执行操作。

**解决方案**：
1. 在执行自动化操作之前关闭多余的 Chrome 窗口。
2. 或确保只有目标窗口被Browser Relay 接管。

**检查被 Browser Relay 接管的标签页**：
```bash
# In agent code
browser action=tabs profile=chrome
```

如果目标标签页不在列表中 → 则说明连接的窗口错误。

**验证单个窗口**：
```bash
osascript -e 'tell application "Google Chrome" to return count of windows'
```

## 点击前的验证步骤

**至关重要**：在点击重要按钮之前，务必先验证坐标。
```bash
# 1. Take screenshot
osascript -e 'do shell script "/usr/sbin/screencapture -x /tmp/before.png"'

# 2. View screenshot (Read tool), note target position

# 3. Move mouse to verify position (optional)
python3 -c "import pyautogui; pyautogui.moveTo(X, Y)"
osascript -e 'do shell script "/usr/sbin/screencapture -C -x /tmp/verify.png"'

# 4. Check cursor is on target, THEN click
/opt/homebrew/bin/cliclick c:X,Y

# 5. Take screenshot to confirm action worked
osascript -e 'do shell script "/usr/sbin/screencapture -x /tmp/after.png"'
```

## 故障排除

**点击位置错误**：使用校准脚本验证缩放因子。

**clicclick m：无法移动光标**：此时可以使用 `c:` 命令进行点击，或者使用 `clicclick p` 命令确认位置是否发生了变化。

**权限被拒绝**：进入系统设置 → 隐私与安全 → 辅助功能 → 添加 `/opt/homebrew/bin/node` 到允许执行的程序列表中。

**找不到窗口**：检查应用程序的完整名称：
```bash
osascript -e 'tell application "System Events" to get name of every process whose background only is false'
```

**在 OAuth/受保护的页面上点击被忽略**：这些页面会阻止合成事件。此时请使用键盘导航（Tab + Enter）。

**pyautogui 与 clicclick 获取的坐标不同**：为了保持一致性，请始终使用 clicclick。pyautogui 可能会有不同的坐标映射方式。

**Quartz CGEvent 点击无效**：某些页面（如 Google OAuth 页面）也会阻止低级别的鼠标事件。在这种情况下，键盘是唯一可靠的方法。