---
name: Desktop Computer Automation
description: |
  Vision-driven desktop automation using Midscene. Control your desktop (macOS, Windows, Linux) with natural language commands.
  Operates entirely from screenshots — no DOM or accessibility labels required. Can interact with all visible elements on screen regardless of technology stack.

  Triggers: open app, press key, desktop, computer, click on screen, type text, screenshot desktop,
  launch application, switch window, desktop automation, control computer, mouse click, keyboard shortcut,
  screen capture, find on screen, read screen, verify window, close app, minimize window, maximize window

  Powered by Midscene.js (https://midscenejs.com)
allowed-tools:
  - Bash
---

# 桌面电脑自动化

> **重要规则 — 违反这些规则将破坏工作流程：**
>
> 1. **切勿在后台运行中间场景命令。**每个命令都必须同步执行，以便您可以在决定下一步操作之前读取其输出（尤其是截图）。后台执行会打断“截图-分析-执行”的循环。
> 2. **每次只能运行一个中间场景命令。**等待上一个命令完成，读取截图后，再决定下一步操作。切勿将多个命令链接在一起。
> 3. **为每个命令留出足够的时间来完成。**中间场景命令涉及人工智能推理和屏幕交互，这可能比普通的shell命令花费更长时间。一个普通的命令大约需要1分钟；复杂的`act`命令可能需要更长时间。

使用`npx @midscene/computer@1`来控制您的桌面（macOS、Windows、Linux）。每个CLI命令都直接对应一个MCP工具——您（人工智能代理）作为大脑，根据截图来决定要执行的操作。

## 先决条件

Midscene需要具有强大视觉理解能力的模型。以下环境变量必须进行配置——可以在系统环境变量中设置，或者在当前工作目录下的`.env`文件中设置（Midscene会自动加载`.env`文件）：

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

如果模型未配置，请让用户进行设置。有关支持的提供者，请参阅[模型配置](https://midscenejs.com/model-common-config)。

## 命令

### 连接桌面

```bash
npx @midscene/computer@1 connect
npx @midscene/computer@1 connect --displayId <id>
```

### 列出显示屏幕

```bash
npx @midscene/computer@1 list_displays
```

### 截取截图

```bash
npx @midscene/computer@1 take_screenshot
```

截取截图后，先读取保存的图像文件以了解当前屏幕状态，然后再决定下一步操作。

### 执行操作

使用`act`与电脑交互并获取结果。它会自动处理所有的UI交互——点击、输入、滚动、等待和导航——因此您应该将复杂的、高层次的任务作为一个整体来描述，而不是分解成小步骤。用自然语言描述**您想要做什么以及期望的效果**：

```bash
# specific instructions
npx @midscene/computer@1 act --prompt "type hello world in the search field and press Enter"
npx @midscene/computer@1 act --prompt "drag the file icon to the Trash"

# or target-driven instructions
npx @midscene/computer@1 act --prompt "search for the weather in Shanghai using the Chrome browser, tell me the result"
```

### 断开连接

```bash
npx @midscene/computer@1 disconnect
```

## 工作流程模式

由于CLI命令在每次调用之间是无状态的，请遵循以下模式：

1. **连接**以建立会话
2. **健康检查**——观察`connect`命令的输出。如果`connect`已经进行了健康检查（截图和鼠标移动测试），则无需额外检查。如果`connect`没有进行健康检查，请手动执行：截取截图并验证是否成功，然后将鼠标移动到随机位置（`act --prompt "move the mouse to a random position"`）并验证是否成功。如果任一步失败，请停止并排查故障后再继续。只有在两次检查都无误后，才能进行下一步。
3. **启动目标应用程序并截取截图**以查看当前状态，确保应用程序已启动并在屏幕上可见。
4. **使用`act`执行操作**以执行所需的操作或目标驱动的指令。
5. **完成后断开连接**

## 最佳实践

1. **始终先进行健康检查**：连接后，观察`connect`命令的输出。如果`connect`已经进行了健康检查（截图和鼠标移动测试），则无需额外检查。如果没有，请手动执行：截取截图并将鼠标移动到随机位置。这两个步骤都必须成功（无错误）才能继续进行任何进一步操作。这可以及早发现环境问题。
2. **在使用此技能之前将目标应用程序带到前台**：为了提高效率，请使用其他方法（例如，在macOS上使用`open -a <AppName>`，在Windows上使用`start <AppName>`）将应用程序带到前台，然后再调用任何中间场景命令。然后截取截图以确认应用程序确实处于前台。只有在视觉确认后，才能使用此技能进行UI自动化。避免通过Midscene使用Spotlight、开始菜单搜索或其他基于启动器的方法——这些方法涉及短暂的UI交互、多次人工智能推理步骤，并且速度明显较慢。
3. **关于UI元素要具体**：不要使用模糊的描述，而要提供清晰、具体的细节。例如，说“Safari窗口左上角的红色关闭按钮”，而不是“关闭按钮”。
4. **尽可能描述位置**：通过描述元素的位置来帮助定位目标元素（例如，“菜单栏右上角的图标”，“左侧边栏的第三个项目”）。
5. **切勿在后台运行**：每个中间场景命令都必须同步执行——后台执行会打断“截图-分析-执行”的循环。
6. **检查多个显示屏幕**：如果您启动了应用程序但在截图中看不到它，可能是应用程序窗口在另一个显示屏幕上打开。使用`list_displays`来检查可用的显示屏幕。您有两个选择：要么将应用程序窗口移动到当前显示屏幕，要么使用`connect --displayId <id>`切换到应用程序所在的显示屏幕。
7. **将相关操作合并到一个`act`命令中**：在同一应用程序内执行连续操作时，将它们合并到一个`act`命令中，而不是分成单独的命令。例如，“搜索X，点击第一个结果，然后向下滚动查看更多细节”应该是一个`act`调用，而不是三个单独的命令。这样可以减少往返次数，避免不必要的截图-分析循环，并显著提高效率。
8. **在运行前设置`PATH`（macOS）**：在macOS上，如果`PATH`不完整，某些命令（例如`system_profiler`）可能无法找到。在运行任何中间场景命令之前，请确保`PATH`包含标准的系统目录：
   ```bash
   export PATH="/usr/sbin:/usr/bin:/bin:/sbin:$PATH"
   ```
   这可以防止因缺少系统工具而导致截图失败。
9. **完成自动化任务后汇总报告文件**：完成自动化任务后，收集并汇总所有报告文件（截图、日志、输出文件等）供用户查看。清楚地总结完成了哪些任务、生成了哪些文件以及它们的位置，以便用户方便地查看结果。

**示例 — 上下文菜单交互：**

```bash
npx @midscene/computer@1 act --prompt "right-click the file icon and select Delete from the context menu"
npx @midscene/computer@1 take_screenshot
```

**示例 — 下拉菜单：**

```bash
npx @midscene/computer@1 act --prompt "open the File menu and click New Window"
npx @midscene/computer@1 take_screenshot
```

## 故障排除

### macOS：访问权限被拒绝
您的终端应用程序没有访问权限：
1. 打开**系统设置 > 隐私与安全 > 访问权限**
2. 添加您的终端应用程序并启用它
3. 授予权限后重新启动终端应用程序

### macOS：找不到Xcode命令行工具
```bash
xcode-select --install
```

### API密钥未设置
检查`.env`文件中是否包含`MIDSCENE_MODEL_API_KEY=<your-key>`。

### macOS：使用`system_profiler`截取截图失败
如果`take_screenshot`失败并显示错误“system_profiler: command not found”，则可能是`PATH`环境变量不完整。请运行以下命令进行修复：
```bash
export PATH="/usr/sbin:/usr/bin:/bin:/sbin:$PATH"
```
然后重新尝试截图命令。

### 人工智能无法找到元素
1. 截取截图以确认元素确实可见
2. 使用更具体的描述（包括颜色、位置、周围文本）
3. 确保元素没有被其他窗口遮挡