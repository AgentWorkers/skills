---
name: Desktop Computer Automation
description: |
  AI-powered desktop automation using Midscene. Control your desktop (macOS, Windows, Linux) with natural language commands.
  Triggers: open app, press key, desktop, computer, click on screen, type text, screenshot desktop,
  launch application, switch window, desktop automation, control computer, mouse click, keyboard shortcut,
  screen capture, find on screen, read screen, verify window, close app, minimize window, maximize window
allowed-tools:
  - Bash
---

# 桌面电脑自动化

> **重要规则 — 违反规则将导致工作流程中断：**
>
> 1. **绝对不要在任何用于执行中间场景命令的 Bash 工具调用中设置 `run_in_background: true`**。每个 `npx @midscene/computer` 命令都必须使用 `run_in_background: false`（或完全省略该参数）。在后台执行命令会导致任务结束后出现大量通知，从而破坏截图分析-执行操作的循环。
> 2. **每次 Bash 工具调用只能发送一个中间场景的 CLI 命令**。等待命令结果，读取截图，然后决定下一步操作。不要使用 `&&`、`;` 或 `sleep` 来链接多个命令。
> 3. **为每次 Bash 工具调用设置 `timeout: 60000`（60 秒）**，以确保中间场景命令有足够的时间同步完成。

使用 `npx @midscene/computer` 来控制你的桌面（macOS、Windows、Linux）。每个 CLI 命令都会直接对应到一个 MCP 工具——你（AI 代理）作为大脑，根据截图来决定要执行的操作。

## 先决条件

CLI 会自动从当前工作目录加载 `.env` 文件。在使用前，请确认 `.env` 文件存在，并且其中包含 API 密钥：

```bash
cat .env | grep MIDSCENE_MODEL_API_KEY | head -c 30
```

如果不存在 `.env` 文件或 API 密钥，请让用户创建一个。有关支持的提供者，请参阅 [模型配置](https://midscenejs.com/zh/model-common-config.html)。

**请不要运行 `echo $MIDSCENE_MODEL_API_KEY`** — 密钥是在运行时从 `.env` 文件中加载的，而不是从 shell 环境中加载的。

## 命令

### 连接桌面

```bash
npx @midscene/computer connect
npx @midscene/computer connect --displayId <id>
```

### 显示列表

```bash
npx @midscene/computer list_displays
```

### 截取截图

```bash
npx @midscene/computer take_screenshot
```

截取截图后，先读取保存的图像文件，了解当前屏幕状态，然后再决定下一步操作。

### 执行操作

使用 `actionSpace` 工具与桌面进行交互：

```bash
npx @midscene/computer Tap --locate '{"prompt":"the Safari icon in the Dock"}'
npx @midscene/computer DoubleClick --locate '{"prompt":"the Documents folder"}'
npx @midscene/computer RightClick --locate '{"prompt":"the desktop background"}'
npx @midscene/computer Input --locate '{"prompt":"the search field"}' --content 'hello world'
npx @midscene/computer Scroll --direction down
npx @midscene/computer KeyboardPress --value 'Command+Space'
npx @midscene/computer DragAndDrop --locate '{"prompt":"the file icon"}' --target '{"prompt":"the Trash icon"}'
```

### 自然语言操作

使用 `act` 命令执行多步骤操作——这对于处理短暂出现的 UI 元素非常有用（例如 Spotlight）：

```bash
npx @midscene/computer act --prompt "press Command+Space, type Safari, press Enter"
```

### 断开连接

```bash
npx @midscene/computer disconnect
```

## 工作流程模式

由于 CLI 命令在每次调用之间是无状态的，请遵循以下模式：

1. **连接** 以建立会话
2. **截取截图** 以查看当前状态
3. **分析截图** 以决定下一步操作
4. **执行操作**（点击、输入、按键等）
5. **再次截取截图** 以验证结果
6. **重复步骤 3-5，直到任务完成**
7. **完成后断开连接**

## 最佳实践

1. **频繁截取截图**：在每个操作之前和之后都截取截图，以验证状态变化。
2. **使用键盘快捷键**：`KeyboardPress --value 'Command+C'` 通常比点击 UI 元素更可靠。
3. **明确指定 UI 元素**：不要使用模糊的描述，而要提供具体、明确的细节。例如，应该说 “Safari 窗口左上角的红色关闭按钮”，而不是 “关闭按钮”。
4. **尽可能描述位置**：通过描述元素的位置来帮助定位目标元素（例如，“菜单栏右上角的图标”、“左侧边栏的第三个项目”）。
5. **切勿在后台运行**：在每次 Bash 工具调用中，要么省略 `run_in_background` 参数，要么明确将其设置为 `false`。绝对不要设置 `run_in_background: true`。

### 处理短暂出现的 UI — 必须使用 `act`

每个 CLI 命令都是作为一个 **独立的进程** 来运行的。当一个进程结束时，操作系统可能会将焦点返回到终端，这可能会导致短暂出现的 UI 元素（如应用程序启动器、上下文菜单、下拉菜单、通知弹窗等）消失。这意味着像 `KeyboardPress` → `Input` 这样的单独命令对于短暂出现的 UI 是无效的——这些 UI 元素会在命令执行期间消失。

**对于任何涉及短暂出现 UI 的交互，你必须使用 `act` 命令**。`act` 命令会在一个进程中执行所有步骤，从而保持焦点的稳定——就像 JavaScript 中的 `agent.aiAct()` 一样。

- 持久性的 UI 元素（应用程序窗口、文件管理器、任务栏/码头）可以在不同的命令之间通过截图进行交互。

**示例 — 通过启动器打开应用程序（macOS Spotlight / Windows 开始菜单 / Linux 应用程序菜单）：**

```bash
npx @midscene/computer act --prompt "open the app launcher, type Visual Studio Code, press Enter"
npx @midscene/computer take_screenshot
```

**示例 — 上下文菜单交互：**

```bash
npx @midscene/computer act --prompt "right-click the file icon, then click Delete in the context menu"
npx @midscene/computer take_screenshot
```

**示例 — 下拉菜单：**

```bash
npx @midscene/computer act --prompt "click the File menu, then click New Window"
npx @midscene/computer take_screenshot
```

## 常见模式

### 通过启动器打开应用程序

**必须使用 `act`** — 因为启动器在 CLI 进程结束后会关闭，所以单独的命令总是会失败。

```bash
# macOS
npx @midscene/computer act --prompt "press Command+Space, type Visual Studio Code, press Enter"
# Windows
npx @midscene/computer act --prompt "press the Windows key, type Visual Studio Code, press Enter"
# Linux (varies by DE)
npx @midscene/computer act --prompt "open the application menu, type Visual Studio Code, press Enter"
npx @midscene/computer take_screenshot
```

### 键盘快捷键

```bash
# macOS uses Command, Windows/Linux use Ctrl
npx @midscene/computer KeyboardPress --value 'Command+C'
npx @midscene/computer KeyboardPress --value 'Ctrl+C'
```

### 窗口管理

```bash
# macOS
npx @midscene/computer KeyboardPress --value 'Command+W'
npx @midscene/computer KeyboardPress --value 'Command+Tab'
# Windows/Linux
npx @midscene/computer KeyboardPress --value 'Alt+F4'
npx @midscene/computer KeyboardPress --value 'Alt+Tab'
```

## 故障排除

### macOS：访问权限被拒绝
你的终端应用程序没有访问权限：
1. 打开 **系统设置 > 隐私与安全 > 访问权限**
2. 添加你的终端应用程序并启用访问权限
3. 授予权限后重启终端应用程序

### macOS：找不到 Xcode 命令行工具
```bash
xcode-select --install
```

### API 密钥未设置
检查 `.env` 文件中是否包含 `MIDSCENE_MODEL_API_KEY=<your-key>`。

### AI 无法找到元素
1. 截取截图以确认该元素确实可见
2. 使用更具体的描述（包括颜色、位置、周围文本）
3. 确保该元素没有被其他窗口遮挡