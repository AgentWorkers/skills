---
name: Android Device Automation
description: >
  AI-powered Android device automation using Midscene.
  Control Android devices with natural language commands via ADB.
  Perform taps, swipes, text input, app launches, screenshots, and more.
triggers:
  - android
  - phone
  - mobile app
  - tap
  - swipe
  - install app
  - open app on phone
  - android device
  - mobile automation
  - adb
  - launch app
  - mobile screen
allowed-tools:
  - Bash
---

# Android设备自动化

> **重要规则 — 违反这些规则将导致工作流程中断：**
>
> 1. **绝对不要在任何Bash工具调用中设置`run_in_background: true`**。每个`npx @midscene/android`命令都必须使用`run_in_background: false`（或者完全省略该参数）。在后台执行会导致任务结束后出现大量通知，并破坏截图分析-执行循环。
> 2. **每次Bash工具调用只能发送一个midscene CLI命令**。等待命令结果，读取截图，然后再决定下一步操作。**不要使用`&&`、`;`或`sleep`来链接命令**。
> 3. **为每次Bash工具调用设置`timeout: 60000`（60秒）**，以确保midscene命令有足够的时间同步完成。

使用`npx @midscene/android`自动化Android设备。每个CLI命令都直接对应一个MCP工具——你（AI代理）作为“大脑”，根据截图来决定要执行的操作。

## 先决条件

CLI会自动从当前工作目录加载`.env`文件。在使用前，请确认`.env`文件存在并且包含API密钥：

```bash
cat .env | grep MIDSCENE_MODEL_API_KEY | head -c 30
```

如果不存在`.env`文件或API密钥，请让用户创建一个。有关支持的提供者，请参阅[模型配置](https://midscenejs.com/zh/model-common-config.html)。

**不要运行`echo $MIDSCENE_MODEL_API_KEY`**——密钥是在运行时从`.env`文件中加载的，而不是从shell环境中加载的。

## 命令

### 连接设备

```bash
npx @midscene/android connect
npx @midscene/android connect --deviceId emulator-5554
```

### 截取截图

```bash
npx @midscene/android take_screenshot
```

截取截图后，先读取保存的图像文件以了解当前屏幕状态，然后再决定下一步操作。

### 执行操作

使用`actionSpace`工具与设备交互。每个操作都使用`--locate`来指定目标元素：

```bash
npx @midscene/android Tap --locate '{"prompt":"the Settings icon"}'
npx @midscene/android Input --locate '{"prompt":"search field"}' --content 'hello world'
npx @midscene/android Scroll --direction down
npx @midscene/android Swipe --locate '{"prompt":"the notification panel"}' --direction down
npx @midscene/android KeyboardPress --value Enter
npx @midscene/android LongPress --locate '{"prompt":"the message bubble"}'
npx @midscene/android Launch --uri 'com.android.settings'
```

### 自然语言操作

使用`act`在一个命令中执行多步骤操作——这对于处理临时性的UI交互非常有用：

```bash
npx @midscene/android act --prompt "long press the message, then tap Delete in the popup menu"
```

### 断开连接

```bash
npx @midscene/android disconnect
```

## 工作流程模式

由于CLI命令在每次调用之间是无状态的，请遵循以下模式：

1. **连接**以建立会话
2. **截取截图**以查看当前状态
3. **分析截图**以决定下一步操作
4. **执行操作**（点击、输入、滚动等）
5. **再次截取截图**以验证结果
6. **重复步骤3-5，直到任务完成**
7. **完成操作后断开连接**

## 最佳实践

1. **频繁截取截图**：在每次操作前后都截取截图，以验证状态变化。
2. **清晰描述UI元素**：使用可见的文本标签、图标或位置描述（例如，“右上角的搜索图标”，而不是模糊的描述）。
3. **使用JSON作为`--locate`参数**：始终将`--locate`作为包含`prompt`字段的JSON字符串传递，该字段用于描述目标元素的外观。
4. **顺序执行操作**：一次执行一个操作，并在进入下一步之前验证结果。
5. **切勿在后台运行**：在每次Bash工具调用中，要么省略`run_in_background`参数，要么明确将其设置为`false`。**绝对不要设置`run_in_background: true`**。

### 处理临时性UI

弹出菜单、通知栏、底部面板和工具栏在命令执行期间会**消失**。在与临时性UI交互时：

- **使用`act`执行多步骤交互**——它会在一个进程中完成所有操作
- **或者快速连续执行命令**——不要在步骤之间截取截图
- **不要暂停进行分析**——连续执行所有与临时UI相关的命令
- 持久性UI（如应用程序屏幕、保持打开的导航抽屉）可以在不同的命令之间进行交互

**示例 — 使用`act`长按弹出菜单（推荐用于临时性UI）：**

```bash
npx @midscene/android act --prompt "long press the message bubble, then tap Delete in the popup menu"
npx @midscene/android take_screenshot
```

**示例 — 使用单独的命令长按弹出菜单（另一种方法）：**

```bash
# These commands must be run back-to-back WITHOUT screenshots in between
npx @midscene/android LongPress --locate '{"prompt":"the message bubble"}'
npx @midscene/android Tap --locate '{"prompt":"Delete option in the popup menu"}'
# NOW take a screenshot to verify the result
npx @midscene/android take_screenshot
```

## 故障排除

| 问题 | 解决方案 |
|---|---|
| **找不到ADB** | 安装Android SDK Platform Tools：在macOS上使用`brew install android-platform-tools`，或从[developer.android.com](https://developer.android.com/tools/releases/platform-tools)下载。|
| **设备未列出** | 检查USB连接，确保在开发者选项中启用了USB调试功能，然后运行`adb devices`。|
| **设备显示“未经授权”** | 解锁设备并接受USB调试授权提示。然后再次运行`adb devices`。|
| **设备显示“离线”** | 断开USB连接并重新连接USB线。运行`adb kill-server && adb start-server`。|
| **命令超时** | 设备屏幕可能已关闭或锁定。使用`adb shell input keyevent KEYCODE_WAKEUP`唤醒设备并解锁它。|
| **API密钥错误** | 确保`.env`文件中包含`MIDSCENE_MODEL_API_KEY=<your-key>`。请参阅[模型配置](https://midscenejs.com/zh/model-common-config.html)。|
| **目标设备错误** | 如果连接了多个设备，请在`connect`命令中使用`--deviceId <id>`标志。|