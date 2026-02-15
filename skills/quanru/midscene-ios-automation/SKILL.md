---
name: iOS Device Automation
description: |
  Vision-driven iOS device automation using Midscene CLI. Operates entirely from screenshots — no DOM or accessibility labels required. Can interact with all visible elements on screen regardless of technology stack.
  Control iOS devices with natural language commands via WebDriverAgent.
  
  Triggers: ios, iphone, ipad, ios app, tap on iphone, swipe, mobile app ios,
  ios device, ios testing, iphone automation, ipad automation, ios screen, ios navigate

  Powered by Midscene.js (https://midscenejs.com)
allowed-tools:
  - Bash
---

# iOS 设备自动化

> **重要规则 — 违反这些规则将导致工作流程中断：**
>
> 1. **切勿在后台运行中间场景命令。**每个命令必须同步执行，以便您可以在决定下一步操作之前读取其输出（特别是截图）。后台执行会打断“截图 → 分析 → 执行”的循环。
> 2. **每次仅运行一个中间场景命令。**等待上一个命令完成，读取截图后，再决定下一步操作。切勿将多个命令连续执行。
> 3. **为每个命令留出足够的时间来完成。**中间场景命令涉及 AI 推理和屏幕交互，这可能比普通的 shell 命令花费更长时间。一个普通的命令大约需要 1 分钟；复杂的 `act` 命令可能需要更长时间。

使用 `npx @midscene/ios@1` 来自动化 iOS 设备。每个 CLI 命令都直接对应一个 MCP 工具——您（AI 代理）作为“大脑”，根据截图来决定要执行的操作。

## 先决条件

Midscene 需要具有强大视觉理解能力的模型。以下环境变量必须进行配置——可以在系统环境变量中设置，或者在当前工作目录下的 `.env` 文件中设置（Midscene 会自动加载 `.env` 文件）：

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

示例：Qwen3-VL

```bash
MIDSCENE_MODEL_API_KEY="your-openrouter-api-key"
MIDSCENE_MODEL_NAME="qwen/qwen3-vl-235b-a22b-instruct"
MIDSCENE_MODEL_BASE_URL="https://openrouter.ai/api/v1"
MIDSCENE_MODEL_FAMILY="qwen3-vl"
```

示例：Doubao Seed 1.6

```bash
MIDSCENE_MODEL_API_KEY="your-doubao-api-key"
MIDSCENE_MODEL_NAME="doubao-seed-1-6-250615"
MIDSCENE_MODEL_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
MIDSCENE_MODEL_FAMILY="doubao-vision"
```

常用模型：Doubao Seed 1.6、Qwen3-VL、Zhipu GLM-4.6V、Gemini-3-Pro、Gemini-3-Flash。

如果模型未配置，请让用户进行设置。有关支持的模型，请参阅 [模型配置](https://midscenejs.com/model-common-config)。

## 命令

### 连接到设备

```bash
npx @midscene/ios@1 connect
```

### 截取屏幕截图

```bash
npx @midscene/ios@1 take_screenshot
```

截取屏幕截图后，读取保存的图像文件以了解当前屏幕状态，然后再决定下一步操作。

### 执行操作

使用 `act` 与设备交互并获取结果。它内部会自动处理所有的 UI 交互——点击、输入、滚动、滑动、等待和导航——因此您应该以整体的方式给出复杂的、高级的任务，而不是将其分解成小步骤。用自然语言描述**您想要做什么以及期望的效果**：

```bash
# specific instructions
npx @midscene/ios@1 act --prompt "type hello world in the search field and press Enter"
npx @midscene/ios@1 act --prompt "tap Delete, then confirm in the alert dialog"

# or target-driven instructions
npx @midscene/ios@1 act --prompt "open Settings and navigate to Wi-Fi, tell me the connected network name"
```

### 断开连接

```bash
npx @midscene/ios@1 disconnect
```

## 工作流程模式

由于 CLI 命令在每次调用之间是无状态的，请遵循以下模式：

1. **连接**以建立会话
2. **启动目标应用程序并截取屏幕截图**以查看当前状态，确保应用程序已启动并在屏幕上可见。
3. **使用 `act` 执行所需操作或目标驱动的指令。
4. **完成后断开连接**

## 最佳实践

1. **明确 UI 元素**：不要使用模糊的描述，而应提供清晰、具体的细节。例如，使用“右上角的设置图标”而不是“图标”。
2. **尽可能描述位置**：通过描述元素的位置来帮助定位目标元素（例如，“右上角的搜索图标”、“列表中的第三个项目”）。
3. **切勿在后台运行**：每个中间场景命令都必须同步执行——后台执行会打断“截图 → 分析 → 执行”的循环。
4. **将相关操作批量放入一个 `act` 命令中**：在同一应用程序内执行连续操作时，将它们合并为一个 `act` 命令，而不是分成多个单独的命令。例如，“打开设置、点击 Wi-Fi 并检查连接的网络”应该是一个 `act` 调用，而不是三个单独的命令。这样可以减少往返次数，避免不必要的截图分析循环，并显著提高效率。
5. **完成任务后汇总报告文件**：自动化任务完成后，收集并汇总所有报告文件（截图、日志、输出文件等）供用户查看。提供关于完成的内容、生成的文件及其位置的清晰总结，以便用户轻松查看结果。

**示例 — 警告对话框交互：**

```bash
npx @midscene/ios@1 act --prompt "tap the Delete button and confirm in the alert dialog"
npx @midscene/ios@1 take_screenshot
```

**示例 — 表单交互：**

```bash
npx @midscene/ios@1 act --prompt "fill in the username field with 'testuser' and the password field with 'pass123', then tap the Login button"
npx @midscene/ios@1 take_screenshot
```

## 故障排除

### WebDriverAgent 未运行
**症状：**连接被拒绝或出现超时错误。
**解决方法：**
- 确保 WebDriverAgent 已安装在设备上并且正在运行。
- 请参阅 https://midscenejs.com/zh/usage-ios.html 以获取设置说明。

### 未找到设备
**症状：**未检测到设备或出现连接错误。
**解决方法：**
- 确保设备已通过 USB 连接并且被系统信任。

### API 密钥问题
**症状：**认证或模型错误。
**解决方法：**
- 检查 `.env` 文件中是否包含 `MIDSCENE_MODEL_API_KEY=<your-key>`。
- 详情请参阅 https://midscenejs.com/zh/model-common-config.html。