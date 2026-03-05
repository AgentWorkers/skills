---
name: macpilot-ui-inspector
description: 使用 MacPilot 的无障碍访问（accessibility）API 来检查和操作 macOS 的用户界面（UI）元素。可以通过元素的角色（role）、标签（label）或位置来查找按钮、文本字段、标签等元素，然后点击、读取或修改它们。
---
# MacPilot UI Inspector

使用 MacPilot 的无障碍功能（AX）命令来检查、查找和操作 macOS 应用程序中的 UI 元素。此功能允许对应用程序界面进行精确的编程控制。

## 使用场景

当用户需要执行以下操作时，请使用此功能：
- 在应用程序中查找特定的按钮、文本字段、复选框或 UI 元素
- 读取 UI 控件的值或状态
- 通过标签点击按钮或与控件进行交互
- 检查应用程序的完整 UI 层级结构/无障碍树
- 以编程方式设置文本字段的值或切换复选框的状态
- 查明应用程序支持的键盘快捷键
- 根据特定屏幕坐标定位元素

## 命令

### 列出 UI 元素
```bash
macpilot ui list --app "Safari" --json                    # All elements
macpilot ui list --app "Safari" --role AXButton --json    # Only buttons
macpilot ui list --app "Safari" --depth 5 --json          # Deeper scan
macpilot ui list --app "Safari" --hierarchy --json        # With hierarchy
```

### 按文本查找元素
```bash
macpilot ui find "Save" --app "TextEdit" --json           # Find by label
macpilot ui find "Save" --role AXButton --json            # Filter by role
macpilot ui find "Save" --exact --json                    # Exact match only
```

### 根据坐标查找元素
```bash
macpilot ui find-text "Submit" --app "Safari" --json
# Returns: position {x, y}, size {w, h} - use for clicking
```

### 通过标签点击 UI 元素
```bash
macpilot ui click "Save" --app "TextEdit" --json
macpilot ui click "Cancel" --role AXButton --json
```

### 获取/设置值
```bash
macpilot ui get-value "Search" --app "Safari" --json          # Read field value
macpilot ui set-value "Search" "query text" --app "Safari"    # Set field value
macpilot ui set-value "Dark Mode" "1" --role AXCheckBox       # Toggle checkbox
```

### 设置焦点
```bash
macpilot ui set-focus "Search" --app "Safari" --json    # Focus an element
```

### 在元素内部滚动
```bash
macpilot ui scroll "content" down 5 --app "Safari"     # Scroll element
```

### 检查元素属性
```bash
macpilot ui attributes "Save" --app "TextEdit" --json   # All AX attributes
```

### 根据坐标定位元素
```bash
macpilot ui elements-at 500 300 --json                  # What's at x=500 y=300
macpilot ui elements-at 500 300 --radius 50 --json      # Search wider area
```

### 无障碍树
```bash
macpilot ui tree --app "Finder" --json                  # Full AX tree
macpilot ui tree --app "Finder" --depth 3 --json        # Limit depth
```

### 键盘快捷键
```bash
macpilot ui shortcuts --app "Safari" --json             # All shortcuts
macpilot ui shortcuts --app "Safari" --menu File --json # Menu-specific
```

### 等待元素出现
```bash
macpilot wait element "Download Complete" --app "Safari" --timeout 30 --json
```

## 常见的无障碍角色（AX Roles）

| 角色 | 描述 |
|------|-------------|
| `AXButton` | 按钮（点击、切换） |
| `AXTextField` | 文本输入框 |
| `AXTextArea` | 多行文本区域 |
| `AXStaticText` | 标签和显示文本 |
| `AXCheckBox` | 复选框 |
| `AXRadioButton` | 单选按钮 |
| `AXPopUpButton` | 下拉菜单 |
| `AXComboBox` | 下拉列表 |
| `AXTable` | 表格和列表 |
| `AXRow` | 表格/列表行 |
| `AXMenuItem` | 菜单项 |
| `AXToolbar` | 工具栏 |
| `AXScrollArea` | 可滚动区域 |
| `AXWindow` | 窗口 |
| `AXSheet` | 模态窗格 |
| `AXImage` | 图像 |
| `AXLink` | 超链接 |
| `AXGroup` | 通用容器 |

## 工作流程模式

### 模式 1：查找并点击元素
```bash
# Always focus app first
macpilot app focus "Safari"
# Find the element to verify it exists
macpilot ui find "Downloads" --app "Safari" --role AXButton --json
# Click it
macpilot ui click "Downloads" --app "Safari"
```

### 模式 2：读取表单状态
```bash
macpilot app focus "System Settings"
macpilot ui get-value "Computer Name" --app "System Settings" --json
```

### 模式 3：填写表单
```bash
macpilot app focus "MyApp"
macpilot ui set-value "Name" "John Doe" --app "MyApp"
macpilot ui set-value "Email" "john@example.com" --app "MyApp"
macpilot ui click "Submit" --app "MyApp"
```

### 模式 4：探索未知的 UI 结构
```bash
# Start with a broad scan
macpilot ui tree --app "SomeApp" --depth 2 --json
# Narrow down to specific elements
macpilot ui list --app "SomeApp" --role AXButton --json
# Inspect a specific element
macpilot ui attributes "Settings" --app "SomeApp" --json
```

### 模式 5：根据坐标点击元素（备用方法）
```bash
# When label-based clicking fails, find coordinates first
macpilot ui find-text "Submit" --app "MyApp" --json
# Use returned x,y to click
macpilot click 450 320
```

## 提示

- 在进行任何 UI 操作之前，务必先调用 `macpilot app focus` 命令来设置焦点。
- 使用 `--json` 选项输出元素属性，以便更可靠地解析数据。
- 如果 `ui click` 命令失败，可以尝试使用 `ui find-text` 后接 `macpilot click x y` 来执行点击操作。
- 在进行深度扫描之前，先使用 `ui tree --depth 2` 命令了解应用程序的结构。
- 需要在系统设置中为 MacPilot.app 授予相应的权限。
- 使用 `--role` 过滤器可以显著加快在复杂应用程序中查找元素的速度。