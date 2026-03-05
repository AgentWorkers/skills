---
name: macpilot-dialog-handler
description: 使用 MacPilot 处理 macOS 的文件对话框（打开、保存、打印）。在任何应用程序中，都可以通过编程方式导航文件夹、选择文件、设置文件名以及关闭对话框。
---
# MacPilot 对话框处理器

使用 MacPilot 的对话框命令与任何应用程序中出现的原生 macOS 文件对话框（打开、另存为、打印等）进行交互。可以导航到文件夹、选择文件、设置文件名，并确认或取消对话框操作。

## 使用场景

在以下情况下使用此功能：
- 当文件打开或另存为对话框出现时，需要对其进行导航；
- 需要通过原生对话框以编程方式打开或保存文件；
- 需要关闭模态对话框（如警告框、确认框）；
- 需要检查对话框中包含的元素；
- 需要自动化文件选择流程。

## 命令

### 检测对话框
```bash
macpilot dialog detect --json
# Returns: whether a modal dialog/sheet is present, its type, and owning app
```

### 检查对话框元素
```bash
macpilot dialog inspect --json
# Returns: all interactive elements (buttons, text fields, lists) in the dialog
macpilot dialog inspect --depth 20 --json   # Deeper inspection
```

### 导航到文件夹
```bash
macpilot dialog navigate "/Users/me/Documents" --json
# Opens the Go To Folder sheet (Cmd+Shift+G), sets the path, presses Return
# Waits for navigation to complete
```

### 列出对话框中的文件
```bash
macpilot dialog list-files --json
# Returns: list of files/folders visible in the current dialog location
```

### 选择文件
```bash
macpilot dialog select "myfile.txt" --json            # Select file (highlight only)
macpilot dialog select "myfile.txt" --confirm --json   # Select and confirm (Open/Save)
```

### 设置文本字段（文件名）
```bash
macpilot dialog set-field "output.pdf" --json              # Set filename in Save dialog
macpilot dialog set-field "query" --label "Search" --json  # Set specific labeled field
macpilot dialog set-field "text" --focused --json          # Set currently focused field
```

### 点击对话框按钮
```bash
macpilot dialog click-button "Save" --json
macpilot dialog click-button "Cancel" --json
macpilot dialog click-button "Open" --json
macpilot dialog click-button "Replace" --json
```

### 等待对话框完成
```bash
macpilot dialog wait-for --timeout 30 --json         # Wait for any dialog to appear
macpilot dialog wait-for --app "Safari" --json        # Wait for dialog in specific app
```

### 点击主按钮
```bash
macpilot dialog click-primary --json                 # Click default/primary button (OK, Allow, Open, etc.)
macpilot dialog click-primary --app "Finder" --json  # In specific app
```

### 关闭对话框
```bash
macpilot dialog dismiss "OK" --json           # Dismiss by clicking named button
macpilot dialog auto-dismiss --json           # Auto-dismiss with safe defaults (Cancel/OK)
```

### 触发文件打开/保存操作
```bash
macpilot dialog file-open "/path/to/file.txt" --json   # Trigger Open and navigate
macpilot dialog file-save "/path/to/output.pdf" --json  # Trigger Save As and navigate
```

## 完整工作流程

### 将文件保存到指定位置
```bash
# 1. Trigger Save dialog (Cmd+S or Cmd+Shift+S)
macpilot app focus "TextEdit"
macpilot keyboard key cmd+shift+s

# 2. Wait for dialog to appear
macpilot wait seconds 1

# 3. Navigate to target folder
macpilot dialog navigate "/Users/me/Desktop"

# 4. Set the filename
macpilot dialog set-field "report.txt"

# 5. Click Save
macpilot dialog click-button "Save"
```

### 打开特定文件
```bash
# 1. Trigger Open dialog
macpilot app focus "TextEdit"
macpilot keyboard key cmd+o

# 2. Wait for dialog
macpilot wait seconds 1

# 3. Navigate and select
macpilot dialog navigate "/Users/me/Documents"
macpilot wait seconds 1
macpilot dialog select "readme.md" --confirm
```

### 处理“替换现有文件”的确认提示
```bash
macpilot dialog click-button "Save"
macpilot wait seconds 0.5
# Check if a confirmation dialog appeared
macpilot dialog detect --json
# If yes, click Replace
macpilot dialog click-button "Replace"
```

### 检查未知类型的对话框
```bash
# First, see what dialog is present
macpilot dialog detect --json

# Then inspect all its interactive elements
macpilot dialog inspect --json

# Now you know what buttons and fields are available
```

### 一次性打开文件
```bash
# Combines triggering the open dialog, navigating, and selecting
macpilot dialog file-open "/Users/me/Documents/report.pdf"
```

## 重要规则

1. **触发对话框后请等待**：在按下 `cmd+o` 或 `cmd+s` 后，务必等待 `macpilot wait seconds 1`，确保对话框完全显示后再进行操作。
2. **先导航再选择**：文件对话框通常会打开在最近使用的目录中。请先使用 `dialog navigate` 导航到正确的文件夹。
3. **对话框具有焦点**：当对话框打开时，对应的应用程序必须处于活动状态。MacPilot 会自动扫描所有应用程序以确定当前显示的对话框。
4. **处理未知类型的对话框**：如果不确定对话框包含哪些元素，先运行 `dialog inspect --json` 以查看所有可用的按钮、字段和控件。
5. **处理级联对话框**：保存操作可能会触发“替换？”或“格式化？”等确认对话框。点击“保存”后，请务必使用 `dialog detect` 检查是否有额外的确认提示。
6. **使用 `dialog set-field` 设置字段值**：输入文件名时，建议使用 `dialog set-field` 而不是 `keyboard type`——这种方式更可靠，因为它可以直接设置 AX 值。
7. **等待后再点击主按钮**：在自动化流程中，先使用 `dialog wait-for` 确认对话框已显示，再使用 `dialog click-primary` 执行默认操作。主按钮的识别会先查找 `AXDefaultButton`，如果找不到则会尝试其他常见标签（如“确定”、“允许”、“打开”、“保存”、“继续”、“是”、“完成”等）。