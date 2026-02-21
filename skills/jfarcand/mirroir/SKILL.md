---
name: mirroir
description: 通过 macOS 的 iPhone 镜像功能，您可以控制真实的 iPhone：截取屏幕截图、点击屏幕、滑动屏幕、输入文本、启动应用程序、录制视频、进行光学字符识别（OCR），以及执行多步骤操作。该功能适用于屏幕上显示的任何应用程序，无需编写源代码或进行越狱操作。
homepage: https://mirroir.dev
metadata:
  {
    "openclaw":
      {
        "emoji": "📱",
        "os": ["darwin"],
        "requires": { "bins": ["iphone-mirroir-mcp"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jfarcand/tap/iphone-mirroir-mcp",
              "bins": ["iphone-mirroir-mcp"],
              "label": "Install mirroir via Homebrew",
            },
            {
              "id": "node",
              "kind": "node",
              "package": "iphone-mirroir-mcp",
              "bins": ["iphone-mirroir-mcp"],
              "label": "Install mirroir (npx)",
            },
          ],
      },
  }
---
# Mirroir — 通过 iPhone 镜像功能控制 iPhone

使用 `mirroir` 可以通过 macOS 的 iPhone 镜像功能来控制真实的 iPhone。你可以从终端执行截图、点击、滑动、输入文本、启动应用程序、录制视频、对屏幕进行光学字符识别（OCR），以及运行多步骤自动化脚本——所有这些操作都不需要修改任何源代码或对设备进行越狱处理。该功能适用于屏幕上显示的任何应用程序。

## 适用场景

✅ **适用于以下情况：**
- 用户需要与 iPhone 进行交互（点击、滑动、输入文本、导航）
- 需要在 iPhone 上发送 iMessage、WhatsApp 或其他消息应用的消息
- 需要在 iPhone 上添加日历事件、提醒或笔记
- 需要测试移动应用程序（如 Expo Go、TestFlight、App Store 应用）
- 需要截图 iPhone 屏幕
- 需要录制 iPhone 操作的视频
- 需要读取 iPhone 屏幕上的内容（通过 OCR）
- 需要自动化多步骤的操作流程（如登录流程、应用程序导航）
- 需要查看 iPhone 设置或切换网络模式
- 需要在 iPhone 上启动应用程序
- 用户提到“在我的手机上”、“在我的 iPhone 上”或“在 iOS 上”

## 不适用场景

❌ **不适用以下情况：**
- 用户需要通过 macOS 的 Messages.app 发送 iMessage — 请使用 `imsg` 功能
- 用户需要管理 Apple Reminders — 请使用 `apple-reminders` 功能
- 用户需要管理 Apple Notes — 请使用 `apple-notes` 功能
- 用户需要自动化 macOS 的用户界面操作 — 请使用 `peekaboo` 功能
- 用户需要控制摄像头 — 请使用 `camsnap` 功能
- 如果任务完全可以在 macOS 上完成，则无需使用此功能
- iPhone 镜像功能未连接（请先使用 `mirroir status` 命令检查连接状态）

## 系统要求

- macOS 15 及更高版本（Sequoia 或后续版本）
- iPhone 通过 [iPhone 镜像功能](https://support.apple.com/en-us/105071) 连接到计算机
- Karabiner-Elements（由 `mirroir` 安装程序自动安装）
- 已授予屏幕录制和辅助功能的权限

## 设置步骤

安装完成后，运行设置程序以配置辅助守护进程和 Karabiner：

```bash
# One-line install (recommended)
/bin/bash -c "$(curl -fsSL https://mirroir.dev/get-mirroir.sh)"

# Or via Homebrew
brew tap jfarcand/tap && brew install iphone-mirroir-mcp

# Or via npx
npx -y iphone-mirroir-mcp install
```

如果系统提示，需批准 Karabiner DriverKit 扩展程序：**系统设置 > 通用 > 登录项和扩展程序** — 启用 Karabiner-Elements 下的所有选项。

## MCP 服务器配置

Mirroir 是一个 MCP 服务器。你可以在 OpenClaw 的 MCP 设置中进行配置：

```json
{
  "mirroir": {
    "command": "npx",
    "args": ["-y", "iphone-mirroir-mcp"]
  }
}
```

如果通过 Homebrew 安装，可以直接使用二进制文件路径进行配置：

```json
{
  "mirroir": {
    "command": "iphone-mirroir-mcp"
  }
}
```

## 常见操作流程

执行任何 iPhone 相关操作的典型流程如下：
1. **检查状态**：`mirroir status` — 确认 iPhone 镜像功能已连接
2. **查看屏幕内容**：`mirroir describe_screen` — 对屏幕进行 OCR 处理，以获取可点击的目标位置
3. **执行操作**：根据屏幕显示的内容进行点击、滑动、输入文本或启动应用程序
4. **验证结果**：再次截图或描述屏幕内容以确认操作是否成功

## 可用工具（共 26 个）

### 屏幕操作相关工具

- `screenshot` — 将 iPhone 屏幕截图为 PNG 格式
- `describe_screen` — 对屏幕进行 OCR 处理，返回文本元素及其精确的点击坐标，并附带网格辅助线
- `get_orientation` — 获取屏幕方向（纵向/横向）和窗口尺寸
- `status` — 显示连接状态、窗口几何信息及设备准备情况
- `check_health` — 提供全面的诊断信息（包括镜像功能、辅助进程、Karabiner 以及屏幕录制状态）

### 输入操作相关工具

- `tap x y` — 在指定坐标处点击
- `double_tap x y` — 迅速点击两次（用于缩放或选择文本）
- `long_press x y` — 长按以显示上下文菜单（默认持续 500 毫秒）
- `swipe from_x from_y to_x to_y` — 在两个点之间滑动
- `drag from_x from_y to_x to_y` — 慢速拖动（用于操作图标或滑块）
- `type_text "text"` — 通过 Karabiner 虚拟键盘输入文本
- `press_key key [modifiers]` — 发送特殊按键（如回车、退出、制表、箭头键），并可添加修饰符（如 Command、Shift、Option、Control）
- `shake` — 触发摇动手势（Ctrl+Cmd+Z），用于撤销或调用菜单

### 导航操作相关工具

- `launch_app "AppName"` — 通过 Spotlight 搜索打开应用程序
- `open_url "https://..."` — 在 Safari 中打开指定 URL
- `press_home` — 返回主屏幕
- `press_app_switcher` — 打开应用程序切换器
- `spotlight` — 打开 Spotlight 搜索
- `scroll_to "label"` — 滚动屏幕直到找到可识别的文本元素
- `reset_app "AppName"` — 通过应用程序切换器强制关闭应用程序

### 录制与测量相关工具

- `start_recording` — 开始录制镜像屏幕的视频
- `stop_recording` — 停止录制并获取录制的 `.mov` 文件路径
- `measure action until [max_seconds]` — 计录屏幕切换所需的时间

### 网络与自动化相关工具

- `set_network mode` — 通过设置切换飞行模式/Wi-Fi/蜂窝网络
- `list_scenarios` — 列出可用的 YAML 自动化脚本
- `getscenario "name"` — 读取指定的自动化脚本文件

## 坐标系统

所有坐标均以镜像窗口左上角为原点。**务必先使用 `describe_screen` 获取精确的点击坐标**。网格辅助线有助于定位那些没有标签的图标（如后退箭头、齿轮图标、星星图标）。

## 示例操作

- **在 iPhone 上发送 iMessage**：```
1. launch_app "Messages"
2. describe_screen → find "New Message" button coordinates
3. tap [x] [y] on "New Message"
4. type_text "Alice"
5. describe_screen → find Alice in suggestions
6. tap [x] [y] on Alice
7. tap [x] [y] on the message field
8. type_text "Running 10 min late"
9. press_key return
10. screenshot → confirm sent
```
- **测试登录流程**：```
1. launch_app "MyApp"
2. describe_screen → find Email field
3. tap [x] [y] on Email
4. type_text "${TEST_EMAIL}"
5. tap [x] [y] on Password
6. type_text "${TEST_PASSWORD}"
7. tap [x] [y] on "Sign In"
8. describe_screen → verify "Welcome" appears
```
- **查看 Waze 的预计到达时间并通知团队**：```
1. launch_app "Waze"
2. describe_screen → read ETA to current destination (e.g. "23 min")
3. press_home
4. launch_app "Slack"
5. describe_screen → find target channel
6. tap [x] [y] on "#standup"
7. tap [x] [y] on message field
8. type_text "Heads up — Waze says 23 min out, be there by 9:25"
9. press_key return
10. screenshot → confirm sent
```
- **录制故障重现过程**：```
1. start_recording
2. launch_app "Settings"
3. scroll_to "General"
4. tap [x] [y] on "General"
5. scroll_to "About"
6. tap [x] [y] on "About"
7. stop_recording → returns path to .mov file
```

## 自动化脚本（YAML 格式）

Mirroir 支持使用 YAML 格式的自动化脚本来实现多步骤操作。脚本中描述的是操作意图，而非具体坐标；AI 会根据屏幕实际显示的内容自动执行相应的操作。

```yaml
name: Expo Go Login Flow
app: Expo Go
description: Test the login screen of an Expo Go app with valid credentials

steps:
  - launch: "Expo Go"
  - wait_for: "${APP_SCREEN:-LoginDemo}"
  - tap: "${APP_SCREEN:-LoginDemo}"
  - wait_for: "Email"
  - tap: "Email"
  - type: "${TEST_EMAIL}"
  - tap: "Password"
  - type: "${TEST_PASSWORD}"
  - tap: "Sign In"
  - assert_visible: "Welcome"
  - screenshot: "login_success"
```

脚本中的标签（`launch`、`wait_for`、`tap`、`type`、`assert_visible`、`screenshot`）代表了具体的操作指令。AI 会解析这些指令，并调用相应的 MCP 工具（`launch_app`、`describe_screen`、`tap`、`type_text`、`snapshot` 等）来执行这些操作。

你可以使用 `list_scenarios` 命令查看可用的自动化脚本，使用 `getscenario` 命令加载特定的脚本。

## 使用技巧

- 在点击之前务必先使用 `describe_screen` 确认坐标位置。
- 使用 `scroll_to "label"` 来定位屏幕外的元素，避免手动滑动。
- 输入文本后，iOS 的自动纠错功能可能会改变文本内容——请谨慎输入或关闭 iPhone 的自动纠错功能。
- 在使用 `launch_app` 之前，请使用 `reset_app` 以确保应用程序处于初始状态。
- 对于应用程序中的键盘快捷键，可以使用 `press_key` 和修饰符组合（例如 `press_key n [command]` 用于在 Mail 应用中发送新消息）。
- 使用 `describe_screen` 时设置 `skip_ocr: true` 可以仅获取带有网格辅助线的屏幕截图，便于视觉识别模型识别那些 OCR 无法识别的图标和图像。

## 常见问题解决方法

- **“未找到 iPhone 镜像”**：手动打开 iPhone 镜像应用程序，确保 iPhone 已正确配对。
- **点击操作未被识别**：检查系统设置中是否已批准 Karabiner DriverKit 扩展程序。
- **截图权限被拒绝**：确保终端具有屏幕录制的权限。
- **辅助进程未运行**：运行 `npx iphone-mirroir-mcp setup` 命令重新安装辅助守护进程。