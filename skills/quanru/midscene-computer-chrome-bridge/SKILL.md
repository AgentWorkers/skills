---
name: Chrome Bridge Automation
description: |
  AI-powered browser automation using Midscene Bridge mode. Use this skill when the user wants to:
  - Browse, navigate, or open web pages in the user's own Chrome browser
  - Interact with pages that require login sessions, cookies, or existing browser state
  - Scrape, extract, or collect data from websites using the user's real browser
  - Fill out forms, click buttons, or interact with web elements
  - Verify, validate, or test frontend UI behavior
  - Take screenshots of web pages
  - Automate multi-step web workflows
  - Check website content or appearance

  This mode connects to the user's real Chrome browser via the Midscene Chrome Extension,
  preserving cookies, sessions, and login state.

  Trigger keywords: browse, navigate, open url, web page, website, scrape, extract, crawl,
  fill form, click, interact, verify, validate, test, assert, screenshot, frontend, UI test,
  web automation, search web, check page, login, submit, chrome, bridge
allowed-tools:
  - Bash
---

# Chrome Bridge自动化

> **重要规则 — 违反这些规则将导致工作流程中断：**
>
> 1. **绝对不要在任何用于中间场景（midscene）命令的Bash工具调用中设置`run_in_background: true`**。每个`npx @midscene/web`命令都必须使用`run_in_background: false`（或者完全省略该参数）。在任务结束后，后台执行会导致通知频繁弹出，从而破坏截图-分析-执行（snapshot-analyze-act）的循环。
> 2. **每次Bash工具调用只能发送一个中间场景的CLI命令**。等待命令的结果，读取截图，然后再决定下一步操作。不要使用`&&`、`;`或`sleep`来链接多个命令。
> 3. **为每次Bash工具调用设置`timeout: 60000`（60秒）**，以确保中间场景命令有足够的时间同步完成。

通过Midscene Chrome扩展程序（Bridge模式）自动化用户的真实Chrome浏览器，同时保留cookies、会话和登录状态。你（AI代理）作为决策者，根据截图来决定采取哪些操作。

## 命令格式

**重要提示 — 每条命令都必须严格遵循此格式。请勿修改命令前缀。**

```
npx @midscene/web --bridge <subcommand> [args]
```

- `--bridge`标志是**必需的** — 它用于激活Bridge模式以连接到用户的真实Chrome浏览器。
- 如果不使用`--bridge`，CLI将启动一个无头浏览器（这对本技能来说是错误的操作）。
- **不要使用`-p`标志，也不要使用环境变量作为替代方案** — 请严格按照示例中的方式使用`--bridge`。

## 先决条件

用户已经安装并配置好了Chrome和Midscene扩展程序。无需检查浏览器或扩展程序的状态，直接进行连接即可。

CLI会自动从当前工作目录加载`.env`文件。首次使用前，请确认`.env`文件存在，并且其中包含API密钥：

```bash
cat .env | grep MIDSCENE_MODEL_API_KEY | head -c 30
```

如果不存在`.env`文件或API密钥，请让用户创建一个。有关支持的提供者，请参阅[模型配置](https://midscenejs.com/zh/model-common-config.html)。

**请不要运行`echo $MIDSCENE_MODEL_API_KEY`** — 密钥是在运行时从`.env`文件中加载的，而不是从shell环境中获取的。

## 命令

### 连接到网页

```bash
npx @midscene/web --bridge connect --url https://example.com
```

### 截取屏幕截图

```bash
npx @midscene/web --bridge take_screenshot
```

截取屏幕截图后，先读取保存的图像文件以了解当前页面的状态，然后再决定下一步操作。

### 执行操作

```bash
npx @midscene/web --bridge Tap --locate '{"prompt":"the Login button"}'
npx @midscene/web --bridge Input --locate '{"prompt":"the email field"}' --value 'user@example.com'
npx @midscene/web --bridge Scroll --direction down
npx @midscene/web --bridge Hover --locate '{"prompt":"the navigation menu"}'
npx @midscene/web --bridge KeyboardPress --value Enter
npx @midscene/web --bridge DragAndDrop --locate '{"prompt":"the draggable item"}' --target '{"prompt":"the drop zone"}'
```

### 使用自然语言执行操作

使用`act`命令在一个命令中执行多步操作 — 这对于处理临时性的用户界面（UI）交互非常有用：

```bash
npx @midscene/web --bridge act --prompt "click the country dropdown and select Japan"
```

### 断开连接

```bash
npx @midscene/web --bridge disconnect
```

## 工作流程模式

由于CLI命令在每次调用之间是无状态的，请遵循以下模式：

1. **连接到目标URL**以建立会话。
2. **截取屏幕截图**以查看当前页面状态。
3. **分析屏幕截图**以决定下一步操作。
4. **执行操作**（点击、输入、滚动等）。
5. **再次截取屏幕截图**以验证结果。
6. **重复步骤3-5，直到任务完成**。
7. **完成后断开连接**。

## 最佳实践

1. **始终先连接**：在任何操作之前，使用`connect --url`导航到目标URL。
2. **频繁截图**：在每次操作前后都截取屏幕截图，以验证状态变化。
3. **在定位提示时具体说明**：不要使用“the button”，而应使用“联系表单中的蓝色提交按钮”这样的描述。
4. **使用自然语言**：描述你在页面上看到的内容，而不是使用CSS选择器。例如，说“红色的立即购买按钮”而不是“#buy-btn”。
5. **处理加载状态**：在导航或触发页面加载的操作之后，截取屏幕截图以确认页面已加载。
6. **完成后断开连接**：始终断开连接以释放资源。
7. **切勿在后台运行**：在每次Bash工具调用中，要么省略`run_in_background`参数，要么明确将其设置为`false`。绝对不要设置`run_in_background: true`。

### 处理临时性UI元素

下拉菜单、自动完成弹窗、工具提示和确认对话框在命令执行过程中可能会消失。在处理这些临时性UI元素时：
- **使用`act`命令执行多步操作** — 它会在一个进程中完成所有操作。
- **或者快速连续执行命令** — 在步骤之间不要截取屏幕截图。
- **不要暂停进行分析** — 直接连续执行所有与临时UI相关的命令。
- 持久性UI元素（页面内容、导航栏、侧边栏）可以在不同的命令之间进行交互。

**示例 — 使用`act`命令选择下拉菜单（推荐用于处理临时性UI）：**

```bash
npx @midscene/web --bridge act --prompt "click the country dropdown and select Japan"
npx @midscene/web --bridge take_screenshot
```

**示例 — 使用单独的命令选择下拉菜单（另一种方法）：**

```bash
# These commands must be run back-to-back WITHOUT screenshots in between
npx @midscene/web --bridge Tap --locate '{"prompt":"the country dropdown"}'
npx @midscene/web --bridge Tap --locate '{"prompt":"Japan option in the dropdown list"}'
# NOW take a screenshot to verify the result
npx @midscene/web --bridge take_screenshot
```

## 常见模式

### 简单浏览

```bash
npx @midscene/web --bridge connect --url 'https://news.ycombinator.com'
npx @midscene/web --bridge take_screenshot
# Read the screenshot, then decide next action
npx @midscene/web --bridge disconnect
```

### 多步交互

```bash
npx @midscene/web --bridge connect --url 'https://example.com'
npx @midscene/web --bridge Tap --locate '{"prompt":"the Sign In link"}'
npx @midscene/web --bridge take_screenshot
npx @midscene/web --bridge Input --locate '{"prompt":"the email field"}' --value 'user@example.com'
npx @midscene/web --bridge Input --locate '{"prompt":"the password field"}' --value 'password123'
npx @midscene/web --bridge Tap --locate '{"prompt":"the Log In button"}'
npx @midscene/web --bridge take_screenshot
npx @midscene/web --bridge disconnect
```

## 故障排除

### Bridge模式连接失败
- 确保Chrome浏览器已打开，并且安装并启用了Midscene扩展程序。
- 检查扩展程序是否显示“已连接”状态。
- 请参阅[Bridge模式文档](https://midscenejs.com/bridge-mode-by-chrome-extension.html)以获取更多信息。

### API密钥错误
- 确保`.env`文件中包含`MIDSCENE_MODEL_API_KEY=<your-key>`。
- 验证该密钥是否适用于配置的模型提供者。

### 超时问题
- 网页可能需要一段时间才能加载。连接后，请先截取屏幕截图以确认页面已准备好再进行操作。
- 对于加载速度较慢的页面，请在步骤之间稍作等待。

### 屏幕截图无法显示
- 屏幕截图的路径是一个指向本地文件的绝对路径。可以使用Read工具来查看截图内容。