---
name: Desktop Control
description: 控制鼠标、键盘和屏幕，以执行桌面自动化任务
---
# 桌面控制技能

该技能通过 PyAutoGUI 提供了全面的桌面自动化功能，使 AI 代理能够控制鼠标、键盘、截图以及与桌面环境进行交互。

## 如何使用该技能

作为 AI 代理，您可以使用 `uvx desktop-agent` CLI 来调用桌面自动化命令。

### 命令结构

所有命令都遵循以下格式：

```bash
uvx desktop-agent <category> <command> [arguments] [options]
```

**类别：**
- `mouse` - 鼠标控制
- `keyboard` - 键盘输入
- `screen` - 截图和屏幕分析
- `message` - 用户对话框
- `app` - 应用程序控制（打开、聚焦、列出窗口）

## 可用命令

### 🖱️ 鼠标控制 (`mouse`)

控制光标的移动和点击操作。

```bash
# Move cursor to coordinates
uvx desktop-agent mouse move <x> <y> [--duration SECONDS]

# Click at current position or specific coordinates
uvx desktop-agent mouse click [x] [y] [--button left|right|middle] [--clicks N]

# Specialized clicks
uvx desktop-agent mouse double-click [x] [y]
uvx desktop-agent mouse right-click [x] [y]
uvx desktop-agent mouse middle-click [x] [y]

# Drag to coordinates
uvx desktop-agent mouse drag <x> <y> [--duration SECONDS] [--button BUTTON]

# Scroll (positive=up, negative=down)
uvx desktop-agent mouse scroll <clicks> [x] [y]

# Get current mouse position
uvx desktop-agent mouse position
```

**示例：**
```bash
# Move to center of 1920x1080 screen
uvx desktop-agent mouse move 960 540 --duration 0.5

# Right-click at specific location
uvx desktop-agent mouse right-click 500 300

# Scroll down 5 clicks
uvx desktop-agent mouse scroll -5
```

### ⌨️ 键盘控制 (`keyboard`)

输入文本并执行键盘快捷键。

```bash
# Type text
uvx desktop-agent keyboard write "<text>" [--interval SECONDS]

# Press keys
uvx desktop-agent keyboard press <key> [--presses N] [--interval SECONDS]

# Execute hotkey combination (comma-separated)
uvx desktop-agent keyboard hotkey "<key1>,<key2>,..."

# Hold/release keys
uvx desktop-agent keyboard keydown <key>
uvx desktop-agent keyboard keyup <key>
```

**示例：**
```bash
# Type text with natural delay
uvx desktop-agent keyboard write "Hello World" --interval 0.05

# Copy selected text
uvx desktop-agent keyboard hotkey "ctrl,c"

# Open Task Manager
uvx desktop-agent keyboard hotkey "ctrl,shift,esc"

# Press Enter 3 times
uvx desktop-agent keyboard press enter --presses 3
```

**常用键名：**
- 修改键：`ctrl`、`shift`、`alt`、`win`
- 特殊键：`enter`、`tab`、`esc`、`space`、`backspace`、`delete`
- 功能键：`f1` 到 `f12`
- 方向键：`up`、`down`、`left`、`right`

### 🖼️ 屏幕与截图 (`screen`)

捕获截图并分析屏幕内容。支持定位特定窗口。

```bash
# Take screenshot
uvx desktop-agent screen screenshot <filename> [--region "x,y,width,height"] [--window <title>] [--active]

# Locate image on screen or within window
uvx desktop-agent screen locate <image_path> [--confidence 0.0-1.0] [--window <title>] [--active]
uvx desktop-agent screen locate-center <image_path> [--confidence 0.0-1.0] [--window <title>] [--active]

# Locate text using OCR within window
uvx desktop-agent screen locate-text-coordinates <text> [--window <title>] [--active]
uvx desktop-agent screen read-all-text [--window <title>] [--active]

# Utility commands
uvx desktop-agent screen pixel <x> <y>
uvx desktop-agent screen size
uvx desktop-agent screen on-screen <x> <y>
```

**示例：**
```bash
# Screenshot of active window
uvx desktop-agent screen screenshot active.png --active

# Screenshot of a specific application
uvx desktop-agent screen screenshot chrome.png --window "Google Chrome"

# Locate image within Notepad
uvx desktop-agent screen locate-center button.png --window "Notepad"
```

### 💬 用户对话框 (`message`)

显示用户交互对话框。

```bash
# Show alert
uvx desktop-agent message alert "<text>" [--title TITLE] [--button BUTTON]

# Show confirmation dialog
uvx desktop-agent message confirm "<text>" [--title TITLE] [--buttons "OK,Cancel"]

# Prompt for input
uvx desktop-agent message prompt "<text>" [--title TITLE] [--default TEXT]

# Password input
uvx desktop-agent message password "<text>" [--title TITLE] [--mask CHAR]
```

**示例：**
```bash
# Simple alert
uvx desktop-agent message alert "Task completed!"

# Get user confirmation
uvx desktop-agent message confirm "Continue with operation?"

# Ask for user input
uvx desktop-agent message prompt "Enter your name:"
```

### 📱 应用程序控制 (`app`)

在 Windows、macOS 和 Linux 上控制应用程序。

```bash
# Open an application by name
uvx desktop-agent app open <name> [--arg ARGS...]

# Focus on a window by title/name
uvx desktop-agent app focus <name>

# List all visible windows
uvx desktop-agent app list
```

**示例：**
```bash
# Windows: Open Notepad
uvx desktop-agent app open notepad

# Windows: Open Chrome with a URL
uvx desktop-agent app open "chrome" --arg "https://google.com"

# macOS: Open Safari
uvx desktop-agent app open "Safari"

# Focus on a specific window
uvx desktop-agent app focus "Untitled - Notepad"

# List all open windows
uvx desktop-agent app list
```

## 常见自动化工作流程

### 工作流程 1：打开应用程序并输入内容

```bash
# Open notepad directly (cross-platform)
uvx desktop-agent app open notepad

# Wait for app to open, then focus it
uvx desktop-agent app focus notepad

# Type some text
uvx desktop-agent keyboard write "Hello from Desktop Skill!"
```

### 工作流程 2：截图 + 分析

```bash
# Get screen size first
uvx desktop-agent screen size

# Take full screenshot
uvx desktop-agent screen screenshot current_screen.png

# Check if specific UI element is visible
uvx desktop-agent screen locate save_button.png
```

### 工作流程 3：填写表单

```bash
# Click first field
uvx desktop-agent mouse click 300 200

# Fill field
uvx desktop-agent keyboard write "John Doe"

# Tab to next field
uvx desktop-agent keyboard press tab

# Fill second field
uvx desktop-agent keyboard write "john@example.com"

# Submit form (Enter)
uvx desktop-agent keyboard press enter
```

### 工作流程 4：复制/粘贴操作

```bash
# Select all text
uvx desktop-agent keyboard hotkey "ctrl,a"

# Copy
uvx desktop-agent keyboard hotkey "ctrl,c"

# Click destination
uvx desktop-agent mouse click 500 600

# Paste
uvx desktop-agent keyboard hotkey "ctrl,v"
```

## 安全注意事项

使用该技能时，AI 代理应：

1. **验证坐标**：在点击前使用 `screen size` 和 `on-screen` 确认坐标位置。
2. **添加延迟**：在命令之间插入适当的延迟，以确保 UI 可响应。
3. **验证图像**：在使用 `locate` 命令前确保图像文件存在。
4. **处理失败情况**：如果窗口位置改变或元素移动，命令可能会失败。
5. **用户安全**：对于可能具有破坏性的操作，务必通过 `message confirm` 与用户确认。

## 故障排除

### PyAutoGUI 的安全机制
PyAutoGUI 具有安全机制：将鼠标移动到屏幕角落时会中止操作。

### 图像未找到
使用 `screen locate` 时，请确保：
- 图像文件存在且路径正确。
- 调整 `--confidence` 参数（建议使用 0.7-0.9）。
- 图像与屏幕实际显示内容一致（分辨率、颜色等）。

## 获取帮助

```bash
# Show all available commands
uvx desktop-agent --help

# Show commands for specific category
uvx desktop-agent mouse --help
uvx desktop-agent keyboard --help
uvx desktop-agent screen --help
uvx desktop-agent message --help

# Show help for specific command
uvx desktop-agent mouse move --help
```

## AI 代理的集成技巧

1. **处理绝对坐标时务必先检查屏幕大小**。
2. **尽可能使用相对定位**（例如，获取当前位置并计算偏移量）。
3. **组合命令以完成复杂的工作流程**。
4. **执行前进行验证**（例如，检查屏幕上是否存在所需图像）。
5. **对重要操作提供用户反馈**。
6. **优雅地处理错误**——如果 UI 状态发生变化，命令可能会失败。

## 性能说明

- 使用 `--duration` 参数设置鼠标移动时会有动画效果，因此会花费一些时间。
- 在大屏幕上，图像定位操作可能会较慢——尽可能使用区域定位。
- 键盘命令通常执行速度很快（< 100ms）。
- 截图的质量取决于屏幕分辨率和区域大小。

## 输出格式

所有命令默认以结构化 JSON 格式输出，非常适合 AI 代理的程序化使用：

```bash
uvx desktop-agent mouse position
# Output: {"success": true, "command": "mouse.position", "timestamp": "2026-01-31T10:00:00Z", "duration_ms": 5, "data": {"position": {"x": 960, "y": 540}}}
```

### 响应格式

所有 JSON 响应都遵循以下格式：

```json
{
  "success": true,
  "command": "category.command",
  "timestamp": "2026-01-31T10:00:00Z",
  "duration_ms": 150,
  "data": { ... },
  "error": null
}
```

### 错误响应格式

```json
{
  "success": false,
  "command": "category.command",
  "timestamp": "2026-01-31T10:00:00Z",
  "duration_ms": 50,
  "data": null,
  "error": {
    "code": "image_not_found",
    "message": "Image file 'button.png' not found",
    "details": {},
    "recoverable": true
  }
}
```

### 错误代码

| 代码 | 描述 |
|------|-------------|
| `success` | 命令成功 |
| `invalid_argument` | 命令参数无效 |
| `coordinates_out_of_bounds` | 坐标超出屏幕范围 |
| `image_not_found` | 图像文件未找到或不在屏幕上 |
| `window_not_found` | 目标窗口未找到 |
| `ocr_failed` | OCR 操作失败 |
| `application_not_found` | 应用程序未找到 |
| `permission_denied` | 权限被拒绝 |
| `platform_not_supported` | 不支持该平台 |
| `timeout` | 操作超时 |
| `unknown_error` | 未知错误 |

**鼠标移动：**
```bash
uvx desktop-agent mouse move 960 540
```
```json
{"success": true, "command": "mouse.move", "timestamp": "...", "duration_ms": 150, "data": {"x": 960, "y": 540, "duration": 0}, "error": null}
```

**屏幕大小：**
```bash
uvx desktop-agent screen size
```
```json
{"success": true, "command": "screen.size", "timestamp": "...", "duration_ms": 5, "data": {"size": {"width": 1920, "height": 1080}}, "error": null}
```

**定位图像：**
```bash
uvx desktop-agent screen locate button.png
```
```json
{"success": true, "command": "screen.locate", "timestamp": "...", "duration_ms": 250, "data": {"image_found": true, "bounding_box": {"left": 100, "top": 200, "width": 50, "height": 30, "center_x": 125, "center_y": 215}}, "error": null}
```

**列出窗口：**
```bash
uvx desktop-agent app list
```
```json
{"success": true, "command": "app.list", "timestamp": "...", "duration_ms": 100, "data": {"windows": ["Untitled - Notepad", "Google Chrome", "Visual Studio Code"]}, "error": null}
```

**错误示例：**
```bash
uvx desktop-agent screen locate missing.png
```
```json
{"success": false, "command": "screen.locate", "timestamp": "...", "duration_ms": 50, "data": null, "error": {"code": "image_not_found", "message": "Image file 'missing.png' not found", "details": {}, "recoverable": true}}
```

## AI 代理的有效使用指南

本节指导 AI 代理如何高效使用该技能，包括最佳命令序列和实用技巧。

### 🎯 核心策略：先观察，再行动

在执行操作之前，务必了解当前屏幕状态。这样可以避免点击错误的坐标或在错误的窗口中输入内容。

**推荐的初始操作顺序：**
```bash
# 1. Get screen dimensions to understand your workspace
uvx desktop-agent screen size
uvx desktop-agent app list
uvx desktop-agent mouse position
```

### 根据任务推荐的命令序列

#### 打开并交互应用程序

```bash
# ✅ CORRECT: Open, wait, verify, then interact
uvx desktop-agent app open notepad              # Step 1: Open app
uvx desktop-agent app list
uvx desktop-agent app focus "Notepad"
uvx desktop-agent keyboard write "Hello World"  # Step 4: Now safe to type

# ❌ WRONG: Type immediately without verification
uvx desktop-agent app open notepad
uvx desktop-agent keyboard write "Hello World"  # May type in wrong window!
```

#### 基于图像查找并点击 UI 元素

```bash
# ✅ CORRECT: Locate first, click if found
uvx desktop-agent screen locate-center button.png --confidence 0.8
# Check if success=true and coordinates are valid
uvx desktop-agent mouse click 125 215  # Use returned coordinates

# ❌ WRONG: Click without verifying element exists
uvx desktop-agent mouse click 125 215  # Might click wrong area!
```

#### 基于文本（使用 OCR）查找并点击 UI 元素

```bash
# ✅ CORRECT: Read screen text, then locate specific text
uvx desktop-agent screen read-all-text --active
uvx desktop-agent screen locate-text-coordinates "Save" --active
# Use returned coordinates to click

# For window-specific OCR:
uvx desktop-agent screen locate-text-coordinates "OK" --window "Dialog Title"
```

#### 填写包含多个字段的表单

```bash
# ✅ CORRECT: Click each field explicitly before typing
uvx desktop-agent mouse click 300 200           # Click first field
uvx desktop-agent keyboard write "John Doe"
uvx desktop-agent mouse click 300 250           # Click second field (more reliable)
uvx desktop-agent keyboard write "john@example.com"
uvx desktop-agent mouse click 300 300           # Click third field
uvx desktop-agent keyboard write "555-1234"

# OR use Tab navigation (less reliable if field order changes)
uvx desktop-agent mouse click 300 200
uvx desktop-agent keyboard write "John Doe"
uvx desktop-agent keyboard press tab
uvx desktop-agent keyboard write "john@example.com"
uvx desktop-agent keyboard press tab
uvx desktop-agent keyboard write "555-1234"
uvx desktop-agent keyboard press enter          # Submit
```

#### 截取目标区域进行分析

```bash
# ✅ CORRECT: Screenshot specific windows for faster processing
uvx desktop-agent app list --json                           # Find exact window title
uvx desktop-agent screen screenshot app.png --window "Google Chrome"

# For active window only
uvx desktop-agent screen screenshot active.png --active

# Full screen only when necessary (slower, larger file)
uvx desktop-agent screen size
uvx desktop-agent screen screenshot full.png
```

#### 安全拖放操作

```bash
# ✅ CORRECT: Move to start, verify position, then drag
uvx desktop-agent mouse move 100 200                 # Move to source
uvx desktop-agent mouse position              # Verify position
uvx desktop-agent mouse drag 500 400 --duration 0.5  # Drag to destination

# For precision, use slower duration
uvx desktop-agent mouse drag 500 400 --duration 1.0
```

### 🔄 错误恢复策略

#### 当窗口未找到时

```bash
# Pattern: List windows, find closest match, retry
uvx desktop-agent app focus "Chrome"             # Fails with window_not_found
uvx desktop-agent app list                # See actual window titles
# Output shows: "Google Chrome - My Page"
uvx desktop-agent app focus "Google Chrome"      # Use correct title
```

#### 当图像未找到时

```bash
# Pattern: Adjust confidence or take new screenshot
uvx desktop-agent screen locate button.png --confidence 0.9
uvx desktop-agent screen locate button.png --confidence 0.7
# If still failing, capture current state for analysis
uvx desktop-agent screen screenshot current.png --active
```

#### 当点击未命中目标时

```bash
# Pattern: Verify coordinates are on screen
uvx desktop-agent screen size             # Get screen bounds
uvx desktop-agent screen on-screen 1500 900      # Check if coords are valid
uvx desktop-agent mouse move 1500 900            # Move first to visualize
uvx desktop-agent mouse click                    # Then click at current position
```

### ⚡ 性能优化

#### 减少截图次数

```bash
# ✅ GOOD: Screenshot only the region you need
uvx desktop-agent screen screenshot button_area.png --region "100,200,200,100"

# ✅ GOOD: Screenshot specific window instead of full screen  
uvx desktop-agent screen screenshot chrome.png --window "Google Chrome"

# ❌ SLOW: Full screen capture when you only need a small area
uvx desktop-agent screen screenshot full.png
```

#### 批量输入键盘内容

```bash
# ✅ FASTER: Write entire text at once
uvx desktop-agent keyboard write "This is a complete sentence with all the text."

# ❌ SLOWER: Multiple write commands
uvx desktop-agent keyboard write "This is "
uvx desktop-agent keyboard write "a complete "
uvx desktop-agent keyboard write "sentence."
```

#### 尽可能使用快捷键代替鼠标操作

```bash
# ✅ FASTER: Use keyboard shortcuts
uvx desktop-agent keyboard hotkey "ctrl,s"       # Save
uvx desktop-agent keyboard hotkey "ctrl,a"       # Select all
uvx desktop-agent keyboard hotkey "ctrl,shift,s" # Save as

# ❌ SLOWER: Navigate menu with mouse
uvx desktop-agent mouse click 50 30              # Click File menu
uvx desktop-agent mouse click 60 80              # Click Save option
```

### 🛡️ 防御性编程技巧

#### 对关键操作始终进行验证

```bash
# Before destructive action, confirm with user
uvx desktop-agent message confirm "This will delete all files. Continue?" --title "Warning"
# Check output: if "Cancel" was clicked, abort operation
```

#### 使用 JSON 格式进行可靠的数据解析

```bash
# ✅ RELIABLE: Parse structured JSON output
uvx desktop-agent screen locate button.png
# Parse: {"success": true, "data": {"center_x": 125, "center_y": 215}}

# ❌ FRAGILE: Parse text output
uvx desktop-agent screen locate button.png
# Parse: "Found at: Box(left=100, top=200, width=50, height=30)"
```

#### 在执行多步操作前进行验证

```bash
# Multi-step file operation with validation
uvx desktop-agent app list
uvx desktop-agent screen locate-text-coordinates "File" --active
uvx desktop-agent mouse click <returned_x> <returned_y>
uvx desktop-agent screen locate-text-coordinates "Save As" --active
uvx desktop-agent mouse click <returned_x> <returned_y>
```

### 🎮 平台特定注意事项

#### Windows

```bash
# Common Windows shortcuts
uvx desktop-agent keyboard hotkey "win,d"        # Show desktop
uvx desktop-agent keyboard hotkey "win,e"        # Open Explorer
uvx desktop-agent keyboard hotkey "alt,tab"      # Switch windows
uvx desktop-agent keyboard hotkey "win,r"        # Run dialog

# Open apps by name
uvx desktop-agent app open notepad
uvx desktop-agent app open calc
uvx desktop-agent app open mspaint
```

#### macOS

```bash
# Common macOS shortcuts (use 'command' for Cmd key)
uvx desktop-agent keyboard hotkey "command,space"   # Spotlight
uvx desktop-agent keyboard hotkey "command,tab"     # App switcher
uvx desktop-agent keyboard hotkey "command,q"       # Quit app
uvx desktop-agent keyboard hotkey "command,shift,3" # Screenshot

# Open apps
uvx desktop-agent app open "Safari"
uvx desktop-agent app open "TextEdit"
```

#### Linux

```bash
# Open apps (uses xdg-open or direct command)
uvx desktop-agent app open firefox
uvx desktop-agent app open gedit

# Common shortcuts may vary by DE
uvx desktop-agent keyboard hotkey "alt,f2"       # Run dialog (many DEs)
```

### 📊 决策树：选择正确的命令

```
 Want to interact with an app?
├── App not running → `app open <name>`
├── App running but not focused → `app focus <name>` 
└── Need to verify windows → `app list`

Want to find a UI element?
├── Have reference image → `screen locate-center <image>`
├── Know the text label → `screen locate-text-coordinates "<text>"`
└── Need to see all text → `screen read-all-text --active`

Want to click something?
├── Know exact coordinates → `mouse click <x> <y>`
├── Need to find first → Use locate commands above, then click returned coords
└── Not sure if on screen → `screen on-screen <x> <y>` first

Want to type something?
├── Regular text → `keyboard write "<text>"`
├── Keyboard shortcut → `keyboard hotkey "<key1>,<key2>"`
├── Single key press → `keyboard press <key>`
└── Multiple of same key → `keyboard press <key> --presses N`
```

## AI 代理的集成技巧

1. **处理绝对坐标时务必先检查屏幕大小**。
2. **尽可能使用相对定位**（例如，获取当前位置并计算偏移量）。
3. **组合命令以完成复杂的工作流程**。
4. **执行前进行验证**（例如，检查屏幕上是否存在所需图像）。
5. **对重要操作提供用户反馈**。
6. **优雅地处理错误**——如果 UI 状态发生变化，命令可能会失败。