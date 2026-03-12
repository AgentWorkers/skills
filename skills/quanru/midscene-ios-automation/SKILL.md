---
name: ios-device-automation
description: >
  使用 Midscene CLI 实现基于视觉的 iOS 设备自动化。完全通过截图进行操作，无需 DOM 或辅助功能标签；可以与屏幕上所有可见元素进行交互，无论其使用的技术栈是什么。  
  通过 WebDriverAgent，可以使用自然语言命令控制 iOS 设备。  
  相关术语：  
  ios、iphone、ipad、ios app、tap on iphone、swipe、mobile app ios、ios device、ios testing、iphone automation、ipad automation、ios screen、ios navigate  
  技术支持：Midscene.js（https://midscenejs.com）
env:
  - MIDSCENE_MODEL_API_KEY
  - MIDSCENE_MODEL_NAME
  - MIDSCENE_MODEL_BASE_URL
  - MIDSCENE_MODEL_FAMILY
allowed-tools:
  - Bash
---
# iOS 设备自动化

> **重要规则 — 违反规则将导致工作流程中断：**
>
> 1. **切勿在后台运行中间场景命令。**每个命令必须同步执行，以便您可以在决定下一步操作之前读取其输出（特别是截图）。后台执行会破坏“截图-分析-执行”的循环。
> 2. **每次只运行一个中间场景命令。**等待上一个命令完成，读取截图后，再决定下一步操作。切勿将多个命令链接在一起。
> 3. **为每个命令留出足够的时间完成。**中间场景命令涉及 AI 推理和屏幕交互，这可能比典型的 shell 命令花费更长时间。一个典型的命令需要大约 1 分钟；复杂的 `act` 命令可能需要更长时间。
> 4. **在完成任务前必须报告结果。**完成自动化任务后，您必须主动向用户总结结果——包括找到的关键数据、完成的操作、拍摄的截图以及任何相关发现。切勿在最后一个自动化步骤后默默结束；用户期望在一次交互中收到完整的回复。

使用 `npx @midscene/ios@1` 来自动化 iOS 设备。每个 CLI 命令都直接对应一个 MCP 工具——您（AI 代理）作为大脑，根据截图来决定采取哪些操作。

## 先决条件

Midscene 需要具有强大视觉理解能力的模型。以下环境变量必须进行配置——可以作为系统环境变量或在当前工作目录中的 `.env` 文件中配置（Midscene 会自动加载 `.env` 文件）：

```bash
MIDSCENE_MODEL_API_KEY="your-api-key"
MIDSCENE_MODEL_NAME="model-name"
MIDSCENE_MODEL_BASE_URL="https://..."
MIDSCENE_MODEL_FAMILY="family-identifier"
```

> ⚠️ **安全提示**：将 `.env` 文件添加到 `.gitignore` 中，以防止 API 密钥被意外提交到版本控制系统中。
> 仅使用官方的、受信任的提供者 URL 作为 `MIDSCENE_MODEL_BASE_URL`。

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

如果模型未配置，请让用户进行设置。有关支持的提供者，请参阅 [模型配置](https://midscenejs.com/model-common-config)。

## 命令

### 连接到设备

```bash
npx @midscene/ios@1 connect
```

### 拍摄截图

```bash
npx @midscene/ios@1 take_screenshot
```

拍摄截图后，读取保存的图像文件以了解当前屏幕状态，然后再决定下一步操作。

### 执行操作

使用 `act` 与设备交互并获取结果。它内部会自动处理所有的 UI 交互——点击、输入、滚动、滑动、等待和导航——因此您应该将复杂的任务作为一个整体来描述，而不是分解成小步骤。用自然语言描述**您想要执行的操作及其预期效果**：

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

由于 CLI 命令在调用之间是无状态的，请遵循以下模式：

1. **连接**以建立会话
2. **启动目标应用程序并拍摄截图**以查看当前状态，确保应用程序已启动并在屏幕上可见。
3. **使用 `act` 执行所需的操作或目标驱动的指令。
4. **完成后断开连接**
5. **报告结果**——总结已完成的内容、任务期间提取的关键数据和文件（截图、日志等）及其路径。

## 最佳实践

1. **明确 UI 元素**：提供清晰、具体的细节，而不是模糊的描述。例如，使用“右上角的设置图标”而不是“图标”。
2. **尽可能描述位置**：通过描述元素的位置来帮助定位目标元素（例如，“右上角的搜索图标”、“列表中的第三个项目”）。
3. **切勿在后台运行**：每个中间场景命令必须同步执行——后台执行会破坏“截图-分析-执行”的循环。
4. **将相关操作批量放入一个 `act` 命令中**：在同一应用程序内执行连续操作时，将它们合并为一个 `act` 命令，而不是分开成多个命令。例如，“打开设置、点击 Wi-Fi 并检查连接的网络”应该是一个 `act` 调用，而不是三个单独的命令。这样可以减少往返次数，避免不必要的截图-分析循环，并显著提高效率。
5. **完成任务后必须报告结果**：完成自动化任务后，您必须主动向用户展示结果，而无需等待用户询问。这包括：(1) 用户原始问题的答案或请求任务的结果，(2) 执行过程中提取或观察到的关键数据，(3) 截图和其他生成的文件及其路径，(4) 所采取步骤的简要总结。切勿在最后一个自动化命令后默默结束——用户期望在一次交互中收到完整的回复。

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
**症状：**连接被拒绝或超时错误。
**解决方法：**
- 确保 WebDriverAgent 已安装在设备上并且正在运行。
- 请参阅 https://midscenejs.com/zh/usage-ios.html 以获取设置说明。

### 未找到设备
**症状：**未检测到设备或连接错误。
**解决方法：**
- 确保设备通过 USB 连接并且被系统信任。

### API 密钥问题
**症状：**身份验证或模型错误。
**解决方法：**
- 检查 `.env` 文件中是否包含 `MIDSCENE_MODEL_API_KEY=<your-key>`。
- 详情请参阅 https://midscenejs.com/zh/model-common-config.html。