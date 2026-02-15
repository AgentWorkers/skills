---
name: windows-control
description: **完全的 Windows 桌面控制功能**：支持鼠标、键盘操作以及截图功能，您可以像人类一样与任何 Windows 应用程序进行交互。
---

# Windows 控制技能

实现 Windows 的全桌面自动化，能够像人类用户一样控制鼠标、键盘和屏幕。

## 快速入门

所有脚本都位于 `skills/windows-control/scripts/` 目录下。

### 截图
```bash
py screenshot.py > output.b64
```
返回整个屏幕的 Base64 编码 PNG 图像。

### 点击
```bash
py click.py 500 300              # Left click at (500, 300)
py click.py 500 300 right        # Right click
py click.py 500 300 left 2       # Double click
```

### 输入文本
```bash
py type_text.py "Hello World"
```
在当前光标位置输入文本（按键之间有 10 毫秒的延迟）。

### 按键
```bash
py key_press.py "enter"
py key_press.py "ctrl+s"
py key_press.py "alt+tab"
py key_press.py "ctrl+shift+esc"
```

### 移动鼠标
```bash
py mouse_move.py 500 300
```
将鼠标移动到指定坐标（动画效果平滑，耗时 0.2 秒）。

### 滚动屏幕
```bash
py scroll.py up 5      # Scroll up 5 notches
py scroll.py down 10   # Scroll down 10 notches
```

### 窗口管理（新增！）
```bash
py focus_window.py "Chrome"           # Bring window to front
py minimize_window.py "Notepad"       # Minimize window
py maximize_window.py "VS Code"       # Maximize window
py close_window.py "Calculator"       # Close window
py get_active_window.py               # Get title of active window
```

### 高级操作（新增！）
```bash
# Click by text (No coordinates needed!)
py click_text.py "Save"               # Click "Save" button anywhere
py click_text.py "Submit" "Chrome"    # Click "Submit" in Chrome only

# Drag and Drop
py drag.py 100 100 500 300            # Drag from (100,100) to (500,300)

# Robust Automation (Wait/Find)
py wait_for_text.py "Ready" "App" 30  # Wait up to 30s for text
py wait_for_window.py "Notepad" 10    # Wait for window to appear
py find_text.py "Login" "Chrome"      # Get coordinates of text
py list_windows.py                    # List all open windows
```

### 读取窗口文本
```bash
py read_window.py "Notepad"           # Read all text from Notepad
py read_window.py "Visual Studio"     # Read text from VS Code
py read_window.py "Chrome"            # Read text from browser
```
使用 Windows UI 自动化技术提取实际文本（而非使用 OCR 技术），速度更快且更准确！

### 读取 UI 元素（新增！）
```bash
py read_ui_elements.py "Chrome"               # All interactive elements
py read_ui_elements.py "Chrome" --buttons-only  # Just buttons
py read_ui_elements.py "Chrome" --links-only    # Just links
py read_ui_elements.py "Chrome" --json          # JSON output
```
返回按钮、链接、标签页、复选框、下拉菜单的坐标，以便进行点击操作。

### 读取网页内容（新增！）
```bash
py read_webpage.py                     # Read active browser
py read_webpage.py "Chrome"            # Target Chrome specifically
py read_webpage.py "Chrome" --buttons  # Include buttons
py read_webpage.py "Chrome" --links    # Include links with coords
py read_webpage.py "Chrome" --full     # All elements (inputs, images)
py read_webpage.py "Chrome" --json     # JSON output
```
增强型网页内容提取功能，可识别标题、文本、按钮和链接。

### 处理对话框（新增！）
```bash
# List all open dialogs
py handle_dialog.py list

# Read current dialog content
py handle_dialog.py read
py handle_dialog.py read --json

# Click button in dialog
py handle_dialog.py click "OK"
py handle_dialog.py click "Save"
py handle_dialog.py click "Yes"

# Type into dialog text field
py handle_dialog.py type "myfile.txt"
py handle_dialog.py type "C:\path\to\file" --field 0

# Dismiss dialog (auto-finds OK/Close/Cancel)
py handle_dialog.py dismiss

# Wait for dialog to appear
py handle_dialog.py wait --timeout 10
py handle_dialog.py wait "Save As" --timeout 5
```
处理保存/打开对话框、消息框、警告框等界面。

### 通过名称点击元素（新增！）
```bash
py click_element.py "Save"                    # Click "Save" anywhere
py click_element.py "OK" --window "Notepad"   # In specific window
py click_element.py "Submit" --type Button    # Only buttons
py click_element.py "File" --type MenuItem    # Menu items
py click_element.py --list                    # List clickable elements
py click_element.py --list --window "Chrome"  # List in specific window
```
无需坐标即可通过名称点击按钮、链接或菜单项。

### 读取屏幕区域内容（OCR - 可选）
```bash
py read_region.py 100 100 500 300     # Read text from coordinates
```
注意：需要安装 Tesseract OCR 工具。建议使用 `read_window.py` 以获得更好的效果。

## 工作流程

1. **读取窗口内容** - 从指定窗口中提取文本（快速且准确）。
2. **读取 UI 元素** - 获取带有坐标的按钮和链接信息。
3. **截图**（如需） - 查看界面布局。
4. **执行操作** - 通过名称或坐标点击元素。
5. **处理对话框** - 与弹出窗口或保存对话框进行交互。
6. **再次读取窗口内容** - 验证操作结果。

## 屏幕坐标

- 原点（0, 0）位于屏幕的左上角。
- 你的屏幕分辨率：2560x1440（可通过截图确认）。
- 坐标数据来自屏幕截图分析结果。

## 示例

### 打开记事本并输入文本
```bash
# Press Windows key
py key_press.py "win"

# Type "notepad"
py type_text.py "notepad"

# Press Enter
py key_press.py "enter"

# Wait a moment, then type
py type_text.py "Hello from AI!"

# Save
py key_press.py "ctrl+s"
```

### 在 VS Code 中点击
```bash
# Read current VS Code content
py read_window.py "Visual Studio Code"

# Click at specific location (e.g., file explorer)
py click.py 50 100

# Type filename
py type_text.py "test.js"

# Press Enter
py key_press.py "enter"

# Verify new file opened
py read_window.py "Visual Studio Code"
```

### 监控记事本中的变化
```bash
# Read current content
py read_window.py "Notepad"

# User types something...

# Read updated content (no screenshot needed!)
py read_window.py "Notepad"
```

## 文本读取方法

**方法 1：Windows UI 自动化（最佳选择）**
- 对于任何窗口，使用 `read_window.py`。
- 对于带有坐标的按钮/链接，使用 `read_ui_elements.py`。
- 对于结构化的网页内容，使用 `read_webpage.py`。
- 该方法能获取实际文本数据（而非基于图像的文本）。

**方法 2：通过名称点击元素（新增）**
- 使用 `click_element.py` 通过名称点击按钮或链接。
- 无需提供坐标，系统会自动定位元素。
- 适用于所有窗口或特定窗口。

**方法 3：处理对话框（新增）**
- 使用 `handle_dialog.py` 处理弹出窗口、保存对话框和警告框。
- 读取对话框内容，点击按钮，输入文本。
- 可使用常见的按钮（如“确定”或“取消”）自动关闭对话框。

**方法 4：截图 + 人工智能识别（备用方案）**
- 截取整个屏幕的图片。
- 通过人工智能技术识别文本。
- 效率较低，但适用于所有类型的屏幕内容。

**方法 5：OCR 技术（可选）**
- 使用 `read_region.py` 和 Tesseract 工具。
- 需要额外安装 Tesseract。
- 适用于包含文本的图片或 PDF 文件。

## 安全特性

- 设置 `pyautogui.failSAFE = True` 可在操作失败时将鼠标移动到屏幕左上角。
- 操作之间有短暂延迟，避免突然的屏幕移动。

## 系统要求

- Python 3.11 或更高版本。
- 已安装 `pyautogui` 和 `pillow` 库。

## 提示

- 建议先截图以查看当前界面状态。
- 坐标是绝对坐标（相对于屏幕的左上角）。
- 点击后稍作等待，等待 UI 更新完成。
- 尽量使用 `Ctrl+Z` 等快捷键来终止操作。

---

**状态：** ✅ 已可使用（版本 2.0 - 支持对话框和 UI 元素处理）
**创建时间：** 2026-02-01
**更新时间：** 2026-02-02