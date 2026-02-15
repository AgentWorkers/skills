---
name: Chrome Bridge Automation
description: |
  Vision-driven browser automation using Midscene Bridge mode. Operates entirely from screenshots — no DOM or accessibility labels required. Can interact with all visible elements on screen regardless of technology stack.

  This mode connects to the user's desktop Chrome browser via the Midscene Chrome Extension, preserving cookies, sessions, and login state.

  Use this skill when the user wants to:
  - Browse, navigate, or open web pages in the user's own Chrome browser
  - Interact with pages that require login sessions, cookies, or existing browser state
  - Scrape, extract, or collect data from websites using the user's real browser
  - Fill out forms, click buttons, or interact with web elements
  - Verify, validate, or test frontend UI behavior
  - Take screenshots of web pages
  - Automate multi-step web workflows
  - Check website content or appearance

  Powered by Midscene.js (https://midscenejs.com)
allowed-tools:
  - Bash
---

# Chrome Bridge自动化

> **重要规则 — 违反这些规则将导致工作流程中断：**
>
> 1. **切勿在后台运行中间场景命令。**每个命令都必须同步执行，以便在决定下一步操作之前能够读取其输出（尤其是截图）。后台执行会破坏“截图-分析-执行”的循环。
> 2. **每次只能运行一个中间场景命令。**等待上一个命令完成，读取截图后，再决定下一步操作。切勿将多个命令链接在一起。
> 3. **为每个命令留出足够的时间完成。**中间场景命令涉及AI推理和屏幕交互，这可能比普通的shell命令花费更长时间。一个普通的命令大约需要1分钟；复杂的`act`命令可能需要更长时间。

通过Midscene Chrome扩展程序（Bridge模式）自动化用户的真实Chrome浏览器，同时保留cookies、会话和登录状态。你（AI代理）作为“大脑”，根据截图来决定采取哪些操作。

## 命令格式

**重要提示 — 每个命令都必须遵循此格式。切勿修改命令前缀。**

```
npx @midscene/web@1 --bridge <subcommand> [args]
```

- `--bridge`标志是**必须的** — 它用于激活Bridge模式，以连接到用户的桌面Chrome浏览器

## 先决条件

用户已经安装了Chrome和Midscene扩展程序。在连接之前无需检查浏览器或扩展程序的状态——直接连接即可。

Midscene需要具有强大视觉理解能力的模型。以下环境变量必须进行配置——可以作为系统环境变量设置，或者放在当前工作目录下的`.env`文件中（Midscene会自动加载`.env`文件）：

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

常用的模型：Doubao Seed 1.6、Qwen3-VL、Zhipu GLM-4.6V、Gemini-3-Pro、Gemini-3-Flash。

如果模型未配置，请让用户进行设置。有关支持的模型提供商，请参阅[模型配置](https://midscenejs.com/model-common-config)。

## 命令

### 连接到网页

```bash
npx @midscene/web@1 --bridge connect --url https://example.com
```

### 截取截图

```bash
npx @midscene/web@1 --bridge take_screenshot
```

截取截图后，读取保存的图像文件以了解当前页面的状态，然后再决定下一步操作。

### 执行操作

使用`act`与页面进行交互并获取结果。它内部会自动处理所有的UI交互——点击、输入、滚动、悬停、等待和导航——因此你应该以整体的方式给出复杂的、高层次的任务，而不是将其分解为小步骤。用自然语言描述**你想要做什么以及期望的效果**：

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

由于CLI命令在每次调用之间是无状态的，请遵循以下模式：

1. **连接到URL**以建立会话
2. **截取截图**以查看当前状态，确保页面已加载。
3. **使用`act`执行操作**以完成所需的操作或目标驱动的指令。
4. **完成后断开连接**

## 最佳实践

1. **始终先连接**：在任何交互之前，使用`connect --url`导航到目标URL。
2. **明确指定UI元素**：不要使用“the button”，而应使用“联系表单中的蓝色提交按钮”。
3. **使用自然语言**：描述你在页面上看到的内容，而不是CSS选择器。例如，使用“红色的立即购买按钮”而不是“#buy-btn”。
4. **处理加载状态**：在导航或触发页面加载的操作之后，截取截图以验证页面是否已加载。
5. **完成后断开连接**：始终断开连接以释放资源。
6. **切勿在后台运行**：每个中间场景命令都必须同步执行——后台执行会破坏“截图-分析-执行”的循环。
7. **将相关操作批量放入一个`act`命令中**：在同一页面内执行连续操作时，将它们合并为一个`act`命令，而不是分成多个单独的命令。例如，“填写电子邮件和密码字段，然后点击登录按钮”应该是一个`act`调用，而不是三个单独的命令。这样可以减少往返次数，避免不必要的截图-分析循环，并显著提高效率。
8. **完成后汇总报告文件**：完成自动化任务后，收集并汇总所有报告文件（截图、日志、输出文件等）供用户查看。提供一个清晰的总结，说明完成了哪些任务、生成了哪些文件以及它们的位置，方便用户查看结果。

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
- 询问用户是否打开了Chrome浏览器，并且Midscene扩展程序已安装并启用。
- Midscene扩展程序可以从Chrome Web Store安装：https://chromewebstore.google.com/detail/midscenejs/gbldofcpkknbggpkmbdaefngejllnief
- 检查扩展程序中的“bridge mode”指示器是否显示“Listening”状态。
- 查看[Bridge模式文档](https://midscenejs.com/bridge-mode-by-chrome-extension.html)。

### 超时
- 网页可能需要时间加载。连接后，截取截图以确认页面已准备好再进行交互。
- 对于加载速度较慢的页面，在步骤之间稍作等待。

### 截图无法显示
- 截图路径是本地文件的绝对路径。使用Read工具来查看截图。