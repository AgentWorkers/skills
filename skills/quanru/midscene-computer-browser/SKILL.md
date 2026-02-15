---
name: Browser Automation
description: |
  Vision-driven browser automation using Midscene. Operates entirely from screenshots — no DOM or accessibility labels required. Can interact with all visible elements on screen regardless of technology stack.

  Opens a new browser tab for each target URL via Puppeteer (headless Chrome).

  Use this skill when the user wants to:
  - Browse, navigate, or open web pages
  - Scrape, extract, or collect data from websites
  - Fill out forms, click buttons, or interact with web elements
  - Verify, validate, or test frontend UI behavior
  - Take screenshots of web pages
  - Automate multi-step web workflows
  - Run browser automation or check website content


  Powered by Midscene.js (https://midscenejs.com)
allowed-tools:
  - Bash
---

# 浏览器自动化

> **重要规则 — 违反这些规则会导致工作流程中断：**
>
> 1. **切勿在后台运行中间场景命令。**每个命令都必须同步执行，以便您可以在决定下一步操作之前读取其输出（特别是截图）。后台执行会打断“截图-分析-执行”的循环。
> 2. **每次只运行一个中间场景命令。**等待上一个命令完成，读取截图，然后决定下一步操作。切勿将多个命令串联在一起。
> 3. **为每个命令留出足够的时间来完成。**中间场景命令涉及人工智能推理和屏幕交互，这可能比普通的shell命令花费更长时间。一个普通的命令大约需要1分钟；复杂的`act`命令可能需要更长时间。

使用`npx @midscene/web@1`来自动化网页浏览。该命令会通过Puppeteer启动一个无头Chrome浏览器，并且**在多次CLI调用之间保持会话的连续性**——命令之间不会丢失会话信息。每个CLI命令都直接对应一个MCP工具——您（人工智能代理）负责根据截图来决定执行哪些操作。

## 适用场景

当以下情况发生时，可以使用此技能：
- 用户希望浏览或导航到特定的URL
- 您需要从网站中抓取、提取或收集数据
- 您想要验证或测试前端用户界面的行为
- 用户需要网页的截图

如果您需要保留登录会话或使用用户现有的浏览器标签页，请改用**Chrome Bridge自动化**技能。

## 先决条件

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

常用的模型包括：Doubao Seed 1.6、Qwen3-VL、Zhipu GLM-4.6V、Gemini-3-Pro、Gemini-3-Flash。

如果模型尚未配置，请让用户进行设置。有关支持的模型提供商，请参阅[模型配置](https://midscenejs.com/model-common-config)。

## 命令

### 连接到网页

```bash
npx @midscene/web@1 connect --url https://example.com
```

### 截取截图

```bash
npx @midscene/web@1 take_screenshot
```

截取截图后，请读取保存的图像文件，以了解当前页面的状态，然后再决定下一步操作。

### 执行操作

使用`act`与页面进行交互并获取结果。它会自动处理所有的UI交互——点击、输入、滚动、悬停、等待和导航——因此您应该以整体的方式给出复杂的、高层次的任务，而不是将其拆分成小步骤。用自然语言描述**您想要做什么以及期望的效果**：

```bash
# specific instructions
npx @midscene/web@1 act --prompt "click the Login button and fill in the email field with 'user@example.com'"
npx @midscene/web@1 act --prompt "scroll down and click the Submit button"

# or target-driven instructions
npx @midscene/web@1 act --prompt "click the country dropdown and select Japan"
```

### 断开连接

断开与页面的连接，但保持浏览器运行：

```bash
npx @midscene/web@1 disconnect
```

### 关闭浏览器

完成后完全关闭浏览器：

```bash
npx @midscene/web@1 close
```

## 工作流程模式

浏览器通过后台的Chrome进程在多次CLI调用之间保持连接。请遵循以下模式：
1. **连接到**一个URL以打开一个新的标签页
2. **截取截图**以查看当前页面的状态，确保页面已加载。
3. **使用`act`执行**所需的操作或基于目标的指令。
4. **关闭**浏览器（或**断开连接**以备后续使用）

## 最佳实践
1. **始终先连接**：在任何交互之前，使用`connect --url`导航到目标URL。
2. **明确指定UI元素**：不要使用“the button”，而应使用“联系表单中的蓝色提交按钮”。
3. **使用自然语言**：描述您在页面上看到的内容，而不是CSS选择器。例如，使用“红色的立即购买按钮”而不是“#buy-btn”。
4. **处理加载状态**：在导航或触发页面加载的操作之后，截取截图以确认页面已加载。
5. **完成后关闭**：使用`close`关闭浏览器并释放资源。
6. **切勿在后台运行**：每个中间场景命令都必须同步执行——后台执行会打断“截图-分析-执行”的循环。
7. **将相关操作批量放入一个`act`命令中**：在同一页面内执行连续操作时，将它们合并为一个`act`命令，而不是分开成多个命令。例如，“填写电子邮件和密码字段，然后点击登录按钮”应该是一个`act`调用，而不是三个单独的命令。这样可以减少往返次数，避免不必要的截图-分析循环，并显著提高效率。
8. **完成后汇总报告文件**：完成自动化任务后，收集并汇总所有报告文件（截图、日志、输出文件等）供用户查看。清晰地总结完成了哪些任务、生成了哪些文件以及它们的位置，以便用户能够方便地查看结果。

**示例 — 下拉菜单选择：**

```bash
npx @midscene/web@1 act --prompt "click the country dropdown and select Japan"
npx @midscene/web@1 take_screenshot
```

**示例 — 表单交互：**

```bash
npx @midscene/web@1 act --prompt "fill in the email field with 'user@example.com' and the password field with 'pass123', then click the Log In button"
npx @midscene/web@1 take_screenshot
```

## 故障排除

### 连接失败
- 确保系统中安装了Chrome/Chromium（Puppeteer默认会自行下载）。
- 检查防火墙是否阻止了Chrome的调试端口。

### API密钥错误
- 确保`.env`文件中包含`MIDSCENE_MODEL_API_KEY=<your-key>`。
- 验证该密钥是否适用于配置的模型提供商。

### 超时
- 网页可能需要时间加载。连接后，请截取截图以确认页面已加载完毕再开始交互。
- 对于加载速度较慢的页面，在步骤之间稍作等待。

### 截图无法显示
- 截图路径是到本地文件的绝对路径。使用Read工具来查看截图。