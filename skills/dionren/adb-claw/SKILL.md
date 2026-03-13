---
name: adb-claw
version: 1.5.4
description: "在 Android 上，你可以使用这些功能：查看屏幕内容（包括截图和索引化的用户界面树结构）、进行交互（点击、滑动、滚动、输入文本、清除输入框内容）、通过深度链接进行导航（从而绕过中文/日文/韩文文本输入的限制）、通过监听用户界面状态的变化来获取更新信息（而非频繁轮询），利用辅助技术框架实时监控用户界面上的文本显示（即使在视频播放期间也能正常工作）、捕获系统音频（Android 11 及更高版本支持，输出为 WAV 格式以便传输给语音识别工具）、管理整个应用程序的生命周期（安装/卸载/清除应用）、控制屏幕显示（开关/解锁/旋转屏幕方向）、执行 shell 命令以及传输文件。该工具经过优化，支持结构化的 JSON 数据输出、精确的目标元素定位功能，并为常用应用程序提供了预先构建的深度链接和界面布局。"
homepage: https://github.com/llm-net/adb-claw
metadata:
  {
    "openclaw":
      {
        "emoji": "📱",
        "version": "1.5.4",
        "os": ["darwin", "linux"],
        "tags": ["android", "adb", "mobile", "automation", "ui-testing", "device-control", "deep-link", "screenshot", "accessibility", "monitoring"],
        "requires": { "bins": ["adb-claw", "adb"] },
        "install":
          [
            {
              "id": "adb-claw-darwin-arm64",
              "kind": "download",
              "url": "https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-darwin-arm64",
              "bins": ["adb-claw"],
              "os": "darwin",
              "label": "Download adb-claw (macOS Apple Silicon)",
            },
            {
              "id": "adb-claw-darwin-amd64",
              "kind": "download",
              "url": "https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-darwin-amd64",
              "bins": ["adb-claw"],
              "os": "darwin",
              "label": "Download adb-claw (macOS Intel)",
            },
            {
              "id": "adb-claw-linux-amd64",
              "kind": "download",
              "url": "https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-linux-amd64",
              "bins": ["adb-claw"],
              "os": "linux",
              "label": "Download adb-claw (Linux x86_64)",
            },
            {
              "id": "adb-claw-linux-arm64",
              "kind": "download",
              "url": "https://github.com/llm-net/adb-claw/releases/latest/download/adb-claw-linux-arm64",
              "bins": ["adb-claw"],
              "os": "linux",
              "label": "Download adb-claw (Linux ARM64)",
            },
            {
              "id": "adb-brew",
              "kind": "brew",
              "formula": "android-platform-tools",
              "bins": ["adb"],
              "label": "Install ADB (brew)",
            },
          ],
      },
  }
---
# ADB Claw — Android设备控制工具

ADB Claw让您能够像使用眼睛、手和耳朵一样与Android设备进行交互。您可以查看屏幕上的内容，点击任意元素，滚动页面，打开深度链接，等待UI元素的变化，捕获系统音频，管理应用程序等等——所有这些操作都通过一个命令行界面（CLI）完成，并且输出格式为结构化的JSON数据。

## 为什么选择ADB Claw

**独特功能：**
- **实时智能监控**：`monitor`命令能够实时读取Android设备的UI文本，即使在视频播放或直播过程中，`uiautomator dump`命令可能无法正常工作时也是如此。该功能可以捕获聊天信息、字幕、动态叠加层等数据，这些信息其他工具无法获取。
- **系统音频捕获**：`audio capture`命令可以通过`REMOTE_SUBMIX`接口（Android 11及以上版本）捕获设备音频，并将音频数据以WAV格式输出到标准输出（stdout），以便进一步处理（例如，传输给语音识别工具）。结合`monitor`命令，您可以同时获取视觉文本和音频信息。

**核心优势：**
- **观察 → 操作 → 验证**：`observe`命令一次调用即可返回截图和索引化的UI元素树；您可以使用元素索引精确地操作屏幕上的任何元素，无论屏幕尺寸如何。
- **深度链接支持中文/日文/韩文输入**：虽然普通的`adb input`命令无法输入中文/日文/韩文，但`adb-claw open`命令可以通过深度链接实现这些操作（例如：`adb-claw open 'app://search?keyword=中文'`）。
- **智能等待**：`wait --text "Done"`命令会等待指定的UI元素出现，避免了使用`sleep`或`observe`命令时可能出现的错误。
- **智能滚动**：该命令会根据屏幕尺寸自动计算滑动坐标，并支持指定方向、滚动次数和在特定元素内的滚动操作。
- **应用程序配置文件**：为热门应用程序（如抖音）预置了配置文件（包含深度链接、UI布局和已知问题），无需反复尝试即可快速使用。
- **完整的应用程序生命周期管理**：支持安装、启动、停止、卸载和清除应用程序数据，无需直接使用原始的`adb`命令。
- **优化的JSON输出**：所有命令的返回格式为`{ok, command, data, error, duration_ms}`，并且在出现错误时还会提供相应的建议。
- **对设备资源占用低**：几乎所有操作都通过标准的ADB命令完成；只有`monitor`和`audio capture`命令会向设备发送约7KB大小的临时辅助文件，这些文件使用完毕后会自动退出。

**持续更新中**：我们定期添加新功能，让您能够控制更多Android设备的功能。

## 开始使用

### Claude插件

安装该插件后，只需与Claude进行交互即可，无需使用任何斜杠（/）分隔的命令：

```bash
claude plugin add llm-net/adb-claw
```

插件会在首次使用时自动下载`adb-claw`二进制文件。请确保已安装`adb`工具，并通过USB连接设备且开启了USB调试功能。

然后，只需向Claude发出指令，它就会开始与您的Android设备进行交互：

```
"Take a screenshot of my phone"
"Open Douyin and search for 猫咪"
"Tap the Login button"
"Monitor the live stream chat for 30 seconds"
```

Claude会读取预设的触发词列表，并在检测到匹配的指令时自动执行相应的操作，无需您手动触发。

### OpenClaw

您也可以从ClawHub网站下载OpenClaw插件：

```bash
claw install adb-claw
```

使用相同的语法与Claude进行交互，它也会调用`adb-claw`命令来控制Android设备。

## 触发词

以下是一些常见的触发词，用于指示Claude执行特定操作：
- 用户请求控制、交互或自动化Android设备
- 用户请求测试Android应用程序或UI
- 用户请求执行点击、滑动、滚动、截图或应用程序管理操作
- 用户希望打开某个URL、深度链接或特定应用程序的界面
- 用户希望等待UI元素的出现或消失
- 用户希望调整屏幕状态（开关/解锁/旋转）
- 用户希望向Android设备上传或下载文件
- 用户希望监控直播聊天内容或在视频播放期间读取UI文本
- 用户希望捕获或录制设备音频
- 用户希望在Android设备上运行shell命令

## 二进制文件

`adb-claw`二进制文件位于`${CLAUDE_PLUGIN_ROOT}/bin/adb-claw`目录下。该文件会通过`SessionStart`钩子自动安装。如果无法找到`adb-claw`文件，请告知用户需要重新安装插件，切勿尝试自行下载或安装。

## 设置

需要两个二进制文件：
1. **adb-claw**：用于控制的命令行工具
2. **adb**：Android调试工具（来自Android SDK Platform-Tools）

### 安装adb-claw

插件会自动完成`adb-claw`的安装。如需手动安装，请参考[GitHub仓库](https://github.com/llm-net/adb-claw/releases)。

### 安装adb

```bash
# macOS
brew install android-platform-tools

# Linux (Debian/Ubuntu)
sudo apt install android-tools-adb
```

### 连接设备

确保Android设备已开启USB调试功能，并通过USB连接到计算机。

```bash
# Verify everything is working
adb-claw doctor
```

## 快速上手

基本的操作流程是：`观察 → 决定 → 操作 → 再观察`：

```bash
# 1. See what's on screen
adb-claw observe --width 540

# 2. Act on what you see (use element index from observe output)
adb-claw tap --index 3

# 3. Verify the result
adb-claw observe --width 540
```

对于支持中文/日文/韩文输入的应用程序，可以使用深度链接来绕过输入限制：

```bash
# Search in Douyin (Chinese TikTok) — no manual typing needed
adb-claw open 'snssdk1128://search/result?keyword=猫咪'

# Wait for results to load
adb-claw wait --text "综合" --timeout 5000
```

## 应用程序配置文件

应用程序配置文件为特定应用程序提供了预置的信息（如深度链接、UI布局和已知问题），可以大大减少自动化操作时的试错次数。

**可用配置文件**：位于`skills/apps/`目录下：

| 应用程序 | 配置文件 | 主要内容 |
|-----|------|-------------|
| 抖音（Douyin） | `douyin.md` | 搜索/用户界面链接、搜索/个人资料页面布局、手机与平板的差异、直播聊天监控 |
| 美团（Meituan） | `meituan.md` | 搜索/外卖链接、首页/菜单/搜索布局、WebView相关设置、弹窗处理 |

**使用方法**：
1. `adb-claw app current`：获取当前前台应用程序的包名。
2. 在`skills/apps/`目录下查找对应的配置文件。
3. 如果有配置文件，可以直接使用深度链接和预设的UI布局；如果没有，可以使用`observe`命令进行探索。
4. 通过`adb-claw device info`命令检查设备屏幕尺寸：短边小于1200px表示手机，大于或等于1200px表示平板。

配置文件为纯Markdown格式。如需支持新的应用程序，只需将对应的`.md`文件放入`skills/apps/`目录即可。

## 全局参数

| 参数 | 缩写 | 说明 | 默认值 |
|------|-------|-------------|---------|
| `--serial` | `-s` | 指定目标设备的序列号（当连接多个设备时使用） | 自动检测 |
| `--output` | `-o` | 输出格式：`json`、`text`、`quiet` | `json` |
| `--timeout` | | 命令超时时间（毫秒） | `30000` |
| `--verbose` | | 将调试信息输出到标准错误日志（stderr） | `false` |

## 命令列表

### observe — 截图 + UI元素树（主要命令）

该命令会一次性捕获屏幕截图和UI元素树。**执行任何操作前后都应使用此命令**。

```bash
adb-claw observe              # Default
adb-claw observe --width 540  # Scale screenshot width
```

返回：Base64编码的PNG截图以及带有文本、索引、边界和坐标信息的UI元素树。

### screenshot — 截取屏幕截图

```bash
adb-claw screenshot                      # Returns base64 PNG in JSON
adb-claw screenshot -f output.png        # Save to file
adb-claw screenshot --width 540          # Scale down
```

### tap — 点击UI元素

可以通过元素索引、资源ID、文本或坐标来点击UI元素：

```bash
adb-claw tap --index 5            # Tap element #5 from observe output
adb-claw tap --id "com.app:id/btn" # Tap by resource ID
adb-claw tap --text "Submit"       # Tap by visible text
adb-claw tap 540 960              # Tap coordinates (x y)
```

**建议优先使用`--index`参数**。索引值来自`observe`命令的输出结果。

### long-press — 长按

```bash
adb-claw long-press 540 960              # Default duration
adb-claw long-press 540 960 --duration 2000  # 2 seconds
```

### swipe — 滚动屏幕

```bash
adb-claw swipe 540 1800 540 600           # Swipe up (scroll down)
adb-claw swipe 540 600 540 1800           # Swipe down (scroll up)
adb-claw swipe 900 960 100 960            # Swipe left
adb-claw swipe 540 1800 540 600 --duration 500  # Slow swipe
```

### type — 输入文本（仅支持ASCII字符）

```bash
adb-claw type "Hello world"
```

**注意**：仅支持ASCII字符输入。对于中文/日文/韩文输入，请使用`open`命令和深度链接（例如：`adb-claw open 'myapp://search?keyword=中文'`）。

### key — 按下系统键

```bash
adb-claw key HOME        # Home screen
adb-claw key BACK        # Navigate back
adb-claw key ENTER       # Confirm / submit
adb-claw key TAB         # Next field
adb-claw key DEL         # Delete character
adb-claw key POWER       # Power button
adb-claw key VOLUME_UP   # Volume up
adb-claw key VOLUME_DOWN # Volume down
adb-claw key PASTE       # Paste from clipboard
adb-claw key COPY        # Copy selection
adb-claw key CUT         # Cut selection
adb-claw key WAKEUP      # Wake screen
adb-claw key SLEEP       # Sleep screen
```

### clear-field — 清空输入框

清除当前焦点所在输入框的内容。可以选择先点击元素以聚焦输入框。

```bash
adb-claw clear-field                   # Clear focused field
adb-claw clear-field --index 5         # Focus element #5 then clear
adb-claw clear-field --id "input_name" # Focus by resource ID then clear
adb-claw clear-field --text "Username" # Focus by text then clear
```

在Android SDK 31及以上版本的设备上，该命令使用Ctrl+A+DEL组合键实现清除；在旧版本设备上则使用重复的DEL键。

### open — 打开URI（深度链接）

使用Android的ACTION_VIEW意图打开任意URI。对于支持中文/日文/韩文输入的应用程序，需要将相应的文本作为URL参数传递。

```bash
adb-claw open https://www.google.com
adb-claw open myapp://path/to/screen
adb-claw open "market://details?id=com.example"
adb-claw open "snssdk1128://search/result?keyword=猫咪"   # Douyin search in Chinese
```

### scroll — 智能滚动

自动计算滑动坐标并根据屏幕尺寸进行滚动。无需手动计算坐标。

```bash
adb-claw scroll down                  # Scroll down one page
adb-claw scroll up                    # Scroll up one page
adb-claw scroll down --pages 3        # Scroll down 3 pages
adb-claw scroll down --index 5        # Scroll within element #5
adb-claw scroll left --distance 500   # Scroll left 500 pixels
```

**建议使用`scroll`命令进行页面导航，而不是手动使用`swipe`命令**。

### wait — 等待UI元素变化

等待指定的UI元素出现或消失。该命令替代了传统的`sleep`和`observe`循环，避免了不必要的等待。

```bash
adb-claw wait --text "Login"                 # Wait for text to appear
adb-claw wait --id "btn_submit"              # Wait for element by ID
adb-claw wait --text "Loading" --gone        # Wait for text to disappear
adb-claw wait --activity ".MainActivity"     # Wait for activity
adb-claw wait --text "Done" --timeout 20000  # Custom timeout (20s)
```

默认超时时间为10秒，轮询间隔为800毫秒。

### screen — 屏幕管理

```bash
adb-claw screen status               # Display on/off, locked, rotation
adb-claw screen on                   # Wake up screen
adb-claw screen off                  # Turn off screen
adb-claw screen unlock               # Wake + swipe unlock (no password)
adb-claw screen rotation auto        # Enable auto-rotation
adb-claw screen rotation 0           # Portrait
adb-claw screen rotation 1           # Landscape
```

### app — 应用程序管理

```bash
adb-claw app list         # Third-party apps
adb-claw app list --all   # Include system apps
adb-claw app current      # Current foreground app
adb-claw app launch <pkg> # Launch app by package name
adb-claw app stop <pkg>   # Force stop app
adb-claw app install <apk> [--replace]  # Install APK
adb-claw app uninstall <pkg>            # Uninstall app
adb-claw app clear <pkg>               # Clear app data/cache
```

### monitor — 持续监控UI文本

通过直接连接到Android设备的无障碍框架来监控UI文本。与`ui tree`命令不同，`monitor`命令会忽略视频相关节点，因此在直播和视频播放期间也能稳定工作。

```bash
adb-claw monitor                            # 10s bounded, returns JSON envelope
adb-claw monitor --duration 30000           # 30s bounded
adb-claw monitor --stream --duration 60000  # 60s streaming, JSON lines
adb-claw monitor --interval 1000            # Faster polling (1s)
```

- **普通模式**：按照指定的`--duration`毫秒时间持续监控，返回所有独特的文本内容。
- **流式模式`（--stream`）：实时将新出现的文本作为JSON字符串输出。

默认持续时间：10秒，轮询间隔：2秒。

注意：首次使用该命令时，系统会向设备发送一个约7KB大小的辅助文件。该文件会在监控完成后自动退出。

### audio capture — 系统音频捕获（Android 11及以上版本）

通过`REMOTE_SUBMIX`接口捕获系统音频，并将音频数据以WAV格式（16kHz单声道16位PCM）输出到标准输出。**注意**：捕获音频时设备扬声器会被静音。

```bash
adb-claw audio capture                            # Stream WAV to stdout (10s)
adb-claw audio capture --duration 30000           # Stream 30s
adb-claw audio capture --duration 0               # Stream until killed (Ctrl+C)
adb-claw audio capture --file recording.wav       # Save to file, returns JSON envelope
adb-claw audio capture --rate 44100               # Custom sample rate
```

- **流式模式**：将音频数据输出到标准输出，适用于后续处理。
- **文件模式`（--file`）：将音频数据保存到本地文件，并返回包含文件路径、文件大小和录制时间的JSON信息。

默认持续时间：10秒，采样率：16000 Hz。此模式需要Android 11及以上版本（API 30）的支持。首次使用该命令时，系统也会向设备发送一个辅助文件。

**使用建议**：
- `monitor`命令用于读取UI文本（如聊天信息、标签等结构化数据）。
- `audio capture`命令用于捕获音频内容（如语音、音乐、音效）。

**组合使用建议**：
- 在直播过程中，`monitor`用于捕获屏幕上的聊天文本，`audio capture`用于捕获声音内容。

### shell — 运行shell命令

当`adb-claw`没有对应的命令时，可以使用此命令执行任意shell命令。

```bash
adb-claw shell "ls /sdcard/"
adb-claw shell "getprop ro.build.version.release"
adb-claw shell "settings put system screen_brightness 128"
```

返回标准输出（stdout）、标准错误日志（stderr）和命令退出码。

### file — 文件传输

```bash
adb-claw file push ./local.apk /sdcard/      # Push to device
adb-claw file pull /sdcard/photo.jpg ./       # Pull from device
```

### device — 设备信息

```bash
adb-claw device list      # List connected devices
adb-claw device info      # Model, Android version, screen size, density
```

### ui — UI元素检查

```bash
adb-claw ui tree                    # Full UI element tree
adb-claw ui find --text "Settings"  # Find by text
adb-claw ui find --id "com.app:id/title"  # Find by resource ID
adb-claw ui find --index 3          # Find by index
```

## 工作流程建议

- **始终先观察**：在执行任何操作之前，先使用`observe`命令查看屏幕内容；操作完成后再次使用`observe`命令确认结果。
- **优先使用索引定位**：建议使用`--index N`参数，因为索引值在不同屏幕尺寸下保持稳定。
- **输入前先聚焦**：在输入文本之前，先点击输入框以聚焦。
- **滚动操作**：建议使用`scroll`命令进行滚动，操作完成后再次使用`observe`命令确认结果。
- **中文/日文/韩文输入**：`adb-claw type`命令仅支持ASCII字符输入。对于中文/日文/韩文输入，建议使用`adb-claw open`命令和深度链接（例如：`adb-claw open 'myapp://search?keyword=中文'`）。
- **等待页面加载**：如果需要等待页面加载完成，可以使用`wait`命令。

### 设备类型检测

使用`adb-claw device info`命令获取屏幕尺寸，从而判断设备类型：
- 短边小于1200px：手机（竖屏显示）
- 短边大于或等于1200px：平板或折叠屏（横屏显示）

不同类型的设备在滑动坐标和UI布局上可能存在差异。应用程序配置文件会记录这些差异。

### 音频捕获

- **使用前请确认**：确保设备支持音频捕获功能。
- **文件录制**：如果需要将音频录制到文件中，请使用`audio capture`命令。
- **语音转录**：如果需要将音频转录为文本，需要单独安装`asrclaw`工具。

**注意事项**：
- 捕获音频时设备扬声器会被静音。请在使用前告知用户。
- 在直播过程中，建议同时使用`monitor`和`audio capture`命令以获取完整的音频和聊天文本。

### 错误处理

如果操作失败或产生意外结果：
1. 使用`observe`命令查看当前设备状态。
2. 检查屏幕是否发生了变化（例如是否弹出了对话框或权限提示）。
3. 调整操作后重试。

## 输出格式

所有命令的返回结果均为JSON格式。

### 错误处理

```json
{
  "ok": false,
  "error": {
    "code": "DEVICE_NOT_FOUND",
    "message": "No device connected",
    "suggestion": "Connect a device via USB and enable USB debugging"
  }
}
```

## 安全性与信任性

**ADB Claw的工作原理**：它只是一个封装了标准ADB命令的命令行工具。它会将高级指令（例如`adb-claw tap --index 3`）转换为`adb shell input tap ...`这样的底层命令。

**ADB Claw不会执行以下操作**：
- 不会在设备上安装APK应用程序或持久化服务；`monitor`和`audio capture`命令仅向设备发送临时文件（约7KB），这些文件使用完毕后会自动退出。
- 不会收集或传输任何数据（如设备日志、分析信息或网络请求）。
- 不会请求用户的凭证或环境变量。
- 不会修改宿主系统的设置。

**源代码公开**：[github.com/llm-net/adb-claw](https://github.com/llm-net/adb-claw)。如果您不信任预编译的二进制文件，可以查看源代码并进行自定义编译——具体步骤请参考[README](https://github.com/llm-net/adb-claw#readme)。每次发布版本都会附带SHA256校验码以验证文件完整性。

**安全提示**：
- ADB Claw仅用于控制设备，不会安装任何软件或服务。它只会发送必要的辅助文件，并在完成后自动退出。
- 请仅连接您信任的设备，并在不需要使用ADB Claw时关闭USB调试功能。
- 请确保仅执行ADB Claw允许执行的命令（如`monitor`和`audio capture`）。切勿尝试安装其他脚本或修改宿主系统。

## 故障排除**

| 故障现象 | 解决方法 |
|---------|----------|
| 无法找到设备 | 确保设备已通过USB连接，并开启了USB调试功能。 |
| 无法找到ADB工具 | 在macOS系统上运行`brew install android-platform-tools`命令进行安装。 |
- 点击错误的目标元素 | 使用`--index`参数代替坐标；重新执行`observe`命令。 |
- `type`命令无效 | 先点击输入框以聚焦，然后输入文本（仅支持ASCII字符）。 |
- 需要输入中文/日文/韩文 | 使用`adb-claw open`命令和包含文本的深度链接。 |
- `ui dump`命令失败 | 暂停动画（点击可暂停视频），等待1秒后重试。 |
- 在搜索页面上`ui dump`命令失败 | 搜索结果可能自动播放视频预览；此时可以使用`snapshot`或`monitor`命令获取文本。 |
- 在直播过程中`ui dump`命令失败 | 使用`monitor`命令，因为它会绕过视频显示层。 |
- 命令超时 | 通过`--timeout 60000`参数延长超时时间。 |
- 出现权限提示 | 使用`observe`命令查看提示信息，然后点击“允许”或“跳过”按钮。 |
- 屏幕关闭 | 使用`adb-claw screen on`或`adb-claw screen unlock`命令重新打开屏幕。 |
- 音频捕获失败 | 确保设备支持`REMOTE_SUBMIX`接口（Android 11及以上版本）；使用`adb-claw device info`命令确认。 |
- 无法捕获音频 | 部分设备或ROM可能不支持`REMOTE_SUBMIX`接口。 |