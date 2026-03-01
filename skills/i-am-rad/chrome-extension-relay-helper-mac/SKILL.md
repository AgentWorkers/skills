---
name: OpenClaw Chrome Relay Helper - Mac
description: 将 OpenClaw Browser Relay Chrome 扩展程序附加到正在运行的标签页上，以确保浏览器工具（profile="chrome"）能够正常工作。在进行任何需要在 macOS 上使用 Chrome 扩展程序进行中继的浏览器自动化操作之前，请先使用此功能。该功能支持标签页的关闭、启动、最大化等操作，并通过 Peekaboo 可访问性机制来验证当前状态；无需使用硬编码的坐标信息，且适用于任何屏幕尺寸。
---
# OpenClaw Chrome 中继助手 - Mac

该脚本可自动将 **OpenClaw 浏览器中继** 插件附加到 macOS 上的活跃标签页中。一旦插件被成功附加，`browser(profile="chrome")` 工具即可正常使用——您可以使用真实的 Chrome 会话进行导航、截图、点击和数据抓取操作。

**仅适用于 macOS。** 需要使用 Peekaboo（macOS UI 自动化 CLI）工具。

## 快速入门

```bash
bash <skill-dir>/scripts/attach.sh
```

脚本会输出以下状态之一：
- `ALREADY_ATTACHED`：已连接完毕，无需进一步操作
- `ATTACHED`：新连接成功，可立即使用
- `FAILED: <reason>`：请查看 `~/.openclaw/media/relay-attach-fail.png` 文件以获取调试截图

随后您可以开始导航和自动化操作：
```python
browser(action="navigate", profile="chrome", targetUrl="https://example.com")
browser(action="snapshot", profile="chrome", compact=True)  # read page content
```

**典型执行时间：约 29 秒（在系统启动完成后）。**

## 先决条件

### 1. Peekaboo（macOS UI 自动化 CLI）

```bash
brew install steipete/tap/peekaboo
```

Peekaboo 通过读取 Chrome 的无障碍访问树（accessibility tree）来定位插件图标，无需使用像素坐标。

### 2. `node` 程序的访问权限设置

请进入 **系统设置 → 隐私与安全 → 无障碍访问**，并将您的 `node` 程序添加到允许执行的列表中。如果没有此权限，Peekaboo 无法发送点击事件。

您可以使用 `which node` 命令来查找 `node` 程序的安装路径。

### 3. `openclaw.json` 配置文件

请将以下配置添加到您的 `~/.openclaw/openclaw.json` 文件中：

```json
"browser": {
  "profiles": {
    "chrome": {
      "cdpUrl": "http://127.0.0.1:18792",
      "driver": "extension",
      "color": "#FF5A36"
    }
  }
}
```

编辑配置文件后，请重新启动 OpenClaw 服务器：`openclaw gateway restart`

### 4. 确保插件已加载并固定在 Chrome 工具栏中

OpenClaw 浏览器中继插件必须以解压后的形式加载到 Chrome 中。该插件随 OpenClaw 一起提供，安装路径如下：
```
~/.openclaw/browser/chrome-extension
```

通过以下步骤在 Chrome 中加载插件：
- 打开 `chrome://extensions`
- 打开 **开发者模式**
- 选择 **加载解压的扩展程序**

此外，该插件还需要被固定在 Chrome 工具栏中。脚本会通过 Chrome 的无障碍访问树来定位插件图标（仅显示固定在工具栏上的插件，而不会显示隐藏在扩展程序面板中的图标）。要固定插件，请点击工具栏上的图标，然后点击 “OpenClaw Browser Relay” 旁边的固定按钮。

## 工作原理

脚本通过 Chrome 的无障碍访问树来定位插件图标，而非依赖像素坐标。插件的图标显示文本会根据其状态发生变化：
- **未连接状态**：`"OpenClaw Browser Relay (点击以连接/断开)"
- **已连接状态**：`"OpenClaw Browser Relay: 已连接 (点击以断开)"

Peekaboo 会搜索标题中包含 “OpenClaw Browser Relay” 的弹出按钮元素，根据当前状态决定是否执行连接操作。如果 Chrome 启动缓慢，脚本会尝试最多 8 次（每次间隔 2 秒）。

在开始扫描之前，请确保将窗口最大化——因为在窗口尺寸较小时或使用默认窗口大小时，Chrome 的工具栏图标无法在无障碍访问树中显示。

## 脚本的具体步骤

1. **快速路径**：如果 Chrome 已在运行且工具栏上已显示 “已连接” 的提示，脚本会立即退出（耗时约 2 秒）。
2. 结束所有正在运行的 Chrome 实例。
3. 修改 `~/Library/Application Support/Google/Chrome/Default/Preferences` 文件，以阻止浏览器在重启时显示 “恢复页面？” 对话框。
4. 打开 `https://info.cern.ch/` 这个网站（一个仅包含 428 字节的静态 HTML 文件，不包含任何反爬虫技术、JavaScript、Cookie 或 Cloudflare 服务）。
5. 使用 Peekaboo 将窗口最大化（这是为了确保工具栏图标能够被正确显示）。
6. 扫描无障碍访问树以定位插件图标（最多尝试 8 次，每次间隔 2 秒）。
7. 点击插件图标以完成连接。
8. 在返回之前确认状态已变为 “已连接”。

## 常见问题及解决方法

| 解决方案 | 原因 |
|---|---|
| 使用硬编码的像素坐标 | 在与测量时不同的屏幕尺寸下会导致脚本失效 |
| 使用 AppleScript 的 Ctrl+Shift 组合键 | 辅助键可能不会被正确识别，只有基础按键会被触发 |
| 依赖 Chrome 插件的键盘快捷键 | 插件 manifest 文件中未定义相关命令，因此快捷键无法触发连接操作 |
| 依赖视觉识别来定位图标 | 在任何分辨率下，这种方法都无法可靠地定位工具栏图标 |
| 忽略窗口最大化操作 | 在窗口尺寸较小时，工具栏图标可能无法在无障碍访问树中显示 |
| 插件未固定在工具栏上 | 未固定的插件会隐藏在扩展程序面板中，从而无法在无障碍访问树中被识别 |
| 配置文件中的配置错误 | `browserprofile="chrome"` 要求配置文件中的配置名称和端口号完全匹配（即配置文件中必须指定 `profile="chrome"` 且端口号为 `18792`）。

## 提高脚本效率的技巧

```python
# ✅ Use snapshot for reading page content (~3k tokens)
browser(action="snapshot", profile="chrome", compact=True)

# ❌ Avoid screenshot + vision for UI element detection
# → Unreliable for toolbar/coordinate identification
# → 10–50x more expensive than snapshot
```

## 集成建议

任何需要使用 Chrome 中继功能的脚本都应该首先调用此脚本：

```bash
# 1. Attach
bash <path-to-chrome-relay>/scripts/attach.sh

# 2. Navigate
browser(action="navigate", profile="chrome", targetUrl="https://target.com")

# 3. Automate
browser(action="snapshot", profile="chrome", compact=True)
browser(action="act", profile="chrome", request={kind: "click", ref: "..."})
```