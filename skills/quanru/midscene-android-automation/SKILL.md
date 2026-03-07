---
name: android-device-automation
description: >
  使用 Midscene 实现基于视觉的 Android 设备自动化。完全通过截图进行操作，无需 DOM 或辅助功能标签；可以交互屏幕上所有可见的元素，无论其使用的技术栈是什么。通过 ADB（Android Debug Bridge）使用自然语言命令控制 Android 设备，支持点击、滑动、文本输入、应用程序启动、截图等操作。
  相关关键词：android、手机、移动应用、点击、滑动、安装应用、在手机上打开应用、android 设备、移动自动化、adb、启动应用、移动屏幕
  技术支持：Midscene.js（https://midscenejs.com）
allowed-tools:
  - Bash
---
# Android设备自动化

> **重要规则 — 违反这些规则将导致工作流程中断：**
>
> 1. **切勿在后台运行中间场景命令。**每个命令都必须同步执行，以便您可以在决定下一个操作之前读取其输出（特别是截图）。后台执行会打断“截图-分析-执行”的循环。
> 2. **一次只运行一个中间场景命令。**等待上一个命令完成，读取截图后，再决定下一个操作。切勿将多个命令链接在一起。
> 3. **为每个命令留出足够的时间来完成。**中间场景命令涉及AI推理和屏幕交互，这可能比典型的shell命令花费更长时间。一个典型的命令需要大约1分钟；复杂的`act`命令可能需要更长时间。
> 4. **在完成任务前必须报告结果。**完成自动化任务后，您必须主动向用户总结结果——包括找到的关键数据、完成的操作、拍摄的截图以及任何相关的发现。切勿在最后一个自动化步骤后默默地结束；用户期望在一次交互中收到完整的响应。

使用`npx @midscene/android@1`来自动化Android设备。每个CLI命令都直接对应一个MCP工具——您（AI代理）作为大脑，根据截图来决定采取哪些操作。

## 先决条件

Midscene需要具有强大视觉理解能力的模型。以下环境变量必须进行配置——可以作为系统环境变量或在当前工作目录中的`.env`文件中配置（Midscene会自动加载`.env`文件）：

```bash
MIDSCENE_MODEL_API_KEY="your-api-key"
MIDSCENE_MODEL_NAME="model-name"
MIDSCENE_MODEL_BASE_URL="https://..."
MIDSCENE_MODEL_FAMILY="family-identifier"
```

示例：Gemini (Gemini-3-Flash)

```bash
MIDSCENE_MODEL_API_KEY="your-google-api-key"
MIDSCENE_MODEL_NAME="gemini-3-flash"
MIDSCENE_MODEL_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
MIDSCENE_MODEL_FAMILY="gemini"
```

示例：Qwen 3.5

```bash
MIDSCENE_MODEL_API_KEY="your-aliyun-api-key"
MIDSCENE_MODEL_NAME="qwen3.5-plus"
MIDSCENE_MODEL_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
MIDSCENE_MODEL_FAMILY="qwen3.5"
MIDSCENE_MODEL_REASONING_ENABLED="false"
# If using OpenRouter, set:
# MIDSCENE_MODEL_API_KEY="your-openrouter-api-key"
# MIDSCENE_MODEL_NAME="qwen/qwen3.5-plus"
# MIDSCENE_MODEL_BASE_URL="https://openrouter.ai/api/v1"
```

示例：Doubao Seed 2.0 Lite

```bash
MIDSCENE_MODEL_API_KEY="your-doubao-api-key"
MIDSCENE_MODEL_NAME="doubao-seed-2-0-lite"
MIDSCENE_MODEL_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
MIDSCENE_MODEL_FAMILY="doubao-seed"
```

常用模型：Doubao Seed 2.0 Lite、Qwen 3.5、Zhipu GLM-4.6V、Gemini-3-Pro、Gemini-3-Flash。

如果模型未配置，请让用户进行设置。有关支持的提供者，请参阅[模型配置](https://midscenejs.com/model-common-config)。

## 命令

### 连接到设备

```bash
npx @midscene/android@1 connect
npx @midscene/android@1 connect --deviceId emulator-5554
```

### 拍摄截图

```bash
npx @midscene/android@1 take_screenshot
```

拍摄截图后，读取保存的图像文件以了解当前屏幕状态，然后再决定下一个操作。

### 执行操作

使用`act`与设备交互并获取结果。它内部会自动处理所有的UI交互——点击、输入、滚动、滑动、等待和导航——因此您应该以整体的形式给出复杂的、高级的任务，而不是将其分解成小步骤。用自然语言描述**您想要做什么以及期望的效果**：

```bash
# specific instructions
npx @midscene/android@1 act --prompt "type hello world in the search field and press Enter"
npx @midscene/android@1 act --prompt "long press the message bubble and tap Delete in the popup menu"

# or target-driven instructions
npx @midscene/android@1 act --prompt "open Settings and navigate to Wi-Fi settings, tell me the connected network name"
```

### 断开连接

```bash
npx @midscene/android@1 disconnect
```

## 工作流程模式

由于CLI命令在每次调用之间是无状态的，请遵循以下模式：

1. **连接**以建立会话
2. **启动目标应用程序并拍摄截图**以查看当前状态，确保应用程序已启动并在屏幕上可见。
3. **使用`act`执行所需的操作或目标驱动的指令。
4. **完成后断开连接**
5. **报告结果**——总结完成了什么，展示任务期间提取的关键发现和数据，并列出生成的文件（截图、日志等）及其路径

## 最佳实践

1. **在使用此技能之前将目标应用程序带到前台**：为了提高效率，请在使用任何中间场景命令之前，使用ADB（例如`adb shell am start -n <package/activity>`）启动应用程序。然后拍摄截图以确认应用程序确实处于前台。只有在视觉确认后，才能使用此技能进行UI自动化。ADB命令比使用midscene来导航和打开应用程序要快得多。
2. **关于UI元素要具体**：不要使用模糊的描述，而是提供清晰、具体的细节。例如，说“右侧的Wi-Fi切换开关”而不是“切换按钮”。
3. **尽可能描述位置**：通过描述元素的位置来帮助定位目标元素（例如，“右上角的搜索图标”、“列表中的第三个项目”）。
4. **切勿在后台运行**：每个中间场景命令都必须同步执行——后台执行会打断“截图-分析-执行”的循环。
5. **将相关操作批量放入一个`act`命令中**：在同一应用程序内执行连续操作时，将它们合并为一个`act`命令，而不是分成单独的命令。例如，“打开设置、点击Wi-Fi并打开它”应该是一个`act`调用，而不是三个。这样可以减少往返次数，避免不必要的截图-分析循环，并显著提高效率。
6. **完成任务后必须报告结果**：完成自动化任务后，您必须主动向用户展示结果，而无需等待用户询问。这包括：(1) 用户原始问题的答案或请求任务的结果，(2) 执行过程中提取或观察到的关键数据，(3) 截图和其他生成的文件及其路径，(4) 所采取步骤的简要总结。切勿在最后一个自动化命令后默默地结束——用户期望在一次交互中收到完整的结果。

**示例 — 弹出菜单交互：**

```bash
npx @midscene/android@1 act --prompt "long press the message bubble and tap Delete in the popup menu"
npx @midscene/android@1 take_screenshot
```

**示例 — 表单交互：**

```bash
npx @midscene/android@1 act --prompt "fill in the username field with 'testuser' and the password field with 'pass123', then tap the Login button"
npx @midscene/android@1 take_screenshot
```

## 故障排除

| 问题 | 解决方案 |
|---|---|
| **找不到ADB** | 安装Android SDK Platform Tools：`brew install android-platform-tools`（macOS）或从[developer.android.com](https://developer.android.com/tools/releases/platform-tools)下载。|
| **设备未列出** | 检查USB连接，确保在开发者选项中启用了USB调试，并运行`adb devices`。|
| **设备显示“未授权”** | 解锁设备并接受USB调试授权提示。然后再次运行`adb devices`。|
| **设备显示“离线”** | 断开USB连接并重新连接USB线。运行`adb kill-server && adb start-server`。|
| **命令超时** | 设备屏幕可能关闭或锁定。使用`adb shell input keyevent KEYCODE_WAKEUP`唤醒设备并解锁它。|
| **API密钥错误** | 检查`.env`文件中是否包含`MIDSCENE_MODEL_API_KEY=<your-key>`。请参阅[模型配置](https://midscenejs.com/zh/model-common-config.html)。|
| **目标设备错误** | 如果连接了多个设备，请在`connect`命令中使用`--deviceId <id>`标志。|