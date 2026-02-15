---
description: **使用鼠标、键盘和屏幕控制实现的高级桌面自动化**

本文档介绍了如何利用鼠标、键盘和屏幕控制功能来实现更高级的桌面自动化任务。通过这些工具，您可以自动化执行一系列重复性操作，提高工作效率。以下是一些常见的自动化应用场景：

1. **文件管理**：自动复制、移动、删除文件；批量重命名文件；整理文件夹结构等。
2. **网页浏览**：自动打开网页；自动填写表单；自动下载网页内容等。
3. **应用程序操作**：自动启动或关闭应用程序；自动执行应用程序中的特定命令等。
4. **系统监控**：自动检查系统资源使用情况；自动更新软件等。
5. **游戏辅助**：自动控制游戏角色；自动执行游戏中的特定操作等。

要实现这些自动化功能，您需要掌握以下技术：

1. **脚本编写**：使用Python、JavaScript等编程语言编写自动化脚本。这些脚本可以模拟用户的操作行为，从而实现自动化任务。
2. **自动化工具**：使用现有的自动化工具，如AutoHotKey、PowerShell等。这些工具提供了丰富的功能，可以简化脚本编写过程。
3. **图形用户界面（GUI）编程**：如果您需要与特定的GUI应用程序进行交互，您可能需要学习Python的PyGUI、PyQt等库进行GUI编程。

通过学习这些技术和工具，您可以开发出更加高效、便捷的自动化脚本，从而提高您的工作效率。
---

# 桌面控制技能

**这是 OpenClaw 最先进的桌面自动化技能。** 提供精确到像素的鼠标控制、极快的键盘输入、屏幕截图、窗口管理和剪贴板操作功能。

## 🎯 主要功能

### 鼠标控制
- ✅ **绝对定位** - 移动到指定坐标
- ✅ **相对移动** - 从当前位置开始移动
- ✅ **平滑移动** - 自然、类似人类的鼠标轨迹
- ✅ **点击类型** - 左键、右键、中键、双击、三击
- ✅ **拖放** - 从点 A 拖到点 B
- ✅ **滚动** - 垂直和水平滚动
- ✅ **位置追踪** - 获取当前鼠标坐标

### 键盘控制
- ✅ **文本输入** - 快速、准确的文本输入
- ✅ **热键** - 执行键盘快捷键（如 Ctrl+C、Win+R 等）
- ✅ **特殊键** - Enter、Tab、Escape、方向键、F 键
- ✅ **按键组合** - 多键组合
- ✅ **按住并释放** - 手动控制键的状态
- ✅ **输入速度** - 可配置的每分钟单词数（从即时到类似人类的速度）

### 屏幕操作
- ✅ **截图** - 截取整个屏幕或指定区域
- ✅ **图像识别** - 通过 OpenCV 在屏幕上查找元素
- ✅ **颜色检测** - 获取指定坐标的像素颜色
- ✅ **多显示器** - 支持多个显示器

### 窗口管理
- ✅ **窗口列表** - 显示所有打开的窗口
- ✅ **激活窗口** - 将窗口置于前台
- ✅ **窗口信息** - 获取窗口的位置、大小和标题
- ✅ **最小化/最大化** - 控制窗口状态

### 安全功能
- ✅ **安全机制** - 将鼠标移动到屏幕角落以中止自动化操作
- ✅ **暂停控制** - 紧急停止机制
- ✅ **确认模式** - 执行操作前需要用户确认
- ✅ **边界检查** - 防止超出屏幕范围的操作
- ✅ **日志记录** - 记录所有自动化操作

---

## 🚀 快速入门

### 安装

首先，安装所需的依赖库：

```bash
pip install pyautogui pillow opencv-python pygetwindow
```

### 基本使用

```python
from skills.desktop_control import DesktopController

# Initialize controller
dc = DesktopController(failsafe=True)

# Mouse operations
dc.move_mouse(500, 300)  # Move to coordinates
dc.click()  # Left click at current position
dc.click(100, 200, button="right")  # Right click at position

# Keyboard operations
dc.type_text("Hello from OpenClaw!")
dc.hotkey("ctrl", "c")  # Copy
dc.press("enter")

# Screen operations
screenshot = dc.screenshot()
position = dc.get_mouse_position()
```

---

## 📋 完整 API 参考

### 鼠标函数

#### `move_mouse(x, y, duration=0, smooth=True)`
将鼠标移动到指定的屏幕坐标。

**参数：**
- `x` (int): X 坐标（从左边的像素数）
- `y` (int): Y 坐标（从顶部的像素数）
- `duration` (float): 移动时间（秒，0 = 立即，0.5 = 平滑）
- `smooth` (bool): 是否使用贝塞尔曲线进行平滑移动

**示例：**
```python
# Instant movement
dc.move_mouse(1000, 500)

# Smooth 1-second movement
dc.move_mouse(1000, 500, duration=1.0)
```

#### `move_relative(x_offset, y_offset, duration=0)`
相对于当前位置移动鼠标。

**参数：**
- `x_offset` (int): 水平移动的像素数（正数表示向右）
- `y_offset` (int): 垂直移动的像素数（正数表示向下）
- `duration` (float): 移动时间（秒）

**示例：**
```python
# Move 100px right, 50px down
dc.move_relative(100, 50, duration=0.3)
```

#### `click(x=None, y=None, button='left', clicks=1, interval=0.1)`
执行鼠标点击。

**参数：**
- `x, y` (int, 可选): 点击的坐标（None 表示当前位置）
- `button` (str): 'left', 'right', 'middle'（点击类型）
- `clicks` (int): 点击次数（1 = 单击，2 = 双击）
- `interval` (float): 多次点击之间的延迟

**示例：**
```python
# Simple left click
dc.click()

# Double-click at specific position
dc.click(500, 300, clicks=2)

# Right-click
dc.click(button='right')
```

#### `drag(start_x, start_y, end_x, end_y, duration=0.5, button='left')`
执行拖放操作。

**参数：**
- `start_x, start_y` (int): 开始坐标
- `end_x, end_y` (int): 结束坐标
- `duration` (float): 拖动持续时间
- `button` (str): 使用的鼠标按钮

**示例：**
```python
# Drag file from desktop to folder
dc.drag(100, 100, 500, 500, duration=1.0)
```

#### `scroll(clicks, direction='vertical', x=None, y=None)`
滚动鼠标滚轮。

**参数：**
- `clicks` (int): 滚动量（正数表示向上/向左，负数表示向下/向右）
- `direction` (str): 'vertical' 或 'horizontal'（滚动方向）
- `x, y` (int, 可选): 滚动的起始位置

**示例：**
```python
# Scroll down 5 clicks
dc.scroll(-5)

# Scroll up 10 clicks
dc.scroll(10)

# Horizontal scroll
dc.scroll(5, direction='horizontal')
```

#### `get_mouse_position()`
获取当前鼠标坐标。

**返回值：** `(x, y)` 元组

**示例：**
```python
x, y = dc.get_mouse_position()
print(f"Mouse is at: {x}, {y}")
```

---

### 键盘函数

#### `type_text(text, interval=0, wpm=None)`
以可配置的速度输入文本。

**参数：**
- `text` (str): 要输入的文本
- `interval` (float): 每次按键之间的延迟（0 = 立即）
- `wpm` (int, 可选): 每分钟输入的单词数（覆盖 interval）

**示例：**
```python
# Instant typing
dc.type_text("Hello World")

# Human-like typing at 60 WPM
dc.type_text("Hello World", wpm=60)

# Slow typing with 0.1s between keys
dc.type_text("Hello World", interval=0.1)
```

#### `press(key, presses=1, interval=0.1)`
按下并释放按键。

**参数：**
- `key` (str): 键名（参见键名部分）
- `presses` (int): 按键次数
- `interval` (float): 每次按键之间的延迟

**示例：**
```python
# Press Enter
dc.press('enter')

# Press Space 3 times
dc.press('space', presses=3)

# Press Down arrow
dc.press('down')
```

#### `hotkey(*keys, interval=0.05)`
执行键盘快捷键。

**参数：**
- `*keys` (str): 同时按下的键
- `interval` (float): 按键之间的延迟

**示例：**
```python
# Copy (Ctrl+C)
dc.hotkey('ctrl', 'c')

# Paste (Ctrl+V)
dc.hotkey('ctrl', 'v')

# Open Run dialog (Win+R)
dc.hotkey('win', 'r')

# Save (Ctrl+S)
dc.hotkey('ctrl', 's')

# Select All (Ctrl+A)
dc.hotkey('ctrl', 'a')
```

#### `key_down(key)` / `key_up(key)`
手动控制键的状态。

**示例：**
```python
# Hold Shift
dc.key_down('shift')
dc.type_text("hello")  # Types "HELLO"
dc.key_up('shift')

# Hold Ctrl and click (for multi-select)
dc.key_down('ctrl')
dc.click(100, 100)
dc.click(200, 100)
dc.key_up('ctrl')
```

---

### 屏幕函数

#### `screenshot(region=None, filename=None)`
捕获整个屏幕或指定区域。

**参数：**
- `region` (tuple, 可选): 要捕获的区域（左上角、宽度、高度）
- `filename` (str, 可选): 保存图像的路径

**返回值：** PIL 图像对象

**示例：**
```python
# Full screen
img = dc.screenshot()

# Save to file
dc.screenshot(filename="screenshot.png")

# Capture specific region
img = dc.screenshot(region=(100, 100, 500, 300))
```

#### `get_pixel_color(x, y)`
获取指定坐标的像素颜色。

**返回值：** RGB 元组 `(r, g, b)`

**示例：**
```python
r, g, b = dc.get_pixel_color(500, 300)
print(f"Color at (500, 300): RGB({r}, {g}, {b})")
```

#### `find_on_screen(image_path, confidence=0.8)`
在屏幕上查找图像（需要 OpenCV）。

**参数：**
- `image_path` (str): 模板图像的路径
- `confidence` (float): 匹配阈值（0-1）

**返回值：** `(x, y, width, height)` 或 None

**示例：**
```python
# Find button on screen
location = dc.find_on_screen("button.png")
if location:
    x, y, w, h = location
    # Click center of found image
    dc.click(x + w//2, y + h//2)
```

#### `get_screen_size()`
获取屏幕分辨率。

**返回值：** `(width, height)` 元组

**示例：**
```python
width, height = dc.get_screen_size()
print(f"Screen: {width}x{height}")
```

---

### 窗口函数

#### `get_all_windows()`
列出所有打开的窗口。

**返回值：** 窗口标题列表

**示例：**
```python
windows = dc.get_all_windows()
for title in windows:
    print(f"Window: {title}")
```

#### `activate_window(title_substring)`
根据窗口标题将窗口置于前台。

**参数：**
- `title_substring` (str): 要匹配的窗口标题的一部分

**示例：**
```python
# Activate Chrome
dc.activate_window("Chrome")

# Activate VS Code
dc.activate_window("Visual Studio Code")
```

#### `get_active_window()`
获取当前聚焦的窗口。

**返回值：** 窗口标题（字符串）

**示例：**
```python
active = dc.get_active_window()
print(f"Active window: {active}")
```

---

### 剪贴板函数

#### `copy_to_clipboard(text)`
将文本复制到剪贴板。

**示例：**
```python
dc.copy_to_clipboard("Hello from OpenClaw!")
```

#### `get_from_clipboard()`
从剪贴板获取文本。

**返回值：** 字符串

**示例：**
```python
text = dc.get_from_clipboard()
print(f"Clipboard: {text}")
```

---

## ⌨️ 键名参考

### 英文字母键
`'a'` 到 `'z'`

### 数字键
`'0'` 到 `'9'`

### 功能键
`'f1'` 到 `'f24'`

### 特殊键
- `'enter'` / `'return'`
- `'esc'` / `'escape'`
- `'space'` / `'spacebar'`
- `'tab'`
- `'backspace'`
- `'delete'` / `'del'`
- `'insert'`
- `'home'`
- `'end'`
- `'pageup'` / `'pgup'`
- `'pagedown'` / `'pgdn'`

### 方向键
- `'up'` / `'down'` / `'left'` / `'right'`

### 修改键
- `'ctrl'` / `'control'`
- `'shift'`
- `'alt'`
- `'win'` / `'winleft'` / `'winright'`
- `'cmd'` / `'command'`（Mac）

### 锁定键
- `'capslock'`
- `'numlock'`
- `'scrolllock'`

### 标点符号
- `'.'` / `','` / `'?'` / `'!'` / `';'` / `:'`
- `'['` / `']'` / `'{'` / `'}'`
- `'('` / `')'`
- `'+'` / `'-'` / `'*'` / `'/'` / `'='`

---

## 🛡️ 安全功能

### 安全机制

将鼠标移动到屏幕的 **任意角落** 以中止所有自动化操作。

```python
# Enable failsafe (enabled by default)
dc = DesktopController(failsafe=True)
```

### 暂停控制

```python
# Pause all automation for 2 seconds
dc.pause(2.0)

# Check if automation is safe to proceed
if dc.is_safe():
    dc.click(500, 500)
```

### 确认模式

执行操作前需要用户确认：

```python
dc = DesktopController(require_approval=True)

# This will ask for confirmation
dc.click(500, 500)  # Prompt: "Allow click at (500, 500)? [y/n]"
```

---

## 🎨 高级示例

### 示例 1：自动填写表单

```python
dc = DesktopController()

# Click name field
dc.click(300, 200)
dc.type_text("John Doe", wpm=80)

# Tab to next field
dc.press('tab')
dc.type_text("john@example.com", wpm=80)

# Tab to password
dc.press('tab')
dc.type_text("SecurePassword123", wpm=60)

# Submit form
dc.press('enter')
```

### 示例 2：截图并保存指定区域

```python
# Capture specific area
region = (100, 100, 800, 600)  # left, top, width, height
img = dc.screenshot(region=region)

# Save with timestamp
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
img.save(f"capture_{timestamp}.png")
```

### 示例 3：多文件选择

```python
# Hold Ctrl and click multiple files
dc.key_down('ctrl')
dc.click(100, 200)  # First file
dc.click(100, 250)  # Second file
dc.click(100, 300)  # Third file
dc.key_up('ctrl')

# Copy selected files
dc.hotkey('ctrl', 'c')
```

### 示例 4：窗口自动化

```python
# Activate Calculator
dc.activate_window("Calculator")
time.sleep(0.5)

# Type calculation
dc.type_text("5+3=", interval=0.2)
time.sleep(0.5)

# Take screenshot of result
dc.screenshot(filename="calculation_result.png")
```

### 示例 5：拖放文件

```python
# Drag file from source to destination
dc.drag(
    start_x=200, start_y=300,  # File location
    end_x=800, end_y=500,       # Folder location
    duration=1.0                 # Smooth 1-second drag
)
```

---

## ⚡ 性能提示

1. **使用即时移动** 以提高速度：`duration=0`
2. **批量操作** 而不是单独调用
3. **缓存屏幕位置** 以避免重新计算
4. **禁用安全机制** 以获得最佳性能（请谨慎使用）
5. **使用热键** 而不是菜单导航

---

## ⚠️ 重要说明

- **屏幕坐标** 从左上角的 (0, 0) 开始
- **多显示器设置** 中，次要显示器的坐标可能是负数
- **Windows 的 DPI 缩放** 可能会影响坐标精度
- **安全机制的角落** 为：(0,0), (width-1, 0), (0, height-1), (width-1, height-1)
- **某些应用程序** 可能会阻止模拟输入（如游戏、安全应用程序）

---

## 🔧 故障排除

### 鼠标没有移动到正确位置
- 检查 DPI 缩放设置
- 确认屏幕分辨率是否符合预期
- 使用 `get_screen_size()` 确认屏幕尺寸

### 键盘输入无效
- 确保目标应用程序具有焦点
- 有些应用程序需要管理员权限
- 尝试增加 `interval` 以提高可靠性

### 安全机制意外触发
- 增加屏幕边缘的容忍度
- 在正常使用中将鼠标移出角落
- 如有需要，可以禁用安全机制：`DesktopController(failsafe=False)`

### 权限问题
- 对于某些操作，需要以管理员权限运行 Python
- 一些安全应用程序会阻止自动化操作

---

## 📦 依赖库

- **PyAutoGUI** - 核心自动化引擎
- **Pillow** - 图像处理库
- **OpenCV**（可选） - 用于图像识别
- **PyGetWindow** - 窗口管理库

安装所有依赖库：
```bash
pip install pyautogui pillow opencv-python pygetwindow
```

---

**专为 OpenClaw 设计** - 终极的桌面自动化工具 🦞