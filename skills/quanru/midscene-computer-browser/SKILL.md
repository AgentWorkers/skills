---
name: Browser Automation
description: |
  AI-powered browser automation using Midscene. Use this skill when the user wants to:
  - Browse, navigate, or open web pages
  - Scrape, extract, or collect data from websites
  - Fill out forms, click buttons, or interact with web elements
  - Verify, validate, or test frontend UI behavior
  - Take screenshots of web pages
  - Automate multi-step web workflows
  - Run browser automation or check website content

  Opens a new browser tab for each target URL via Puppeteer (headless Chrome).

  Trigger keywords: browse, navigate, open url, web page, website, scrape, extract, crawl,
  fill form, click, interact, verify, validate, test, assert, screenshot, frontend, UI test,
  web automation, search web, check page, puppeteer, headless, CI
allowed-tools:
  - Bash
---

# 浏览器自动化

> **重要规则 — 违反这些规则将导致工作流程中断：**
>
> 1. **切勿在任何用于中间场景命令的 Bash 工具调用中设置 `run_in_background: true`**。每个 `npx @midscene/web` 命令都必须使用 `run_in_background: false`（或完全省略该参数）。在后台执行会导致任务结束后出现大量通知，从而破坏截图分析-执行循环。
> 2. **每次 Bash 工具调用只能发送一个中间场景 CLI 命令**。等待其结果，读取截图，然后决定下一步操作。切勿使用 `&&`、`;` 或 `sleep` 来链接命令。
> 3. **为每次 Bash 工具调用设置 `timeout: 60000`（60 秒）**，以确保中间场景命令有足够的时间同步完成。

使用 `npx @midscene/web` 自动化网页浏览。该工具会通过 Puppeteer 启动一个无头 Chrome 浏览器，并且 **在多次 CLI 调用之间保持会话的连续性**——命令之间不会丢失会话信息。每个 CLI 命令都直接对应一个 MCP 工具——你（AI 代理）根据截图来决定执行哪些操作。

## 适用场景

当以下情况发生时，可以使用此技能：
- 用户希望浏览或导航到特定 URL
- 需要从网站中抓取、提取或收集数据
- 需要验证或测试前端用户界面的行为
- 用户需要获取网页的截图

如果需要保留登录会话或使用用户的现有浏览器标签页，请改用 **Chrome Bridge Automation** 技能。

## 先决条件

CLI 会自动从当前工作目录加载 `.env` 文件。首次使用前，请确认 `.env` 文件存在并且包含 API 密钥：

```bash
cat .env | grep MIDSCENE_MODEL_API_KEY | head -c 30
```

如果没有 `.env` 文件或 API 密钥，请让用户创建一个。有关支持的提供者，请参阅 [模型配置](https://midscenejs.com/zh/model-common-config.html)。

**请勿运行 `echo $MIDSCENE_MODEL_API_KEY`**——密钥是在运行时从 `.env` 文件中加载的，而不是从 shell 环境中加载的。

## 命令

### 连接到网页

```bash
npx @midscene/web connect --url https://example.com
```

### 截取截图

```bash
npx @midscene/web take_screenshot
```

截取截图后，先读取保存的图像文件以了解当前页面的状态，然后再决定下一步操作。

### 执行操作

使用 `actionSpace` 工具与页面进行交互：

```bash
npx @midscene/web Tap --locate '{"prompt":"the Login button"}'
npx @midscene/web Input --locate '{"prompt":"the email field"}' --value 'user@example.com'
npx @midscene/web Scroll --direction down
npx @midscene/web Hover --locate '{"prompt":"the navigation menu"}'
npx @midscene/web KeyboardPress --value Enter
npx @midscene/web DragAndDrop --locate '{"prompt":"the draggable item"}' --target '{"prompt":"the drop zone"}'
```

### 自然语言操作

使用 `act` 在一个命令中执行多步骤操作——适用于处理瞬态用户界面：

```bash
npx @midscene/web act --prompt "click the country dropdown and select Japan"
```

### 断开连接

断开与页面的连接，但保持浏览器运行：

```bash
npx @midscene/web disconnect
```

### 关闭浏览器

操作完成后完全关闭浏览器：

```bash
npx @midscene/web close
```

## 工作流程模式

通过后台的 Chrome 进程，浏览器在多次 CLI 调用之间保持会话的连续性。请遵循以下模式：
1. **连接到** 目标 URL 以打开新标签页
2. **截取截图** 以查看当前页面状态
3. **分析截图** 以决定下一步操作
4. **执行操作**（点击、输入、滚动等）
5. **再次截取截图** 以验证结果
6. **重复步骤 3-5 直到任务完成
7. **完成后关闭** 浏览器（或**断开连接** 以备后续使用）

## 最佳实践

1. **始终先连接**：在任何交互之前，使用 `connect --url` 导航到目标 URL。
2. **频繁截图**：在每个操作之前和之后截图，以验证状态变化。
3. **在定位提示时具体说明**：不要使用 “the button”，而应使用 “联系表单中的蓝色提交按钮”。
4. **使用自然语言**：描述你在页面上看到的内容，而不是使用 CSS 选择器。例如，说 “红色的立即购买按钮” 而不是 “#buy-btn”。
5. **处理加载状态**：在导航或触发页面加载的操作之后，截取截图以确认页面已加载。
6. **完成后关闭**：使用 `close` 命令关闭浏览器并释放资源。
7. **切勿在后台运行**：在每次 Bash 工具调用中，要么省略 `run_in_background` 参数，要么明确将其设置为 `false`。切勿将其设置为 `run_in_background: true`。

### 处理瞬态用户界面

下拉菜单、自动完成弹窗、工具提示和确认对话框在命令执行过程中可能会消失。在处理瞬态用户界面时：
- **使用 `act` 来执行多步骤操作**——它会在一个进程中完成所有操作
- **或者快速连续执行命令**——不要在步骤之间截图
- **不要暂停进行分析**——连续执行所有与瞬态界面相关的命令
- 持久性的用户界面元素（页面内容、导航栏、侧边栏）可以在不同的命令之间进行交互

**示例 — 使用 `act` 进行下拉菜单选择（推荐用于处理瞬态用户界面）：**

```bash
npx @midscene/web act --prompt "click the country dropdown and select Japan"
npx @midscene/web take_screenshot
```

**示例 — 使用单独的命令进行下拉菜单选择（另一种方法）：**

```bash
# These commands must be run back-to-back WITHOUT screenshots in between
npx @midscene/web Tap --locate '{"prompt":"the country dropdown"}'
npx @midscene/web Tap --locate '{"prompt":"Japan option in the dropdown list"}'
# NOW take a screenshot to verify the result
npx @midscene/web take_screenshot
```

## 常见模式

### 简单浏览

```bash
npx @midscene/web connect --url 'https://news.ycombinator.com'
npx @midscene/web take_screenshot
# Read the screenshot, then decide next action
npx @midscene/web close
```

### 多步骤交互

```bash
npx @midscene/web connect --url 'https://example.com'
npx @midscene/web Tap --locate '{"prompt":"the Sign In link"}'
npx @midscene/web take_screenshot
npx @midscene/web Input --locate '{"prompt":"the email field"}' --value 'user@example.com'
npx @midscene/web Input --locate '{"prompt":"the password field"}' --value 'password123'
npx @midscene/web Tap --locate '{"prompt":"the Log In button"}'
npx @midscene/web take_screenshot
npx @midscene/web close
```

### 前端验证

```bash
npx @midscene/web connect --url 'http://localhost:3000'
npx @midscene/web take_screenshot
# Analyze: verify login form is visible
npx @midscene/web Input --locate '{"prompt":"the email field"}' --value 'test@example.com'
npx @midscene/web Input --locate '{"prompt":"the password field"}' --value 'password'
npx @midscene/web Tap --locate '{"prompt":"the Submit button"}'
npx @midscene/web take_screenshot
# Analyze: verify the welcome message is displayed
npx @midscene/web close
```

### 数据提取

```bash
npx @midscene/web connect --url 'https://example.com/products'
npx @midscene/web take_screenshot
# Read the screenshot to extract product names, prices, and ratings
npx @midscene/web close
```

## 前端验证工作流程

当需要验证或测试前端应用程序时：
1. 如果开发服务器尚未运行，请先启动它（例如，`npm run dev`）。
2. **连接到** 本地 URL（例如，`http://localhost:3000`）。
3. **截取截图** 以查看初始状态。
4. **分析截图** 以确认预期的用户界面元素是否存在。
5. **执行操作**（点击、输入、滚动等）以测试用户流程。
6. **每步操作后截取截图** 以验证结果。
7. **完成后关闭** 浏览器。

## 故障排除

### 连接失败
- 确保系统上安装了 Chrome/Chromium（Puppeteer 会默认下载所需的浏览器）。
- 检查防火墙是否阻塞了 Chrome 的调试端口。

### API 密钥错误
- 确保 `.env` 文件中包含 `MIDSCENE_MODEL_API_KEY=<your-key>`。
- 验证该密钥是否适用于配置的模型提供者。

### 超时
- 网页可能需要时间加载。连接后，先截取截图以确认页面已准备好再进行交互。
- 对于加载速度较慢的页面，在步骤之间稍作等待。

### 截图未显示
- 截图路径是指向本地文件的绝对路径。可以使用 Read 工具来查看截图文件。