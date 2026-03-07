---
name: chrome-bridge-automation
description: >
  **基于Midscene Bridge模式的视觉驱动浏览器自动化工具**  
  该工具完全通过截图进行操作，无需依赖DOM结构或辅助技术（如屏幕阅读器）即可工作。无论网站使用何种技术栈，它都能与屏幕上所有可见的元素进行交互。  
  该模式通过Midscene的Chrome扩展程序与用户的桌面Chrome浏览器连接，从而保留用户的Cookie、会话状态及登录信息。  
  **适用场景：**  
  - 在用户的Chrome浏览器中浏览、导航或打开网页  
  - 与需要登录会话、Cookie或浏览器状态才能正常运行的网页进行交互  
  - 使用用户的真实浏览器从网站中抓取数据  
  - 填写表单、点击按钮或操作网页元素  
  - 验证前端用户界面的行为  
  - 截取网页截图  
  - 自动化多步骤的网页操作流程  
  - 检查网站的内容或外观  
  **技术支持：**  
  该工具由Midscene.js（https://midscenejs.com）提供技术支持。
allowed-tools:
  - Bash
---
# Chrome Bridge自动化

> **重要规则 — 违反这些规则将导致工作流程中断：**
>
> 1. **切勿在后台运行中间场景命令。**每个命令都必须同步执行，以便您可以在决定下一步操作之前读取其输出（尤其是截图）。后台执行会破坏“截图-分析-执行”的循环。
> 2. **每次只运行一个中间场景命令。**等待上一个命令完成，读取截图，然后再决定下一步操作。切勿将多个命令链式执行。
> 3. **为每个命令留出足够的时间来完成。**中间场景命令涉及人工智能推理和屏幕交互，这可能比普通的shell命令花费更长时间。一个普通的命令大约需要1分钟；复杂的`act`命令可能需要更长时间。
> 4. **在完成任务前必须报告结果。**在完成自动化任务后，您必须主动向用户总结结果——包括找到的关键数据、完成的操作、拍摄的截图以及任何相关的发现。切勿在最后一个自动化步骤后默默结束；用户期望在一次交互中得到完整的反馈。

通过Midscene Chrome扩展程序（Bridge模式）自动化用户的真实Chrome浏览器，同时保留cookies、会话和登录状态。您（AI代理）作为“大脑”，根据截图来决定采取哪些操作。

## 命令格式

**重要提示 — 每个命令都必须遵循这个确切的格式。请勿修改命令前缀。**

```
npx @midscene/web@1 --bridge <subcommand> [args]
```

- `--bridge`标志是**必须的**——它激活Bridge模式以连接到用户的桌面Chrome浏览器

## 先决条件

用户已经安装了Chrome和Midscene扩展程序。在连接之前无需检查浏览器或扩展程序的状态——直接连接即可。

Midscene需要具有强大视觉理解能力的模型。以下环境变量必须进行配置——可以作为系统环境变量或在当前工作目录下的`.env`文件中配置（Midscene会自动加载`.env`文件）：

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

如果模型未配置，请让用户进行设置。有关支持的模型，请参阅[模型配置](https://midscenejs.com/model-common-config)。

## 命令

### 连接到网页

```bash
npx @midscene/web@1 --bridge connect --url https://example.com
```

### 拍摄截图

```bash
npx @midscene/web@1 --bridge take_screenshot
```

拍摄截图后，读取保存的图像文件以了解当前页面的状态，然后再决定下一步操作。

### 执行操作

使用`act`与页面进行交互并获取结果。它内部会自动处理所有的UI交互——点击、输入、滚动、悬停、等待和导航——因此您应该以整体的方式给出复杂的、高层次的任务，而不是将其拆分成小步骤。用自然语言描述**您想要做什么以及期望的效果**：

```bash
# specific instructions
npx @midscene/web@1 --bridge act --prompt "click the Login button and fill in the email field with 'user@example.com'"
npx @midscene/web@1 --bridge act --prompt "scroll down and click the Submit button"

# or target-driven instructions
npx @midscene/web@1 --bridge act --prompt "click the country dropdown and select Japan"
```

### 断开连接

```bash
npx @midscene/web@1 --bridge disconnect
```

## 工作流程模式

Bridge模式连接到用户的真实Chrome浏览器。每个CLI命令都会建立自己的临时连接，但**浏览器、标签页以及所有状态（cookies、登录会话）始终会被保留**，无论您是否断开连接。这使得重新连接变得简单且不会丢失数据。

遵循以下流程：
1. **连接到**目标URL以建立会话
2. **拍摄截图**以查看当前状态，确保页面已加载。
3. **执行操作**使用`act`来执行所需的操作或基于目标的指令。
4. **报告结果**——总结已完成的任务、任务中提取的关键数据和文件（截图、日志等）及其路径
5. **仅在用户完成任务后断开连接**。**如果用户还有后续操作，请勿断开连接**——保持会话状态以便在后续对话中继续交互。

## 最佳实践

1. **始终先连接**：在使用任何交互之前，使用`connect --url`导航到目标URL。
2. **明确指定UI元素**：不要使用“the button”，而应使用“联系表单中的蓝色提交按钮”。
3. **使用自然语言**：描述您在页面上看到的内容，而不是CSS选择器。例如，使用“红色的立即购买按钮”而不是“#buy-btn”。
4. **处理加载状态**：在导航或触发页面加载的操作之后，拍摄截图以验证页面是否已加载。
5. **仅在任务完全完成后断开连接**：只有在用户的整体任务完全完成且没有后续操作时才断开连接。在多轮对话中，可以跳过断开连接，以便继续使用浏览器进行交互。断开连接是安全的——它只会关闭CLI端的连接，而不会关闭浏览器或标签页——但如果用户希望继续操作，则重新连接会带来不必要的开销。
6. **切勿在后台运行**：每个中间场景命令都必须同步执行——后台执行会破坏“截图-分析-执行”的循环。
7. **将相关操作批量放入一个`act`命令中**：在同一页面内执行连续操作时，将它们合并为一个`act`命令，而不是分成多个单独的命令。例如，“填写电子邮件和密码字段，然后点击登录按钮”应该是一个`act`调用，而不是三个单独的命令。这样可以减少往返次数，避免不必要的截图-分析循环，并显著提高效率。
8. **完成任务后务必报告结果**：在完成自动化任务后，您必须主动向用户展示结果，而无需等待用户询问。这包括：(1) 用户原始问题的答案或请求任务的结果，(2) 执行过程中提取的关键数据或观察到的内容，(3) 截图和其他生成的文件及其路径，(4) 执行步骤的简要总结。切勿在最后一个自动化命令后默默结束——用户期望在一次交互中得到完整的反馈。

**示例 — 下拉菜单选择：**

```bash
npx @midscene/web@1 --bridge act --prompt "click the country dropdown and select Japan"
npx @midscene/web@1 --bridge take_screenshot
```

**示例 — 表单交互：**

```bash
npx @midscene/web@1 --bridge act --prompt "fill in the email field with 'user@example.com' and the password field with 'pass123', then click the Log In button"
npx @midscene/web@1 --bridge take_screenshot
```

## 故障排除

### Bridge模式连接失败
- 请用户检查Chrome是否已打开，并且Midscene扩展程序已安装并启用。
- Midscene扩展程序可以从Chrome Web Store安装：https://chromewebstore.google.com/detail/midscenejs/gbldofcpkknbggpkmbdaefngejllnief
- 确认扩展程序中的“bridge mode”指示器显示为“Listening”状态。
- 查看[Bridge模式文档](https://midscenejs.com/bridge-mode-by-chrome-extension.html)。

### 超时
- 网页可能需要时间加载。连接后，请先拍摄截图以确认页面已准备好再进行交互。
- 对于加载速度较慢的页面，请在步骤之间稍作等待。

### 截图无法显示
- 截图路径是本地文件的绝对路径。使用Read工具来查看截图。