---
description: 使用鼠标、键盘和屏幕控制实现的高级桌面自动化
---
# 桌面控制技能

**这是OpenClaw最先进的桌面自动化技能。** 提供精确到像素的鼠标控制、极快的键盘输入、屏幕截图、窗口管理和剪贴板操作功能。

## 🎯 主要功能

### 鼠标控制
- ✅ **绝对定位** - 移动到指定坐标
- ✅ **相对移动** - 从当前位置开始移动
- ✅ **平滑移动** - 自然、类似人类的鼠标轨迹
- ✅ **点击类型** - 左键、右键、中键、双击、三击
- ✅ **拖放** - 从A点拖动到B点
- ✅ **滚动** - 垂直和水平滚动
- ✅ **位置追踪** - 获取当前鼠标坐标

### 键盘控制
- ✅ **文本输入** - 快速、准确的文本输入
- ✅ **热键** - 执行键盘快捷键（如Ctrl+C、Win+R等）
- ✅ **特殊键** - Enter、Tab、Esc、箭头键、F键
- ✅ **键组合** - 多键同时按下
- ✅ **按键状态控制** - 手动控制按键状态
- ✅ **输入速度** - 可配置的每分钟输入字数（WPM，从即时到类似人类的速度）

### 屏幕操作
- ✅ **截图** - 截取整个屏幕或指定区域
- ✅ **图像识别** - 通过OpenCV在屏幕上查找元素
- ✅ **颜色检测** - 获取指定坐标的像素颜色
- ✅ **多显示器支持** - 支持多个显示器

### 窗口管理
- ✅ **窗口列表** - 显示所有打开的窗口
- ✅ **激活窗口** - 将窗口置前
- ✅ **窗口信息** - 获取窗口位置、大小和标题
- ✅ **最小化/最大化** - 控制窗口状态

### 安全功能
- ✅ **安全机制** - 将鼠标移动到屏幕角落以中止自动化操作
- ✅ **暂停控制** - 紧急停止功能
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

# 初始化控制器
dc = DesktopController(failsafe=True)

# 鼠标操作
dc.move_mouse(500, 300)  # 移动到指定坐标
dc.click()  # 在当前位置左键点击
dc.click(100, 200, button="right")  # 在指定位置右键点击

# 键盘操作
dc.type_text("Hello from OpenClaw!")  # 输入文本
dc.hotkey("ctrl", "c")  # 复制
dc.press("enter")  # 按下Enter键

# 屏幕操作
screenshot = dc.screenshot()  # 截取屏幕截图
position = dc.get_mouse_position()  # 获取鼠标位置
```

---

## 📋 完整API参考

### 鼠标函数

#### `move_mouse(x, y, duration=0, smooth=True)`  
将鼠标移动到绝对屏幕坐标。

**参数：**
- `x` (int): X坐标（从左边开始的像素值）
- `y` (int): Y坐标（从顶部开始的像素值）
- `duration` (float): 移动时间（秒，0表示立即移动，0.5表示平滑移动）
- `smooth` (bool): 是否使用贝塞尔曲线进行平滑移动

**示例：**
```python
# 立即移动
dc.move_mouse(1000, 500)

# 平滑移动1秒
dc.move_mouse(1000, 500, duration=1.0)
```

#### `move_relative(x_offset, y_offset, duration=0)`  
相对于当前位置移动鼠标。

**参数：**
- `x_offset` (int): 水平移动的像素值（正数表示向右）
- `y_offset` (int): 垂直移动的像素值（正数表示向下）
- `duration` (float): 移动时间（秒）

**示例：**
```python
# 向右移动100像素，向下移动50像素
dc.move_relative(100, 50, duration=0.3)
```

#### `click(x=None, y=None, button='left', clicks=1, interval=0.1)`  
执行鼠标点击。

**参数：**
- `x, y` (int, 可选): 点击坐标（None表示当前位置）
- `button` (str): 'left', 'right', 'middle'：点击类型
- `clicks` (int): 点击次数（1表示单击，2表示双击）
- `interval` (float): 多次点击之间的延迟

**示例：**
```python
# 简单左键点击
dc.click()

# 在指定位置双击
dc.click(500, 300, clicks=2)

# 右键点击
dc.click(button='right')
```

#### `drag(start_x, start_y, end_x, end_y, duration=0.5, button='left')`  
执行拖放操作。

**参数：**
- `start_x, start_y` (int): 开始坐标
- `end_x, end_y` (int): 结束坐标
- `duration` (float): 拖动时间
- `button` (str): 使用的鼠标按钮

**示例：**
```python
# 从桌面拖动文件到文件夹
dc.drag(100, 100, 500, 500, duration=1.0)
```

#### `scroll(clicks, direction='vertical', x=None, y=None)`  
滚动鼠标滚轮。

**参数：**
- `clicks` (int): 滚动次数（正数表示向上/向左，负数表示向下/向右）
- `direction` (str): 'vertical'或'horizontal'：滚动方向
- `x, y` (int, 可选): 滚动起始位置

**示例：**
```python
# 向下滚动5次
dc.scroll(-5)

# 向上滚动10次
dc.scroll(10)

# 水平滚动
dc.scroll(5, direction='horizontal')
```

#### `get_mouse_position()`  
获取当前鼠标坐标。

**返回值：** `(x, y)` 元组

**示例：**
```python
x, y = dc.get_mouse_position()
print(f"鼠标位置：{x}, {y}")
```

---

### 键盘函数

#### `type_text(text, interval=0, wpm=None)`  
以可配置的速度输入文本。

**参数：**
- `text` (str): 要输入的文本
- `interval` (float): 每次按键之间的延迟（秒）
- `wpm` (int, 可选): 每分钟输入的单词数（覆盖interval参数）

**示例：**
```python
# 立即输入文本
dc.type_text("Hello World")

# 以每分钟60个单词的速度输入文本
dc.type_text("Hello World", wpm=60)

# 以0.1秒的间隔输入文本
dc.type_text("Hello World", interval=0.1)
```

#### `press(key, presses=1, interval=0.1)`  
按下并释放按键。

**参数：**
- `key` (str): 键名
- `presses` (int): 按键次数
- `interval` (float): 按键之间的延迟

**示例：**
```python
# 按下Enter键
dc.press('enter')

# 按下空格键3次
dc.press('space', presses=3)

# 下箭头键
dc.press('down')
```

#### `hotkey(*keys, interval=0.05)`  
执行键盘快捷键。

**参数：**
- `*keys` (str): 同时按下的键
- `interval` (float): 按键之间的延迟

**示例：**
```python
# 复制（Ctrl+C）
dc.hotkey('ctrl', 'c')

# 粘贴（Ctrl+V）
dc.hotkey('ctrl', 'v')

# 打开“运行”对话框（Win+R）
dc.hotkey('win', 'r')

# 保存（Ctrl+S）
dc.hotkey('ctrl', 's')

# 选择全部（Ctrl+A）
dc.hotkey('ctrl', 'a')
```

#### `key_down(key)` / `key_up(key)`  
手动控制按键状态。

**示例：**
```python
# 按住Shift键
dc.key_down('shift')
dc.type_text("hello")  # 输入“HELLO”
dc.key_up('shift')

# 按住Ctrl键并点击（用于多选）
dc.key_down('ctrl')
dc.click(100, 100)
dc.click(200, 100)
dc.key_up('ctrl')
```

---

### 屏幕函数

#### `screenshot(region=None, filename=None)`  
捕获屏幕或指定区域。

**参数：**
- `region` (tuple, 可选): 要捕获的区域（左上角、宽度、高度）
- `filename` (str, 可选): 图像保存路径

**返回值：** PIL图像对象

**示例：**
```python
# 截取整个屏幕
img = dc.screenshot()

# 保存到文件
dc.screenshot(filename="screenshot.png")

# 捕获指定区域
img = dc.screenshot(region=(100, 100, 500, 300)
```

#### `get_pixel_color(x, y)`  
获取指定坐标的像素颜色。

**返回值：** RGB颜色值（元组）

**示例：**
```python
r, g, b = dc.get_pixel_color(500, 300)
print(f"坐标(500, 300)的像素颜色为：RGB({r}, {g}, {b}")
```

#### `find_on_screen(image_path, confidence=0.8)`  
在屏幕上查找指定图像（需要OpenCV库）。

**参数：**
- `image_path` (str): 模板图像的路径
- `confidence` (float): 匹配阈值（0-1）

**返回值：** 如果找到图像，则返回`(x, y, width, height)`；否则返回`None`

**示例：**
```python
# 在屏幕上查找按钮
location = dc.find_on_screen("button.png")
if location:
    x, y, w, h = location
    # 点击找到的图像中心
    dc.click(x + w//2, y + h//2)
```

#### `get_screen_size()`  
获取屏幕分辨率。

**返回值：** 屏幕宽度（width）和高度（height）的元组

**示例：**
```python
width, height = dc.get_screen_size()
print(f"屏幕分辨率：{width}x{height}")
```

---

### 窗口函数

#### `get_all_windows()`  
获取所有打开的窗口列表。

**返回值：** 窗口标题的列表

**示例：**
```python
windows = dc.get_all_windows()
for title in windows:
    print(f"窗口：{title}")
```

#### `activate_window(title_substring)`  
根据窗口标题的一部分激活窗口。

**参数：**
- `title_substring` (str): 要匹配的窗口标题的一部分

**示例：**
```python
# 激活Chrome浏览器
dc.activate_window("Chrome")

# 激活Visual Studio Code
dc.activate_window("Visual Studio Code")
```

#### `get_active_window()`  
获取当前聚焦的窗口。

**返回值：** 当前聚焦的窗口标题

**示例：**
```python
active = dc.get_active_window()
print(f"当前活动窗口：{active}")
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
print(f"剪贴板内容：{text}")
```

---

## ⌨️ 键名参考

### 字母键
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

### 箭头键
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
- `'['` / `']` / `'{'` / `'}'`
- `'('` / `')'`
- `'+'` / `'-'` / `'*'` / `'/'` / `'='`

---

## 🛡️ 安全功能

### 安全机制

将鼠标移动到屏幕的**任何角落**以中止所有自动化操作。

```python
# 启用安全机制（默认启用）
dc = DesktopController(failsafe=True)
```

### 暂停控制

```python
# 暂停所有自动化操作2秒
dc.pause(2.0)

# 检查是否可以安全地继续自动化
if dc.is_safe():
    dc.click(500, 500)
```

### 确认模式

执行操作前需要用户确认：

```python
dc = DesktopController(require_approval=True)

# 这将提示用户确认
dc.click(500, 500)  # 提示："允许在(500, 500)处点击？[y/n]"
```

---

## 🎨 高级示例

### 示例1：自动填写表单

```python
dc = DesktopController()

# 点击名称字段
dc.click(300, 200)
dc.type_text("John Doe", wpm=80)

# 切换到下一个字段
dc.press('tab')
dc.type_text("john@example.com", wpm=80)

# 切换到密码字段
dc.press('tab')
dc.type_text("SecurePassword123", wpm=60)

# 提交表单
dc.press('enter')
```

### 示例2：截图指定区域并保存

```python
# 捕获指定区域
region = (100, 100, 800, 600)  # 左上角、宽度、高度
img = dc.screenshot(region=region)

# 带时间戳保存图像
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
img.save(f"capture_{timestamp}.png")
```

### 示例3：多文件选择

```python
# 按住Ctrl键并点击多个文件
dc.key_down('ctrl')
dc.click(100, 200)  # 第一个文件
dc.click(100, 250)  # 第二个文件
dc.click(100, 300)  # 第三个文件
dc.key_up('ctrl')

# 复制选中的文件
dc.hotkey('ctrl', 'c')
```

### 示例4：窗口自动化

```python
# 激活计算器
dc.activate_window("Calculator")

# 输入计算内容
dc.type_text("5+3=", interval=0.2)

# 拍下计算结果的截图
dc.screenshot(filename="calculation_result.png")
```

### 示例5：文件拖放

```python
# 从源位置拖动文件到目标位置
dc.drag(
    start_x=200, start_y=300,  # 文件位置
    end_x=800, end_y=500,       # 目标文件夹位置
    duration=1.0                 # 平滑拖动1秒
)
```

---

## ⚡ 性能提示

1. **使用立即移动**（`duration=0`）以提高速度
2. **批量操作**而不是单独调用
3. **缓存屏幕位置**以避免重新计算
4. **关闭安全机制**以获得最佳性能（请谨慎使用）
5. **使用热键**而不是菜单导航

---

## ⚠️ 重要说明

- **屏幕坐标**以屏幕左上角的(0, 0)为原点
- **多显示器设置**可能导致次要显示器的坐标为负值
- **Windows的DPI缩放**可能会影响坐标精度
- **安全机制的角落**为：(0,0), (width-1, 0), (0, height-1), (width-1, height-1)
- **某些应用程序**可能会阻止模拟输入（如游戏、安全应用程序）

---

## 🔧 故障排除

### 鼠标未移动到正确位置
- 检查DPI缩放设置
- 确认屏幕分辨率符合预期
- 使用`get_screen_size()`确认屏幕尺寸

### 键盘输入无效
- 确保目标应用程序具有焦点
- 有些应用程序可能需要管理员权限
- 尝试增加`interval`以提高可靠性

### 安全机制意外触发
- 增加屏幕边界的容忍范围
- 在正常使用中将鼠标移出角落
- 如需关闭安全机制：`DesktopController(failsafe=False)`

### 权限问题
- 对于某些操作，需要以管理员权限运行Python
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

**专为OpenClaw设计** - 终极的桌面自动化工具 🦞