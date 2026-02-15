---
name: airpoint
description: 通过自然语言控制 Mac：打开应用程序、点击按钮、查看屏幕内容、输入文本、管理窗口，并利用 Airpoint 的 AI 计算机使用代理来自动化多步骤任务。
metadata: {"openclaw": {"emoji": "🖐️", "homepage": "https://airpoint.app", "requires": {"bins": ["airpoint"]}, "os": ["darwin"]}}
---
# Airpoint — 适用于 macOS 的 AI 计算机辅助工具

Airpoint 提供了一个 AI 助手，可以帮助你**查看和控制 Mac**：打开应用程序、点击用户界面元素、阅读屏幕上的文本、输入内容、滚动页面、拖动元素以及管理窗口。你只需用自然语言发出指令，AI 助手便会通过感知屏幕内容（包括可访问性树、截图和视觉定位信息）、规划操作步骤、执行这些操作并验证结果来自动完成任务。

所有操作都通过 `airpoint` 命令行界面（CLI）来执行。

## 系统要求

- **macOS**（支持 Apple Silicon 或 Intel 处理器）  
- **Airpoint 应用程序**：必须已安装。请从 [airpoint.app](https://airpoint.app) 下载。  
- **Airpoint CLI**：`airpoint` 命令必须添加到系统的 `PATH` 环境变量中。你可以在 Airpoint 应用程序的“设置”→“插件”→“安装 CLI”中完成安装。

## 命令说明

### 向 AI 助手发送指令（核心命令）

这是最重要的命令。它向 Airpoint 内置的计算机辅助功能发送自然语言指令，该功能可以查看屏幕内容、移动鼠标、点击屏幕、输入文本、滚动页面、通过 Spotlight 打开应用程序以及管理窗口，并能验证自己的操作结果。

```bash
# Synchronous — waits for the agent to finish (up to 5 min) and returns output
airpoint ask "open Safari and go to github.com"
airpoint ask "what's on my screen right now?"
airpoint ask "find the Slack notification and read it"
airpoint ask "open System Settings and enable Dark Mode"
airpoint ask "open Mail, find the latest email from John, and summarize it"

# Fire-and-forget — returns immediately
airpoint ask "open Spotify and play my liked songs" --no-wait

# Hidden mode — runs without showing the assistant panel on screen
airpoint ask "take a screenshot of the current window" --hidden
```

使用 `--hidden` 选项可进行后台自动化操作，此时助手面板将不会显示在屏幕上。

### 拍摄屏幕截图

```bash
airpoint see
```

用于获取当前屏幕的截图。在发送指令前后查看屏幕状态时非常有用。

### 检查应用程序状态

```bash
airpoint status
airpoint status --json
```

显示应用程序的版本信息及其当前运行状态（例如是否处于活动状态等）。

### 手势控制（可选）

Airpoint 还支持通过摄像头进行手势控制来移动光标。以下命令可用于开启/关闭该功能：

```bash
airpoint tracking on
airpoint tracking off
airpoint tracking        # show current state
```

### 查看或修改设置

```bash
airpoint settings list             # all current settings
airpoint settings list --json      # machine-readable
airpoint settings get cursor.sensitivity
airpoint settings set cursor.sensitivity 1.5
```

常见设置包括：`cursor.sensitivity`（默认值 1.0）、`cursor.acceleration`（默认值 true）、`scroll.sensitivity`（默认值 1.0）、`scroll.inertia`（默认值 true）。

### 查看系统基本信息

```bash
airpoint vitals          # CPU, RAM, temperature
airpoint vitals --json
```

### 启动应用程序

```bash
airpoint open            # opens/focuses the Airpoint macOS app
```

## 使用建议

- **几乎所有操作都可以使用 `airpoint ask` 来完成**。AI 助手可以读取屏幕内容、与任何应用程序交互，并自动执行多步骤工作流程。
- 当需要以编程方式解析输出数据时，请务必使用 `--json` 选项。
- AI 助手可以回答关于屏幕内容的问题（例如：“当前哪个应用程序处于前台？”、“读取这个对话框中的错误信息”）。
- Airpoint 是一款经过认证并带有代码签名的 macOS 应用程序。请从 [airpoint.app](https://airpoint.app) 下载。